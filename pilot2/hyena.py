"""E4 arm (b): pretrained HyenaDNA (single-nucleotide, causal) on the planted-canary data.

    python -m pilot2.hyena --model hyenadna-small-32k-seqlen-hf --seed 0 --gpu 0
    python -m pilot2.hyena --model hyenadna-medium-160k-seqlen-hf --smoke

Same data as pilot2 (288-nt windows, probes at random offsets by default). The pretrained
unembedding is kept (no new head). HyenaDNA is a character model, so the pilot2 metrics apply
directly: p(nt_j | nt_<j) is read from the four ACGT logits at position j, normalised over the
four letters; ranking against a random pool; greedy extraction from a 48-nt prefix.
A [BOS] token is prepended so that position 0 is predictable. Fine-tuning follows the
published HyenaDNA config: AdamW, lr 2e-5, wd 0.01, 10% warm-up then constant, batch 8 x 2.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Probe, build_dataset, random_dna
from .real_data import DATA_PATHS, REAL_DATA, build_real_dataset

MODEL_ROOT = "/data/wh/yqdata/models/HyenaDNA"
NT_IDS = torch.tensor([7, 8, 9, 10])   # HyenaDNA vocab: A C G T  (pilot2 nt ids 1..4 -> +6)
BOS = 2


def load_model(name: str, device):
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(Path(MODEL_ROOT) / name, trust_remote_code=True).to(device)
    return model


def encode(nt: torch.Tensor) -> torch.Tensor:
    """(B, W) pilot2 nt ids -> (B, W+1) HyenaDNA ids with [BOS] in front."""
    bos = torch.full((nt.shape[0], 1), BOS, dtype=torch.long, device=nt.device)
    return torch.cat([bos, nt + 6], 1)


@torch.no_grad()
def nt_logprobs(model, nt: torch.Tensor, positions, device, batch=128):
    """log2 p(true nt_j | nt_<j) for every window and every j in positions, normalised over ACGT."""
    ids = encode(nt.to(device))
    pos = torch.tensor(list(positions), device=device)
    nt_ids = NT_IDS.to(device)
    out = torch.empty(ids.shape[0], len(pos), device=device)
    for b0 in range(0, ids.shape[0], batch):
        xb = ids[b0:b0 + batch]
        logits = model(input_ids=xb).logits.float()                       # (w, W+1, V); index j predicts ids[j+1] = nt j
        at = logits[:, pos][..., nt_ids]                                   # (w, P, 4)
        lp = F.log_softmax(at, dim=-1)
        true = nt[b0:b0 + batch].to(device)[:, pos] - 1                     # 0..3
        out[b0:b0 + xb.shape[0]] = lp.gather(-1, true[..., None])[..., 0] / math.log(2.0)
    return out


def heldout_floor(model, test_nt, device, n=200):
    bits = (-nt_logprobs(model, torch.from_numpy(test_nt[:n]), range(WINDOW), device)).mean(1).cpu().numpy()
    return {"scorer": "causal", "n_windows": int(len(bits)), "positions": WINDOW, "bits_per_nt_mean": float(bits.mean()),
            "bits_per_nt_std": float(bits.std()), "floor_ok": bool(bits.mean() >= 1.95)}


def rank_probe(model, probe: Probe, host, pool, device, offset: int):
    n = len(pool)
    win = np.tile(host[None, :], (n + 1, 1))
    win[0, offset:offset + PROBE_LEN] = probe.seq
    win[1:, offset:offset + PROBE_LEN] = pool
    s = nt_logprobs(model, torch.from_numpy(win), range(offset, offset + PROBE_LEN), device).sum(1).cpu().numpy()
    true, cands = s[0], s[1:]
    rank = 1 + int((cands > true).sum())
    return {"rank": rank, "n_pool": n, "p_chance": rank / (n + 1), "offset": int(offset), "positions": PROBE_LEN,
            "probe_bits_per_nt": float(-true / PROBE_LEN), "pool_bits_per_nt_mean": float((-cands / PROBE_LEN).mean()),
            "z": float((true - cands.mean()) / (cands.std() + 1e-9))}


@torch.no_grad()
def extract_prefix(model, probe: Probe, host, device, offset: int, k_nt: int = 48):
    start, end = offset + k_nt, offset + PROBE_LEN
    win = host.copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    truth = win[start:end].copy()
    cur = torch.from_numpy(win[:start])[None].to(device)
    nt_ids = NT_IDS.to(device)
    pred = []
    for _ in range(end - start):
        lg = model(input_ids=encode(cur)).logits[0, -1].float()[nt_ids]
        a = int(lg.argmax()) + 1
        pred.append(a)
        cur = torch.cat([cur, torch.tensor([[a]], device=device)], 1)
    pred = np.array(pred)
    ham = int((pred != truth).sum())
    return {"k_revealed_nt": k_nt, "offset": int(offset), "n_generated_nt": int(end - start), "exact": bool(ham == 0), "hamming_nt": ham}


def score_run(model, ds, device, pool_size, seed, probes_per_tier=None):
    rng = np.random.default_rng(10_000 + seed)
    pool = random_dna(rng, pool_size, PROBE_LEN)
    fresh_hosts = {p.probe_id: random_dna(rng, 1, WINDOW)[0] for p in ds.probes}
    off_rng = np.random.default_rng(20_000 + seed)
    fresh_off = {p.probe_id: int(off_rng.integers(0, WINDOW - PROBE_LEN + 1)) for p in ds.probes}
    probes = ds.probes
    if probes_per_tier:
        keep, seen = [], {}
        for p in probes:
            if seen.get(p.repetitions, 0) < probes_per_tier:
                keep.append(p); seen[p.repetitions] = seen.get(p.repetitions, 0) + 1
        probes = keep
    res = {"kind": "hyena", "k": 1, "objective": "causal", "pool_size": pool_size,
           "floors": [heldout_floor(model, ds.test, device)], "probes": []}
    for p in probes:
        fo = fresh_off[p.probe_id]
        e = {"probe_id": p.probe_id, "repetitions": p.repetitions, "ranks": {}, "extract": {},
             "train_offsets": list(p.offsets), "fresh_offset": fo}
        hosts = {"fresh": (fresh_hosts[p.probe_id], fo)}
        if p.repetitions > 0:
            hosts["train"] = (ds.train[p.host_rows[0]], p.offsets[0] if p.offsets else PROBE_OFFSET)
        for hname, (host, off) in hosts.items():
            e["ranks"][f"causal/{hname}"] = rank_probe(model, p, host, pool, device, off)
            e["extract"][hname] = extract_prefix(model, p, host, device, off)
        res["probes"].append(e)
    return res


def train(model, ds, device, out_dir: Path, epochs, lr, batch, accum, seed, save_epochs, log):
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    train_nt = torch.from_numpy(ds.train)
    steps_per_epoch = math.ceil(len(train_nt) / batch / accum)
    total = steps_per_epoch * epochs
    warm = int(0.1 * total)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    lr_at = lambda s: lr * (0.1 + 0.9 * (s + 1) / max(1, warm)) if s < warm else lr
    step, t0 = 0, time.time()
    model.train()
    for ep in range(1, epochs + 1):
        order = rng.permutation(len(train_nt))
        tot, n = 0.0, 0
        for i in range(0, len(order), batch * accum):
            for g in opt.param_groups:
                g["lr"] = lr_at(step)
            opt.zero_grad(set_to_none=True)
            for a in range(accum):
                idx = order[i + a * batch:i + (a + 1) * batch]
                if len(idx) == 0:
                    continue
                ids = encode(train_nt[torch.as_tensor(idx)].to(device))
                logits = model(input_ids=ids).logits[:, :-1].float()
                loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), ids[:, 1:].reshape(-1))
                (loss / accum).backward()
                tot += loss.item(); n += 1
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); step += 1
        log.write(json.dumps({"epoch": ep, "train_loss": tot / max(1, n), "lr": lr_at(step), "sec": time.time() - t0}) + "\n"); log.flush()
        print(f"[hyena s{seed}] epoch {ep}/{epochs} loss {tot / max(1, n):.4f} ({time.time() - t0:.0f}s)", flush=True)
        if ep in save_epochs:
            torch.save(model.state_dict(), out_dir / f"ep{ep}.pt")
    model.eval()
    return {"epochs": epochs, "steps": step, "lr": lr, "batch": batch * accum, "objective": "causal",
            "train_sec": time.time() - t0, "n_params": sum(p.numel() for p in model.parameters())}


def summary_line(tag, sc):
    out = [f"floor {sc['floors'][0]['bits_per_nt_mean']:.3f}"]
    for t in (1, 4, 16):
        for host in ("train", "fresh"):
            ps = [p for p in sc["probes"] if p["repetitions"] == t]
            if ps:
                b = np.mean([p["ranks"][f"causal/{host}"]["probe_bits_per_nt"] for p in ps])
                r1 = np.mean([p["ranks"][f"causal/{host}"]["rank"] == 1 for p in ps])
                ex = np.mean([p["extract"][host]["exact"] for p in ps])
                out.append(f"r{t}/{host} {b:.2f}/{r1:.2f}/{ex:.2f}")
    fp = [p for p in sc["probes"] if p["repetitions"] == 0]
    if fp:
        out.append(f"fp {np.mean([p['ranks']['causal/fresh']['rank'] == 1 for p in fp]):.2f}")
    return f"[{tag}] " + " | ".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="hyenadna-small-32k-seqlen-hf")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/hyena")
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--probe_offset", default="random", choices=["fixed", "random"])
    ap.add_argument("--data", default="synthetic", choices=["synthetic", *REAL_DATA],
                    help="synthetic iid DNA, or real E. coli windows (held-out E. coli loss then doubles as the utility metric)")
    ap.add_argument("--fasta", default=None, help="override the default path of --data")
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--accum", type=int, default=2)
    ap.add_argument("--pool", type=int, default=500)
    ap.add_argument("--save_epochs", default="1,3,8,15,30")
    ap.add_argument("--snapshot_probes", type=int, default=20)
    ap.add_argument("--score_epoch0", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args(argv)
    if args.smoke:
        args.n_train, args.probes_per_tier, args.n_nonmember = 200, 2, 2
        args.epochs, args.pool, args.save_epochs = 1, 10, "1"
        args.out = os.path.join(args.out, "smoke")
    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    short = args.model.replace("hyenadna-", "").replace("-seqlen-hf", "")
    tag = f"_lr{args.lr:g}" if args.lr != 2e-5 else ""
    if args.data != "synthetic":
        tag += f"_{args.data}"
    out_dir = Path(args.out) / f"hyena_{short}{tag}_s{args.seed}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")
    tiers = tuple(int(t) for t in args.tiers.split(","))
    if args.data != "synthetic":
        args.fasta = args.fasta or DATA_PATHS[args.data]
        ds = build_real_dataset(args.fasta, args.n_train, 200, 200, args.probes_per_tier, tiers, args.n_nonmember,
                                args.data_seed, offset_mode=args.probe_offset)
    else:
        ds = build_dataset(args.n_train, 200, 200, args.probes_per_tier, tiers, args.n_nonmember, args.data_seed,
                           offset_mode=args.probe_offset)
    ds.save_meta(out_dir / "data_meta.json")
    model = load_model(args.model, device)
    print(f"[hyena] {args.model}: {sum(p.numel() for p in model.parameters()) / 1e6:.2f}M params", flush=True)
    save_epochs = sorted(int(e) for e in args.save_epochs.split(",") if e)
    t0 = time.time()
    if args.score_epoch0:
        model.eval()
        sc = score_run(model, ds, device, args.pool, args.seed, args.snapshot_probes)
        sc.update(epoch=0, score_sec=time.time() - t0)
        (out_dir / "scores_ep0.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
        print(summary_line("ep0", sc), flush=True)
    with open(out_dir / "train_log.jsonl", "w", encoding="utf-8") as log:
        summary = train(model, ds, device, out_dir, args.epochs, args.lr, args.batch, args.accum, args.seed, save_epochs, log)
    (out_dir / "train_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    t1 = time.time()
    sc = score_run(model, ds, device, args.pool, args.seed)
    sc.update(train_summary=summary, epoch=args.epochs, score_sec=time.time() - t1, checkpoint="final")
    (out_dir / "scores_final.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
    print(summary_line("final", sc), flush=True)
    for e in save_epochs:
        ck = out_dir / f"ep{e}.pt"
        if not ck.exists() or e == args.epochs:
            if ck.exists():
                ck.unlink()
            continue
        model.load_state_dict(torch.load(ck, map_location=device)); model.eval()
        s2 = score_run(model, ds, device, args.pool, args.seed, args.snapshot_probes)
        s2.update(epoch=e, checkpoint=f"ep{e}")
        (out_dir / f"scores_ep{e}.json").write_text(json.dumps(s2, indent=1), encoding="utf-8")
        print(summary_line(f"ep{e}", s2), flush=True)
        ck.unlink()
    print(f"[hyena] done in {time.time() - t0:.0f}s -> {out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
