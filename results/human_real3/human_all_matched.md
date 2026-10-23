# Matched-utility memorisation — human_all

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned, minus its own value at epoch 0, where nothing is memorised and the reading is the fixed offset between the two canary groups. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.624 to 1.629 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.624 | @1.626 | @1.628 | @1.629 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.13 (0.00) | 0.15 (0.00) | 0.16 (0.00) | 0.18 (0.00) |
| DNABERT 4-mer [causal] | 0.11 (0.00) | 0.12 (0.00) | 0.13 (0.00) | 0.14 (0.00) |
| DNABERT 5-mer [causal] | -0.07 (0.00) | -0.05 (0.00) | -0.02 (0.00) | -0.01 (0.00) |
| DNABERT 6-mer [causal] | -0.16 (0.01) | -0.16 (0.01) | -0.15 (0.01) | -0.14 (0.01) |
| DNABERT-2 BPE [causal] | 0.18 (0.00) | 0.20 (0.00) | 0.21 (0.00) | 0.23 (0.00) |
| hyena_medium-160k | 0.30 (0.00) | 0.31 (0.00) | 0.32 (0.00) | 0.32 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.624 | @1.626 | @1.628 | @1.629 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 1.26 (0.89) | 1.28 (0.91) | 1.30 (0.93) | 1.32 (0.95) |
| DNABERT 4-mer [causal] | 0.98 (0.43) | 1.00 (0.45) | 1.02 (0.47) | 1.04 (0.48) |
| DNABERT 5-mer [causal] | 0.74 (0.23) | 0.86 (0.31) | 0.94 (0.37) | 0.95 (0.38) |
| DNABERT 6-mer [causal] | 1.07 (0.56) | 1.08 (0.57) | 1.09 (0.58) | 1.09 (0.58) |
| DNABERT-2 BPE [causal] | 1.27 (0.72) | 1.30 (0.75) | 1.33 (0.78) | 1.37 (0.81) |
| hyena_medium-160k | 1.49 (0.67) | 1.49 (0.68) | 1.50 (0.68) | 1.50 (0.68) |

## Epoch-0 group offset subtracted above (excess that is present before any training)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer [causal] | +0.22 | +0.16 |
| DNABERT 4-mer [causal] | -0.00 | +0.02 |
| DNABERT 5-mer [causal] | +0.13 | +0.05 |
| DNABERT 6-mer [causal] | +0.50 | +0.28 |
| DNABERT-2 BPE [causal] | +0.04 | +0.10 |
| hyena_medium-160k | +0.00 | -0.00 |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0 | 2.873 | 0.00 | 0.00 | 3.00 |
| DNABERT 3-mer [causal] | 1 | 1.912 | -0.20 | -0.17 | 1.96 |
| DNABERT 3-mer [causal] | 3 | 1.879 | -0.19 | -0.14 | 1.95 |
| DNABERT 3-mer [causal] | 8 | 1.604 | -0.33 | 0.03 | 1.77 |
| DNABERT 3-mer [causal] | 15 | 1.573 | -0.31 | 0.26 | 1.74 |
| DNABERT 3-mer [causal] | 30 | 1.589 | -0.19 | 0.77 | 1.77 |
| DNABERT 3-mer [causal] | 50 | 1.629 | 0.18 | 1.32 | 1.84 |
| DNABERT 4-mer [causal] | 0 | 2.619 | 0.00 | 0.00 | 2.57 |
| DNABERT 4-mer [causal] | 1 | 1.955 | 0.04 | 0.01 | 2.00 |
| DNABERT 4-mer [causal] | 3 | 1.877 | 0.04 | 0.01 | 1.95 |
| DNABERT 4-mer [causal] | 8 | 1.664 | -0.05 | 0.20 | 1.84 |
| DNABERT 4-mer [causal] | 15 | 1.630 | 0.00 | 0.42 | 1.83 |
| DNABERT 4-mer [causal] | 30 | 1.624 | 0.11 | 0.98 | 1.87 |
| DNABERT 4-mer [causal] | 50 | 1.669 | 0.44 | 1.49 | 1.90 |
| DNABERT 5-mer [causal] | 0 | 3.152 | 0.00 | 0.00 | 3.07 |
| DNABERT 5-mer [causal] | 1 | 1.998 | -0.14 | -0.04 | 2.06 |
| DNABERT 5-mer [causal] | 3 | 1.786 | -0.13 | 0.02 | 1.88 |
| DNABERT 5-mer [causal] | 8 | 1.644 | -0.14 | 0.19 | 1.83 |
| DNABERT 5-mer [causal] | 15 | 1.620 | -0.15 | 0.41 | 1.80 |
| DNABERT 5-mer [causal] | 30 | 1.627 | -0.03 | 0.93 | 1.84 |
| DNABERT 5-mer [causal] | 50 | 1.688 | 0.35 | 1.44 | 1.91 |
| DNABERT 6-mer [causal] | 0 | 4.473 | 0.00 | 0.00 | 4.94 |
| DNABERT 6-mer [causal] | 1 | 1.918 | -0.54 | -0.24 | 1.97 |
| DNABERT 6-mer [causal] | 3 | 1.638 | -0.49 | -0.07 | 1.87 |
| DNABERT 6-mer [causal] | 8 | 1.581 | -0.52 | 0.17 | 1.79 |
| DNABERT 6-mer [causal] | 15 | 1.576 | -0.46 | 0.45 | 1.80 |
| DNABERT 6-mer [causal] | 30 | 1.613 | -0.23 | 1.02 | 1.89 |
| DNABERT 6-mer [causal] | 50 | 1.702 | 0.25 | 1.42 | 1.99 |
| DNABERT-2 BPE [causal] | 0 | 2.566 | 0.00 | 0.00 | 2.56 |
| DNABERT-2 BPE [causal] | 1 | 1.883 | -0.06 | -0.06 | 1.90 |
| DNABERT-2 BPE [causal] | 3 | 1.677 | -0.11 | 0.07 | 1.78 |
| DNABERT-2 BPE [causal] | 8 | 1.602 | -0.00 | 0.83 | 1.77 |
| DNABERT-2 BPE [causal] | 15 | 1.634 | 0.26 | 1.45 | 1.84 |
| DNABERT-2 BPE [causal] | 30 | 1.801 | 1.13 | 1.83 | 2.05 |
| DNABERT-2 BPE [causal] | 50 | 2.157 | 2.17 | 2.27 | 2.41 |
| hyena_medium-160k | 0 | 1.680 | 0.00 | 0.00 | 1.76 |
| hyena_medium-160k | 1 | 1.636 | 0.01 | 0.07 | 1.74 |
| hyena_medium-160k | 3 | 1.606 | 0.04 | 0.34 | 1.73 |
| hyena_medium-160k | 8 | 1.603 | 0.13 | 1.26 | 1.73 |
| hyena_medium-160k | 15 | 1.623 | 0.30 | 1.49 | 1.77 |
| hyena_medium-160k | 30 | 1.752 | 0.75 | 1.76 | 1.96 |
| hyena_medium-160k | 50 | 2.185 | 1.61 | 2.39 | 2.53 |
