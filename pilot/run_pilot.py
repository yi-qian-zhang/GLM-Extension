"""Run one pilot cell end to end: build data -> train -> score -> scores.json.

    python -m pilot.run_pilot --objective ar      --seed 0 --gpu 0
    python -m pilot.run_pilot --objective mlm@0.15 --seed 0 --gpu 1
    python -m pilot.run_pilot --smoke                          # 2-minute sanity pass

Outputs land in outputs/pilot/<objective>_s<seed>/ on the machine that runs it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch

from .data import build_dataset
from .score import score_run
from .train import parse_objective, train_cell


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--objective", default="ar", help="ar | mlm@0.15 | mlm@0.30 ...")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/pilot")
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--n_val", type=int, default=500)
    ap.add_argument("--n_test", type=int, default=500)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--pool", type=int, default=500)
    ap.add_argument("--floor_n", type=int, default=500)
    ap.add_argument("--smoke", action="store_true", help="tiny settings to shake out bugs")
    args = ap.parse_args(argv)

    if args.smoke:
        args.n_train, args.n_val, args.n_test = 400, 64, 64
        args.probes_per_tier, args.n_nonmember = 3, 3
        args.epochs, args.pool, args.floor_n = 2, 30, 64
        args.out = os.path.join(args.out, "smoke")

    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    kind, _ = parse_objective(args.objective)
    name = f"{args.objective.replace('@', '')}_s{args.seed}"
    out_dir = Path(args.out) / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")

    t0 = time.time()
    ds = build_dataset(args.n_train, args.n_val, args.n_test, args.probes_per_tier,
                       tuple(int(t) for t in args.tiers.split(",")), args.n_nonmember, args.data_seed)
    ds.save_meta(out_dir / "data_meta.json")
    print(f"[{name}] data: train={ds.train.shape} val={ds.val.shape} test={ds.test.shape} "
          f"probes={len(ds.probes)} ({len(ds.members())} member, {len(ds.nonmembers())} non-member)", flush=True)

    model, summary = train_cell(ds, args.objective, args.seed, out_dir, device,
                                epochs=args.epochs, batch=args.batch, lr=args.lr)
    print(f"[{name}] trained: {summary['n_params']/1e6:.2f}M params, best val "
          f"{summary['best_val_loss_nats']:.4f} nats @ epoch {summary['best_epoch']}, "
          f"{summary['total_train_sec']:.0f}s", flush=True)

    t1 = time.time()
    scores = score_run(model, kind, ds, device, pool_size=args.pool, seed=args.seed, floor_n=args.floor_n)
    scores["train_summary"] = summary
    scores["score_sec"] = time.time() - t1
    scores["total_sec"] = time.time() - t0
    (out_dir / "scores.json").write_text(json.dumps(scores, indent=1), encoding="utf-8")
    for f in scores["floors"]:
        flag = "OK " if f["floor_ok"] else "VIOLATION"
        print(f"[{name}] floor {f['scorer']:6s}: {f['bits_per_nt_mean']:.4f} bits/nt "
              f"(ppl {f['perplexity']:.4f})  {flag}", flush=True)
    print(f"[{name}] done in {scores['total_sec']:.0f}s -> {out_dir/'scores.json'}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
