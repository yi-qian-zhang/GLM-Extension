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

A third correction was tried and REJECTED by measurement, and `--baseline` is kept only to reproduce
it. At epoch 0 a pretrained checkpoint reads the member canaries as easier than the non-members
(up to 0.9 bits/nt for the DNABERT family on chromosome 22), which looks like a fixed offset between
the two canary groups that ought to be subtracted. Four independent re-draws of the split
(`pilot2/queue_dseed.sh`) show it is not:
  * after ONE epoch of fine-tuning the offset is gone -- excess at epoch 1 is 0.00 +- 0.05 for every
    model on every split, whatever the epoch-0 reading was;
  * regressing each split's epoch-50 excess on its own epoch-0 offset gives a slope of 0.05 (16x
    tier) to 0.19 (single copy), so subtracting the offset in full over-corrects by 5-20x;
  * and that shows up directly as variance: across the four splits the raw epoch-50 excess has
    sd 0.04-0.11, the baseline-corrected one sd 0.15-0.39.
So the epoch-0 reading is a diagnostic, not a baseline: it says the pretrained model's prior over two
sets of real haplotypes is unstable (HyenaDNA, the only causal-pretrained model in the panel, shows
+-0.09 where the masked-pretrained DNABERTs reach +-0.9), and it does not propagate into the
fine-tuned statistic. The error bar on real-canary numbers is the spread across re-drawn splits.

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
def _base(m):
    return m.split(" [")[0]


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
                # key on model AND objective: a tokenizer trained next-token and the same tokenizer
                # trained masked are different cells, and merging them averages two different curves
                obj = "".join(x for x in (m["var"] or "").split("_")
                              if x and not x.startswith(("ecoli", "yeast", "gue", "human")))
                out[m["model"] + (f" [{obj}]" if obj else "")][epoch_of(f, r)].append(
                    (r["floors"][0]["bits_per_nt_mean"], vals, ctrl[0]))
    return out


def baseline(eps, tiers):
    """excess at epoch 0, per tier: nothing is memorised there, so whatever it reads is the pretrained
    model's own prior over the two canary groups.

    Reported always, subtracted only under --baseline: the module docstring has the four-split
    measurement showing that this offset does not propagate into the fine-tuned statistic, so
    subtracting it over-corrects and inflates the across-split variance."""
    if 0 not in eps:
        return {t: 0.0 for t in tiers}
    runs = eps[0]
    ctrl = float(np.mean([x[2] for x in runs]))
    out = {}
    for t in tiers:
        v = [x[1][t] for x in runs if x[1][t] is not None]
        out[t] = (ctrl - float(np.mean([y[0] for y in v]))) if v else 0.0
    return out


def curve(eps, base=None):
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
                b0 = (base or {}).get(t, 0.0)
                d[t] = (ctrl - bits - b0, bits, float(np.mean([y[1] for y in v])))
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
    ap.add_argument("--baseline", action="store_true",
                    help="subtract each cell's epoch-0 excess (rejected by measurement; see the module docstring)")
    ap.add_argument("--raw", action="store_true", help="kept for older queue scripts: raw is now the default")
    args = ap.parse_args(argv)
    tiers = [int(t) for t in args.tiers.split(",")]

    data = collect(args.root, tiers)
    offsets = {m: baseline(eps, tiers) for m, eps in data.items()}
    bases = offsets if args.baseline else {m: {t: 0.0 for t in tiers} for m in data}
    curves = {m: curve(eps, bases[m]) for m, eps in data.items()}
    curves = {m: c for m, c in curves.items() if len(c) >= 2}
    if not curves:
        print("nothing to match under", args.root)
        return 1
    lo = max(c[0][0] for c in curves.values())
    hi = min(c[-1][0] for c in curves.values())
    models = sorted(curves, key=lambda m: (ORDER.get(_base(m), 99), m))

    md = [f"# Matched-utility memorisation — {args.name}", "",
          "`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score "
          "that is the planted record rather than biology the model legitimately learned. Higher = more memorised. "
          "Every model is interpolated onto the same held-out-loss values, on the overfitting branch."
          + (" Each cell's epoch-0 excess is subtracted (`--baseline`), which the four-split measurement in the "
             "module docstring shows to over-correct; prefer the default." if args.baseline else
             " No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the "
             "module docstring), so it is reported below as a diagnostic only."), ""]
    if hi <= lo:
        md += [f"**No common range.** The models' overfitting branches do not overlap "
               f"(lowest common loss {lo:.3f}, highest {hi:.3f}), so no matched-utility comparison is possible; "
               "report the per-model trajectories instead.", ""]
        for m in models:
            c = curves[m]
            md.append(f"- {LABEL.get(_base(m), _base(m))}{m[len(_base(m)):]}: held-out loss {c[0][0]:.3f} to {c[-1][0]:.3f}")
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
                md.append(f"| {LABEL.get(_base(m), _base(m))}{m[len(_base(m)):]} | " + " | ".join(cells) + " |")
            md.append("")

    md += [f"## Epoch-0 excess — the pretrained model's prior over the two canary groups "
           f"({'subtracted above' if args.baseline else 'diagnostic only, not subtracted'})", "",
           "| model | " + " | ".join(f"r={t}" for t in tiers) + " |", "|---|" + "---|" * len(tiers)]
    for m in models:
        md.append(f"| {LABEL.get(_base(m), _base(m))}{m[len(_base(m)):]} | " + " | ".join(f"{offsets[m].get(t, 0.0):+.2f}" for t in tiers) + " |")
    md += ["", "## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)", "",
           "| model | epoch | held-out loss | " + " | ".join(f"r={t} excess" for t in tiers) + " | control bits |",
           "|---|---|---|" + "---|" * (len(tiers) + 1)]
    for m in models:
        for ep in sorted(data[m]):
            runs = data[m][ep]
            fl = float(np.mean([x[0] for x in runs]))
            ctrl = float(np.mean([x[2] for x in runs]))
            cells = []
            for t in tiers:
                # per-run excess (each run against its own control), so the spread is over runs --
                # model seeds, and data seeds when several roots are given -- not over canaries
                ex = [x[2] - x[1][t][0] - bases[m].get(t, 0.0) for x in runs if x[1][t] is not None]
                if not ex:
                    cells.append("—")
                    continue
                cells.append(f"{np.mean(ex):.2f}" + (f" ±{np.std(ex):.2f}" if len(ex) > 1 else ""))
            md.append(f"| {LABEL.get(_base(m), _base(m))}{m[len(_base(m)):]} | {ep} | {fl:.3f} | " + " | ".join(cells) + f" | {ctrl:.2f} |")
    out = Path(args.root[0]) / f"{args.name}_matched.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
