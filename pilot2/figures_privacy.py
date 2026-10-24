"""The privacy-first paper's figures, built from the published derived table.

    python -m pilot2.figures_privacy --out paper/figures

F5 slots   extraction against the slot count at matched held-out loss, and what full
           extraction costs; the window-288 sweep overlaid as a replication
F6 ident   DNABERT-2 on chromosome 22: identification of a single-copy haplotype rises to
           0.94 while verbatim recovery of the same records stays at zero
F7 blind   the number practitioners select on, beside the leak from the same weights

WHY THE INPUT IS A CSV. The score files these numbers come from are 725 MB and are not in
the repository; `results/figure_data.csv` is the flattened table that is (27k rows, 2.3 MB,
written by `pilot2.export_figure_data`). Reading the figures from the same file a reader can
download means the figures and the tables cannot disagree, and it was checked: the matched-loss
cells recomputed here reproduce Table 3 of the paper exactly, cell for cell, including the
window-288 replication column.

Style follows `figures_paper.py`: 6.5 in text width, 8 pt serif, no LaTeX dependency.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.01,
})
INK = "#1A2333"
C_ID, C_VERB, C_UTIL, C_REF = "#C2410C", "#3B8686", "#1E4F8A", "#7C8CA3"
TARGETS = (2.05, 2.10, 2.20, 2.40)
TOKS = ["char", "2mer", "3mer", "4mer", "5mer", "6mer"]
SLOTS = {"char": 48, "2mer": 24, "3mer": 16, "4mer": 12, "5mer": 9.6, "6mer": 8}
TOKLAB = {"char": "char", "2mer": "2-mer", "3mer": "3-mer", "4mer": "4-mer",
          "5mer": "5-mer", "6mer": "6-mer"}


def _save(fig, out: Path, stem: str):
    fig.savefig(out / f"{stem}.pdf")
    fig.savefig(out / f"{stem}.png", dpi=220)
    print(f"  wrote {stem}.pdf / .png")


def _style(ax, grid="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis=grid, lw=0.3, color="#B9C0CC", alpha=0.7)
    ax.set_axisbelow(True)


def load(csv_path: Path):
    return list(csv.DictReader(open(csv_path, encoding="utf-8")))


# --------------------------------------------------------------- matched-loss reading
def series(rows, group, run, tier="16", host="train", drop_final=True):
    """[(held-out bits/nt, exact rate)] over a run's snapshots, loss ascending.

    The final snapshot is dropped so this matches `kcurve_report.py`, which globs
    `scores_ep*.json` only; including it would move the interpolation at 2.40 by a point or
    two and the figure would stop agreeing with the table.
    """
    pts = [(float(r["heldout_bits_per_nt"]), float(r["exact_rate"])) for r in rows
           if r["group"] == group and r["run"] == run and r["tier"] == tier
           and r["host"] == host and not (drop_final and r["epoch"] == "final")]
    return sorted(pts)


def at(pts, target):
    if not pts or not (pts[0][0] <= target <= pts[-1][0]):
        return None
    for (f0, r0), (f1, r1) in zip(pts, pts[1:]):
        if f0 <= target <= f1:
            return r0 if f1 == f0 else r0 + (target - f0) / (f1 - f0) * (r1 - r0)
    return None


def cost_of_full(pts, thresh=0.99):
    for floor, rate in pts:
        if rate >= thresh:
            return floor
    return None


def matched(rows, group, seeds=(0, 1, 2)):
    """{tok: ([rate at each target or None], cost of 100% or None)}, averaged over seeds."""
    table = {}
    for tok in TOKS:
        per_seed, costs = [], []
        for sd in seeds:
            s = series(rows, group, f"{tok}_ar_s{sd}")
            if not s:
                continue
            per_seed.append([at(s, t) for t in TARGETS])
            costs.append(cost_of_full(s))
        if not per_seed:
            continue
        cells = []
        for i in range(len(TARGETS)):
            v = [c[i] for c in per_seed if c[i] is not None]
            cells.append(sum(v) / len(v) if v else None)
        cc = [c for c in costs if c is not None]
        table[tok] = (cells, sum(cc) / len(cc) if cc else None)
    return table


def fig_slots(rows, out: Path):
    """(a) extraction against slot count at four matched losses; (b) what 100% costs."""
    main, repl = matched(rows, "kcurve300"), matched(rows, "kcurve")
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(6.5, 2.25), constrained_layout=True,
                                   gridspec_kw={"width_ratios": [1.35, 1.0]})

    toks = [t for t in TOKS if t in main]
    x = list(range(len(toks)))                      # categorical: slots fall left to right
    shades = ["#C9D2DE", "#8FA3BC", "#4F6B90", "#1E4F8A"]
    for ti, target in enumerate(TARGETS):
        y = [main[t][0][ti] for t in toks]
        xs = [xi for xi, yi in zip(x, y) if yi is not None]
        ys = [yi for yi in y if yi is not None]
        axa.plot(xs, ys, "-o", color=shades[ti], ms=3.2, lw=1.1,
                 label=f"held-out {target:.2f}")
    # the second geometry, as hollow markers at the loss where the rates are largest
    ti = len(TARGETS) - 1
    xs = [xi for xi, t in zip(x, toks) if t in repl and repl[t][0][ti] is not None]
    ys = [repl[t][0][ti] for t in toks if t in repl and repl[t][0][ti] is not None]
    axa.plot(xs, ys, "o", mfc="none", mec=INK, ms=5.5, mew=0.7,
             label="window 300$\\to$288, @2.40")

    axa.set_xticks(x)
    axa.set_xticklabels([f"{TOKLAB[t]}\n{SLOTS[t]:g}" for t in toks])
    axa.set_xlabel("tokenizer, and token slots the hidden 48 nt occupy")
    axa.set_ylabel("records returned verbatim")
    axa.set_ylim(-0.03, 1.0)
    axa.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    axa.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
    axa.annotate("never reaches\nthese losses", xy=(0.012, 0.09), xycoords="axes fraction",
                 color=C_REF, fontsize=6.5, ha="left")
    axa.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.06, 1.03), ncol=2,
               handlelength=1.6, columnspacing=1.2)
    _style(axa)

    have = [t for t in toks if main[t][1] is not None]
    axb.plot([x[toks.index(t)] for t in have], [main[t][1] for t in have], "-s",
             color=C_ID, ms=3.4, lw=1.1, label="window 300")
    have2 = [t for t in toks if t in repl and repl[t][1] is not None]
    axb.plot([x[toks.index(t)] for t in have2], [repl[t][1] for t in have2], "o",
             mfc="none", mec=INK, ms=5.5, mew=0.7, label="window 288")
    for t in toks:
        if main.get(t, (None, None))[1] is None:
            axb.annotate("never", xy=(x[toks.index(t)], 2.36), fontsize=6.5,
                         color=C_REF, ha="center", va="bottom")
    axb.set_xticks(x)
    axb.set_xticklabels([TOKLAB[t] for t in toks])
    axb.set_xlabel("tokenizer")
    axb.set_ylabel("bits/nt at 100% extraction")
    axb.set_ylim(2.3, 4.5)
    axb.legend(frameon=False, loc="upper right", handlelength=1.6)
    _style(axb)
    _save(fig, out, "F5_slots")


# --------------------------------------------------------------- the divergence figure
EPOCH_X = {"15": 15, "30": 30, "50": 50, "80": 80, "120": 120, "final": 150}


def _band(rows, group, runs, tier, host, field):
    """{epoch: (mean, lo, hi)} across seeds for one measured field."""
    byep = {}
    for r in rows:
        if r["group"] == group and r["run"] in runs and r["tier"] == tier and r["host"] == host:
            byep.setdefault(r["epoch"], []).append(float(r[field]))
    return {e: (sum(v) / len(v), min(v), max(v)) for e, v in byep.items()}


def _plot_band(ax, d, color, label, marker="o"):
    eps = sorted(d, key=lambda e: EPOCH_X[e])
    xs = [EPOCH_X[e] for e in eps]
    ax.fill_between(xs, [d[e][1] for e in eps], [d[e][2] for e in eps],
                    color=color, alpha=0.15, lw=0)
    ax.plot(xs, [d[e][0] for e in eps], "-" + marker, color=color, ms=3.2, lw=1.1, label=label)


def fig_ident(rows, out: Path):
    """DNABERT-2 on chr22: identification climbs, verbatim recovery does not move."""
    runs = {f"dnabert2bpe_human_s{s}" for s in (0, 1, 2)}
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.1), sharey=True, constrained_layout=True)
    for ax, tier, title in ((axes[0], "1", "one copy: the realistic case"),
                            (axes[1], "16", "sixteen copies")):
        _plot_band(ax, _band(rows, "bpe_human", runs, tier, "train", "rank1_rate"),
                   C_ID, "identified against 100 real rare segments")
        _plot_band(ax, _band(rows, "bpe_human", runs, tier, "train", "exact_rate"),
                   C_VERB, "returned verbatim", marker="s")
        _plot_band(ax, _band(rows, "bpe_human", runs, "0", "fresh", "rank1_rate"),
                   C_REF, "never-trained control", marker="^")
        ax.axhline(0.01, color=C_REF, lw=0.5, ls=":")
        ax.set_title(title, color=INK)
        ax.set_xlabel("fine-tuning round")
        ax.set_ylim(-0.04, 1.04)
        ax.set_xlim(0, 160)
        _style(ax)
    axes[0].set_ylabel("rate")
    axes[0].set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    axes[0].set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
    axes[0].annotate("chance 0.0099", xy=(84, 0.035), fontsize=6.5, color=C_REF)
    axes[1].legend(frameon=False, loc="upper left", bbox_to_anchor=(0.14, 0.86),
                   handlelength=1.6)
    _save(fig, out, "F6_ident")


# --------------------------------------------------------------- the blind-metric figure
def _util(path: Path):
    """[(round, held-out bits, MCC, single-copy identification)] from utility_at_leak.

    Two kinds of entry have to be dropped: one carrying a downstream score and no leak
    numbers (written when the utility probe ran on a checkpoint the scorer had not reached),
    and the `final` entry, which is the last round again under a different label. Both would
    otherwise appear as extra points on the x axis.
    """
    rows = []
    for e in json.loads(path.read_text(encoding="utf-8")):
        lp = e.get("downstream", {}).get("linear_probe", {})
        if "mcc" not in lp or e.get("floor") is None:
            continue
        rows.append((EPOCH_X.get(str(e["epoch"]), 150), e["floor"], lp["mcc"],
                     e.get("r1_recognition")))
    seen, floors, keep = set(), set(), []
    for r in sorted(rows):
        if r[0] in seen or round(r[1], 6) in floors:
            continue
        seen.add(r[0])
        floors.add(round(r[1], 6))
        keep.append(r)
    return keep


def fig_blind(res: Path, out: Path):
    """Downstream score against the leak, on the two released models fine-tuned on chr22."""
    panels = [("DNABERT-2 117M", [res / "bpe_human" / f"dnabert2bpe_human_s{s}"
                                  / "utility_at_leak.json" for s in (0, 1, 2)]),
              ("NT 250M", [res / "nt_ckpt" / "nt250m_mlm_human_s0" / "utility_at_leak.json"])]
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.1), constrained_layout=True)
    for ax, (name, paths) in zip(axes, panels):
        got = [_util(p) for p in paths if p.exists()]
        if not got:
            continue
        xs = [r[0] for r in got[0]]
        mcc = [[r[2] for r in g] for g in got]
        idr = [[r[3] for r in g] for g in got]
        n = min(len(m) for m in mcc)
        mean = lambda col, i: sum(c[i] for c in col) / len(col)
        ax.fill_between(xs[:n], [min(c[i] for c in mcc) for i in range(n)],
                        [max(c[i] for c in mcc) for i in range(n)], color=C_UTIL,
                        alpha=0.15, lw=0)
        ax.plot(xs[:n], [mean(mcc, i) for i in range(n)], "-o", color=C_UTIL, ms=3.2, lw=1.1,
                label="downstream MCC (left)")
        ax.set_ylim(0.70, 0.84)
        ax.set_ylabel("MCC, GUE promoters", color=C_UTIL)
        ax.tick_params(axis="y", colors=C_UTIL)
        ax.set_xlabel("fine-tuning round")
        ax.set_title(name + ", chromosome 22", color=INK)
        _style(ax)

        ax2 = ax.twinx()
        ax2.plot(xs[:n], [mean(idr, i) for i in range(n)], "--s", color=C_ID, ms=3.2, lw=1.1,
                 label="single-copy identification (right)")
        ax2.set_ylim(-0.04, 1.04)
        ax2.set_ylabel("identification, one copy", color=C_ID)
        ax2.tick_params(axis="y", colors=C_ID)
        ax2.spines["top"].set_visible(False)
        best = max(range(n), key=lambda i: mean(mcc, i))
        ax.annotate("best MCC", xy=(xs[best], mean(mcc, best)), xytext=(5, 4),
                    textcoords="offset points", fontsize=6.5, color=C_UTIL)
        if ax is axes[0]:
            h1, l1 = ax.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            ax.legend(h1 + h2, l1 + l2, frameon=False, loc="lower left", handlelength=1.8)
    _save(fig, out, "F7_blind")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results", help="directory holding figure_data.csv")
    ap.add_argument("--out", default="paper/figures")
    ap.add_argument("--only", default=None, help="slots | ident | blind")
    args = ap.parse_args(argv)

    res, out = Path(args.results), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = load(res / "figure_data.csv")
    print(f"{len(rows)} rows from {res / 'figure_data.csv'}")
    if args.only in (None, "slots"):
        fig_slots(rows, out)
    if args.only in (None, "ident"):
        fig_ident(rows, out)
    if args.only in (None, "blind"):
        fig_blind(res, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
