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

import os

import math
from pathlib import Path

import numpy as np

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Dataset, Probe, random_dna

_ENC = {"A": 1, "C": 2, "G": 3, "T": 4}


# Alex's real datasets (config/*.yaml, src/data/real_data_loader.py): E. coli K-12 MG1655 (GCF_000005845.2),
# yeast S288C R64 (GCF_000146045.2), and the GUE human promoter set prom_300_all (leannmlindsey/GUE, 300-nt rows).
# Downloaded corpora may live outside the synced repo (set GLMEXT_DATA=/data/wh/yqdata/glm_data);
# "data" is the in-repo default.
DATA_ROOT = os.environ.get("GLMEXT_DATA", "data")
DATA_PATHS = {
    "ecoli": "data/genomes/ecoli_K12_MG1655.fna",
    "yeast": "data/genomes/yeast_S288C_R64.fna",
    "gue": f"{DATA_ROOT}/gue/prom_300_all_train.csv",
    "human": f"{DATA_ROOT}/human/chr22.fa",
}
REAL_DATA = tuple(DATA_PATHS)


def read_sequences_csv(path: str | Path, window: int = WINDOW) -> np.ndarray:
    """One sequence per row (column 'sequence'); centre-crop to `window`, drop short / non-ACGT rows."""
    import csv
    out = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            s = row["sequence"].strip().upper()
            if len(s) < window:
                continue
            a = (len(s) - window) // 2
            s = s[a:a + window]
            if all(c in _ENC for c in s):
                out.append([_ENC[c] for c in s])
    return np.array(out, dtype=np.int64)


def load_windows(path: str | Path) -> np.ndarray:
    """Genome FASTA -> non-overlapping windows; CSV of fixed-length sequences -> one window per row."""
    if str(path).endswith(".csv"):
        return read_sequences_csv(path)
    return windows_from_genome(read_fasta(path))


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
                       data_seed: int = 1234, offset_mode: str = "fixed", canary_npz=None) -> Dataset:
    """offset_mode as in pilot2.data.build_dataset: 'fixed' = every copy at PROBE_OFFSET, 'random' = per-copy offset."""
    assert offset_mode in ("fixed", "random"), offset_mode
    rng = np.random.default_rng(data_seed)
    if canary_npz:            # real human haplotype segments instead of iid uniform 96-mers
        from .human_canary import load_canaries
        pool_seqs, _ = load_canaries(canary_npz)
        need = probes_per_tier * len(tiers) + n_nonmember
        assert len(pool_seqs) >= need, (len(pool_seqs), need)
        perm = rng.permutation(len(pool_seqs))
        probe_seqs, rank_pool = pool_seqs[perm[:need]], pool_seqs[perm[need:]]
        pool_i = iter(range(need))
        next_probe_seq = lambda: probe_seqs[next(pool_i)].copy()
    else:
        next_probe_seq = lambda: random_dna(rng, 1, PROBE_LEN)[0]
    off_rng = np.random.default_rng(data_seed + 7_777)
    all_w = load_windows(fasta)
    assert len(all_w) >= n_train + n_val + n_test, (len(all_w), n_train, n_val, n_test)
    perm = rng.permutation(len(all_w))
    train = all_w[perm[:n_train]]
    val = all_w[perm[n_train:n_train + n_val]]
    test = all_w[perm[n_train + n_val:n_train + n_val + n_test]]

    # probes: iid uniform 96-mers; each repetition gets its own REAL host window
    # drawn from the unused remainder of the genome, so hosts are in-distribution
    remainder = all_w[perm[n_train + n_val + n_test:]]
    ridx = 0
    probes, extra_rows, extra_pid, extra_off, pid = [], [], [], [], 0
    for r in tiers:
        for _ in range(probes_per_tier):
            seq = next_probe_seq()
            for _ in range(r):
                host = remainder[ridx % len(remainder)].copy(); ridx += 1
                off = PROBE_OFFSET if offset_mode == "fixed" else int(off_rng.integers(0, WINDOW - PROBE_LEN + 1))
                host[off:off + PROBE_LEN] = seq
                extra_rows.append(host); extra_pid.append(pid); extra_off.append(off)
            probes.append(Probe(pid, r, seq, [])); pid += 1
    for _ in range(n_nonmember):
        probes.append(Probe(pid, 0, next_probe_seq(), [])); pid += 1

    all_train = np.concatenate([train, np.stack(extra_rows)], axis=0)
    tag = np.concatenate([np.full(n_train, -1, dtype=np.int64), np.array(extra_pid, dtype=np.int64)])
    offs = np.concatenate([np.full(n_train, -1, dtype=np.int64), np.array(extra_off, dtype=np.int64)])
    perm2 = rng.permutation(all_train.shape[0])
    all_train, tag, offs = all_train[perm2], tag[perm2], offs[perm2]
    for p in probes:
        p.host_rows = np.nonzero(tag == p.probe_id)[0].tolist()
        p.offsets = [int(offs[row]) for row in p.host_rows]
        assert len(p.host_rows) == p.repetitions
        for row, off in zip(p.host_rows, p.offsets):
            assert np.array_equal(all_train[row, off:off + PROBE_LEN], p.seq)
    ds = Dataset(all_train, val, test, probes, tag, data_seed)
    ds.source = str(fasta)
    ds.canary_source = str(canary_npz) if canary_npz else "iid_uniform"
    if canary_npz:
        # the ranking pool has to be as real and as rare as the canary, otherwise any real sequence
        # outranks uniform random DNA and a non-member scores rank 1 regardless of membership
        ds.pool_seqs = rank_pool
        # and the "fresh host" has to be a real window too: a canary read inside random DNA is a
        # different measurement from the same canary read inside a chromosome, so comparing a member
        # in its real host with a non-member in a random host confounds membership with host type
        unused = all_w[perm[n_train + n_val + n_test:]]
        ds.fresh_hosts = unused[rng.permutation(len(unused))[:max(400, len(probes))]]
    ds.h0_bits_train = zero_order_entropy_bits(train)
    ds.h0_bits_test = zero_order_entropy_bits(test)
    return ds


if __name__ == "__main__":
    import sys
    ds = build_real_dataset(sys.argv[1] if len(sys.argv) > 1 else "data/genomes/ecoli_K12_MG1655.fna")
    print(f"train {ds.train.shape} val {ds.val.shape} test {ds.test.shape} probes {len(ds.probes)}")
    print(f"0-order entropy: train {ds.h0_bits_train:.4f}  test {ds.h0_bits_test:.4f} bits/nt "
          f"(uniform = 2.0000; order-0 floor on this corpus = {2**ds.h0_bits_test:.4f} ppl/nt)")
