"""Downstream utility probe: GUE human promoter detection (prom_300_all), DNABERT's own benchmark.

Called at every scored snapshot of a real-model run (`--downstream` in dnabert.py / dnabert2.py / hyena.py):
  * linear probe  — frozen mean-pooled last hidden states -> logistic regression (sklearn); cheap, measures representation quality
  * fine-tune     — DNABERT-2 recipe scaled down: deepcopy of the model + linear head on mean-pooled states, AdamW lr 3e-5,
                    batch 32, 2 epochs on N_TRAIN = 20k labelled sequences (the paper: 3 epochs on all 47k); the copy is discarded
Both report accuracy and MCC (the GUE metric) on the full 5,920-sequence test split. Labelled training rows are drawn from
prom_300_all_train.csv, the same file whose unlabelled sequences form the memorisation fine-tuning set, so promoter rows seen
during memorisation fine-tuning may re-appear with labels here (as in any pretrain-then-fine-tune pipeline); the TEST split is
disjoint.
"""
from __future__ import annotations

import copy
import csv
import math
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from .data import encode as nt_encode

GUE_DIR = Path("data/gue")
N_TRAIN = 20_000
N_TEST = None            # all 5,920


def load_gue(n_train=N_TRAIN, seed=0):
    def read(split):
        with open(GUE_DIR / f"prom_300_all_{split}.csv", encoding="utf-8", newline="") as f:
            rows = [(r["sequence"].strip().upper(), int(r["label"])) for r in csv.DictReader(f)]
        return [(s, y) for s, y in rows if set(s) <= set("ACGT")]
    tr, te = read("train"), read("test")
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(tr))[:n_train]
    tr = [tr[i] for i in idx]
    if N_TEST:
        te = te[:N_TEST]
    return tr, te


class _Backbone(torch.nn.Module):
    """Mean-pooled last hidden state for the three model families, on pilot2 nt-id windows (B, L) or raw strings."""

    def __init__(self, kind, model, voc, causal):
        super().__init__()
        self.kind, self.model, self.voc, self.causal = kind, model, voc, causal

    def forward(self, seqs: list[str], device):
        if self.kind == "kmer":
            from .dnabert import causal_attention_mask
            nt = torch.from_numpy(np.stack([nt_encode(s) for s in seqs])).to(device)
            ids = self.voc.encode(nt)
            am = causal_attention_mask(ids.shape[0], ids.shape[1], device) if self.causal else None
            h = self.model.bert(input_ids=ids, attention_mask=am).last_hidden_state
            return h[:, 1:-1].mean(1)
        if self.kind == "bpe":
            ids, am = self.voc.pad_batch([self.voc.encode_str(s)[0] for s in seqs], device)
            out = self.model.bert(input_ids=ids, attention_mask=am)
            h = out[0] if isinstance(out, (tuple, list)) else out
            m = am.clone(); m[:, 0] = 0; m[ids == self.voc.sep] = 0
            return (h * m[..., None]).sum(1) / m.sum(1, keepdim=True)
        if self.kind == "hyena":
            from .hyena import encode as hy_encode
            nt = torch.from_numpy(np.stack([nt_encode(s) for s in seqs])).to(device)
            h = self.model.hyena(input_ids=hy_encode(nt), return_dict=True).last_hidden_state
            return h[:, 1:].mean(1)
        raise ValueError(self.kind)

    @property
    def d_model(self):
        if self.kind == "hyena":
            return self.model.config.d_model
        return self.model.config.hidden_size


@torch.no_grad()
def _features(bb, seqs, device, batch=64):
    out = []
    for i in range(0, len(seqs), batch):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out.append(bb(seqs[i:i + batch], device).float().cpu())
    return torch.cat(out).numpy()


def _mcc(y, p):
    y, p = np.asarray(y), np.asarray(p)
    tp = int(((p == 1) & (y == 1)).sum()); tn = int(((p == 0) & (y == 0)).sum())
    fp = int(((p == 1) & (y == 0)).sum()); fn = int(((p == 0) & (y == 1)).sum())
    den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    return (tp * tn - fp * fn) / den if den else 0.0


def linear_probe(bb, tr, te, device):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    t0 = time.time()
    xtr, xte = _features(bb, [s for s, _ in tr], device), _features(bb, [s for s, _ in te], device)
    ytr, yte = [y for _, y in tr], [y for _, y in te]
    sc = StandardScaler().fit(xtr)
    clf = LogisticRegression(max_iter=3000, C=1.0).fit(sc.transform(xtr), ytr)
    p = clf.predict(sc.transform(xte))
    return {"acc": float((p == np.asarray(yte)).mean()), "mcc": float(_mcc(yte, p)), "n_train": len(tr), "n_test": len(te),
            "sec": time.time() - t0}


def finetune_probe(bb, tr, te, device, lr=3e-5, batch=32, epochs=2, seed=0):
    """DNABERT-style supervised fine-tuning on a deep copy; the original model is untouched."""
    t0 = time.time()
    torch.manual_seed(seed)
    m = copy.deepcopy(bb.model).train()
    bb2 = _Backbone(bb.kind, m, bb.voc, bb.causal)
    head = torch.nn.Linear(bb.d_model, 2).to(device)
    params = list(m.parameters()) + list(head.parameters())
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    steps = epochs * math.ceil(len(tr) / batch); warm = max(1, int(0.1 * steps)); step = 0
    rng = np.random.default_rng(seed)
    for _ in range(epochs):
        order = rng.permutation(len(tr))
        for i in range(0, len(order), batch):
            idx = order[i:i + batch]
            seqs = [tr[j][0] for j in idx]; y = torch.tensor([tr[j][1] for j in idx], device=device)
            for g in opt.param_groups:
                g["lr"] = lr * min(1.0, (step + 1) / warm)
            opt.zero_grad(set_to_none=True)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                logits = head(bb2(seqs, device).float())
            loss = F.cross_entropy(logits.float(), y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(params, 1.0)
            opt.step(); step += 1
    m.eval()
    preds = []
    with torch.no_grad():
        for i in range(0, len(te), 64):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                preds.append(head(bb2([s for s, _ in te[i:i + 64]], device).float()).argmax(-1).cpu())
    p = torch.cat(preds).numpy(); yte = np.array([y for _, y in te])
    del m, bb2, head, opt
    torch.cuda.empty_cache()
    return {"acc": float((p == yte).mean()), "mcc": float(_mcc(yte, p)), "n_train": len(tr), "n_test": len(te),
            "epochs": epochs, "lr": lr, "batch": batch, "sec": time.time() - t0}


def evaluate(kind, model, voc, device, causal=False, seed=0, n_train=N_TRAIN, finetune=True):
    """-> {"task": "gue_prom_300_all", "linear_probe": {...}, "finetune": {...}}"""
    was_training = model.training
    model.eval()
    tr, te = load_gue(n_train, seed)
    bb = _Backbone(kind, model, voc, causal)
    res = {"task": "gue_prom_300_all", "linear_probe": linear_probe(bb, tr, te, device)}
    if finetune:
        res["finetune"] = finetune_probe(bb, tr, te, device, seed=seed)
    if was_training:
        model.train()
    return res
