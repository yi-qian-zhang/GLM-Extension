# Matched-utility memorisation — human_all4

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.624 to 1.629 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.624 | @1.626 | @1.628 | @1.629 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.35 (0.00) | 0.37 (0.00) | 0.38 (0.00) | 0.40 (0.00) |
| DNABERT 4-mer [causal] | 0.11 (0.00) | 0.12 (0.00) | 0.13 (0.00) | 0.14 (0.00) |
| DNABERT 5-mer [causal] | 0.06 (0.00) | 0.09 (0.00) | 0.11 (0.00) | 0.12 (0.00) |
| DNABERT 6-mer [causal] | 0.34 (0.01) | 0.34 (0.01) | 0.35 (0.01) | 0.36 (0.01) |
| DNABERT-2 BPE [causal] | 0.22 (0.00) | 0.24 (0.00) | 0.25 (0.00) | 0.27 (0.00) |
| hyena_medium-160k | 0.30 (0.00) | 0.31 (0.00) | 0.32 (0.00) | 0.32 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.624 | @1.626 | @1.628 | @1.629 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 1.41 (0.89) | 1.44 (0.91) | 1.46 (0.93) | 1.48 (0.95) |
| DNABERT 4-mer [causal] | 1.00 (0.43) | 1.02 (0.45) | 1.04 (0.47) | 1.06 (0.48) |
| DNABERT 5-mer [causal] | 0.79 (0.23) | 0.91 (0.31) | 0.99 (0.37) | 1.01 (0.38) |
| DNABERT 6-mer [causal] | 1.35 (0.56) | 1.36 (0.57) | 1.36 (0.58) | 1.37 (0.58) |
| DNABERT-2 BPE [causal] | 1.37 (0.72) | 1.40 (0.75) | 1.44 (0.78) | 1.47 (0.81) |
| hyena_medium-160k | 1.49 (0.67) | 1.49 (0.68) | 1.50 (0.68) | 1.50 (0.68) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer [causal] | +0.22 | +0.16 |
| DNABERT 4-mer [causal] | -0.00 | +0.02 |
| DNABERT 5-mer [causal] | +0.13 | +0.05 |
| DNABERT 6-mer [causal] | +0.50 | +0.28 |
| DNABERT-2 BPE [causal] | +0.04 | +0.10 |
| hyena_medium-160k | +0.00 | -0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0 | 2.873 | 0.22 ±0.33 | 0.16 ±0.24 | 3.00 |
| DNABERT 3-mer [causal] | 1 | 1.912 | 0.02 ±0.06 | -0.02 ±0.03 | 1.96 |
| DNABERT 3-mer [causal] | 3 | 1.879 | 0.04 ±0.06 | 0.02 ±0.02 | 1.95 |
| DNABERT 3-mer [causal] | 8 | 1.604 | -0.11 ±0.06 | 0.18 ±0.19 | 1.77 |
| DNABERT 3-mer [causal] | 15 | 1.573 | -0.09 ±0.12 | 0.42 ±0.24 | 1.74 |
| DNABERT 3-mer [causal] | 30 | 1.589 | 0.03 ±0.18 | 0.93 ±0.21 | 1.77 |
| DNABERT 3-mer [causal] | 50 | 1.629 | 0.40 ±0.10 | 1.48 ±0.08 | 1.84 |
| DNABERT 4-mer [causal] | 0 | 2.619 | -0.00 ±0.09 | 0.02 ±0.12 | 2.57 |
| DNABERT 4-mer [causal] | 1 | 1.955 | 0.04 ±0.06 | 0.03 ±0.04 | 2.00 |
| DNABERT 4-mer [causal] | 3 | 1.877 | 0.04 ±0.04 | 0.03 ±0.02 | 1.95 |
| DNABERT 4-mer [causal] | 8 | 1.664 | -0.05 ±0.03 | 0.22 ±0.20 | 1.84 |
| DNABERT 4-mer [causal] | 15 | 1.630 | 0.00 ±0.08 | 0.45 ±0.20 | 1.83 |
| DNABERT 4-mer [causal] | 30 | 1.624 | 0.11 ±0.15 | 1.00 ±0.18 | 1.87 |
| DNABERT 4-mer [causal] | 50 | 1.669 | 0.44 ±0.12 | 1.51 ±0.06 | 1.90 |
| DNABERT 5-mer [causal] | 0 | 3.152 | 0.13 ±0.32 | 0.05 ±0.18 | 3.07 |
| DNABERT 5-mer [causal] | 1 | 1.998 | -0.01 ±0.07 | 0.01 ±0.05 | 2.06 |
| DNABERT 5-mer [causal] | 3 | 1.786 | 0.01 ±0.02 | 0.07 ±0.09 | 1.88 |
| DNABERT 5-mer [causal] | 8 | 1.644 | -0.01 ±0.03 | 0.24 ±0.19 | 1.83 |
| DNABERT 5-mer [causal] | 15 | 1.620 | -0.02 ±0.08 | 0.46 ±0.22 | 1.80 |
| DNABERT 5-mer [causal] | 30 | 1.627 | 0.10 ±0.16 | 0.99 ±0.18 | 1.84 |
| DNABERT 5-mer [causal] | 50 | 1.688 | 0.48 ±0.12 | 1.50 ±0.06 | 1.91 |
| DNABERT 6-mer [causal] | 0 | 4.473 | 0.50 ±0.45 | 0.28 ±0.39 | 4.94 |
| DNABERT 6-mer [causal] | 1 | 1.918 | -0.04 ±0.06 | 0.04 ±0.04 | 1.97 |
| DNABERT 6-mer [causal] | 3 | 1.638 | 0.01 ±0.06 | 0.21 ±0.22 | 1.87 |
| DNABERT 6-mer [causal] | 8 | 1.581 | -0.02 ±0.08 | 0.45 ±0.21 | 1.79 |
| DNABERT 6-mer [causal] | 15 | 1.576 | 0.04 ±0.13 | 0.73 ±0.24 | 1.80 |
| DNABERT 6-mer [causal] | 30 | 1.613 | 0.27 ±0.22 | 1.30 ±0.09 | 1.89 |
| DNABERT 6-mer [causal] | 50 | 1.702 | 0.75 ±0.08 | 1.70 ±0.04 | 1.99 |
| DNABERT-2 BPE [causal] | 0 | 2.566 | 0.04 ±0.09 | 0.10 ±0.09 | 2.56 |
| DNABERT-2 BPE [causal] | 1 | 1.883 | -0.02 ±0.02 | 0.04 ±0.05 | 1.90 |
| DNABERT-2 BPE [causal] | 3 | 1.677 | -0.07 ±0.06 | 0.17 ±0.07 | 1.78 |
| DNABERT-2 BPE [causal] | 8 | 1.602 | 0.04 ±0.11 | 0.93 ±0.15 | 1.77 |
| DNABERT-2 BPE [causal] | 15 | 1.634 | 0.30 ±0.18 | 1.55 ±0.10 | 1.84 |
| DNABERT-2 BPE [causal] | 30 | 1.801 | 1.17 ±0.19 | 1.93 ±0.11 | 2.05 |
| DNABERT-2 BPE [causal] | 50 | 2.157 | 2.21 ±0.08 | 2.38 ±0.06 | 2.41 |
| hyena_medium-160k | 0 | 1.680 | 0.00 ±0.05 | -0.00 ±0.06 | 1.76 |
| hyena_medium-160k | 1 | 1.636 | 0.01 ±0.06 | 0.07 ±0.07 | 1.74 |
| hyena_medium-160k | 3 | 1.606 | 0.04 ±0.05 | 0.34 ±0.07 | 1.73 |
| hyena_medium-160k | 8 | 1.603 | 0.13 ±0.05 | 1.26 ±0.05 | 1.73 |
| hyena_medium-160k | 15 | 1.623 | 0.30 ±0.05 | 1.49 ±0.04 | 1.77 |
| hyena_medium-160k | 30 | 1.752 | 0.75 ±0.08 | 1.76 ±0.06 | 1.96 |
| hyena_medium-160k | 50 | 2.185 | 1.61 ±0.12 | 2.39 ±0.09 | 2.53 |
