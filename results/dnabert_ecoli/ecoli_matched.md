# Matched-utility memorisation — ecoli

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 1.921, highest 1.919), so no matched-utility comparison is possible; report the per-model trajectories instead.

- DNABERT 3-mer: held-out loss 1.890 to 1.919
- DNABERT 4-mer: held-out loss 1.915 to 1.930
- DNABERT 5-mer: held-out loss 1.907 to 1.935
- DNABERT 6-mer: held-out loss 1.921 to 1.988
- DNABERT-2 BPE: held-out loss 1.860 to 2.386
- hyena_medium-160k: held-out loss 1.917 to 2.849
## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer | 0 | 2.882 | 0.04 | -0.04 | 2.71 |
| DNABERT 3-mer | 1 | 2.022 | 0.02 | 0.03 | 2.13 |
| DNABERT 3-mer | 3 | 1.958 | 0.00 | 0.01 | 2.06 |
| DNABERT 3-mer | 8 | 1.940 | -0.03 | 0.02 | 2.06 |
| DNABERT 3-mer | 15 | 1.909 | -0.05 | 0.07 | 2.09 |
| DNABERT 3-mer | 30 | 1.890 | 0.02 | 0.16 | 2.11 |
| DNABERT 3-mer | 50 | 1.919 | 0.15 | 0.54 | 2.14 |
| DNABERT 4-mer | 0 | 2.744 | 0.17 | 0.21 | 2.78 |
| DNABERT 4-mer | 1 | 2.012 | -0.02 | 0.03 | 2.12 |
| DNABERT 4-mer | 3 | 1.947 | -0.02 | 0.02 | 2.08 |
| DNABERT 4-mer | 8 | 1.937 | -0.03 | 0.02 | 2.07 |
| DNABERT 4-mer | 15 | 1.927 | -0.03 | 0.08 | 2.08 |
| DNABERT 4-mer | 30 | 1.915 | 0.01 | 0.32 | 2.10 |
| DNABERT 4-mer | 50 | 1.930 | 0.22 | 1.30 | 2.18 |
| DNABERT 5-mer | 0 | 3.147 | 0.11 | 0.01 | 3.17 |
| DNABERT 5-mer | 1 | 2.156 | -0.03 | 0.16 | 2.32 |
| DNABERT 5-mer | 3 | 1.943 | -0.01 | 0.02 | 2.07 |
| DNABERT 5-mer | 8 | 1.931 | -0.02 | 0.05 | 2.07 |
| DNABERT 5-mer | 15 | 1.916 | -0.01 | 0.12 | 2.09 |
| DNABERT 5-mer | 30 | 1.907 | 0.04 | 0.43 | 2.12 |
| DNABERT 5-mer | 50 | 1.935 | 0.32 | 1.64 | 2.24 |
| DNABERT 6-mer | 0 | 4.787 | -0.09 | 0.05 | 4.74 |
| DNABERT 6-mer | 1 | 2.035 | -0.03 | 0.02 | 2.16 |
| DNABERT 6-mer | 3 | 1.935 | -0.01 | 0.07 | 2.09 |
| DNABERT 6-mer | 8 | 1.928 | -0.01 | 0.12 | 2.09 |
| DNABERT 6-mer | 15 | 1.921 | 0.03 | 0.25 | 2.10 |
| DNABERT 6-mer | 30 | 1.923 | 0.19 | 1.21 | 2.20 |
| DNABERT 6-mer | 50 | 1.988 | 0.56 | 2.04 | 2.34 |
| DNABERT-2 BPE | 0 | 2.525 | 0.06 | -0.04 | 2.55 |
| DNABERT-2 BPE | 1 | 1.891 | -0.00 | 0.01 | 2.04 |
| DNABERT-2 BPE | 3 | 1.862 | 0.00 | 0.10 | 2.03 |
| DNABERT-2 BPE | 8 | 1.860 | 0.05 | 0.66 | 2.05 |
| DNABERT-2 BPE | 15 | 1.879 | 0.18 | 1.72 | 2.09 |
| DNABERT-2 BPE | 30 | 2.048 | 0.94 | 2.17 | 2.28 |
| DNABERT-2 BPE | 50 | 2.386 | 2.03 | 2.63 | 2.67 |
| hyena_medium-160k | 0 | 2.066 | 0.03 | 0.03 | 2.11 |
| hyena_medium-160k | 1 | 1.939 | 0.00 | 0.01 | 2.05 |
| hyena_medium-160k | 3 | 1.926 | 0.00 | 0.05 | 2.06 |
| hyena_medium-160k | 8 | 1.917 | 0.02 | 1.45 | 2.07 |
| hyena_medium-160k | 15 | 1.956 | 0.15 | 1.87 | 2.14 |
| hyena_medium-160k | 30 | 2.194 | 0.78 | 2.29 | 2.46 |
| hyena_medium-160k | 50 | 2.849 | 2.17 | 3.24 | 3.36 |
