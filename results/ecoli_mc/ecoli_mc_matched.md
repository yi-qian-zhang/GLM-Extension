# Matched-utility memorisation — ecoli_mc

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.954 to 2.250 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.954 | @2.053 | @2.151 | @2.250 |
|---|---|---|---|---|
| 3-mer [ar] | 0.22 (0.00) | 0.57 (0.00) | 0.90 (0.00) | 1.17 (0.00) |
| 4-mer [ar] | 0.04 (0.00) | 0.53 (0.00) | 0.92 (0.00) | 1.29 (0.01) |
| 6-mer [ar] | 0.05 (0.00) | 0.87 (0.03) | 1.42 (0.13) | 1.80 (0.46) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.954 | @2.053 | @2.151 | @2.250 |
|---|---|---|---|---|
| 3-mer [ar] | 0.28 (0.00) | 0.68 (0.00) | 1.05 (0.00) | 1.32 (0.00) |
| 4-mer [ar] | 0.06 (0.00) | 0.67 (0.00) | 1.07 (0.01) | 1.45 (0.05) |
| 6-mer [ar] | 0.09 (0.00) | 1.10 (0.19) | 1.67 (0.61) | 1.96 (0.76) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| 3-mer [ar] | +0.00 | +0.00 |
| 4-mer [ar] | +0.00 | +0.00 |
| 6-mer [ar] | +0.00 | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| 3-mer [ar] | 1 | 1.930 | -0.01 ±0.00 | -0.02 ±0.00 | 2.04 |
| 3-mer [ar] | 2 | 1.914 | -0.01 ±0.00 | -0.01 ±0.00 | 2.05 |
| 3-mer [ar] | 3 | 1.910 | 0.00 ±0.00 | 0.00 ±0.00 | 2.05 |
| 3-mer [ar] | 5 | 1.914 | 0.05 ±0.00 | 0.07 ±0.00 | 2.07 |
| 3-mer [ar] | 8 | 1.976 | 0.31 ±0.02 | 0.40 ±0.02 | 2.17 |
| 3-mer [ar] | 12 | 2.150 | 0.90 ±0.03 | 1.04 ±0.03 | 2.39 |
| 3-mer [ar] | 15 | 2.250 | 1.17 ±0.03 | 1.32 ±0.02 | 2.49 |
| 4-mer [ar] | 1 | 1.978 | -0.01 ±0.00 | -0.01 ±0.00 | 2.03 |
| 4-mer [ar] | 2 | 1.958 | 0.01 ±0.00 | 0.01 ±0.00 | 2.04 |
| 4-mer [ar] | 3 | 1.950 | 0.02 ±0.00 | 0.03 ±0.00 | 2.04 |
| 4-mer [ar] | 5 | 1.972 | 0.13 ±0.01 | 0.20 ±0.01 | 2.09 |
| 4-mer [ar] | 8 | 2.043 | 0.49 ±0.02 | 0.63 ±0.00 | 2.16 |
| 4-mer [ar] | 12 | 2.225 | 1.21 ±0.02 | 1.37 ±0.00 | 2.31 |
| 4-mer [ar] | 20 | 2.505 | 2.10 ±0.00 | 2.19 ±0.00 | 2.56 |
| 6-mer [ar] | 1 | 1.972 | 0.00 ±0.00 | 0.01 ±0.00 | 2.04 |
| 6-mer [ar] | 2 | 1.969 | 0.01 ±0.00 | 0.02 ±0.00 | 2.04 |
| 6-mer [ar] | 3 | 1.954 | 0.05 ±0.00 | 0.09 ±0.00 | 2.04 |
| 6-mer [ar] | 5 | 1.972 | 0.27 ±0.01 | 0.40 ±0.01 | 2.06 |
| 6-mer [ar] | 8 | 2.026 | 0.71 ±0.00 | 0.94 ±0.00 | 2.11 |
| 6-mer [ar] | 12 | 2.149 | 1.42 ±0.00 | 1.66 ±0.01 | 2.23 |
| 6-mer [ar] | 20 | 2.409 | 2.41 ±0.01 | 2.43 ±0.01 | 2.49 |
| 6-mer [ar] | 30 | 2.542 | 2.62 ±0.01 | 2.62 ±0.01 | 2.64 |
