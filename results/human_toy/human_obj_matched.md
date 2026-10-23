# Matched-utility memorisation — human_obj

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 1.874 to 2.348 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.874 | @2.032 | @2.190 | @2.348 |
|---|---|---|---|---|
| 3-mer [ar] | 0.69 (0.01) | 1.24 (0.03) | 1.58 (0.11) | 1.87 (0.20) |
| 4-mer [ar] | 0.73 (0.00) | 1.29 (0.04) | 1.83 (0.08) | 2.12 (0.30) |
| 6-mer [ar] | 0.47 (0.00) | 1.57 (0.18) | 2.11 (0.78) | 2.45 (1.00) |
| BPE-4096 [ar] | 0.33 (0.00) | 1.13 (0.01) | 1.68 (0.04) | 2.12 (0.42) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.874 | @2.032 | @2.190 | @2.348 |
|---|---|---|---|---|
| 3-mer [ar] | 1.00 (0.13) | 1.60 (0.29) | 1.91 (0.39) | 2.15 (0.47) |
| 4-mer [ar] | 1.00 (0.04) | 1.54 (0.20) | 2.03 (0.37) | 2.27 (0.53) |
| 6-mer [ar] | 0.68 (0.02) | 1.76 (0.55) | 2.17 (0.88) | 2.45 (1.00) |
| BPE-4096 [ar] | 1.15 (0.11) | 1.84 (0.65) | 2.14 (0.75) | 2.37 (0.86) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| 3-mer [ar] | +0.00 | +0.00 |
| 4-mer [ar] | +0.00 | +0.00 |
| 6-mer [ar] | +0.00 | +0.00 |
| BPE-4096 [ar] | +0.00 | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| 3-mer [ar] | 1 | 1.908 | 0.00 ±0.00 | 0.02 ±0.00 | 1.93 |
| 3-mer [ar] | 2 | 1.887 | 0.02 ±0.01 | 0.05 ±0.01 | 1.93 |
| 3-mer [ar] | 3 | 1.850 | 0.04 ±0.01 | 0.08 ±0.00 | 1.91 |
| 3-mer [ar] | 5 | 1.774 | 0.11 ±0.01 | 0.20 ±0.01 | 1.87 |
| 3-mer [ar] | 8 | 1.797 | 0.41 ±0.01 | 0.70 ±0.00 | 1.92 |
| 3-mer [ar] | 12 | 2.058 | 1.33 ±0.00 | 1.70 ±0.03 | 2.24 |
| 3-mer [ar] | 20 | 3.148 | 3.35 ±0.04 | 3.40 ±0.04 | 3.45 |
| 3-mer [ar] | 30 | 3.921 | 4.23 ±0.05 | 4.24 ±0.05 | 4.24 |
| 4-mer [ar] | 1 | 1.924 | -0.00 ±0.00 | 0.01 ±0.00 | 1.95 |
| 4-mer [ar] | 2 | 1.876 | 0.03 ±0.00 | 0.07 ±0.01 | 1.93 |
| 4-mer [ar] | 3 | 1.828 | 0.07 ±0.00 | 0.13 ±0.01 | 1.90 |
| 4-mer [ar] | 5 | 1.785 | 0.22 ±0.02 | 0.36 ±0.02 | 1.89 |
| 4-mer [ar] | 8 | 1.886 | 0.79 ±0.00 | 1.09 ±0.02 | 2.01 |
| 4-mer [ar] | 12 | 2.191 | 1.84 ±0.02 | 2.04 ±0.02 | 2.33 |
| 4-mer [ar] | 20 | 2.822 | 2.97 ±0.01 | 2.97 ±0.01 | 2.99 |
| 4-mer [ar] | 30 | 3.051 | 3.23 ±0.02 | 3.23 ±0.02 | 3.24 |
| 6-mer [ar] | 1 | 1.945 | 0.00 ±0.00 | 0.02 ±0.00 | 1.96 |
| 6-mer [ar] | 2 | 1.915 | 0.02 ±0.00 | 0.05 ±0.00 | 1.95 |
| 6-mer [ar] | 3 | 1.883 | 0.10 ±0.00 | 0.18 ±0.00 | 1.92 |
| 6-mer [ar] | 5 | 1.862 | 0.31 ±0.00 | 0.50 ±0.00 | 1.92 |
| 6-mer [ar] | 8 | 1.899 | 0.80 ±0.01 | 1.06 ±0.01 | 1.97 |
| 6-mer [ar] | 12 | 2.019 | 1.53 ±0.02 | 1.73 ±0.01 | 2.11 |
| 6-mer [ar] | 20 | 2.249 | 2.31 ±0.01 | 2.32 ±0.01 | 2.35 |
| 6-mer [ar] | 30 | 2.348 | 2.45 ±0.01 | 2.45 ±0.01 | 2.46 |
| BPE-4096 [ar] | 1 | 2.030 | 0.01 ±0.00 | 0.04 ±0.00 | 2.03 |
| BPE-4096 [ar] | 2 | 1.949 | 0.05 ±0.01 | 0.18 ±0.01 | 1.99 |
| BPE-4096 [ar] | 3 | 1.892 | 0.12 ±0.01 | 0.49 ±0.01 | 1.96 |
| BPE-4096 [ar] | 5 | 1.874 | 0.33 ±0.02 | 1.15 ±0.02 | 1.96 |
| BPE-4096 [ar] | 8 | 1.972 | 0.92 ±0.02 | 1.73 ±0.01 | 2.06 |
| BPE-4096 [ar] | 12 | 2.221 | 1.79 ±0.01 | 2.19 ±0.01 | 2.33 |
| BPE-4096 [ar] | 20 | 2.536 | 2.60 ±0.01 | 2.64 ±0.01 | 2.66 |
| BPE-4096 [ar] | 30 | 2.675 | 2.80 ±0.01 | 2.80 ±0.01 | 2.81 |
