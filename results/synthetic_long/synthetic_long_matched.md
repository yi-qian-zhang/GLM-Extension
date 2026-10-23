# Matched-utility memorisation — synthetic_long

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 3.516 to 3.664 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @3.516 | @3.565 | @3.615 | @3.664 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.47 (0.06) | 2.54 (0.07) | 2.61 (0.07) | 2.67 (0.07) |
| 3-mer [ar] | 3.37 (0.15) | 3.43 (0.17) | 3.49 (0.19) | 3.55 (0.22) |
| 4-mer [ar] | 3.52 (0.86) | 3.57 (0.86) | 3.62 (0.86) | 3.67 (0.86) |
| 6-mer [ar] | 3.57 (1.00) | 3.62 (1.00) | 3.67 (1.00) | 3.71 (1.00) |
| BPE-4096 [ar] | 3.56 (1.00) | 3.61 (0.99) | 3.66 (0.99) | 3.71 (0.99) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @3.516 | @3.565 | @3.615 | @3.664 |
|---|---|---|---|---|
| char (1 nt) [ar] | 2.46 (0.07) | 2.53 (0.07) | 2.59 (0.08) | 2.66 (0.08) |
| 3-mer [ar] | 3.40 (0.22) | 3.45 (0.24) | 3.51 (0.25) | 3.56 (0.27) |
| 4-mer [ar] | 3.52 (0.87) | 3.57 (0.87) | 3.62 (0.88) | 3.67 (0.88) |
| 6-mer [ar] | 3.56 (1.00) | 3.61 (1.00) | 3.66 (1.00) | 3.70 (1.00) |
| BPE-4096 [ar] | 3.57 (0.99) | 3.62 (0.99) | 3.67 (0.99) | 3.72 (0.99) |

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
| char (1 nt) [ar] | 20 | 2.020 | 0.05 ±0.00 | 0.05 ±0.00 | 2.02 |
| char (1 nt) [ar] | 30 | 2.044 | 0.12 ±0.01 | 0.12 ±0.01 | 2.05 |
| char (1 nt) [ar] | 50 | 2.636 | 1.28 ±0.06 | 1.27 ±0.05 | 2.67 |
| char (1 nt) [ar] | 80 | 6.359 | 6.33 ±0.09 | 6.32 ±0.10 | 6.45 |
| char (1 nt) [ar] | 110 | 8.406 | 8.52 ±0.13 | 8.51 ±0.14 | 8.54 |
| char (1 nt) [ar] | 150 | 9.787 | 9.99 ±0.13 | 9.99 ±0.13 | 10.00 |
| 3-mer [ar] | 20 | 3.516 | 3.37 ±0.04 | 3.40 ±0.02 | 3.58 |
| 3-mer [ar] | 30 | 4.403 | 4.40 ±0.01 | 4.40 ±0.01 | 4.47 |
| 3-mer [ar] | 50 | 5.132 | 5.18 ±0.02 | 5.18 ±0.02 | 5.21 |
| 3-mer [ar] | 80 | 5.805 | 5.89 ±0.03 | 5.89 ±0.03 | 5.90 |
| 3-mer [ar] | 110 | 6.225 | 6.35 ±0.04 | 6.35 ±0.04 | 6.35 |
| 3-mer [ar] | 150 | 6.348 | 6.47 ±0.00 | 6.47 ±0.00 | 6.47 |
| 4-mer [ar] | 20 | 3.299 | 3.30 ±0.01 | 3.30 ±0.01 | 3.34 |
| 4-mer [ar] | 30 | 3.909 | 3.92 ±0.03 | 3.92 ±0.03 | 3.95 |
| 4-mer [ar] | 50 | 4.498 | 4.52 ±0.01 | 4.52 ±0.01 | 4.53 |
| 4-mer [ar] | 80 | 4.947 | 4.99 ±0.01 | 4.99 ±0.01 | 4.99 |
| 4-mer [ar] | 110 | 5.103 | 5.17 ±0.05 | 5.17 ±0.05 | 5.17 |
| 4-mer [ar] | 150 | 5.060 | 5.14 ±0.04 | 5.14 ±0.04 | 5.15 |
| 6-mer [ar] | 20 | 2.626 | 2.62 ±0.01 | 2.62 ±0.01 | 2.64 |
| 6-mer [ar] | 30 | 2.980 | 3.01 ±0.00 | 3.00 ±0.01 | 3.01 |
| 6-mer [ar] | 50 | 3.393 | 3.44 ±0.01 | 3.44 ±0.01 | 3.45 |
| 6-mer [ar] | 80 | 3.627 | 3.68 ±0.02 | 3.67 ±0.02 | 3.68 |
| 6-mer [ar] | 110 | 3.664 | 3.71 ±0.02 | 3.70 ±0.02 | 3.71 |
| 6-mer [ar] | 150 | 3.653 | 3.69 ±0.02 | 3.69 ±0.02 | 3.69 |
| BPE-4096 [ar] | 20 | 2.949 | 2.87 ±0.00 | 2.94 ±0.01 | 2.97 |
| BPE-4096 [ar] | 30 | 3.431 | 3.47 ±0.01 | 3.48 ±0.01 | 3.49 |
| BPE-4096 [ar] | 50 | 3.959 | 4.02 ±0.02 | 4.02 ±0.01 | 4.03 |
| BPE-4096 [ar] | 80 | 4.249 | 4.27 ±0.01 | 4.27 ±0.01 | 4.27 |
| BPE-4096 [ar] | 110 | 4.303 | 4.36 ±0.01 | 4.36 ±0.01 | 4.37 |
| BPE-4096 [ar] | 150 | 4.287 | 4.34 ±0.01 | 4.34 ±0.01 | 4.34 |
