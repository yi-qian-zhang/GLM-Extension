"""Fixed backbone: 4-layer pre-LN transformer, d=512, 8 heads, tied embeddings.

Non-embedding parameters are identical across tokenizers; the embedding
table scales with vocab size and is reported as a covariate.
causal=True/False differs ONLY in the attention mask.

Capacity-matched controls (default off, so old checkpoints load unchanged):
  emb_rank=r  factorized tied embedding, vocab x r then r -> d (ALBERT-style);
              shrinks a large vocab's table while leaving the body untouched.
  d_ff=n      feed-forward width (default 4*d); shrinks the body instead.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class Backbone(nn.Module):
    def __init__(self, vocab_size: int, max_len: int, d_model: int = 512, n_layers: int = 4,
                 n_heads: int = 8, dropout: float = 0.0, causal: bool = True,
                 d_ff: int | None = None, emb_rank: int | None = None):
        super().__init__()
        self.causal = causal
        self.d_model = d_model
        self.emb_rank = emb_rank
        self.tok = nn.Embedding(vocab_size, emb_rank or d_model)
        self.emb_proj = nn.Linear(emb_rank, d_model, bias=False) if emb_rank else None
        self.pos = nn.Embedding(max_len, d_model)
        layer = nn.TransformerEncoderLayer(d_model, n_heads, d_ff or 4 * d_model, dropout,
                                           activation="gelu", batch_first=True, norm_first=True)
        self.blocks = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        self.ln_f = nn.LayerNorm(d_model)
        if not emb_rank:
            self.head = nn.Linear(d_model, vocab_size, bias=False)
            self.head.weight = self.tok.weight  # tied
        self.apply(self._init)
        self.register_buffer(
            "_causal_mask",
            torch.triu(torch.full((max_len, max_len), float("-inf")), diagonal=1),
            persistent=False,
        )

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, 0.0, 0.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.zeros_(m.bias)

    def forward(self, ids: torch.Tensor) -> torch.Tensor:
        B, L = ids.shape
        e = self.tok(ids)
        if self.emb_rank:
            e = self.emb_proj(e)
        x = e + self.pos(torch.arange(L, device=ids.device))[None]
        mask = self._causal_mask[:L, :L] if self.causal else None
        x = self.ln_f(self.blocks(x, mask=mask))
        if self.emb_rank:  # tied through the factorization: h -> r -> vocab
            return F.linear(x @ self.emb_proj.weight, self.tok.weight)
        return self.head(x)

    def n_params(self, non_embedding: bool = False) -> int:
        n = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n -= self.pos.weight.numel() + self.tok.weight.numel()
            if self.emb_rank:
                n -= self.emb_proj.weight.numel()
        return n
