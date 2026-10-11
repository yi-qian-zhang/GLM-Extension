"""Memorisation of sequence the corpus repeats BY ITSELF -- no canary is planted anywhere.

    python -m pilot2.natural_dups --root outputs/ecoli_ar outputs/human_toy --gpu 0

Every number in the paper so far comes from records we inserted. The obvious objection is that
insertion is the effect: a 96\,nt block dropped into otherwise unrelated windows may be memorised
because it is anomalous, not because it repeats. Real genomes repeat sequence on their own --
transposons, paralogues, segmental duplications, promoter motifs -- so the objection is testable
without changing anything about the models.

This script re-reads a finished run's own training set, finds 96\,nt blocks that occur more than once
in it by nature, and applies the paper's three rulers to them from the saved `final.pt`:

  * duplicates are found by hashing every 96\,nt block at a fixed stride across the training windows,
    then keeping the distinct blocks whose occurrence count is at least 2. Blocks that overlap a
    planted canary are dropped, so the two populations never mix;
  * each duplicate is scored in one of its own host windows, exactly as a planted canary would be:
    surprise per nucleotide, rank against a pool of single-occurrence blocks, and 48\,nt
    prefix-conditioned extraction;
  * singletons (count 1) are the control, drawn from the same corpus and scored the same way.

The claim to test is that the two axes of the paper reappear without planting: memorisation rising
with how often the block repeats, and, at matched held-out loss, with the coarseness of the
tokeniser. Writes <name>_natural.md next to the first root.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch

from .data import PROBE_LEN, Probe, build_dataset, decode
from .model import Backbone
from .real_data import DATA_PATHS, build_real_dataset
from .score import extract_prefix, rank_probe
from .tokenizers import get_tokenizer
from .train import parse_objective

RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?|bpe\d+)(?P<rest>_[A-Za-z0-9._@-]+?)?_s(?P<seed>\d+)$")
BINS = [(1, 1), (2, 2), (3, 4), (5, 8), (9, 10 ** 9)]
BINLAB = {(1, 1): "1 (control)", (2, 2): "2", (3, 4): "3-4", (5, 8): "5-8", (9, 10 ** 9): "9+"}


def find_duplicates(train: np.ndarray, tag: np.ndarray, stride: int, max_rows: int):
    """-> {count_bin: [(seq, row, offset)]}, from blocks the corpus repeats on its own.

    `tag` is the dataset's canary tag per row (-1 = ordinary window); rows carrying a planted canary
    are skipped entirely, so a planted record can never be counted as a natural duplicate."""
    rows = np.flatnonzero(tag == -1)[:max_rows]
    where = defaultdict(list)
    for r in rows:
        w = train[r]
        for off in range(0, len(w) - PROBE_LEN + 1, stride):
            where[w[off:off + PROBE_LEN].tobytes()].append((int(r), int(off)))
    out = defaultdict(list)
    for key, hits in where.items():
        n = len(hits)
        for lo, hi in BINS:
            if lo <= n <= hi:
                seq = np.frombuffer(key, dtype=train.dtype).copy()
                out[(lo, hi)].append((seq, hits[0][0], hits[0][1], n))
                break
    return out


def rebuild(d: Path, device):
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    kind, _ = parse_objective(a.get("objective") or "ar")
    tok = get_tokenizer(a["tokenizer"], 288)
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    if a.get("data", "synthetic") != "synthetic":
        ds = build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], a["n_train"], a["n_val"], a["n_test"],
                                a["probes_per_tier"], tiers, a["n_nonmember"], a["data_seed"],
                                offset_mode=a["probe_offset"], canary_npz=a.get("canary_npz"))
    else:
        ds = build_dataset(a["n_train"], a["n_val"], a["n_test"], a["probes_per_tier"], tiers,
                           a["n_nonmember"], a["data_seed"], offset_mode=a["probe_offset"])
    kw = {k: v for k, v in (("d_model", a.get("d_model")), ("n_layers", a.get("n_layers")),
                            ("n_heads", a.get("n_heads")), ("d_ff", a.get("d_ff")),
                            ("emb_rank", a.get("emb_rank"))) if v}
    if a.get("pos_enc", "abs") != "abs":
        kw["pos_enc"] = a["pos_enc"]
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), **kw).to(device)
    model.load_state_dict(torch.load(d / "final.pt", map_location=device))
    model.eval()
    return model, tok, kind, ds, a


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--stride", type=int, default=12, help="block start spacing when hashing the corpus")
    ap.add_argument("--max_rows", type=int, default=5000, help="training windows to hash")
    ap.add_argument("--per_bin", type=int, default=25, help="blocks scored per occurrence bin")
    ap.add_argument("--pool", type=int, default=100)
    ap.add_argument("--name", default="natural")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    rng = np.random.default_rng(0)

    rows_md, census = [], {}
    for root in args.root:
        for d in sorted(Path(root).iterdir()):
            m = RUN.fullmatch(d.name) if d.is_dir() else None
            if not m or not (d / "final.pt").exists() or not (d / "args.json").exists():
                continue
            model, tok, kind, ds, a = rebuild(d, device)
            dups = find_duplicates(ds.train, ds.train_probe_id, args.stride, args.max_rows)
            key = (a.get("data", "synthetic"), args.stride)
            census[key] = {BINLAB[b]: len(dups.get(b, [])) for b in BINS}
            singles = [x[0] for x in dups.get((1, 1), [])]
            if len(singles) < args.pool + 1:
                print(f"  {d.name}: only {len(singles)} singletons, skipping")
                continue
            pool = np.stack(singles[:args.pool])
            for b in BINS:
                items = dups.get(b, [])
                if not items:
                    continue
                sel = [items[i] for i in rng.permutation(len(items))[:args.per_bin]]
                ex, bits, r1 = [], [], []
                for seq, row, off, n in sel:
                    host = ds.train[row].copy()
                    p = Probe(-1, n, seq, [])
                    sc = "ar" if kind == "ar" else "pll"
                    rk = rank_probe(model, tok, sc, p, host, pool, device, offset=off)
                    xt = extract_prefix(model, tok, kind, p, host, device, offset=off)
                    bits.append(rk["probe_bits_per_nt"])
                    r1.append(float(rk["rank"] == 1))
                    ex.append(float(xt["exact"]))
                rows_md.append((a.get("data", "synthetic"), a["tokenizer"], a.get("objective", "ar"),
                                a["seed"], BINLAB[b], len(sel), float(np.mean(bits)),
                                float(np.mean(r1)), float(np.mean(ex))))
                print(f"  {d.name:22s} dup={BINLAB[b]:11s} n={len(sel):3d} "
                      f"bits {np.mean(bits):.3f}  rank-1 {100 * np.mean(r1):5.1f}%  "
                      f"exact {100 * np.mean(ex):5.1f}%", flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows_md:
        print("nothing scored under", args.root)
        return 1
    md = [f"# Memorisation of natural duplicates — {args.name}", "",
          "No canary is planted here. Blocks of 96\\,nt that the training corpus repeats by itself are "
          "found by hashing every block at a fixed stride, scored in one of their own host windows with "
          "the paper's three rulers, and compared against single-occurrence blocks from the same corpus. "
          "Rows carrying a planted canary are excluded, so the two populations never mix.", "",
          "## Corpus census (distinct 96-nt blocks by occurrence count)", "",
          "| dataset | " + " | ".join(BINLAB[b] for b in BINS) + " |",
          "|---|" + "---|" * len(BINS)]
    for (data, _stride), c in census.items():
        md.append(f"| {data} | " + " | ".join(str(c.get(BINLAB[b], 0)) for b in BINS) + " |")
    md += ["", "## Scores", "",
           "| dataset | tokeniser | objective | seed | occurrences | n | bits/nt | rank-1 | verbatim |",
           "|---|---|---|---|---|---|---|---|---|"]
    for r in rows_md:
        md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]:.3f} | "
                  f"{100 * r[7]:.0f}% | {100 * r[8]:.0f}% |")
    out = Path(args.root[0]) / f"{args.name}_natural.md"
    out.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:10]))
    print(f"-> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
