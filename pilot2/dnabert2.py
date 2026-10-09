"""E4 arm (c), BPE member: DNABERT-2 (117M, BPE vocab 4096, ALiBi) on our planted-canary data.

    python -m pilot2.dnabert2 --objective causal --data ecoli --seed 0 --gpu 0 --out outputs/dnabert2_ecoli
    python -m pilot2.dnabert2 --smoke

Same data and the same score files as pilot2/dnabert.py (288-nt windows, probes at random
offsets, 100-sequence pool, 48-nt prefix extraction, held-out floor), so the numbers sit
next to the DNABERT 3/4/5/6-mer rows. Out dir: dnabert2bpe[_causal][_lr..][_<data>]_s<seed>.

BPE tokens are NON-overlapping and variable length (1-32 nt, median ~6), so there is no
exact per-nucleotide probability. Everything is scored per TOKEN and converted to bits per
nucleotide by dividing by the number of nucleotides the scored tokens cover:
  * probe score  = sum over tokens overlapping the probe span of -log2 p(token) / nt covered
  * floor        = same over all tokens of a held-out window (= whole window)
Objectives:
  mlm     native masked-LM head; training masks --mask_rate (15%) of tokens with [MASK]; scoring
          is pseudo-log-likelihood (one token masked at a time, bidirectional context).
  causal  next-token prediction with a causal mask folded into the ALiBi bias (upper triangle
          -1e4); scoring is one forward pass per window.
Extraction reveals the tokens that END at or before offset+48 (so the revealed prefix is <= 48
nt; the actual count is recorded), then decodes greedily token by token until the probe end.
For mlm the unknown region keeps the TOKEN LAYOUT of the true sequence (number and lengths
of masked slots), which the k-mer version also implicitly has; this is a mild advantage to
the model and is stated in the notes.

Triton flash attention is disabled (libcuda stub problem on the server); the module's PyTorch
attention path is used instead, which is exact.

Fine-tuning hyper-parameters as in pilot2/dnabert.py: AdamW, lr 2e-5, wd 0.01, 10% warm-up
then constant, effective batch 16, grad clip 1.0.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Probe, build_dataset, decode, random_dna
from .real_data import DATA_PATHS, REAL_DATA, build_real_dataset

MODEL_DIR = "/data/wh/yqdata/models/DNABERT2"
LN2 = math.log(2.0)


class BpeVocab:
    def __init__(self, model_dir: str):
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        t = self.tok
        self.pad, self.cls, self.sep, self.mask = t.pad_token_id, t.cls_token_id, t.sep_token_id, t.mask_token_id
        self.vocab_size = t.vocab_size
        self.id2str = {i: s for s, i in t.get_vocab().items()}
        self.k = "bpe"

    def encode_str(self, s: str):
        """-> (ids incl. [CLS]/[SEP], spans [(start, end)] of the content tokens in nt coordinates)."""
        e = self.tok(s, return_offsets_mapping=True, add_special_tokens=True)
        ids = e["input_ids"]
        spans = [tuple(o) for o in e["offset_mapping"][1:-1]]
        assert ids[0] == self.cls and ids[-1] == self.sep
        return ids, spans

    def encode_nt(self, nt: np.ndarray):
        return self.encode_str(decode(nt))

    def pad_batch(self, id_lists, device):
        L = max(len(x) for x in id_lists)
        ids = torch.full((len(id_lists), L), self.pad, dtype=torch.long)
        am = torch.zeros((len(id_lists), L), dtype=torch.long)
        for i, x in enumerate(id_lists):
            ids[i, :len(x)] = torch.tensor(x); am[i, :len(x)] = 1
        return ids.to(device), am.to(device)


def load_model(device, causal: bool):
    from transformers import AutoModelForMaskedLM
    model = AutoModelForMaskedLM.from_pretrained(MODEL_DIR, trust_remote_code=True)
    mod = sys.modules[type(model.bert.encoder.layer[0].attention.self).__module__]
    mod.flash_attn_qkvpacked_func = None          # force the exact PyTorch attention path
    if causal:
        enc = model.bert.encoder
        S = enc.alibi.shape[-1]
        enc.alibi = enc.alibi + torch.triu(torch.full((S, S), -10000.0), 1)[None, None]
        enc._pilot2_causal = True
    model = model.to(device)
    # ALiBi lives outside the state dict; rebuilding would drop the causal term, so windows must stay <= 512 tokens
    return model, BpeVocab(MODEL_DIR)


def _logits(model, ids, am):
    with torch.autocast("cuda", dtype=torch.bfloat16):
        return model(input_ids=ids, attention_mask=am).logits.float()


# ---------------------------------------------------------------- scoring
@torch.no_grad()
def token_logprobs_causal(model, voc, id_lists, device, batch=128):
    """Per content token t (index 1..T in ids): log2 p(ids[t] | ids[<t]) read from logits at t-1."""
    out = []
    for b0 in range(0, len(id_lists), batch):
        chunk = id_lists[b0:b0 + batch]
        ids, am = voc.pad_batch(chunk, device)
        lp = torch.log_softmax(_logits(model, ids, am), -1)
        for i, x in enumerate(chunk):
            T = len(x) - 2
            tgt = torch.tensor(x[1:T + 1], device=device)
            out.append((lp[i, torch.arange(T), tgt] / LN2).cpu().numpy())
    return out


@torch.no_grad()
def token_logprobs_pll(model, voc, id_lists, device, which=None, rows_per_batch=256):
    """Per content token: log2 p(token | all other tokens), masking one at a time.
    which: optional list (per sequence) of content-token indices (0-based) to score; default all."""
    jobs = []  # (seq idx, token idx, masked ids)
    for i, x in enumerate(id_lists):
        T = len(x) - 2
        for t in (range(T) if which is None else which[i]):
            m = list(x); m[t + 1] = voc.mask
            jobs.append((i, t, m))
    res = [dict() for _ in id_lists]
    for b0 in range(0, len(jobs), rows_per_batch):
        chunk = jobs[b0:b0 + rows_per_batch]
        ids, am = voc.pad_batch([j[2] for j in chunk], device)
        lp = torch.log_softmax(_logits(model, ids, am), -1)
        for r, (i, t, _) in enumerate(chunk):
            res[i][t] = float(lp[r, t + 1, id_lists[i][t + 1]]) / LN2
    return [np.array([d[t] for t in sorted(d)]) for d in res]


def _probe_tokens(spans, offset):
    """indices of content tokens overlapping [offset, offset+PROBE_LEN), and the nt they cover."""
    idx = [t for t, (a, b) in enumerate(spans) if b > offset and a < offset + PROBE_LEN]
    cov = sum(spans[t][1] - spans[t][0] for t in idx)
    return idx, cov


def window_bits(model, voc, windows: list[np.ndarray], device, objective, offset=None):
    """bits/nt over the probe span (offset given) or the whole window (offset None) for each window."""
    enc = [voc.encode_nt(w) for w in windows]
    id_lists = [e[0] for e in enc]
    if offset is None:
        which = [list(range(len(x) - 2)) for x in id_lists]
        cov = [WINDOW] * len(windows)
    else:
        sel = [_probe_tokens(e[1], offset) for e in enc]
        which, cov = [s[0] for s in sel], [s[1] for s in sel]
    if objective == "causal":
        lp = token_logprobs_causal(model, voc, id_lists, device)
        tot = [-(l[w].sum()) for l, w in zip(lp, which)]
    else:
        lp = token_logprobs_pll(model, voc, id_lists, device, which)
        tot = [-(l.sum()) for l in lp]
    return np.array(tot) / np.array(cov), np.array([len(w) for w in which])


def heldout_floor(model, voc, test_nt, device, n=200, objective="mlm"):
    bits, _ = window_bits(model, voc, list(test_nt[:n]), device, objective)
    return {"scorer": "causal" if objective == "causal" else "token_pll", "n_windows": int(len(bits)), "positions": WINDOW,
            "bits_per_nt_mean": float(bits.mean()), "bits_per_nt_std": float(bits.std()), "floor_ok": bool(bits.mean() >= 1.95)}


def rank_probe(model, voc, probe: Probe, host, pool, device, offset, objective):
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, offset:offset + PROBE_LEN] = probe.seq
    win[1:, offset:offset + PROBE_LEN] = pool
    bits, ntok = window_bits(model, voc, list(win), device, objective, offset)
    s = -bits * PROBE_LEN                       # total bits over the probe span, sign as in dnabert.py (higher = more likely)
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1), "offset": int(offset), "positions": int(ntok[0]),
            "probe_bits_per_nt": float(bits[0]), "pool_bits_per_nt_mean": float(bits[1:].mean()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, voc, probe: Probe, host, device, offset, objective, k_nt=48):
    start, end = offset + k_nt, offset + PROBE_LEN
    win = host.copy(); win[offset:offset + PROBE_LEN] = probe.seq
    s = decode(win)
    ids, spans = voc.encode_str(s)
    n_rev = sum(1 for a, b in spans if b <= start)          # tokens fully inside the revealed prefix
    revealed = spans[n_rev - 1][1] if n_rev else 0
    truth = s[revealed:end]
    if objective == "causal":
        cur = ids[:n_rev + 1]                                 # [CLS] + revealed tokens, no [SEP]
        gen = ""
        while len(gen) < len(truth) and len(cur) < 512:
            x = torch.tensor([cur], device=device)
            lg = _logits(model, x, torch.ones_like(x))[0, -1]
            lg[[voc.pad, voc.cls, voc.sep, voc.mask, 0]] = float("-inf")
            t = int(lg.argmax()); cur.append(t); gen += voc.id2str[t]
    else:
        cur = list(ids)
        for t in range(n_rev, len(spans)):                    # everything right of the prefix is unknown (as in dnabert.py)
            cur[t + 1] = voc.mask
        last = max(t for t, (a, b) in enumerate(spans) if a < end)
        for t in range(n_rev, last + 1):                      # left to right, one slot at a time
            x = torch.tensor([cur], device=device)
            lg = _logits(model, x, torch.ones_like(x))[0, t + 1]
            lg[[voc.pad, voc.cls, voc.sep, voc.mask, 0]] = float("-inf")
            cur[t + 1] = int(lg.argmax())
        gen = "".join(voc.id2str[cur[t + 1]] for t in range(n_rev, last + 1))
    pred = gen[:len(truth)]
    ham = sum(1 for a, b in zip(pred, truth) if a != b) + max(0, len(truth) - len(pred))
    return {"k_revealed_nt": int(revealed - offset), "offset": int(offset), "n_generated_nt": int(len(truth)),
            "exact": bool(ham == 0), "hamming_nt": int(ham), "pred_nt": pred, "truth_nt": truth}


def score_run(model, voc, ds, device, pool_size, seed, probes_per_tier=None, floor_n=200, objective="mlm"):
    rng = np.random.default_rng(10_000 + seed)
    pool = random_dna(rng, pool_size, PROBE_LEN)
    fresh_hosts = {p.probe_id: random_dna(rng, 1, WINDOW)[0] for p in ds.probes}
    off_rng = np.random.default_rng(20_000 + seed)
    fresh_off = {p.probe_id: int(off_rng.integers(0, WINDOW - PROBE_LEN + 1)) for p in ds.probes}
    probes = ds.probes
    if probes_per_tier:
        keep, seen = [], {}
        for p in probes:
            if seen.get(p.repetitions, 0) < probes_per_tier:
                keep.append(p); seen[p.repetitions] = seen.get(p.repetitions, 0) + 1
        probes = keep
    sc = "causal" if objective == "causal" else "span_pll"      # same key as dnabert.py so analyze_dnabert reads it
    res = {"kind": "dnabert2", "k": "bpe", "objective": objective, "pool_size": pool_size, "stride": 1,
           "floors": [heldout_floor(model, voc, ds.test, device, floor_n, objective=objective)], "probes": []}
    for p in probes:
        fo = fresh_off[p.probe_id]
        e = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {},
             "train_offsets": list(p.offsets), "fresh_offset": fo}
        hosts = {"fresh": (fresh_hosts[p.probe_id], fo)}
        if p.repetitions > 0:
            hosts["train"] = (ds.train[p.host_rows[0]], p.offsets[0] if p.offsets else PROBE_OFFSET)
        for hname, (host, off) in hosts.items():
            e["ranks"][f"{sc}/{hname}"] = rank_probe(model, voc, p, host, pool, device, off, objective)
            e["extract"][hname] = extract_prefix(model, voc, p, host, device, off, objective)
        res["probes"].append(e)
    return res


# ---------------------------------------------------------------- training
def mlm_loss(model, voc, ids, am, rate, gen):
    content = am.bool().clone(); content[:, 0] = False
    content &= ids != voc.sep
    m = (torch.rand(ids.shape, generator=gen, device=ids.device) < rate) & content
    labels = torch.where(m, ids, torch.full_like(ids, -100))
    x = ids.clone(); x[m] = voc.mask
    with torch.autocast("cuda", dtype=torch.bfloat16):
        logits = model(input_ids=x, attention_mask=am).logits
    return F.cross_entropy(logits.float().reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100)


def causal_loss(model, voc, ids, am):
    labels = ids[:, 1:].clone()
    labels[(labels == voc.sep) | (labels == voc.pad)] = -100
    with torch.autocast("cuda", dtype=torch.bfloat16):
        logits = model(input_ids=ids, attention_mask=am).logits[:, :-1]
    return F.cross_entropy(logits.float().reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100)


def train(model, voc, ds, device, out_dir: Path, epochs, lr, batch, accum, mask_rate, seed, save_epochs, log, objective):
    torch.manual_seed(seed)
    gen = torch.Generator(device=device).manual_seed(seed)
    rng = np.random.default_rng(seed)
    enc = [voc.encode_nt(w)[0] for w in ds.train]           # fixed tokenisation of the training windows
    ntok = np.array([len(x) - 2 for x in enc])
    steps_per_epoch = math.ceil(len(enc) / batch / accum)
    total = steps_per_epoch * epochs
    warm = int(0.1 * total)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    lr_at = lambda s: lr * (0.1 + 0.9 * (s + 1) / max(1, warm)) if s < warm else lr
    step, t0 = 0, time.time()
    model.train()
    for ep in range(1, epochs + 1):
        order = rng.permutation(len(enc))
        tot, n = 0.0, 0
        for i in range(0, len(order), batch * accum):
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            opt.zero_grad(set_to_none=True)
            for a in range(accum):
                idx = order[i + a * batch:i + (a + 1) * batch]
                if len(idx) == 0:
                    continue
                ids, am = voc.pad_batch([enc[j] for j in idx], device)
                loss = causal_loss(model, voc, ids, am) if objective == "causal" else mlm_loss(model, voc, ids, am, mask_rate, gen)
                (loss / accum).backward()
                tot += loss.item(); n += 1
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); step += 1
        log.write(json.dumps({"epoch": ep, "train_loss": tot / max(1, n), "lr": lr_at(step), "sec": time.time() - t0}) + "\n")
        log.flush()
        print(f"[bpe s{seed}] epoch {ep}/{epochs} loss {tot / max(1, n):.4f} ({time.time() - t0:.0f}s)", flush=True)
        if ep in save_epochs:
            torch.save(model.state_dict(), out_dir / f"ep{ep}.pt")
    model.eval()
    return {"epochs": epochs, "steps": step, "lr": lr, "batch": batch * accum, "mask_rate": mask_rate, "objective": objective,
            "train_sec": time.time() - t0, "n_params": sum(p.numel() for p in model.parameters()),
            "tokens_per_window_mean": float(ntok.mean()), "tokens_per_window_max": int(ntok.max())}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/dnabert2")
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--data", default="synthetic", choices=["synthetic", *REAL_DATA])
    ap.add_argument("--fasta", default=None, help="override the default path of --data")
    ap.add_argument("--canary_npz", default=None, help="real-canary pool from pilot2.human_canary (default: iid uniform 96-mers)")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--objective", default="mlm", choices=["mlm", "causal"])
    ap.add_argument("--mask_rate", type=float, default=0.15, help="mlm: fraction of TOKENS masked")
    ap.add_argument("--pool", type=int, default=100)
    ap.add_argument("--save_epochs", default="1,3,8,15,30")
    ap.add_argument("--snapshot_probes", type=int, default=10)
    ap.add_argument("--score_epoch0", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--downstream", action="store_true", help="GUE promoter probe (linear + fine-tune) at every scored snapshot")
    ap.add_argument("--downstream_tasks", default=None, help="comma list of GUE tasks; default by --data (gue: prom_300_all; yeast: emp_H3,emp_H3K4me3)")
    args = ap.parse_args(argv)
    if args.smoke:
        args.n_train, args.probes_per_tier, args.n_nonmember = 200, 2, 2
        args.epochs, args.pool, args.save_epochs, args.snapshot_probes = 1, 10, "1", 2
        args.out = os.path.join(args.out, "smoke")
    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    tag = "_causal" if args.objective == "causal" else ""
    if args.lr != 2e-5:
        tag += f"_lr{args.lr:g}"
    if args.data != "synthetic":
        tag += f"_{args.data}"
    out_dir = Path(args.out) / f"dnabert2bpe{tag}_s{args.seed}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")
    tiers = tuple(int(t) for t in args.tiers.split(","))
    if args.data != "synthetic":
        args.fasta = args.fasta or DATA_PATHS[args.data]
        ds = build_real_dataset(args.fasta, args.n_train, 200, 200, args.probes_per_tier, tiers, args.n_nonmember,
                                args.data_seed, offset_mode=args.probe_offset,
                                canary_npz=args.canary_npz)
    else:
        ds = build_dataset(args.n_train, 200, 200, args.probes_per_tier, tiers, args.n_nonmember, args.data_seed,
                           offset_mode=args.probe_offset)
    ds.save_meta(out_dir / "data_meta.json")
    model, voc = load_model(device, causal=args.objective == "causal")
    save_epochs = sorted(int(e) for e in args.save_epochs.split(",") if e)
    t0 = time.time()
    obj = args.objective
    DS_TASKS = tuple(t for t in (args.downstream_tasks.split(",") if args.downstream_tasks else
                     __import__("pilot2.downstream", fromlist=["DEFAULT_TASKS"]).DEFAULT_TASKS.get(args.data, [])) if t)
    if args.downstream and not DS_TASKS:
        raise SystemExit("--downstream needs --downstream_tasks for data=" + args.data)
    DS = lambda m: __import__("pilot2.downstream", fromlist=["evaluate"]).evaluate("bpe", m, voc, device, causal=args.objective == "causal", seed=args.seed, tasks=DS_TASKS) if args.downstream else None
    if args.score_epoch0:
        model.eval()
        sc = score_run(model, voc, ds, device, args.pool, args.seed, args.snapshot_probes, objective=obj)
        sc.update(epoch=0, score_sec=time.time() - t0)
        sc["downstream"] = DS(model)
        (out_dir / "scores_ep0.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
        print(f"[bpe s{args.seed}] ep0 floor {sc['floors'][0]['bits_per_nt_mean']:.3f} ({sc['score_sec']:.0f}s)", flush=True)
    with open(out_dir / "train_log.jsonl", "w", encoding="utf-8") as log:
        summary = train(model, voc, ds, device, out_dir, args.epochs, args.lr, args.batch, args.accum, args.mask_rate,
                        args.seed, save_epochs, log, obj)
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    t1 = time.time()
    sc = score_run(model, voc, ds, device, args.pool, args.seed, objective=obj)
    sc.update(train_summary=summary, epoch=args.epochs, score_sec=time.time() - t1, checkpoint="final")
    sc["downstream"] = DS(model)
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(f"[bpe s{args.seed}] final floor {sc['floors'][0]['bits_per_nt_mean']:.3f} ({sc['score_sec']:.0f}s)", flush=True)
    for e in save_epochs:
        ck = out_dir / f"ep{e}.pt"
        if not ck.exists() or e == args.epochs:
            if ck.exists():
                ck.unlink()
            continue
        model.load_state_dict(torch.load(ck, map_location=device)); model.eval()
        t2 = time.time()
        s2 = score_run(model, voc, ds, device, args.pool, args.seed, args.snapshot_probes, objective=obj)
        s2.update(epoch=e, score_sec=time.time() - t2, checkpoint=f"ep{e}")
        s2["downstream"] = DS(model)
        (out_dir / f"scores_ep{e}.json").write_text(json.dumps(s2, indent=1), encoding="utf-8")
        print(f"[bpe s{args.seed}] ep{e} floor {s2['floors'][0]['bits_per_nt_mean']:.3f} ({s2['score_sec']:.0f}s)", flush=True)
        ck.unlink()
    print(f"[bpe s{args.seed}] done in {time.time() - t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
