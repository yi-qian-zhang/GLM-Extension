"""E2 dose-response figures from a mask-rate sweep.

    python -m pilot2.plot_e2 --root outputs/e2lite

x-axis: mask rate m (causal AR plotted at m = 1.0, since "predict the next
token from the prefix" is the limit of masking everything to the right).
Panels:
  (1) probe bits/nt by tier vs m, per scorer          -- the dose-response
  (2) rank-1 rate and exact-extraction rate vs m       -- discoverable vs extractable
  (3) held-out floor per scorer vs m                   -- where pll and prefix re-converge
Also writes e2_table.md with the numbers.
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


def mask_rate(name: str) -> float:
    if name.startswith("ar"):
        return 1.0
    m = re.match(r"(?:\w+_)?mlm([0-9.]+)_s\d+", name)
    return float(m.group(1))


def load(root: Path, scores_name="scores_final.json"):
    runs = {}
    for f in sorted(root.glob(f"*/{scores_name}")):
        if "smoke" in str(f):
            continue
        runs[f.parent.name] = json.loads(f.read_text(encoding="utf-8"))
    return runs


def collect(runs):
    """-> rows[(m, scorer, host, tier)] = list over seeds of dict(bits, rank1, exact)"""
    rows = defaultdict(list)
    floors = defaultdict(list)  # (m, scorer) -> floor bits
    for name, r in runs.items():
        m = mask_rate(name)
        for fl in r["floors"]:
            floors[(m, fl["scorer"])].append(fl["bits_per_nt_mean"])
        by = defaultdict(list)
        for p in r["probes"]:
            for key, v in p["ranks"].items():
                sc, host = key.split("/")
                ex = p["extract"][host]
                by[(sc, host, p["repetitions"])].append((v["probe_bits_per_nt"], v["rank"] == 1, ex["exact"]))
        for (sc, host, tier), vals in by.items():
            a = np.array(vals, dtype=float)
            rows[(m, sc, host, tier)].append({"bits": a[:, 0].mean(), "rank1": a[:, 1].mean(), "exact": a[:, 2].mean()})
    return rows, floors


def agg(lst, key):
    v = np.array([d[key] for d in lst])
    return v.mean(), v.std()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/e2lite")
    ap.add_argument("--host", default="fresh", help="fresh | train (members only)")
    args = ap.parse_args(argv)
    root = Path(args.root)
    runs = load(root)
    if not runs:
        print("no runs under", root); return 1
    rows, floors = collect(runs)
    ms = sorted({k[0] for k in rows})
    tiers = sorted({k[3] for k in rows})
    scorers = ["ar", "pll", "prefix"]

    # ---- table
    md = [f"# E2 mask-rate sweep — {root}", "", f"host = {args.host}; values are mean over seeds (± std)", ""]
    md += ["| m | scorer | " + " | ".join(f"r={t} bits/nt" for t in tiers) + " | " +
           " | ".join(f"r={t} rank-1" for t in tiers) + " | " + " | ".join(f"r={t} exact" for t in tiers) + " | floor |",
           "|---|---|" + "---|" * (3 * len(tiers) + 1)]
    for m in ms:
        for sc in scorers:
            cells = []
            for stat in ("bits", "rank1", "exact"):
                for t in tiers:
                    lst = rows.get((m, sc, args.host, t)) or rows.get((m, sc, "fresh", t))
                    if lst:
                        mu, sd = agg(lst, stat)
                        cells.append(f"{mu:.3f}±{sd:.3f}" if stat == "bits" else f"{mu:.2f}")
                    else:
                        cells.append("—")
            fl = floors.get((m, sc))
            if any(c != "—" for c in cells):
                md.append(f"| {m:.2f} | {sc} | " + " | ".join(cells) + f" | {np.mean(fl):.4f} |" if fl else " | — |")
    (root / "e2_table.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))

    if plt is None:
        return 0
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.6))
    # (1) bits/nt vs m
    ax = axes[0]
    for sc, ls in (("pll", "-"), ("prefix", "--")):
        for t in tiers:
            xs, ys, es = [], [], []
            for m in ms:
                lst = rows.get((m, sc, args.host, t)) or rows.get((m, sc, "fresh", t))
                if lst:
                    mu, sd = agg(lst, "bits"); xs.append(m); ys.append(mu); es.append(sd)
            if xs:
                ax.errorbar(xs, ys, yerr=es, ls=ls, marker="o", ms=4, label=f"{sc} r={t}")
    for t in tiers:  # AR point at m=1
        lst = rows.get((1.0, "ar", args.host, t)) or rows.get((1.0, "ar", "fresh", t))
        if lst:
            mu, sd = agg(lst, "bits"); ax.errorbar([1.0], [mu], yerr=[sd], marker="s", ms=7, ls="none", label=f"ar r={t}")
    ax.axhline(2.0, color="gray", lw=0.8, ls=":"); ax.set_xlabel("mask rate m  (AR = 1.0)"); ax.set_ylabel("probe bits / nt")
    ax.set_title("memorization vs mask rate"); ax.legend(fontsize=7, ncol=2)
    # (2) rank-1 and exact vs m
    ax = axes[1]
    for stat, ls in (("rank1", "-"), ("exact", "--")):
        for t in tiers:
            xs, ys = [], []
            for m in ms:
                sc = "ar" if m == 1.0 else "pll"
                lst = rows.get((m, sc, args.host, t)) or rows.get((m, sc, "fresh", t))
                if lst:
                    xs.append(m); ys.append(agg(lst, stat)[0])
            if xs:
                ax.plot(xs, ys, ls=ls, marker="o", ms=4, label=f"{stat} r={t}")
    ax.set_xlabel("mask rate m  (AR = 1.0)"); ax.set_ylabel("rate"); ax.set_ylim(-0.02, 1.02)
    ax.set_title("discoverable (rank-1) vs extractable (exact)"); ax.legend(fontsize=7, ncol=2)
    # (3) floors vs m
    ax = axes[2]
    for sc, mk in (("pll", "o"), ("prefix", "s"), ("ar", "^")):
        xs = [m for m in ms if (m, sc) in floors]
        ys = [np.mean(floors[(m, sc)]) for m in xs]
        if xs:
            ax.plot(xs, ys, marker=mk, label=sc)
    ax.axhline(2.0, color="gray", lw=0.8, ls=":"); ax.set_xlabel("mask rate m"); ax.set_ylabel("held-out bits / nt")
    ax.set_title("scorer calibration vs mask rate"); ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(root / "e2_dose_response.png", dpi=150)
    print(f"-> {root/'e2_dose_response.png'}, {root/'e2_table.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
