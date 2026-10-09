"""Training-trajectory analysis: does a tokenizer memorize MORE, or only SOONER?

    python -m pilot2.analyze_traj --root outputs/traj1

Reads every <run>/scores_ep<N>.json. For each (tokenizer, seed, epoch) reports
the held-out floor (how overfit the model is), probe bits/nt / rank-1 / exact
extraction per tier, and non-member rank-1 (false-positive check).

The comparison that separates "more" from "sooner" is memorization at MATCHED
overfitting: plot probe bits/nt against held-out bits/nt instead of against
epoch. If the coarse tokenizer's curve lies on top of char's once the x-axis is
held-out loss, the effect is speed; if it lies below, it memorizes more at
equal generalization cost.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:  # pragma: no cover
    plt = None

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?|bpe\d+)(?:_(?:ecoli|yeast|gue|human))?_(?P<obj>ar|mlm[0-9.]+)_s(?P<seed>\d+)")


def summarize(r, tier, host):
    sc = "ar" if r["kind"] == "ar" else "pll"
    key = f"{sc}/{host}"
    ps = [p for p in r["probes"] if p["repetitions"] == tier and key in p["ranks"]]
    if not ps:
        return None
    b = np.mean([p["ranks"][key]["probe_bits_per_nt"] for p in ps])
    r1 = np.mean([p["ranks"][key]["rank"] == 1 for p in ps])
    ex = np.mean([p["extract"][host]["exact"] for p in ps])
    return b, r1, ex


GRID = (2.03, 2.05, 2.10, 2.20, 2.40, 3.00)


def matched_table(rows):
    """Probe bits/nt interpolated at fixed held-out floors, per (tok, obj), mean over seeds.

    Each seed's curve is taken from its least-overfit snapshot onward (the floor
    first dips as the model learns, then rises as it overfits), sorted by floor,
    and linearly interpolated; floors outside a curve's range are left blank.
    """
    cur = defaultdict(list)
    for w in rows:
        cur[(w["tok"], w["obj"], w["seed"])].append(w)
    out = defaultdict(lambda: defaultdict(list))
    for (tok, obj, _), ws in cur.items():
        ws = sorted(ws, key=lambda w: w["epoch"])
        ws = ws[int(np.argmin([w["floor"] for w in ws])):]
        ws = sorted(ws, key=lambda w: w["floor"])
        fl = np.array([w["floor"] for w in ws])
        for t in (1, 4, 16):
            if not all(f"b{t}" in w for w in ws):
                continue
            b = np.array([w[f"b{t}"] for w in ws])
            for x in GRID:
                if fl[0] <= x <= fl[-1]:
                    out[(tok, obj, t)][x].append(float(np.interp(x, fl, b)))
    md = ["", "## Memorization at matched overfitting", "",
          "probe bits/nt interpolated at each held-out floor (mean over seeds; — = curve never reaches that floor). "
          "Lower = more memorized; 2.000 = nothing memorized.", "",
          "| tok | obj | tier | " + " | ".join(f"@{x:.2f}" for x in GRID) + " |",
          "|---|---|---|" + "---|" * len(GRID)]
    for (tok, obj, t) in sorted(out, key=lambda k: (k[2], k[1], k[0])):
        v = out[(tok, obj, t)]
        md.append(f"| {tok} | {obj} | r={t} | " + " | ".join(f"{np.mean(v[x]):.3f}" if v.get(x) else "—" for x in GRID) + " |")
    return md


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", default=["outputs/traj1"],
                    help="one or more sweep dirs; with several, runs are tagged by dir name and the outputs go to the first")
    args = ap.parse_args(argv)
    roots = [Path(r) for r in args.root]
    root = roots[0]
    rows = []
    dirs = [(r, d) for r in roots for d in sorted(r.iterdir())]
    for rt, d in dirs:
        m = RUN.fullmatch(d.name) if d.is_dir() else None
        if not m:
            continue
        for f in sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem.split("ep")[1])):
            r = json.loads(f.read_text(encoding="utf-8"))
            e = r.get("epoch") or int(f.stem.split("ep")[1])
            obj = m["obj"] if len(roots) == 1 else f'{m["obj"]}[{rt.name}]'
            row = {"tok": m["tok"], "obj": obj, "seed": int(m["seed"]), "epoch": e,
                   "floor": r["floors"][0]["bits_per_nt_mean"]}
            for t in (1, 4, 16):
                s = summarize(r, t, "train")
                if s:
                    row[f"b{t}"], row[f"r{t}"], row[f"x{t}"] = s
            s0 = summarize(r, 0, "fresh")
            row["fp"] = s0[1] if s0 else float("nan")
            rows.append(row)
    if not rows:
        print("no snapshots under", roots); return 1

    md = [f"# Training trajectory — {', '.join(map(str, roots))}", "",
          "floor = held-out bits/nt (2.000 = generalizes as well as possible on random data; higher = overfit). "
          "b/r/x = probe bits/nt / rank-1 / exact-extraction at tier r (training host). fp = non-member rank-1 (false positives).", "",
          "| tok | obj | seed | epoch | floor | b1 | b4 | b16 | r1 | r4 | r16 | x1 | x4 | x16 | fp |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for w in sorted(rows, key=lambda w: (w["obj"], w["tok"], w["seed"], w["epoch"])):
        g = lambda k, f="{:.3f}": (f.format(w[k]) if k in w and w[k] == w[k] else "—")
        md.append(f"| {w['tok']} | {w['obj']} | {w['seed']} | {w['epoch']} | {g('floor')} | {g('b1')} | {g('b4')} | {g('b16')} | "
                  f"{g('r1','{:.2f}')} | {g('r4','{:.2f}')} | {g('r16','{:.2f}')} | {g('x1','{:.2f}')} | {g('x4','{:.2f}')} | "
                  f"{g('x16','{:.2f}')} | {g('fp','{:.2f}')} |")
    md += matched_table(rows)
    (root / "trajectory.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))

    if plt is None:
        return 0
    by = defaultdict(list)
    for w in rows:
        by[(w["tok"], w["obj"])].append(w)
    fig, axes = plt.subplots(1, 4, figsize=(21, 4.6))
    palette = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for i, ((tok, obj), ws) in enumerate(sorted(by.items())):
        agg = defaultdict(list)
        for w in ws:
            agg[w["epoch"]].append(w)
        es = sorted(agg)
        mean = lambda k: [np.mean([w[k] for w in agg[e] if k in w]) for e in es]
        lab, c = f"{tok} {obj}", palette[i % len(palette)]
        axes[0].plot(es, mean("b16"), color=c, marker="o", ms=3, label=f"{lab} r=16")
        axes[0].plot(es, mean("b1"), color=c, ls="--", marker=".", ms=3, label=f"{lab} r=1")
        axes[1].plot(es, mean("floor"), color=c, marker="o", ms=3, label=lab)
        for ax in axes[2:]:
            ax.plot(mean("floor"), mean("b16"), color=c, marker="o", ms=3, label=f"{lab} r=16")
            ax.plot(mean("floor"), mean("b1"), color=c, ls="--", marker=".", ms=3, label=f"{lab} r=1")
    axes[0].set_xlabel("epoch"); axes[0].set_ylabel("probe bits/nt"); axes[0].set_title("memorization vs epoch")
    axes[1].set_xlabel("epoch"); axes[1].set_ylabel("held-out bits/nt"); axes[1].set_title("overfitting vs epoch")
    axes[1].axhline(2.0, color="gray", lw=0.8, ls=":")
    for ax in axes[2:]:
        ax.set_xlabel("held-out bits/nt (overfitting)"); ax.set_ylabel("probe bits/nt")
    axes[2].set_title("memorization at matched overfitting")
    # the band every tokenizer crosses (6mer AR tops out at ~2.5 held-out bits)
    axes[3].set_xlim(1.995, 2.6); axes[3].set_title("same, zoomed to the shared overfitting range")
    for ax in axes:
        ax.legend(fontsize=6)
    fig.tight_layout(); fig.savefig(root / "trajectory.png", dpi=150)
    print(f"-> {root/'trajectory.png'}, {root/'trajectory.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
