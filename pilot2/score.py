"""Scorers, ranking and extraction (prefix-conditioned and edge-conditioned) -- tokenizer-aware.

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

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Dataset, Probe, random_dna, decode
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
        if hasattr(tok, "fill_id"):  # spaced k-mers: FILL carries no information, do not score it
            lp = lp * (xb[:, 1:] != tok.fill_id)
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


def _cover(tok, nt_start: int, nt_end: int):
    """Token-aligned nt range [lo, hi) covering [nt_start, nt_end) (identity when aligned)."""
    return (nt_start // tok.k) * tok.k, -(-nt_end // tok.k) * tok.k


def _kmer_letters(tok, device):
    """(n_content, k) nt ids 1..4 of every content token, for prefix-consistent decoding."""
    ids = (tok.content_ids - tok.content_ids[0]).numpy()
    return torch.from_numpy(np.stack([(ids // p) % 4 + 1 for p in tok._pow], 1)).to(device)


@torch.no_grad()
def rank_probe(model, tok, scorer, probe: Probe, host: np.ndarray, pool: np.ndarray, device,
               offset: int = PROBE_OFFSET):
    """Rank the probe against the pool, all placed at `offset` in the same host.

    When `offset` is not a multiple of k the scored span is widened to whole tokens, so it
    includes up to 2(k-1) host nucleotides shared by every candidate: the ranking is exact,
    and bits/nt is normalised by the covered nucleotides (= PROBE_LEN when aligned)."""
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, offset:offset + PROBE_LEN] = probe.seq
    win[1:, offset:offset + PROBE_LEN] = pool
    x = torch.from_numpy(tok.encode(win)).to(device)
    lo, hi = _cover(tok, offset, offset + PROBE_LEN)
    span = tok.span(lo, hi)
    s = SCORERS[scorer](model, tok, x, span).cpu().numpy()
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1), "offset": int(offset),
            "probe_bits_per_nt": float(-true / (hi - lo)),
            "pool_bits_per_nt_mean": float((-cands / (hi - lo)).mean()),
            "pool_bits_per_nt_std": float((-cands / (hi - lo)).std()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, tok, kind, probe: Probe, host: np.ndarray, device, k_nt: int = 48,
                   offset: int = PROBE_OFFSET):
    """Reveal host[:offset] + probe[:k_nt]; recover probe[k_nt:] token by token, compare in nt.

    If the first unknown nucleotide falls inside a token, that token's already-revealed
    letters are enforced: decoding is restricted to k-mers consistent with the known prefix."""
    content = tok.content_ids.to(device)
    start_nt, end_nt = offset + k_nt, offset + PROBE_LEN
    lo, hi = _cover(tok, start_nt, end_nt)
    start, end = tok.nt_to_tok(lo), tok.nt_to_tok(hi)
    win = host.copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    truth_nt = torch.from_numpy(win[start_nt:end_nt]).to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None

    def allowed(pos):
        """Content-token mask consistent with revealed nucleotides inside token `pos` (or None)."""
        if letters is None:
            return None
        nt0 = pos if hasattr(tok, "fill_id") else pos * tok.k
        known = [(i, int(win[nt0 + i])) for i in range(tok.k) if nt0 + i < start_nt]
        if not known:
            return None
        m = torch.ones(len(content), dtype=torch.bool, device=device)
        for i, v in known:
            m &= letters[:, i] == v
        return m

    def pick(logits, pos):
        lc = logits[content]
        m = allowed(pos)
        if m is not None:
            lc = lc.masked_fill(~m, float("-inf"))
        return content[lc.argmax()]
    if kind == "ar":
        ctx = with_bos(xt[None, :start], tok.bos_id)
        gen = []
        for pos in range(start, end):
            if hasattr(tok, "is_fill") and tok.is_fill(pos):
                nxt = torch.tensor(tok.fill_id, device=device)
                gen.append(nxt)
                ctx = torch.cat([ctx, nxt.view(1, 1)], dim=1)
                continue
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(ctx)[0, -1].float()
            nxt = pick(logits, pos)
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
            xb[0, pos + 1] = pick(logits, pos)
        pred_tok = xb[0, start + 1:end + 1]
    pred_nt = tok.decode_t(pred_tok[None])[0][start_nt - lo:end_nt - lo]
    ham = int((pred_nt != truth_nt).sum())
    return {"k_revealed_nt": k_nt, "offset": int(offset), "n_generated_nt": int(end_nt - start_nt),
            "n_generated_tok": int(end - start),
            "exact": bool(ham == 0), "hamming_nt": ham, "chance_exact": float(4.0 ** -(end_nt - start_nt)),
            "pred_nt": decode(pred_nt.cpu().numpy()), "truth_nt": decode(truth_nt.cpu().numpy())}


@torch.no_grad()
def extract_infill(model, tok, kind, probe: Probe, host: np.ndarray, device, k_nt: int = 48,
                   offset: int = PROBE_OFFSET, order: str = "confidence"):
    """Edge-conditioned extraction for bidirectional models: the same 48 nt are generated as in
    `extract_prefix`, but the host AFTER the canary stays visible instead of being masked.

    Why this exists. `extract_prefix` masks everything from the first unknown token to the end of
    the window, which matches autoregressive conditioning and is the protocol the paper reports.
    For a model that denoises arbitrary positions that is one mask geometry among many, and
    prefix-only probing is known to understate extractability: on diffusion language models
    edge-conditioned masks recover up to three times more verbatim sequences than prefix-conditioned
    ones (Wang and Asokan, arXiv:2605.24173). A masked cell that reproduces nothing under
    `extract_prefix` has therefore not been shown safe until it is also asked in its own idiom.

    Decoding order: "confidence" fills the masked position whose argmax probability is highest,
    re-runs the model, and repeats (the usual diffusion decoding, and the stronger attack);
    "left" reproduces the left-to-right order of `extract_prefix` for a controlled comparison.
    Returns None for causal models, which cannot condition on a suffix.
    """
    if kind == "ar":
        return None
    content = tok.content_ids.to(device)
    start_nt, end_nt = offset + k_nt, offset + PROBE_LEN
    lo, hi = _cover(tok, start_nt, end_nt)
    start, end = tok.nt_to_tok(lo), tok.nt_to_tok(hi)
    win = host.copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    truth_nt = torch.from_numpy(win[start_nt:end_nt]).to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None

    def allowed(pos):
        """As in extract_prefix: keep the revealed letters of a partly-revealed boundary token."""
        if letters is None:
            return None
        nt0 = pos if hasattr(tok, "fill_id") else pos * tok.k
        known = [(i, int(win[nt0 + i])) for i in range(tok.k) if nt0 + i < start_nt]
        if not known:
            return None
        m = torch.ones(len(content), dtype=torch.bool, device=device)
        for i, v in known:
            m &= letters[:, i] == v
        return m

    cur = xt.clone()
    cur[start:end] = tok.mask_id                      # only the middle; the suffix stays real
    xb = with_bos(cur[None], tok.bos_id)
    todo = [pos for pos in range(start, end)
            if not (hasattr(tok, "is_fill") and tok.is_fill(pos))]
    for pos in range(start, end):                     # spaced tokenizers: filler is deterministic
        if hasattr(tok, "is_fill") and tok.is_fill(pos):
            xb[0, pos + 1] = tok.fill_id
    while todo:
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(xb)[0].float()
        best, best_pos, best_tok = -1.0, None, None
        for pos in todo:
            lc = logits[pos + 1][content]
            m = allowed(pos)
            if m is not None:
                lc = lc.masked_fill(~m, float("-inf"))
            pr = F.softmax(lc, dim=-1)
            v, i = pr.max(0)
            if order != "confidence":                 # left-to-right: take the first and stop
                best_pos, best_tok = pos, content[i]
                break
            if float(v) > best:
                best, best_pos, best_tok = float(v), pos, content[i]
        xb[0, best_pos + 1] = best_tok
        todo.remove(best_pos)
    pred_tok = xb[0, start + 1:end + 1]
    pred_nt = tok.decode_t(pred_tok[None])[0][start_nt - lo:end_nt - lo]
    ham = int((pred_nt != truth_nt).sum())
    return {"protocol": f"infill-{order}", "k_revealed_nt": k_nt, "offset": int(offset),
            "n_generated_nt": int(end_nt - start_nt), "n_generated_tok": int(end - start),
            "exact": bool(ham == 0), "hamming_nt": ham,
            "chance_exact": float(4.0 ** -(end_nt - start_nt)),
            "pred_nt": decode(pred_nt.cpu().numpy()), "truth_nt": decode(truth_nt.cpu().numpy())}


def score_run(model, tok: KmerTokenizer, kind: str, ds: Dataset, device, pool_size=500, seed=0, floor_n=500,
              offset_mode: str = "fixed"):
    """offset_mode="random": the training host is scored at that copy's own offset, and the
    fresh host at a new random offset (`phase_match` = fraction of training copies whose
    k-mer phase equals the fresh offset's)."""
    rng = np.random.default_rng(10_000 + seed)
    real_pool = getattr(ds, "pool_seqs", None)            # real canaries -> rank against real segments
    pool = random_dna(rng, pool_size, PROBE_LEN) if real_pool is None else real_pool[:pool_size]
    real_hosts = getattr(ds, "fresh_hosts", None)        # real canaries -> real fresh hosts
    fresh_hosts = {p.probe_id: (random_dna(rng, 1, WINDOW)[0] if real_hosts is None
                                else real_hosts[i % len(real_hosts)].copy())
                   for i, p in enumerate(ds.probes)}
    off_rng = np.random.default_rng(20_000 + seed)
    fresh_off = {p.probe_id: (PROBE_OFFSET if offset_mode == "fixed"
                              else int(off_rng.integers(0, WINDOW - PROBE_LEN + 1))) for p in ds.probes}
    res = {"kind": kind, "tokenizer": tok.name, "k": tok.k, "pool_size": pool_size, "floors": [], "probes": []}
    for sc in SCORERS_FOR[kind]:
        res["floors"].append(heldout_floor(model, tok, sc, ds.test, device, floor_n))
    for p in ds.probes:
        fo = fresh_off[p.probe_id]
        entry = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {},
                 "train_offsets": list(p.offsets), "fresh_offset": fo,
                 "phase_match": (float(np.mean([(fo - o) % tok.k == 0 for o in p.offsets])) if p.offsets else None)}
        hosts = {"fresh": (fresh_hosts[p.probe_id], fo)}
        if p.repetitions > 0:
            hosts["train"] = (ds.train[p.host_rows[0]], p.offsets[0])
        for hname, (host, off) in hosts.items():
            for sc in SCORERS_FOR[kind]:
                entry["ranks"][f"{sc}/{hname}"] = rank_probe(model, tok, sc, p, host, pool, device, offset=off)
            entry["extract"][hname] = extract_prefix(model, tok, kind, p, host, device, offset=off)
        res["probes"].append(entry)
    return res
