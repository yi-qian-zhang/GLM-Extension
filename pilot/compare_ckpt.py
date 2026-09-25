"""Compare best.pt vs final.pt scoring for runs that have both scores files.

    python -m pilot.compare_ckpt --root outputs/pilot
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np


def summarize(d, tier):
    ps = [p for p in d["probes"] if p["repetitions"] == tier]
    host = "train" if tier > 0 else "fresh"
    scorer = "ar" if d["kind"] == "ar" else "prefix"
    key = f"{scorer}/{host}"
    r = np.array([p["ranks"][key]["rank"] for p in ps])
    bits = np.array([p["ranks"][key]["probe_bits_per_nt"] for p in ps])
    ex = np.array([p["extract"][host]["exact"] for p in ps])
    ham = np.array([p["extract"][host]["hamming"] for p in ps])
    return (f"median rank {np.median(r):5.0f}/{d['pool_size']+1}  rank-1 {np.mean(r == 1):.2f}  "
            f"bits/nt {bits.mean():.4f}  exact-extract {ex.mean():.2f}  hamming {ham.mean():.1f}/48")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/pilot")
    args = ap.parse_args(argv)
    for run in sorted(Path(args.root).glob("*/")):
        b, f = run / "scores.json", run / "scores_final.json"
        if not (b.exists() and f.exists()):
            continue
        B, F = json.loads(b.read_text()), json.loads(f.read_text())
        ep = B["train_summary"]["best_epoch"]
        last = B["train_summary"]["epochs"] - 1
        print(f"=== {run.name}: best.pt (epoch {ep}) vs final.pt (epoch {last}) ===")
        for fl_b, fl_f in zip(B["floors"], F["floors"]):
            print(f"  floor {fl_b['scorer']:6s}: best {fl_b['bits_per_nt_mean']:.4f}   final {fl_f['bits_per_nt_mean']:.4f}  bits/nt")
        tiers = sorted({p["repetitions"] for p in B["probes"]}, reverse=True)
        for t in tiers:
            print(f"  r={t:2d} best : {summarize(B, t)}")
            print(f"  r={t:2d} final: {summarize(F, t)}")


if __name__ == "__main__":
    main()
