---
license: mit
tags:
  - biology
  - dna
  - genomics
  - memorization
  - privacy
  - membership-inference
base_model: zhihan1996/DNABERT-2-117M
library_name: transformers
---

# DNABERT-2 fine-tuned on chromosome-22 haplotypes: checkpoints for a memorisation study

These are **research artefacts, not models to deploy**. They exist so that one result can be
checked: a released genomic language model identifies which individual's haplotype was in its
fine-tuning set at checkpoints where it reproduces nothing at all.

Three seeds of DNABERT-2 (117M) fine-tuned on human chromosome 22, with rare-variant
haplotypes planted as canaries at 1, 4 and 16 copies. Seven checkpoints per seed, saved along
the training run rather than only at the end, so the leak can be measured as a function of
how far training went.

## What these checkpoints show

Identification runs far ahead of reproduction. At round 120, across three seeds, the model
ranks a single-copy planted haplotype first against 100 other real rare-variant segments
**0.70 / 0.80 / 0.80** of the time, where chance is 0.01 — while verbatim reproduction of
that same record reads **0.00 in every seed at every checkpoint**. Of 150 never-trained
control segments, none was ever identified.

| checkpoint | held-out bits/nt | single copy identified | reproduced |
|---|---|---|---|
| `ep15.pt` (best held-out loss) | 1.266 | 0.00 | 0% |
| `ep30.pt` | 1.299 | 0.00 | 0% |
| `ep50.pt` | 1.357 | 0.00 | 0% |
| `ep80.pt` | 1.454 | 0.20 / 0.20 / 0.40 | 0% |
| `ep120.pt` | 1.599 | **0.70 / 0.80 / 0.80** | 0% |
| `ep150.pt`, `final.pt` | 1.726 | **0.92 / 0.94 / 0.96** | 0% |

The downstream task score over the same range moves about one per cent (GUE promoter
classification, linear probe on frozen features, MCC 0.787–0.802, declining monotonically).
The metric a practitioner would select on does not see any of this.

## Files

```
seed0/ep15.pt  ep30.pt  ep50.pt  ep80.pt  ep120.pt  ep150.pt  final.pt
seed1/…
seed2/…
```

Each file is a `state_dict` for DNABERT-2 117M, loadable with the architecture from
`zhihan1996/DNABERT-2-117M`. The planted-canary construction, the decoders and the scoring
code are in the repository linked below; `results/figure_data.csv` there carries the numbers
above in tidy form.

## Data and ethics

The planted records are 96-nucleotide windows of human chromosome 22 built around variants
carried by at most 5 of the 2,548 individuals in **1000 Genomes phase 3**, written with that
carrier's own alleles. That cohort is public, consented and redistributable, which is why a
study demonstrating re-identification can be run and published on it at all: nothing these
checkpoints can reveal about an individual is not already downloadable from the 1000 Genomes
release.

The point of publishing them is the opposite of exposure. The finding is that a model
fine-tuned on a **private** cohort would carry the same signal while passing the safety check
the field currently applies, and that claim should be checkable rather than taken on trust.

## Caveats on the numbers

Two things recorded in the repository's `notes/17_experiment_log_week3_EN.md` §3.58 make a
quoted percentage less exact than it looks:

1. The extraction decoder is chaotic in the model's last-bit arithmetic — restart
   trajectories do not reproduce across batch shapes — so a rate carries a few points of
   run-to-run uncertainty beyond the binomial interval on the probe count.
2. The host machine's floating-point behaviour changed across a reboot during the study.
   Every cell backing a published claim was re-measured on a single basis afterwards.

## Code and full results

<https://github.com/yi-qian-zhang/GLM-Extension/tree/glmex>

Working logs are under `notes/`, the measured output under `results/`.
