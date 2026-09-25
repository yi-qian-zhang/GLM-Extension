"""Aggregate outputs/pilot/*/scores.json into a Gate-1 report (markdown + json).

    python -m pilot2.report --root outputs/pilot

Answers the three Gate-1 questions:
  Q1  scorer consistency on the MLM model: do pll and prefix rank the same
      probes the same way, and do both sit on the 2.000 bits/nt floor?
  Q2  dynamic range: does r=16 beat r=1 beat non-member, beyond seed noise?
  Q3  objective signal: under matched conditioning (ar scorer on the AR
      model vs prefix scorer on the MLM model), do the objectives differ?
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

try:
    from scipy.stats import mannwhitneyu, spearmanr
except Exception:  # scipy is optional
    mannwhitneyu = spearmanr = None


def load_runs(root: Path, scores_name: str = "scores.json"):
    runs = {}
    for f in sorted(root.glob(f"*/{scores_name}")):
        if "smoke" in str(f):
            continue
        runs[f.parent.name] = json.loads(f.read_text(encoding="utf-8"))
    return runs


def tier_stats(run, key):
    """key like 'ar/train'. Returns {repetitions: {ranks, bits, exact}}."""
    out = defaultdict(lambda: {"rank": [], "p": [], "bits": [], "z": []})
    for p in run["probes"]:
        if key in p["ranks"]:
            r = p["ranks"][key]
            d = out[p["repetitions"]]
            d["rank"].append(r["rank"]); d["p"].append(r["p_chance"])
            d["bits"].append(r["probe_bits_per_nt"]); d["z"].append(r["z"])
    return out


def extract_stats(run, host):
    out = defaultdict(list)
    for p in run["probes"]:
        if host in p["extract"]:
            out[p["repetitions"]].append(p["extract"][host])
    return {r: {"n": len(v), "exact_rate": float(np.mean([e["exact"] for e in v])),
                "mean_hamming": float(np.mean([e["hamming"] for e in v]))} for r, v in out.items()}


def fmt_tier(d):
    rows = []
    for r in sorted(d):
        s = d[r]
        rank = np.array(s["rank"]); p = np.array(s["p"])
        rows.append(f"| r={r} | {len(rank)} | {np.median(rank):.0f} | {(rank == 1).mean():.2f} | "
                    f"{(p <= 0.01).mean():.2f} | {np.mean(s['bits']):.3f} | {np.mean(s['z']):+.2f} |")
    return ["| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |",
            "|---|---|---|---|---|---|---|"] + rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/pilot")
    ap.add_argument("--scores_name", default="scores.json")
    args = ap.parse_args(argv)
    root = Path(args.root)
    runs = load_runs(root, args.scores_name)
    suffix = "" if args.scores_name == "scores.json" else "_" + args.scores_name.replace("scores_", "").replace(".json", "")
    if not runs:
        print("no runs found under", root); return 1
    md = ["# Gate 1 report", "", f"root: {root}   scores file: {args.scores_name}", f"runs: {', '.join(runs)}", ""]
    summary = {}

    md += ["## Training and throughput", "", "| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |", "|---|---|---|---|---|---|---|---|"]
    for name, r in runs.items():
        ts = r["train_summary"]
        log = [json.loads(l) for l in (root / name / "train_log.jsonl").read_text().splitlines() if '"mfu"' in l]
        mfu = log[-1]["mfu"] if log else float("nan")
        md.append(f"| {name} | {ts.get('tokenizer','char')} | {ts['n_params']/1e6:.2f}M ({ts['n_params_non_embedding']/1e6:.2f}M) | "
                  f"{ts.get('steps','?')} | {ts.get('supervised_tokens_seen',0)/1e6:.1f}M | "
                  f"{ts['total_train_sec']:.0f} | {r['score_sec']:.0f} | {mfu:.2f} |")
        summary.setdefault(name, {})["mfu"] = mfu

    md += ["", "## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)", "",
           "| run | scorer | bits/nt | perplexity | min window | ok |", "|---|---|---|---|---|---|"]
    for name, r in runs.items():
        for f in r["floors"]:
            md.append(f"| {name} | {f['scorer']} | {f['bits_per_nt_mean']:.4f} | {f.get('perplexity_nt', f.get('perplexity', 0)):.4f} | "
                      f"{f['min_window_bits']:.3f} | {'OK' if f['floor_ok'] else '**VIOLATION**'} |")
            summary[name][f"floor/{f['scorer']}"] = f["bits_per_nt_mean"]

    md += ["", "## Ranking against the random pool, by tier (host = training window for members, fresh for all)", ""]
    for name, r in runs.items():
        for key in sorted({k for p in r["probes"] for k in p["ranks"]}):
            md += [f"### {name} — scorer `{key}`  (pool n={r['pool_size']}, chance rank-1 = {1/(r['pool_size']+1):.4f})", ""]
            md += fmt_tier(tier_stats(r, key)) + [""]

    md += ["## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)", "",
           "| run | host | tier | n | exact rate | mean hamming (of 48) |", "|---|---|---|---|---|---|"]
    for name, r in runs.items():
        for host in ("train", "fresh"):
            for tier, s in sorted(extract_stats(r, host).items()):
                md.append(f"| {name} | {host} | r={tier} | {s['n']} | {s['exact_rate']:.2f} | {s['mean_hamming']:.1f} |")

    # ---- Q1: pll vs prefix agreement on MLM runs
    md += ["", "## Q1 — scorer consistency on the MLM model (pll vs prefix)", ""]
    for name, r in runs.items():
        if r["kind"] != "mlm":
            continue
        for host in ("fresh", "train"):
            a = [p["ranks"].get(f"pll/{host}") for p in r["probes"]]
            b = [p["ranks"].get(f"prefix/{host}") for p in r["probes"]]
            pairs = [(x["probe_bits_per_nt"], y["probe_bits_per_nt"], x["rank"], y["rank"]) for x, y in zip(a, b) if x and y]
            if not pairs:
                continue
            arr = np.array(pairs)
            if spearmanr:
                rho_b = spearmanr(arr[:, 0], arr[:, 1]).correlation
                rho_r = spearmanr(arr[:, 2], arr[:, 3]).correlation
            else:
                rho_b = np.corrcoef(arr[:, 0], arr[:, 1])[0, 1]; rho_r = np.corrcoef(arr[:, 2], arr[:, 3])[0, 1]
            top_a = {i for i, p in enumerate(pairs) if p[2] == 1}; top_b = {i for i, p in enumerate(pairs) if p[3] == 1}
            jac = len(top_a & top_b) / max(1, len(top_a | top_b))
            md.append(f"- **{name} / {host}**: n={len(pairs)}, Spearman(bits) = {rho_b:.3f}, Spearman(rank) = {rho_r:.3f}, "
                      f"rank-1 set Jaccard = {jac:.2f} ({len(top_a)} vs {len(top_b)} rank-1)")
            summary[name][f"q1/{host}/spearman_bits"] = float(rho_b)

    # ---- Q2: dynamic range, r=16 vs r=1 vs non-member, per run on its natural scorer
    md += ["", "## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host", ""]
    for name, r in runs.items():
        key = ("ar" if r["kind"] == "ar" else "prefix") + "/fresh"
        d = tier_stats(r, key)
        if 16 in d and 1 in d and 0 in d:
            b16, b1, b0 = map(np.array, (d[16]["bits"], d[1]["bits"], d[0]["bits"]))
            line = (f"- **{name}** ({key}): bits/nt  r=16 {b16.mean():.3f}±{b16.std():.3f} | r=1 {b1.mean():.3f}±{b1.std():.3f} | "
                    f"non-member {b0.mean():.3f}±{b0.std():.3f};  rank-1 rate r=16 {np.mean(np.array(d[16]['rank'])==1):.2f}, "
                    f"r=1 {np.mean(np.array(d[1]['rank'])==1):.2f}, non-member {np.mean(np.array(d[0]['rank'])==1):.2f}")
            if mannwhitneyu:
                p16 = mannwhitneyu(b16, b0, alternative="less").pvalue
                p1 = mannwhitneyu(b1, b0, alternative="less").pvalue
                line += f";  MWU p(r=16 < non-member) = {p16:.2e}, p(r=1 < non-member) = {p1:.2e}"
            md.append(line)
            summary[name]["q2/gap_r16_vs_nonmember_bits"] = float(b0.mean() - b16.mean())
            summary[name]["q2/gap_r1_vs_nonmember_bits"] = float(b0.mean() - b1.mean())

    # ---- Q3: objective signal under matched conditioning
    md += ["", "## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)", ""]
    by_kind = defaultdict(list)
    for name, r in runs.items():
        key = ("ar" if r["kind"] == "ar" else "prefix") + "/train"
        d = tier_stats(r, key)
        if 16 in d:
            by_kind[r["kind"]].append((name, np.mean(d[16]["bits"]), np.mean(np.array(d[16]["rank"]) == 1),
                                       extract_stats(r, "train").get(16, {}).get("exact_rate", float("nan"))))
    for kind, rows in by_kind.items():
        for name, bits, r1, ex in rows:
            md.append(f"- {kind:3s} **{name}**: r=16 probe bits/nt {bits:.3f}, rank-1 rate {r1:.2f}, exact-extraction rate {ex:.2f}")
    if "ar" in by_kind and "mlm" in by_kind:
        a = np.array([x[1] for x in by_kind["ar"]]); m = np.array([x[1] for x in by_kind["mlm"]])
        md.append(f"- **Δ(MLM − AR) r=16 bits/nt = {m.mean()-a.mean():+.3f}**  (seed spread: AR ±{a.std():.3f}, MLM ±{m.std():.3f})")
        summary["q3/delta_bits_mlm_minus_ar"] = float(m.mean() - a.mean())

    md += ["", "> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask "
           "already hides every position to the right, so masking the target changes nothing and PLL reduces exactly "
           "to AR scoring. The consistency check is therefore run on the MLM model between its two scorers."]
    (root / "gate1_report.md").write_text("\n".join(md), encoding="utf-8")
    (root / "gate1_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
