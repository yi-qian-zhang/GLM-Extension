# Matched-utility memorisation — chr21

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.658 to 1.685 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.658 | @1.667 | @1.676 | @1.685 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.21 (0.00) | 0.27 (0.00) | 0.32 (0.00) | 0.37 (0.00) |
| DNABERT 4-mer [causal] | 0.01 (0.00) | 0.06 (0.00) | 0.12 (0.00) | 0.18 (0.00) |
| DNABERT 5-mer [causal] | -0.11 (0.00) | 0.03 (0.00) | 0.09 (0.00) | 0.14 (0.00) |
| DNABERT 6-mer [causal] | 0.24 (0.00) | 0.28 (0.00) | 0.32 (0.00) | 0.36 (0.00) |
| DNABERT-2 BPE [causal] | 0.09 (0.00) | 0.14 (0.00) | 0.19 (0.00) | 0.24 (0.00) |
| hyena_medium-160k | 0.19 (0.00) | 0.22 (0.00) | 0.25 (0.00) | 0.28 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.658 | @1.667 | @1.676 | @1.685 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.91 (0.35) | 1.09 (0.50) | 1.26 (0.64) | 1.44 (0.79) |
| DNABERT 4-mer [causal] | 0.55 (0.04) | 0.72 (0.16) | 0.89 (0.27) | 1.07 (0.39) |
| DNABERT 5-mer [causal] | 0.06 (0.00) | 0.40 (0.04) | 0.57 (0.10) | 0.71 (0.16) |
| DNABERT 6-mer [causal] | 0.90 (0.09) | 0.99 (0.15) | 1.08 (0.24) | 1.17 (0.33) |
| DNABERT-2 BPE [causal] | 1.49 (0.99) | 1.52 (1.00) | 1.55 (1.00) | 1.57 (1.00) |
| hyena_medium-160k | 1.59 (0.82) | 1.61 (0.82) | 1.63 (0.82) | 1.65 (0.82) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer [causal] | +0.26 | +0.35 |
| DNABERT 4-mer [causal] | +0.01 | -0.10 |
| DNABERT 5-mer [causal] | -0.15 | +0.13 |
| DNABERT 6-mer [causal] | +0.06 | -0.08 |
| DNABERT-2 BPE [causal] | -0.20 | -0.12 |
| hyena_medium-160k | -0.02 | -0.11 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0 | 2.894 | 0.26 ±0.02 | 0.35 ±0.02 | 3.04 |
| DNABERT 3-mer [causal] | 1 | 1.926 | -0.03 ±0.00 | 0.00 ±0.00 | 1.91 |
| DNABERT 3-mer [causal] | 3 | 1.893 | -0.00 ±0.01 | 0.02 ±0.01 | 1.90 |
| DNABERT 3-mer [causal] | 8 | 1.670 | -0.12 ±0.03 | -0.05 ±0.02 | 1.84 |
| DNABERT 3-mer [causal] | 15 | 1.624 | -0.08 ±0.05 | -0.02 ±0.05 | 1.84 |
| DNABERT 3-mer [causal] | 30 | 1.637 | 0.09 ±0.04 | 0.48 ±0.03 | 1.94 |
| DNABERT 3-mer [causal] | 50 | 1.685 | 0.37 ±0.01 | 1.44 ±0.01 | 1.99 |
| DNABERT 4-mer [causal] | 0 | 2.577 | 0.01 ±0.09 | -0.10 ±0.09 | 2.56 |
| DNABERT 4-mer [causal] | 1 | 1.939 | 0.02 ±0.01 | -0.03 ±0.01 | 1.94 |
| DNABERT 4-mer [causal] | 3 | 1.877 | -0.03 ±0.02 | 0.04 ±0.02 | 1.90 |
| DNABERT 4-mer [causal] | 8 | 1.726 | -0.14 ±0.01 | -0.05 ±0.01 | 1.81 |
| DNABERT 4-mer [causal] | 15 | 1.663 | -0.15 ±0.02 | -0.02 ±0.01 | 1.81 |
| DNABERT 4-mer [causal] | 30 | 1.655 | -0.01 ±0.01 | 0.49 ±0.05 | 1.91 |
| DNABERT 4-mer [causal] | 50 | 1.707 | 0.32 ±0.04 | 1.50 ±0.05 | 2.03 |
| DNABERT 5-mer [causal] | 0 | 3.006 | -0.15 ±0.07 | 0.13 ±0.07 | 2.96 |
| DNABERT 5-mer [causal] | 1 | 2.034 | -0.16 ±0.00 | 0.01 ±0.00 | 2.01 |
| DNABERT 5-mer [causal] | 3 | 1.876 | -0.04 ±0.00 | 0.03 ±0.00 | 1.87 |
| DNABERT 5-mer [causal] | 8 | 1.691 | -0.13 ±0.01 | -0.02 ±0.02 | 1.83 |
| DNABERT 5-mer [causal] | 15 | 1.658 | -0.11 ±0.03 | 0.06 ±0.01 | 1.86 |
| DNABERT 5-mer [causal] | 30 | 1.668 | 0.05 ±0.06 | 0.45 ±0.06 | 1.95 |
| DNABERT 5-mer [causal] | 50 | 1.735 | 0.43 ±0.00 | 1.49 ±0.01 | 2.08 |
| DNABERT 6-mer [causal] | 0 | 4.367 | 0.06 ±0.11 | -0.08 ±0.11 | 4.49 |
| DNABERT 6-mer [causal] | 1 | 1.924 | 0.02 ±0.01 | 0.07 ±0.01 | 1.98 |
| DNABERT 6-mer [causal] | 3 | 1.679 | -0.06 ±0.01 | 0.04 ±0.02 | 1.87 |
| DNABERT 6-mer [causal] | 8 | 1.612 | -0.04 ±0.02 | 0.07 ±0.00 | 1.88 |
| DNABERT 6-mer [causal] | 15 | 1.609 | 0.03 ±0.02 | 0.28 ±0.01 | 1.91 |
| DNABERT 6-mer [causal] | 30 | 1.662 | 0.25 ±0.04 | 0.94 ±0.05 | 2.01 |
| DNABERT 6-mer [causal] | 50 | 1.744 | 0.62 ±0.01 | 1.74 ±0.00 | 2.09 |
| DNABERT-2 BPE [causal] | 0 | 2.543 | -0.20 | -0.12 | 2.36 |
| DNABERT-2 BPE [causal] | 1 | 1.905 | -0.08 | -0.05 | 1.83 |
| DNABERT-2 BPE [causal] | 3 | 1.736 | -0.14 | -0.02 | 1.75 |
| DNABERT-2 BPE [causal] | 8 | 1.627 | -0.12 | 0.44 | 1.76 |
| DNABERT-2 BPE [causal] | 15 | 1.658 | 0.09 | 1.50 | 1.81 |
| DNABERT-2 BPE [causal] | 30 | 1.808 | 0.95 | 1.90 | 2.05 |
| DNABERT-2 BPE [causal] | 50 | 2.160 | 2.19 | 2.45 | 2.49 |
| hyena_medium-160k | 0 | 1.741 | -0.02 | -0.11 | 1.79 |
| hyena_medium-160k | 1 | 1.683 | -0.02 | -0.08 | 1.78 |
| hyena_medium-160k | 3 | 1.637 | 0.01 | 0.13 | 1.79 |
| hyena_medium-160k | 8 | 1.631 | 0.04 | 1.29 | 1.80 |
| hyena_medium-160k | 15 | 1.651 | 0.16 | 1.57 | 1.85 |
| hyena_medium-160k | 30 | 1.772 | 0.58 | 1.84 | 2.04 |
| hyena_medium-160k | 50 | 2.201 | 1.42 | 2.41 | 2.56 |
