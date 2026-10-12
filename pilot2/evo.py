"""Evo 1 (7B, StripedHyena, byte-level) with LoRA -- the model whose behaviour we are explaining.

    PYTHONPATH=/data/wh/yqdata/envs/tf444 python -m pilot2.evo --data ecoli --gpu 0

Why. In the study this paper follows, Evo is the leakiest model of the four by a distance: 100 %
canary extraction on all three real genomes even at a single insertion, where DNABERT-2 resists
extraction entirely. That is the result our tokeniser axis has to answer for, because Evo is
byte-level -- the finest tokenisation there is -- and our grid says fine tokenisation memorises
least. Evo also differs from that panel in scale, architecture, objective and fine-tuning strategy
at once, so the comparison there cannot say which is responsible. `queue_1011d` isolates the
fine-tuning strategy on our own backbone; this script measures the model itself under our rulers,
per nucleotide and at matched held-out loss rather than through a thresholded risk score.

Configuration follows the predecessor's so the numbers are comparable: LoRA rank 8, alpha 16,
dropout 0.05, on ["Wqkv", "dense", "gated_layers", "wo"], AdamW at 5e-5.

Fitting 7B on one 24 GB card: bf16 weights are about 14 GB, the adapter is megabytes, and gradient
checkpointing keeps activations small at our 288-nt windows. The tokenizer is byte-level, so a
window is 288 tokens and the model is character-level in our sense -- the scoring path is the same
one our own character cells use, with ASCII bytes in place of our nucleotide ids. Evo defines no BOS
token, so position 0 is a fixed padding byte: constant across members and controls, which is what
the comparison needs.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import WINDOW, build_dataset
from .real_data import DATA_PATHS, build_real_dataset
from .score import score_run

ROOT = os.environ.get("EVO_ROOT", "/data/wh/yqdata/models/EVO/evo-1-8k-base")
BYTES = {1: ord("A"), 2: ord("C"), 3: ord("G"), 4: ord("T")}   # our nt ids -> ASCII
PAD_BYTE = 1                                                    # Evo has no BOS; the predecessor pads with 1


class EvoVocab:
    """Evo's byte vocabulary, presented as one of our (character-level) tokenizers."""

    k = 1
    name = "evobyte"

    def __init__(self, window_nt: int = WINDOW, vocab_size: int = 512):
        self.window_nt, self.n_tokens = window_nt, window_nt
        self.vocab_size = vocab_size
        self.pad_id = self.bos_id = PAD_BYTE
        self.mask_id = PAD_BYTE                       # unused: Evo is causal
        self._to = np.zeros(5, dtype=np.int64)
        for k, v in BYTES.items():
            self._to[k] = v
        self._from = np.zeros(vocab_size, dtype=np.int64)
        for k, v in BYTES.items():
            self._from[v] = k
        self.content_ids = torch.tensor([BYTES[i] for i in (1, 2, 3, 4)])

    def to(self, device):
        self.content_ids = self.content_ids.to(device)
        return self

    def encode(self, nt: np.ndarray) -> np.ndarray:
        return self._to[nt]

    def decode(self, tok: np.ndarray) -> np.ndarray:
        return self._from[tok]

    def encode_t(self, nt: torch.Tensor) -> torch.Tensor:
        return torch.from_numpy(self.encode(nt.cpu().numpy())).to(nt.device)

    def decode_t(self, tok: torch.Tensor) -> torch.Tensor:
        return torch.from_numpy(self.decode(tok.cpu().numpy())).to(tok.device)

    def nt_to_tok(self, nt_pos: int) -> int:
        return nt_pos

    def span(self, nt_start: int, nt_end: int) -> slice:
        return slice(nt_start, nt_end)


class EvoModel(torch.nn.Module):
    """Chunks the batch, because the rulers do not know they are driving a 7B model.

    `rank_probe` scores a canary against its whole candidate pool in one forward, which is free for
    a 12.9M backbone and 2.8 GiB of FFT workspace for StripedHyena at 4096 channels. Chunking here
    keeps every scorer and the extraction loop unchanged."""

    def __init__(self, hf, max_batch: int = 2):
        super().__init__()
        self.hf, self.max_batch = hf, max_batch

    def _one(self, ids):
        out = self.hf(input_ids=ids)
        return out.logits if hasattr(out, "logits") else out[0]

    def forward(self, ids: torch.Tensor):
        if ids.shape[0] <= self.max_batch:
            return self._one(ids)
        return torch.cat([self._one(ids[i:i + self.max_batch])
                          for i in range(0, ids.shape[0], self.max_batch)], 0)


def _fix_triton_libcuda():
    """Triton insists on finding libcuda.so beside the libcuda.so.1 that ldconfig reports, and
    Ubuntu 18.04 ships only the runtime library. CUDA's own stub is the documented substitute for
    the link step (the real driver is loaded at run time), so point Triton at it rather than adding
    a symlink to a system directory on a machine other people share."""
    import glob
    stubs = [d for d in ("/usr/local/cuda/lib64/stubs", "/usr/local/cuda-12.1/lib64/stubs")
             if glob.glob(d + "/libcuda.so")]
    if not stubs:
        return
    try:
        import triton.common.build as tb
        tb.libcuda_dirs = lambda: stubs
        print(f"[evo] triton libcuda_dirs -> {stubs[0]}", flush=True)
    except Exception as e:
        print(f"[evo] could not patch triton: {type(e).__name__}: {e}", flush=True)


def load(device, lora_r: int, lora_alpha: int, lora_dropout: float, grad_ckpt: bool,
         max_batch: int = 2):
    _fix_triton_libcuda()
    from transformers import AutoModelForCausalLM
    hf = AutoModelForCausalLM.from_pretrained(ROOT, trust_remote_code=True,
                                              torch_dtype=torch.bfloat16)
    n = sum(p.numel() for p in hf.parameters())
    if grad_ckpt and hasattr(hf, "gradient_checkpointing_enable"):
        try:
            hf.gradient_checkpointing_enable()
        except Exception as e:                       # StripedHyena may not implement it
            print(f"[evo] gradient checkpointing unavailable: {e}", flush=True)
    if lora_r:
        from peft import LoraConfig, get_peft_model
        hf = get_peft_model(hf, LoraConfig(
            r=lora_r, lora_alpha=lora_alpha, lora_dropout=lora_dropout, bias="none",
            # no task_type: peft's CAUSAL_LM wrapper calls forward(inputs_embeds=...), which
            # StripedHyena does not accept. Without it peft only injects adapters into the
            # targeted Linear layers and leaves the forward signature alone.
            target_modules=["Wqkv", "dense", "gated_layers", "wo"]))
        tr = sum(p.numel() for p in hf.parameters() if p.requires_grad)
        print(f"[evo] LoRA r={lora_r} -> {tr/1e6:.2f}M trainable of {n/1e9:.2f}B "
              f"({100*tr/n:.4f}%)", flush=True)
    hf = hf.to(device)
    print(f"[evo] {n/1e9:.2f}B parameters, {torch.cuda.memory_allocated(device)/2**30:.1f} GiB on card",
          flush=True)
    return EvoModel(hf, max_batch), n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="ecoli", choices=["synthetic", *DATA_PATHS])
    ap.add_argument("--fasta", default=None)
    ap.add_argument("--canary_npz", default=None)
    ap.add_argument("--n_train", type=int, default=2000)
    ap.add_argument("--n_val", type=int, default=200)
    ap.add_argument("--n_test", type=int, default=200)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--n_nonmember", type=int, default=20)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--pool", type=int, default=100)
    ap.add_argument("--floor_n", type=int, default=100)
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--batch", type=int, default=1)
    ap.add_argument("--accum", type=int, default=16)
    ap.add_argument("--lr", type=float, default=5e-5)
    ap.add_argument("--lora_r", type=int, default=8)
    ap.add_argument("--lora_alpha", type=int, default=16)
    ap.add_argument("--lora_dropout", type=float, default=0.05)
    ap.add_argument("--no_grad_ckpt", action="store_true")
    ap.add_argument("--max_batch", type=int, default=2, help="forward-pass chunk for the scorers")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--save_epochs", default="1,2,5,10")
    ap.add_argument("--score_epoch0", action="store_true")
    ap.add_argument("--smoke", action="store_true", help="load, score once, exit")
    ap.add_argument("--out", default="outputs/evo")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(args.seed)
    t0 = time.time()

    tiers = tuple(int(t) for t in args.tiers.split(","))
    if args.data != "synthetic":
        ds = build_real_dataset(args.fasta or DATA_PATHS[args.data], args.n_train, args.n_val, args.n_test,
                                args.probes_per_tier, tiers, args.n_nonmember, args.data_seed,
                                offset_mode=args.probe_offset, canary_npz=args.canary_npz)
    else:
        ds = build_dataset(args.n_train, args.n_val, args.n_test, args.probes_per_tier, tiers,
                           args.n_nonmember, args.data_seed, offset_mode=args.probe_offset)

    # the run name carries every knob that changes the experiment, so two cells of the same arm
    # can never write into the same directory
    name = (f"evo1_lora{args.lora_r}_{args.data}_e{args.epochs}_n{args.n_train}"
            f"_{args.probe_offset}_s{args.seed}")
    out_dir = Path(args.out) / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")
    ds.save_meta(out_dir / "data_meta.json")

    model, n_params = load(device, args.lora_r, args.lora_alpha, args.lora_dropout,
                           not args.no_grad_ckpt, args.max_batch)
    voc = EvoVocab().to(device)
    train_tok = torch.from_numpy(voc.encode(ds.train))
    bos = torch.full((train_tok.shape[0], 1), voc.bos_id, dtype=train_tok.dtype)
    train_tok = torch.cat([bos, train_tok], 1)

    def score(tag, epoch):
        model.eval()
        with torch.no_grad():
            sc = score_run(model, voc, "ar", ds, device, pool_size=args.pool, seed=args.seed,
                           floor_n=args.floor_n, offset_mode=args.probe_offset)
        sc["epoch"] = epoch
        (out_dir / f"scores_{tag}.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
        print(f"[{name}] {tag}: floor {sc['floors'][0]['bits_per_nt_mean']:.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)
        return sc

    if args.smoke or args.score_epoch0:
        score("ep0", 0)
        if args.smoke:
            return 0

    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=0.01)
    rng = np.random.default_rng(args.seed)
    save_epochs = {int(e) for e in args.save_epochs.split(",") if e}
    log = open(out_dir / "train_log.jsonl", "w", encoding="utf-8")
    for epoch in range(args.epochs):
        model.train()
        order = rng.permutation(len(train_tok))
        tot, nb = 0.0, 0
        opt.zero_grad(set_to_none=True)
        for i in range(0, len(order), args.batch):
            ids = train_tok[order[i:i + args.batch]].to(device)
            logits = model(ids)[:, :-1]
            loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]).float(),
                                   ids[:, 1:].reshape(-1))
            (loss / args.accum).backward()
            if (i // args.batch + 1) % args.accum == 0:
                torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
                opt.step()
                opt.zero_grad(set_to_none=True)
            tot += float(loss)
            nb += 1
        log.write(json.dumps({"epoch": epoch + 1, "train_loss": tot / max(1, nb),
                              "sec": time.time() - t0}) + "\n")
        log.flush()
        print(f"[{name}] epoch {epoch+1}/{args.epochs} loss {tot/max(1,nb):.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)
        if epoch + 1 in save_epochs:
            score(f"ep{epoch+1}", epoch + 1)
    log.close()
    if args.lora_r:                      # keep the adapter: it is megabytes, and without it the
        try:                             # fine-tuned state cannot be re-examined afterwards
            model.hf.save_pretrained(out_dir / "adapter")
            print(f"[{name}] adapter saved", flush=True)
        except Exception as e:
            print(f"[{name}] could not save adapter: {type(e).__name__}: {e}", flush=True)
    sc = score("final", args.epochs)
    sc.update(n_params=n_params, total_sec=time.time() - t0)
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(f"[{name}] done in {time.time()-t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
