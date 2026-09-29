"""Synthetic uniform DNA with probes (canaries) embedded inside host windows.

Design decisions (see claude_notes/04_experiment_plan.md, section 0):
  * window length 288 nt, probe length 96 nt, probe placed at offset 96
  * probes are EMBEDDED in host windows and TAGGED AT CONSTRUCTION, so every
    training sequence has identical length and membership can never separate
    on length
  * all windows are fixed length -> no padding anywhere in the pilot
  * data seed is fixed and independent of the model seed, so every run in a
    comparison sees byte-identical data
"""
from __future__ import annotations

import dataclasses
import json
from pathlib import Path

import numpy as np
import torch

# char vocabulary. PAD is reserved but never used (fixed-length windows).
PAD, A, C, G, T, MASK, BOS = 0, 1, 2, 3, 4, 5, 6
VOCAB_SIZE = 7
NUC_IDS = torch.tensor([A, C, G, T])
WINDOW = 288
PROBE_LEN = 96
PROBE_OFFSET = 96
ENTROPY_BITS_PER_NT = 2.0  # log2(4): uniform iid over {A,C,G,T}

_ENC = {"A": A, "C": C, "G": G, "T": T}
_DEC = {A: "A", C: "C", G: "G", T: "T", MASK: "?", BOS: "^", PAD: "_"}


def encode(seq: str) -> np.ndarray:
    return np.fromiter((_ENC[ch] for ch in seq), dtype=np.int64, count=len(seq))


def decode(ids) -> str:
    return "".join(_DEC[int(i)] for i in ids)


def random_dna(rng: np.random.Generator, n: int, length: int) -> np.ndarray:
    """n x length array of nucleotide ids, iid uniform (GC = 0.5 exactly)."""
    return rng.integers(A, T + 1, size=(n, length), dtype=np.int64)


@dataclasses.dataclass
class Probe:
    probe_id: int
    repetitions: int          # 0 = non-member control (never inserted)
    seq: np.ndarray           # PROBE_LEN ids
    host_rows: list           # indices into train set carrying this probe
    offsets: list = dataclasses.field(default_factory=list)  # nt offset of the probe in each host row


@dataclasses.dataclass
class Dataset:
    train: np.ndarray           # (N_train, WINDOW) ids, probes already embedded
    val: np.ndarray             # (N_val, WINDOW) held-out, no probes
    test: np.ndarray            # (N_test, WINDOW) held-out, no probes
    probes: list
    train_probe_id: np.ndarray  # (N_train,) probe_id or -1, tagged at construction
    data_seed: int

    def members(self):
        return [p for p in self.probes if p.repetitions > 0]

    def nonmembers(self):
        return [p for p in self.probes if p.repetitions == 0]

    def save_meta(self, path: Path):
        meta = {
            "data_seed": self.data_seed,
            "n_train": int(self.train.shape[0]),
            "n_val": int(self.val.shape[0]),
            "n_test": int(self.test.shape[0]),
            "window": WINDOW,
            "probe_len": PROBE_LEN,
            "probe_offset": PROBE_OFFSET,
            "probes": [
                {"probe_id": p.probe_id, "repetitions": p.repetitions,
                 "seq": decode(p.seq), "host_rows": p.host_rows, "offsets": p.offsets}
                for p in self.probes
            ],
        }
        path.write_text(json.dumps(meta, indent=1), encoding="utf-8")


def build_dataset(
    n_train: int = 5000,
    n_val: int = 500,
    n_test: int = 500,
    probes_per_tier: int = 20,
    tiers=(1, 16),
    n_nonmember: int = 40,
    data_seed: int = 1234,
    offset_mode: str = "fixed",
) -> Dataset:
    """offset_mode: "fixed" puts every probe copy at PROBE_OFFSET (token-aligned for k | 96);
    "random" draws each copy's offset uniformly from 0..WINDOW-PROBE_LEN, so copies of the
    same probe are tokenized with different k-mer phases (real duplicates occur anywhere).
    Offsets come from a separate stream, so hosts and probes are identical in both modes."""
    assert offset_mode in ("fixed", "random"), offset_mode
    rng = np.random.default_rng(data_seed)
    off_rng = np.random.default_rng(data_seed + 7_777)
    train = random_dna(rng, n_train, WINDOW)
    val = random_dna(rng, n_val, WINDOW)
    test = random_dna(rng, n_test, WINDOW)

    probes = []
    pid = 0
    extra_rows = []  # host windows that carry probes
    extra_pid = []
    extra_off = []
    for r in tiers:
        for _ in range(probes_per_tier):
            seq = random_dna(rng, 1, PROBE_LEN)[0]
            for _ in range(r):
                host = random_dna(rng, 1, WINDOW)[0]
                off = PROBE_OFFSET if offset_mode == "fixed" else int(off_rng.integers(0, WINDOW - PROBE_LEN + 1))
                host[off:off + PROBE_LEN] = seq
                extra_rows.append(host)
                extra_pid.append(pid)
                extra_off.append(off)
            probes.append(Probe(pid, r, seq, []))
            pid += 1
    for _ in range(n_nonmember):
        probes.append(Probe(pid, 0, random_dna(rng, 1, PROBE_LEN)[0], []))
        pid += 1

    # Append probe-carrying windows, shuffle the whole train set, and carry
    # the tag through the SAME permutation. This is the construction-time
    # tagging that replaces position bookkeeping.
    all_train = np.concatenate([train, np.stack(extra_rows)], axis=0)
    tag = np.concatenate([np.full(n_train, -1, dtype=np.int64),
                          np.array(extra_pid, dtype=np.int64)])
    offs = np.concatenate([np.full(n_train, -1, dtype=np.int64), np.array(extra_off, dtype=np.int64)])
    perm = rng.permutation(all_train.shape[0])
    all_train, tag, offs = all_train[perm], tag[perm], offs[perm]
    for p in probes:
        p.host_rows = np.nonzero(tag == p.probe_id)[0].tolist()
        p.offsets = [int(offs[row]) for row in p.host_rows]
        assert len(p.host_rows) == p.repetitions, (p.probe_id, len(p.host_rows), p.repetitions)
        for row, off in zip(p.host_rows, p.offsets):  # golden test: flag precision and recall are exactly 1.0
            assert np.array_equal(all_train[row, off:off + PROBE_LEN], p.seq)
    return Dataset(all_train, val, test, probes, tag, data_seed)


def with_bos(x: torch.Tensor) -> torch.Tensor:
    """Prepend BOS so the AR model can predict position 0. (B, L) -> (B, L+1)."""
    bos = torch.full((x.shape[0], 1), BOS, dtype=x.dtype, device=x.device)
    return torch.cat([bos, x], dim=1)
