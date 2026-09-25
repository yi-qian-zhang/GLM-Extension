"""Scorers, ranking against a random candidate pool, and prefix extraction.

All scores are log2-probabilities summed over a slice of nucleotide positions,
so dividing by the slice length gives bits per nucleotide directly.

Scorers by model type (never cross-applied -- see report for why PLL on a
causal model degenerates to plain AR scoring):
  ar      causal model: sum_i log2 p(x_i | x_<i)
  pll     bidirectional model: sum_i log2 p(x_i | x_{\\i}), one masked copy
          per position (Salazar et al. 2020)
  prefix  bidirectional model: sum_i log2 p(x_i | x_<i) by masking every
          position >= i and reading position i. Matches the AR conditioning
          set exactly, so AR-vs-MLM comparisons under it are like for like and
          the 4.0 floor applies to both.

Entropy floor: on iid uniform DNA, E[-log2 q] >= 2.000 bits/nt for any
scorer whose conditionals are normalized over {A,C,G,T} and never see their
own target. pll, prefix and ar all satisfy this on single-nucleotide tokens
(pll via the per-position Gibbs inequality; population optimum = erasure
entropy, which equals the entropy rate exactly when positions are iid).
"""
from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn.functional as F

from .data import (A, MASK, NUC_IDS, PROBE_LEN, PROBE_OFFSET, T, WINDOW,
                   Dataset, Probe, random_dna, with_bos)

ALL = slice(0, WINDOW)
PROBE_SPAN = slice(PROBE_OFFSET, PROBE_OFFSET + PROBE_LEN)


def _log2_softmax(logits: torch.Tensor) -> torch.Tensor:
    return F.log_softmax(logits.float(), dim=-1) / math.log(2.0)


@torch.no_grad()
def score_ar(model, x: torch.Tensor, span: slice = ALL, batch: int = 512) -> torch.Tensor:
    """x: (B, WINDOW) -> (B,) sum of log2 p over span. Causal model only."""
    out = []
    for i in range(0, len(x), batch):
        xb = with_bos(x[i:i + batch])
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(xb[:, :-1])                       # column j predicts x_j
        lp = _log2_softmax(logits).gather(-1, xb[:, 1:, None])[..., 0]  # (b, WINDOW)
        out.append(lp[:, span].sum(-1))
    return torch.cat(out)


@torch.no_grad()
def _score_bidir(model, x: torch.Tensor, span: slice, mode: str, rows_per_batch: int = 4096) -> torch.Tensor:
    """Shared implementation for pll / prefix. One masked copy per scored position."""
    positions = list(range(WINDOW))[span]
    P = len(positions)
    xb_all = with_bos(x)                                     # (B, WINDOW+1); nucleotide j at column j+1
    out = torch.empty(len(x), device=x.device)
    cols = torch.tensor([p + 1 for p in positions], device=x.device)
    # how many windows fit per forward
    wpb = max(1, rows_per_batch // P)
    for i in range(0, len(x), wpb):
        xb = xb_all[i:i + wpb]                               # (w, L)
        w = xb.shape[0]
        rep = xb[:, None, :].expand(w, P, -1).clone()        # (w, P, L)
        if mode == "pll":
            rep[torch.arange(w)[:, None], torch.arange(P)[None, :], cols[None, :]] = MASK
        else:  # prefix: mask every nucleotide column >= target column
            L = xb.shape[1]
            colgrid = torch.arange(L, device=x.device)[None, None, :]          # (1,1,L)
            rep[(colgrid >= cols[None, :, None]).expand(w, P, L)] = MASK
        flat = rep.reshape(w * P, -1)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(flat)                             # (w*P, L, V)
        logits = logits.reshape(w, P, -1, logits.shape[-1])
        # read the masked column itself; target is the true nucleotide there
        tgt = xb[:, None, :].expand(w, P, -1).gather(2, cols[None, :, None].expand(w, P, 1))  # (w,P,1)
        at = logits[torch.arange(w)[:, None], torch.arange(P)[None, :], cols[None, :], :]     # (w,P,V)
        lp = _log2_softmax(at).gather(-1, tgt)[..., 0]      # (w, P)
        out[i:i + w] = lp.sum(-1)
    return out


def score_pll(model, x, span=ALL, **kw):
    return _score_bidir(model, x, span, "pll", **kw)


def score_prefix(model, x, span=ALL, **kw):
    return _score_bidir(model, x, span, "prefix", **kw)


SCORERS = {"ar": score_ar, "pll": score_pll, "prefix": score_prefix}
SCORERS_FOR = {"ar": ["ar"], "mlm": ["pll", "prefix"]}


@torch.no_grad()
def heldout_floor(model, scorer: str, test: np.ndarray, device, n: int = 500) -> dict:
    x = torch.from_numpy(test[:n]).to(device)
    s = SCORERS[scorer](model, x, ALL)
    bits = (-s / WINDOW).cpu().numpy()
    return {"scorer": scorer, "n_windows": int(len(bits)), "bits_per_nt_mean": float(bits.mean()),
            "bits_per_nt_std": float(bits.std()), "perplexity": float(2 ** bits.mean()),
            "floor_ok": bool(bits.mean() >= 1.999),
            "min_window_bits": float(bits.min())}


@torch.no_grad()
def rank_probe(model, scorer: str, probe: Probe, host: np.ndarray, pool: np.ndarray, device) -> dict:
    """Rank the true probe against `pool` random 96-mers, all placed in `host`.
    Score is over the probe span only. Returns rank in 1..n+1 and the chance
    p-value rank/(n+1)."""
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, PROBE_SPAN] = probe.seq
    win[1:, PROBE_SPAN] = pool
    x = torch.from_numpy(win).to(device)
    s = SCORERS[scorer](model, x, PROBE_SPAN).cpu().numpy()
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1),
            "probe_bits_per_nt": float(-true / PROBE_LEN),
            "pool_bits_per_nt_mean": float((-cands / PROBE_LEN).mean()),
            "pool_bits_per_nt_std": float((-cands / PROBE_LEN).std()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, kind: str, probe: Probe, host: np.ndarray, device, k: int = 48) -> dict:
    """Carlini-2023-style: reveal host[:96] + probe[:k], recover probe[k:].
    ar  : greedy decode, argmax restricted to {A,C,G,T}
    mlm : mask everything from PROBE_OFFSET+k onward, unmask strictly left to
          right, argmax restricted to {A,C,G,T}. Same conditioning set as ar."""
    nuc = NUC_IDS.to(device)
    start = PROBE_OFFSET + k
    end = PROBE_OFFSET + PROBE_LEN
    win = torch.from_numpy(host.copy()).to(device)
    win[PROBE_SPAN] = torch.from_numpy(probe.seq).to(device)
    truth = win[start:end].clone()
    if kind == "ar":
        ctx = with_bos(win[None, :start])                    # (1, start+1)
        gen = []
        for _ in range(end - start):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(ctx)[0, -1].float()
            nxt = nuc[logits[nuc].argmax()]
            gen.append(nxt)
            ctx = torch.cat([ctx, nxt.view(1, 1)], dim=1)
        pred = torch.stack(gen)
    else:
        cur = win.clone()
        cur[start:] = MASK
        xb = with_bos(cur[None])
        for pos in range(start, end):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0, pos + 1].float()
            xb[0, pos + 1] = nuc[logits[nuc].argmax()]
        pred = xb[0, start + 1:end + 1]
    ham = int((pred != truth).sum())
    return {"k_revealed": k, "n_generated": int(end - start), "exact": bool(ham == 0),
            "hamming": ham, "chance_exact": float(4.0 ** -(end - start))}


def score_run(model, kind: str, ds: Dataset, device, pool_size: int = 500, seed: int = 0,
              floor_n: int = 500) -> dict:
    """Everything a single trained model contributes to Gate 1."""
    rng = np.random.default_rng(10_000 + seed)
    pool = random_dna(rng, pool_size, PROBE_LEN)             # same pool for every probe
    fresh_hosts = {p.probe_id: random_dna(rng, 1, WINDOW)[0] for p in ds.probes}
    res = {"kind": kind, "pool_size": pool_size, "floors": [], "probes": []}
    for sc in SCORERS_FOR[kind]:
        res["floors"].append(heldout_floor(model, sc, ds.test, device, floor_n))
    for p in ds.probes:
        entry = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {}}
        hosts = {"fresh": fresh_hosts[p.probe_id]}
        if p.repetitions > 0:
            hosts["train"] = ds.train[p.host_rows[0]]
        for hname, host in hosts.items():
            for sc in SCORERS_FOR[kind]:
                entry["ranks"][f"{sc}/{hname}"] = rank_probe(model, sc, p, host, pool, device)
            entry["extract"][hname] = extract_prefix(model, kind, p, host, device)
        res["probes"].append(entry)
    return res
