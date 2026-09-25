"""Fixed backbone: 4-layer pre-LN transformer, d=512, 8 heads, tied embeddings.

causal=True  -> autoregressive: position i attends to <= i, predicts i+1.
causal=False -> bidirectional encoder used with a masked objective.
The ONLY architectural difference between the two is the attention mask.
"""
from __future__ import annotations

import torch
import torch.nn as nn

from .data import VOCAB_SIZE, WINDOW


class Backbone(nn.Module):
    def __init__(self, vocab_size: int = VOCAB_SIZE, d_model: int = 512, n_layers: int = 4,
                 n_heads: int = 8, max_len: int = WINDOW + 1, dropout: float = 0.0,
                 causal: bool = True):
        super().__init__()
        self.causal = causal
        self.d_model = d_model
        self.tok = nn.Embedding(vocab_size, d_model)
        self.pos = nn.Embedding(max_len, d_model)
        layer = nn.TransformerEncoderLayer(d_model, n_heads, 4 * d_model, dropout,
                                           activation="gelu", batch_first=True, norm_first=True)
        self.blocks = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)
        self.head.weight = self.tok.weight  # tied input/output embeddings
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
        x = self.tok(ids) + self.pos(torch.arange(L, device=ids.device))[None]
        mask = self._causal_mask[:L, :L] if self.causal else None
        x = self.blocks(x, mask=mask)
        return self.head(self.ln_f(x))  # (B, L, V) logits

    def n_params(self, non_embedding: bool = False) -> int:
        n = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n -= self.pos.weight.numel() + self.tok.weight.numel()
        return n
