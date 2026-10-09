"""Rare-allele recovery: when a model continues a real human haplotype, does it return the
individual's rare allele or the reference base?

    python -m pilot2.analyze_human --root outputs/human_real --canary_npz data/human/canaries_chr22.npz

For every canary the extraction step reveals the first 48 nt and decodes the rest greedily, and the
decoded bases are stored (`pred_nt`). A canary from `pilot2.human_canary` carries the positions of
its rare variants, so each variant that falls in the decoded region gives one trial with three
outcomes: the individual's ALT allele, the reference base (what a model that only learned the
reference genome would say), or something else. The reference base is the natural null, which makes
this a direct read of genotype leakage rather than a string-matching score.

Members (inserted r times, scored in their training host) are compared with non-members (r = 0,
equally real and equally rare, never inserted, scored in a fresh host). The gap is the leakage.

Writes human_report.md next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<model>dnabert\d|dnabert2bpe|hyena_[a-z0-9-]+?|bpe\d+|char|\d+mer)(?P<var>_[A-Za-z0-9._-]+?)?_s(?P<seed>\d+)$")


def variant_index(npz):
    from .human_canary import load_canaries
    _, meta = load_canaries(npz)
    return {c["seq"]: c for c in meta["canaries"]}, meta


def allele_trials(probe_meta, extract, vmap):
    """-> list of ('alt'|'ref'|'other') for the variants inside the decoded region."""
    c = vmap.get(probe_meta["seq"])
    if not c or "pred_nt" not in extract:
        return []
    k_rev, pred = extract["k_revealed_nt"], extract["pred_nt"]
    out = []
    for v in c["variants"]:
        i = v["index"] - k_rev
        if i < 0 or i >= len(pred):
            continue
        b = pred[i]
        out.append("alt" if b == v["alt"] else "ref" if b == v["ref"] else "other")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--canary_npz", default="data/human/canaries_chr22.npz")
    ap.add_argument("--name", default="human")
    args = ap.parse_args(argv)
    vmap, meta = variant_index(args.canary_npz)

    rows = []
    for root in args.root:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m:
                continue
            dm = d / "data_meta.json"
            if not dm.exists():
                continue
            pmeta = {p["probe_id"]: p for p in json.loads(dm.read_text(encoding="utf-8"))["probes"]}
            for f in sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem.split("ep")[1])) + [d / "scores_final.json"]:
                if not f.exists():
                    continue
                r = json.loads(f.read_text(encoding="utf-8"))
                sc = next((k.split("/")[0] for p in r["probes"] for k in p["ranks"]), "ar")
                by = defaultdict(lambda: {"alt": 0, "ref": 0, "other": 0, "exact": [], "bits": []})
                for p in r["probes"]:
                    tier = p["repetitions"]
                    host = "train" if tier > 0 and "train" in p["extract"] else "fresh"
                    e = p["extract"].get(host)
                    if not e:
                        continue
                    pm = pmeta.get(p["probe_id"])
                    if pm is None:
                        continue
                    for o in allele_trials(pm, e, vmap):
                        by[tier][o] += 1
                    by[tier]["exact"].append(e["exact"])
                    key = f"{sc}/{host}"
                    if key in p["ranks"]:
                        by[tier]["bits"].append(p["ranks"][key]["probe_bits_per_nt"])
                for tier, v in by.items():
                    n = v["alt"] + v["ref"] + v["other"]
                    rows.append({"model": m["model"] + (m["var"] or ""), "seed": int(m["seed"]), "epoch": int(r["epoch"]),
                                 "floor": r["floors"][0]["bits_per_nt_mean"], "tier": tier, "n_trials": n,
                                 "alt": v["alt"] / n if n else None, "ref": v["ref"] / n if n else None,
                                 "other": v["other"] / n if n else None,
                                 "exact": float(np.mean(v["exact"])) if v["exact"] else None,
                                 "bits": float(np.mean(v["bits"])) if v["bits"] else None})
    if not rows:
        print("no runs with human canaries under", args.root); return 1

    md = [f"# Rare-allele recovery on real human canaries — {args.name}", "",
          f"Canaries: {meta['n_canaries']} haplotype segments of {meta['probe_len']} nt from "
          f"{meta['source']['cohort']}, {meta['source']['chrom']} ({meta['source']['assembly']}), "
          f"variants with AF <= {meta['max_af']} and <= {meta['max_carriers']} carriers.", "",
          "`alt` = the individual's rare allele was produced, `ref` = the reference base was produced "
          "(the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a "
          "fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.", "",
          "| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |",
          "|---|---|---|---|---|---|---|---|---|"]
    agg = defaultdict(list)
    for w in rows:
        agg[(w["model"], w["epoch"], w["tier"])].append(w)
    f3 = lambda v: f"{v:.3f}" if v is not None else "—"
    for (mod, ep, tier), ws in sorted(agg.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        mean = lambda k: (lambda v: float(np.mean(v)) if v else None)([w[k] for w in ws if w[k] is not None])
        md.append(f"| {mod} | {ep} | r={tier} | {sum(w['n_trials'] for w in ws)} | {f3(mean('alt'))} | "
                  f"{f3(mean('ref'))} | {f3(mean('other'))} | {f3(mean('bits'))} | {f3(mean('exact'))} |")
    md += ["", "## Leakage: member minus non-member rare-allele recovery", "",
           "| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |", "|---|---|---|---|---|---|"]
    for (mod, ep) in sorted({(w["model"], w["epoch"]) for w in rows}):
        get = lambda t: (lambda v: float(np.mean(v)) if v else None)(
            [w["alt"] for w in rows if w["model"] == mod and w["epoch"] == ep and w["tier"] == t and w["alt"] is not None])
        a16, a1, a0 = get(16), get(1), get(0)
        gap = f"{a16 - a0:+.3f}" if (a16 is not None and a0 is not None) else "—"
        md.append(f"| {mod} | {ep} | {f3(a16)} | {f3(a1)} | {f3(a0)} | {gap} |")
    out = Path(args.root[0]) / "human_report.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    (Path(args.root[0]) / "human_rows.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    print("\n".join(md)); print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
