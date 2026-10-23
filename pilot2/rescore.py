"""Score a saved checkpoint again, without retraining it.

    python -m pilot2.rescore --root outputs/bpe_human/dnabert2bpe_human_s0 \
        --ckpt ep120.pt --name scores_ep120_rb --gpu 0

WHY. Recognition -- whether the model ranks a planted record first against a pool of real
rare-variant segments -- is produced by the scoring pass, which the three released-model
scripts run inline right after training. There was no way to ask for it again on an existing
checkpoint, so every number of that kind dated from the day its run finished. That became a
problem when the host's floating-point behaviour changed across a reboot (notes 3.58d): the
extraction cells could be re-measured on one basis with the decoders, but the recognition
cells could not be re-measured at all.

This rebuilds the run from its own `args.json` -- the same corpus, the same data seed, the
same probes, the same canary file -- loads one checkpoint and runs that family's `score_run`.
Nothing is retrained and nothing already on disk is overwritten unless `--name` says so.

The point is not only to refresh numbers. Running it against a checkpoint whose old scores
still exist answers a question the paper has to answer anyway: how much of a reported rate is
the measurement and how much is the machine it ran on.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch

from .real_data import DATA_PATHS, build_real_dataset
from .data import build_dataset


def _dataset(a: dict):
    """The dataset the run was built on, from its own recorded arguments."""
    tiers = tuple(int(t) for t in str(a.get("tiers", "1,4,16")).split(",") if t)
    n_val = a.get("n_val", 200)
    n_test = a.get("n_test", 200)
    common = (a["n_train"], n_val, n_test, a["probes_per_tier"], tiers,
              a["n_nonmember"], a.get("data_seed", 1234))
    if a.get("data", "synthetic") != "synthetic":
        return build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], *common,
                                  offset_mode=a.get("probe_offset", "random"),
                                  canary_npz=a.get("canary_npz"))
    return build_dataset(*common, offset_mode=a.get("probe_offset", "random"))


def _score(a: dict, d: Path, ckpt: str, device, pool: int, probes: int | None):
    """(scores, family) for one checkpoint, dispatched the way utility_at_leak dispatches."""
    obj = a.get("objective", "mlm")
    sd = torch.load(d / ckpt, map_location=device)
    ds = _dataset(a)

    if "size" in a:                                   # Nucleotide Transformer
        # NT scores through pilot2.score.score_run, whose signature differs from the two
        # family-specific ones below: it takes the tokenizer kind and an offset mode, and
        # has no probes_per_tier.
        from . import nt as ntmod
        from .score import score_run as score_nt
        model, kind = ntmod.load(a["size"], obj == "causal", device)
        model.hf.load_state_dict(sd)
        model.eval()
        voc = ntmod.NTVocab(Path(ntmod.ROOT) / ntmod.SIZES[a["size"]]).to(device)
        return score_nt(model, voc, kind, ds, device, pool_size=pool, seed=a["seed"],
                        floor_n=a.get("floor_n", 500),
                        offset_mode=a.get("probe_offset", "random")), "nt"

    if a.get("k"):                                    # DNABERT, overlapping k-mers
        from .dnabert import load_model, score_run
        model, voc = load_model(int(a["k"]), device)
        model.load_state_dict(sd)
        model.eval()
        return score_run(model, voc, ds, device, pool, a["seed"], a.get("stride", 1),
                         probes, objective=obj), "dnabert"

    from .dnabert2 import load_model, score_run      # DNABERT-2, BPE
    model, voc = load_model(device, causal=obj == "causal")
    model.load_state_dict(sd)
    model.eval()
    return score_run(model, voc, ds, device, pool, a["seed"], probes, objective=obj), "bpe"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="a finished run directory")
    ap.add_argument("--ckpt", required=True, help="checkpoint file inside --root")
    ap.add_argument("--name", default=None, help="output stem (default scores_<ckpt>_rescored)")
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--pool", type=int, default=None, help="candidate pool; default the run's own")
    ap.add_argument("--probes", type=int, default=None, help="probes per tier; default all")
    ap.add_argument("--compare", default=None,
                    help="an existing scores_*.json to diff against, to show how much of a "
                         "rate is the measurement and how much is the machine")
    args = ap.parse_args(argv)

    d = Path(args.root)
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    pool = args.pool if args.pool is not None else a.get("pool", 500)

    t0 = time.time()
    sc, family = _score(a, d, args.ckpt, device, pool, args.probes)
    sc.update(checkpoint=args.ckpt, score_sec=time.time() - t0, rescored=True)
    out = d / f"{args.name or ('scores_' + Path(args.ckpt).stem + '_rescored')}.json"
    out.write_text(json.dumps(sc, indent=1), encoding="utf-8")
    floor = sc["floors"][0]["bits_per_nt_mean"]
    print(f"[{family}] {d.name} {args.ckpt} floor {floor:.3f} ({sc['score_sec']:.0f}s) -> {out.name}",
          flush=True)

    if args.compare:
        old = json.loads((d / args.compare).read_text(encoding="utf-8"))
        print(f"\n{'':22s} {'old':>10s} {'new':>10s} {'delta':>10s}")
        of = old["floors"][0]["bits_per_nt_mean"]
        print(f"{'held-out bits/nt':22s} {of:10.4f} {floor:10.4f} {floor - of:+10.4f}")
        for tier in sorted({p.get("repetitions") for p in old.get("probes", [])}, reverse=True):
            for label, fn in (("rank-1", lambda p, k: 1.0 * (p["ranks"][k]["rank"] == 1)),
                              ("verbatim", lambda p, k: 1.0 * p["extract"][k.split("/")[-1]]["exact"])):
                def rate(doc):
                    ps = [(p, k) for p in doc.get("probes", [])
                          if p.get("repetitions") == tier
                          for k in p.get("ranks", {}) if k.endswith("/train")]
                    try:
                        return sum(fn(p, k) for p, k in ps) / len(ps) if ps else float("nan")
                    except KeyError:
                        return float("nan")
                o, n = rate(old), rate(sc)
                if o == o or n == n:
                    print(f"{f'r={tier} {label}':22s} {o:10.3f} {n:10.3f} {n - o:+10.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
