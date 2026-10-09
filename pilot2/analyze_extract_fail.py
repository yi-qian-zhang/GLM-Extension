"""Where does greedy extraction fail, and why is the rate not monotone in k on chromosome 22?

    python -m pilot2.analyze_extract_fail --root outputs/human_real3 --canary_npz $GLMEXT_DATA/human/canaries_chr22.npz

The extraction metric is all-or-nothing over 48 nucleotides, so a model can hold a record almost
perfectly and still score zero. On human chromosome 22 the rate reads 97 / 86 / 67 / 85 per cent for
the released 3- to 6-mer checkpoints, which is not monotone by more than its standard error, while
the control-corrected surprise on the same runs is flat for k = 3,4,5 with the 6-mer highest. This
script asks what the failures actually are, using the decoded bases that every run records:

  * how many nucleotides are wrong when extraction fails (1 wrong letter and 20 wrong letters are
    the same zero in the headline metric);
  * whether the wrong letters sit at the carrier's rare-variant positions or elsewhere;
  * whether a wrong letter at a variant position is the REFERENCE base, which would mean the model
    is being pulled toward the reference genome it was pretrained on rather than failing at random;
  * whether failures cluster at the k-mer grid phase of the revealed prefix.

Writes extract_fail.md next to the root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<model>dnabert\d|dnabert2bpe|hyena_[a-z0-9-]+?|bpe\d+|char|\d+mer)"
                 r"(?P<var>_[A-Za-z0-9._-]+?)?_s(?P<seed>\d+)$")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--canary_npz", default=None)
    ap.add_argument("--tier", type=int, default=16)
    ap.add_argument("--epoch", type=int, default=50)
    args = ap.parse_args(argv)

    vmap = {}
    if args.canary_npz:
        from .human_canary import load_canaries
        _, meta = load_canaries(args.canary_npz)
        vmap = {c["seq"]: c for c in meta["canaries"]}

    rows = defaultdict(list)
    for root in args.root:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m:
                continue
            f = d / (f"scores_ep{args.epoch}.json" if (d / f"scores_ep{args.epoch}.json").exists()
                     else "scores_final.json")
            if not f.exists():
                continue
            r = json.loads(f.read_text(encoding="utf-8"))
            dm = d / "data_meta.json"
            pmeta = {p["probe_id"]: p for p in json.loads(dm.read_text(encoding="utf-8"))["probes"]} if dm.exists() else {}
            for p in r["probes"]:
                if p["repetitions"] != args.tier:
                    continue
                e = p["extract"].get("train")
                if not e or "pred_nt" not in e or "truth_nt" not in e:
                    continue
                pred, truth = e["pred_nt"], e["truth_nt"]
                n = min(len(pred), len(truth))
                wrong = [i for i in range(n) if pred[i] != truth[i]]
                rec = {"exact": bool(e["exact"]), "n": n, "n_wrong": len(wrong), "first_wrong": wrong[0] if wrong else None}
                c = vmap.get((pmeta.get(p["probe_id"]) or {}).get("seq"))
                if c:
                    k_rev = e["k_revealed_nt"]
                    vpos = {v["index"] - k_rev: v for v in c["variants"] if 0 <= v["index"] - k_rev < n}
                    at_var = [i for i in wrong if i in vpos]
                    rec["n_variants_in_region"] = len(vpos)
                    rec["n_wrong_at_variant"] = len(at_var)
                    rec["n_wrong_to_reference"] = sum(1 for i in at_var if pred[i] == vpos[i]["ref"])
                rows[m["model"] + (m["var"] or "")].append(rec)

    if not rows:
        print("no runs with recorded extraction under", args.root)
        return 1

    md = [f"# Where greedy extraction fails — tier r={args.tier}, round {args.epoch}", "",
          "`exact` is the headline all-or-nothing rate. `wrong nt` counts only the failures, so it says "
          "how close a failure was. `at variant` is how many of those wrong letters sit on a rare-variant "
          "position, and `-> reference` how many of those produced the reference base instead of the "
          "carrier's allele.", "",
          "| model | n | exact | mean wrong nt (failures) | median wrong nt | first wrong position | wrong at variant | of which -> reference |",
          "|---|---|---|---|---|---|---|---|"]
    for mod in sorted(rows):
        rs = rows[mod]
        fails = [r for r in rs if not r["exact"]]
        f = lambda v: f"{v:.2f}" if v is not None else "—"
        mw = np.mean([r["n_wrong"] for r in fails]) if fails else None
        md_ = np.median([r["n_wrong"] for r in fails]) if fails else None
        fw = np.mean([r["first_wrong"] for r in fails if r["first_wrong"] is not None]) if fails else None
        av = [r for r in fails if "n_wrong_at_variant" in r]
        wav = np.mean([r["n_wrong_at_variant"] for r in av]) if av else None
        ref = (np.sum([r["n_wrong_to_reference"] for r in av]) / max(1, np.sum([r["n_wrong_at_variant"] for r in av]))) if av else None
        md.append(f"| {mod} | {len(rs)} | {np.mean([r['exact'] for r in rs]):.2f} | {f(mw)} | "
                  f"{f(md_)} | {f(fw)} | {f(wav)} | {f(ref)} |")
    out = Path(args.root[0]) / "extract_fail.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
