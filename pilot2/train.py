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
               max_steps: int | None = None, save_epochs=None, model_kw=None, emb_lr_mult: float = 1.0,
               lora_r: int = 0, lora_alpha: int | None = None, lora_dropout: float = 0.05,
               init_from=None):
    """max_steps: optional hard cap on optimizer steps (fixed-supervised-token budget runs).
    save_epochs: iterable of 1-indexed epochs at which to save ep<N>.pt snapshots (training trajectory).
    model_kw: extra Backbone kwargs (d_ff, emb_rank, pos_enc) for capacity / position-encoding controls.
    emb_lr_mult: learning-rate multiplier for the token embedding table only (tied, so also the output head).
    lora_r: if > 0, train a LoRA adapter instead of all parameters, on the RoPE blocks' qkv / proj /
        ff1 / ff2 projections -- the analogue of the ["Wqkv", "dense", "gated_layers", "wo"] target
        set used to adapt Evo in the study this paper follows. The backbone's own weights are frozen,
        so the comparison against a full fine-tune isolates the fine-tuning strategy. Requires
        pos_enc="rope", because the default path uses nn.TransformerEncoder, whose fused in-projection
        is a raw Parameter rather than a Linear and so cannot be adapted.
    init_from: path to another run's final.pt to start from instead of a random initialisation. With
        this the cell is a FINE-TUNE of a model pretrained on other sequence, which is the setting the
        released checkpoints are in and the only setting in which "full against LoRA" is the question
        anyone is actually asking."""
    model_kw = {k: v for k, v in (model_kw or {}).items() if v}
    save_epochs = set(save_epochs or ())
    out_dir.mkdir(parents=True, exist_ok=True)
    kind, p = parse_objective(objective)
    torch.manual_seed(seed)
    np.random.seed(seed)
    train_tok = tok.encode(ds.train)          # pre-tokenize once
    val_tok = tok.encode(ds.val)
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), dropout=dropout, **model_kw).to(device)
    n_params = model.n_params()
    if init_from:
        sd = torch.load(init_from, map_location=device)
        if any(k.startswith("base_model.model.") for k in sd):   # a LoRA run's checkpoint
            sd = {k.replace("base_model.model.", "").replace(".base_layer.", "."): v
                  for k, v in sd.items() if "lora_" not in k}
        missing, unexpected = model.load_state_dict(sd, strict=False)
        assert not unexpected, f"{init_from}: unexpected keys {unexpected[:4]}"
        print(f"[init] from {init_from}" + (f" (missing {len(missing)})" if missing else ""), flush=True)
    if lora_r:
        assert model_kw.get("pos_enc") == "rope", "LoRA needs --pos_enc rope (see the docstring)"
        from peft import LoraConfig, get_peft_model
        model = get_peft_model(model, LoraConfig(
            r=lora_r, lora_alpha=lora_alpha or 2 * lora_r, lora_dropout=lora_dropout,
            target_modules=["qkv", "proj", "ff1", "ff2"], bias="none"))
        trainable = sum(q.numel() for q in model.parameters() if q.requires_grad)
        print(f"[lora] r={lora_r} -> {trainable/1e6:.3f}M trainable of {n_params/1e6:.2f}M "
              f"({100*trainable/n_params:.2f}%)", flush=True)
    emb_w = model.get_base_model().tok.weight if lora_r else model.tok.weight
    emb = [emb_w] if emb_w.requires_grad else []
    rest = [q for q in model.parameters() if q is not emb_w and q.requires_grad]
    opt = torch.optim.AdamW([{"params": rest, "mult": 1.0}] +
                            ([{"params": emb, "mult": emb_lr_mult}] if emb else []),
                            lr=lr, betas=(0.9, 0.95), weight_decay=0.01)
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
                g["lr"] = lr_at(step) * g["mult"]
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
        if (epoch + 1) in save_epochs:
            torch.save(model.state_dict(), out_dir / f"ep{epoch + 1}.pt")
        if done:
            break
    log.close()
    torch.save(model.state_dict(), out_dir / "final.pt")
    summary = {
        "objective": objective, "tokenizer": tok.name, "k": tok.k, "vocab_size": tok.vocab_size,
        "seed": seed, "model_kw": model_kw, "emb_lr_mult": emb_lr_mult, "n_params": n_params, "n_params_non_embedding": model.n_params(non_embedding=True),
        "epochs": epoch + 1, "steps": step, "batch": batch, "lr": lr,
        "best_val_loss_nats": best, "best_epoch": best_epoch,
        "total_train_sec": time.time() - t_start, "tokens_seen": tokens_seen,
        "supervised_tokens_seen": supervised_seen,
    }
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    model.eval()
    return model, summary
