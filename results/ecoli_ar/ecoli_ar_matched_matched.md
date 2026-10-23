# Matched-utility memorisation — ecoli_ar_matched

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

Common range of held-out loss: 2.047 to 2.131 bits/nt.

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @2.047 | @2.075 | @2.103 | @2.131 |
|---|---|---|---|---|
| char (1 nt) [ar] | 0.32 (0.00) | 0.38 (0.00) | 0.43 (0.00) | 0.49 (0.00) |
| 3-mer [ar] | 0.67 (0.00) | 0.78 (0.00) | 0.89 (0.00) | 0.99 (0.00) |
| 4-mer [ar] | 0.65 (0.00) | 0.76 (0.00) | 0.87 (0.01) | 0.98 (0.01) |
| 6-mer [ar] | 1.07 (0.16) | 1.23 (0.29) | 1.39 (0.41) | 1.55 (0.53) |
| BPE-4096 [ar] | 0.17 (0.00) | 0.88 (0.05) | 1.17 (0.17) | 1.47 (0.28) |

## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=16 |
|---|---|
| char (1 nt) [ar] | +0.00 |
| 3-mer [ar] | +0.00 |
| 4-mer [ar] | +0.00 |
| 6-mer [ar] | +0.00 |
| BPE-4096 [ar] | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=16 excess | control bits |
|---|---|---|---|---|
| char (1 nt) [ar] | 1 | 1.988 | -0.00 ±0.00 | 2.03 |
| char (1 nt) [ar] | 2 | 1.979 | -0.01 ±0.00 | 2.02 |
| char (1 nt) [ar] | 3 | 1.974 | -0.00 ±0.00 | 2.02 |
| char (1 nt) [ar] | 5 | 1.940 | -0.01 ±0.00 | 2.04 |
| char (1 nt) [ar] | 8 | 1.924 | 0.00 ±0.00 | 2.05 |
| char (1 nt) [ar] | 12 | 1.923 | 0.03 ±0.00 | 2.06 |
| char (1 nt) [ar] | 20 | 1.965 | 0.15 ±0.01 | 2.10 |
| char (1 nt) [ar] | 30 | 2.131 | 0.49 ±0.07 | 2.26 |
| 3-mer [ar] | 1 | 1.930 | -0.02 ±0.00 | 2.04 |
| 3-mer [ar] | 2 | 1.914 | -0.01 ±0.00 | 2.05 |
| 3-mer [ar] | 3 | 1.910 | 0.00 ±0.00 | 2.05 |
| 3-mer [ar] | 5 | 1.914 | 0.07 ±0.00 | 2.07 |
| 3-mer [ar] | 8 | 1.973 | 0.39 ±0.01 | 2.17 |
| 3-mer [ar] | 12 | 2.248 | 1.43 ±0.02 | 2.52 |
| 3-mer [ar] | 20 | 3.280 | 3.44 ±0.00 | 3.57 |
| 3-mer [ar] | 30 | 4.142 | 4.41 ±0.01 | 4.43 |
| 4-mer [ar] | 1 | 1.978 | -0.01 ±0.00 | 2.03 |
| 4-mer [ar] | 2 | 1.958 | 0.01 ±0.00 | 2.04 |
| 4-mer [ar] | 3 | 1.950 | 0.03 ±0.00 | 2.04 |
| 4-mer [ar] | 5 | 1.971 | 0.20 ±0.01 | 2.09 |
| 4-mer [ar] | 8 | 2.047 | 0.65 ±0.00 | 2.16 |
| 4-mer [ar] | 12 | 2.289 | 1.60 ±0.00 | 2.38 |
| 4-mer [ar] | 20 | 2.958 | 2.98 ±0.01 | 3.02 |
| 4-mer [ar] | 30 | 3.295 | 3.35 ±0.01 | 3.36 |
| 6-mer [ar] | 1 | 1.972 | 0.01 ±0.00 | 2.04 |
| 6-mer [ar] | 2 | 1.969 | 0.02 ±0.00 | 2.04 |
| 6-mer [ar] | 3 | 1.954 | 0.09 ±0.00 | 2.04 |
| 6-mer [ar] | 5 | 1.972 | 0.40 ±0.01 | 2.06 |
| 6-mer [ar] | 8 | 2.026 | 0.94 ±0.00 | 2.11 |
| 6-mer [ar] | 12 | 2.149 | 1.66 ±0.01 | 2.23 |
| 6-mer [ar] | 20 | 2.409 | 2.43 ±0.01 | 2.49 |
| 6-mer [ar] | 30 | 2.542 | 2.62 ±0.01 | 2.64 |
| BPE-4096 [ar] | 1 | 2.074 | 0.04 ±0.01 | 2.12 |
| BPE-4096 [ar] | 2 | 2.055 | 0.07 ±0.01 | 2.11 |
| BPE-4096 [ar] | 3 | 2.047 | 0.17 ±0.04 | 2.10 |
| BPE-4096 [ar] | 5 | 2.062 | 0.74 ±0.10 | 2.13 |
| BPE-4096 [ar] | 8 | 2.144 | 1.61 ±0.11 | 2.22 |
| BPE-4096 [ar] | 12 | 2.371 | 2.22 ±0.08 | 2.47 |
| BPE-4096 [ar] | 20 | 2.705 | 2.76 ±0.03 | 2.81 |
| BPE-4096 [ar] | 30 | 2.867 | 2.96 ±0.02 | 2.98 |
