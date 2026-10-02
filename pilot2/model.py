"""Fixed backbone: 4-layer pre-LN transformer, d=512, 8 heads, tied embeddings.

Non-embedding parameters are identical across tokenizers; the embedding
table scales with vocab size and is reported as a covariate.
causal=True/False differs ONLY in the attention mask.

Capacity-matched controls (default off, so old checkpoints load unchanged):
  emb_rank=r  factorized tied embedding, vocab x r then r -> d (ALBERT-style);
              shrinks a large vocab's table while leaving the body untouched.
  d_ff=n      feed-forward width (default 4*d); shrinks the body instead.

Position encoding (default "abs", so old checkpoints load unchanged):
  pos_enc="abs"   learned absolute position embedding added to the input.
  pos_enc="rope"  rotary embedding applied to queries and keys in every layer;
                  attention then depends only on relative offsets, and there is
                  no position table. Same pre-LN block shape and parameter count
                  as the default body.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


def _rope_cache(max_len: int, head_dim: int):
    inv = 1.0 / (10000 ** (torch.arange(0, head_dim, 2).float() / head_dim))
    ang = torch.arange(max_len).float()[:, None] * inv[None, :]        # (L, head_dim/2)
    return ang.cos(), ang.sin()


def _rotate(x, cos, sin):
    """x: (B, H, L, D). Rotate consecutive feature pairs by the position angle."""
    x1, x2 = x[..., 0::2], x[..., 1::2]
    return torch.stack((x1 * cos - x2 * sin, x1 * sin + x2 * cos), dim=-1).flatten(-2)


class RopeBlock(nn.Module):
    """Pre-LN block with the same shape as nn.TransformerEncoderLayer(norm_first=True, gelu)."""

    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float):
        super().__init__()
        self.n_heads = n_heads
        self.ln1 = nn.LayerNorm(d_model)
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
        self.ln2 = nn.LayerNorm(d_model)
        self.ff1 = nn.Linear(d_model, d_ff)
        self.ff2 = nn.Linear(d_ff, d_model)
        self.drop = nn.Dropout(dropout)

    def forward(self, x, cos, sin, causal: bool):
        B, L, D = x.shape
        q, k, v = self.qkv(self.ln1(x)).view(B, L, 3, self.n_heads, D // self.n_heads).permute(2, 0, 3, 1, 4)
        q, k = _rotate(q, cos, sin), _rotate(k, cos, sin)
        a = F.scaled_dot_product_attention(q, k, v, is_causal=causal)
        x = x + self.drop(self.proj(a.transpose(1, 2).reshape(B, L, D)))
        return x + self.drop(self.ff2(self.drop(F.gelu(self.ff1(self.ln2(x))))))


class Backbone(nn.Module):
    def __init__(self, vocab_size: int, max_len: int, d_model: int = 512, n_layers: int = 4,
                 n_heads: int = 8, dropout: float = 0.0, causal: bool = True,
                 d_ff: int | None = None, emb_rank: int | None = None, pos_enc: str = "abs"):
        super().__init__()
        assert pos_enc in ("abs", "rope"), pos_enc
        self.pos_enc = pos_enc
        self.causal = causal
        self.d_model = d_model
        self.emb_rank = emb_rank
        self.tok = nn.Embedding(vocab_size, emb_rank or d_model)
        self.emb_proj = nn.Linear(emb_rank, d_model, bias=False) if emb_rank else None
        if pos_enc == "abs":
            self.pos = nn.Embedding(max_len, d_model)
            layer = nn.TransformerEncoderLayer(d_model, n_heads, d_ff or 4 * d_model, dropout,
                                               activation="gelu", batch_first=True, norm_first=True)
            self.blocks = nn.TransformerEncoder(layer, n_layers, enable_nested_tensor=False)
        else:
            self.pos = None
            self.blocks = nn.ModuleList(RopeBlock(d_model, n_heads, d_ff or 4 * d_model, dropout)
                                        for _ in range(n_layers))
            cos, sin = _rope_cache(max_len, d_model // n_heads)
            self.register_buffer("_cos", cos, persistent=False)
            self.register_buffer("_sin", sin, persistent=False)
        self.ln_f = nn.LayerNorm(d_model)
        if not emb_rank:
            self.head = nn.Linear(d_model, vocab_size, bias=False)
            self.head.weight = self.tok.weight  # tied
        self.apply(self._init)
        if pos_enc == "rope":  # match nn.MultiheadAttention's default init of the q/k/v projection
            for b in self.blocks:
                nn.init.xavier_uniform_(b.qkv.weight)
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
        if self.pos_enc == "abs":
            x = e + self.pos(torch.arange(L, device=ids.device))[None]
            mask = self._causal_mask[:L, :L] if self.causal else None
            x = self.blocks(x, mask=mask)
        else:
            x = e
            for b in self.blocks:
                x = b(x, self._cos[:L], self._sin[:L], self.causal)
        x = self.ln_f(x)
        if self.emb_rank:  # tied through the factorization: h -> r -> vocab
            return F.linear(x @ self.emb_proj.weight, self.tok.weight)
        return self.head(x)

    def n_params(self, non_embedding: bool = False) -> int:
        n = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n -= self.tok.weight.numel() + (self.pos.weight.numel() if self.pos is not None else 0)
            if self.emb_rank:
                n -= self.emb_proj.weight.numel()
        return n
