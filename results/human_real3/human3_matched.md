# Matched-utility memorisation — human3

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.655 to 1.664 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.655 | @1.658 | @1.661 | @1.664 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0.33 (0.00) | 0.36 (0.00) | 0.40 (0.00) | 0.44 (0.00) |
| DNABERT 4-mer [causal] | -0.02 (0.00) | 0.01 (0.00) | 0.04 (0.00) | 0.07 (0.00) |
| DNABERT 5-mer [causal] | -0.00 (0.00) | 0.02 (0.00) | 0.04 (0.00) | 0.06 (0.00) |
| DNABERT 6-mer [causal] | 0.19 (0.01) | 0.21 (0.01) | 0.24 (0.01) | 0.26 (0.02) |
| DNABERT-2 BPE [causal] | 0.14 (0.00) | 0.16 (0.00) | 0.18 (0.00) | 0.19 (0.00) |
| hyena_medium-160k | 0.31 (0.00) | 0.32 (0.00) | 0.33 (0.00) | 0.34 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.655 | @1.658 | @1.661 | @1.664 |
|---|---|---|---|---|
| DNABERT 3-mer [causal] | 1.46 (0.89) | 1.49 (0.92) | 1.52 (0.95) | 1.55 (0.97) |
| DNABERT 4-mer [causal] | 1.15 (0.60) | 1.17 (0.62) | 1.19 (0.63) | 1.21 (0.65) |
| DNABERT 5-mer [causal] | 1.17 (0.57) | 1.18 (0.57) | 1.19 (0.58) | 1.21 (0.58) |
| DNABERT 6-mer [causal] | 1.43 (0.66) | 1.44 (0.67) | 1.45 (0.68) | 1.46 (0.69) |
| DNABERT-2 BPE [causal] | 1.52 (0.81) | 1.56 (0.84) | 1.60 (0.87) | 1.61 (0.87) |
| hyena_medium-160k | 1.50 (0.66) | 1.51 (0.66) | 1.52 (0.66) | 1.52 (0.66) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer [causal] | +0.41 | +0.01 |
| DNABERT 4-mer [causal] | -0.02 | +0.05 |
| DNABERT 5-mer [causal] | +0.10 | +0.06 |
| DNABERT 6-mer [causal] | +0.75 | +0.21 |
| DNABERT-2 BPE [causal] | +0.03 | +0.15 |
| hyena_medium-160k | +0.04 | +0.05 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer [causal] | 0 | 2.869 | 0.41 ±0.22 | 0.01 ±0.22 | 3.00 |
| DNABERT 3-mer [causal] | 1 | 1.908 | 0.04 ±0.02 | -0.00 ±0.02 | 1.98 |
| DNABERT 3-mer [causal] | 3 | 1.877 | 0.05 ±0.01 | 0.02 ±0.01 | 1.97 |
| DNABERT 3-mer [causal] | 8 | 1.623 | -0.15 ±0.01 | 0.37 ±0.02 | 1.82 |
| DNABERT 3-mer [causal] | 15 | 1.596 | -0.19 ±0.01 | 0.66 ±0.02 | 1.75 |
| DNABERT 3-mer [causal] | 30 | 1.621 | -0.11 ±0.00 | 1.11 ±0.02 | 1.78 |
| DNABERT 3-mer [causal] | 50 | 1.664 | 0.44 ±0.01 | 1.55 ±0.01 | 1.88 |
| DNABERT 4-mer [causal] | 0 | 2.624 | -0.02 ±0.07 | 0.05 ±0.07 | 2.58 |
| DNABERT 4-mer [causal] | 1 | 1.946 | 0.06 ±0.01 | 0.06 ±0.01 | 2.02 |
| DNABERT 4-mer [causal] | 3 | 1.876 | 0.06 ±0.00 | 0.05 ±0.00 | 1.97 |
| DNABERT 4-mer [causal] | 8 | 1.691 | -0.07 ±0.01 | 0.41 ±0.02 | 1.92 |
| DNABERT 4-mer [causal] | 15 | 1.661 | -0.07 ±0.02 | 0.63 ±0.04 | 1.89 |
| DNABERT 4-mer [causal] | 30 | 1.655 | -0.02 ±0.04 | 1.15 ±0.06 | 1.90 |
| DNABERT 4-mer [causal] | 50 | 1.704 | 0.45 ±0.02 | 1.52 ±0.02 | 1.91 |
| DNABERT 5-mer [causal] | 0 | 3.139 | 0.10 ±0.05 | 0.06 ±0.05 | 3.05 |
| DNABERT 5-mer [causal] | 1 | 2.005 | -0.00 ±0.01 | 0.03 ±0.01 | 2.08 |
| DNABERT 5-mer [causal] | 3 | 1.790 | 0.01 ±0.01 | 0.17 ±0.01 | 1.94 |
| DNABERT 5-mer [causal] | 8 | 1.675 | -0.01 ±0.03 | 0.42 ±0.04 | 1.92 |
| DNABERT 5-mer [causal] | 15 | 1.652 | -0.08 ±0.03 | 0.68 ±0.01 | 1.87 |
| DNABERT 5-mer [causal] | 30 | 1.653 | -0.01 ±0.02 | 1.16 ±0.02 | 1.90 |
| DNABERT 5-mer [causal] | 50 | 1.726 | 0.48 ±0.03 | 1.49 ±0.03 | 1.93 |
| DNABERT 6-mer [causal] | 0 | 4.483 | 0.75 ±0.28 | 0.21 ±0.28 | 4.97 |
| DNABERT 6-mer [causal] | 1 | 1.930 | -0.05 ±0.01 | 0.08 ±0.00 | 2.01 |
| DNABERT 6-mer [causal] | 3 | 1.667 | 0.05 ±0.04 | 0.43 ±0.06 | 1.98 |
| DNABERT 6-mer [causal] | 8 | 1.609 | -0.07 ±0.00 | 0.65 ±0.01 | 1.84 |
| DNABERT 6-mer [causal] | 15 | 1.605 | -0.06 ±0.04 | 0.97 ±0.03 | 1.84 |
| DNABERT 6-mer [causal] | 30 | 1.642 | 0.09 ±0.03 | 1.37 ±0.03 | 1.93 |
| DNABERT 6-mer [causal] | 50 | 1.728 | 0.76 ±0.02 | 1.73 ±0.02 | 2.01 |
| DNABERT-2 BPE [causal] | 0 | 2.574 | 0.03 ±0.03 | 0.15 ±0.03 | 2.58 |
| DNABERT-2 BPE [causal] | 1 | 1.884 | -0.02 ±0.00 | 0.08 ±0.01 | 1.91 |
| DNABERT-2 BPE [causal] | 3 | 1.703 | -0.11 ±0.01 | 0.23 ±0.02 | 1.82 |
| DNABERT-2 BPE [causal] | 8 | 1.626 | -0.03 ±0.02 | 1.08 ±0.02 | 1.82 |
| DNABERT-2 BPE [causal] | 15 | 1.660 | 0.17 ±0.02 | 1.60 ±0.02 | 1.89 |
| DNABERT-2 BPE [causal] | 30 | 1.832 | 1.07 ±0.01 | 1.97 ±0.02 | 2.10 |
| DNABERT-2 BPE [causal] | 50 | 2.199 | 2.27 ±0.01 | 2.42 ±0.01 | 2.45 |
| hyena_medium-160k | 0 | 1.661 | 0.04 ±0.01 | 0.05 ±0.01 | 1.80 |
| hyena_medium-160k | 1 | 1.636 | 0.06 ±0.01 | 0.14 ±0.00 | 1.78 |
| hyena_medium-160k | 3 | 1.623 | 0.08 ±0.00 | 0.39 ±0.01 | 1.76 |
| hyena_medium-160k | 8 | 1.627 | 0.15 ±0.00 | 1.30 ±0.01 | 1.75 |
| hyena_medium-160k | 15 | 1.652 | 0.30 ±0.01 | 1.50 ±0.01 | 1.79 |
| hyena_medium-160k | 30 | 1.786 | 0.73 ±0.03 | 1.77 ±0.02 | 1.97 |
| hyena_medium-160k | 50 | 2.230 | 1.58 ±0.01 | 2.39 ±0.01 | 2.52 |
