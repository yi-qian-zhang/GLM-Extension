"""Tokenizers over the fixed {A,C,G,T} alphabet.

The dataset is always stored at nucleotide level (ids A=1..T=4, from pilot2.data).
A tokenizer is a *view*: it maps an (B, L_nt) nucleotide array to (B, L_tok)
token ids and back, losslessly. Because the alphabet is closed and complete,
every tokenizer sees exactly the same information -- only the granularity
changes. That is the whole point of the tokenizer axis.

Token id layout (every tokenizer): PAD=0, MASK=1, BOS=2, content ids 3..
"""
from __future__ import annotations

import numpy as np
import torch

PAD, MASK, BOS = 0, 1, 2
N_SPECIAL = 3


class KmerTokenizer:
    """Non-overlapping k-mers. k=1 is the character tokenizer."""

    def __init__(self, k: int, window_nt: int):
        assert window_nt % k == 0, (window_nt, k)
        self.k = k
        self.window_nt = window_nt
        self.n_tokens = window_nt // k          # tokens per window (no BOS)
        self.n_content = 4 ** k
        self.vocab_size = N_SPECIAL + self.n_content
        self.pad_id, self.mask_id, self.bos_id = PAD, MASK, BOS
        self.content_ids = torch.arange(N_SPECIAL, self.vocab_size)
        self._pow = (4 ** np.arange(k - 1, -1, -1)).astype(np.int64)  # big-endian digits
        self.name = "char" if k == 1 else f"{k}mer"

    # ---- nt <-> token -------------------------------------------------
    def encode(self, nt: np.ndarray) -> np.ndarray:
        """(B, L_nt) nt ids 1..4 -> (B, L_nt/k) token ids."""
        B, L = nt.shape
        assert L % self.k == 0
        digits = (nt - 1).reshape(B, L // self.k, self.k)
        return N_SPECIAL + (digits * self._pow).sum(-1)

    def decode(self, tok: np.ndarray) -> np.ndarray:
        """(B, L_tok) token ids (content only) -> (B, L_tok*k) nt ids 1..4."""
        B, T = tok.shape
        v = tok - N_SPECIAL
        out = np.empty((B, T, self.k), dtype=np.int64)
        for i, p in enumerate(self._pow):
            out[:, :, i] = (v // p) % 4
        return out.reshape(B, T * self.k) + 1

    def encode_t(self, nt: torch.Tensor) -> torch.Tensor:
        return torch.from_numpy(self.encode(nt.cpu().numpy())).to(nt.device)

    def decode_t(self, tok: torch.Tensor) -> torch.Tensor:
        return torch.from_numpy(self.decode(tok.cpu().numpy())).to(tok.device)

    # ---- geometry ------------------------------------------------------
    def nt_to_tok(self, nt_pos: int) -> int:
        assert nt_pos % self.k == 0, (nt_pos, self.k)
        return nt_pos // self.k

    def span(self, nt_start: int, nt_end: int) -> slice:
        return slice(self.nt_to_tok(nt_start), self.nt_to_tok(nt_end))

    def n_embedding_params(self, d_model: int, max_len: int) -> int:
        return self.vocab_size * d_model + max_len * d_model


def get_tokenizer(name: str, window_nt: int) -> KmerTokenizer:
    if name == "char":
        return KmerTokenizer(1, window_nt)
    if name.endswith("mer"):
        return KmerTokenizer(int(name[:-3]), window_nt)
    raise ValueError(f"unknown tokenizer {name!r} (expected char | 3mer | 6mer ...)")
