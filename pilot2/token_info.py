"""Mechanism: why does a coarser tokenizer memorise more? Per-token accounting of the canary.

    python -m pilot2.token_info --root outputs/core100 outputs/bpe_arm --name synthetic
    python -m pilot2.token_info --root outputs/ecoli_ar outputs/bpe_arm --name ecoli --data ecoli

The tokenizer axis changes two things at once about a planted 96-nt canary:
  * how many token slots it occupies, T = 96 / k (char 96, 3-mer 32, 6-mer 16, BPE ~19);
  * how much information each slot carries, 2k bits at chance (char 2, 3-mer 6, 6-mer 12).
Their product is the same 192 bits for every tokenizer, so a per-nucleotide score is already
normalised for "how much there is to learn". The question is whether a model stores a roughly
fixed amount per SLOT, in which case a canary with fewer slots is memorised more completely for
the same effort, and the per-nucleotide curves that separate by tokenizer should collapse when
re-expressed per token slot.

This script re-reads the saved score files and reports, at matched held-out loss:
    memorised bits/nt  = 2 - probe_bits_per_nt                     (what the reports show)
    memorised bits/tok = (2 - probe_bits_per_nt) * 96 / T          (the same thing per slot)
    stored fraction    = memorised bits/nt / 2                     (unitless)
and, from the training corpus, the statistic that explains the per-slot cost: the number of times
the tokens making up a canary occur elsewhere in the corpus. A canary token that is unique to the
canary needs no interference-free capacity bargain; a token shared with thousands of ordinary
windows must be stored in context, which is harder. Coarse tokenizers put canaries into rarer
tokens, so their slots are cheaper to make unique.

Writes <name>_token_info.md and, with --plot, <name>_token_info.png next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .data import PROBE_LEN, WINDOW, build_dataset, decode

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?|bpe\d+)(?:_(?P<data>ecoli|yeast|gue))?_(?P<obj>ar|mlm[0-9.]+)_s(?P<seed>\d+)$")
GRID = (2.03, 2.05, 2.10, 2.20, 2.40)


def tokens_per_probe(tok_name: str, ds, vocab_file=None) -> tuple[float, int]:
    """(mean token slots covering a 96-nt canary, vocab size)."""
    if tok_name.startswith("bpe"):
        from .bpe_arm import BpeTokenizer
        voc = BpeTokenizer(vocab_file or f"data/tokenizers/{tok_name}_ecoli.json")
        n = []
        for p in ds.probes[:200]:
            ids, spans = voc.encode_str(decode(p.seq))
            n.append(len(ids))
        return float(np.mean(n)), voc.vocab_size
    k = 1 if tok_name == "char" else int(re.match(r"(\d+)", tok_name).group(1))
    return PROBE_LEN / k, 3 + 4 ** k


def corpus_token_stats(tok_name: str, ds, vocab_file=None) -> dict:
    """How often do the tokens of a canary occur in the training corpus outside the canary rows?"""
    from .tokenizers import get_tokenizer
    probe_rows = {r for p in ds.probes for r in p.host_rows}
    ordinary = np.array([i for i in range(len(ds.train)) if i not in probe_rows])[:4000]
    if tok_name.startswith("bpe"):
        from .bpe_arm import BpeTokenizer
        voc = BpeTokenizer(vocab_file or f"data/tokenizers/{tok_name}_ecoli.json")
        enc = lambda rows: [voc.encode_str(decode(w))[0] for w in rows]
        corpus = Counter(t for ids in enc(ds.train[ordinary]) for t in ids)
        probe_tok = [voc.encode_str(decode(p.seq))[0] for p in ds.probes[:200]]
    else:
        t = get_tokenizer(tok_name, WINDOW)
        corpus = Counter(int(x) for x in t.encode(ds.train[ordinary]).ravel())
        probe_tok = []
        for p in ds.probes[:200]:
            pad = PROBE_LEN - PROBE_LEN % t.k
            probe_tok.append([int(x) for x in t.encode(p.seq[None, :pad])[0]])
    freq = np.array([np.mean([corpus.get(x, 0) for x in ids]) for ids in probe_tok])
    uniq = np.array([np.mean([corpus.get(x, 0) == 0 for x in ids]) for ids in probe_tok])
    return {"corpus_windows": int(len(ordinary)),
            "canary_token_corpus_count_mean": float(freq.mean()),
            "canary_token_unseen_fraction": float(uniq.mean()),
            "distinct_tokens_in_corpus": int(len(corpus))}


def tier_bits(r, tier, host="train"):
    sc = "ar" if r.get("kind") == "ar" else "pll"
    key = f"{sc}/{host}"
    ps = [p for p in r["probes"] if p["repetitions"] == tier and key in p["ranks"]]
    if not ps:
        return None
    return float(np.mean([p["ranks"][key]["probe_bits_per_nt"] for p in ps]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--name", default="synthetic")
    ap.add_argument("--data", default="synthetic")
    ap.add_argument("--fasta", default=None)
    ap.add_argument("--tiers", default="1,16")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args(argv)

    if args.data == "synthetic":
        ds = build_dataset(5000, 500, 500, 50, (1, 4, 16), 50, 1234, offset_mode="random")
    else:
        from .real_data import DATA_PATHS, build_real_dataset
        ds = build_real_dataset(args.fasta or DATA_PATHS[args.data], 5000, 500, 500, 50, (1, 4, 16), 50, 1234,
                                offset_mode="random")

    curves = defaultdict(lambda: defaultdict(list))      # tok -> epoch -> [(floor, {tier: bits})]
    vocab_files = {}
    for root in args.root:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m or m["obj"] != "ar":
                continue
            if m["data"] and m["data"] != args.data:   # a run name may carry its dataset; a plain name
                continue                                   # belongs to whatever --data the roots were built with
            for f in sorted(d.glob("scores_ep*.json"), key=lambda p: int(p.stem.split("ep")[1])):
                r = json.loads(f.read_text(encoding="utf-8"))
                if "vocab_file" in r:
                    vocab_files[m["tok"]] = r["vocab_file"]
                ep = int(f.stem.split("ep")[1])
                curves[m["tok"]][ep].append((r["floors"][0]["bits_per_nt_mean"],
                                             {t: tier_bits(r, t) for t in (1, 4, 16)}))
    if not curves:
        print("no AR runs for data =", args.data, "under", args.root); return 1

    stats, rows = {}, []
    for tok in curves:
        T, V = tokens_per_probe(tok, ds, vocab_files.get(tok))
        cs = corpus_token_stats(tok, ds, vocab_files.get(tok))
        stats[tok] = {"tokens_per_canary": T, "nt_per_token": PROBE_LEN / T, "vocab_size": V,
                      "bits_per_token_at_chance": 2 * PROBE_LEN / T, **cs}
        for ep, runs in sorted(curves[tok].items()):
            fl = float(np.mean([x[0] for x in runs]))
            for t in (1, 4, 16):
                v = [x[1][t] for x in runs if x[1][t] is not None]
                if v:
                    b = float(np.mean(v))
                    rows.append({"tok": tok, "epoch": ep, "floor": fl, "tier": t, "probe_bits_nt": b,
                                 "mem_bits_nt": 2.0 - b, "mem_bits_tok": (2.0 - b) * PROBE_LEN / T})

    order = sorted(stats, key=lambda t: stats[t]["nt_per_token"])
    md = [f"# Per-token accounting of the canary — {args.name}", "",
          "A 96-nt canary is 192 bits for every tokenizer; what changes is how many token slots carry them.", "",
          "| tokenizer | nt/token | slots per canary | vocab | bits/slot at chance | canary-token corpus count | unseen in corpus |",
          "|---|---|---|---|---|---|---|"]
    for t in order:
        s = stats[t]
        md.append(f"| {t} | {s['nt_per_token']:.2f} | {s['tokens_per_canary']:.1f} | {s['vocab_size']} | "
                  f"{s['bits_per_token_at_chance']:.1f} | {s['canary_token_corpus_count_mean']:.0f} | "
                  f"{s['canary_token_unseen_fraction']:.2f} |")

    tiers = [int(x) for x in args.tiers.split(",")]
    md += ["", "## Memorisation at matched held-out loss: per nucleotide vs per token slot", "",
           "Per-nucleotide values separate the tokenizers (the result of the paper). If a model stores a roughly "
           "fixed amount per slot, the per-slot values are closer together, and the residual spread is the part the "
           "tokenizer explains beyond slot counting.", ""]
    for tier in tiers:
        md += [f"### r={tier}", "",
               "| tokenizer | " + " | ".join(f"@{g:.2f}" for g in GRID) + " | unit |",
               "|---|" + "---|" * (len(GRID) + 1)]
        for t in order:
            pts = sorted({(w["floor"], w["mem_bits_nt"], w["mem_bits_tok"]) for w in rows
                          if w["tok"] == t and w["tier"] == tier})
            if len(pts) < 2:
                continue
            f = np.array([p[0] for p in pts]); start = int(np.argmin(f))
            for col, unit in ((1, "bits/nt"), (2, "bits/slot")):
                y = np.array([p[col] for p in pts])
                f2, y2 = f[start:], y[start:]
                o = np.argsort(f2); f2, y2 = f2[o], y2[o]
                cells = [f"{np.interp(g, f2, y2):.3f}" if f2[0] <= g <= f2[-1] else "—" for g in GRID]
                md.append(f"| {t} | " + " | ".join(cells) + f" | {unit} |")
        md.append("")

    out = Path(args.root[0]) / f"{args.name}_token_info.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    (Path(args.root[0]) / f"{args.name}_token_info.json").write_text(
        json.dumps({"stats": stats, "rows": rows}, indent=1), encoding="utf-8")
    print("\n".join(md)); print(f"-> {out}")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
        for ax, col, lab in ((axes[0], "mem_bits_nt", "memorised bits / nucleotide"),
                             (axes[1], "mem_bits_tok", "memorised bits / token slot")):
            for t in order:
                pts = sorted({(w["floor"], w[col]) for w in rows if w["tok"] == t and w["tier"] == 16})
                if len(pts) < 2:
                    continue
                f = np.array([p[0] for p in pts]); y = np.array([p[1] for p in pts])
                s = int(np.argmin(f))
                ax.plot(f[s:], y[s:], "o-", ms=3.5, label=t)
            ax.set_xlabel("held-out loss (bits/nt, higher = more overfit)")
            ax.set_ylabel(lab); ax.set_xlim(1.95, 2.6); ax.grid(alpha=0.3)
        axes[0].set_title("per nucleotide: tokenizers separate")
        axes[1].set_title("per token slot: same amount stored per slot?")
        axes[1].legend(fontsize=8)
        fig.suptitle(f"16x canary, {args.name}: the tokenizer effect is slot accounting", fontsize=10)
        fig.tight_layout()
        png = Path(args.root[0]) / f"{args.name}_token_info.png"
        fig.savefig(png, dpi=150)
        print(f"-> {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
