"""Downstream utility probes: GUE classification tasks (Zhou et al., DNABERT-2), DNABERT's own benchmark.

Called at every scored snapshot of a real-model run (`--downstream` + `--downstream_tasks` in dnabert.py / dnabert2.py /
hyena.py). For each task:
  * linear probe  — frozen mean-pooled last hidden states -> logistic regression (sklearn); cheap, measures representation quality
  * fine-tune     — DNABERT-2 recipe scaled down: deepcopy of the model + linear head on mean-pooled states, AdamW lr 3e-5,
                    batch 32, 2 epochs on up to N_TRAIN labelled sequences (the paper: 3 epochs on all); the copy is discarded
Both report accuracy and MCC (the GUE metric; multi-class MCC for splice) on the task's full test split.

Tasks (files data/gue/<task>_{train,dev,test}.csv, column 'sequence' / 'label'):
  human : prom_300_all (300 nt), prom_core_all (70 nt), human_tf_0 (100 nt), splice_reconstructed (400 nt, 3 classes)
  yeast : emp_H3, emp_H3K4me3 (500 nt histone-mark datasets of S. cerevisiae)
Default task set per memorisation dataset: gue -> prom_300_all; yeast -> emp_H3,emp_H3K4me3; ecoli -> none (GUE has no bacterium).
Labelled training rows of prom_300_all come from the same file whose unlabelled sequences form the GUE memorisation
fine-tuning set (as in any pretrain-then-fine-tune pipeline); every TEST split is disjoint.
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
DEFAULT_TASKS = {"gue": ["prom_300_all"], "yeast": ["emp_H3", "emp_H3K4me3"]}
HUMAN_WIDE = ["prom_core_all", "human_tf_0", "splice_reconstructed"]


def load_task(task, n_train=N_TRAIN, seed=0):
    def read(split):
        with open(GUE_DIR / f"{task}_{split}.csv", encoding="utf-8", newline="") as f:
            rows = [(r["sequence"].strip().upper(), int(r["label"])) for r in csv.DictReader(f)
                    if r.get("label") not in (None, "") and r.get("sequence")]
        rows = [(s, y) for s, y in rows if set(s) <= set("ACGT")]
        # a handful of GUE rows have odd lengths (e.g. 449 among 500-nt rows); keep the modal length so batches stack
        from collections import Counter
        L = Counter(len(s) for s, _ in rows).most_common(1)[0][0]
        return [(s, y) for s, y in rows if len(s) == L]
    tr, te = read("train"), read("test")
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(tr))[:n_train]
    tr = [tr[i] for i in idx]
    n_cls = 1 + max(max(y for _, y in tr), max(y for _, y in te))
    return tr, te, n_cls


class _Backbone(torch.nn.Module):
    """Mean-pooled last hidden state for the three model families, from raw ACGT strings (any length <= ~500 nt)."""

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
    from sklearn.metrics import matthews_corrcoef
    return float(matthews_corrcoef(np.asarray(y), np.asarray(p)))


def linear_probe(bb, tr, te, device):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    t0 = time.time()
    xtr, xte = _features(bb, [s for s, _ in tr], device), _features(bb, [s for s, _ in te], device)
    ytr, yte = [y for _, y in tr], [y for _, y in te]
    sc = StandardScaler().fit(xtr)
    clf = LogisticRegression(max_iter=3000, C=1.0).fit(sc.transform(xtr), ytr)
    p = clf.predict(sc.transform(xte))
    return {"acc": float((p == np.asarray(yte)).mean()), "mcc": _mcc(yte, p), "n_train": len(tr), "n_test": len(te),
            "sec": time.time() - t0}


def finetune_probe(bb, tr, te, n_cls, device, lr=3e-5, batch=32, epochs=2, seed=0):
    """DNABERT-style supervised fine-tuning on a deep copy; the original model is untouched."""
    t0 = time.time()
    torch.manual_seed(seed)
    m = copy.deepcopy(bb.model).train()
    bb2 = _Backbone(bb.kind, m, bb.voc, bb.causal)
    head = torch.nn.Linear(bb.d_model, n_cls).to(device)
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
    return {"acc": float((p == yte).mean()), "mcc": _mcc(yte, p), "n_train": len(tr), "n_test": len(te),
            "epochs": epochs, "lr": lr, "batch": batch, "sec": time.time() - t0}


def evaluate(kind, model, voc, device, causal=False, seed=0, tasks=("prom_300_all",), n_train=N_TRAIN, finetune=True):
    """-> {"tasks": {task: {"n_classes", "linear_probe": {...}, "finetune": {...}}},
           "task", "linear_probe", "finetune"}  (the flat keys mirror the FIRST task, for older readers)"""
    was_training = model.training
    model.eval()
    bb = _Backbone(kind, model, voc, causal)
    res = {"tasks": {}}
    for task in tasks:
        tr, te, n_cls = load_task(task, n_train, seed)
        r = {"n_classes": n_cls, "linear_probe": linear_probe(bb, tr, te, device)}
        if finetune:
            r["finetune"] = finetune_probe(bb, tr, te, n_cls, device, seed=seed)
        res["tasks"][task] = r
        print(f"    [downstream {task}] probe mcc {r['linear_probe']['mcc']:.3f}" +
              (f" | ft mcc {r['finetune']['mcc']:.3f}" if finetune else ""), flush=True)
    first = tasks[0]
    res.update(task=first, linear_probe=res["tasks"][first]["linear_probe"], finetune=res["tasks"][first].get("finetune"))
    if was_training:
        model.train()
    return res
