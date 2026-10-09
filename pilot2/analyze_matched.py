"""Matched-utility comparison for real data, with the non-member control subtracted.

    python -m pilot2.analyze_matched --root outputs/human_real2 --name human
    python -m pilot2.analyze_matched --root outputs/dnabert_ecoli outputs/hyena_ecoli --name ecoli

Two corrections that a fixed-epoch table on real data gets wrong.

1. **Matched utility, not matched epoch.** Models reach their own best held-out loss at different
   epochs and overfit at different rates, so a column at epoch 50 compares models at different points
   of their own trajectories. Here every model's canary score is interpolated onto a common grid of
   held-out loss values, taken from the overlap of all models on the rising (overfitting) branch, which
   is the only range where all of them can be compared.

2. **Excess over the matched control.** A real canary is ordinary sequence, so part of its score is
   biology the model legitimately learned. The planted-record component is the gap to the matched
   non-member canaries (equally real, equally rare, never trained on):
       excess bits = non-member bits/nt  -  member bits/nt
   On synthetic data the control sits at 2.000 and this reduces to the usual reading; on real data it is
   the statistic that isolates memorisation, and it is what the paper should report.

Writes <name>_matched.md next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<model>dnabert\d|dnabert2bpe|hyena_[a-z0-9-]+?|bpe\d+|char|\d+mer(?:sp)?)"
                 r"(?P<var>_[A-Za-z0-9._-]+?)?_s(?P<seed>\d+)$")
ORDER = {"char": 0, "3mer": 1, "4mer": 2, "5mer": 3, "6mer": 4, "bpe4096": 5,
         "dnabert3": 10, "dnabert4": 11, "dnabert5": 12, "dnabert6": 13, "dnabert2bpe": 14}
LABEL = {"dnabert3": "DNABERT 3-mer", "dnabert4": "DNABERT 4-mer", "dnabert5": "DNABERT 5-mer",
         "dnabert6": "DNABERT 6-mer", "dnabert2bpe": "DNABERT-2 BPE", "char": "char (1 nt)",
         "3mer": "3-mer", "4mer": "4-mer", "5mer": "5-mer", "6mer": "6-mer", "bpe4096": "BPE-4096"}


def epoch_of(f: Path, r: dict) -> int:
    if f.stem.startswith("scores_ep"):
        return int(f.stem.split("ep")[1])
    return int(r.get("epoch") or r.get("train_summary", {}).get("epochs") or 0)


def tier(r, t, host):
    key = next((k for k in (f"causal/{host}", f"ar/{host}", f"span_pll/{host}", f"pll/{host}")
                if any(k in p["ranks"] for p in r["probes"])), None)
    ps = [p for p in r["probes"] if p["repetitions"] == t and key in p["ranks"]]
    if not ps:
        return None
    return (float(np.mean([p["ranks"][key]["probe_bits_per_nt"] for p in ps])),
            float(np.mean([p["extract"][host]["exact"] for p in ps])), len(ps))


def collect(roots, tiers):
    """model -> epoch -> list over seeds of (floor, {tier: (bits, exact, n)}, control_bits)"""
    out = defaultdict(lambda: defaultdict(list))
    for root in roots:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m:
                continue
            files = sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem.split("ep")[1])) + [d / "scores_final.json"]
            for f in files:
                if not f.exists():
                    continue
                r = json.loads(f.read_text(encoding="utf-8"))
                ctrl = tier(r, 0, "fresh")
                vals = {t: tier(r, t, "train") for t in tiers}
                if ctrl is None or all(v is None for v in vals.values()):
                    continue
                out[m["model"]][epoch_of(f, r)].append((r["floors"][0]["bits_per_nt_mean"], vals, ctrl[0]))
    return out


def curve(eps):
    """-> [(floor, {tier: (excess, bits, exact)})] on the rising branch, seed-averaged, sorted by floor."""
    pts = []
    for ep in sorted(eps):
        if ep == 0:
            continue                                  # before fine-tuning there is nothing to match
        runs = eps[ep]
        fl = float(np.mean([x[0] for x in runs]))
        ctrl = float(np.mean([x[2] for x in runs]))
        d = {}
        for t in runs[0][1]:
            v = [x[1][t] for x in runs if x[1][t] is not None]
            if v:
                bits = float(np.mean([y[0] for y in v]))
                d[t] = (ctrl - bits, bits, float(np.mean([y[1] for y in v])))
        pts.append((ep, fl, d))
    if not pts:
        return []
    start = int(np.argmin([p[1] for p in pts]))        # from the least-overfit epoch onward
    rising = sorted(pts[start:], key=lambda p: p[1])
    return [(fl, d) for _, fl, d in rising]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--name", default="matched")
    ap.add_argument("--tiers", default="1,16")
    ap.add_argument("--n_grid", type=int, default=4)
    args = ap.parse_args(argv)
    tiers = [int(t) for t in args.tiers.split(",")]

    data = collect(args.root, tiers)
    curves = {m: curve(eps) for m, eps in data.items()}
    curves = {m: c for m, c in curves.items() if len(c) >= 2}
    if not curves:
        print("nothing to match under", args.root)
        return 1
    lo = max(c[0][0] for c in curves.values())
    hi = min(c[-1][0] for c in curves.values())
    models = sorted(curves, key=lambda m: ORDER.get(m, 99))

    md = [f"# Matched-utility memorisation — {args.name}", "",
          "`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score "
          "that is the planted record rather than biology the model legitimately learned. Higher = more memorised. "
          "Every model is interpolated onto the same held-out-loss values, on the overfitting branch.", ""]
    if hi <= lo:
        md += [f"**No common range.** The models' overfitting branches do not overlap "
               f"(lowest common loss {lo:.3f}, highest {hi:.3f}), so no matched-utility comparison is possible; "
               "report the per-model trajectories instead.", ""]
        for m in models:
            c = curves[m]
            md.append(f"- {LABEL.get(m, m)}: held-out loss {c[0][0]:.3f} to {c[-1][0]:.3f}")
    else:
        grid = np.linspace(lo, hi, args.n_grid)
        md += [f"Common range of held-out loss: {lo:.3f} to {hi:.3f} bits/nt.", ""]
        for t in tiers:
            md += [f"## Canary planted {t}x — excess bits/nt (verbatim extraction in brackets)", "",
                   "| model | " + " | ".join(f"@{g:.3f}" for g in grid) + " |",
                   "|---|" + "---|" * len(grid)]
            for m in models:
                c = [(fl, d[t]) for fl, d in curves[m] if t in d]
                if len(c) < 2:
                    continue
                f = np.array([x[0] for x in c])
                ex = np.array([x[1][0] for x in c])
                xx = np.array([x[1][2] for x in c])
                cells = [f"{np.interp(g, f, ex):.2f} ({np.interp(g, f, xx):.2f})" if f[0] <= g <= f[-1] else "—"
                         for g in grid]
                md.append(f"| {LABEL.get(m, m)} | " + " | ".join(cells) + " |")
            md.append("")

    md += ["## Per-model trajectory (seed means, epoch > 0)", "",
           "| model | epoch | held-out loss | " + " | ".join(f"r={t} excess" for t in tiers) + " | control bits |",
           "|---|---|---|" + "---|" * (len(tiers) + 1)]
    for m in models:
        for ep in sorted(data[m]):
            runs = data[m][ep]
            fl = float(np.mean([x[0] for x in runs]))
            ctrl = float(np.mean([x[2] for x in runs]))
            cells = []
            for t in tiers:
                v = [x[1][t] for x in runs if x[1][t] is not None]
                cells.append(f"{ctrl - float(np.mean([y[0] for y in v])):.2f}" if v else "—")
            md.append(f"| {LABEL.get(m, m)} | {ep} | {fl:.3f} | " + " | ".join(cells) + f" | {ctrl:.2f} |")
    out = Path(args.root[0]) / f"{args.name}_matched.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
