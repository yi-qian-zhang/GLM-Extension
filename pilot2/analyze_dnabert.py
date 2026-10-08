"""Summarise the DNABERT k-mer family runs (pilot2.dnabert outputs).

    python -m pilot2.analyze_dnabert --root outputs/dnabert

Per k and epoch (mean over seeds): held-out floor, and per tier the probe bits/nt,
rank-1 rate and exact-extraction rate on the training host and on a fresh host.
Also a memorisation-at-matched-floor table across k, as for the from-scratch grid.
The pre-registered prediction is 3 < 4 < 5 < 6 in memorisation at matched floor.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"dnabert(?P<k>\d|2bpe)(?P<var>_[A-Za-z0-9._-]+?)?_s(?P<seed>\d+)")
KLABEL = lambda k: "BPE" if k == 7 else str(k)   # DNABERT-2 (BPE) sorts after the 6-mer
GRID = (2.03, 2.05, 2.10, 2.20, 2.40)


def tier_stats(r, tier, host):
    key = f"{'causal' if r.get('objective') == 'causal' else 'span_pll'}/{host}"
    ps = [p for p in r["probes"] if p["repetitions"] == tier and key in p["ranks"]]
    if not ps:
        return None
    return (np.mean([p["ranks"][key]["probe_bits_per_nt"] for p in ps]),
            np.mean([p["ranks"][key]["rank"] == 1 for p in ps]),
            np.mean([p["extract"][host]["exact"] for p in ps]), len(ps))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/dnabert")
    args = ap.parse_args(argv)
    root = Path(args.root)
    rows = []
    for d in sorted(root.iterdir()):
        m = RUN.fullmatch(d.name) if d.is_dir() else None
        if not m:
            continue
        files = sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem[9:])) + [d / "scores_final.json"]
        for f in files:
            if not f.exists():
                continue
            r = json.loads(f.read_text(encoding="utf-8"))
            row = {"k": 7 if m["k"] == "2bpe" else int(m["k"]), "var": (m["var"] or "_mlm").lstrip("_"), "seed": int(m["seed"]), "epoch": int(r["epoch"]),
                   "floor": r["floors"][0]["bits_per_nt_mean"]}
            for t in (0, 1, 4, 16):
                for host in ("train", "fresh"):
                    s = tier_stats(r, t, host)
                    if s:
                        row[(t, host)] = s
            rows.append(row)
    if not rows:
        print("no runs under", root); return 1
    rows.sort(key=lambda w: (w["var"], w["k"], w["epoch"], w["seed"]))
    md = [f"# DNABERT k-mer family — {root}", "",
          "Fine-tuned with planted canaries at random offsets; native MLM head; span-masked per-nt scoring. "
          "Cells: probe bits/nt / rank-1 / exact extraction (mean over seeds; n per seed in the header). "
          "fp = non-member rank-1 on a fresh host.", "",
          "| variant | k | epoch | floor | r=1 train | r=4 train | r=16 train | r=16 fresh | fp |", "|---|---|---|---|---|---|---|---|---|"]
    by = defaultdict(list)
    for w in rows:
        by[(w["var"], w["k"], w["epoch"])].append(w)
    fmt = lambda s: f"{s[0]:.2f} / {s[1]:.2f} / {s[2]:.2f}" if s else "—"
    agg = {}
    for (var, k, e), ws in sorted(by.items()):
        def mean_stat(key):
            v = [w[key] for w in ws if key in w]
            return (np.mean([x[0] for x in v]), np.mean([x[1] for x in v]), np.mean([x[2] for x in v])) if v else None
        fl = np.mean([w["floor"] for w in ws])
        cells = [mean_stat((1, "train")), mean_stat((4, "train")), mean_stat((16, "train")), mean_stat((16, "fresh"))]
        fp = mean_stat((0, "fresh"))
        agg[(var, k, e)] = (fl, cells)
        md.append(f"| {var} | {KLABEL(k)} | {e} | {fl:.3f} | " + " | ".join(fmt(c) for c in cells) + (f" | {fp[1]:.2f} |" if fp else " | — |"))
    # matched-floor interpolation per k (seed-mean curves, from the least-overfit epoch onward)
    md += ["", "## Memorisation at matched held-out floor (r=1 and r=16, training host; lower = more memorised)", "",
           "| variant | k | tier | " + " | ".join(f"@{x:.2f}" for x in GRID) + " |", "|---|---|---|" + "---|" * len(GRID)]
    for var, k in sorted({(w["var"], w["k"]) for w in rows}):
        pts = sorted((e, agg[(vv, kk, e)]) for (vv, kk, e) in agg if vv == var and kk == k)
        fl = np.array([v[0] for _, v in pts])
        start = int(np.argmin(fl))
        for t, idx in ((1, 0), (16, 2)):
            b = np.array([v[1][idx][0] if v[1][idx] else np.nan for _, v in pts])
            f2, b2 = fl[start:], b[start:]
            order = np.argsort(f2); f2, b2 = f2[order], b2[order]
            cells = [f"{np.interp(x, f2, b2):.3f}" if f2[0] <= x <= f2[-1] else "—" for x in GRID]
            md.append(f"| {var} | {KLABEL(k)} | r={t} | " + " | ".join(cells) + " |")
    out = root / "dnabert_report.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md)); print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
