"""Real-genome windows for the E. coli arm of E1, with probes embedded exactly
as in the synthetic arm.

    ds = build_real_dataset("data/genomes/ecoli_K12_MG1655.fna", n_train=15000, ...)

Differences from the synthetic builder that matter for interpretation:
  * Windows are non-overlapping (stride = WINDOW), so no train/val/test window
    shares nucleotides with another. Splits are by random window, seeded.
  * Windows containing any non-ACGT symbol are dropped.
  * The 2.000 bits/nt floor does NOT apply to real sequence (there is structure
    to learn). We report the corpus' 0-order entropy as a reference value only;
    the floor assertion in the scorer is expected to still pass (real DNA is
    harder than 1.9998 bits/nt at order 0 for a small model), but it is not the
    calibration argument -- the synthetic arm is.
  * Probes stay iid uniform random 96-mers, so a probe never resembles real
    sequence and any preferential treatment is memorization, not biology.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Dataset, Probe, random_dna

_ENC = {"A": 1, "C": 2, "G": 3, "T": 4}


def read_fasta(path: str | Path) -> str:
    seq = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith(">"):
                continue
            seq.append(line.strip().upper())
    return "".join(seq)


def windows_from_genome(genome: str, window: int = WINDOW, stride: int | None = None) -> np.ndarray:
    """Non-overlapping (default) windows as (N, window) nt ids; drops windows with non-ACGT."""
    stride = stride or window
    out = []
    for i in range(0, len(genome) - window + 1, stride):
        w = genome[i:i + window]
        if all(c in _ENC for c in w):
            out.append([_ENC[c] for c in w])
    return np.array(out, dtype=np.int64)


def zero_order_entropy_bits(x: np.ndarray) -> float:
    counts = np.bincount(x.ravel(), minlength=5)[1:5].astype(float)
    p = counts / counts.sum()
    return float(-(p * np.log2(p)).sum())


def build_real_dataset(fasta: str | Path, n_train: int = 15000, n_val: int = 500, n_test: int = 500,
                       probes_per_tier: int = 30, tiers=(1, 4, 8, 16), n_nonmember: int = 40,
                       data_seed: int = 1234) -> Dataset:
    rng = np.random.default_rng(data_seed)
    all_w = windows_from_genome(read_fasta(fasta))
    assert len(all_w) >= n_train + n_val + n_test, (len(all_w), n_train, n_val, n_test)
    perm = rng.permutation(len(all_w))
    train = all_w[perm[:n_train]]
    val = all_w[perm[n_train:n_train + n_val]]
    test = all_w[perm[n_train + n_val:n_train + n_val + n_test]]

    # probes: iid uniform 96-mers; each repetition gets its own REAL host window
    # drawn from the unused remainder of the genome, so hosts are in-distribution
    remainder = all_w[perm[n_train + n_val + n_test:]]
    ridx = 0
    probes, extra_rows, extra_pid, pid = [], [], [], 0
    for r in tiers:
        for _ in range(probes_per_tier):
            seq = random_dna(rng, 1, PROBE_LEN)[0]
            for _ in range(r):
                host = remainder[ridx % len(remainder)].copy(); ridx += 1
                host[PROBE_OFFSET:PROBE_OFFSET + PROBE_LEN] = seq
                extra_rows.append(host); extra_pid.append(pid)
            probes.append(Probe(pid, r, seq, [])); pid += 1
    for _ in range(n_nonmember):
        probes.append(Probe(pid, 0, random_dna(rng, 1, PROBE_LEN)[0], [])); pid += 1

    all_train = np.concatenate([train, np.stack(extra_rows)], axis=0)
    tag = np.concatenate([np.full(n_train, -1, dtype=np.int64), np.array(extra_pid, dtype=np.int64)])
    perm2 = rng.permutation(all_train.shape[0])
    all_train, tag = all_train[perm2], tag[perm2]
    for p in probes:
        p.host_rows = np.nonzero(tag == p.probe_id)[0].tolist()
        assert len(p.host_rows) == p.repetitions
        for row in p.host_rows:
            assert np.array_equal(all_train[row, PROBE_OFFSET:PROBE_OFFSET + PROBE_LEN], p.seq)
    ds = Dataset(all_train, val, test, probes, tag, data_seed)
    ds.source = str(fasta)
    ds.h0_bits_train = zero_order_entropy_bits(train)
    ds.h0_bits_test = zero_order_entropy_bits(test)
    return ds


if __name__ == "__main__":
    import sys
    ds = build_real_dataset(sys.argv[1] if len(sys.argv) > 1 else "data/genomes/ecoli_K12_MG1655.fna")
    print(f"train {ds.train.shape} val {ds.val.shape} test {ds.test.shape} probes {len(ds.probes)}")
    print(f"0-order entropy: train {ds.h0_bits_train:.4f}  test {ds.h0_bits_test:.4f} bits/nt "
          f"(uniform = 2.0000; order-0 floor on this corpus = {2**ds.h0_bits_test:.4f} ppl/nt)")
