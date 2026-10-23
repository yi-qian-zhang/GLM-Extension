# Matched-utility memorisation — human_ds_raw

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned, minus its own value at epoch 0, where nothing is memorised and the reading is the fixed offset between the two canary groups. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.594 to 1.595 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.594 | @1.595 | @1.595 | @1.595 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.35 (0.00) | 0.35 (0.00) | 0.36 (0.00) | 0.36 (0.00) |
| DNABERT 4-mer [causal] | 0.23 (0.00) | 0.23 (0.00) | 0.23 (0.00) | 0.23 (0.00) |
| DNABERT 5-mer [causal] | 0.13 (0.00) | 0.13 (0.00) | 0.14 (0.00) | 0.14 (0.00) |
| DNABERT 6-mer [causal] | 0.49 (0.00) | 0.49 (0.00) | 0.49 (0.00) | 0.49 (0.00) |
| DNABERT-2 BPE [causal] | 0.28 (0.00) | 0.28 (0.00) | 0.29 (0.00) | 0.29 (0.00) |
| hyena_medium-160k | 0.29 (0.00) | 0.29 (0.00) | 0.30 (0.00) | 0.30 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.594 | @1.595 | @1.595 | @1.595 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 1.39 (0.91) | 1.40 (0.92) | 1.41 (0.93) | 1.41 (0.93) |
| DNABERT 4-mer [causal] | 0.86 (0.27) | 0.87 (0.27) | 0.87 (0.28) | 0.88 (0.28) |
| DNABERT 5-mer [causal] | 0.53 (0.08) | 0.54 (0.09) | 0.55 (0.09) | 0.57 (0.09) |
| DNABERT 6-mer [causal] | 1.27 (0.46) | 1.27 (0.46) | 1.28 (0.46) | 1.28 (0.46) |
| DNABERT-2 BPE [causal] | 1.17 (0.56) | 1.18 (0.57) | 1.19 (0.58) | 1.20 (0.59) |
| hyena_medium-160k | 1.47 (0.69) | 1.47 (0.69) | 1.47 (0.69) | 1.47 (0.69) |

## Epoch-0 group offset subtracted above (excess that is present before any training)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer [causal] | +0.00 | +0.00 |
| DNABERT 4-mer [causal] | +0.00 | +0.00 |
| DNABERT 5-mer [causal] | +0.00 | +0.00 |
| DNABERT 6-mer [causal] | +0.00 | +0.00 |
| DNABERT-2 BPE [causal] | +0.00 | +0.00 |
| hyena_medium-160k | +0.00 | +0.00 |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0 | 2.876 | 0.04 | 0.30 | 3.01 |
| DNABERT 3-mer [causal] | 1 | 1.916 | 0.00 | -0.03 | 1.93 |
| DNABERT 3-mer [causal] | 3 | 1.882 | 0.02 | 0.01 | 1.93 |
| DNABERT 3-mer [causal] | 8 | 1.585 | -0.07 | -0.00 | 1.71 |
| DNABERT 3-mer [causal] | 15 | 1.549 | 0.01 | 0.19 | 1.72 |
| DNABERT 3-mer [causal] | 30 | 1.558 | 0.18 | 0.75 | 1.76 |
| DNABERT 3-mer [causal] | 50 | 1.595 | 0.36 | 1.41 | 1.81 |
| DNABERT 4-mer [causal] | 0 | 2.614 | 0.02 | -0.01 | 2.56 |
| DNABERT 4-mer [causal] | 1 | 1.964 | 0.03 | -0.00 | 1.98 |
| DNABERT 4-mer [causal] | 3 | 1.879 | 0.02 | 0.01 | 1.92 |
| DNABERT 4-mer [causal] | 8 | 1.638 | -0.02 | 0.04 | 1.75 |
| DNABERT 4-mer [causal] | 15 | 1.598 | 0.07 | 0.26 | 1.77 |
| DNABERT 4-mer [causal] | 30 | 1.594 | 0.23 | 0.86 | 1.84 |
| DNABERT 4-mer [causal] | 50 | 1.634 | 0.43 | 1.50 | 1.90 |
| DNABERT 5-mer [causal] | 0 | 3.166 | 0.16 | 0.05 | 3.09 |
| DNABERT 5-mer [causal] | 1 | 1.990 | -0.02 | -0.00 | 2.05 |
| DNABERT 5-mer [causal] | 3 | 1.783 | 0.00 | -0.02 | 1.82 |
| DNABERT 5-mer [causal] | 8 | 1.613 | -0.00 | 0.06 | 1.74 |
| DNABERT 5-mer [causal] | 15 | 1.588 | 0.04 | 0.25 | 1.74 |
| DNABERT 5-mer [causal] | 30 | 1.601 | 0.22 | 0.81 | 1.78 |
| DNABERT 5-mer [causal] | 50 | 1.649 | 0.48 | 1.50 | 1.90 |
| DNABERT 6-mer [causal] | 0 | 4.462 | 0.25 | 0.35 | 4.90 |
| DNABERT 6-mer [causal] | 1 | 1.906 | -0.02 | -0.00 | 1.94 |
| DNABERT 6-mer [causal] | 3 | 1.610 | -0.03 | -0.01 | 1.76 |
| DNABERT 6-mer [causal] | 8 | 1.553 | 0.03 | 0.24 | 1.74 |
| DNABERT 6-mer [causal] | 15 | 1.546 | 0.15 | 0.49 | 1.75 |
| DNABERT 6-mer [causal] | 30 | 1.584 | 0.45 | 1.22 | 1.85 |
| DNABERT 6-mer [causal] | 50 | 1.676 | 0.75 | 1.67 | 1.96 |
| DNABERT-2 BPE [causal] | 0 | 2.559 | 0.05 | 0.06 | 2.54 |
| DNABERT-2 BPE [causal] | 1 | 1.883 | -0.01 | -0.00 | 1.88 |
| DNABERT-2 BPE [causal] | 3 | 1.650 | -0.03 | 0.11 | 1.73 |
| DNABERT-2 BPE [causal] | 8 | 1.579 | 0.10 | 0.78 | 1.72 |
| DNABERT-2 BPE [causal] | 15 | 1.607 | 0.43 | 1.51 | 1.79 |
| DNABERT-2 BPE [causal] | 30 | 1.769 | 1.26 | 1.89 | 2.00 |
| DNABERT-2 BPE [causal] | 50 | 2.116 | 2.15 | 2.33 | 2.36 |
| hyena_medium-160k | 0 | 1.699 | -0.04 | -0.06 | 1.73 |
| hyena_medium-160k | 1 | 1.636 | -0.03 | 0.01 | 1.71 |
| hyena_medium-160k | 3 | 1.589 | -0.01 | 0.28 | 1.70 |
| hyena_medium-160k | 8 | 1.579 | 0.12 | 1.23 | 1.71 |
| hyena_medium-160k | 15 | 1.594 | 0.29 | 1.47 | 1.76 |
| hyena_medium-160k | 30 | 1.718 | 0.76 | 1.76 | 1.95 |
| hyena_medium-160k | 50 | 2.141 | 1.64 | 2.39 | 2.53 |
