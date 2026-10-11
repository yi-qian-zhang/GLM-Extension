"""The paper's figures, as vector PDFs, built from the saved score files.

    python -m pilot2.figures_paper --out outputs/figures_paper [--only objective]

F1 objective   the objective x tokeniser grid on all five datasets (replaces a wide table)
F2 mechanism   per-nucleotide against per-slot memorisation, and excess against token corpus count
F3 variance    share of variance by factor, random against fixed canary placement
F4 delay       150-round trajectories: the character cell only postpones extraction

Every panel is drawn at the paper's text width (6.5 in) or half of it, in 8 pt serif to match 10 pt
Times body text, with no LaTeX dependency.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from .analyze_objaxis import collect as collect_obj

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "pdf.fonttype": 42, "savefig.bbox": "tight", "savefig.pad_inches": 0.01,
})
INK = "#1A2333"
C_AR, C_M15, C_M50 = "#C2410C", "#3B8686", "#7C8CA3"
TOKS = ["char", "3mer", "4mer", "6mer"]
TOKLAB = {"char": "char", "3mer": "3-mer", "4mer": "4-mer", "6mer": "6-mer"}
DATASETS = [("synthetic", ["outputs/core_all"], "synthetic"),
            ("ecoli", ["outputs/ecoli_ar", "outputs/ecoli_mlm"], "E. coli"),
            ("yeast", ["outputs/yeast_ar", "outputs/yeast_mlm"], "yeast"),
            ("gue", ["outputs/gue_ar", "outputs/gue_mlm"], "GUE promoters"),
            ("human", ["outputs/human_toy", "outputs/human_mlm"], "human chr22")]


def _save(fig, out: Path, stem: str):
    """PDF for the paper, PNG at 220 dpi for reading the figure on screen and for slides."""
    fig.savefig(out / f"{stem}.pdf")
    fig.savefig(out / f"{stem}.png", dpi=220)


def _style(ax, grid="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis=grid, lw=0.3, color="#B9C0CC", alpha=0.7)
    ax.set_axisbelow(True)


def fig_objective(out: Path, epoch=30, tier=16):
    """Excess per cell, three objectives side by side, one panel per dataset; a cross marks a cell
    whose planted records come back verbatim."""
    fig, axes = plt.subplots(2, len(DATASETS), figsize=(6.5, 2.9), sharey="row",
                             gridspec_kw={"height_ratios": [2.1, 1.0]}, constrained_layout=True)
    series = [("ar", C_AR, "next-token"), ("mlm@0.15", C_M15, "masked 15%"),
              ("mlm@0.5", C_M50, "masked 50%")]
    w = 0.26
    for col_i, (key, roots, label) in enumerate(DATASETS):
        g = collect_obj(roots, key, tier)
        for row, keep in enumerate((None, "masked")):       # row 1 repeats the masked cells, zoomed
            ax = axes[row, col_i]
            for si, (obj, col, lab) in enumerate(series):
                if keep == "masked" and obj == "ar":
                    continue
                xs, ys, ex = [], [], []
                for ti, t in enumerate(TOKS):
                    v = g.get((t, obj)) or g.get((t, obj.replace("0.5", "0.50")))
                    if not v or epoch not in v:
                        continue
                    a = np.array(v[epoch]).mean(0)
                    xs.append(ti + (si - 1) * w)
                    ys.append(a[1])
                    ex.append(a[2])
                if not xs:
                    continue
                ax.bar(xs, ys, width=w, color=col, linewidth=0,
                       label=lab if (row == 0 and col_i == 0) else None)
                if row == 0:
                    for x, y, e in zip(xs, ys, ex):
                        if e > 0.5:
                            ax.plot([x], [y + 0.18], marker="x", ms=3.2, mew=0.9, color=INK, clip_on=False)
            ax.set_xticks(range(len(TOKS)))
            ax.set_xticklabels([TOKLAB[t] for t in TOKS] if row == 1 else [], rotation=45, ha="right")
            ax.set_ylim(0, 4.8 if row == 0 else 0.36)
            if row == 0:
                ax.set_title(label)
            _style(ax)
    axes[0, 0].set_ylabel("excess bits/nt")
    axes[1, 0].set_ylabel("masked only")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels + ["$\\times$ = every planted record reproduced verbatim"],
               frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.09),
               handlelength=1.0, columnspacing=1.4)
    _save(fig, out, "F1_objective")
    plt.close(fig)
    return "F1_objective.pdf"


def fig_mechanism(out: Path, info="outputs/ecoli_ar/ecoli_token_info.json", tier=16):
    """(a) memorised bits per nucleotide and (b) per token slot against held-out loss; (c) excess at
    a matched loss against how often the canary's tokens occur elsewhere in the corpus."""
    d = json.loads(Path(info).read_text(encoding="utf-8"))
    rows = [r for r in d["rows"] if r["tier"] == tier]
    toks = [t for t in ["char", "3mer", "4mer", "bpe4096", "6mer"] if any(r["tok"] == t for r in rows)]
    cols = dict(zip(["char", "3mer", "4mer", "bpe4096", "6mer"],
                    ["#7C8CA3", "#D9822B", "#A9742B", "#3B8686", "#C2410C"]))
    lab = {"char": "char", "3mer": "3-mer", "4mer": "4-mer", "bpe4096": "BPE-4096", "6mer": "6-mer"}
    fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.05), constrained_layout=True)
    for ax, field, ylab, title in ((axes[0], "mem_bits_nt", "memorised bits/nt", "(a) per nucleotide"),
                                   (axes[1], "mem_bits_tok", "memorised bits/slot", "(b) per token slot")):
        for t in toks:
            v = sorted([(r["floor"], r[field]) for r in rows if r["tok"] == t])
            if len(v) < 2:
                continue
            ax.plot([x for x, _ in v], [y for _, y in v], color=cols[t], lw=1.0, marker="o", ms=2.0,
                    label=lab[t] if ax is axes[0] else None)
        ax.set_xlabel("held-out loss (bits/nt)")
        ax.set_ylabel(ylab)
        ax.set_title(title)
        _style(ax)
    axes[0].legend(frameon=False, handlelength=1.2, borderpad=0.1)
    ax = axes[2]
    st = d["stats"]
    xs, ys, ls = [], [], []
    for t in toks:
        if t not in st:
            continue
        v = [(r["floor"], r["mem_bits_nt"]) for r in rows if r["tok"] == t]
        if not v:
            continue
        f = np.array([x for x, _ in v]); y = np.array([y for _, y in v])
        o = np.argsort(f)
        xs.append(max(st[t]["canary_token_corpus_count_mean"], 0.5))
        ys.append(float(np.interp(2.10, f[o], y[o])))
        ls.append(lab[t])
    ax.scatter(xs, ys, s=14, color=[cols[t] for t in toks if t in st], zorder=3)
    for x, y, l in zip(xs, ys, ls):
        ax.annotate(l, (x, y), textcoords="offset points", xytext=(3, 3), fontsize=6.5, color=INK)
    ax.set_xscale("log")
    ax.set_xlabel("corpus count of the canary's tokens")
    ax.set_xlim(20, 1e6)
    ax.set_ylabel("memorised bits/nt at loss 2.10")
    ax.set_title("(c) rarity predicts the ordering")
    _style(ax, grid="both")
    _save(fig, out, "F2_mechanism")
    plt.close(fig)
    return "F2_mechanism.pdf"


def fig_variance(out: Path):
    """Shares from `python -m pilot2.analyze_tok --root outputs/core_all --tier 16` (random
    placement, 24 runs) and the same command on outputs/tok1 (fixed placement, 18 runs); the
    three-tokeniser subset of core_all gives 57.7 / 15.4 / 26.9 / 0.0, printed in the caption."""
    labels = ["objective", "tokeniser", "interaction", "seed"]
    rand = [67.1, 12.0, 21.0, 0.0]
    fixed = [25.7, 59.5, 14.0, 0.8]
    cols = ["#C2410C", "#3B8686", "#D9BC8B", "#B9C0CC"]
    fig, ax = plt.subplots(figsize=(3.2, 1.05), constrained_layout=True)
    for i, (name, vals) in enumerate((("drawn offsets\n(every number in this paper)", rand),
                                      ("fixed offsets", fixed))):
        left = 0.0
        for v, c, l in zip(vals, cols, labels):
            ax.barh([i], [v], left=left, color=c, height=0.55, linewidth=0,
                    label=l if i == 0 else None)
            if v >= 8:
                ax.text(left + v / 2, i, f"{v:.0f}%", ha="center", va="center", fontsize=6.5,
                        color="white" if c != "#D9BC8B" else INK)
            left += v
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["drawn offsets", "fixed offsets"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("share of variance in canary memorisation (%)")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.42),
              handlelength=0.9, columnspacing=1.0, borderpad=0.0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="y", length=0)
    _save(fig, out, "F3_variance")
    plt.close(fig)
    return "F3_variance.pdf"


def fig_delay(out: Path, root="outputs/human_long", tier=16):
    """Excess and verbatim extraction over a 150-round schedule: the character cell is late, not
    safe, and by the time it reproduces everything its held-out loss has collapsed."""
    runs = {}
    for d in sorted(Path(root).iterdir()):
        if not d.is_dir():
            continue
        tok = d.name.split("_")[0]
        pts = []
        for f in sorted(d.glob("scores_ep*.json"), key=lambda q: int(q.stem.split("ep")[1])):
            r = json.loads(f.read_text(encoding="utf-8"))
            key = next((k.split("/")[0] for p in r["probes"] for k in p["ranks"]), None)
            mem = [p for p in r["probes"] if p["repetitions"] == tier and f"{key}/train" in p["ranks"]]
            ctl = [p for p in r["probes"] if p["repetitions"] == 0 and f"{key}/fresh" in p["ranks"]]
            if not mem or not ctl:
                continue
            ex = float(np.mean([p["extract"]["train"]["exact"] for p in mem]))
            b = float(np.mean([p["ranks"][f"{key}/train"]["probe_bits_per_nt"] for p in mem]))
            c = float(np.mean([p["ranks"][f"{key}/fresh"]["probe_bits_per_nt"] for p in ctl]))
            pts.append((int(f.stem.split("ep")[1]), r["floors"][0]["bits_per_nt_mean"], c - b, ex))
        if pts:
            runs.setdefault(tok, []).append(pts)
    cols = {"char": "#7C8CA3", "6mer": "#C2410C"}
    lab = {"char": "char", "6mer": "6-mer"}
    fig, axes = plt.subplots(1, 2, figsize=(3.3, 1.9), sharex=True, constrained_layout=True)
    for tok, rs in runs.items():
        eps = [p[0] for p in rs[0]]
        ext = np.mean([[p[3] for p in r] for r in rs], axis=0)
        fl = np.mean([[p[1] for p in r] for r in rs], axis=0)
        axes[0].plot(eps, 100 * ext, color=cols.get(tok, INK), lw=1.1, marker="o", ms=2.2,
                     label=f"{lab.get(tok, tok)} ({len(rs)} seed{'s' if len(rs) > 1 else ''})")
        axes[1].plot(eps, fl, color=cols.get(tok, INK), lw=1.1, marker="o", ms=2.2)
    axes[0].set_ylabel("verbatim extraction (%)")
    axes[0].set_ylim(-3, 103)
    axes[1].set_ylabel("held-out loss (bits/nt)")
    axes[1].axhline(2.0, color=INK, lw=0.5, ls=":")
    for ax in axes:
        ax.set_xlabel("round")
        _style(ax)
    axes[0].legend(frameon=False, loc="center right", handlelength=1.1, borderpad=0.1)
    _save(fig, out, "F4_delay")
    plt.close(fig)
    return "F4_delay.pdf"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/figures_paper")
    ap.add_argument("--only", default=None, choices=["objective", "mechanism", "variance", "delay"])
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    jobs = {"objective": fig_objective, "mechanism": fig_mechanism,
            "variance": fig_variance, "delay": fig_delay}
    for name, fn in jobs.items():
        if args.only and name != args.only:
            continue
        try:
            print("wrote", fn(out), flush=True)
        except Exception as e:                      # one bad panel should not block the others
            print(f"FAILED {name}: {type(e).__name__}: {e}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
