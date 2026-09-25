"""Train one (tokenizer, objective, seed) cell. Reports throughput and MFU.

Objectives:
  ar         causal next-token prediction over all tokens
  mlm@p      bidirectional; fraction p of content tokens replaced by MASK,
             loss only on those positions (pure masking)

Two optimisation budgets are recorded per epoch: tokens processed and
supervised tokens (AR: all; MLM: the masked ones). The dual-budget analysis
in the report uses both.

Model selection: `best.pt` = lowest validation loss (kept for reference),
`final.pt` = last epoch. On iid synthetic data val-loss selection picks the
LEAST memorized epoch, so memorization metrics are read from final.pt.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import Dataset
from .model import Backbone
from .tokenizers import KmerTokenizer

RTX4090_BF16_PEAK_TFLOPS = 165.0


def parse_objective(obj: str):
    if obj == "ar":
        return "ar", 0.0
    assert obj.startswith("mlm@"), obj
    return "mlm", float(obj.split("@", 1)[1])


def with_bos(x: torch.Tensor, bos_id: int) -> torch.Tensor:
    bos = torch.full((x.shape[0], 1), bos_id, dtype=x.dtype, device=x.device)
    return torch.cat([bos, x], dim=1)


def mlm_corrupt(x: torch.Tensor, p: float, mask_id: int, gen: torch.Generator):
    B, L = x.shape
    sel = torch.rand((B, L), generator=gen, device=x.device) < p
    sel[:, 0] = False  # never BOS
    corrupted = x.clone()
    corrupted[sel] = mask_id
    return corrupted, sel


def loss_fn(model, tok: KmerTokenizer, x_tok: torch.Tensor, kind: str, p: float, gen):
    """x_tok: (B, T) content token ids (no BOS). Returns (loss, n_supervised)."""
    xb = with_bos(x_tok, tok.bos_id)
    if kind == "ar":
        logits = model(xb[:, :-1])
        tgt = xb[:, 1:]
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)).float(), tgt.reshape(-1))
        return loss, tgt.numel()
    corrupted, sel = mlm_corrupt(xb, p, tok.mask_id, gen)
    logits = model(corrupted)
    loss = F.cross_entropy(logits[sel].float(), xb[sel])
    return loss, int(sel.sum())


@torch.no_grad()
def eval_loss(model, tok, data_tok: np.ndarray, kind, p, device, batch=256, seed=0):
    model.eval()
    gen = torch.Generator(device=device).manual_seed(seed)
    tot, n = 0.0, 0
    for i in range(0, len(data_tok), batch):
        x = torch.from_numpy(data_tok[i:i + batch]).to(device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss, k = loss_fn(model, tok, x, kind, p, gen)
        tot += loss.item() * k
        n += k
    model.train()
    return tot / n


def train_cell(ds: Dataset, tok: KmerTokenizer, objective: str, seed: int, out_dir: Path,
               device: str = "cuda", epochs: int = 20, batch: int = 64, lr: float = 3e-4,
               warmup: int = 100, log_every: int = 50, dropout: float = 0.0,
               max_steps: int | None = None):
    """max_steps: optional hard cap on optimizer steps (fixed-supervised-token budget runs)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    kind, p = parse_objective(objective)
    torch.manual_seed(seed)
    np.random.seed(seed)
    train_tok = tok.encode(ds.train)          # pre-tokenize once
    val_tok = tok.encode(ds.val)
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), dropout=dropout).to(device)
    n_params = model.n_params()
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.01)
    steps_per_epoch = math.ceil(len(train_tok) / batch)
    total = steps_per_epoch * epochs if max_steps is None else min(max_steps, steps_per_epoch * epochs)

    def lr_at(step):
        if step < warmup:
            return lr * (step + 1) / warmup
        t = (step - warmup) / max(1, total - warmup)
        return lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, t))))

    gen = torch.Generator(device=device).manual_seed(seed)
    rng = np.random.default_rng(seed)
    log = open(out_dir / "train_log.jsonl", "w", encoding="utf-8")
    best, best_epoch, step = float("inf"), -1, 0
    tokens_seen, supervised_seen, t_start = 0, 0, time.time()
    model.train()
    done = False
    for epoch in range(epochs):
        order = rng.permutation(len(train_tok))
        t_ep, tok_ep, sup_ep = time.time(), 0, 0
        for i in range(0, len(order), batch):
            if max_steps is not None and step >= max_steps:
                done = True
                break
            x = torch.from_numpy(train_tok[order[i:i + batch]]).to(device, non_blocking=True)
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss, k = loss_fn(model, tok, x, kind, p, gen)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            tokens_seen += x.numel(); tok_ep += x.numel()
            supervised_seen += k; sup_ep += k
            if step % log_every == 0:
                log.write(json.dumps({"step": step, "epoch": epoch, "loss": loss.item(),
                                      "lr": lr_at(step), "supervised": k}) + "\n")
            step += 1
        torch.cuda.synchronize()
        dt = time.time() - t_ep
        v = eval_loss(model, tok, val_tok, kind, p, device)
        tflops = 6 * n_params * tok_ep / dt / 1e12
        rec = {"epoch": epoch, "step": step, "val_loss_nats": v,
               "val_bits_per_pred_token": v / math.log(2), "val_bits_per_nt": v / math.log(2) / tok.k,
               "epoch_sec": dt, "tokens_per_sec": tok_ep / dt, "supervised_tokens_epoch": sup_ep,
               "supervised_tokens_cum": supervised_seen, "tflops": tflops,
               "mfu": tflops / RTX4090_BF16_PEAK_TFLOPS}
        log.write(json.dumps(rec) + "\n"); log.flush()
        print(json.dumps(rec), flush=True)
        if v < best:
            best, best_epoch = v, epoch
            torch.save(model.state_dict(), out_dir / "best.pt")
        if done:
            break
    log.close()
    torch.save(model.state_dict(), out_dir / "final.pt")
    summary = {
        "objective": objective, "tokenizer": tok.name, "k": tok.k, "vocab_size": tok.vocab_size,
        "seed": seed, "n_params": n_params, "n_params_non_embedding": model.n_params(non_embedding=True),
        "epochs": epoch + 1, "steps": step, "batch": batch, "lr": lr,
        "best_val_loss_nats": best, "best_epoch": best_epoch,
        "total_train_sec": time.time() - t_start, "tokens_seen": tokens_seen,
        "supervised_tokens_seen": supervised_seen,
    }
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    model.eval()
    return model, summary
