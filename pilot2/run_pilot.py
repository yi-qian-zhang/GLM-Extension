"""Run one (tokenizer, objective, seed) cell end to end.

    python -m pilot2.run_pilot --tokenizer 3mer --objective ar --seed 0 --gpu 0
    python -m pilot2.run_pilot --smoke --tokenizer 6mer --objective mlm@0.15

Run name: <tokenizer>_<objective>_s<seed>, under --out.
Memorization metrics are read from final.pt unless --checkpoint best.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import torch

from .data import WINDOW, build_dataset
from .model import Backbone
from .score import score_run
from .tokenizers import get_tokenizer
from .train import parse_objective, train_cell


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenizer", default="char", help="char | 3mer | 6mer")
    ap.add_argument("--objective", default="ar")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/pilot2")
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--n_val", type=int, default=500)
    ap.add_argument("--n_test", type=int, default=500)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    ap.add_argument("--epochs", type=int, default=30)
    ap.add_argument("--max_steps", type=int, default=None, help="cap optimizer steps (fixed-supervised-token budget)")
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--pool", type=int, default=500)
    ap.add_argument("--floor_n", type=int, default=500)
    ap.add_argument("--checkpoint", default="final", choices=["best", "final"])
    ap.add_argument("--score_only", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--save_epochs", default="", help="comma list of 1-indexed epochs to snapshot, e.g. 1,2,5,10")
    ap.add_argument("--score_snapshots", action="store_true", help="also score every saved ep<N>.pt -> scores_ep<N>.json")
    ap.add_argument("--d_ff", type=int, default=None, help="capacity control: feed-forward width (default 4*d)")
    ap.add_argument("--emb_rank", type=int, default=None, help="capacity control: factorized tied embedding rank")
    ap.add_argument("--emb_lr_mult", type=float, default=1.0, help="learning-rate multiplier for the token embedding only")
    ap.add_argument("--keep_snapshots", action="store_true", help="keep ep<N>.pt after scoring (default: delete; disk is shared)")
    args = ap.parse_args(argv)
    if args.smoke:
        args.n_train, args.n_val, args.n_test = 400, 64, 64
        args.probes_per_tier, args.n_nonmember = 3, 3
        args.epochs, args.pool, args.floor_n = 2, 30, 64
        args.out = os.path.join(args.out, "smoke")

    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    kind, _ = parse_objective(args.objective)
    tok = get_tokenizer(args.tokenizer, WINDOW)
    name = f"{tok.name}_{args.objective.replace('@', '')}_s{args.seed}"
    out_dir = Path(args.out) / name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "args.json").write_text(json.dumps(vars(args), indent=1), encoding="utf-8")

    t0 = time.time()
    ds = build_dataset(args.n_train, args.n_val, args.n_test, args.probes_per_tier,
                       tuple(int(t) for t in args.tiers.split(",")), args.n_nonmember, args.data_seed)
    ds.save_meta(out_dir / "data_meta.json")
    print(f"[{name}] tokenizer {tok.name}: k={tok.k}, vocab={tok.vocab_size}, {tok.n_tokens} tok/window; "
          f"train={ds.train.shape} probes={len(ds.probes)}", flush=True)

    model_kw = {k: v for k, v in (("d_ff", args.d_ff), ("emb_rank", args.emb_rank)) if v}
    if args.score_only:
        model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), **model_kw).to(device)
        summary = json.loads((out_dir / "train_summary.json").read_text(encoding="utf-8"))
    else:
        model, summary = train_cell(ds, tok, args.objective, args.seed, out_dir, device,
                                    epochs=args.epochs, batch=args.batch, lr=args.lr, max_steps=args.max_steps,
                                    save_epochs=[int(e) for e in args.save_epochs.split(',') if e], model_kw=model_kw, emb_lr_mult=args.emb_lr_mult)
        print(f"[{name}] trained {summary['n_params']/1e6:.2f}M ({summary['n_params_non_embedding']/1e6:.2f}M non-emb), "
              f"{summary['steps']} steps, {summary['supervised_tokens_seen']/1e6:.1f}M supervised tokens, "
              f"{summary['total_train_sec']:.0f}s", flush=True)
    if args.score_only or args.checkpoint != "best":
        model.load_state_dict(torch.load(out_dir / f"{args.checkpoint}.pt", map_location=device))
    model.eval()

    t1 = time.time()
    scores = score_run(model, tok, kind, ds, device, pool_size=args.pool, seed=args.seed, floor_n=args.floor_n)
    scores.update(train_summary=summary, score_sec=time.time() - t1, total_sec=time.time() - t0,
                  checkpoint=args.checkpoint)
    fname = "scores.json" if args.checkpoint == "best" else "scores_final.json"
    (out_dir / fname).write_text(json.dumps(scores, indent=1), encoding="utf-8")
    for f in scores["floors"]:
        print(f"[{name}] floor {f['scorer']:6s}: {f['bits_per_nt_mean']:.4f} bits/nt "
              f"{'OK' if f['floor_ok'] else 'VIOLATION'}", flush=True)
    print(f"[{name}] done in {scores['total_sec']:.0f}s -> {out_dir/fname}", flush=True)

    if args.score_snapshots:
        for e in sorted(int(x) for x in args.save_epochs.split(",") if x):
            ck = out_dir / f"ep{e}.pt"
            if not ck.exists():
                continue
            model.load_state_dict(torch.load(ck, map_location=device)); model.eval()
            t2 = time.time()
            sc = score_run(model, tok, kind, ds, device, pool_size=args.pool, seed=args.seed, floor_n=args.floor_n)
            sc.update(train_summary=summary, score_sec=time.time() - t2, checkpoint=f"ep{e}", epoch=e)
            (out_dir / f"scores_ep{e}.json").write_text(json.dumps(sc, indent=1), encoding="utf-8")
            fl = sc["floors"][0]["bits_per_nt_mean"]
            print(f"[{name}] snapshot ep{e}: floor {fl:.4f}  ({sc['score_sec']:.0f}s)", flush=True)
            if not args.keep_snapshots:
                ck.unlink()


if __name__ == "__main__":
    sys.exit(main())
