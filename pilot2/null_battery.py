"""E0 null battery: what does every metric read when there is nothing to find?

(a) untrained model      -- random init, never saw the data. Probe ranks must be
                            uniform on 1..n+1; verifies the chance floor formula
                            P(rank <= k) = k/(n+1) and that scorers do not leak.
(b) blind baseline       -- no model at all. Logistic regression on surface
                            statistics of the probe sequence (GC, k-mer counts)
                            to separate member from non-member probes. By
                            construction (all probes iid uniform) this must be
                            at chance; reported so that a reviewer can see it.

    python -m pilot2.null_battery --tokenizer char --gpu 0 --out outputs/null
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch

from .data import PROBE_LEN, WINDOW, build_dataset
from .model import Backbone
from .score import SCORERS_FOR, heldout_floor, rank_probe
from .tokenizers import get_tokenizer


def ks_uniform(ranks: np.ndarray, n_pool: int) -> float:
    """KS statistic of ranks against Uniform{1..n_pool+1}."""
    x = np.sort(ranks) / (n_pool + 1)
    e = np.arange(1, len(x) + 1) / len(x)
    return float(max(np.max(e - x), np.max(x - (e - 1 / len(x)))))


def untrained(args, ds, tok, device):
    out = {}
    for kind in ("ar", "mlm"):
        torch.manual_seed(args.seed)
        model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar")).to(device).eval()
        rng = np.random.default_rng(777)
        pool = (rng.integers(1, 5, size=(args.pool, PROBE_LEN))).astype(np.int64)
        fresh = {p.probe_id: rng.integers(1, 5, size=WINDOW).astype(np.int64) for p in ds.probes}
        res = {"floors": [heldout_floor(model, tok, sc, ds.test, device, args.floor_n) for sc in SCORERS_FOR[kind]],
               "scorers": {}}
        for sc in SCORERS_FOR[kind]:
            ranks = np.array([rank_probe(model, tok, sc, p, fresh[p.probe_id], pool, device)["rank"] for p in ds.probes])
            res["scorers"][sc] = {
                "n_probes": int(len(ranks)), "n_pool": args.pool,
                "rank_1_rate": float(np.mean(ranks == 1)), "expected_rank_1_rate": 1 / (args.pool + 1),
                "rank_le_1pct_rate": float(np.mean(ranks <= max(1, args.pool // 100))),
                "median_rank": float(np.median(ranks)), "expected_median": (args.pool + 1) / 2,
                "ks_vs_uniform": ks_uniform(ranks, args.pool),
                "ks_crit_05": float(1.36 / np.sqrt(len(ranks))),
            }
        out[kind] = res
        for sc, r in res["scorers"].items():
            flag = "uniform OK" if r["ks_vs_uniform"] < r["ks_crit_05"] else "NOT UNIFORM"
            print(f"[untrained/{kind}/{sc}] median rank {r['median_rank']:.0f} (exp {r['expected_median']:.0f}), "
                  f"rank-1 {r['rank_1_rate']:.3f} (exp {r['expected_rank_1_rate']:.3f}), KS {r['ks_vs_uniform']:.3f} "
                  f"< {r['ks_crit_05']:.3f}? {flag}", flush=True)
        for f in res["floors"]:
            print(f"[untrained/{kind}/{f['scorer']}] floor {f['bits_per_nt_mean']:.3f} bits/nt "
                  f"(random-init model; >= 2.0 expected, typically ~log2(vocab)/k)", flush=True)
    return out


def blind_baseline(ds, k_max: int = 3, seed: int = 0):
    """Surface-statistics classifier, member vs non-member probes, 5-fold CV."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    def feats(seq):
        f = [np.mean((seq == 2) | (seq == 3))]  # GC
        for k in range(1, k_max + 1):
            counts = np.zeros(4 ** k)
            for i in range(len(seq) - k + 1):
                idx = 0
                for j in range(k):
                    idx = idx * 4 + (seq[i + j] - 1)
                counts[idx] += 1
            f.extend(counts / counts.sum())
        return f

    X = np.array([feats(p.seq) for p in ds.probes])
    y = np.array([1 if p.repetitions > 0 else 0 for p in ds.probes])
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    auc = cross_val_score(LogisticRegression(max_iter=2000, C=1.0), X, y, cv=cv, scoring="roc_auc")
    res = {"n_member": int(y.sum()), "n_nonmember": int((1 - y).sum()), "n_features": int(X.shape[1]),
           "cv_auc_mean": float(auc.mean()), "cv_auc_std": float(auc.std()), "folds": auc.tolist()}
    print(f"[blind] member vs non-member from surface stats: AUC {res['cv_auc_mean']:.3f} ± {res['cv_auc_std']:.3f} "
          f"(chance 0.5; must be ~0.5 by construction)", flush=True)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenizer", default="char")
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--out", default="outputs/null")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--pool", type=int, default=200)
    ap.add_argument("--floor_n", type=int, default=200)
    ap.add_argument("--n_train", type=int, default=5000)
    ap.add_argument("--probes_per_tier", type=int, default=20)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--n_nonmember", type=int, default=40)
    ap.add_argument("--data_seed", type=int, default=1234)
    args = ap.parse_args(argv)
    device = f"cuda:{args.gpu}"
    torch.cuda.set_device(args.gpu)
    tok = get_tokenizer(args.tokenizer, WINDOW)
    ds = build_dataset(args.n_train, 500, 500, args.probes_per_tier,
                       tuple(int(t) for t in args.tiers.split(",")), args.n_nonmember, args.data_seed)
    out = {"tokenizer": tok.name, "untrained": untrained(args, ds, tok, device), "blind": blind_baseline(ds)}
    od = Path(args.out); od.mkdir(parents=True, exist_ok=True)
    (od / f"null_{tok.name}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"-> {od / f'null_{tok.name}.json'}")


if __name__ == "__main__":
    main()
