"""Nucleotide Transformer v2 on the planted-canary data -- the released model that sits ON our axis.

    PYTHONPATH=/data/wh/yqdata/envs/tf444 python -m pilot2.nt --size 250m --data ecoli --gpu 0

Why this model and not another. Every released checkpoint we audit tokenises in a way that is NOT
the axis of the controlled grid: DNABERT uses OVERLAPPING k-mers, so changing k changes the
vocabulary without changing how many slots carry a record; DNABERT-2 uses BPE; HyenaDNA is
character-level but differs in architecture. The Nucleotide Transformer v2 is the missing case --
its vocabulary is the 4096 NON-overlapping 6-mers, which is exactly our \\kmer{6} cell with 250M or
500M pretrained parameters behind it. A 288-nt window is 48 tokens for both, so the comparison is
direct rather than analogical.

Implementation. Rather than reimplement the rulers, this wraps NT so that it satisfies the same
interface our own tokenisers do (`encode`, `decode_t`, `nt_to_tok`, `span`, `content_ids`,
`mask_id`, `bos_id`), after which `pilot2.score`'s ranking, surprise and extraction run on it
unchanged. The vocabulary mapping is read from the checkpoint's own `vocab.txt` rather than assumed:
NT orders its 6-mers A,T,C,G per position while ours are A,C,G,T, so a hard-coded formula would
silently score the wrong k-mer.

Objective. Masked only, which is a limitation of the checkpoint rather than a choice: we fine-tune
DNABERT causally as well as masked by passing a causal attention mask into the encoder, but NT's
released modelling code multiplies its embeddings by the attention mask
(`embeddings * attention_mask.unsqueeze(-1)`), so it accepts a padding mask and nothing else. A
causal variant would need the published code to be rewritten, which would stop it being the released
model. We therefore run NT under its native masked objective and score it with the same two
bidirectional scorers used for every masked cell in this paper -- pseudo-log-likelihood and the
prefix-conditioned scorer, the latter emulating causal conditioning by masking everything after the
position being read, with no attention mask involved. One masked token hides 6 nucleotides, so
--mask_rate is the hidden-nucleotide rate divided by 6.
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

from .data import PROBE_LEN, WINDOW, build_dataset, decode
from .real_data import DATA_PATHS, build_real_dataset
from .score import score_run

ROOT = os.environ.get("NT_ROOT", "/data/wh/yqdata/models/NT")
SIZES = {"50m": "nucleotide-transformer-v2-50m-multi-species",
         "100m": "nucleotide-transformer-v2-100m-multi-species",
         "250m": "nucleotide-transformer-v2-250m-multi-species",
         "500m": "nucleotide-transformer-v2-500m-multi-species"}
LETTERS = "ACGT"                      # our nt ids are A=1, C=2, G=3, T=4


class NTVocab:
    """NT's non-overlapping 6-mer vocabulary, presented as one of our tokenizers."""

    k = 6
    name = "nt6mer"

    def __init__(self, model_dir: Path, window_nt: int = WINDOW):
        vocab = [l.strip() for l in open(model_dir / "vocab.txt", encoding="utf-8") if l.strip()]
        self.vocab_size = len(vocab)
        self.index = {t: i for i, t in enumerate(vocab)}
        self.pad_id, self.mask_id = self.index["<pad>"], self.index["<mask>"]
        self.bos_id = self.index["<cls>"]              # NT prepends <cls>; our scorers prepend bos
        assert window_nt % self.k == 0
        self.window_nt, self.n_tokens = window_nt, window_nt // self.k
        # our content id -> NT id, read off the checkpoint's own vocabulary
        ours = np.arange(4 ** self.k)
        digits = [(ours // 4 ** (self.k - 1 - i)) % 4 for i in range(self.k)]
        strs = ["".join(LETTERS[d[j]] for d in digits) for j in range(len(ours))]
        missing = [s for s in strs if s not in self.index]
        assert not missing, f"{len(missing)} k-mers absent from the NT vocabulary, e.g. {missing[:3]}"
        self._our2nt = torch.tensor([self.index[s] for s in strs])
        self._nt2our = torch.full((self.vocab_size,), -1, dtype=torch.long)
        self._nt2our[self._our2nt] = torch.arange(len(strs))
        self.content_ids = self._our2nt.clone()        # the 4096 6-mers, in NT's numbering
        self._pow = (4 ** np.arange(self.k - 1, -1, -1)).astype(np.int64)

    def kmer_letters(self, device):
        """(4096, 6) nt ids 1..4 for content_ids, in the same order -- ours, not NT's."""
        ours = np.arange(4 ** self.k)
        cols = [((ours // p) % 4) + 1 for p in self._pow]
        return torch.from_numpy(np.stack(cols, 1)).to(device)

    def to(self, device):
        self._our2nt = self._our2nt.to(device)
        self._nt2our = self._nt2our.to(device)
        self.content_ids = self.content_ids.to(device)
        return self

    # ---- nt <-> token --------------------------------------------------
    def encode(self, nt: np.ndarray) -> np.ndarray:
        B, L = nt.shape
        ours = ((nt - 1).reshape(B, L // self.k, self.k) * self._pow).sum(-1)
        return self._our2nt.cpu().numpy()[ours]

    def decode(self, tok: np.ndarray) -> np.ndarray:
        ours = self._nt2our.cpu().numpy()[tok]
        assert (ours >= 0).all(), "a non-k-mer token reached decode"
        out = np.empty((*ours.shape, self.k), dtype=np.int64)
        for i, p in enumerate(self._pow):
            out[..., i] = (ours // p) % 4
        return out.reshape(ours.shape[0], -1) + 1

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


class NTModel(torch.nn.Module):
    """model(ids) -> logits, with the causal mask folded in for the next-token objective."""

    def __init__(self, hf, causal: bool):
        super().__init__()
        self.hf, self.causal = hf, causal

    def forward(self, ids: torch.Tensor):
        return self.hf(input_ids=ids).logits


def load(size: str, causal: bool, device):
    from transformers import AutoModelForMaskedLM
    d = Path(ROOT) / SIZES[size]
    assert d.exists(), f"{d} not downloaded"
    hf = AutoModelForMaskedLM.from_pretrained(d, trust_remote_code=True).to(device)
    n = sum(p.numel() for p in hf.parameters())
    print(f"[nt-{size}] {n/1e6:.1f}M parameters, vocab {hf.config.vocab_size}", flush=True)
    return NTModel(hf, causal).to(device), n


def causal_loss(model, voc, ids):
    """next-token over 6-mer tokens; <cls> is position 0 so token j is predicted from column j."""
    logits = model(ids)[:, :-1]
    return F.cross_entropy(logits.reshape(-1, logits.shape[-1]).float(), ids[:, 1:].reshape(-1))


def mlm_loss(model, voc, ids, rate, gen):
    keep = torch.rand(ids.shape, device=ids.device, generator=gen) < rate
    keep[:, 0] = False                                  # never mask <cls>
    if not keep.any():
        keep[:, 1] = True
    x = ids.clone()
    x[keep] = voc.mask_id
    logits = model(x)
    return F.cross_entropy(logits[keep].float(), ids[keep])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="250m", choices=list(SIZES))
    ap.add_argument("--objective", default="mlm", choices=["mlm"],
                    help="masked only; the released NT code cannot take a causal attention mask")
    ap.add_argument("--mask_rate", type=float, default=0.15)
    ap.add_argument("--data", default="synthetic", choices=["synthetic", *DATA_PATHS])
    ap.add_argument("--fasta", default=None)
    ap.add_argument("--canary_npz", default=None)
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--n_val", type=int, default=500)
    ap.add_argument("--n_test", type=int, default=500)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--probes_per_tier", type=int, default=50)
    ap.add_argument("--n_nonmember", type=int, default=50)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--pool", type=int, default=100)
    ap.add_argument("--floor_n", type=int, default=200)
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--save_epochs", default="1,3,8,15,30,50")
    ap.add_argument("--save_ckpt", action="store_true",
                    help="accepted for compatibility and now a no-op: weights are kept by default")
    ap.add_argument("--no_save_ckpt", action="store_true",
                    help="do not write the fine-tuned weights. NOT the default any more: keeping checkpoints is now the default: /data has 5.3 TiB free, our own snapshots are 56 MiB each and a 250M released one is about 1 GiB, and keeping them is what lets the search-based decoder in pilot2.recon_audit be pointed at any round of a finished run instead of only at its last one. That is how the extraction-versus-training-round curve gets measured without retraining anything.")
    ap.add_argument("--score_epoch0", action="store_true")
    ap.add_argument("--out", default="outputs/nt")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    t0 = time.time()

    tiers = tuple(int(t) for t in args.tiers.split(","))
    if args.data != "synthetic":
        ds = build_real_dataset(args.fasta or DATA_PATHS[args.data], args.n_train, args.n_val, args.n_test,
                                args.probes_per_tier, tiers, args.n_nonmember, args.data_seed,
                                offset_mode=args.probe_offset, canary_npz=args.canary_npz)
    else:
        ds = build_dataset(args.n_train, args.n_val, args.n_test, args.probes_per_tier, tiers,
                           args.n_nonmember, args.data_seed, offset_mode=args.probe_offset)

    name = f"nt{args.size}_{args.objective}" + (f"_{args.data}" if args.data != "synthetic" else "") + f"_s{args.seed}"
    out_dir = Path(args.out) / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")
    ds.save_meta(out_dir / "data_meta.json")

    model, n_params = load(args.size, False, device)
    voc = NTVocab(Path(ROOT) / SIZES[args.size]).to(device)
    kind = "mlm"
    train_tok = torch.from_numpy(voc.encode(ds.train))
    cls = torch.full((train_tok.shape[0], 1), voc.bos_id, dtype=train_tok.dtype)
    train_tok = torch.cat([cls, train_tok], 1)

    save_epochs = {int(e) for e in args.save_epochs.split(",") if e}
    if args.score_epoch0:
        model.eval()
        sc = score_run(model, voc, kind, ds, device, pool_size=args.pool, seed=args.seed,
                       floor_n=args.floor_n, offset_mode=args.probe_offset)
        (out_dir / "scores_ep0.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
        print(f"[{name}] epoch 0 floor {sc['floors'][0]['bits_per_nt_mean']:.4f}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    gen = torch.Generator(device=device).manual_seed(args.seed)
    rng = np.random.default_rng(args.seed)
    steps = math.ceil(len(train_tok) / args.batch / args.accum)
    log = open(out_dir / "train_log.jsonl", "w", encoding="utf-8")
    for epoch in range(args.epochs):
        model.train()
        order = rng.permutation(len(train_tok))
        tot, nb = 0.0, 0
        opt.zero_grad(set_to_none=True)
        for i in range(0, len(order), args.batch):
            ids = train_tok[order[i:i + args.batch]].to(device)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss = mlm_loss(model, voc, ids, args.mask_rate, gen)
            (loss / args.accum).backward()
            if (i // args.batch + 1) % args.accum == 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
                opt.zero_grad(set_to_none=True)
            tot += float(loss)
            nb += 1
        log.write(json.dumps({"epoch": epoch + 1, "train_loss": tot / max(1, nb)}) + "\n")
        log.flush()
        print(f"[{name}] epoch {epoch+1}/{args.epochs} loss {tot/max(1,nb):.4f} "
              f"({time.time()-t0:.0f}s)", flush=True)
        if epoch + 1 in save_epochs:
            model.eval()
            sc = score_run(model, voc, kind, ds, device, pool_size=args.pool, seed=args.seed,
                           floor_n=args.floor_n, offset_mode=args.probe_offset)
            sc["epoch"] = epoch + 1
            (out_dir / f"scores_ep{epoch+1}.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
            print(f"[{name}] ep{epoch+1} floor {sc['floors'][0]['bits_per_nt_mean']:.4f}", flush=True)
            if not args.no_save_ckpt:
                torch.save(model.hf.state_dict(), out_dir / f"ckpt_ep{epoch+1}.pt")
    log.close()
    model.eval()
    sc = score_run(model, voc, kind, ds, device, pool_size=args.pool, seed=args.seed,
                   floor_n=args.floor_n, offset_mode=args.probe_offset)
    sc.update(epoch=args.epochs, n_params=n_params, total_sec=time.time() - t0)
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    if not args.no_save_ckpt:
        torch.save(model.hf.state_dict(), out_dir / "final.pt")
    print(f"[{name}] done in {time.time()-t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
