"""E4 arm (c): the DNABERT k-mer family (3/4/5/6-mer) on our planted-canary data.

    python -m pilot2.dnabert --k 6 --seed 0 --gpu 0 --out outputs/dnabert
    python -m pilot2.dnabert --k 6 --smoke

Same data as pilot2 (288-nt windows, probes at random offsets by default), so the
numbers are comparable with the from-scratch grid. Differences from the published
pipeline (PLM-Memorization): the NATIVE masked-LM head is used (no causal head is
added), checkpoints are scored at fixed epochs (no early stopping), and every
score is per nucleotide.

DNABERT tokenizes with OVERLAPPING k-mers (stride 1): token t = nt[t : t+k], so a
window of W nt has W-k+1 tokens, and nucleotide j is covered by tokens
j-k+1 .. j. Hiding one nucleotide therefore means masking a span of k tokens
(as in DNABERT pretraining); predicting it means reading the token whose k-mer
STARTS at j and keeping only the k-mers whose remaining k-1 letters agree with the
still-visible neighbours.

Two objectives:
  mlm     native masked-LM head, DNABERT-style span masking. --mask_rate is the TOKEN
          rate (15% as in pretraining); --mask_nt_rate instead fixes the rate of HIDDEN
          NUCLEOTIDES (token rate = k x nt rate), which makes the pressure comparable
          across k: at a 15% token rate a 6-mer model hides only ~2.5% of nucleotides.
  causal  next-token prediction with a causal attention mask on the encoder (the
          published pipeline's objective, but without the bidirectional leak and
          without a new head). With overlapping k-mers the next token adds exactly
          one nucleotide, so this is nucleotide-level AR over k-mer embeddings and
          per-nt scoring is exact: p(nt_j | prefix) = p(token_{j-k+1} | prefix)
          restricted to the four k-mers consistent with the k-1 known letters.

Fine-tuning hyper-parameters follow the published configs: AdamW, lr 2e-5,
weight decay 0.01, 10% linear warm-up then constant, effective batch 16, grad clip 1.0.
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

NT = "ACGT"                       # pilot2 nt ids: A=1, C=2, G=3, T=4
MODEL_ROOT = "/data/wh/yqdata/models/DNABERT"


class KmerVocab:
    """DNABERT vocab: specials + all 4^k k-mers; maps nt-id windows to token ids."""

    def __init__(self, model_dir: Path, k: int):
        toks = [l.rstrip("\n") for l in open(model_dir / "vocab.txt", encoding="utf-8")]
        self.k = k
        self.id = {t: i for i, t in enumerate(toks)}
        self.pad, self.cls, self.sep, self.mask = (self.id[s] for s in ("[PAD]", "[CLS]", "[SEP]", "[MASK]"))
        kmers = [t for t in toks if len(t) == k and set(t) <= set(NT)]
        assert len(kmers) == 4 ** k, (len(kmers), k)
        self.kmer_ids = torch.tensor([self.id[m] for m in kmers])                      # (4^k,)
        self.letters = torch.tensor([[NT.index(c) + 1 for c in m] for m in kmers])    # (4^k, k) nt ids
        # lookup: nt-id k-tuple -> token id, via base-4 index into a table
        table = torch.zeros(4 ** k, dtype=torch.long)
        pw = 4 ** torch.arange(k - 1, -1, -1)
        table[((self.letters - 1) * pw).sum(1)] = self.kmer_ids
        self.table, self.pw = table, pw

    def encode(self, nt: torch.Tensor) -> torch.Tensor:
        """(B, W) nt ids -> (B, W-k+1+2) token ids with [CLS] ... [SEP]."""
        B, W = nt.shape
        win = nt.unfold(1, self.k, 1) - 1                                               # (B, W-k+1, k)
        ids = self.table.to(nt.device)[(win * self.pw.to(nt.device)).sum(-1)]
        cls = torch.full((B, 1), self.cls, dtype=torch.long, device=nt.device)
        sep = torch.full((B, 1), self.sep, dtype=torch.long, device=nt.device)
        return torch.cat([cls, ids, sep], 1)

    def n_tokens(self, W: int) -> int:
        return W - self.k + 1


def load_model(k: int, device):
    from transformers import AutoModelForMaskedLM
    d = Path(MODEL_ROOT) / f"DNA_bert_{k}"
    model = AutoModelForMaskedLM.from_pretrained(d, trust_remote_code=True).to(device)
    return model, KmerVocab(d, k)


@torch.no_grad()
def nt_logprobs(model, voc: KmerVocab, nt: torch.Tensor, positions, device, rows_per_batch=256):
    """log2 p(nt_j | everything except the k tokens covering j), for each window and each j in positions.

    nt: (B, W) nt ids. Returns (B, P) log2-probabilities of the TRUE nucleotide.
    For each (window, j): mask tokens j-k+1..j (clipped to the token range), read the
    logits of token t0 = j (the k-mer starting at j; if j > W-k, the last token, which
    then has j inside it), restrict to k-mers consistent with the visible nucleotides
    inside that token, marginalise onto the letter at j's offset, normalise over ACGT.
    """
    k, B, W = voc.k, nt.shape[0], nt.shape[1]
    T = voc.n_tokens(W)
    ids = voc.encode(nt).to(device)                                                   # (B, T+2)
    P = len(positions)
    letters = voc.letters.to(device)
    kmer_ids = voc.kmer_ids.to(device)
    out = torch.empty(B, P, device=device)
    wpb = max(1, rows_per_batch // P)
    for b0 in range(0, B, wpb):
        xb = ids[b0:b0 + wpb]
        w = xb.shape[0]
        rep = xb[:, None, :].expand(w, P, -1).clone()                                  # (w, P, T+2)
        tread = []
        for pi, j in enumerate(positions):
            lo, hi = max(0, j - k + 1), min(j, T - 1)                                  # tokens covering nt j
            rep[:, pi, lo + 1:hi + 2] = voc.mask                                         # +1 for [CLS]
            tread.append(min(j, T - 1))
        tread = torch.tensor(tread, device=device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(input_ids=rep.reshape(w * P, -1)).logits.float()
        logits = logits.reshape(w, P, -1, logits.shape[-1])
        at = logits[torch.arange(w)[:, None], torch.arange(P)[None, :], tread[None, :] + 1]   # (w, P, V)
        lk = at[..., kmer_ids]                                                          # (w, P, 4^k)
        ntb = nt[b0:b0 + wpb].to(device)
        for pi, j in enumerate(positions):
            t0 = int(tread[pi])
            off = j - t0                                                                # letter index of j inside token t0
            # visible nucleotides inside token t0: all of t0's letters except those hidden by the mask
            # (the mask hides tokens lo..hi, i.e. nucleotides that are covered ONLY by masked tokens: just j)
            cons = torch.ones(w, 4 ** k, dtype=torch.bool, device=device)
            for i in range(k):
                if i == off:
                    continue
                cons &= letters[:, i][None, :] == ntb[:, t0 + i, None]
            lp = lk[:, pi].masked_fill(~cons, float("-inf"))
            # marginalise onto the letter at `off`, then normalise over the four letters
            m = torch.full((w, 4), float("-inf"), device=device)
            for a in range(4):
                sel = letters[:, off] == a + 1
                m[:, a] = torch.logsumexp(lp[:, sel], dim=1)
            m = m - torch.logsumexp(m, dim=1, keepdim=True)
            out[b0:b0 + w, pi] = m[torch.arange(w), ntb[:, j] - 1] / math.log(2.0)
    return out


def heldout_floor(model, voc, test_nt: np.ndarray, device, n=200, stride=7, objective="mlm"):
    x = torch.from_numpy(test_nt[:n])
    pos = list(range(voc.k, WINDOW - voc.k, stride))
    f = nt_logprobs_causal if objective == "causal" else nt_logprobs
    bits = (-f(model, voc, x, pos, device)).mean(1).cpu().numpy()
    return {"scorer": "causal" if objective == "causal" else "span_pll", "n_windows": int(len(bits)), "positions": len(pos),
            "bits_per_nt_mean": float(bits.mean()), "bits_per_nt_std": float(bits.std()),
            "floor_ok": bool(bits.mean() >= 1.95)}


def rank_probe(model, voc, probe: Probe, host: np.ndarray, pool: np.ndarray, device, offset: int, stride: int,
               objective="mlm"):
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, offset:offset + PROBE_LEN] = probe.seq
    win[1:, offset:offset + PROBE_LEN] = pool
    pos = [j for j in range(offset, offset + PROBE_LEN, stride) if objective != "causal" or j >= voc.k - 1]
    f = nt_logprobs_causal if objective == "causal" else nt_logprobs
    s = f(model, voc, torch.from_numpy(win), pos, device).sum(1).cpu().numpy()
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1), "offset": int(offset), "positions": len(pos),
            "probe_bits_per_nt": float(-true / len(pos)), "pool_bits_per_nt_mean": float((-cands / len(pos)).mean()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, voc, probe: Probe, host: np.ndarray, device, offset: int, k_nt: int = 48):
    """Reveal everything before offset+k_nt; recover the remaining probe nucleotides left to right.

    All tokens covering any unknown nucleotide are masked. At step j the token starting at
    j-k+1 has k-1 known letters and one unknown (j); its restricted argmax gives nt_j, and
    that token is then unmasked. Host nucleotides after the probe are treated as unknown too
    (masked), matching the AR extraction where nothing to the right is visible.
    """
    k = voc.k
    start, end = offset + k_nt, offset + PROBE_LEN
    win = host.copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    truth = win[start:end].copy()
    cur = torch.from_numpy(win)[None]                                                   # (1, W)
    ids = voc.encode(cur).to(device)
    T = voc.n_tokens(WINDOW)
    first_unknown_tok = max(0, start - k + 1)
    ids[0, first_unknown_tok + 1:T + 1] = voc.mask
    letters = voc.letters.to(device)
    kmer_ids = voc.kmer_ids.to(device)
    pred = []
    for j in range(start, end):
        t0 = j - k + 1                                                                  # token whose last letter is j
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg = model(input_ids=ids).logits[0, t0 + 1].float()[kmer_ids]
        cons = torch.ones(4 ** k, dtype=torch.bool, device=device)
        for i in range(k - 1):                                                          # letters t0..j-1 are known
            cons &= letters[:, i] == int(cur[0, t0 + i])
        a = int(letters[lg.masked_fill(~cons, float("-inf")).argmax(), k - 1])
        cur[0, j] = a
        pred.append(a)
        ids[0, t0 + 1] = voc.table.to(device)[((cur[0, t0:t0 + k].to(device) - 1) * voc.pw.to(device)).sum()]
    pred = np.array(pred)
    ham = int((pred != truth).sum())
    return {"k_revealed_nt": k_nt, "offset": int(offset), "n_generated_nt": int(end - start),
            "exact": bool(ham == 0), "hamming_nt": ham, "pred_nt": decode(pred), "truth_nt": decode(truth)}



def causal_attention_mask(B: int, L: int, device) -> torch.Tensor:
    """(B, L, L) 1/0 mask: position i may attend to j <= i. HF BERT accepts a 3-D attention_mask."""
    return torch.tril(torch.ones(L, L, device=device)).expand(B, L, L).contiguous()


@torch.no_grad()
def nt_logprobs_causal(model, voc: KmerVocab, nt: torch.Tensor, positions, device, batch=64):
    """Causal model: log2 p(nt_j | nt_<j) read from the token that introduces nt j (token j-k+1).

    Positions j < k-1 are not scorable (they sit inside the first token) and are skipped."""
    k = voc.k
    ids = voc.encode(nt).to(device)
    B, L = ids.shape
    letters = voc.letters.to(device)
    kmer_ids = voc.kmer_ids.to(device)
    pos = [j for j in positions if j >= k - 1]
    tok = torch.tensor([j - k + 1 for j in pos], device=device)        # token index whose last letter is j
    out = torch.empty(B, len(pos), device=device)
    ntd = nt.to(device)
    for b0 in range(0, B, batch):
        xb = ids[b0:b0 + batch]
        w = xb.shape[0]
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(input_ids=xb, attention_mask=causal_attention_mask(w, L, device)).logits.float()
        # logits at ids-index t predict ids-index t+1; token tok sits at ids-index tok+1, so read index tok
        at = logits[torch.arange(w)[:, None], tok[None, :]]                  # (w, P, V)
        lk = at[..., kmer_ids]                                                # (w, P, 4^k)
        for pi, j in enumerate(pos):
            t0 = j - k + 1
            cons = torch.ones(w, 4 ** k, dtype=torch.bool, device=device)
            for i in range(k - 1):
                cons &= letters[:, i][None, :] == ntd[b0:b0 + w, t0 + i, None]
            lp = lk[:, pi].masked_fill(~cons, float("-inf"))
            lp = lp - torch.logsumexp(lp, dim=1, keepdim=True)              # normalise over the 4 consistent k-mers
            true_tok = ((ntd[b0:b0 + w, t0:t0 + k] - 1) * voc.pw.to(device)).sum(1)
            # index of the true k-mer in kmer order
            idx = torch.searchsorted(voc.kmer_ids.to(device), voc.table.to(device)[true_tok])
            out[b0:b0 + w, pi] = lp[torch.arange(w), idx] / math.log(2.0)
    return out


@torch.no_grad()
def extract_prefix_causal(model, voc: KmerVocab, probe: Probe, host: np.ndarray, device, offset: int, k_nt: int = 48):
    """Greedy nucleotide-by-nucleotide continuation from host[:offset+k_nt] (nothing to the right is used)."""
    k = voc.k
    start, end = offset + k_nt, offset + PROBE_LEN
    win = host.copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    truth = win[start:end].copy()
    cur = torch.from_numpy(win)[None].clone()
    letters = voc.letters.to(device)
    kmer_ids = voc.kmer_ids.to(device)
    pred = []
    for j in range(start, end):
        t0 = j - k + 1
        ids = voc.encode(cur[:, :j]).to(device)[:, :-1]                    # [CLS] + tokens 0..t0-1 (no [SEP])
        L = ids.shape[1]
        with torch.autocast("cuda", dtype=torch.bfloat16):
            lg = model(input_ids=ids, attention_mask=causal_attention_mask(1, L, device)).logits[0, -1].float()[kmer_ids]
        cons = torch.ones(4 ** k, dtype=torch.bool, device=device)
        for i in range(k - 1):
            cons &= letters[:, i] == int(cur[0, t0 + i])
        a = int(letters[lg.masked_fill(~cons, float("-inf")).argmax(), k - 1])
        cur[0, j] = a
        pred.append(a)
    pred = np.array(pred)
    ham = int((pred != truth).sum())
    return {"k_revealed_nt": k_nt, "offset": int(offset), "n_generated_nt": int(end - start),
            "exact": bool(ham == 0), "hamming_nt": ham, "pred_nt": decode(pred), "truth_nt": decode(truth)}


def score_run(model, voc, ds, device, pool_size, seed, stride, probes_per_tier=None, floor_n=200, objective="mlm"):
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
    sc = "causal" if objective == "causal" else "span_pll"
    res = {"kind": "dnabert", "k": voc.k, "objective": objective, "pool_size": pool_size, "stride": stride,
           "floors": [heldout_floor(model, voc, ds.test, device, floor_n, objective=objective)], "probes": []}
    for p in probes:
        fo = fresh_off[p.probe_id]
        e = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {},
             "train_offsets": list(p.offsets), "fresh_offset": fo}
        hosts = {"fresh": (fresh_hosts[p.probe_id], fo)}
        if p.repetitions > 0:
            hosts["train"] = (ds.train[p.host_rows[0]], p.offsets[0] if p.offsets else PROBE_OFFSET)
        for hname, (host, off) in hosts.items():
            e["ranks"][f"{sc}/{hname}"] = rank_probe(model, voc, p, host, pool, device, off, stride, objective)
            e["extract"][hname] = (extract_prefix_causal if objective == "causal" else extract_prefix)(model, voc, p, host, device, off)
        res["probes"].append(e)
    return res


def span_mask(ids: torch.Tensor, voc: KmerVocab, rate: float, gen) -> tuple[torch.Tensor, torch.Tensor]:
    """DNABERT-style masking: spans of k consecutive tokens, ~rate of tokens masked. Returns (input, labels)."""
    B, L = ids.shape
    k = voc.k
    T = L - 2
    starts = torch.rand(B, T, generator=gen, device=ids.device) < rate / k
    m = torch.zeros(B, T, dtype=torch.bool, device=ids.device)
    for i in range(k):
        m[:, i:] |= starts[:, :T - i]
    full = torch.zeros(B, L, dtype=torch.bool, device=ids.device)
    full[:, 1:T + 1] = m
    labels = torch.where(full, ids, torch.full_like(ids, -100))
    x = ids.clone()
    x[full] = voc.mask
    return x, labels


def causal_loss(model, voc, ids):
    """Next-token loss over all content tokens (predict tokens 0..T-1 from [CLS] + their prefix)."""
    B, L = ids.shape
    labels = ids[:, 1:].clone()
    labels[labels == voc.sep] = -100
    with torch.autocast("cuda", dtype=torch.bfloat16):
        logits = model(input_ids=ids, attention_mask=causal_attention_mask(B, L, ids.device)).logits[:, :-1]
    return F.cross_entropy(logits.float().reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100)


def train(model, voc, ds, device, out_dir: Path, epochs, lr, batch, accum, mask_rate, seed, save_epochs, log,
          objective="mlm"):
    torch.manual_seed(seed)
    gen = torch.Generator(device=device).manual_seed(seed)
    rng = np.random.default_rng(seed)
    train_nt = torch.from_numpy(ds.train)
    steps_per_epoch = math.ceil(len(train_nt) / batch / accum)
    total = steps_per_epoch * epochs
    warm = int(0.1 * total)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    lr_at = lambda s: lr * (0.1 + 0.9 * (s + 1) / max(1, warm)) if s < warm else lr   # published: LinearLR warm-up 0.1->1, then constant
    step, t0 = 0, time.time()
    model.train()
    for ep in range(1, epochs + 1):
        order = rng.permutation(len(train_nt))
        tot, n = 0.0, 0
        for i in range(0, len(order), batch * accum):
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            opt.zero_grad(set_to_none=True)
            for a in range(accum):
                idx = order[i + a * batch:i + (a + 1) * batch]
                if len(idx) == 0:
                    continue
                ids = voc.encode(train_nt[torch.as_tensor(idx)].to(device))
                if objective == "causal":
                    loss = causal_loss(model, voc, ids)
                else:
                    x, y = span_mask(ids, voc, mask_rate, gen)
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        loss = model(input_ids=x, labels=y).loss
                (loss / accum).backward()
                tot += loss.item(); n += 1
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); step += 1
        log.write(json.dumps({"epoch": ep, "train_loss": tot / max(1, n), "lr": lr_at(step), "sec": time.time() - t0}) + "\n")
        log.flush()
        print(f"[k={voc.k} s{seed}] epoch {ep}/{epochs} loss {tot / max(1, n):.4f} ({time.time() - t0:.0f}s)", flush=True)
        if ep in save_epochs:
            torch.save(model.state_dict(), out_dir / f"ep{ep}.pt")
    model.eval()
    return {"epochs": epochs, "steps": step, "lr": lr, "batch": batch * accum, "mask_rate": mask_rate, "objective": objective,
            "train_sec": time.time() - t0, "n_params": sum(p.numel() for p in model.parameters())}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=6, choices=[3, 4, 5, 6])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/dnabert")
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--data", default="synthetic", choices=["synthetic", *REAL_DATA],
                    help="synthetic iid DNA, or real E. coli windows (held-out E. coli loss then doubles as the utility metric)")
    ap.add_argument("--fasta", default=None, help="override the default path of --data")
    ap.add_argument("--canary_npz", default=None, help="real-canary pool from pilot2.human_canary (default: iid uniform 96-mers)")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--objective", default="mlm", choices=["mlm", "causal"])
    ap.add_argument("--mask_rate", type=float, default=0.15, help="mlm: fraction of TOKENS masked (DNABERT pretraining: 0.15)")
    ap.add_argument("--mask_nt_rate", type=float, default=None,
                    help="mlm: fix the fraction of HIDDEN NUCLEOTIDES instead (token rate = k * this, capped at 0.9)")
    ap.add_argument("--pool", type=int, default=100)
    ap.add_argument("--stride", type=int, default=3, help="score every stride-th nucleotide of the probe")
    ap.add_argument("--save_epochs", default="1,3,8,15,30")
    ap.add_argument("--snapshot_probes", type=int, default=10, help="probes per tier scored at snapshots (all at the end)")
    ap.add_argument("--score_epoch0", action="store_true", help="also score the pretrained model before fine-tuning")
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
    if args.mask_nt_rate:
        args.mask_rate = min(0.9, args.mask_nt_rate * args.k)
    tag = ""
    if args.objective == "causal":
        tag = "_causal"
    elif args.mask_nt_rate:
        tag = f"_nt{args.mask_nt_rate:g}"
    if args.lr != 2e-5:
        tag += f"_lr{args.lr:g}"
    if args.data != "synthetic":
        tag += f"_{args.data}"
    out_dir = Path(args.out) / f"dnabert{args.k}{tag}_s{args.seed}"
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
    model, voc = load_model(args.k, device)
    save_epochs = sorted(int(e) for e in args.save_epochs.split(",") if e)
    t0 = time.time()
    DS_TASKS = tuple(t for t in (args.downstream_tasks.split(",") if args.downstream_tasks else
                     __import__("pilot2.downstream", fromlist=["DEFAULT_TASKS"]).DEFAULT_TASKS.get(args.data, [])) if t)
    if args.downstream and not DS_TASKS:
        raise SystemExit("--downstream needs --downstream_tasks for data=" + args.data)
    DS = lambda m: __import__("pilot2.downstream", fromlist=["evaluate"]).evaluate("kmer", m, voc, device, causal=args.objective == "causal", seed=args.seed, tasks=DS_TASKS) if args.downstream else None
    if args.score_epoch0:
        model.eval()
        sc = score_run(model, voc, ds, device, args.pool, args.seed, args.stride, args.snapshot_probes, objective=args.objective)
        sc.update(epoch=0, score_sec=time.time() - t0)
        sc["downstream"] = DS(model)
        (out_dir / "scores_ep0.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
        print(f"[k={args.k} s{args.seed}] ep0 floor {sc['floors'][0]['bits_per_nt_mean']:.3f} ({sc['score_sec']:.0f}s)", flush=True)
    with open(out_dir / "train_log.jsonl", "w", encoding="utf-8") as log:
        summary = train(model, voc, ds, device, out_dir, args.epochs, args.lr, args.batch, args.accum, args.mask_rate,
                        args.seed, save_epochs, log, objective=args.objective)
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    t1 = time.time()
    sc = score_run(model, voc, ds, device, args.pool, args.seed, args.stride, objective=args.objective)
    sc.update(train_summary=summary, epoch=args.epochs, score_sec=time.time() - t1, checkpoint="final")
    sc["downstream"] = DS(model)
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(f"[k={args.k} s{args.seed}] final floor {sc['floors'][0]['bits_per_nt_mean']:.3f} ({sc['score_sec']:.0f}s)", flush=True)
    for e in save_epochs:
        ck = out_dir / f"ep{e}.pt"
        if not ck.exists() or e == args.epochs:
            if ck.exists():
                ck.unlink()
            continue
        model.load_state_dict(torch.load(ck, map_location=device)); model.eval()
        t2 = time.time()
        s2 = score_run(model, voc, ds, device, args.pool, args.seed, args.stride, args.snapshot_probes, objective=args.objective)
        s2.update(epoch=e, score_sec=time.time() - t2, checkpoint=f"ep{e}")
        s2["downstream"] = DS(model)
        (out_dir / f"scores_ep{e}.json").write_text(json.dumps(s2, indent=1), encoding="utf-8")
        print(f"[k={args.k} s{args.seed}] ep{e} floor {s2['floors'][0]['bits_per_nt_mean']:.3f} ({s2['score_sec']:.0f}s)", flush=True)
        ck.unlink()
    print(f"[k={args.k} s{args.seed}] done in {time.time() - t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
