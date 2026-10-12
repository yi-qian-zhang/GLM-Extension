"""Why a masked model can recognise a record perfectly and still reconstruct none of it.

The 150-round masked cells read 0.12 bits/nt on a planted canary and rank it first out of a hundred
candidates with probability 1.00, including a canary inserted once, while greedy reconstruction of
its second half gets 0 of 50 probes exactly right. That looks like a contradiction, and a reviewer
will read it as a broken extractor unless we say which conditional each ruler uses.

  pll/*     every token scored with ALL other tokens of the record visible
  prefix/*  every token scored left to right, nothing after it visible
  extraction  reveal the first 48 nt, generate the next 48 with the suffix masked

Recognition and surprise are measured in the first idiom, extraction demands the third. This script
prints both scorers side by side for every masked cell, so the arithmetic is on the page: if the
prefix-conditioned surprise stays near the model's own held-out floor while the PLL surprise
collapses, then tens of bits of prefix-conditional uncertainty remain over the 48 target
nucleotides, no decoder recovers that, and the 0 % is a property of the model rather than of our
decoding.

Reports excess (non-member minus member) as well as raw bits, because on chromosome 22 the canaries
are real haplotype segments: 2.000 bits/nt is an upper reference there, not the chance level, so raw
bits credit biology the model legitimately learned, and they are not comparable between models with
different held-out floors.

    python -m pilot2.prefix_vs_pll --root outputs/human_mlm_long outputs/nt
"""
import argparse
import glob
import json
import os
import re
import statistics as st


def cells(roots):
    for root in roots:
        for f in sorted(glob.glob(os.path.join(root, "**", "scores_*.json"), recursive=True)):
            try:
                r = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            if not r.get("probes"):
                continue
            scorers = set()
            for p in r["probes"]:
                scorers |= {k.split("/")[0] for k in p.get("ranks", {})}
            if "pll" not in scorers:
                continue           # causal cells have no bidirectional conditional to compare
            yield f, r


def mean(xs):
    xs = [x for x in xs if x is not None]
    return st.mean(xs) if xs else float("nan")


def tier_stats(probes, scorer, host):
    key = f"{scorer}/{host}"
    ps = [p for p in probes if key in p.get("ranks", {})]
    if not ps:
        return None
    return dict(
        n=len(ps),
        bits=mean(p["ranks"][key]["probe_bits_per_nt"] for p in ps),
        rank1=mean(float(p["ranks"][key]["rank"] == 1) for p in ps),
        ham=mean((p.get("extract", {}).get(host) or {}).get("hamming_nt") for p in ps),
        exact=mean(float((p.get("extract", {}).get(host) or {}).get("exact", 0)) for p in ps),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--tiers", default="16,4,1")
    args = ap.parse_args()
    tiers = [int(t) for t in args.tiers.split(",")]

    hdr = ("cell", "ep", "r", "n", "floor_pll", "floor_pre", "pll", "PREFIX", "ex_pll", "ex_PRE",
           "rank1", "ham", "exact")
    print("%-46s %4s %3s %4s %9s %9s %6s %6s %6s %6s %5s %5s %5s" % hdr)
    print("-" * 134)
    for f, r in cells(args.root):
        fl = {x["scorer"]: x["bits_per_nt_mean"] for x in r.get("floors", [])}
        ep = r.get("epoch")
        if ep is None:
            m = re.search(r"scores_ep(\d+)", f)
            ep = m.group(1) if m else "fin"
        # the matched non-member control: same decode, same scorers, untrained windows
        non = {sc: tier_stats(r["probes"], sc, "fresh") for sc in ("pll", "prefix")}
        name = os.path.basename(os.path.dirname(f))
        for t in tiers:
            ps = [p for p in r["probes"] if p.get("repetitions") == t]
            if not ps:
                continue
            a = tier_stats(ps, "pll", "train")
            b = tier_stats(ps, "prefix", "train")
            if a is None:
                continue
            ex_pll = (non["pll"]["bits"] - a["bits"]) if non["pll"] else float("nan")
            ex_pre = (non["prefix"]["bits"] - b["bits"]) if (b and non["prefix"]) else float("nan")
            print("%-46s %4s %3d %4d %9.3f %9.3f %6.3f %6.3f %6.2f %6.2f %5.2f %5.1f %5.2f" % (
                name[:46], ep, t, a["n"],
                fl.get("pll", float("nan")), fl.get("prefix", float("nan")),
                a["bits"], b["bits"] if b else float("nan"),
                ex_pll, ex_pre, a["rank1"], a["ham"], a["exact"]))
    print()
    print("ex_* = non-member minus member bits/nt under the same scorer (higher = more memorised).")
    print("A large ex_pll beside a small ex_PRE is the dissociation: the record is held in the")
    print("bidirectional conditional and not in the left-to-right one that extraction must use.")


if __name__ == "__main__":
    main()
