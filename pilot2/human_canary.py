"""Real human canaries: haplotype segments carrying an individual's rare alleles (1000 Genomes chr22).

Preparation (once, CPU, ~5 min):
    python -m pilot2.human_canary --vcf data/human/ALL.chr22.GRCh38.phased.vcf.gz \
        --fasta data/human/chr22.fa --out data/human/canaries_chr22.npz

Why. Every result so far plants canaries that are uniform random 96-mers: a clean lower bound
("if the model cannot even be made to memorise an unlearnable string, nothing is memorised"), but
a reviewer is entitled to ask what it has to do with a real person's genome. A real segment is
in-distribution, so the model can partly predict it from biology, which makes memorisation harder
to see and the test strictly more conservative. What makes it privacy-relevant is the rare allele:
a variant carried by a handful of the 2,548 individuals is, in context, close to an identifier,
and the question becomes whether a model fine-tuned on one person's haplotype reproduces THAT
allele rather than the reference base.

Construction. From the phased VCF, keep biallelic SNVs with population frequency <= --max_af
(default 0.001, i.e. at most ~5 chromosomes in 1000G) that pass the filter and have at least one
carrier. For each kept variant, take the 96-nt reference window centred on it, require pure ACGT,
and substitute the carrier's alternate allele(s) at every rare variant inside the window. The
result is a real human sequence that differs from the reference at 1 or more positions and is
carried by at most a few individuals. Each canary records its variant positions (index inside the
96-nt segment), REF and ALT bases, allele frequency, and the number of carriers, so that after
extraction one can score not only "did the whole segment come back" but "did the individual's
rare allele come back", with the reference base as the natural null.

Both the member canaries and the non-member controls come from this same pool, so the control is
matched: equally real, equally rare, differing only in having been in the training data.

Use (the dataset builders take `canary_npz`):
    python -m pilot2.dnabert --k 6 --data human --canary_npz data/human/canaries_chr22.npz ...
"""
from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path

import numpy as np

from .data import PROBE_LEN, encode

ACGT = set("ACGT")


def read_chrom_fasta(path: str | Path) -> str:
    """Single-record FASTA -> uppercase sequence string (hg38 chromosome files are soft-masked)."""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(">"):
                continue
            out.append(line.strip())
    return "".join(out).upper()


def scan_variants(vcf: str | Path, max_af: float, max_carriers: int, limit: int | None = None):
    """Rare biallelic SNVs: [{pos(1-based), ref, alt, af, n_carriers, carrier}]. Genotypes are parsed
    only for variants that already pass the frequency filter, which keeps the scan cheap."""
    kept, samples = [], None
    with gzip.open(vcf, "rt") as f:
        for line in f:
            if line.startswith("##"):
                continue
            if line.startswith("#CHROM"):
                samples = line.rstrip("\n").split("\t")[9:]
                continue
            p = line.split("\t", 9)
            ref, alt, flt, info = p[3], p[4], p[6], p[7]
            if len(ref) != 1 or len(alt) != 1 or ref not in ACGT or alt not in ACGT:
                continue
            if flt not in ("PASS", "."):
                continue
            af = None
            for kv in info.split(";"):
                if kv.startswith("AF="):
                    af = float(kv[3:].split(",")[0])
                    break
            if af is None or af <= 0 or af > max_af:
                continue
            gts = p[9].rstrip("\n").split("\t")
            carriers = [i for i, g in enumerate(gts) if "1" in g[:3]]
            if not carriers or len(carriers) > max_carriers:
                continue
            kept.append({"pos": int(p[1]), "ref": ref, "alt": alt, "af": af,
                         "n_carriers": len(carriers), "carrier": samples[carriers[0]]})
            if limit and len(kept) >= limit:
                break
    return kept


def build_canaries(variants, genome: str, n: int, seed: int = 0, min_gap: int = 1000):
    """One canary per anchor variant: the 96-nt window centred on it with every rare ALT in the
    window substituted (the carrier's haplotype). Anchors are at least `min_gap` apart so canaries
    never overlap, and the variant list is shared so a window picks up its neighbours' rare alleles."""
    rng = np.random.default_rng(seed)
    by_pos = {v["pos"]: v for v in variants}
    anchors, last = [], -10 ** 9
    for v in sorted(variants, key=lambda x: x["pos"]):
        if v["pos"] - last < min_gap:
            continue
        s = v["pos"] - 1 - PROBE_LEN // 2
        if s < 0 or s + PROBE_LEN > len(genome):
            continue
        seg = genome[s:s + PROBE_LEN]
        if not set(seg) <= ACGT:
            continue
        anchors.append((s, v))
        last = v["pos"]
    rng.shuffle(anchors)
    out = []
    for s, v in anchors[:n]:
        seg = list(genome[s:s + PROBE_LEN])
        vs = []
        for off in range(PROBE_LEN):
            w = by_pos.get(s + off + 1)
            if w and seg[off] == w["ref"]:
                seg[off] = w["alt"]
                vs.append({"index": off, "ref": w["ref"], "alt": w["alt"], "af": w["af"],
                           "n_carriers": w["n_carriers"], "pos": w["pos"]})
        if not vs:
            continue
        out.append({"start0": s, "anchor_pos": v["pos"], "carrier": v["carrier"],
                    "seq": "".join(seg), "variants": vs})
    return out


def load_canaries(npz: str | Path):
    """-> (seqs (N, 96) nt ids, meta list)."""
    z = np.load(npz, allow_pickle=True)
    return z["seqs"], json.loads(str(z["meta"]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--vcf", default="data/human/ALL.chr22.GRCh38.phased.vcf.gz")
    ap.add_argument("--fasta", default="data/human/chr22.fa")
    ap.add_argument("--out", default="data/human/canaries_chr22.npz")
    ap.add_argument("--max_af", type=float, default=0.001)
    ap.add_argument("--max_carriers", type=int, default=5)
    ap.add_argument("--n", type=int, default=400)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--scan_limit", type=int, default=None)
    args = ap.parse_args(argv)

    genome = read_chrom_fasta(args.fasta)
    print(f"[human] chr22 {len(genome):,} nt, {genome.count('N'):,} N", flush=True)
    variants = scan_variants(args.vcf, args.max_af, args.max_carriers, args.scan_limit)
    print(f"[human] {len(variants):,} rare biallelic SNVs (AF <= {args.max_af}, <= {args.max_carriers} carriers)", flush=True)
    cans = build_canaries(variants, genome, args.n, args.seed)
    seqs = np.stack([encode(c["seq"]) for c in cans])
    nv = np.array([len(c["variants"]) for c in cans])
    af = np.array([v["af"] for c in cans for v in c["variants"]])
    meta = {"source": {"vcf": str(args.vcf), "fasta": str(args.fasta), "chrom": "chr22",
                       "assembly": "GRCh38", "cohort": "1000 Genomes phase 3 (2,548 samples)"},
            "max_af": args.max_af, "max_carriers": args.max_carriers, "probe_len": PROBE_LEN,
            "n_canaries": len(cans), "canaries": cans}
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out, seqs=seqs, meta=json.dumps(meta))
    print(json.dumps({"n_canaries": len(cans), "variants_per_canary_mean": float(nv.mean()),
                      "variants_per_canary_max": int(nv.max()), "af_mean": float(af.mean()),
                      "af_max": float(af.max()), "distinct_carriers": len({c["carrier"] for c in cans}),
                      "gc": float(np.mean([(s == 2) | (s == 3) for s in seqs]))}, indent=1))
    print(f"-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
