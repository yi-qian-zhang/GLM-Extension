"""Flatten every scored snapshot into one tidy table, so the figures can be redrawn
without the 750 MB of raw score files behind them.

    python -m pilot2.export_figure_data --root outputs --out results/figure_data.csv

WHY. Each `scores_ep*.json` is a few hundred kilobytes of per-probe detail, and there are
three thousand of them. Every figure in the paper reads the same handful of fields out of
them: where the run sat in held-out loss at that snapshot, and what fraction of the planted
records came back at each repetition tier. Publishing the raw files would add three quarters
of a gigabyte to the repository for a reader who wants a curve; publishing this table lets
them redraw every curve, and the raw files remain on request.

One row per (run, snapshot, tier, host). `host=train` is the window the record was planted
in; `host=fresh` is a window the model never saw, which is the control, and its rate should
be zero everywhere.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

# `group` is the sweep directory the run sits in. Without it the table is ambiguous: the
# same run name (3mer_ar_s0) exists under both kcurve and kcurve300, and several released
# cells repeat across nt/, nt_ckpt/ and nt_opt/.
FIELDS = [
    "group", "run", "tokenizer", "objective", "seed", "data", "window", "n_train",
    "epoch", "heldout_bits_per_nt", "tier", "host", "n_probes",
    "exact_rate", "mean_hamming_nt", "rank1_rate",
]


def _runs(root: Path):
    """Every directory holding at least one scored snapshot."""
    seen = set()
    for f in root.rglob("scores_*.json"):
        if f.parent not in seen:
            seen.add(f.parent)
            yield f.parent


def _meta(d: Path) -> dict:
    out = {}
    for name, keys in (("args.json", ("tokenizer", "objective", "seed", "data", "size", "k", "n_train")),
                       ("data_meta.json", ("window", "n_train"))):
        f = d / name
        if not f.exists():
            continue
        try:
            a = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        for k in keys:
            if a.get(k) is not None and out.get(k) is None:
                out[k] = a[k]
    # released checkpoints record their family under a different key than our own runs
    if out.get("tokenizer") is None:
        out["tokenizer"] = out.pop("size", None) or (f"{out['k']}mer" if out.get("k") else None)
    out.pop("size", None)
    out.pop("k", None)
    return out


def _rows(d: Path, meta: dict, group: str):
    for f in sorted(d.glob("scores_*.json")):
        m = re.search(r"scores_(ep\d+|final)\.json$", f.name)
        if not m:
            continue
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        floor = (s.get("floors") or [{}])[0].get("bits_per_nt_mean")
        probes = s.get("probes") or []
        # (tier, host) -> [exact, hamming, rank1]
        acc: dict[tuple, list[list]] = {}
        for p in probes:
            tier = p.get("repetitions")
            for host, ex in (p.get("extract") or {}).items():
                if not isinstance(ex, dict):
                    continue
                ranks = p.get("ranks") or {}
                r1 = next((1.0 if v.get("rank") == 1 else 0.0)
                          for k, v in ranks.items() if k.endswith("/" + host)) \
                    if any(k.endswith("/" + host) for k in ranks) else None
                acc.setdefault((tier, host), []).append(
                    [1.0 if ex.get("exact") else 0.0, ex.get("hamming_nt"), r1])
        for (tier, host), vals in sorted(acc.items(), key=lambda kv: (str(kv[0][0]), kv[0][1])):
            ex = [v[0] for v in vals]
            ham = [v[1] for v in vals if v[1] is not None]
            r1 = [v[2] for v in vals if v[2] is not None]
            yield {
                "group": group, "run": d.name, "tokenizer": meta.get("tokenizer"),
                "objective": meta.get("objective"), "seed": meta.get("seed"),
                "data": meta.get("data"), "window": meta.get("window"),
                "n_train": meta.get("n_train"),
                "epoch": m.group(1).replace("ep", ""),
                "heldout_bits_per_nt": None if floor is None else round(floor, 6),
                "tier": tier, "host": host, "n_probes": len(vals),
                "exact_rate": round(sum(ex) / len(ex), 6) if ex else None,
                "mean_hamming_nt": round(sum(ham) / len(ham), 3) if ham else None,
                "rank1_rate": round(sum(r1) / len(r1), 6) if r1 else None,
            }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs")
    ap.add_argument("--out", default="results/figure_data.csv")
    args = ap.parse_args(argv)
    root = Path(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    n_runs = n_rows = 0
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        for d in sorted(_runs(root)):
            meta = _meta(d)
            got = 0
            group = d.parent.relative_to(root).as_posix() if d.parent != root else "."
            for row in _rows(d, meta, group):
                w.writerow(row)
                got += 1
            if got:
                n_runs += 1
                n_rows += got
    print(f"{n_rows} rows from {n_runs} runs -> {out} ({out.stat().st_size/1048576:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
