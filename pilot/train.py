"""Train one (objective, seed) cell. Reports throughput and MFU.

Objectives:
  ar         causal next-token prediction over all 288 positions
  mlm@p      bidirectional; p of the 288 positions replaced by MASK, loss only
             on those positions (pure masking, no BERT 80/10/10 trick)

Model selection: lowest loss on the VALIDATION split (disjoint from test),
under the same objective. Loss is only ever computed on real nucleotide
positions -- there is no padding in this harness by construction.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import A, BOS, MASK, T, WINDOW, Dataset, with_bos
from .model import Backbone

RTX4090_BF16_PEAK_TFLOPS = 165.0  # dense tensor-core peak, used for MFU


def parse_objective(obj: str):
    if obj == "ar":
        return "ar", 0.0
    assert obj.startswith("mlm@"), obj
    return "mlm", float(obj.split("@", 1)[1])


def mlm_corrupt(x: torch.Tensor, p: float, gen: torch.Generator):
    """x: (B, L) with BOS at column 0. Mask a fraction p of the nucleotide
    positions (never BOS). Returns (corrupted, target_mask)."""
    B, L = x.shape
    sel = torch.rand((B, L), generator=gen, device=x.device) < p
    sel[:, 0] = False
    corrupted = x.clone()
    corrupted[sel] = MASK
    return corrupted, sel


def loss_fn(model: Backbone, x: torch.Tensor, kind: str, p: float, gen: torch.Generator):
    """Returns (loss, n_supervised_tokens). x is (B, WINDOW) nucleotide ids."""
    xb = with_bos(x)
    if kind == "ar":
        logits = model(xb[:, :-1])
        tgt = xb[:, 1:]
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)).float(), tgt.reshape(-1))
        return loss, tgt.numel()
    corrupted, sel = mlm_corrupt(xb, p, gen)
    logits = model(corrupted)
    loss = F.cross_entropy(logits[sel].float(), xb[sel])
    return loss, int(sel.sum())


@torch.no_grad()
def eval_loss(model, data: np.ndarray, kind, p, device, batch=256, seed=0):
    model.eval()
    gen = torch.Generator(device=device).manual_seed(seed)  # fixed mask pattern for val
    tot, n = 0.0, 0
    for i in range(0, len(data), batch):
        x = torch.from_numpy(data[i:i + batch]).to(device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss, k = loss_fn(model, x, kind, p, gen)
        tot += loss.item() * k
        n += k
    model.train()
    return tot / n


def train_cell(ds: Dataset, objective: str, seed: int, out_dir: Path, device: str = "cuda",
               epochs: int = 20, batch: int = 64, lr: float = 3e-4, warmup: int = 100,
               log_every: int = 50, dropout: float = 0.0):
    out_dir.mkdir(parents=True, exist_ok=True)
    kind, p = parse_objective(objective)
    torch.manual_seed(seed)
    np.random.seed(seed)
    model = Backbone(causal=(kind == "ar"), dropout=dropout).to(device)
    n_params = model.n_params()
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.01)
    steps_per_epoch = math.ceil(len(ds.train) / batch)
    total = steps_per_epoch * epochs

    def lr_at(step):
        if step < warmup:
            return lr * (step + 1) / warmup
        t = (step - warmup) / max(1, total - warmup)
        return lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * t)))

    gen = torch.Generator(device=device).manual_seed(seed)
    rng = np.random.default_rng(seed)
    log = open(out_dir / "train_log.jsonl", "w", encoding="utf-8")
    best, best_epoch, step = float("inf"), -1, 0
    tokens_seen, t_start = 0, time.time()
    model.train()
    for epoch in range(epochs):
        order = rng.permutation(len(ds.train))
        t_ep, tok_ep = time.time(), 0
        for i in range(0, len(order), batch):
            x = torch.from_numpy(ds.train[order[i:i + batch]]).to(device, non_blocking=True)
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss, k = loss_fn(model, x, kind, p, gen)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            # throughput counts every position the model processed, supervised or not
            tokens_seen += x.numel()
            tok_ep += x.numel()
            if step % log_every == 0:
                log.write(json.dumps({"step": step, "epoch": epoch, "loss": loss.item(),
                                      "lr": lr_at(step), "supervised": k}) + "\n")
            step += 1
        torch.cuda.synchronize()
        dt = time.time() - t_ep
        v = eval_loss(model, ds.val, kind, p, device)
        tflops = 6 * n_params * tok_ep / dt / 1e12
        rec = {"epoch": epoch, "val_loss_nats": v, "val_bits_per_pred": v / math.log(2),
               "epoch_sec": dt, "tokens_per_sec": tok_ep / dt, "tflops": tflops,
               "mfu": tflops / RTX4090_BF16_PEAK_TFLOPS}
        log.write(json.dumps(rec) + "\n")
        log.flush()
        print(json.dumps(rec), flush=True)
        if v < best:
            best, best_epoch = v, epoch
            torch.save(model.state_dict(), out_dir / "best.pt")
    log.close()
    torch.save(model.state_dict(), out_dir / "final.pt")
    summary = {
        "objective": objective, "seed": seed, "n_params": n_params,
        "n_params_non_embedding": model.n_params(non_embedding=True),
        "epochs": epochs, "batch": batch, "lr": lr, "best_val_loss_nats": best,
        "best_epoch": best_epoch, "total_train_sec": time.time() - t_start,
        "tokens_seen": tokens_seen,
    }
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    model.load_state_dict(torch.load(out_dir / "best.pt", map_location=device))
    model.eval()
    return model, summary
