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

RUN = re.compile(r"(?P<tok>char|\d+mer)_(?P<obj>ar|mlm[0-9.]+)_s(?P<seed>\d+)")


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


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/traj1")
    args = ap.parse_args(argv)
    root = Path(args.root)
    rows = []
    for d in sorted(root.iterdir()):
        m = RUN.fullmatch(d.name) if d.is_dir() else None
        if not m:
            continue
        for f in sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem.split("ep")[1])):
            r = json.loads(f.read_text(encoding="utf-8"))
            e = r.get("epoch") or int(f.stem.split("ep")[1])
            row = {"tok": m["tok"], "obj": m["obj"], "seed": int(m["seed"]), "epoch": e,
                   "floor": r["floors"][0]["bits_per_nt_mean"]}
            for t in (1, 4, 16):
                s = summarize(r, t, "train")
                if s:
                    row[f"b{t}"], row[f"r{t}"], row[f"x{t}"] = s
            s0 = summarize(r, 0, "fresh")
            row["fp"] = s0[1] if s0 else float("nan")
            rows.append(row)
    if not rows:
        print("no snapshots under", root); return 1

    md = [f"# Training trajectory — {root}", "",
          "floor = held-out bits/nt (2.000 = generalizes as well as possible on random data; higher = overfit). "
          "b/r/x = probe bits/nt / rank-1 / exact-extraction at tier r (training host). fp = non-member rank-1 (false positives).", "",
          "| tok | obj | seed | epoch | floor | b1 | b4 | b16 | r1 | r4 | r16 | x1 | x4 | x16 | fp |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for w in sorted(rows, key=lambda w: (w["obj"], w["tok"], w["seed"], w["epoch"])):
        g = lambda k, f="{:.3f}": (f.format(w[k]) if k in w and w[k] == w[k] else "—")
        md.append(f"| {w['tok']} | {w['obj']} | {w['seed']} | {w['epoch']} | {g('floor')} | {g('b1')} | {g('b4')} | {g('b16')} | "
                  f"{g('r1','{:.2f}')} | {g('r4','{:.2f}')} | {g('r16','{:.2f}')} | {g('x1','{:.2f}')} | {g('x4','{:.2f}')} | "
                  f"{g('x16','{:.2f}')} | {g('fp','{:.2f}')} |")
    (root / "trajectory.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))

    if plt is None:
        return 0
    by = defaultdict(list)
    for w in rows:
        by[(w["tok"], w["obj"])].append(w)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
    for (tok, obj), ws in sorted(by.items()):
        agg = defaultdict(list)
        for w in ws:
            agg[w["epoch"]].append(w)
        es = sorted(agg)
        mean = lambda k: [np.mean([w[k] for w in agg[e] if k in w]) for e in es]
        lab = f"{tok} {obj}"
        axes[0].plot(es, mean("b16"), marker="o", ms=3, label=f"{lab} r=16")
        axes[0].plot(es, mean("b1"), ls="--", marker=".", ms=3, label=f"{lab} r=1")
        axes[1].plot(es, mean("floor"), marker="o", ms=3, label=lab)
        axes[2].plot(mean("floor"), mean("b16"), marker="o", ms=3, label=f"{lab} r=16")
        axes[2].plot(mean("floor"), mean("b1"), ls="--", marker=".", ms=3, label=f"{lab} r=1")
    axes[0].set_xlabel("epoch"); axes[0].set_ylabel("probe bits/nt"); axes[0].set_title("memorization vs epoch")
    axes[1].set_xlabel("epoch"); axes[1].set_ylabel("held-out bits/nt"); axes[1].set_title("overfitting vs epoch")
    axes[1].axhline(2.0, color="gray", lw=0.8, ls=":")
    axes[2].set_xlabel("held-out bits/nt (overfitting)"); axes[2].set_ylabel("probe bits/nt")
    axes[2].set_title("memorization at matched overfitting")
    for ax in axes:
        ax.legend(fontsize=6)
    fig.tight_layout(); fig.savefig(root / "trajectory.png", dpi=150)
    print(f"-> {root/'trajectory.png'}, {root/'trajectory.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
