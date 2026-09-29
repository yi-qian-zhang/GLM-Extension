"""Random-offset control: does k-mer memorization survive when probe copies sit at random offsets?

    python -m pilot2.analyze_offset --random outputs/off1 --fixed outputs/traj1

For every (tokenizer, tier) reports, from scores_final.json (mean over seeds):
  fixed/train   probe at nt 96 in its training host (all copies share one k-mer phase)
  random/train  probe at its first copy's own offset in that copy's host
  random/fresh  probe in a new host at a new random offset, split by whether that offset's
                k-mer phase matches at least one training copy (`phase_match` > 0) or none.
The phase split asks whether a k-mer model's memory of a sequence transfers across
tokenizations of the same nucleotides. For char every offset is in phase.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?)_(?P<obj>ar|mlm[0-9.]+)_s(?P<seed>\d+)")


def cells(root: Path):
    for d in sorted(root.iterdir()):
        m = RUN.fullmatch(d.name) if d.is_dir() else None
        f = d / "scores_final.json"
        if m and f.exists():
            yield m["tok"], m["obj"], json.loads(f.read_text(encoding="utf-8"))


def stats(entries, key, host):
    if not entries:
        return None
    b = np.mean([e["ranks"][key]["probe_bits_per_nt"] for e in entries])
    r1 = np.mean([e["ranks"][key]["rank"] == 1 for e in entries])
    ex = np.mean([e["extract"][host]["exact"] for e in entries])
    return b, r1, ex, len(entries)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--random", default="outputs/off1")
    ap.add_argument("--fixed", default="outputs/traj1")
    args = ap.parse_args(argv)
    acc = defaultdict(list)  # (tok, obj, tier, condition) -> list of (bits, r1, exact, n)
    for label, root in (("fixed", Path(args.fixed)), ("random", Path(args.random))):
        for tok, obj, r in cells(root):
            sc = "ar" if r["kind"] == "ar" else "pll"
            for tier in sorted({p["repetitions"] for p in r["probes"]}):
                ps = [p for p in r["probes"] if p["repetitions"] == tier]
                if tier > 0:
                    acc[(tok, obj, tier, f"{label}/train")].append(stats(ps, f"{sc}/train", "train"))
                if label == "random":
                    if tier > 0:
                        inph = [p for p in ps if p.get("phase_match")]
                        outph = [p for p in ps if p.get("phase_match") == 0]
                        acc[(tok, obj, tier, "random/fresh in-phase")].append(stats(inph, f"{sc}/fresh", "fresh"))
                        acc[(tok, obj, tier, "random/fresh out-of-phase")].append(stats(outph, f"{sc}/fresh", "fresh"))
                    else:
                        acc[(tok, obj, tier, "random/fresh non-member")].append(stats(ps, f"{sc}/fresh", "fresh"))
    md = [f"# Random-offset control — {args.random} vs {args.fixed}", "",
          "bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). "
          "2.000 bits = nothing memorized; rank-1 chance 0.002.", "",
          "| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |", "|---|---|---|---|---|---|---|---|"]
    order = ["fixed/train", "random/train", "random/fresh in-phase", "random/fresh out-of-phase", "random/fresh non-member"]
    for (tok, obj, tier, cond) in sorted(acc, key=lambda k: (k[1], k[0], k[2], order.index(k[3]))):
        v = [x for x in acc[(tok, obj, tier, cond)] if x]
        if not v:
            continue
        b, r1, ex = (np.average([x[i] for x in v], weights=[x[3] for x in v]) for i in range(3))
        md.append(f"| {tok} | {obj} | r={tier} | {cond} | {b:.3f} | {r1:.2f} | {ex:.2f} | {sum(x[3] for x in v)} |")
    out = Path(args.random) / "offset_report.md"
    out.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
