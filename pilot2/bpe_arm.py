"""The BPE cell of the tokenizer axis, on OUR backbone (the control DNABERT-2 cannot give).

    python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_ecoli.json --data ecoli --seed 0 --gpu 0
    python -m pilot2.bpe_arm --smoke

DNABERT-2 answers "does the BPE model memorise more than the k-mer models", but it also has
117M instead of 86-89M parameters, ALiBi instead of learned absolute positions, and a different
pretraining corpus, so it cannot isolate the tokenizer. This module trains the SAME 12.9M
Backbone as `run_pilot.py` (d512, 4 layers, 8 heads, pre-LN, tied embedding, absolute positions,
AR objective, identical optimiser and schedule) with a BPE vocabulary in place of the k-mer one,
so `char / 3mer / 6mer / bpe` differ in the tokenizer and nothing else.

Three differences from the k-mer cells are forced by BPE itself and are stated with the results:
  * tokens are variable length, so a window gives a variable number of tokens; sequences are
    right-padded with [PAD] and the objective is AR only (with a causal mask trailing pads cannot
    reach a real position; a bidirectional objective would leak through them, so MLM is left to
    `dnabert2.py`, where the native model provides an attention mask).
  * there is no exact per-nucleotide probability: every score is a token sum divided by the number
    of nucleotides those tokens cover (the convention of `dnabert2.py`).
  * the embedding table is larger (4096 x 512 vs 67 x 512 for the 3-mer); non-embedding parameters
    are identical, and `--emb_rank` / `--d_ff` from the capacity controls still apply.

Output schema matches `score.py`, with scorer key `ar/...`, so `analyze_traj.py` puts the BPE rows
straight into the matched-overfitting table next to char / 3mer / 6mer.
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
from .model import Backbone
from .real_data import DATA_PATHS, REAL_DATA, build_real_dataset

PAD, MASK, BOS = 0, 1, 2
LN2 = math.log(2.0)


class BpeTokenizer:
    """HF `tokenizers` BPE over {A,C,G,T}; ids 0/1/2 are [PAD]/[MASK]/[BOS] (see pilot2/train_bpe.py)."""

    def __init__(self, path: str | Path):
        from tokenizers import Tokenizer
        self.tok = Tokenizer.from_file(str(path))
        self.vocab_size = self.tok.get_vocab_size()
        self.pad_id, self.mask_id, self.bos_id = PAD, MASK, BOS
        self.id2str = {i: s for s, i in self.tok.get_vocab().items()}
        self.name = f"bpe{self.vocab_size}"
        self.path = str(path)

    def encode_str(self, s: str):
        e = self.tok.encode(s)
        return list(e.ids), [tuple(o) for o in e.offsets]

    def encode_nt(self, nt: np.ndarray):
        return self.encode_str(decode(nt))

    def batch(self, id_lists, device, bos=True, length=None):
        """-> (B, L) ids, [BOS] in front when asked, right-padded with [PAD]."""
        off = 1 if bos else 0
        L = length or (max(len(x) for x in id_lists) + off)
        out = torch.full((len(id_lists), L), PAD, dtype=torch.long)
        if bos:
            out[:, 0] = BOS
        for i, x in enumerate(id_lists):
            out[i, off:off + len(x)] = torch.tensor(x)
        return out.to(device)


# ---------------------------------------------------------------- scoring
@torch.no_grad()
def token_logprobs(model, voc: BpeTokenizer, id_lists, device, batch=128):
    """log2 p(token_t | tokens_<t) for every content token of every sequence."""
    out = []
    for b0 in range(0, len(id_lists), batch):
        chunk = id_lists[b0:b0 + batch]
        x = voc.batch(chunk, device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(x[:, :-1]).float()
        lp = torch.log_softmax(logits, -1)
        tgt = x[:, 1:]
        g = lp.gather(-1, tgt[..., None])[..., 0] / LN2
        for i, ids in enumerate(chunk):
            out.append(g[i, :len(ids)].cpu().numpy())
    return out


def _probe_tokens(spans, offset):
    idx = [t for t, (a, b) in enumerate(spans) if b > offset and a < offset + PROBE_LEN]
    cov = sum(spans[t][1] - spans[t][0] for t in idx)
    return idx, cov


def window_bits(model, voc, windows, device, offset=None):
    enc = [voc.encode_nt(w) for w in windows]
    lp = token_logprobs(model, voc, [e[0] for e in enc], device)
    bits, ntok = [], []
    for (ids, spans), l in zip(enc, lp):
        if offset is None:
            bits.append(-l.sum() / WINDOW); ntok.append(len(ids))
        else:
            sel, cov = _probe_tokens(spans, offset)
            bits.append(-l[sel].sum() / cov); ntok.append(len(sel))
    return np.array(bits), np.array(ntok)


def heldout_floor(model, voc, test_nt, device, n=500):
    bits, _ = window_bits(model, voc, list(test_nt[:n]), device)
    return {"scorer": "ar", "n_windows": int(len(bits)), "positions": WINDOW,
            "bits_per_nt_mean": float(bits.mean()), "bits_per_nt_std": float(bits.std()),
            "floor_ok": bool(bits.mean() >= 1.95)}


def rank_probe(model, voc, probe: Probe, host, pool, device, offset):
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, offset:offset + PROBE_LEN] = probe.seq
    win[1:, offset:offset + PROBE_LEN] = pool
    bits, ntok = window_bits(model, voc, list(win), device, offset)
    s = -bits * PROBE_LEN
    true, cands = s[0], s[1:]
    return {"rank": 1 + int((cands > true).sum()), "n_pool": n, "p_chance": (1 + int((cands > true).sum())) / (n + 1),
            "offset": int(offset), "positions": int(ntok[0]), "probe_bits_per_nt": float(bits[0]),
            "pool_bits_per_nt_mean": float(bits[1:].mean()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, voc, probe: Probe, host, device, offset, k_nt=48, max_len=None):
    """Reveal the tokens ending at or before offset+k_nt, then decode greedily to the probe end."""
    s = decode(np.concatenate([host[:offset], probe.seq, host[offset + PROBE_LEN:]]))
    ids, spans = voc.encode_str(s)
    start, end = offset + k_nt, offset + PROBE_LEN
    n_rev = sum(1 for a, b in spans if b <= start)
    revealed = spans[n_rev - 1][1] if n_rev else 0
    truth = s[revealed:end]
    cur = ids[:n_rev]
    gen = ""
    cap = (max_len or 160) - 2
    while len(gen) < len(truth) and len(cur) < cap:
        x = voc.batch([cur], device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg = model(x)[0, -1].float()
        lg[[PAD, MASK, BOS]] = float("-inf")
        t = int(lg.argmax())
        cur.append(t); gen += voc.id2str[t]
    pred = gen[:len(truth)]
    ham = sum(1 for a, b in zip(pred, truth) if a != b) + max(0, len(truth) - len(pred))
    return {"k_revealed_nt": int(revealed - offset), "offset": int(offset), "n_generated_nt": int(len(truth)),
            "exact": bool(ham == 0), "hamming_nt": int(ham)}


def score_run(model, voc, ds, device, pool_size, seed, floor_n=500, max_len=None):
    rng = np.random.default_rng(10_000 + seed)
    pool = random_dna(rng, pool_size, PROBE_LEN)
    fresh_hosts = {p.probe_id: random_dna(rng, 1, WINDOW)[0] for p in ds.probes}
    off_rng = np.random.default_rng(20_000 + seed)
    fresh_off = {p.probe_id: int(off_rng.integers(0, WINDOW - PROBE_LEN + 1)) for p in ds.probes}
    res = {"kind": "ar", "tokenizer": voc.name, "k": None, "vocab_file": voc.path, "pool_size": pool_size,
           "floors": [heldout_floor(model, voc, ds.test, device, floor_n)], "probes": []}
    for p in ds.probes:
        fo = fresh_off[p.probe_id]
        e = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {},
             "train_offsets": list(p.offsets), "fresh_offset": fo, "phase_match": None}
        hosts = {"fresh": (fresh_hosts[p.probe_id], fo)}
        if p.repetitions > 0:
            hosts["train"] = (ds.train[p.host_rows[0]], p.offsets[0] if p.offsets else PROBE_OFFSET)
        for hname, (host, off) in hosts.items():
            e["ranks"][f"ar/{hname}"] = rank_probe(model, voc, p, host, pool, device, off)
            e["extract"][hname] = extract_prefix(model, voc, p, host, device, off, max_len=max_len)
        res["probes"].append(e)
    return res


# ---------------------------------------------------------------- training
def train(model, voc, ds, device, out_dir: Path, epochs, batch, lr, seed, save_epochs, warmup=100,
          emb_lr_mult=1.0, max_len=None):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    enc = [voc.encode_nt(w)[0] for w in ds.train]
    val = [voc.encode_nt(w)[0] for w in ds.val]
    ntok = np.array([len(x) for x in enc])
    emb = [model.tok.weight]
    rest = [q for q in model.parameters() if q is not model.tok.weight]
    opt = torch.optim.AdamW([{"params": rest, "mult": 1.0}, {"params": emb, "mult": emb_lr_mult}],
                            lr=lr, betas=(0.9, 0.95), weight_decay=0.01)
    steps_per_epoch = math.ceil(len(enc) / batch)
    total = steps_per_epoch * epochs

    def lr_at(step):
        if step < warmup:
            return lr * (step + 1) / warmup
        t = (step - warmup) / max(1, total - warmup)
        return lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, t))))

    def batch_loss(id_lists):
        x = voc.batch(id_lists, device, length=max_len)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(x[:, :-1])
        return F.cross_entropy(logits.reshape(-1, logits.size(-1)).float(), x[:, 1:].reshape(-1), ignore_index=PAD)

    step, t0 = 0, time.time()
    log = open(out_dir / "train_log.jsonl", "w", encoding="utf-8")
    model.train()
    for ep in range(1, epochs + 1):
        order = rng.permutation(len(enc))
        tot, n = 0.0, 0
        for i in range(0, len(order), batch):
            for g in opt.param_groups:
                g["lr"] = lr_at(step) * g["mult"]
            loss = batch_loss([enc[j] for j in order[i:i + batch]])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tot += loss.item(); n += 1; step += 1
        model.eval()
        with torch.no_grad():
            vl = float(np.mean([batch_loss(val[i:i + 256]).item() for i in range(0, len(val), 256)]))
        model.train()
        rec = {"epoch": ep, "step": step, "train_loss": tot / max(1, n), "val_loss_nats": vl,
               "val_bits_per_token": vl / LN2, "sec": time.time() - t0}
        log.write(json.dumps(rec) + "\n"); log.flush()
        print(f"[{voc.name} s{seed}] epoch {ep}/{epochs} loss {rec['train_loss']:.4f} val {vl:.4f} ({rec['sec']:.0f}s)", flush=True)
        if ep in save_epochs:
            torch.save(model.state_dict(), out_dir / f"ep{ep}.pt")
    log.close()
    torch.save(model.state_dict(), out_dir / "final.pt")
    model.eval()
    return {"objective": "ar", "tokenizer": voc.name, "vocab_size": voc.vocab_size, "vocab_file": voc.path,
            "seed": seed, "epochs": epochs, "steps": step, "batch": batch, "lr": lr,
            "n_params": model.n_params(), "n_params_non_embedding": model.n_params(non_embedding=True),
            "tokens_per_window_mean": float(ntok.mean()), "tokens_per_window_max": int(ntok.max()),
            "k_nt_per_token": float(WINDOW / ntok.mean()), "total_train_sec": time.time() - t0}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vocab_file", default="data/tokenizers/bpe4096_ecoli.json")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/bpe_arm")
    ap.add_argument("--data", default="synthetic", choices=["synthetic", *REAL_DATA])
    ap.add_argument("--fasta", default=None)
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--n_val", type=int, default=500)
    ap.add_argument("--n_test", type=int, default=500)
    ap.add_argument("--probes_per_tier", type=int, default=50)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=50)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--pool", type=int, default=500)
    ap.add_argument("--floor_n", type=int, default=500)
    ap.add_argument("--d_ff", type=int, default=None)
    ap.add_argument("--emb_rank", type=int, default=None)
    ap.add_argument("--emb_lr_mult", type=float, default=1.0)
    ap.add_argument("--save_epochs", default="1,2,3,5,8,12,20,30")
    ap.add_argument("--keep_snapshots", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args(argv)
    if args.smoke:
        args.n_train, args.n_val, args.n_test = 300, 100, 100
        args.probes_per_tier, args.n_nonmember, args.epochs = 2, 2, 1
        args.pool, args.floor_n, args.save_epochs = 20, 50, "1"
        args.out = os.path.join(args.out, "smoke")
    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    voc = BpeTokenizer(args.vocab_file)
    tag = "" if args.data == "synthetic" else f"_{args.data}"
    name = f"{voc.name}{tag}_ar_s{args.seed}"
    out_dir = Path(args.out) / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")
    tiers = tuple(int(t) for t in args.tiers.split(","))
    if args.data != "synthetic":
        args.fasta = args.fasta or DATA_PATHS[args.data]
        ds = build_real_dataset(args.fasta, args.n_train, args.n_val, args.n_test, args.probes_per_tier, tiers,
                                args.n_nonmember, args.data_seed, offset_mode=args.probe_offset)
    else:
        ds = build_dataset(args.n_train, args.n_val, args.n_test, args.probes_per_tier, tiers, args.n_nonmember,
                           args.data_seed, offset_mode=args.probe_offset)
    ds.save_meta(out_dir / "data_meta.json")
    # one position per token slot: longest window in the data plus BOS, with headroom for extraction
    n_max = max(len(voc.encode_nt(w)[0]) for w in np.concatenate([ds.train, ds.val, ds.test])[:4000])
    max_len = n_max + 8
    model = Backbone(voc.vocab_size, max_len + 2, causal=True, d_ff=args.d_ff, emb_rank=args.emb_rank).to(device)
    print(f"[{name}] vocab {voc.vocab_size}, <= {n_max} tok/window ({WINDOW / n_max:.2f}+ nt/token), "
          f"{model.n_params() / 1e6:.2f}M params ({model.n_params(non_embedding=True) / 1e6:.2f}M non-emb)", flush=True)
    t0 = time.time()
    save_epochs = sorted(int(e) for e in args.save_epochs.split(",") if e)
    summary = train(model, voc, ds, device, out_dir, args.epochs, args.batch, args.lr, args.seed, save_epochs,
                    emb_lr_mult=args.emb_lr_mult, max_len=max_len + 1)
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    sc = score_run(model, voc, ds, device, args.pool, args.seed, args.floor_n, max_len)
    sc.update(train_summary=summary, epoch=args.epochs, checkpoint="final", score_sec=time.time() - t0)
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    (out_dir / f"scores_ep{args.epochs}.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(f"[{name}] final floor {sc['floors'][0]['bits_per_nt_mean']:.4f}", flush=True)
    for e in save_epochs:
        ck = out_dir / f"ep{e}.pt"
        if not ck.exists():
            continue
        if e == args.epochs:
            ck.unlink(); continue
        model.load_state_dict(torch.load(ck, map_location=device)); model.eval()
        t2 = time.time()
        s2 = score_run(model, voc, ds, device, args.pool, args.seed, args.floor_n, max_len)
        s2.update(train_summary=summary, epoch=e, checkpoint=f"ep{e}", score_sec=time.time() - t2)
        (out_dir / f"scores_ep{e}.json").write_text(json.dumps(s2, indent=1), encoding="utf-8")
        print(f"[{name}] snapshot ep{e}: floor {s2['floors'][0]['bits_per_nt_mean']:.4f} ({s2['score_sec']:.0f}s)", flush=True)
        if not args.keep_snapshots:
            ck.unlink()
    print(f"[{name}] done in {time.time() - t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
