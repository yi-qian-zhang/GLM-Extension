"""Load-test the DNABERT 3/4/5/6-mer checkpoints (E4 arm c) and sanity-check the weights.

    python -m pilot2.check_dnabert --root /data/wh/yqdata/models/DNABERT --gpu 0

DNABERT tokenizes with OVERLAPPING k-mers (stride 1): token t covers nt t..t+k-1,
so nucleotide j appears in tokens j-k+1..j. Masking a single token leaks it from
its neighbours; to hide nt j we mask that contiguous span of k tokens (as in
DNABERT pretraining) and read p(nt_j) as the marginal of the first letter of the
k-mer predicted at token j.

Sanity check: on real E. coli DNA the span-masked accuracy should beat chance
(0.25); on iid uniform DNA it must sit at chance and the per-nt loss near 2 bits.
If the weights failed to load, both would sit at chance.
"""
from __future__ import annotations

import argparse
import itertools
import math
from pathlib import Path

import numpy as np
import torch
from transformers import AutoModelForMaskedLM

NT = "ACGT"


def load_vocab(d: Path):
    toks = [l.rstrip("\n") for l in open(d / "vocab.txt", encoding="utf-8")]
    return {t: i for i, t in enumerate(toks)}


def kmer_ids(seq: str, k: int, vocab):
    return [vocab[seq[i:i + k]] for i in range(len(seq) - k + 1)]


@torch.no_grad()
def span_masked_nt(model, seq: str, k: int, vocab, device, positions):
    """Return (accuracy, mean bits) of predicting nt j with its k covering tokens masked."""
    ids = [vocab["[CLS]"]] + kmer_ids(seq, k, vocab) + [vocab["[SEP]"]]
    mask_id = vocab["[MASK]"]
    kmers = ["".join(p) for p in itertools.product(NT, repeat=k)]
    kid = torch.tensor([vocab[m] for m in kmers], device=device)
    first = torch.tensor([NT.index(m[0]) for m in kmers], device=device)
    rows = []
    for j in positions:
        x = list(ids)
        for t in range(j - k + 1, j + 1):   # tokens covering nt j (offset +1 for [CLS])
            x[t + 1] = mask_id
        rows.append(x)
    x = torch.tensor(rows, device=device)
    logits = model(input_ids=x).logits.float()                    # (P, L, V)
    at = logits[torch.arange(len(positions)), torch.tensor(positions, device=device) + 1]
    p = torch.softmax(at[:, kid], -1)                             # restrict to content k-mers
    pnt = torch.zeros(len(positions), 4, device=device).index_add_(1, first, p)
    truth = torch.tensor([NT.index(seq[j]) for j in positions], device=device)
    acc = (pnt.argmax(-1) == truth).float().mean().item()
    bits = (-torch.log2(pnt[torch.arange(len(positions)), truth].clamp_min(1e-12))).mean().item()
    return acc, bits


def read_fasta(path: Path) -> str:
    return "".join(l.strip() for l in open(path) if not l.startswith(">")).upper()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/data/wh/yqdata/models/DNABERT")
    ap.add_argument("--genome", default="data/genomes/ecoli_K12_MG1655.fna")
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--n_windows", type=int, default=8)
    args = ap.parse_args(argv)
    device = f"cuda:{args.gpu}"
    rng = np.random.default_rng(0)
    genome = read_fasta(Path(args.genome))
    L = 300
    starts = rng.integers(0, len(genome) - L, args.n_windows)
    real = [genome[s:s + L] for s in starts]
    real = [s for s in real if set(s) <= set(NT)]
    rand = ["".join(rng.choice(list(NT), L)) for _ in range(args.n_windows)]
    print(f"{'model':12s} {'params':>8s} {'vocab':>6s} | {'E.coli acc':>10s} {'bits':>6s} | {'uniform acc':>11s} {'bits':>6s}")
    for k in (3, 4, 5, 6):
        d = Path(args.root) / f"DNA_bert_{k}"
        model = AutoModelForMaskedLM.from_pretrained(d, trust_remote_code=True).to(device).eval()
        vocab = load_vocab(d)
        n = sum(p.numel() for p in model.parameters())
        pos = list(range(k + 5, L - k - 5, 7))
        res = {}
        for name, seqs in (("real", real), ("rand", rand)):
            a = [span_masked_nt(model, s, k, vocab, device, pos) for s in seqs]
            res[name] = (np.mean([x[0] for x in a]), np.mean([x[1] for x in a]))
        print(f"DNA_bert_{k:<3d} {n/1e6:7.1f}M {len(vocab):6d} | {res['real'][0]:10.3f} {res['real'][1]:6.3f} | "
              f"{res['rand'][0]:11.3f} {res['rand'][1]:6.3f}", flush=True)
        del model
        torch.cuda.empty_cache()
    print("chance: acc 0.250, 2.000 bits/nt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
