"""Tokenizer curve read at MATCHED held-out loss.

    python -m pilot2.kcurve_report --root outputs/kcurve300

WHY. Comparing tokenizers after the same number of epochs says nothing: they converge at
very different rates, and on uniform DNA every k >= 3 saturates at 100 % extraction by
epoch 30 -- including records planted once -- so the final-epoch table shows 0 / 1 / 1 / 1 / 1
and separates nothing. The comparison that carries the claim is the one section 3.11 used:
read every run at the same held-out bits per nucleotide and ask how much of the planted
record comes back there. A coarse tokenizer then differs from a fine one in two ways that
matter, and both are visible here -- it extracts more at any matched loss, and it reaches
full extraction at a far smaller loss, which is the same "what does the leak cost" currency
the released-model results are reported in.

The x axis is not k. It is the number of token slots the hidden 48 nucleotides occupy,
which is what a decoder has to get right simultaneously: 48/k for a non-overlapping
tokenizer. That is why the released DNABERT family, whose tokens overlap and whose slot
count therefore barely moves with k, shows no trend at all.
"""
from __future__ import annotations

import argparse
import glob
import json
import os

TARGET_FLOORS = (2.05, 2.10, 2.20, 2.40)


def _rate(probes, tier, host):
    hits = [p["extract"][host]["exact"] for p in probes
            if p.get("repetitions") == tier and host in p.get("extract", {})]
    return (sum(1.0 for h in hits if h) / len(hits)) if hits else float("nan")


def series(run_dir):
    """[(held-out bits/nt, r16, r1, control, epoch)] over the snapshots, loss ascending."""
    out = []
    for f in glob.glob(os.path.join(run_dir, "scores_ep*.json")):
        d = json.load(open(f))
        out.append((d["floors"][0]["bits_per_nt_mean"],
                    _rate(d["probes"], 16, "train"), _rate(d["probes"], 1, "train"),
                    _rate(d["probes"], 0, "fresh"), d.get("epoch")))
    return sorted(out)


def at_floor(s, target, col=1):
    """linear interpolation of one column at a given held-out loss; nan outside the range."""
    pts = [(row[0], row[col]) for row in s if row[col] == row[col]]
    if not pts or not (pts[0][0] <= target <= pts[-1][0]):
        return float("nan")
    for (f0, r0), (f1, r1) in zip(pts, pts[1:]):
        if f0 <= target <= f1:
            return r0 if f1 == f0 else r0 + (target - f0) / (f1 - f0) * (r1 - r0)
    return float("nan")


def full_extraction_cost(s, thresh=0.99):
    """the smallest held-out loss at which extraction reaches `thresh` (nan if never)."""
    for floor, r16, _, _, _ in s:
        if r16 == r16 and r16 >= thresh:
            return floor
    return float("nan")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--toks", default="char,2mer,3mer,4mer,5mer,6mer")
    ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--probe_nt", type=int, default=48,
                    help="hidden nucleotides, for the slot count on the x axis")
    args = ap.parse_args(argv)
    toks = [t for t in args.toks.split(",") if t]
    seeds = [int(s) for s in args.seeds.split(",") if s]

    def k_of(t):
        return 1 if t == "char" else int(t.replace("mer", ""))

    curves = {}
    print("Trajectory per run: held-out bits/nt -> exact extraction, 16 copies, training host\n")
    for t in toks:
        for sd in seeds:
            d = os.path.join(args.root, f"{t}_ar_s{sd}")
            if not os.path.isdir(d):
                continue
            curves[(t, sd)] = s = series(d)
            print(f"{t:5s} s{sd} | " + "  ".join(
                f"ep{e}:{f:.2f}/{r:.0%}" for f, r, _, _, e in s))

    print("\n\nExtraction at matched held-out loss (mean over seeds, 16 copies)\n")
    print(f"{'tok':6s} {'slots':>6s}  " + "  ".join(f"@{t:.2f}".rjust(7) for t in TARGET_FLOORS)
          + "   loss at 100%")
    for t in toks:
        have = [sd for sd in seeds if (t, sd) in curves]
        if not have:
            continue
        cells = []
        for target in TARGET_FLOORS:
            v = [at_floor(curves[(t, sd)], target) for sd in have]
            v = [x for x in v if x == x]
            cells.append(f"{sum(v)/len(v):7.0%}" if v else "      -")
        costs = [full_extraction_cost(curves[(t, sd)]) for sd in have]
        costs = [c for c in costs if c == c]
        cost = f"{sum(costs)/len(costs):.2f}" if costs else "never"
        print(f"{t:6s} {args.probe_nt // k_of(t):6d}  " + "  ".join(cells) + f"   {cost:>12s}")

    print("\nControl, never-trained records on a fresh host (max over all snapshots and seeds)")
    for t in toks:
        c = [x for sd in seeds if (t, sd) in curves
             for row in curves[(t, sd)] for x in [row[3]] if x == x]
        print(f"  {t:6s} {max(c):.2f}" if c else f"  {t:6s} -")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
