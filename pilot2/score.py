"""Scorers, ranking and prefix extraction -- tokenizer-aware.

Every score is a sum of log2 token probabilities converted to BITS PER
NUCLEOTIDE by dividing by the number of nucleotides covered, never by the
number of tokens. With k nucleotides per token the per-token floor on uniform
DNA is 2k bits, so the per-nucleotide floor is 2.000 for every tokenizer.

Scorers by model type (never cross-applied):
  ar      causal: sum_j log2 p(t_j | t_<j)
  pll     bidirectional: one masked copy per token, read the masked column
  prefix  bidirectional: mask every token >= j, read j (matches AR conditioning)
Both bidirectional scorers are always computed and reported; each carries its
own held-out floor check.
"""
from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn.functional as F

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Dataset, Probe, random_dna
from .tokenizers import KmerTokenizer
from .train import with_bos


def _log2_softmax(logits):
    return F.log_softmax(logits.float(), dim=-1) / math.log(2.0)


@torch.no_grad()
def score_ar(model, tok: KmerTokenizer, x_tok: torch.Tensor, span: slice, batch: int = 512):
    out = []
    for i in range(0, len(x_tok), batch):
        xb = with_bos(x_tok[i:i + batch], tok.bos_id)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(xb[:, :-1])
        lp = _log2_softmax(logits).gather(-1, xb[:, 1:, None])[..., 0]
        out.append(lp[:, span].sum(-1))
    return torch.cat(out)


@torch.no_grad()
def _score_bidir(model, tok, x_tok, span, mode, rows_per_batch=2048):
    positions = list(range(tok.n_tokens))[span]
    P = len(positions)
    xb_all = with_bos(x_tok, tok.bos_id)
    cols = torch.tensor([p + 1 for p in positions], device=x_tok.device)
    out = torch.empty(len(x_tok), device=x_tok.device)
    wpb = max(1, rows_per_batch // P)
    L = xb_all.shape[1]
    for i in range(0, len(x_tok), wpb):
        xb = xb_all[i:i + wpb]
        w = xb.shape[0]
        rep = xb[:, None, :].expand(w, P, -1).clone()
        if mode == "pll":
            rep[torch.arange(w)[:, None], torch.arange(P)[None, :], cols[None, :]] = tok.mask_id
        else:
            colgrid = torch.arange(L, device=x_tok.device)[None, None, :]
            rep[(colgrid >= cols[None, :, None]).expand(w, P, L)] = tok.mask_id
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(rep.reshape(w * P, L))
        logits = logits.reshape(w, P, L, -1)
        tgt = xb[:, None, :].expand(w, P, -1).gather(2, cols[None, :, None].expand(w, P, 1))
        at = logits[torch.arange(w)[:, None], torch.arange(P)[None, :], cols[None, :], :]
        out[i:i + w] = _log2_softmax(at).gather(-1, tgt)[..., 0].sum(-1)
    return out


def score_pll(model, tok, x, span, **kw):
    return _score_bidir(model, tok, x, span, "pll", **kw)


def score_prefix(model, tok, x, span, **kw):
    return _score_bidir(model, tok, x, span, "prefix", **kw)


SCORERS = {"ar": score_ar, "pll": score_pll, "prefix": score_prefix}
SCORERS_FOR = {"ar": ["ar"], "mlm": ["pll", "prefix"]}


@torch.no_grad()
def heldout_floor(model, tok, scorer, test_nt: np.ndarray, device, n=500):
    x = torch.from_numpy(tok.encode(test_nt[:n])).to(device)
    s = SCORERS[scorer](model, tok, x, slice(0, tok.n_tokens))
    bits = (-s / WINDOW).cpu().numpy()
    return {"scorer": scorer, "n_windows": int(len(bits)), "bits_per_nt_mean": float(bits.mean()),
            "bits_per_nt_std": float(bits.std()), "perplexity_nt": float(2 ** bits.mean()),
            "floor_ok": bool(bits.mean() >= 1.999), "min_window_bits": float(bits.min())}


@torch.no_grad()
def rank_probe(model, tok, scorer, probe: Probe, host: np.ndarray, pool: np.ndarray, device):
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, PROBE_OFFSET:PROBE_OFFSET + PROBE_LEN] = probe.seq
    win[1:, PROBE_OFFSET:PROBE_OFFSET + PROBE_LEN] = pool
    x = torch.from_numpy(tok.encode(win)).to(device)
    span = tok.span(PROBE_OFFSET, PROBE_OFFSET + PROBE_LEN)
    s = SCORERS[scorer](model, tok, x, span).cpu().numpy()
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1),
            "probe_bits_per_nt": float(-true / PROBE_LEN),
            "pool_bits_per_nt_mean": float((-cands / PROBE_LEN).mean()),
            "pool_bits_per_nt_std": float((-cands / PROBE_LEN).std()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, tok, kind, probe: Probe, host: np.ndarray, device, k_nt: int = 48):
    """Reveal host[:96] + probe[:k_nt]; recover probe[k_nt:] token by token, compare in nt."""
    content = tok.content_ids.to(device)
    start_nt, end_nt = PROBE_OFFSET + k_nt, PROBE_OFFSET + PROBE_LEN
    start, end = tok.nt_to_tok(start_nt), tok.nt_to_tok(end_nt)
    win = host.copy()
    win[PROBE_OFFSET:PROBE_OFFSET + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    truth_nt = torch.from_numpy(win[start_nt:end_nt]).to(device)
    if kind == "ar":
        ctx = with_bos(xt[None, :start], tok.bos_id)
        gen = []
        for _ in range(end - start):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(ctx)[0, -1].float()
            nxt = content[logits[content].argmax()]
            gen.append(nxt)
            ctx = torch.cat([ctx, nxt.view(1, 1)], dim=1)
        pred_tok = torch.stack(gen)
    else:
        cur = xt.clone()
        cur[start:] = tok.mask_id
        xb = with_bos(cur[None], tok.bos_id)
        for pos in range(start, end):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0, pos + 1].float()
            xb[0, pos + 1] = content[logits[content].argmax()]
        pred_tok = xb[0, start + 1:end + 1]
    pred_nt = tok.decode_t(pred_tok[None])[0]
    ham = int((pred_nt != truth_nt).sum())
    return {"k_revealed_nt": k_nt, "n_generated_nt": int(end_nt - start_nt), "n_generated_tok": int(end - start),
            "exact": bool(ham == 0), "hamming_nt": ham, "chance_exact": float(4.0 ** -(end_nt - start_nt))}


def score_run(model, tok: KmerTokenizer, kind: str, ds: Dataset, device, pool_size=500, seed=0, floor_n=500):
    rng = np.random.default_rng(10_000 + seed)
    pool = random_dna(rng, pool_size, PROBE_LEN)
    fresh_hosts = {p.probe_id: random_dna(rng, 1, WINDOW)[0] for p in ds.probes}
    res = {"kind": kind, "tokenizer": tok.name, "k": tok.k, "pool_size": pool_size, "floors": [], "probes": []}
    for sc in SCORERS_FOR[kind]:
        res["floors"].append(heldout_floor(model, tok, sc, ds.test, device, floor_n))
    for p in ds.probes:
        entry = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {}}
        hosts = {"fresh": fresh_hosts[p.probe_id]}
        if p.repetitions > 0:
            hosts["train"] = ds.train[p.host_rows[0]]
        for hname, host in hosts.items():
            for sc in SCORERS_FOR[kind]:
                entry["ranks"][f"{sc}/{hname}"] = rank_probe(model, tok, sc, p, host, pool, device)
            entry["extract"][hname] = extract_prefix(model, tok, kind, p, host, device)
        res["probes"].append(entry)
    return res
