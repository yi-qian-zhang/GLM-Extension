"""The re-masking decoder for a VARIABLE-LENGTH (BPE) vocabulary, i.e. DNABERT-2.

    python -m pilot2.recon_bpe --root outputs/dnabert_long --restarts 16 --gpu 0

WHY A THIRD FILE. The decoder that takes a masked model from 0 % to 95 % re-masks one unit at a time
and sweeps to a fixed point. What "one unit" means depends on the vocabulary, and all three cases are
genuinely different:

  pilot2/recon_audit.py    fixed-width non-overlapping k-mers (ours, and NT's 4096 6-mers). One TOKEN
                           at a time; token t always covers nucleotides [t*k, (t+1)*k).
  pilot2/recon_overlap.py  overlapping stride-1 k-mers (DNABERT). One token at a time is undefined,
                           because neighbouring tokens share k-1 nucleotides and a changed token
                           decodes to no DNA string. One NUCLEOTIDE at a time, masking the k tokens
                           that cover it.
  this file                BPE. Tokens have no fixed length and no fixed boundaries: changing one
                           nucleotide RE-SEGMENTS the window, so there is no persistent token grid to
                           iterate over at all. The latent variable is again the nucleotide string.

THE SCORE. For candidate letter a at nucleotide j: write a into the window, re-tokenise, mask every
token whose nucleotide span covers j, and read the model's log-probability of those tokens' true
identities. Different candidates re-segment differently and so mask different numbers of tokens
covering different numbers of nucleotides, which makes raw log-probabilities incomparable -- the
standard length bias of BPE likelihoods. Dividing by the nucleotides those masked tokens cover
removes it, and bits per nucleotide is the unit every scorer in this paper already uses. The mode of
that 4-way distribution is the ICM update.

WHAT IT IS FOR. DNABERT-2 is the second released tokeniser family with a FEW-SLOT target, and the
only one besides NT. Under the standard protocol it already reaches 30 % verbatim on E. coli at
0.026 bits past its own utility optimum (3.46(a)). If the search decoder lifts that the way it lifted
NT from 35 % to 70 %, the under-reporting result rests on two independent released families rather
than one. If it does not, the result is NT-specific and the paper has to say so.

Restarts are batched and positions are swept sequentially, as in recon_overlap: parallel updates
oscillate, and batching the restarts is what makes a 4-candidate score per position affordable.
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
from .dnabert2 import BpeVocab, _logits, load_model
from .real_data import DATA_PATHS, build_real_dataset

RUN = re.compile(r"dnabert2bpe_.*$")
NTS = "ACGT"


@torch.no_grad()
def nt_dist_bpe(model, voc: BpeVocab, wins: np.ndarray, j: int, device, chunk: int = 128):
    """log2 p(letter at j | the rest of the window), shape (B, 4), one row per window in `wins`.

    For each candidate the window is re-tokenised, every token whose span covers j is masked, and the
    score is the summed log-probability of those tokens' true identities divided by the nucleotides
    they cover -- per nucleotide, because candidates re-segment differently and raw token
    log-probabilities are not comparable across segmentations.
    """
    B = wins.shape[0]
    jobs, meta = [], []
    for b in range(B):
        for a in range(4):
            w = wins[b].copy()
            w[j] = a + 1
            ids, spans = voc.encode_str(decode(w))
            cover = [t for t, (s, e) in enumerate(spans) if s <= j < e]
            if not cover:                                 # j fell outside every span: cannot happen
                jobs.append(ids); meta.append((b, a, [], 1)); continue
            nts = sum(spans[t][1] - spans[t][0] for t in cover)
            masked = list(ids)
            true = [ids[t + 1] for t in cover]            # +1 for [CLS]
            for t in cover:
                masked[t + 1] = voc.mask
            jobs.append(masked)
            meta.append((b, a, [(t + 1, tid) for t, tid in zip(cover, true)], nts))

    out = torch.full((B, 4), float("-inf"), device=device)
    for c0 in range(0, len(jobs), chunk):
        sl = slice(c0, c0 + chunk)
        ids, am = voc.pad_batch(jobs[sl], device)
        lp = F.log_softmax(_logits(model, ids, am), dim=-1) / math.log(2.0)
        for r, (b, a, pos_tok, nts) in enumerate(meta[sl]):
            tot = 0.0
            for p, tid in pos_tok:
                tot += float(lp[r, p, tid])
            out[b, a] = tot / max(1, nts)
    return out


@torch.no_grad()
def icm_bpe(model, voc: BpeVocab, win: np.ndarray, offset: int, device, k_nt: int = 48,
            restarts: int = 16, sweeps: int = 4, seed: int = 0):
    """Reveal win[:offset+k_nt]; recover the next 48 nucleotides by ICM in nucleotide space."""
    start, end = offset + k_nt, offset + PROBE_LEN
    target = list(range(start, end))
    truth = win[start:end].copy()
    g = np.random.default_rng(seed)

    cur = np.tile(win[None, :], (restarts, 1)).copy()
    cur[0, start:end] = 1
    if restarts > 1:
        cur[1:, start:end] = g.integers(1, 5, size=(restarts - 1, end - start))

    n_sweeps = 0
    for _ in range(sweeps):
        changed, n_sweeps = 0, n_sweeps + 1
        for j in target:
            d = nt_dist_bpe(model, voc, cur, j, device)
            new = (d.argmax(1) + 1).cpu().numpy()
            changed += int((new != cur[:, j]).sum())
            cur[:, j] = new
        if changed == 0:
            break

    # truth-free selection: the summed per-nucleotide score of the fixed point it converged to
    score = np.zeros(restarts)
    for j in target:
        d = nt_dist_bpe(model, voc, cur, j, device).cpu().numpy()
        score += d[np.arange(restarts), cur[:, j] - 1]
    best = int(np.argmax(score))
    ham = [int((cur[r, start:end] != truth).sum()) for r in range(restarts)]

    # leave-one-out: every other target nucleotide at its TRUE value, one unknown
    tw = win.copy()[None, :]
    tw[0, start:end] = truth
    hits, bits = [], 0.0
    for j in target:
        d = nt_dist_bpe(model, voc, tw, j, device)[0]
        hits.append(bool(int(d.argmax()) + 1 == int(tw[0, j])))
        bits -= float(d[int(tw[0, j]) - 1])
    loo = float(np.mean(hits))
    return {"protocol": f"icm-bpe-r{restarts}", "sweeps_used": n_sweeps, "restarts": restarts,
            "n_generated_nt": len(target), "exact": bool(ham[best] == 0), "hamming_nt": ham[best],
            "oracle_exact": bool(min(ham) == 0), "ham_by_restart": ham,
            "loo_top1": loo, "loo_bits_per_nt": bits / len(target),
            "loo_bound": loo ** len(target),
            "pred_nt": decode(cur[best, start:end]), "truth_nt": decode(truth)}


def rebuild(d: Path, device, ckpt: str):
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    model, voc = load_model(device, causal=(a.get("objective") == "causal"))
    model.load_state_dict(torch.load(d / ckpt, map_location=device))
    model.eval()
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    # dnabert2.py hardcodes n_val=n_test=200 without recording it; a wrong value would relocate
    # every probe host into a window the model never trained on
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
    ap.add_argument("--name", default="recon_bpe")
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
            per, cells = defaultdict(lambda: defaultdict(list)), []
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
                    r = icm_bpe(model, voc, win, off, device, restarts=args.restarts,
                                sweeps=args.sweeps, seed=1000 * int(p.probe_id) + tier)
                    v = per[tier]
                    for key in ("exact", "oracle_exact"):
                        v[key].append(float(r[key]))
                    v["ham"].append(r["hamming_nt"])
                    v["loo_top1"].append(r["loo_top1"])
                    v["loo_bits"].append(r["loo_bits_per_nt"])
                    v["loo_bound"].append(r["loo_bound"])
                    cells.append({"tier": tier, "probe_id": p.probe_id, "icm_bpe": r})
            (d / f"{args.name}.json").write_text(
                json.dumps({"run": d.name, "data": a.get("data"), "seed": a["seed"],
                            "ckpt": args.ckpt, "cells": cells}, indent=1), encoding="utf-8")
            for t in sorted(per, reverse=True):
                m = lambda key: float(np.mean(per[t][key])) if per[t][key] else float("nan")
                rows.append(dict(run=d.name, data=a.get("data"), seed=a["seed"], tier=t,
                                 n=len(per[t]["exact"]), exact=m("exact"), ham=m("ham"),
                                 oracle=m("oracle_exact"), loo_top1=m("loo_top1"),
                                 loo_bits=m("loo_bits"), loo_bound=m("loo_bound")))
                r = rows[-1]
                print(f"  {d.name:26s} r={t:<3d} n={r['n']:3d} | loo top1 {r['loo_top1']:.2f} "
                      f"bits {r['loo_bits']:5.3f} bound {r['loo_bound']:.3f} | icm-bpe "
                      f"{100*r['exact']:5.1f}% (ham {r['ham']:4.1f}) | oracle {100*r['oracle']:5.1f}%",
                      flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows:
        print("no DNABERT-2 cells with a checkpoint under", args.root)
        return 1
    md = [f"# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — {args.name}", "",
          "BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the "
          "window and there is no persistent token grid to iterate over. The latent variable is the "
          "nucleotide string: for each candidate letter the window is re-tokenised, every token whose "
          "span covers that position is masked, and the score is the summed log-probability of those "
          "tokens divided by the nucleotides they cover -- per nucleotide, because candidates "
          "re-segment differently and raw BPE log-probabilities carry a length bias.", "",
          "| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['run']} | {r['data']} | {r['seed']} | r={r['tier']} | {r['n']} | "
                  f"{r['loo_top1']:.2f} | {r['loo_bits']:.3f} | {r['loo_bound']:.3f} | "
                  f"**{100*r['exact']:.0f}%** | {r['ham']:.1f} | {100*r['oracle']:.0f}% |")
    p = Path(args.root[0]) / f"{args.name}.md"
    p.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"-> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
