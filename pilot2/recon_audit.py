"""Why a masked cell can hold a record completely and reconstruct none of it, measured.

    python -m pilot2.recon_audit --root outputs/human_mlm_long --tiers 1,4,16 --gpu 1

The 150-round masked cells are the paper's strongest result and its most attackable one: a planted
canary sits ~1.9 bits below the non-member control under the bidirectional scorer and is ranked
first against 100 candidates even after a single insertion, while greedy reconstruction of its
second half is exactly 0 % in all 30 cells and leaves 30-34 of 48 nucleotides wrong, which is the
non-member distance. A reviewer will say the extractor is broken. Two measurements answer that, and
neither exists in the saved runs:

1. THE CONDITIONAL THE RULERS ACTUALLY USE. `rank_probe` normalises bits/nt over the whole 96-nt
   canary, and `extract_prefix` reveals the first 48 of those for free. So a low canary surprise can
   coexist with a hopeless reconstruction simply because half the scored span is the half the
   attacker was given. This script measures the quantity extraction has to invert and nothing else:
   the teacher-forced chain-rule surprise of the 48 TARGET nucleotides given the revealed prefix,
   together with the fraction of decoding steps at which the true token is the argmax. All-48-exact
   requires every step, so top1_rate**n_steps is an upper bound on the extraction rate, and a cell
   with high target surprise cannot be rescued by any decoder, beam search included.

2. THE DECODE THAT WAS NEVER RUN. Both shipped protocols mask 8-16 target tokens at once, far
   outside the 15 % iid masking the model was trained on, while the surprise and recognition rulers
   read a conditional with ONE token masked. Iterated conditional modes closes that gap: initialise
   the target, then re-mask exactly one target token at a time with every other target token at its
   current value, sweeping to a fixed point. That is ~1/48 masking, inside the training
   distribution, and it is the strongest attack available to someone holding only the flanking
   sequence. If it still returns 0 %, the 0 % is a property of the model under every conditioning
   such an attacker can construct, and the paper can say so.

Reads only saved checkpoints, writes only new files, and does not touch pilot2/score.py, because
queue_1012a is mid-flight and must score every cell with the same code. Fold the ICM decoder into
`score.py:extract_infill` as `order="icm"` once that queue has finished.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Probe, decode, random_dna
from .model import Backbone
from .real_data import DATA_PATHS, build_real_dataset
from .score import _cover, _kmer_letters, extract_infill, extract_prefix
from .tokenizers import get_tokenizer
from .train import parse_objective, with_bos

try:                                     # synthetic cells only
    from .data import build_dataset
except ImportError:                      # pragma: no cover
    build_dataset = None

# accepts the plain cells and the --init_from / --lora_r ones, which run_pilot names <tok>_<obj>_ft_s<n>
RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?)_(?P<obj>ar|mlm[0-9.]+)(?:_ft)?(?:_lora\d+)?_s(?P<seed>\d+)$")
# released Nucleotide Transformer cells, e.g. nt250m_mlm_ecoli_s0, which pilot2/nt.py names itself
NT_RUN = re.compile(r"nt\d+m_(?:ar|mlm)_[a-z0-9]+_s\d+$")


def rebuild(d: Path, device, ckpt="final.pt"):
    """(model, tok, kind, ds, args) for one run directory, from its own args.json and checkpoint.

    Reads the backbone geometry out of args.json. Without that, every cell of queue_1012a -- which
    is the 59.9M (768/8/12) and 201M (1024/16/16) arm -- dies in load_state_dict.
    """
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    is_nt = "size" in a                  # a released Nucleotide Transformer cell, not our backbone
    kind = _kind_of(a)
    tok = _nt_vocab(a["size"]) if is_nt else get_tokenizer(a["tokenizer"], 288)
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    n_val, n_test = _split_sizes(a)
    if a.get("data", "synthetic") != "synthetic":
        ds = build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], a["n_train"], n_val,
                                n_test, a["probes_per_tier"], tiers, a["n_nonmember"],
                                a["data_seed"], offset_mode=a["probe_offset"],
                                canary_npz=a.get("canary_npz"))
    else:
        ds = build_dataset(a["n_train"], n_val, n_test, a["probes_per_tier"], tiers,
                           a["n_nonmember"], a["data_seed"], offset_mode=a["probe_offset"],
                           enrich_k=a.get("enrich_k"), enrich_factor=a.get("enrich_factor", 1.0))
    if is_nt:
        # The 95-100 % reconstruction result is measured on our own from-scratch backbone. Asking a
        # RELEASED masked checkpoint the same question is the obvious next thing a reader wants, and
        # it needs the fine-tuned weights, which pilot2/nt.py now writes under --save_ckpt.
        from . import nt as ntmod
        model, _ = ntmod.load(a["size"], False, device)
        model.hf.load_state_dict(torch.load(d / ckpt, map_location=device))
        model.eval()
        return model, tok, kind, ds, a
    kw = {k: v for k, v in (("d_model", a.get("d_model")), ("n_layers", a.get("n_layers")),
                            ("n_heads", a.get("n_heads")), ("d_ff", a.get("d_ff")),
                            ("emb_rank", a.get("emb_rank"))) if v}
    if a.get("pos_enc", "abs") != "abs":
        kw["pos_enc"] = a["pos_enc"]
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), **kw).to(device)
    sd = torch.load(d / ckpt, map_location=device)
    sd = {k.replace("base_model.model.", "").replace(".base_layer", ""): v for k, v in sd.items()}
    model.load_state_dict(sd, strict=False) if any("lora" in k for k in sd) else model.load_state_dict(sd)
    model.eval()
    return model, tok, kind, ds, a


def _nt_vocab(size: str):
    from pathlib import Path as _P

    from . import nt as ntmod
    return ntmod.NTVocab(_P(ntmod.ROOT) / ntmod.SIZES[size])


def _kind_of(a: dict) -> str:
    """'mlm' or 'ar', from whatever spelling the wrapper that produced this run happened to use.

    `parse_objective` is our backbone's parser and demands "mlm@<rate>"; it raises on the bare
    "mlm" that pilot2/nt.py writes and on the "causal" that pilot2/dnabert.py writes. Calling it
    unguarded here meant every released cell died before the decoder ever ran.
    """
    obj = a.get("objective")
    if obj is None:                       # pilot2/hyena.py records no objective; it is causal-only
        return "ar"
    if obj in ("causal", "ar"):
        return "ar"
    if obj == "mlm":
        return "mlm"
    return parse_objective(obj)[0]


# The wrappers that hardcode their validation and test split sizes instead of recording them.
# Guessing here is worse than crashing: real_data.py draws every probe HOST from the windows after
# n_train + n_val + n_test, so a wrong value silently moves every canary into a window the model
# never trained on, and the decoder would then report a number for the wrong sequence.
_HARDCODED_SPLIT = 200


def _split_sizes(a: dict):
    n_val, n_test = a.get("n_val"), a.get("n_test")
    if n_val is not None and n_test is not None:
        return n_val, n_test
    assert "size" not in a, "NT records its split sizes; a missing one means something else is wrong"
    # dnabert.py, dnabert2.py and hyena.py all pass n_val=n_test=200 and do not write it down
    return (n_val if n_val is not None else _HARDCODED_SPLIT,
            n_test if n_test is not None else _HARDCODED_SPLIT)


def _span(tok, offset, k_nt):
    start_nt, end_nt = offset + k_nt, offset + PROBE_LEN
    lo, hi = _cover(tok, start_nt, end_nt)
    return start_nt, end_nt, lo, hi, tok.nt_to_tok(lo), tok.nt_to_tok(hi)


def _allowed_fn(tok, win, start_nt, letters, content, device):
    """Content-token mask keeping the already-revealed letters of a partly-revealed token."""
    def allowed(pos):
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
    return allowed


@torch.no_grad()
def target_surprise(model, tok, kind, probe: Probe, host, device, k_nt=48, offset=PROBE_OFFSET):
    """Teacher-forced surprise of the TRUE target half under the extractor's own conditioning.

    Returns bits per TARGET nucleotide (not per canary nucleotide: the revealed half is excluded,
    which is the whole point), the fraction of steps whose argmax is the true token, and the upper
    bound that fraction places on all-48-exact extraction.
    """
    content = tok.content_ids.to(device)
    start_nt, end_nt, lo, hi, start, end = _span(tok, offset, k_nt)
    win = np.asarray(host).copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None
    allowed = _allowed_fn(tok, win, start_nt, letters, content, device)

    def step_logp(logits, pos):
        lc = logits[content]
        m = allowed(pos)
        if m is not None:
            lc = lc.masked_fill(~m, float("-inf"))
        lp = F.log_softmax(lc.float(), dim=-1) / math.log(2.0)
        true = int((content == xt[pos]).nonzero()[0, 0])
        return float(lp[true]), bool(int(lc.argmax()) == true)

    bits, hits = 0.0, []
    if kind == "ar":
        ctx = with_bos(xt[None, :start], tok.bos_id)
        for pos in range(start, end):
            if hasattr(tok, "is_fill") and tok.is_fill(pos):
                ctx = torch.cat([ctx, xt[pos].view(1, 1)], dim=1)
                continue
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(ctx)[0, -1].float()
            lp, hit = step_logp(logits, pos)
            bits -= lp
            hits.append(hit)
            ctx = torch.cat([ctx, xt[pos].view(1, 1)], dim=1)   # teacher forcing
    else:
        cur = xt.clone()
        cur[start:] = tok.mask_id
        xb = with_bos(cur[None], tok.bos_id)
        for pos in range(start, end):
            if hasattr(tok, "is_fill") and tok.is_fill(pos):
                xb[0, pos + 1] = xt[pos]
                continue
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0, pos + 1].float()
            lp, hit = step_logp(logits, pos)
            bits -= lp
            hits.append(hit)
            xb[0, pos + 1] = xt[pos]                            # teacher forcing
    n = max(1, len(hits))
    rate = float(np.mean(hits))
    return {"target_bits_per_nt": bits / (end_nt - start_nt), "target_bits_total": bits,
            "top1_rate": rate, "n_steps": n, "exact_upper_bound": rate ** n}


@torch.no_grad()
def extract_icm(model, tok, kind, probe: Probe, host, device, k_nt=48, offset=PROBE_OFFSET,
                sweeps: int = 6, init: str = "confidence", restarts: int = 1):
    """Iterated conditional modes: re-mask ONE target token at a time, sweep to a fixed point.

    The conditional used here (1 of ~48 tokens masked, the rest at their current values) is the one
    the model was trained on and the one the surprise and recognition rulers read, which neither
    shipped extraction protocol ever enters. Returns None for causal models.
    """
    if kind == "ar":
        return None
    content = tok.content_ids.to(device)
    start_nt, end_nt, lo, hi, start, end = _span(tok, offset, k_nt)
    win = np.asarray(host).copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    truth_nt = torch.from_numpy(win[start_nt:end_nt]).to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None
    allowed = _allowed_fn(tok, win, start_nt, letters, content, device)

    # the shipped edge-conditioned decode, reported beside ICM so the gain is attributable
    seed_pred = extract_infill(model, tok, kind, probe, host, device, k_nt=k_nt, offset=offset,
                               order=init)
    base = xt.clone()
    base[start:end] = tok.mask_id
    xb0 = with_bos(base[None], tok.bos_id)
    todo = []
    for pos in range(start, end):
        if hasattr(tok, "is_fill") and tok.is_fill(pos):
            xb0[0, pos + 1] = tok.fill_id
        else:
            todo.append(pos)

    def masked_logits(xb, pos):
        keep = xb[0, pos + 1].clone()
        xb[0, pos + 1] = tok.mask_id
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = model(xb)[0, pos + 1].float()
        xb[0, pos + 1] = keep
        lc = out[content]
        m = allowed(pos)
        return lc.masked_fill(~m, float("-inf")) if m is not None else lc

    def sweep(xb):
        """Re-mask one target token at a time and take its mode, until nothing changes."""
        used = 0
        for _ in range(sweeps):
            changed = 0
            used += 1
            for pos in todo:
                new_tok = content[int(masked_logits(xb, pos).argmax())]
                changed += int(new_tok.item() != xb[0, pos + 1].item())
                xb[0, pos + 1] = new_tok
            if changed == 0:
                break
        return used

    def pseudo_ll(xb):
        """Sum of log2 p(token | all others) over the target, computable WITHOUT the truth.

        This is what lets the attack choose between fixed points. Without it, restarts would only
        be an oracle number, because an attacker cannot ask which reconstruction is correct.
        """
        tot = 0.0
        for pos in todo:
            lp = F.log_softmax(masked_logits(xb, pos).float(), dim=-1) / math.log(2.0)
            tot += float(lp[int((content == xb[0, pos + 1]).nonzero()[0, 0])])
        return tot

    def read_out(xb):
        pred_nt = tok.decode_t(xb[0, start + 1:end + 1][None])[0][start_nt - lo:end_nt - lo]
        return pred_nt, int((pred_nt != truth_nt).sum())

    results = []
    for r in range(max(1, restarts)):
        xb = xb0.clone()
        if r == 0:                                   # the published initialisation: one joint pass
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0].float()
            for pos in todo:
                lc = logits[pos + 1][content]
                m = allowed(pos)
                if m is not None:
                    lc = lc.masked_fill(~m, float("-inf"))
                xb[0, pos + 1] = content[int(lc.argmax())]
        else:                                        # a random admissible start, seeded per probe
            g = torch.Generator(device="cpu").manual_seed(1000 * int(probe.probe_id) + r)
            for pos in todo:
                m = allowed(pos)
                idx = torch.arange(len(content)) if m is None else torch.nonzero(m.cpu())[:, 0]
                xb[0, pos + 1] = content[int(idx[torch.randint(len(idx), (1,), generator=g)])]
        used = sweep(xb)
        pred_nt, ham_r = read_out(xb)
        results.append({"score": pseudo_ll(xb), "ham": ham_r, "exact": ham_r == 0,
                        "sweeps": used, "pred": decode(pred_nt.cpu().numpy())})

    best = max(results, key=lambda d: d["score"])    # the attack's own choice, truth-free
    ham, n_sweeps = best["ham"], best["sweeps"]
    oracle = any(d["exact"] for d in results)

    # The predictor that matches THIS decoder. The prefix-conditional top-1 rate bounds left-to-right
    # decoding, and ICM beat that bound by two orders of magnitude on the one cell that extracts,
    # because ICM conditions on the suffix and on the other target tokens. The operative quantity is
    # therefore leave-one-out: every other target token at its TRUE value, one masked, is the
    # conditional ICM converges to and the one the PLL scorer reads. Its product over the target
    # tokens is the rate at which a fixed point can be the true string.
    xb = xb0.clone()
    for q in todo:
        xb[0, q + 1] = xt[q]
    loo_hits, loo_bits = [], 0.0
    for pos in todo:
        lc = masked_logits(xb, pos)
        true = int((content == xt[pos]).nonzero()[0, 0])
        lp = F.log_softmax(lc.float(), dim=-1) / math.log(2.0)
        loo_bits -= float(lp[true])
        loo_hits.append(bool(int(lc.argmax()) == true))
    loo_rate = float(np.mean(loo_hits)) if loo_hits else float("nan")
    return {"protocol": f"icm-{init}-r{restarts}", "sweeps_used": n_sweeps,
            "k_revealed_nt": k_nt, "restarts": int(max(1, restarts)),
            "offset": int(offset), "n_generated_nt": int(end_nt - start_nt),
            "exact": bool(ham == 0), "hamming_nt": ham,
            "oracle_exact": bool(oracle), "best_score": float(best["score"]),
            "ham_by_restart": [d["ham"] for d in results],
            "loo_top1": loo_rate, "loo_bits_per_nt": loo_bits / (end_nt - start_nt),
            "loo_bound": loo_rate ** max(1, len(loo_hits)), "n_target_tok": len(todo),
            "seed_exact": bool(seed_pred["exact"]), "seed_hamming_nt": int(seed_pred["hamming_nt"]),
            "pred_nt": best["pred"], "truth_nt": decode(truth_nt.cpu().numpy())}


def fresh_views(ds, seed, pool_size):
    """The same fresh hosts and offsets score_run uses, so the control is phase-matched.

    score_run draws the candidate pool from this generator first when the canaries are synthetic, so
    the pool size has to be replayed or every fresh host would differ from the one actually scored.
    """
    rng = np.random.default_rng(10_000 + seed)
    real_pool = getattr(ds, "pool_seqs", None)
    if real_pool is None:
        random_dna(rng, pool_size, PROBE_LEN)                            # keep the rng in step
    real_hosts = getattr(ds, "fresh_hosts", None)
    hosts = {p.probe_id: (random_dna(rng, 1, WINDOW)[0] if real_hosts is None
                          else real_hosts[i % len(real_hosts)].copy())
             for i, p in enumerate(ds.probes)}
    off_rng = np.random.default_rng(20_000 + seed)
    offs = {p.probe_id: int(off_rng.integers(0, WINDOW - PROBE_LEN + 1)) for p in ds.probes}
    return hosts, offs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--max_probes", type=int, default=25, help="per tier")
    ap.add_argument("--sweeps", type=int, default=6)
    ap.add_argument("--restarts", type=int, default=1,
                    help="ICM restarts; >1 adds random admissible starts and picks the fixed point "
                         "with the best pseudo-log-likelihood, which an attacker can compute")
    ap.add_argument("--ckpt", default="final.pt")
    ap.add_argument("--name", default="recon_audit")
    ap.add_argument("--no_icm", action="store_true", help="target surprise only, no ICM decode")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    tiers = [int(t) for t in args.tiers.split(",")]

    rows = []
    for root in args.root:
        rd = Path(root)
        dirs = [rd] if (rd / "args.json").exists() else sorted(p for p in rd.iterdir() if p.is_dir())
        for d in dirs:
            if not ((d / "args.json").exists() and (d / args.ckpt).exists()
                    and (RUN.fullmatch(d.name) or NT_RUN.fullmatch(d.name))):
                continue
            model, tok, kind, ds, a = rebuild(d, device, args.ckpt)
            tok = tok.to(device) if hasattr(tok, "to") else tok
            fh, fo = fresh_views(ds, a["seed"], a.get("pool", 500))
            out = {"run": d.name, "ckpt": args.ckpt, "data": a.get("data", "synthetic"),
                   "objective": a["objective"], "tokenizer": a.get("tokenizer", a.get("size")),
                   "seed": a["seed"],
                   "d_model": a.get("d_model"), "n_layers": a.get("n_layers"), "cells": []}
            per = defaultdict(lambda: defaultdict(list))
            for tier in tiers + [0]:
                ps = [p for p in ds.probes if p.repetitions == tier][:args.max_probes]
                for p in ps:
                    if tier > 0:
                        host, off, hname = ds.train[p.host_rows[0]], p.offsets[0], "train"
                    else:
                        host, off, hname = fh[p.probe_id], fo[p.probe_id], "fresh"
                    ts = target_surprise(model, tok, kind, p, host, device, offset=off)
                    pre = extract_prefix(model, tok, kind, p, host, device, offset=off)
                    icm = (None if args.no_icm else
                           extract_icm(model, tok, kind, p, host, device, offset=off,
                                       sweeps=args.sweeps, restarts=args.restarts))
                    v = per[tier]
                    v["tgt_bits"].append(ts["target_bits_per_nt"])
                    v["top1"].append(ts["top1_rate"])
                    v["bound"].append(ts["exact_upper_bound"])
                    v["pre_exact"].append(float(pre["exact"]))
                    v["pre_ham"].append(pre["hamming_nt"])
                    if icm:
                        v["icm_exact"].append(float(icm["exact"]))
                        v["icm_ham"].append(icm["hamming_nt"])
                        v["seed_exact"].append(float(icm["seed_exact"]))
                        v["seed_ham"].append(icm["seed_hamming_nt"])
                        v["loo_top1"].append(icm["loo_top1"])
                        v["loo_bound"].append(icm["loo_bound"])
                        v["loo_bits"].append(icm["loo_bits_per_nt"])
                        v["oracle"].append(float(icm["oracle_exact"]))
                    out["cells"].append({"tier": tier, "host": hname, "probe_id": p.probe_id,
                                         "target": ts, "prefix": pre, "icm": icm})
            (d / f"{args.name}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            for t in sorted(per, reverse=True):
                m = lambda k: float(np.mean(per[t][k])) if per[t][k] else float("nan")
                rows.append(dict(run=d.name, data=out["data"],
                                 tok=a.get("tokenizer", a.get("size")), obj=a["objective"],
                                 seed=a["seed"], tier=t, n=len(per[t]["tgt_bits"]),
                                 tgt_bits=m("tgt_bits"), top1=m("top1"), bound=m("bound"),
                                 pre_exact=m("pre_exact"), pre_ham=m("pre_ham"),
                                 icm_exact=m("icm_exact"), icm_ham=m("icm_ham"),
                                 seed_exact=m("seed_exact"), seed_ham=m("seed_ham"),
                                 loo_top1=m("loo_top1"), loo_bound=m("loo_bound"),
                                 loo_bits=m("loo_bits"), oracle=m("oracle")))
                r = rows[-1]
                print(f"  {d.name:28s} r={t:<3d} n={r['n']:3d} | target {r['tgt_bits']:5.3f} b/nt "
                      f"top1 {r['top1']:.2f} bound {r['bound']:.3f} | prefix {100*r['pre_exact']:5.1f}% "
                      f"(ham {r['pre_ham']:4.1f}) | icm {100*r['icm_exact']:5.1f}% "
                      f"(ham {r['icm_ham']:4.1f}) | loo top1 {r['loo_top1']:.2f} "
                      f"bound {r['loo_bound']:.3f} bits {r['loo_bits']:5.3f} | "
                      f"oracle {100*r['oracle']:5.1f}%", flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows:
        print("no runs with a checkpoint under", args.root)
        return 1
    md = [f"# Reconstruction audit — {args.name}", "",
          "`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed "
          "48, in bits per target nucleotide: the conditional extraction has to invert, with the "
          "revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true "
          "token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a "
          "cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token "
          "at a time and sweeps to a fixed point, which is the in-distribution conditional the "
          "surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the "
          "predictor that matches THAT decoder rather than left-to-right decoding: every other "
          "target token held at its true value, one masked, which is the conditional ICM converges "
          "to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to "
          "the number of target tokens, so it is the rate at which a fixed point can be the true "
          "string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: "
          "several restarts, each swept to a fixed point, and the one with the best "
          "pseudo-log-likelihood is output, which an attacker can compute without the truth. "
          "`any-restart` is the oracle over the same restarts and is an upper bound, not an "
          "attack, because choosing it needs the answer.", "",
          "| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['run']} | {r['data']} | {r['tok']} | {r['obj']} | r={r['tier']} | {r['n']} | "
                  f"{r['tgt_bits']:.3f} | {r['top1']:.2f} | "
                  f"{100*r['pre_exact']:.0f}% | {r['loo_bits']:.3f} | {r['loo_top1']:.2f} | "
                  f"{r['loo_bound']:.3f} | **{100*r['icm_exact']:.0f}%** | {r['icm_ham']:.1f} | "
                  f"{100*r['oracle']:.0f}% |")
    mem = [r for r in rows if r["tier"] > 0]
    non = [r for r in rows if r["tier"] == 0]
    if mem and non:
        md += ["", f"Members: target surprise {np.mean([r['tgt_bits'] for r in mem]):.3f} b/nt against "
                   f"{np.mean([r['tgt_bits'] for r in non]):.3f} for the matched non-member control; "
                   f"ICM extraction at worst {100*max(r['icm_exact'] for r in mem):.0f}%."]
    p = Path(args.root[0]) / f"{args.name}.md"
    p.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[-2:]))
    print(f"-> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
