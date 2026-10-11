"""Re-ask the masked cells for their records in their own idiom, from the saved final checkpoint.

    python -m pilot2.infill_audit --root outputs/human_mlm outputs/ecoli_mlm --gpu 0

The paper's extraction ruler reveals a prefix and masks everything after it, which matches
autoregressive conditioning and is the protocol every table reports. For a model that denoises
arbitrary positions that is one mask geometry among many, and it is the weakest one: on diffusion
language models, edge-conditioned masks recover up to three times more verbatim sequences than
prefix-conditioned ones (Wang and Asokan, arXiv:2605.24173). The paper's strongest claim -- a masked
objective reproduces nothing -- is therefore not established until the masked cells are asked with
the suffix left visible.

This script loads each masked cell's `final.pt`, rebuilds its dataset from `args.json` (the split is
a deterministic function of --data_seed, so the probes and hosts are the same sequences the run
trained on), and runs both protocols on the same checkpoints and the same canaries: prefix-
conditioned as in the paper, and edge-conditioned infilling with confidence-ordered decoding.
Non-members in a fresh host go through both as the control. Nothing is overwritten: results go to
`infill_audit.json` in each run directory and a summary table next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

from .data import build_dataset
from .model import Backbone
from .real_data import DATA_PATHS, build_real_dataset
from .score import extract_infill, extract_prefix
from .tokenizers import get_tokenizer
from .train import parse_objective

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?)_(?P<obj>mlm[0-9.]+)_s(?P<seed>\d+)$")


def rebuild(d: Path, device):
    """(model, tok, kind, ds) for one run directory, from its own args.json and final.pt."""
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    kind, _ = parse_objective(a["objective"])
    if kind == "ar":
        return None
    tok = get_tokenizer(a["tokenizer"], 288)
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    if a.get("data", "synthetic") != "synthetic":
        ds = build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], a["n_train"], a["n_val"], a["n_test"],
                                a["probes_per_tier"], tiers, a["n_nonmember"], a["data_seed"],
                                offset_mode=a["probe_offset"], canary_npz=a.get("canary_npz"))
    else:
        ds = build_dataset(a["n_train"], a["n_val"], a["n_test"], a["probes_per_tier"], tiers,
                           a["n_nonmember"], a["data_seed"], offset_mode=a["probe_offset"],
                           enrich_k=a.get("enrich_k"), enrich_factor=a.get("enrich_factor", 1.0))
    kw = {k: v for k, v in (("d_ff", a.get("d_ff")), ("emb_rank", a.get("emb_rank"))) if v}
    if a.get("pos_enc", "abs") != "abs":
        kw["pos_enc"] = a["pos_enc"]
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=False, **kw).to(device)
    model.load_state_dict(torch.load(d / "final.pt", map_location=device))
    model.eval()
    return model, tok, kind, ds, a


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--tiers", default="1,16")
    ap.add_argument("--max_probes", type=int, default=20, help="per tier, to keep the audit cheap")
    ap.add_argument("--name", default="infill_audit")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    tiers = [int(t) for t in args.tiers.split(",")]

    rows = []
    for root in args.root:
        for d in sorted(Path(root).iterdir()):
            if not (d.is_dir() and RUN.fullmatch(d.name) and (d / "final.pt").exists()):
                continue
            built = rebuild(d, device)
            if built is None:
                continue
            model, tok, kind, ds, a = built
            out = {"run": d.name, "data": a.get("data", "synthetic"), "objective": a["objective"],
                   "tokenizer": a["tokenizer"], "seed": a["seed"], "cells": []}
            per = defaultdict(lambda: defaultdict(list))
            for tier in tiers + [0]:
                ps = [p for p in ds.probes if p.repetitions == tier][:args.max_probes]
                for p in ps:
                    if tier > 0:
                        host, off = ds.train[p.host_rows[0]], p.offsets[0]
                        hname = "train"
                    else:
                        hosts = getattr(ds, "fresh_hosts", None)
                        host = (hosts[p.probe_id % len(hosts)].copy() if hosts is not None
                                else ds.test[p.probe_id % len(ds.test)].copy())
                        off, hname = 96, "fresh"
                    pre = extract_prefix(model, tok, kind, p, host, device, offset=off)
                    inf = extract_infill(model, tok, kind, p, host, device, offset=off)
                    per[tier]["prefix"].append(pre["exact"])
                    per[tier]["prefix_ham"].append(pre["hamming_nt"])
                    per[tier]["infill"].append(inf["exact"])
                    per[tier]["infill_ham"].append(inf["hamming_nt"])
                    out["cells"].append({"tier": tier, "host": hname, "probe_id": p.probe_id,
                                         "prefix": pre, "infill": inf})
            (d / "infill_audit.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            for tier in sorted(per, reverse=True):
                v = per[tier]
                rows.append((a.get("data", "synthetic"), a["tokenizer"], a["objective"], a["seed"], tier,
                             len(v["prefix"]), float(np.mean(v["prefix"])), float(np.mean(v["prefix_ham"])),
                             float(np.mean(v["infill"])), float(np.mean(v["infill_ham"]))))
                print(f"  {d.name:24s} r={tier:<3d} n={len(v['prefix']):3d}  "
                      f"prefix {100 * np.mean(v['prefix']):5.1f}% (ham {np.mean(v['prefix_ham']):5.1f})  "
                      f"infill {100 * np.mean(v['infill']):5.1f}% (ham {np.mean(v['infill_ham']):5.1f})", flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows:
        print("no masked cells with a final checkpoint under", args.root)
        return 1
    md = [f"# Edge-conditioned extraction audit of the masked cells — {args.name}", "",
          "`prefix` is the protocol the paper reports: reveal 48\\,nt and mask everything after it. "
          "`infill` reveals the same 48\\,nt and leaves the host AFTER the canary visible, decoding the "
          "48 masked nucleotides in confidence order -- the geometry that recovers up to 3x more from "
          "diffusion language models (Wang and Asokan, arXiv:2605.24173). Same checkpoints, same "
          "canaries, same hosts. `ham` is the mean number of wrong nucleotides out of 48.", "",
          "| dataset | tokeniser | objective | seed | tier | n | prefix exact | prefix ham | infill exact | infill ham |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | r={r[4]} | {r[5]} | {100 * r[6]:.0f}% | "
                  f"{r[7]:.1f} | **{100 * r[8]:.0f}%** | {r[9]:.1f} |")
    mem = [r for r in rows if r[4] > 0]
    if mem:
        md += ["", f"Member cells: prefix extraction {100 * max(r[6] for r in mem):.0f}% at worst, "
                   f"infill extraction {100 * max(r[8] for r in mem):.0f}% at worst; "
                   f"mean wrong nucleotides {np.mean([r[7] for r in mem]):.1f} (prefix) against "
                   f"{np.mean([r[9] for r in mem]):.1f} (infill)."]
    out = Path(args.root[0]) / f"{args.name}.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[-4:]))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
