# Matched-utility memorisation — gue_long

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 3.322 to 3.458 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @3.322 | @3.367 | @3.413 | @3.458 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.30 (0.05) | 2.37 (0.05) | 2.43 (0.05) | 2.50 (0.05) |
| 3-mer [ar] | 3.26 (0.18) | 3.32 (0.19) | 3.37 (0.20) | 3.43 (0.21) |
| 4-mer [ar] | 3.33 (0.83) | 3.38 (0.83) | 3.43 (0.83) | 3.48 (0.84) |
| 6-mer [ar] | 3.41 (1.00) | 3.46 (1.00) | 3.51 (1.00) | 3.56 (1.00) |
| BPE-4096 [ar] | 3.51 (0.96) | 3.56 (0.97) | 3.62 (0.97) | 3.68 (0.97) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @3.322 | @3.367 | @3.413 | @3.458 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.32 (0.04) | 2.39 (0.05) | 2.45 (0.05) | 2.52 (0.05) |
| 3-mer [ar] | 3.30 (0.30) | 3.35 (0.31) | 3.41 (0.32) | 3.46 (0.33) |
| 4-mer [ar] | 3.33 (0.86) | 3.38 (0.86) | 3.43 (0.86) | 3.48 (0.86) |
| 6-mer [ar] | 3.41 (1.00) | 3.46 (1.00) | 3.50 (1.00) | 3.56 (1.00) |
| BPE-4096 [ar] | 3.51 (0.98) | 3.56 (0.98) | 3.62 (0.99) | 3.67 (0.99) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| char (1 nt) [ar] | +0.00 | +0.00 |
| 3-mer [ar] | +0.00 | +0.00 |
| 4-mer [ar] | +0.00 | +0.00 |
| 6-mer [ar] | +0.00 | +0.00 |
| BPE-4096 [ar] | +0.00 | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| char (1 nt) [ar] | 20 | 1.957 | 0.06 ±0.00 | 0.06 ±0.01 | 2.04 |
| char (1 nt) [ar] | 30 | 1.991 | 0.13 ±0.00 | 0.13 ±0.00 | 2.07 |
| char (1 nt) [ar] | 50 | 2.511 | 1.14 ±0.11 | 1.16 ±0.13 | 2.55 |
| char (1 nt) [ar] | 80 | 6.179 | 6.41 ±0.24 | 6.42 ±0.25 | 6.57 |
| char (1 nt) [ar] | 110 | 8.697 | 9.14 ±0.21 | 9.14 ±0.21 | 9.17 |
| char (1 nt) [ar] | 150 | 10.291 | 10.78 ±0.16 | 10.78 ±0.16 | 10.79 |
| 3-mer [ar] | 20 | 3.322 | 3.26 ±0.08 | 3.30 ±0.07 | 3.50 |
| 3-mer [ar] | 30 | 4.318 | 4.49 ±0.02 | 4.50 ±0.02 | 4.58 |
| 3-mer [ar] | 50 | 5.087 | 5.32 ±0.04 | 5.32 ±0.04 | 5.35 |
| 3-mer [ar] | 80 | 5.742 | 6.09 ±0.02 | 6.09 ±0.01 | 6.10 |
| 3-mer [ar] | 110 | 6.135 | 6.47 ±0.01 | 6.47 ±0.01 | 6.48 |
| 3-mer [ar] | 150 | 6.220 | 6.56 ±0.03 | 6.56 ±0.03 | 6.56 |
| 4-mer [ar] | 20 | 3.129 | 3.11 ±0.02 | 3.12 ±0.02 | 3.18 |
| 4-mer [ar] | 30 | 3.759 | 3.81 ±0.03 | 3.81 ±0.03 | 3.84 |
| 4-mer [ar] | 50 | 4.348 | 4.46 ±0.02 | 4.46 ±0.02 | 4.47 |
| 4-mer [ar] | 80 | 4.799 | 4.93 ±0.00 | 4.93 ±0.00 | 4.94 |
| 4-mer [ar] | 110 | 4.966 | 5.09 ±0.02 | 5.09 ±0.02 | 5.10 |
| 4-mer [ar] | 150 | 4.971 | 5.12 ±0.01 | 5.11 ±0.01 | 5.12 |
| 6-mer [ar] | 20 | 2.534 | 2.58 ±0.00 | 2.58 ±0.00 | 2.60 |
| 6-mer [ar] | 30 | 2.848 | 2.92 ±0.01 | 2.92 ±0.01 | 2.93 |
| 6-mer [ar] | 50 | 3.215 | 3.31 ±0.04 | 3.31 ±0.04 | 3.31 |
| 6-mer [ar] | 80 | 3.433 | 3.53 ±0.03 | 3.52 ±0.03 | 3.53 |
| 6-mer [ar] | 110 | 3.458 | 3.56 ±0.01 | 3.56 ±0.01 | 3.56 |
| 6-mer [ar] | 150 | 3.439 | 3.53 ±0.01 | 3.53 ±0.01 | 3.53 |
| BPE-4096 [ar] | 20 | 2.843 | 2.90 ±0.01 | 2.95 ±0.01 | 2.98 |
| BPE-4096 [ar] | 30 | 3.280 | 3.46 ±0.02 | 3.46 ±0.02 | 3.47 |
| BPE-4096 [ar] | 50 | 3.731 | 4.01 ±0.04 | 4.01 ±0.03 | 4.02 |
| BPE-4096 [ar] | 80 | 3.988 | 4.27 ±0.04 | 4.27 ±0.04 | 4.28 |
| BPE-4096 [ar] | 110 | 4.036 | 4.27 ±0.01 | 4.27 ±0.01 | 4.27 |
| BPE-4096 [ar] | 150 | 4.023 | 4.27 ±0.00 | 4.26 ±0.00 | 4.27 |
