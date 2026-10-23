# Matched-utility memorisation — ecoli_big

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.960 to 2.444 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.960 | @2.122 | @2.283 | @2.444 |
|---|---|---|---|---|
| char (1 nt) [ar] | 0.15 (0.00) | 0.49 (0.00) | 0.74 (0.00) | 0.99 (0.00) |
| 3-mer [ar] | 0.23 (0.00) | 0.80 (0.01) | 1.35 (0.01) | 1.90 (0.02) |
| 4-mer [ar] | 0.12 (0.00) | 0.78 (0.03) | 1.37 (0.21) | 1.96 (0.40) |
| 6-mer [ar] | 0.01 (0.00) | 1.45 (0.39) | 2.27 (1.00) | 2.52 (1.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.960 | @2.122 | @2.283 | @2.444 |
|---|---|---|---|---|
| char (1 nt) [ar] | 0.17 (0.00) | 0.55 (0.00) | 0.81 (0.00) | 1.06 (0.00) |
| 3-mer [ar] | 0.29 (0.00) | 0.89 (0.02) | 1.45 (0.03) | 2.01 (0.05) |
| 4-mer [ar] | 0.16 (0.00) | 0.93 (0.03) | 1.49 (0.27) | 2.04 (0.51) |
| 6-mer [ar] | 0.02 (0.00) | 1.61 (0.57) | 2.29 (1.00) | 2.51 (1.00) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| char (1 nt) [ar] | +0.00 | +0.00 |
| 3-mer [ar] | +0.00 | +0.00 |
| 4-mer [ar] | +0.00 | +0.00 |
| 6-mer [ar] | +0.00 | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| char (1 nt) [ar] | 1 | 2.005 | -0.00 ±0.01 | -0.00 ±0.00 | 2.04 |
| char (1 nt) [ar] | 2 | 1.983 | -0.01 ±0.00 | -0.01 ±0.00 | 2.02 |
| char (1 nt) [ar] | 3 | 1.974 | -0.00 ±0.00 | -0.00 ±0.00 | 2.02 |
| char (1 nt) [ar] | 5 | 1.933 | -0.01 ±0.01 | -0.01 ±0.00 | 2.04 |
| char (1 nt) [ar] | 8 | 1.918 | 0.01 ±0.00 | 0.01 ±0.00 | 2.05 |
| char (1 nt) [ar] | 12 | 1.920 | 0.04 ±0.00 | 0.06 ±0.00 | 2.07 |
| char (1 nt) [ar] | 20 | 2.048 | 0.37 ±0.00 | 0.44 ±0.01 | 2.21 |
| char (1 nt) [ar] | 30 | 3.273 | 2.27 ±0.00 | 2.36 ±0.00 | 3.38 |
| 3-mer [ar] | 1 | 1.927 | -0.01 ±0.00 | -0.02 ±0.00 | 2.05 |
| 3-mer [ar] | 2 | 1.916 | -0.00 ±0.00 | -0.01 ±0.00 | 2.05 |
| 3-mer [ar] | 3 | 1.913 | 0.01 ±0.00 | 0.01 ±0.00 | 2.06 |
| 3-mer [ar] | 5 | 1.918 | 0.06 ±0.00 | 0.09 ±0.00 | 2.07 |
| 3-mer [ar] | 8 | 1.985 | 0.34 ±0.02 | 0.42 ±0.02 | 2.18 |
| 3-mer [ar] | 12 | 2.510 | 2.12 ±0.06 | 2.24 ±0.04 | 2.86 |
| 3-mer [ar] | 20 | 4.270 | 4.67 ±0.07 | 4.66 ±0.07 | 4.69 |
| 3-mer [ar] | 30 | 4.711 | 5.17 ±0.04 | 5.17 ±0.04 | 5.18 |
| 4-mer [ar] | 1 | 1.979 | -0.01 ±0.00 | -0.01 ±0.00 | 2.03 |
| 4-mer [ar] | 2 | 1.960 | 0.00 ±0.00 | 0.00 ±0.00 | 2.04 |
| 4-mer [ar] | 3 | 1.949 | 0.01 ±0.00 | 0.02 ±0.01 | 2.04 |
| 4-mer [ar] | 5 | 1.957 | 0.11 ±0.01 | 0.15 ±0.01 | 2.08 |
| 4-mer [ar] | 8 | 2.099 | 0.70 ±0.02 | 0.85 ±0.04 | 2.23 |
| 4-mer [ar] | 12 | 2.589 | 2.49 ±0.03 | 2.54 ±0.02 | 2.67 |
| 4-mer [ar] | 20 | 3.276 | 3.35 ±0.00 | 3.35 ±0.00 | 3.36 |
| 4-mer [ar] | 30 | 3.420 | 3.50 ±0.01 | 3.49 ±0.01 | 3.50 |
| 6-mer [ar] | 1 | 1.975 | 0.00 ±0.01 | 0.01 ±0.00 | 2.04 |
| 6-mer [ar] | 2 | 1.972 | 0.00 ±0.00 | 0.01 ±0.00 | 2.04 |
| 6-mer [ar] | 3 | 1.960 | 0.01 ±0.00 | 0.02 ±0.00 | 2.04 |
| 6-mer [ar] | 5 | 1.975 | 0.25 ±0.01 | 0.36 ±0.01 | 2.07 |
| 6-mer [ar] | 8 | 2.061 | 1.02 ±0.01 | 1.25 ±0.01 | 2.14 |
| 6-mer [ar] | 12 | 2.223 | 2.17 ±0.00 | 2.21 ±0.00 | 2.30 |
| 6-mer [ar] | 20 | 2.412 | 2.48 ±0.00 | 2.47 ±0.00 | 2.49 |
| 6-mer [ar] | 30 | 2.444 | 2.52 ±0.00 | 2.51 ±0.00 | 2.52 |
