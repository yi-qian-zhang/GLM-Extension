"""Figures for the NIH proposal update (Aims 1.1 / 1.2) and the paper, built from the saved reports.

    python -m pilot2.figures_proposal --out outputs/figures

F1  variance decomposition, fixed vs random canary placement (tok1 vs core_all)
F2  memorisation at matched held-out loss, synthetic (core100) and E. coli (ecoli_ar), r=1 canaries
F3  DNABERT family: r=16 recognition at epoch 30 by k (training host / new host), 3 seeds; 100-epoch trajectories
F4  canary position: r=16 recognition in a new host, absolute vs relative positions (off1 / rope_rand)
F5  real models: r=16 canary bits/nt over epochs, HyenaDNA vs DNABERT-6 (causal)
All panels: 'memorised' = (2 - bits/nt) / 2 on uniform DNA.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = {"char": "#7C8CA3", "3mer": "#D9822B", "6mer": "#C2410C", "ink": "#1A2333", "mint": "#3B8686"}
KC = {3: "#9DB2BF", 4: "#D9822B", 5: "#A93F0A", 6: "#C2410C"}
mem = lambda b: max(0.0, (2.0 - b) / 2.0 * 100.0)


def matched_table(md: Path):
    """Parse the '## Memorization at matched overfitting' table -> {(tok, tier): {floor: bits}}."""
    out, grid = {}, None
    for line in md.read_text(encoding="utf-8").splitlines():
        if line.startswith("| tok | obj | tier |"):
            grid = [float(x.strip("@ ")) for x in line.split("|")[4:-1]]
        elif grid and re.match(r"\| (char|\dmer\w*) \| ", line):
            c = [x.strip() for x in line.split("|")[1:-1]]
            tier = int(c[2].split("=")[1])
            out[(c[0], tier)] = {g: float(v) for g, v in zip(grid, c[3:]) if v != "—"}
    return out


def dnabert_rows(report: Path, variant: str):
    rows = {}
    for line in report.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"| {variant} | "):
            c = [x.strip() for x in line.split("|")[1:-1]]
            if c[2].startswith("r="):          # matched-floor section, different layout
                continue
            k, ep, fl = int(c[1]), int(c[2]), float(c[3])
            cells = [tuple(float(v) for v in x.split(" / ")) for x in c[4:8]]
            rows[(k, ep)] = (fl, cells)   # cells: r1 train, r4 train, r16 train, r16 fresh
    return rows


def hyena_curve(root: Path, name: str):
    pts = {}
    for f in root.glob(f"{name}/scores_ep*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        ps = [p for p in r["probes"] if p["repetitions"] == 16]
        pts[int(r["epoch"])] = np.mean([p["ranks"]["causal/train"]["probe_bits_per_nt"] for p in ps])
    f = root / name / "scores_final.json"
    if f.exists():
        r = json.loads(f.read_text(encoding="utf-8"))
        ps = [p for p in r["probes"] if p["repetitions"] == 16]
        pts[int(r["epoch"])] = np.mean([p["ranks"]["causal/train"]["probe_bits_per_nt"] for p in ps])
    return dict(sorted(pts.items()))


def style(ax, title, xl, yl):
    ax.set_title(title, loc="left", fontsize=11, color=C["ink"], pad=8)
    ax.set_xlabel(xl); ax.set_ylabel(yl)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="y", color="#E2E1DB", lw=0.8); ax.set_axisbelow(True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="outputs/figures")
    args = ap.parse_args(argv)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    O = Path("outputs")

    # ---------------- F1 variance decomposition
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    labels = ["Tokenizer", "Objective", "Interaction", "Seed"]
    fixed = [59.5, 25.7, 14.0, 0.8]
    rnd = [15.4, 57.7, 26.9, 0.0]
    x = np.arange(4); w = 0.38
    ax.bar(x - w / 2, fixed, w, color="#9DB2BF", label="canaries at a fixed position")
    ax.bar(x + w / 2, rnd, w, color=C["6mer"], label="canaries at random positions")
    for i in range(4):
        ax.text(x[i] - w / 2, fixed[i] + 1, f"{fixed[i]:.0f}%", ha="center", fontsize=9)
        ax.text(x[i] + w / 2, rnd[i] + 1, f"{rnd[i]:.0f}%", ha="center", fontsize=9)
    ax.set_xticks(x, labels); ax.set_ylim(0, 70); ax.legend(frameon=False, fontsize=9)
    style(ax, "Share of variance in canary memorisation (fixed backbone)", "", "share of variance (%)")
    fig.tight_layout(); fig.savefig(out / "F1_variance.png", dpi=200); plt.close(fig)

    # ---------------- F2 matched-floor curves, synthetic + E. coli
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6), sharey=True)
    for ax, (root, title) in zip(axes, ((O / "core100", "Synthetic iid DNA (100 canaries, 3 seeds)"), (O / "ecoli_ar", "E. coli genome (50 canaries, 2 seeds)"))):
        t = matched_table(root / "trajectory.md")
        for tok, lab in (("char", "1-mer"), ("3mer", "3-mer"), ("6mer", "6-mer")):
            d = t.get((tok, 1), {})
            xs = sorted(d); ax.plot(xs, [mem(d[g]) for g in xs], "o-", color=C[tok], lw=2.2, ms=5, label=lab)
        style(ax, title, "held-out loss, bits/nt (overfitting)", "canary memorised (%)")
        ax.set_xlim(2.0, 2.45); ax.legend(frameon=False, fontsize=9)
    fig.suptitle("Memorisation of a canary seen once, at matched held-out loss (causal objective, random placement)", fontsize=10, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(out / "F2_matched_floor.png", dpi=200); plt.close(fig)

    # ---------------- F3 DNABERT family
    rows = dnabert_rows(O / "dnabert" / "dnabert_report.md", "causal")
    e100 = dnabert_rows(O / "dnabert_e100" / "dnabert_report.md", "causal") if (O / "dnabert_e100" / "dnabert_report.md").exists() else {}
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
    ax = axes[0]
    ks = [3, 4, 5, 6]; x = np.arange(4); w = 0.38
    tr = [rows[(k, 30)][1][2][1] * 100 for k in ks]; fr = [rows[(k, 30)][1][3][1] * 100 for k in ks]
    ax.bar(x - w / 2, tr, w, color="#9DB2BF", label="in its training sequence")
    ax.bar(x + w / 2, fr, w, color=C["6mer"], label="in a new sequence, new position")
    for i in range(4):
        ax.text(x[i] - w / 2, tr[i] + 2, f"{tr[i]:.0f}%", ha="center", fontsize=9); ax.text(x[i] + w / 2, fr[i] + 2, f"{fr[i]:.0f}%", ha="center", fontsize=9)
    ax.set_xticks(x, [f"{k}-mer" for k in ks]); ax.set_ylim(0, 125); ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    style(ax, "Recognised after 30 epochs (rank 1 of 101), 3 seeds", "DNABERT variant", "recognised (%)")
    ax = axes[1]
    for k in ks:
        pts = sorted((e, v) for (kk, e), v in e100.items() if kk == k and e > 0)
        if pts:
            ax.plot([e for e, _ in pts], [mem(v[1][2][0]) for _, v in pts], "o-", color=KC[k], lw=2, ms=4, label=f"{k}-mer")
    style(ax, "Memorised over 100 epochs (one seed)", "epoch", "canary memorised (%)")
    ax.legend(frameon=False, fontsize=9)
    fig.suptitle("Canary seen 16x — pretrained DNABERT family fine-tuned with canaries (same architecture, data, objective; only k differs)", fontsize=10, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95)); fig.savefig(out / "F3_dnabert_family.png", dpi=200); plt.close(fig)

    # ---------------- F4 position
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    toks = ["1-mer", "3-mer", "6-mer"]; x = np.arange(3); w = 0.26
    vals = {"absolute positions, canaries at one fixed offset": [100, 100, 100],
            "absolute positions, random offsets": [0, 2, 39],
            "relative positions (RoPE), random offsets": [0, 30, 80]}
    cols = ["#9DB2BF", C["6mer"], C["3mer"]]
    for i, (lab, v) in enumerate(vals.items()):
        ax.bar(x + (i - 1) * w, v, w, color=cols[i], label=lab)
        for j in range(3):
            ax.text(x[j] + (i - 1) * w, v[j] + 2, f"{v[j]}%", ha="center", fontsize=8.5)
    ax.set_xticks(x, toks); ax.set_ylim(0, 150); ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=1)
    style(ax, "Canary seen 16x, placed in a new sequence (from-scratch backbone)", "", "recognised (%)")
    fig.tight_layout(); fig.savefig(out / "F4_position.png", dpi=200); plt.close(fig)

    # ---------------- F5 real models over epochs
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    hy = hyena_curve(O / "hyena", "hyena_medium-160k_s0")
    if hy:
        ax.plot(list(hy), [mem(v) for v in hy.values()], "o-", color=C["char"], lw=2.2, ms=5, label="HyenaDNA medium (1-mer, causal pretraining)")
    for k in (3, 6):
        pts = sorted((e, v) for (kk, e), v in rows.items() if kk == k)
        ax.plot([e for e, _ in pts], [mem(v[1][2][0]) for _, v in pts], "s-", color=KC[k], lw=2, ms=4, label=f"DNABERT {k}-mer (masked pretraining, causal fine-tuning)")
    style(ax, "Canary seen 16x: memorised over fine-tuning, lr 2e-5, random placement", "epoch", "canary memorised (%)")
    ax.legend(frameon=False, fontsize=8.5)
    fig.tight_layout(); fig.savefig(out / "F5_real_models.png", dpi=200); plt.close(fig)
    print("->", sorted(p.name for p in out.glob("F*.png")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
