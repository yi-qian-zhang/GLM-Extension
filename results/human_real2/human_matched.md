# Matched-utility memorisation — human

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 1.872, highest 1.666), so no matched-utility comparison is possible; report the per-model trajectories instead.

- 6-mer: held-out loss 1.863 to 2.345
- BPE-4096: held-out loss 1.872 to 2.678
- DNABERT 3-mer: held-out loss 1.595 to 1.666
- DNABERT 4-mer: held-out loss 1.653 to 1.705
- DNABERT 5-mer: held-out loss 1.649 to 1.719
- DNABERT 6-mer: held-out loss 1.603 to 1.726
- DNABERT-2 BPE: held-out loss 1.626 to 2.201
- hyena_medium-160k: held-out loss 1.624 to 2.221
## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| 6-mer | 1 | 1.945 | 0.00 | 0.02 | 1.96 |
| 6-mer | 2 | 1.916 | 0.03 | 0.05 | 1.95 |
| 6-mer | 3 | 1.883 | 0.10 | 0.18 | 1.93 |
| 6-mer | 5 | 1.863 | 0.31 | 0.50 | 1.92 |
| 6-mer | 8 | 1.901 | 0.80 | 1.06 | 1.97 |
| 6-mer | 12 | 2.019 | 1.55 | 1.74 | 2.12 |
| 6-mer | 20 | 2.249 | 2.33 | 2.33 | 2.36 |
| 6-mer | 30 | 2.345 | 2.45 | 2.45 | 2.46 |
| BPE-4096 | 1 | 2.028 | 0.01 | 0.05 | 2.04 |
| BPE-4096 | 2 | 1.950 | 0.05 | 0.17 | 2.00 |
| BPE-4096 | 3 | 1.893 | 0.13 | 0.48 | 1.97 |
| BPE-4096 | 5 | 1.872 | 0.34 | 1.15 | 1.96 |
| BPE-4096 | 8 | 1.973 | 0.92 | 1.75 | 2.07 |
| BPE-4096 | 12 | 2.220 | 1.78 | 2.20 | 2.32 |
| BPE-4096 | 20 | 2.538 | 2.59 | 2.63 | 2.65 |
| BPE-4096 | 30 | 2.678 | 2.78 | 2.79 | 2.79 |
| DNABERT 3-mer | 0 | 2.869 | 0.30 | -0.09 | 2.89 |
| DNABERT 3-mer | 1 | 1.907 | 0.02 | -0.02 | 1.97 |
| DNABERT 3-mer | 3 | 1.877 | 0.03 | 0.01 | 1.95 |
| DNABERT 3-mer | 8 | 1.628 | -0.31 | 0.21 | 1.66 |
| DNABERT 3-mer | 15 | 1.595 | -0.34 | 0.50 | 1.59 |
| DNABERT 3-mer | 30 | 1.626 | -0.26 | 0.98 | 1.63 |
| DNABERT 3-mer | 50 | 1.666 | 0.34 | 1.46 | 1.78 |
| DNABERT 4-mer | 0 | 2.624 | 0.09 | 0.16 | 2.69 |
| DNABERT 4-mer | 1 | 1.945 | 0.06 | 0.05 | 2.01 |
| DNABERT 4-mer | 3 | 1.876 | 0.07 | 0.06 | 1.97 |
| DNABERT 4-mer | 8 | 1.691 | -0.20 | 0.28 | 1.79 |
| DNABERT 4-mer | 15 | 1.656 | -0.30 | 0.38 | 1.65 |
| DNABERT 4-mer | 30 | 1.653 | -0.26 | 0.91 | 1.66 |
| DNABERT 4-mer | 50 | 1.705 | 0.31 | 1.37 | 1.77 |
| DNABERT 5-mer | 0 | 3.139 | 0.13 | 0.09 | 3.09 |
| DNABERT 5-mer | 1 | 2.006 | -0.05 | -0.01 | 2.03 |
| DNABERT 5-mer | 3 | 1.791 | -0.04 | 0.12 | 1.88 |
| DNABERT 5-mer | 8 | 1.674 | -0.15 | 0.27 | 1.77 |
| DNABERT 5-mer | 15 | 1.649 | -0.23 | 0.52 | 1.72 |
| DNABERT 5-mer | 30 | 1.652 | -0.17 | 0.99 | 1.74 |
| DNABERT 5-mer | 50 | 1.719 | 0.37 | 1.39 | 1.82 |
| DNABERT 6-mer | 0 | 4.483 | 0.62 | 0.08 | 4.84 |
| DNABERT 6-mer | 1 | 1.927 | -0.08 | 0.05 | 1.98 |
| DNABERT 6-mer | 3 | 1.668 | -0.11 | 0.28 | 1.83 |
| DNABERT 6-mer | 8 | 1.610 | -0.21 | 0.51 | 1.69 |
| DNABERT 6-mer | 15 | 1.603 | -0.22 | 0.80 | 1.68 |
| DNABERT 6-mer | 30 | 1.637 | -0.12 | 1.15 | 1.72 |
| DNABERT 6-mer | 50 | 1.726 | 0.59 | 1.55 | 1.83 |
| DNABERT-2 BPE | 0 | 2.574 | 0.08 | 0.20 | 2.63 |
| DNABERT-2 BPE | 1 | 1.881 | -0.03 | 0.07 | 1.90 |
| DNABERT-2 BPE | 3 | 1.704 | -0.16 | 0.18 | 1.77 |
| DNABERT-2 BPE | 8 | 1.626 | -0.18 | 0.93 | 1.67 |
| DNABERT-2 BPE | 15 | 1.660 | 0.00 | 1.43 | 1.71 |
| DNABERT-2 BPE | 30 | 1.831 | 0.83 | 1.76 | 1.88 |
| DNABERT-2 BPE | 50 | 2.201 | 2.15 | 2.30 | 2.33 |
| hyena_medium-160k | 0 | 1.661 | -0.00 | 0.01 | 1.76 |
| hyena_medium-160k | 1 | 1.635 | 0.02 | 0.10 | 1.75 |
| hyena_medium-160k | 3 | 1.624 | 0.04 | 0.35 | 1.73 |
| hyena_medium-160k | 8 | 1.626 | 0.10 | 1.26 | 1.71 |
| hyena_medium-160k | 15 | 1.654 | 0.26 | 1.45 | 1.74 |
| hyena_medium-160k | 30 | 1.782 | 0.61 | 1.66 | 1.87 |
| hyena_medium-160k | 50 | 2.221 | 1.43 | 2.27 | 2.40 |
