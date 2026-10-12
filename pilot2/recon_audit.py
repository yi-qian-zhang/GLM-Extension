"""Why a masked cell can hold a record completely and reconstruct none of it, measured.

    python -m pilot2.recon_audit --root outputs/human_mlm_long --tiers 1,4,16 --gpu 1

The 150-round masked cells are the paper's strongest result and its most attackable one: a planted
canary sits ~1.9 bits below the non-member control under the bidirectional scorer and is ranked
first against 100 candidates even after a single insertion, while greedy reconstruction of its
second half is exactly 0 % in all 30 cells and leaves 30-34 of 48 nucleotides wrong, which is the
non-member distance. A reviewer will say the extractor is broken. Two measurements answer that, and
neither exists in the saved runs:

1. THE CONDITIONAL THE RULERS ACTUALLY USE. `rank_probe` normalises bits/nt over the whole 96-nt
   canary, and `extract_prefix` reveals the first 48 of those for free. So a low canary surprise can
   coexist with a hopeless reconstruction simply because half the scored span is the half the
   attacker was given. This script measures the quantity extraction has to invert and nothing else:
   the teacher-forced chain-rule surprise of the 48 TARGET nucleotides given the revealed prefix,
   together with the fraction of decoding steps at which the true token is the argmax. All-48-exact
   requires every step, so top1_rate**n_steps is an upper bound on the extraction rate, and a cell
   with high target surprise cannot be rescued by any decoder, beam search included.

2. THE DECODE THAT WAS NEVER RUN. Both shipped protocols mask 8-16 target tokens at once, far
   outside the 15 % iid masking the model was trained on, while the surprise and recognition rulers
   read a conditional with ONE token masked. Iterated conditional modes closes that gap: initialise
   the target, then re-mask exactly one target token at a time with every other target token at its
   current value, sweeping to a fixed point. That is ~1/48 masking, inside the training
   distribution, and it is the strongest attack available to someone holding only the flanking
   sequence. If it still returns 0 %, the 0 % is a property of the model under every conditioning
   such an attacker can construct, and the paper can say so.

Reads only saved checkpoints, writes only new files, and does not touch pilot2/score.py, because
queue_1012a is mid-flight and must score every cell with the same code. Fold the ICM decoder into
`score.py:extract_infill` as `order="icm"` once that queue has finished.
"""
from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import PROBE_LEN, PROBE_OFFSET, WINDOW, Probe, decode, random_dna
from .model import Backbone
from .real_data import DATA_PATHS, build_real_dataset
from .score import _cover, _kmer_letters, extract_infill, extract_prefix
from .tokenizers import get_tokenizer
from .train import parse_objective, with_bos

try:                                     # synthetic cells only
    from .data import build_dataset
except ImportError:                      # pragma: no cover
    build_dataset = None

# accepts the plain cells and the --init_from / --lora_r ones, which run_pilot names <tok>_<obj>_ft_s<n>
RUN = re.compile(r"(?P<tok>char|\d+mer(?:sp)?)_(?P<obj>ar|mlm[0-9.]+)(?:_ft)?(?:_lora\d+)?_s(?P<seed>\d+)$")


def rebuild(d: Path, device, ckpt="final.pt"):
    """(model, tok, kind, ds, args) for one run directory, from its own args.json and checkpoint.

    Reads the backbone geometry out of args.json. Without that, every cell of queue_1012a -- which
    is the 59.9M (768/8/12) and 201M (1024/16/16) arm -- dies in load_state_dict.
    """
    a = json.loads((d / "args.json").read_text(encoding="utf-8"))
    kind, _ = parse_objective(a["objective"])
    tok = get_tokenizer(a["tokenizer"], 288)
    tiers = tuple(int(t) for t in str(a["tiers"]).split(","))
    if a.get("data", "synthetic") != "synthetic":
        ds = build_real_dataset(a.get("fasta") or DATA_PATHS[a["data"]], a["n_train"], a["n_val"],
                                a["n_test"], a["probes_per_tier"], tiers, a["n_nonmember"],
                                a["data_seed"], offset_mode=a["probe_offset"],
                                canary_npz=a.get("canary_npz"))
    else:
        ds = build_dataset(a["n_train"], a["n_val"], a["n_test"], a["probes_per_tier"], tiers,
                           a["n_nonmember"], a["data_seed"], offset_mode=a["probe_offset"],
                           enrich_k=a.get("enrich_k"), enrich_factor=a.get("enrich_factor", 1.0))
    kw = {k: v for k, v in (("d_model", a.get("d_model")), ("n_layers", a.get("n_layers")),
                            ("n_heads", a.get("n_heads")), ("d_ff", a.get("d_ff")),
                            ("emb_rank", a.get("emb_rank"))) if v}
    if a.get("pos_enc", "abs") != "abs":
        kw["pos_enc"] = a["pos_enc"]
    model = Backbone(tok.vocab_size, tok.n_tokens + 1, causal=(kind == "ar"), **kw).to(device)
    sd = torch.load(d / ckpt, map_location=device)
    sd = {k.replace("base_model.model.", "").replace(".base_layer", ""): v for k, v in sd.items()}
    model.load_state_dict(sd, strict=False) if any("lora" in k for k in sd) else model.load_state_dict(sd)
    model.eval()
    return model, tok, kind, ds, a


def _span(tok, offset, k_nt):
    start_nt, end_nt = offset + k_nt, offset + PROBE_LEN
    lo, hi = _cover(tok, start_nt, end_nt)
    return start_nt, end_nt, lo, hi, tok.nt_to_tok(lo), tok.nt_to_tok(hi)


def _allowed_fn(tok, win, start_nt, letters, content, device):
    """Content-token mask keeping the already-revealed letters of a partly-revealed token."""
    def allowed(pos):
        if letters is None:
            return None
        nt0 = pos if hasattr(tok, "fill_id") else pos * tok.k
        known = [(i, int(win[nt0 + i])) for i in range(tok.k) if nt0 + i < start_nt]
        if not known:
            return None
        m = torch.ones(len(content), dtype=torch.bool, device=device)
        for i, v in known:
            m &= letters[:, i] == v
        return m
    return allowed


@torch.no_grad()
def target_surprise(model, tok, kind, probe: Probe, host, device, k_nt=48, offset=PROBE_OFFSET):
    """Teacher-forced surprise of the TRUE target half under the extractor's own conditioning.

    Returns bits per TARGET nucleotide (not per canary nucleotide: the revealed half is excluded,
    which is the whole point), the fraction of steps whose argmax is the true token, and the upper
    bound that fraction places on all-48-exact extraction.
    """
    content = tok.content_ids.to(device)
    start_nt, end_nt, lo, hi, start, end = _span(tok, offset, k_nt)
    win = np.asarray(host).copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None
    allowed = _allowed_fn(tok, win, start_nt, letters, content, device)

    def step_logp(logits, pos):
        lc = logits[content]
        m = allowed(pos)
        if m is not None:
            lc = lc.masked_fill(~m, float("-inf"))
        lp = F.log_softmax(lc.float(), dim=-1) / math.log(2.0)
        true = int((content == xt[pos]).nonzero()[0, 0])
        return float(lp[true]), bool(int(lc.argmax()) == true)

    bits, hits = 0.0, []
    if kind == "ar":
        ctx = with_bos(xt[None, :start], tok.bos_id)
        for pos in range(start, end):
            if hasattr(tok, "is_fill") and tok.is_fill(pos):
                ctx = torch.cat([ctx, xt[pos].view(1, 1)], dim=1)
                continue
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(ctx)[0, -1].float()
            lp, hit = step_logp(logits, pos)
            bits -= lp
            hits.append(hit)
            ctx = torch.cat([ctx, xt[pos].view(1, 1)], dim=1)   # teacher forcing
    else:
        cur = xt.clone()
        cur[start:] = tok.mask_id
        xb = with_bos(cur[None], tok.bos_id)
        for pos in range(start, end):
            if hasattr(tok, "is_fill") and tok.is_fill(pos):
                xb[0, pos + 1] = xt[pos]
                continue
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0, pos + 1].float()
            lp, hit = step_logp(logits, pos)
            bits -= lp
            hits.append(hit)
            xb[0, pos + 1] = xt[pos]                            # teacher forcing
    n = max(1, len(hits))
    rate = float(np.mean(hits))
    return {"target_bits_per_nt": bits / (end_nt - start_nt), "target_bits_total": bits,
            "top1_rate": rate, "n_steps": n, "exact_upper_bound": rate ** n}


@torch.no_grad()
def extract_icm(model, tok, kind, probe: Probe, host, device, k_nt=48, offset=PROBE_OFFSET,
                sweeps: int = 6, init: str = "confidence"):
    """Iterated conditional modes: re-mask ONE target token at a time, sweep to a fixed point.

    The conditional used here (1 of ~48 tokens masked, the rest at their current values) is the one
    the model was trained on and the one the surprise and recognition rulers read, which neither
    shipped extraction protocol ever enters. Returns None for causal models.
    """
    if kind == "ar":
        return None
    content = tok.content_ids.to(device)
    start_nt, end_nt, lo, hi, start, end = _span(tok, offset, k_nt)
    win = np.asarray(host).copy()
    win[offset:offset + PROBE_LEN] = probe.seq
    xt = torch.from_numpy(tok.encode(win[None]))[0].to(device)
    truth_nt = torch.from_numpy(win[start_nt:end_nt]).to(device)
    letters = _kmer_letters(tok, device) if lo < start_nt else None
    allowed = _allowed_fn(tok, win, start_nt, letters, content, device)

    # the shipped edge-conditioned decode, reported beside ICM so the gain is attributable
    seed_pred = extract_infill(model, tok, kind, probe, host, device, k_nt=k_nt, offset=offset,
                               order=init)
    cur = xt.clone()
    cur[start:end] = tok.mask_id
    xb = with_bos(cur[None], tok.bos_id)
    todo = []
    for pos in range(start, end):
        if hasattr(tok, "is_fill") and tok.is_fill(pos):
            xb[0, pos + 1] = tok.fill_id
        else:
            todo.append(pos)
    with torch.autocast("cuda", dtype=torch.bfloat16):   # all target slots at once, then sweep
        logits = model(xb)[0].float()
    for pos in todo:
        lc = logits[pos + 1][content]
        m = allowed(pos)
        if m is not None:
            lc = lc.masked_fill(~m, float("-inf"))
        xb[0, pos + 1] = content[int(lc.argmax())]

    n_sweeps = 0
    for _ in range(sweeps):
        changed = 0
        n_sweeps += 1
        for pos in todo:
            keep = xb[0, pos + 1].clone()
            xb[0, pos + 1] = tok.mask_id
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = model(xb)[0, pos + 1].float()
            lc = logits[content]
            m = allowed(pos)
            if m is not None:
                lc = lc.masked_fill(~m, float("-inf"))
            new = content[int(lc.argmax())]
            xb[0, pos + 1] = new
            changed += int(new.item() != keep.item())
        if changed == 0:
            break
    pred_tok = xb[0, start + 1:end + 1]
    pred_nt = tok.decode_t(pred_tok[None])[0][start_nt - lo:end_nt - lo]
    ham = int((pred_nt != truth_nt).sum())
    return {"protocol": f"icm-{init}", "sweeps_used": n_sweeps, "k_revealed_nt": k_nt,
            "offset": int(offset), "n_generated_nt": int(end_nt - start_nt),
            "exact": bool(ham == 0), "hamming_nt": ham,
            "seed_exact": bool(seed_pred["exact"]), "seed_hamming_nt": int(seed_pred["hamming_nt"]),
            "pred_nt": decode(pred_nt.cpu().numpy()), "truth_nt": decode(truth_nt.cpu().numpy())}


def fresh_views(ds, seed, pool_size):
    """The same fresh hosts and offsets score_run uses, so the control is phase-matched.

    score_run draws the candidate pool from this generator first when the canaries are synthetic, so
    the pool size has to be replayed or every fresh host would differ from the one actually scored.
    """
    rng = np.random.default_rng(10_000 + seed)
    real_pool = getattr(ds, "pool_seqs", None)
    if real_pool is None:
        random_dna(rng, pool_size, PROBE_LEN)                            # keep the rng in step
    real_hosts = getattr(ds, "fresh_hosts", None)
    hosts = {p.probe_id: (random_dna(rng, 1, WINDOW)[0] if real_hosts is None
                          else real_hosts[i % len(real_hosts)].copy())
             for i, p in enumerate(ds.probes)}
    off_rng = np.random.default_rng(20_000 + seed)
    offs = {p.probe_id: int(off_rng.integers(0, WINDOW - PROBE_LEN + 1)) for p in ds.probes}
    return hosts, offs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", nargs="+", required=True)
    ap.add_argument("--gpu", type=int, default=0)
    ap.add_argument("--tiers", default="1,4,16")
    ap.add_argument("--max_probes", type=int, default=25, help="per tier")
    ap.add_argument("--sweeps", type=int, default=6)
    ap.add_argument("--ckpt", default="final.pt")
    ap.add_argument("--name", default="recon_audit")
    ap.add_argument("--no_icm", action="store_true", help="target surprise only, no ICM decode")
    args = ap.parse_args(argv)
    device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() else "cpu")
    tiers = [int(t) for t in args.tiers.split(",")]

    rows = []
    for root in args.root:
        rd = Path(root)
        dirs = [rd] if (rd / "args.json").exists() else sorted(p for p in rd.iterdir() if p.is_dir())
        for d in dirs:
            if not ((d / "args.json").exists() and (d / args.ckpt).exists() and RUN.fullmatch(d.name)):
                continue
            model, tok, kind, ds, a = rebuild(d, device, args.ckpt)
            fh, fo = fresh_views(ds, a["seed"], a.get("pool", 500))
            out = {"run": d.name, "ckpt": args.ckpt, "data": a.get("data", "synthetic"),
                   "objective": a["objective"], "tokenizer": a["tokenizer"], "seed": a["seed"],
                   "d_model": a.get("d_model"), "n_layers": a.get("n_layers"), "cells": []}
            per = defaultdict(lambda: defaultdict(list))
            for tier in tiers + [0]:
                ps = [p for p in ds.probes if p.repetitions == tier][:args.max_probes]
                for p in ps:
                    if tier > 0:
                        host, off, hname = ds.train[p.host_rows[0]], p.offsets[0], "train"
                    else:
                        host, off, hname = fh[p.probe_id], fo[p.probe_id], "fresh"
                    ts = target_surprise(model, tok, kind, p, host, device, offset=off)
                    pre = extract_prefix(model, tok, kind, p, host, device, offset=off)
                    icm = (None if args.no_icm else
                           extract_icm(model, tok, kind, p, host, device, offset=off,
                                       sweeps=args.sweeps))
                    v = per[tier]
                    v["tgt_bits"].append(ts["target_bits_per_nt"])
                    v["top1"].append(ts["top1_rate"])
                    v["bound"].append(ts["exact_upper_bound"])
                    v["pre_exact"].append(float(pre["exact"]))
                    v["pre_ham"].append(pre["hamming_nt"])
                    if icm:
                        v["icm_exact"].append(float(icm["exact"]))
                        v["icm_ham"].append(icm["hamming_nt"])
                        v["seed_exact"].append(float(icm["seed_exact"]))
                        v["seed_ham"].append(icm["seed_hamming_nt"])
                    out["cells"].append({"tier": tier, "host": hname, "probe_id": p.probe_id,
                                         "target": ts, "prefix": pre, "icm": icm})
            (d / f"{args.name}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
            for t in sorted(per, reverse=True):
                m = lambda k: float(np.mean(per[t][k])) if per[t][k] else float("nan")
                rows.append(dict(run=d.name, data=out["data"], tok=a["tokenizer"], obj=a["objective"],
                                 seed=a["seed"], tier=t, n=len(per[t]["tgt_bits"]),
                                 tgt_bits=m("tgt_bits"), top1=m("top1"), bound=m("bound"),
                                 pre_exact=m("pre_exact"), pre_ham=m("pre_ham"),
                                 icm_exact=m("icm_exact"), icm_ham=m("icm_ham"),
                                 seed_exact=m("seed_exact"), seed_ham=m("seed_ham")))
                r = rows[-1]
                print(f"  {d.name:28s} r={t:<3d} n={r['n']:3d} | target {r['tgt_bits']:5.3f} b/nt "
                      f"top1 {r['top1']:.2f} bound {r['bound']:.3f} | prefix {100*r['pre_exact']:5.1f}% "
                      f"(ham {r['pre_ham']:4.1f}) | icm {100*r['icm_exact']:5.1f}% "
                      f"(ham {r['icm_ham']:4.1f}, seed {100*r['seed_exact']:5.1f}%)", flush=True)
            del model
            torch.cuda.empty_cache()

    if not rows:
        print("no runs with a checkpoint under", args.root)
        return 1
    md = [f"# Reconstruction audit — {args.name}", "",
          "`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed "
          "48, in bits per target nucleotide: the conditional extraction has to invert, with the "
          "revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true "
          "token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a "
          "cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token "
          "at a time and sweeps to a fixed point, which is the in-distribution conditional the "
          "surprise and recognition rulers read and neither shipped protocol enters; `seed` is the "
          "confidence-ordered edge-conditioned decode it starts from.", "",
          "| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['run']} | {r['data']} | {r['tok']} | {r['obj']} | r={r['tier']} | {r['n']} | "
                  f"{r['tgt_bits']:.3f} | {r['top1']:.2f} | {r['bound']:.3f} | "
                  f"{100*r['pre_exact']:.0f}% | {r['pre_ham']:.1f} | **{100*r['icm_exact']:.0f}%** | "
                  f"{r['icm_ham']:.1f} |")
    mem = [r for r in rows if r["tier"] > 0]
    non = [r for r in rows if r["tier"] == 0]
    if mem and non:
        md += ["", f"Members: target surprise {np.mean([r['tgt_bits'] for r in mem]):.3f} b/nt against "
                   f"{np.mean([r['tgt_bits'] for r in non]):.3f} for the matched non-member control; "
                   f"ICM extraction at worst {100*max(r['icm_exact'] for r in mem):.0f}%."]
    p = Path(args.root[0]) / f"{args.name}.md"
    p.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[-2:]))
    print(f"-> {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
