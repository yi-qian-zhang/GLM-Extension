"""The objective x tokenizer grid for one dataset, at the end of a fixed schedule.

    python -m pilot2.analyze_objaxis --root outputs/human_toy outputs/human_mlm --data human --epoch 30

One row per (tokenizer, objective) cell: the held-out loss, the control-corrected excess and the
verbatim extraction rate at --epoch, averaged over model seeds, with the across-seed spread and the
seed count. The epoch-1 excess is printed as well: for a from-scratch backbone it must be ~0, because
an untrained model has no preference between the member and non-member canary groups, and a non-zero
value there is the group offset that analyze_matched has to subtract for pretrained models.

Comparing cells at the same epoch is only sound when they share a schedule AND their epoch-1 offsets
agree; the held-out-loss column is printed next to every cell so a reader can see what each one paid.

Writes <name>_objaxis.md next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?|bpe\d+)(?P<rest>_[A-Za-z0-9._@-]+?)?_s(?P<seed>\d+)$")
DATASETS = ("ecoli", "yeast", "gue", "human")
ORDER = {"char": 0, "3mer": 1, "4mer": 2, "5mer": 3, "6mer": 4, "bpe4096": 5}
OBJ_ORDER = {"ar": 0}
LABEL = {"char": "char (1 nt)", "3mer": "3-mer", "4mer": "4-mer", "5mer": "5-mer", "6mer": "6-mer",
         "bpe4096": "BPE-4096"}
OBJ_LABEL = {"ar": "next-token"}


def objective_of(rest: str | None) -> str:
    """'_mlm0.15_human' -> 'mlm@0.15'; '_human' or None -> 'ar' (the default of every arm)."""
    parts = [p for p in (rest or "").split("_") if p and p not in DATASETS]
    if not parts:
        return "ar"
    o = parts[0]
    return o.replace("mlm", "mlm@") if o.startswith("mlm") and "@" not in o else o


def cell(r: dict, tier: int):
    """(floor, excess, exact) at one snapshot, or None. excess = non-member - member bits/nt."""
    key = next((k.split("/")[0] for p in r["probes"] for k in p["ranks"]), None)
    if key is None:
        return None
    mem = [p for p in r["probes"] if p["repetitions"] == tier and f"{key}/train" in p["ranks"]]
    ctl = [p for p in r["probes"] if p["repetitions"] == 0 and f"{key}/fresh" in p["ranks"]]
    if not mem or not ctl:
        return None
    bits = float(np.mean([p["ranks"][f"{key}/train"]["probe_bits_per_nt"] for p in mem]))
    ctrl = float(np.mean([p["ranks"][f"{key}/fresh"]["probe_bits_per_nt"] for p in ctl]))
    return (float(r["floors"][0]["bits_per_nt_mean"]), ctrl - bits,
            float(np.mean([p["extract"]["train"]["exact"] for p in mem])))


def collect(roots, data, tier):
    """(tokenizer, objective) -> epoch -> list over seeds of (floor, excess, exact)"""
    out = defaultdict(lambda: defaultdict(list))
    for root in roots:
        p = Path(root)
        if not p.is_dir():
            continue
        for d in sorted(p.iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m or not (d / "args.json").exists():
                continue
            a = json.loads((d / "args.json").read_text(encoding="utf-8"))
            if data and (a.get("data") or "synthetic") != data:   # the dataset the run used, not the directory it sits in
                continue
            for f in sorted(d.glob("scores_ep*.json"), key=lambda q: int(q.stem.split("ep")[1])):
                v = cell(json.loads(f.read_text(encoding="utf-8")), tier)
                if v:
                    out[(m["tok"], objective_of(m["rest"]))][int(f.stem.split("ep")[1])].append(v)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--data", default="human")
    ap.add_argument("--epoch", type=int, default=30, help="the end of the shared schedule")
    ap.add_argument("--tier", type=int, default=16)
    ap.add_argument("--name", default=None)
    args = ap.parse_args(argv)

    g = collect(args.root, args.data, args.tier)
    if not g:
        print("no runs under", args.root, "for data", args.data)
        return 1
    name = args.name or f"{args.data}_r{args.tier}"
    md = [f"# Objective x tokenizer — {args.data}, canary planted {args.tier}x, round {args.epoch}", "",
          "`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the "
          "same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and "
          "whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, "
          "with the across-seed range where there is more than one seed.", "",
          "| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |",
          "|---|---|---|---|---|---|---|"]

    def fmt(vals, prec=2):
        if len(vals) < 2:
            return f"{vals[0]:.{prec}f}"
        return f"{np.mean(vals):.{prec}f} ({min(vals):.{prec}f}-{max(vals):.{prec}f})"

    for k in sorted(g, key=lambda x: (ORDER.get(x[0], 9), OBJ_ORDER.get(x[1], 9), x[1])):
        eps = g[k]
        e1 = f"{np.mean([v[1] for v in eps[1]]):+.2f}" if 1 in eps else "—"
        if args.epoch not in eps:
            md.append(f"| {LABEL.get(k[0], k[0])} | {OBJ_LABEL.get(k[1], k[1])} | {e1} | "
                      f"— | — | — | 0 (last ep {max(eps)}) |")
            continue
        v = eps[args.epoch]
        md.append(f"| {LABEL.get(k[0], k[0])} | {OBJ_LABEL.get(k[1], k[1])} | {e1} | "
                  f"{fmt([x[0] for x in v], 3)} | {fmt([x[1] for x in v])} | "
                  f"{fmt([100 * x[2] for x in v], 0)}% | {len(v)} |")
    out = Path(args.root[0]) / f"{name}_objaxis.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
