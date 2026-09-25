"""Train a BPE vocabulary over {A,C,G,T} on real genome windows and measure its
mean token length k on several corpora.

    python -m pilot2.train_bpe --fasta data/genomes/ecoli_K12_MG1655.fna --vocab 4096

Writes data/tokenizers/bpe<vocab>_<name>.json (HF `tokenizers` format) plus a
small stats json. The mean token length is the conversion constant between
per-token and per-nucleotide perplexity (PPL_nt = PPL_tok^(1/k)); it is
corpus-dependent, which is why it must be measured, never assumed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from tokenizers import Tokenizer, models, trainers

from .data import WINDOW, random_dna
from .real_data import read_fasta, windows_from_genome

_DEC = {1: "A", 2: "C", 3: "G", 4: "T"}


def ids_to_str(rows: np.ndarray):
    return ["".join(_DEC[int(i)] for i in r) for r in rows]


def mean_token_len(tok: Tokenizer, seqs) -> dict:
    lens = np.array([len(tok.encode(s).ids) for s in seqs])
    nt = np.array([len(s) for s in seqs])
    k = nt.sum() / lens.sum()  # aggregate first, normalize last
    return {"n_seqs": int(len(seqs)), "tokens_per_window_mean": float(lens.mean()),
            "tokens_per_window_std": float(lens.std()), "k_nt_per_token": float(k),
            "ppl_floor_per_token_if_uniform": float(4.0 ** k)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fasta", default="data/genomes/ecoli_K12_MG1655.fna")
    ap.add_argument("--name", default="ecoli")
    ap.add_argument("--vocab", type=int, default=4096)
    ap.add_argument("--out", default="data/tokenizers")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    genome = read_fasta(args.fasta)
    real = windows_from_genome(genome)                 # (N, 288) ids
    real_str = ids_to_str(real)
    tok = Tokenizer(models.BPE(unk_token=None))
    # no pre-tokenizer: each window is one "word", merges run over the whole string
    trainer = trainers.BpeTrainer(vocab_size=args.vocab, initial_alphabet=list("ACGT"),
                                  special_tokens=["[PAD]", "[MASK]", "[BOS]"], limit_alphabet=4,
                                  show_progress=False)
    tok.train_from_iterator(real_str, trainer=trainer)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    tpath = out / f"bpe{args.vocab}_{args.name}.json"
    tok.save(str(tpath))

    rng = np.random.default_rng(args.seed)
    rand_str = ids_to_str(random_dna(rng, 2000, WINDOW))
    stats = {
        "vocab_size": tok.get_vocab_size(), "trained_on": args.fasta, "n_train_windows": int(len(real_str)),
        "k_on_training_corpus": mean_token_len(tok, real_str[:5000]),
        "k_on_uniform_random_dna": mean_token_len(tok, rand_str),
        "roundtrip_ok": all(tok.decode(tok.encode(s).ids).replace(" ", "") == s for s in real_str[:200] + rand_str[:200]),
        "longest_token_nt": max(len(t) for t in tok.get_vocab()),
    }
    (out / f"bpe{args.vocab}_{args.name}.stats.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
    print(json.dumps(stats, indent=1))
    print(f"-> {tpath}")


if __name__ == "__main__":
    main()
