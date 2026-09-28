"""Tokenizer x objective grid: memorization table and a first-pass variance
decomposition (the paper's headline shape).

    python -m pilot2.analyze_tok --root outputs/tok1 [--tier 16] [--host train]

Response y = probe bits/nt at the chosen tier, from each model's natural
scorer (ar for causal; both pll and prefix reported for masked, pll used for
the decomposition). Factors: tokenizer, objective; replicate = seed.
Decomposition is the classical two-way sums of squares on cell means with a
seed residual; with an unbalanced grid it is reported as eta^2 of main effects
computed from marginal means (flagged).
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

NAME = re.compile(r"(?P<tok>char|\d+mer)_(?P<obj>ar|mlm[0-9.]+)_s(?P<seed>\d+)")


def load(root: Path):
    out = []
    for f in sorted(root.glob("*/scores_final.json")):
        m = NAME.fullmatch(f.parent.name)
        if not m:
            continue
        out.append((m["tok"], m["obj"], int(m["seed"]), json.loads(f.read_text(encoding="utf-8"))))
    return out


def probe_stats(r, tier, host, scorer):
    key = f"{scorer}/{host}"
    ps = [p for p in r["probes"] if p["repetitions"] == tier and key in p["ranks"]]
    if not ps:
        return None
    bits = np.array([p["ranks"][key]["probe_bits_per_nt"] for p in ps])
    r1 = np.array([p["ranks"][key]["rank"] == 1 for p in ps])
    ex = np.array([p["extract"][host]["exact"] for p in ps])
    return bits.mean(), r1.mean(), ex.mean()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/tok1")
    ap.add_argument("--tier", type=int, default=16)
    ap.add_argument("--host", default="train")
    args = ap.parse_args(argv)
    runs = load(Path(args.root))
    toks = [t for t in ("char", "3mer", "6mer") if any(r[0] == t for r in runs)]
    objs = sorted({r[1] for r in runs}, key=lambda o: (o != "ar", o))

    cells = defaultdict(list)          # (tok,obj) -> list of dict per seed
    floors = defaultdict(list)
    for tok, obj, seed, r in runs:
        scs = ["ar"] if obj == "ar" else ["pll", "prefix"]
        row = {"seed": seed}
        for sc in scs:
            st = probe_stats(r, args.tier, args.host, sc)
            if st:
                row[sc] = st
        for fl in r["floors"]:
            floors[(tok, obj, fl["scorer"])].append(fl["bits_per_nt_mean"])
        row["n_params"] = r["train_summary"]["n_params"]
        row["supervised"] = r["train_summary"].get("supervised_tokens_seen", 0)
        cells[(tok, obj)].append(row)

    md = [f"# Tokenizer x objective — {args.root}", "",
          f"tier r={args.tier}, host={args.host}; mean over seeds (n per cell shown). bits/nt: chance = 2.000", "",
          "| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for tok in toks:
        for obj in objs:
            rows = cells.get((tok, obj), [])
            if not rows:
                md.append(f"| {tok} | {obj} | 0 | — | — | — | — | — | — | — |"); continue
            for sc in (["ar"] if obj == "ar" else ["pll", "prefix"]):
                vals = np.array([row[sc] for row in rows if sc in row])
                if not len(vals):
                    continue
                b, r1, ex = vals.mean(0)
                bsd = vals[:, 0].std()
                fl = np.mean(floors[(tok, obj, sc)])
                md.append(f"| {tok} | {obj} | {len(vals)} | {sc} | {b:.3f}±{bsd:.3f} | {r1:.2f} | {ex:.2f} | {fl:.4f} | "
                          f"{rows[0]['n_params']/1e6:.2f}M | {np.mean([x['supervised'] for x in rows])/1e6:.0f}M |")

    # ---- variance decomposition on natural scorer (ar / pll)
    ys, T, O = [], [], []
    for (tok, obj), rows in cells.items():
        sc = "ar" if obj == "ar" else "pll"
        for row in rows:
            if sc in row:
                ys.append(row[sc][0]); T.append(tok); O.append(obj)
    y = np.array(ys); grand = y.mean(); sst = ((y - grand) ** 2).sum()
    T, O = np.array(T), np.array(O)
    def ss_main(f):
        return sum((f == lv).sum() * (y[f == lv].mean() - grand) ** 2 for lv in np.unique(f))
    ss_t, ss_o = ss_main(T), ss_main(O)
    cell_mean = {(t, o): y[(T == t) & (O == o)].mean() for t in np.unique(T) for o in np.unique(O) if ((T == t) & (O == o)).any()}
    ss_cells = sum(((T == t) & (O == o)).sum() * (m - grand) ** 2 for (t, o), m in cell_mean.items())
    ss_int = ss_cells - ss_t - ss_o
    ss_res = sst - ss_cells
    balanced = len({((T == t) & (O == o)).sum() for (t, o) in cell_mean}) == 1 and len(cell_mean) == len(np.unique(T)) * len(np.unique(O))
    md += ["", f"## Variance decomposition of r={args.tier} probe bits/nt (natural scorer; n={len(y)} runs)", "",
           "| source | SS | share of total |", "|---|---|---|"]
    for lab, ss in (("tokenizer", ss_t), ("objective", ss_o), ("tokenizer x objective", ss_int), ("seed (residual)", ss_res)):
        md.append(f"| {lab} | {ss:.4f} | **{ss / sst:.1%}** |")
    md.append(f"| total | {sst:.4f} | 100% |")
    if not balanced:
        md.append("\n> Grid is unbalanced (a cell is missing or has fewer seeds); shares are approximate.")

    # ---- the same, within masked models only (does tokenizer matter once objective is fixed?)
    mask = np.array([o != "ar" for o in O])
    if mask.sum() > 3:
        yy, TT = y[mask], T[mask]; g = yy.mean(); st = ((yy - g) ** 2).sum()
        sst_t = sum((TT == lv).sum() * (yy[TT == lv].mean() - g) ** 2 for lv in np.unique(TT))
        md.append(f"\nWithin masked models only: tokenizer explains **{sst_t / st:.1%}** of the variance (n={mask.sum()}).")
    maskar = np.array([o == "ar" for o in O])
    if maskar.sum() > 2:
        yy, TT = y[maskar], T[maskar]; g = yy.mean(); st = ((yy - g) ** 2).sum()
        sst_t = sum((TT == lv).sum() * (yy[TT == lv].mean() - g) ** 2 for lv in np.unique(TT))
        md.append(f"Within causal models only: tokenizer explains **{sst_t / st:.1%}** of the variance (n={maskar.sum()}).")

    out = Path(args.root) / f"tok_analysis_r{args.tier}_{args.host}.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md)); print(f"\n-> {out}")


if __name__ == "__main__":
    main()
