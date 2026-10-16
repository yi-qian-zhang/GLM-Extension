"""Downstream task accuracy at the checkpoints where the leak begins, on released weights.

    python -m pilot2.utility_at_leak --root outputs/bpe_human/dnabert2bpe_human_s0 --gpu 2

WHY. Every statement in this paper about what a leak costs is in held-out bits per nucleotide: a
released DNABERT-2 reproduces 20 % of real rare-variant haplotypes at **+0.033 bits** past its own
optimum, a released NT recovers records at **+0.028**. Nobody chooses a checkpoint in bits. The
advisor asked for a utility metric beside memorisation on 2 Oct and the paper still does not have
one attached to the leakage numbers, which means the sentence a practitioner needs -- "the model
that leaks is still as good at its job as the one that does not" -- is unsupported.

This reads each saved checkpoint of a released-model run and reports, beside its held-out loss and
its memorisation numbers, the GUE downstream metric the DNABERT-2 paper itself uses: a linear probe
on frozen mean-pooled states and a short fine-tune, both scored by MCC on the task's held-out test
split. If MCC is flat from the utility optimum through the point where reproduction starts, the
leak is free in the only currency a practitioner spends.

Only the human runs are meaningful here: GUE has no bacterial task, so an E. coli memorisation cell
has no downstream counterpart. Nothing is retrained and nothing is overwritten.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import torch

from . import downstream


def _load(d: Path, ckpt: str, device):
    """(kind, model, voc, causal) for a released-model run directory."""
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    if "size" in a:                                     # Nucleotide Transformer
        from . import nt as ntmod
        model, _ = ntmod.load(a["size"], False, device)
        model.hf.load_state_dict(torch.load(d / ckpt, map_location=device))
        voc = ntmod.NTVocab(Path(ntmod.ROOT) / ntmod.SIZES[a["size"]]).to(device)
        model.eval()
        return "nt", model, voc, False, a
    if "k" in a and a.get("k"):                         # DNABERT, overlapping k-mers
        from .dnabert import load_model as dnabert_load
        model, voc = dnabert_load(int(a["k"]), device)
        model.load_state_dict(torch.load(d / ckpt, map_location=device))
        model.eval()
        return "dnabert", model, voc, a.get("objective") == "causal", a
    from .dnabert2 import load_model as bpe_load        # DNABERT-2, BPE
    model, voc = bpe_load(device, causal=(a.get("objective") == "causal"))
    model.load_state_dict(torch.load(d / ckpt, map_location=device))
    model.eval()
    return "bpe", model, voc, a.get("objective") == "causal", a


def _memo(d: Path, ep):
    """held-out loss and the memorisation numbers already scored at this epoch, if present."""
    f = d / (f"scores_ep{ep}.json" if ep != "final" else "scores_final.json")
    if not f.exists():
        return {}
    s = json.loads(f.read_text(encoding="utf-8"))
    out = {"floor": s["floors"][0]["bits_per_nt_mean"]}
    for tier in (16, 1):
        ps = [p for p in s["probes"] if p.get("repetitions") == tier]
        ps = [(p, k) for p in ps for k in p.get("ranks", {}) if k.endswith("/train")]
        if not ps:
            continue
        m = lambda g: sum(g(p, k) for p, k in ps) / len(ps)
        out[f"r{tier}_recognition"] = m(lambda p, k: 1.0 * (p["ranks"][k]["rank"] == 1))
        out[f"r{tier}_verbatim"] = m(lambda p, k: 1.0 * p["extract"]["train"]["exact"])
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--tasks", default="prom_300_all")
    ap.add_argument("--n_train", type=int, default=20_000)
    ap.add_argument("--no_finetune", action="store_true",
                    help="linear probe only; the fine-tune copies the model and is the slow half")
    ap.add_argument("--name", default="utility_at_leak")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    tasks = tuple(t for t in args.tasks.split(",") if t)

    rows = []
    for root in args.root:
        d = Path(root)
        cks = sorted((p.name for p in d.glob("ckpt_ep*.pt")), key=lambda s: int(re.search(r"\d+", s).group())) \
            or sorted((p.name for p in d.glob("ep*.pt")), key=lambda s: int(re.search(r"\d+", s).group()))
        if (d / "final.pt").exists():
            cks.append("final.pt")
        if not cks:
            print("no checkpoints under", d)
            continue
        for ck in cks:
            ep = re.search(r"(\d+)", ck).group(1) if ck != "final.pt" else "final"
            kind, model, voc, causal, a = _load(d, ck, device)
            ds = downstream.evaluate(kind, model, voc, device, causal=causal, tasks=tasks,
                                     n_train=args.n_train, finetune=not args.no_finetune)
            row = {"run": d.name, "ckpt": ck, "epoch": ep, **_memo(d, ep), "downstream": ds}
            rows.append(row)
            mem = {k: v for k, v in row.items() if k.startswith("r") or k == "floor"}
            print(f"  {d.name:26s} {ck:14s} floor {row.get('floor', float('nan')):.3f} | "
                  f"r16 vb {row.get('r16_verbatim', float('nan')):.2f} rec {row.get('r16_recognition', float('nan')):.2f} | "
                  f"r1 rec {row.get('r1_recognition', float('nan')):.2f} | downstream {json.dumps(ds)[:170]}",
                  flush=True)
            del model
            torch.cuda.empty_cache()
        (d / f"{args.name}.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")

    if rows:
        out = Path(args.root[0]) / f"{args.name}.json"
        out.write_text(json.dumps(rows, indent=1), encoding="utf-8")
        print(f"-> {out}")
    return 0 if rows else 1


if __name__ == "__main__":
    raise SystemExit(main())
