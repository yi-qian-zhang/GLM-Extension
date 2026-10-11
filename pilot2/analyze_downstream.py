"""Downstream utility against leakage, per task and per round -- the table Sec. 6 of the paper needs.

    python -m pilot2.analyze_downstream --root outputs/dnabert_gue_ds outputs/dnabert_gue_ds2 \
        outputs/dnabert_yeast_ds outputs/hyena_gue_ds outputs/hyena_gue_ds2 outputs/hyena_yeast_ds

For every (model, task, round) it reports the fine-tuned and frozen-probe MCC beside the canary of
the SAME checkpoint, because the paper's claim is that the two move independently: the task score is
flat while the planted record goes from unmemorised to verbatim. Two summaries follow:

  * per task, the round-0 / mid / last MCC and the total movement, with the leakage at the last round;
  * per model, the round of lowest held-out loss (what early stopping would pick) and the round of
    highest downstream MCC (what benchmark selection would pick), with the canary at each.

Writes <name>_downstream.md next to the first root.
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
LABEL = {"dnabert3": "DNABERT 3-mer", "dnabert4": "DNABERT 4-mer", "dnabert5": "DNABERT 5-mer",
         "dnabert6": "DNABERT 6-mer", "dnabert2bpe": "DNABERT-2 BPE", "hyena_medium-160k": "HyenaDNA medium"}
TASK = {"prom_300_all": "promoter detection (human)", "gue_prom_300_all": "promoter detection (human)",
        "prom_core_all": "core promoter (human)", "human_tf_0": "TF binding (human)",
        "splice_reconstructed": "splice sites (human, 3-class)", "emp_H3": "histone H3 (yeast)",
        "emp_H3K4me3": "histone H3K4me3 (yeast)"}
ORDER = list(TASK)


def epoch_of(f: Path, r: dict) -> int:
    if f.stem.startswith("scores_ep"):
        return int(f.stem.split("ep")[1])
    return int(r.get("epoch") or r.get("train_summary", {}).get("epochs") or 0)


def canary(r: dict, tier: int = 16):
    """(bits/nt, recognition rate, extraction rate) for the member canaries of this checkpoint."""
    key = next((k for k in ("causal/train", "ar/train", "span_pll/train", "pll/train")
                if any(k in p["ranks"] for p in r["probes"])), None)
    ps = [p for p in r["probes"] if p["repetitions"] == tier and key and key in p["ranks"]]
    if not ps:
        return None
    rk = [p["ranks"][key] for p in ps]
    top1 = [float(x.get("rank", 0) == 1) if "rank" in x else float(x.get("top1", 0.0)) for x in rk]
    return (float(np.mean([x["probe_bits_per_nt"] for x in rk])), float(np.mean(top1)),
            float(np.mean([p["extract"]["train"]["exact"] for p in ps])))


def collect(roots):
    """model -> epoch -> {"floor", "canary", task -> (probe_mcc, ft_mcc)}, averaged over seeds"""
    acc = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for root in roots:
        p = Path(root)
        if not p.is_dir():
            continue
        for d in sorted(p.iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m:
                continue
            for f in sorted(d.glob("scores_ep*.json")) + [d / "scores_final.json"]:
                if not f.exists():
                    continue
                r = json.loads(f.read_text(encoding="utf-8"))
                ds = (r.get("downstream") or {}).get("tasks") or {}
                if not ds:
                    continue
                ep = epoch_of(f, r)
                cell = acc[m["model"]][ep]
                cell["floor"].append(r["floors"][0]["bits_per_nt_mean"])
                c = canary(r)
                if c:
                    cell["canary"].append(c)
                for t, v in ds.items():
                    cell[t].append((v.get("linear_probe", {}).get("mcc"), v.get("finetune", {}).get("mcc")))
    return acc


def mean_task(vals):
    pr = [v[0] for v in vals if v[0] is not None]
    ft = [v[1] for v in vals if v[1] is not None]
    return (float(np.mean(pr)) if pr else None, float(np.mean(ft)) if ft else None)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--name", default="utility")
    args = ap.parse_args(argv)

    acc = collect(args.root)
    if not acc:
        print("no downstream results under", args.root)
        return 1
    models = sorted(acc, key=lambda m: (not m.startswith("dnabert"), m))
    md = [f"# Downstream utility against leakage — {args.name}", "",
          "MCC on each task's full test split, seed means: `ft` is the fine-tuned head (the published "
          "recipe, scaled down), `probe` is a frozen mean-pooled linear probe. `canary` is the "
          "$16\\times$ member canary of the SAME checkpoint: bits/nt, recognition (rank-1 among 100), "
          "verbatim extraction.", ""]

    for m in models:
        eps = sorted(acc[m])
        tasks = [t for t in ORDER if any(t in acc[m][e] for e in eps)]
        if not tasks:
            continue
        md += [f"## {LABEL.get(m, m)}", "",
               "| round | held-out loss | canary bits/nt | recognised | extracted | "
               + " | ".join(f"{TASK.get(t, t)}" for t in tasks) + " |",
               "|---|---|---|---|---|" + "---|" * len(tasks)]
        for e in eps:
            cell = acc[m][e]
            fl = float(np.mean(cell["floor"])) if cell["floor"] else float("nan")
            c = (float(np.mean([x[0] for x in cell["canary"]])),
                 float(np.mean([x[1] for x in cell["canary"]])),
                 float(np.mean([x[2] for x in cell["canary"]]))) if cell["canary"] else (float("nan"),) * 3
            cells = []
            for t in tasks:
                if t not in cell:
                    cells.append("—")
                    continue
                pr, ft = mean_task(cell[t])
                cells.append((f"{ft:.3f}" if ft is not None else "—") + (f" ({pr:.3f})" if pr is not None else ""))
            md.append(f"| {e} | {fl:.3f} | {c[0]:.2f} | {100 * c[1]:.0f}% | {100 * c[2]:.0f}% | "
                      + " | ".join(cells) + " |")
        md.append("")

    md += ["## What a practitioner's stopping rule would pick", "",
           "| model | best held-out loss | canary there | best downstream | canary there | last round | canary there |",
           "|---|---|---|---|---|---|---|"]
    for m in models:
        eps = [e for e in sorted(acc[m]) if e > 0 and acc[m][e]["canary"]]
        if not eps:
            continue
        floor = {e: float(np.mean(acc[m][e]["floor"])) for e in eps}
        ext = {e: float(np.mean([x[2] for x in acc[m][e]["canary"]])) for e in eps}
        ftm = {}
        for e in eps:
            v = [mean_task(acc[m][e][t])[1] for t in ORDER if t in acc[m][e]]
            v = [x for x in v if x is not None]
            if v:
                ftm[e] = float(np.mean(v))
        if not ftm:
            continue
        e_loss = min(floor, key=floor.get)
        e_ds = max(ftm, key=ftm.get)
        e_last = max(eps)
        md.append(f"| {LABEL.get(m, m)} | round {e_loss} ({floor[e_loss]:.3f}) | {100 * ext[e_loss]:.0f}% extracted "
                  f"| round {e_ds} (MCC {ftm[e_ds]:.3f}) | {100 * ext[e_ds]:.0f}% extracted "
                  f"| round {e_last} | {100 * ext[e_last]:.0f}% extracted |")

    out = Path(args.root[0]) / f"{args.name}_downstream.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
