"""The re-masking decoder for OVERLAPPING k-mer models, which is the only form it can take there.

    python -m pilot2.recon_overlap --root outputs/dnabert_long --restarts 16 --gpu 2

WHY THIS FILE EXISTS, SEPARATELY FROM recon_audit.
`pilot2/recon_audit.py` re-masks one TOKEN at a time. On a non-overlapping vocabulary -- our own
k-mers, NT's 4096 non-overlapping 6-mers, DNABERT-2's BPE -- that is exactly the conditional the
model was trained on, and it takes a masked model from 0 % to 95 % verbatim reproduction. On
DNABERT it is not merely weaker, it is undefined:

  * DNABERT tokenises with stride 1, so token t is the k-mer starting at nucleotide t and any valid
    token string satisfies token_t[1:] == token_{t+1}[:k-1]. Changing one token alone contradicts
    the 2(k-1) tokens overlapping it, and the result decodes to no DNA string at all.
  * Even if it decoded, five of a 6-mer's six letters are still visible in its neighbours, so a
    single-token conditional is answerable from context with no memorisation whatever, and a
    leave-one-out accuracy near 1.00 there would mean nothing.
  * Hiding 48 nucleotides needs every token overlapping them, i.e. 48 + (k-1) tokens, which is about
    48 FOR EVERY k. The joint-slot count is pinned to the nucleotide count.

The latent variable is the nucleotide string, not the token string, so the correct analogue is
ITERATED CONDITIONAL MODES IN NUCLEOTIDE SPACE: to re-mask nucleotide j, mask the k tokens covering
j, read the distribution over the four letters at j, take its mode, and sweep. DNABERT's own
pretraining defines that conditional, and `pilot2.dnabert.nt_logprobs` already computes it exactly,
renormalised over ACGT; `nt_dist` below is that function returning all four letters instead of only
the true one.

WHAT THE RESULT MEANS EITHER WAY. Our mechanism claim is that the number of joint slots sets the
price of recovery: 8 slots for a non-overlapping 6-mer against 16 for a 3-mer is 95 % against 0 %.
Overlapping k-mers pin the slot count at ~48 for every k, so that claim PREDICTS a flat profile
across DNABERT k=3,4,5,6. A flat profile here beside the 0-to-95 split on the non-overlapping axis
is evidence for the mechanism that neither measurement gives alone, and it is evidence on released
checkpoints rather than on a backbone we trained. A large spread across k here would refute the
mechanism, which is worth knowing before the abstract is written.

Updates are sequential across positions, because parallel ones oscillate, and batched across
restarts, which is what makes 16-128 restarts affordable: one model call per (position, sweep) with
the restarts as the batch.
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

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, decode, random_dna
from .dnabert import KmerVocab, load_model
from .real_data import DATA_PATHS, build_real_dataset

RUN = re.compile(r"dnabert(?P<k>[3-6])_.*_s(?P<seed>\d+)$")


@torch.no_grad()
def nt_dist(model, voc: KmerVocab, nt: torch.Tensor, positions, device, rows_per_batch=256):
    """log2 p(letter | everything except the k tokens covering j), shape (B, P, 4).

    This is pilot2.dnabert.nt_logprobs with the readout opened up: that function returns the
    probability of the nucleotide actually present at j, which is what a scorer needs, while a
    decoder needs the whole distribution so it can take the mode. Everything else -- which tokens
    are masked, which k-mers are consistent with the letters still visible inside the read token,
    the marginalisation onto the letter at j's offset and the renormalisation over ACGT -- is
    unchanged, so the conditional is the same one the surprise ruler reads.
    """
    k, B, W = voc.k, nt.shape[0], nt.shape[1]
    T = voc.n_tokens(W)
    ids = voc.encode(nt).to(device)
    P = len(positions)
    letters = voc.letters.to(device)
    kmer_ids = voc.kmer_ids.to(device)
    out = torch.full((B, P, 4), float("-inf"), device=device)
    wpb = max(1, rows_per_batch // max(1, P))
    for b0 in range(0, B, wpb):
        xb = ids[b0:b0 + wpb]
        w = xb.shape[0]
        rep = xb[:, None, :].expand(w, P, -1).clone()
        tread = []
        for pi, j in enumerate(positions):
            lo, hi = max(0, j - k + 1), min(j, T - 1)
            rep[:, pi, lo + 1:hi + 2] = voc.mask          # +1 for [CLS]
            tread.append(min(j, T - 1))
        tread = torch.tensor(tread, device=device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            logits = model(input_ids=rep.reshape(w * P, -1)).logits.float()
        logits = logits.reshape(w, P, -1, logits.shape[-1])
        at = logits[torch.arange(w)[:, None], torch.arange(P)[None, :], tread[None, :] + 1]
        lk = at[..., kmer_ids]
        ntb = nt[b0:b0 + wpb].to(device)
        for pi, j in enumerate(positions):
            t0 = int(tread[pi])
            off = j - t0
            cons = torch.ones(w, 4 ** k, dtype=torch.bool, device=device)
            for i in range(k):
                if i == off:
                    continue
                cons &= letters[:, i][None, :] == ntb[:, t0 + i, None]
            lp = lk[:, pi].masked_fill(~cons, float("-inf"))
            m = torch.full((w, 4), float("-inf"), device=device)
            for a in range(4):
                sel = letters[:, off] == a + 1
                m[:, a] = torch.logsumexp(lp[:, sel], dim=1)
            out[b0:b0 + w, pi] = (m - torch.logsumexp(m, dim=1, keepdim=True)) / math.log(2.0)
    return out


@torch.no_grad()
def icm_nt(model, voc: KmerVocab, win: np.ndarray, offset: int, device, k_nt: int = 48,
           restarts: int = 16, sweeps: int = 4, seed: int = 0):
    """Reveal win[:offset+k_nt]; recover the next 48 nucleotides by nucleotide-level ICM.

    Returns the attack's own choice (the fixed point with the best pseudo-log-likelihood, which an
    attacker can compute without the answer), the oracle over the same restarts as an upper bound,
    and the leave-one-out statistics that say whether the record is stored at all.
    """
    start, end = offset + k_nt, offset + PROBE_LEN
    target = list(range(start, end))
    truth = win[start:end].copy()
    g = np.random.default_rng(seed)

    # restarts as the batch: one model call per (position, sweep) instead of one per restart
    cur = np.tile(win[None, :], (restarts, 1)).copy()
    cur[0, start:end] = 1                                     # a fixed start, for reproducibility
    if restarts > 1:
        cur[1:, start:end] = g.integers(1, 5, size=(restarts - 1, end - start))

    for _ in range(sweeps):
        changed = 0
        for j in target:                                      # sequential: parallel updates oscillate
            d = nt_dist(model, voc, torch.from_numpy(cur), [j], device)[:, 0]      # (R, 4)
            new = (d.argmax(1) + 1).cpu().numpy()
            changed += int((new != cur[:, j]).sum())
            cur[:, j] = new
        if changed == 0:
            break

    # truth-free score for each fixed point: sum_j log2 p(cur_j | rest of cur)
    d = nt_dist(model, voc, torch.from_numpy(cur), target, device)                 # (R, P, 4)
    idx = torch.from_numpy(cur[:, start:end] - 1).long().to(device)
    pll = d.gather(2, idx[..., None])[..., 0].sum(1).cpu().numpy()                 # (R,)
    best = int(np.argmax(pll))
    ham = [int((cur[r, start:end] != truth).sum()) for r in range(restarts)]

    # leave-one-out: every other target nucleotide at its TRUE value, one unknown. This is the
    # conditional ICM converges to and the one the surprise ruler reads, so its per-position top-1
    # rate is what predicts whether a fixed point can be the true string at all.
    tw = np.tile(win[None, :], (1, 1)).copy()
    tw[0, start:end] = truth
    dl = nt_dist(model, voc, torch.from_numpy(tw), target, device)[0]              # (P, 4)
    loo_top1 = float((dl.argmax(1).cpu().numpy() + 1 == truth).mean())
    loo_bits = float(-dl.gather(1, torch.from_numpy(truth - 1).long().to(device)[:, None]).sum())
    return {"protocol": f"icm-nt-r{restarts}", "n_generated_nt": len(target), "restarts": restarts,
            "exact": bool(ham[best] == 0), "hamming_nt": ham[best],
            "oracle_exact": bool(min(ham) == 0), "ham_by_restart": ham,
            "loo_top1": loo_top1, "loo_bits_per_nt": loo_bits / len(target),
            "loo_bound": loo_top1 ** len(target),
            "pred_nt": decode(cur[best, start:end]), "truth_nt": decode(truth)}


def rebuild(d: Path, device, ckpt: str):
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    model, voc = load_model(int(a["k"]), device)   # load_model returns (model, KmerVocab)
    model.load_state_dict(torch.load(d / ckpt, map_location=device))
    model.eval()
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    # dnabert.py hardcodes n_val=n_test=200 and does not record it; getting this wrong would move
    # every probe host, so it is spelled out rather than defaulted silently
    ds = build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], a["n_train"], 200, 200,
                            a["probes_per_tier"], tiers, a["n_nonmember"], a["data_seed"],
                            offset_mode=a["probe_offset"], canary_npz=a.get("canary_npz"))
    return model, voc, ds, a


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--max_probes", type=int, default=20)
    ap.add_argument("--restarts", type=int, default=16)
    ap.add_argument("--sweeps", type=int, default=4)
    ap.add_argument("--ckpt", default="final.pt")
    ap.add_argument("--name", default="recon_overlap")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    tiers = [int(t) for t in args.tiers.split(",")]

    rows = []
    for root in args.root:
        rd = Path(root)
        dirs = [rd] if (rd / "args.json").exists() else sorted(p for p in rd.iterdir() if p.is_dir())
        for d in dirs:
            if not ((d / "args.json").exists() and (d / args.ckpt).exists() and RUN.fullmatch(d.name)):
                continue
            model, voc, ds, a = rebuild(d, device, args.ckpt)
            rng = np.random.default_rng(10_000 + a["seed"])
            real_hosts = getattr(ds, "fresh_hosts", None)
            per = defaultdict(lambda: defaultdict(list))
            cells = []
            for tier in tiers + [0]:
                ps = [p for p in ds.probes if p.repetitions == tier][:args.max_probes]
                for p in ps:
                    if tier > 0:
                        host, off = ds.train[p.host_rows[0]].copy(), p.offsets[0]
                    else:
                        host = (real_hosts[p.probe_id % len(real_hosts)].copy()
                                if real_hosts is not None else random_dna(rng, 1, WINDOW)[0])
                        off = PROBE_OFFSET
                    win = host.copy()
                    win[off:off + PROBE_LEN] = p.seq
                    r = icm_nt(model, voc, win, off, device, restarts=args.restarts,
                               sweeps=args.sweeps, seed=1000 * int(p.probe_id) + tier)
                    v = per[tier]
                    v["exact"].append(float(r["exact"]))
                    v["ham"].append(r["hamming_nt"])
                    v["oracle"].append(float(r["oracle_exact"]))
                    v["loo_top1"].append(r["loo_top1"])
                    v["loo_bits"].append(r["loo_bits_per_nt"])
                    v["loo_bound"].append(r["loo_bound"])
                    cells.append({"tier": tier, "probe_id": p.probe_id, "icm_nt": r})
            (d / f"{args.name}.json").write_text(
                json.dumps({"run": d.name, "k": a["k"], "data": a.get("data"), "seed": a["seed"],
                            "ckpt": args.ckpt, "cells": cells}, indent=1), encoding="utf-8")
            for t in sorted(per, reverse=True):
                m = lambda key: float(np.mean(per[t][key])) if per[t][key] else float("nan")
                rows.append(dict(run=d.name, k=int(a["k"]), data=a.get("data"), seed=a["seed"],
                                 tier=t, n=len(per[t]["exact"]), exact=m("exact"), ham=m("ham"),
                                 oracle=m("oracle"), loo_top1=m("loo_top1"),
                                 loo_bits=m("loo_bits"), loo_bound=m("loo_bound")))
                r = rows[-1]
                print(f"  {d.name:34s} r={t:<3d} n={r['n']:3d} | loo top1 {r['loo_top1']:.2f} "
                      f"bits {r['loo_bits']:5.3f} bound {r['loo_bound']:.3f} | icm-nt "
                      f"{100*r['exact']:5.1f}% (ham {r['ham']:4.1f}) | oracle {100*r['oracle']:5.1f}%",
                      flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows:
        print("no DNABERT cells with a checkpoint under", args.root)
        return 1
    md = [f"# Nucleotide-level re-masking on DNABERT's overlapping k-mers — {args.name}", "",
          "One TOKEN at a time is undefined on a stride-1 vocabulary: changing a token contradicts "
          "the ones overlapping it and decodes to no DNA string, and a token's letters are anyway "
          "visible in its neighbours. So the latent variable is the nucleotide string and the "
          "conditional is DNABERT's own: to re-mask nucleotide j, mask the k tokens covering j, "
          "marginalise onto the letter at j and renormalise over ACGT. `loo top1` is the per-position "
          "accuracy with every other target nucleotide at its true value, so it says whether the "
          "record is stored; `icm-nt` is the attack, choosing between fixed points by "
          "pseudo-log-likelihood, and `oracle` is the upper bound over the same restarts.", "",
          "Hiding 48 nucleotides takes 48+(k-1) tokens here, i.e. about 48 slots for EVERY k, so the "
          "joint-slot mechanism predicts a FLAT profile across k. A large spread would refute it.", "",
          "| run | k | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-nt exact | ham | any-restart |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['run']} | {r['k']} | {r['data']} | {r['seed']} | r={r['tier']} | {r['n']} | "
                  f"{r['loo_top1']:.2f} | {r['loo_bits']:.3f} | {r['loo_bound']:.3f} | "
                  f"**{100*r['exact']:.0f}%** | {r['ham']:.1f} | {100*r['oracle']:.0f}% |")
    mem = [r for r in rows if r["tier"] > 0]
    if mem:
        ks = sorted({r["k"] for r in mem})
        spread = {k: max(r["exact"] for r in mem if r["k"] == k) for k in ks}
        md += ["", "Best member extraction by k: " + ", ".join(f"k={k} {100*v:.0f}%" for k, v in spread.items())
               + f" (spread {100*(max(spread.values())-min(spread.values())):.0f} points)."]
    p = Path(args.root[0]) / f"{args.name}.md"
    p.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[-2:]))
    print(f"-> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
