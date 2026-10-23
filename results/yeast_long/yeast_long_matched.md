# Matched-utility memorisation — yeast_long

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 3.372 to 3.518 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @3.372 | @3.421 | @3.470 | @3.518 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.50 (0.05) | 2.57 (0.06) | 2.63 (0.06) | 2.70 (0.06) |
| 3-mer [ar] | 3.41 (0.24) | 3.47 (0.25) | 3.53 (0.27) | 3.59 (0.28) |
| 4-mer [ar] | 3.44 (0.80) | 3.50 (0.81) | 3.55 (0.82) | 3.61 (0.82) |
| 6-mer [ar] | 3.50 (0.99) | 3.55 (1.00) | 3.60 (1.00) | 3.65 (1.00) |
| BPE-4096 [ar] | 3.49 (0.97) | 3.55 (0.97) | 3.60 (0.97) | 3.65 (0.97) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @3.372 | @3.421 | @3.470 | @3.518 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.52 (0.05) | 2.58 (0.06) | 2.65 (0.06) | 2.72 (0.06) |
| 3-mer [ar] | 3.43 (0.38) | 3.48 (0.39) | 3.54 (0.39) | 3.60 (0.40) |
| 4-mer [ar] | 3.44 (0.93) | 3.50 (0.93) | 3.55 (0.93) | 3.61 (0.93) |
| 6-mer [ar] | 3.49 (1.00) | 3.54 (1.00) | 3.59 (1.00) | 3.64 (1.00) |
| BPE-4096 [ar] | 3.50 (1.00) | 3.55 (1.00) | 3.60 (1.00) | 3.65 (1.00) |

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
| char (1 nt) [ar] | 20 | 1.952 | 0.06 ±0.00 | 0.07 ±0.00 | 2.06 |
| char (1 nt) [ar] | 30 | 1.991 | 0.14 ±0.00 | 0.15 ±0.01 | 2.10 |
| char (1 nt) [ar] | 50 | 2.637 | 1.46 ±0.01 | 1.48 ±0.02 | 2.78 |
| char (1 nt) [ar] | 80 | 6.311 | 6.64 ±0.09 | 6.64 ±0.09 | 6.77 |
| char (1 nt) [ar] | 110 | 8.483 | 9.16 ±0.04 | 9.16 ±0.04 | 9.18 |
| char (1 nt) [ar] | 150 | 9.906 | 10.67 ±0.06 | 10.67 ±0.06 | 10.68 |
| 3-mer [ar] | 20 | 3.372 | 3.41 ±0.05 | 3.43 ±0.04 | 3.60 |
| 3-mer [ar] | 30 | 4.342 | 4.57 ±0.04 | 4.57 ±0.03 | 4.65 |
| 3-mer [ar] | 50 | 5.129 | 5.48 ±0.05 | 5.47 ±0.05 | 5.51 |
| 3-mer [ar] | 80 | 5.838 | 6.23 ±0.06 | 6.23 ±0.06 | 6.24 |
| 3-mer [ar] | 110 | 6.228 | 6.66 ±0.10 | 6.65 ±0.10 | 6.66 |
| 3-mer [ar] | 150 | 6.320 | 6.69 ±0.14 | 6.68 ±0.14 | 6.69 |
| 4-mer [ar] | 20 | 3.190 | 3.24 ±0.02 | 3.24 ±0.02 | 3.30 |
| 4-mer [ar] | 30 | 3.791 | 3.91 ±0.01 | 3.91 ±0.01 | 3.94 |
| 4-mer [ar] | 50 | 4.381 | 4.61 ±0.00 | 4.61 ±0.00 | 4.62 |
| 4-mer [ar] | 80 | 4.825 | 5.08 ±0.02 | 5.07 ±0.02 | 5.08 |
| 4-mer [ar] | 110 | 4.997 | 5.28 ±0.03 | 5.27 ±0.03 | 5.28 |
| 4-mer [ar] | 150 | 4.994 | 5.24 ±0.06 | 5.24 ±0.06 | 5.25 |
| 6-mer [ar] | 20 | 2.577 | 2.65 ±0.01 | 2.65 ±0.01 | 2.67 |
| 6-mer [ar] | 30 | 2.916 | 3.01 ±0.03 | 3.01 ±0.03 | 3.02 |
| 6-mer [ar] | 50 | 3.282 | 3.40 ±0.01 | 3.40 ±0.01 | 3.41 |
| 6-mer [ar] | 80 | 3.487 | 3.62 ±0.01 | 3.61 ±0.01 | 3.62 |
| 6-mer [ar] | 110 | 3.518 | 3.65 ±0.00 | 3.64 ±0.00 | 3.65 |
| 6-mer [ar] | 150 | 3.495 | 3.60 ±0.01 | 3.60 ±0.01 | 3.61 |
| BPE-4096 [ar] | 20 | 2.897 | 2.91 ±0.03 | 2.98 ±0.02 | 3.02 |
| BPE-4096 [ar] | 30 | 3.344 | 3.46 ±0.02 | 3.47 ±0.02 | 3.48 |
| BPE-4096 [ar] | 50 | 3.830 | 3.98 ±0.02 | 3.98 ±0.02 | 3.99 |
| BPE-4096 [ar] | 80 | 4.111 | 4.28 ±0.03 | 4.27 ±0.03 | 4.28 |
| BPE-4096 [ar] | 110 | 4.160 | 4.36 ±0.00 | 4.36 ±0.00 | 4.36 |
| BPE-4096 [ar] | 150 | 4.155 | 4.35 ±0.01 | 4.35 ±0.01 | 4.35 |
