"""Memorisation vs utility for the real-model runs (DNABERT k-mer, DNABERT-2 BPE, HyenaDNA) on one dataset root
or several (one table per root), plus the from-scratch backbone roots if given.

    python -m pilot2.analyze_real --root outputs/dnabert_ecoli outputs/hyena_ecoli --name ecoli
    python -m pilot2.analyze_real --root outputs/dnabert_yeast outputs/hyena_yeast --name yeast

Rows = (model, epoch), averaged over seeds. Utility = held-out floor (bits/nt on unseen real windows; lower is better).
Canary cells = probe bits/nt / rank-1 / exact extraction (training host; r=16 also on a fresh host).
The "best utility" table takes, per model, the epoch with the lowest seed-mean floor and reports the r=16 canary there,
which is the test of "does stopping at the utility optimum prevent memorisation".
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

RUN = re.compile(r"(?P<model>dnabert\d|dnabert2bpe|hyena_[a-z0-9-]+?)(?P<var>_[A-Za-z0-9._-]+?)?_s(?P<seed>\d+)$")
ORDER = {"dnabert3": 0, "dnabert4": 1, "dnabert5": 2, "dnabert6": 3, "dnabert2bpe": 4}
LABEL = {"dnabert3": "DNABERT 3-mer", "dnabert4": "DNABERT 4-mer", "dnabert5": "DNABERT 5-mer", "dnabert6": "DNABERT 6-mer",
         "dnabert2bpe": "DNABERT-2 BPE"}


def label(model, var):
    base = LABEL.get(model, model.replace("hyena_", "HyenaDNA "))
    v = [x for x in (var or "").strip("_").split("_") if x and x not in ("causal",) and not x.startswith(("ecoli", "yeast", "gue"))]
    if model.startswith("dnabert") and "causal" not in (var or ""):
        v.insert(0, "mlm")
    return base + (f" ({' '.join(v)})" if v else "")


def tier(r, t, host):
    key = next((k for k in (f"causal/{host}", f"span_pll/{host}", f"pll/{host}") if any(k in p["ranks"] for p in r["probes"])), None)
    ps = [p for p in r["probes"] if p["repetitions"] == t and key in p["ranks"]]
    if not ps:
        return None
    return (np.mean([p["ranks"][key]["probe_bits_per_nt"] for p in ps]), np.mean([p["ranks"][key]["rank"] == 1 for p in ps]),
            np.mean([p["extract"][host]["exact"] for p in ps]), len(ps))


def collect(roots):
    rows = []
    for root in roots:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m:
                continue
            files = sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem[9:])) + [d / "scores_final.json"]
            for f in files:
                if not f.exists():
                    continue
                r = json.loads(f.read_text(encoding="utf-8"))
                row = {"model": m["model"], "var": m["var"] or "", "seed": int(m["seed"]), "epoch": int(r["epoch"]),
                       "floor": r["floors"][0]["bits_per_nt_mean"], "lab": label(m["model"], m["var"])}
                ds = r.get("downstream") or {}
                tasks = ds.get("tasks") or ({ds["task"]: ds} if ds else {})
                row["tasks"] = list(tasks)
                row["probe_by_task"] = {t: v["linear_probe"]["mcc"] for t, v in tasks.items() if v.get("linear_probe")}
                row["ft_by_task"] = {t: v["finetune"]["mcc"] for t, v in tasks.items() if v.get("finetune")}
                row["probe_mcc"] = float(np.mean(list(row["probe_by_task"].values()))) if row["probe_by_task"] else None
                row["ft_mcc"] = float(np.mean(list(row["ft_by_task"].values()))) if row["ft_by_task"] else None
                for t in (0, 1, 4, 16):
                    for host in ("train", "fresh"):
                        s = tier(r, t, host)
                        if s:
                            row[(t, host)] = s
                rows.append(row)
    return rows


def fmt(s):
    return f"{s[0]:.2f} / {s[1]:.2f} / {s[2]:.2f}" if s else "—"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--name", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    rows = collect(args.root)
    if not rows:
        print("no runs"); return 1
    name = args.name or Path(args.root[0]).name
    by = defaultdict(list)
    for w in rows:
        by[(w["lab"], w["model"], w["var"], w["epoch"])].append(w)
    key = lambda k: (ORDER.get(k[1], 9), k[2], k[3])
    md = [f"# Real models on {name}: memorisation vs utility", "",
          "utility = held-out bits/nt on unseen windows of the same dataset (lower = better); canary cells = bits/nt / rank-1 / exact extraction, "
          "r=16 on the training host and on a fresh host; seeds = runs averaged.", "",
          "| model | epoch | seeds | utility | GUE probe MCC | GUE ft MCC | r=1 train | r=4 train | r=16 train | r=16 fresh |", "|---|---|---|---|---|---|---|---|---|---|"]
    all_tasks = sorted({t for w in rows for t in w.get("tasks", [])})
    if all_tasks:
        md.insert(3, f"downstream tasks (GUE, MCC on the full test split; several tasks are listed in this order): {', '.join(all_tasks)}; the best-downstream table uses the mean over tasks.")
    agg = defaultdict(dict)
    for k in sorted(by, key=key):
        ws = by[k]
        ms = lambda kk: (lambda v: (np.mean([x[0] for x in v]), np.mean([x[1] for x in v]), np.mean([x[2] for x in v])) if v else None)([w[kk] for w in ws if kk in w])
        fl = float(np.mean([w["floor"] for w in ws]))
        cells = [ms((1, "train")), ms((4, "train")), ms((16, "train")), ms((16, "fresh"))]
        mm = lambda key: (lambda v: float(np.mean(v)) if v else None)([w[key] for w in ws if w.get(key) is not None])
        pm, fm = mm("probe_mcc"), mm("ft_mcc")
        def per_task(key):
            ts = sorted({t for w in ws for t in w.get(key, {})})
            if not ts: return None
            return " / ".join(f"{np.mean([w[key][t] for w in ws if t in w.get(key, {})]):.3f}" for t in ts)
        f3 = lambda v: (v if isinstance(v, str) else f"{v:.3f}") if v is not None else "—"
        agg[(k[0], k[1], k[2])][k[3]] = (fl, cells, len(ws), fm)
        md.append(f"| {k[0]} | {k[3]} | {len(ws)} | {fl:.3f} | {f3(per_task('probe_by_task'))} | {f3(per_task('ft_by_task'))} | " + " | ".join(fmt(c) for c in cells) + " |")
    md += ["", "## At the best-utility epoch (lowest seed-mean held-out loss, epoch > 0)", "",
           "| model | best epoch | utility there | r=16 train | r=16 fresh | r=1 train | utility at last epoch | r=16 train at last |",
           "|---|---|---|---|---|---|---|---|"]
    ds_rows = []
    for (lab, model, var), eps in sorted(agg.items(), key=lambda kv: (ORDER.get(kv[0][1], 9), kv[0][2])):
        cand = {e: v for e, v in eps.items() if e > 0}
        if not cand:
            continue
        be = min(cand, key=lambda e: cand[e][0]); le = max(cand)
        fl, cells, _, _ = cand[be]; fl2, cells2, _, _ = cand[le]
        md.append(f"| {lab} | {be} | {fl:.3f} | {fmt(cells[2])} | {fmt(cells[3])} | {fmt(cells[0])} | {fl2:.3f} (ep {le}) | {fmt(cells2[2])} |")
        dsc = {e: v for e, v in cand.items() if v[3] is not None}
        if dsc:
            bd = max(dsc, key=lambda e: dsc[e][3])
            ds_rows.append(f"| {lab} | {bd} | {dsc[bd][3]:.3f} | {dsc[bd][0]:.3f} | {fmt(dsc[bd][1][2])} | {fmt(dsc[bd][1][3])} | {dsc[le][3]:.3f} (ep {le}) |" if le in dsc else f"| {lab} | {bd} | {dsc[bd][3]:.3f} | {dsc[bd][0]:.3f} | {fmt(dsc[bd][1][2])} | {fmt(dsc[bd][1][3])} | — |")
    if ds_rows:
        md += ["", "## At the best DOWNSTREAM epoch (highest GUE promoter fine-tune MCC, epoch > 0)", "",
               "| model | best epoch | ft MCC there | utility there | r=16 train | r=16 fresh | ft MCC at last epoch |", "|---|---|---|---|---|---|---|"] + ds_rows
    out = Path(args.out) if args.out else Path(args.root[0]) / f"real_report_{name}.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md)); print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
