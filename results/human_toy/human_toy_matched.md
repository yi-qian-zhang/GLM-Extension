# Matched-utility memorisation — human_toy

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.878 to 2.347 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.878 | @2.034 | @2.191 | @2.347 |
|---|---|---|---|---|
| 3-mer | 0.71 (0.01) | 1.27 (0.04) | 1.59 (0.12) | 1.89 (0.21) |
| 6-mer | 0.52 (0.00) | 1.59 (0.19) | 2.12 (0.78) | 2.45 (1.00) |
| BPE-4096 | 0.32 (0.00) | 1.11 (0.01) | 1.68 (0.03) | 2.12 (0.40) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.878 | @2.034 | @2.191 | @2.347 |
|---|---|---|---|---|
| 3-mer | 1.02 (0.12) | 1.64 (0.32) | 1.93 (0.41) | 2.17 (0.48) |
| 6-mer | 0.74 (0.02) | 1.77 (0.55) | 2.17 (0.88) | 2.45 (1.00) |
| BPE-4096 | 1.13 (0.14) | 1.84 (0.66) | 2.14 (0.77) | 2.37 (0.88) |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| 3-mer | 1 | 1.908 | 0.00 | 0.02 | 1.93 |
| 3-mer | 2 | 1.888 | 0.02 | 0.05 | 1.93 |
| 3-mer | 3 | 1.851 | 0.04 | 0.08 | 1.91 |
| 3-mer | 5 | 1.775 | 0.11 | 0.20 | 1.87 |
| 3-mer | 8 | 1.795 | 0.41 | 0.70 | 1.92 |
| 3-mer | 12 | 2.051 | 1.33 | 1.71 | 2.24 |
| 3-mer | 20 | 3.144 | 3.38 | 3.43 | 3.48 |
| 3-mer | 30 | 3.925 | 4.27 | 4.27 | 4.27 |
| 6-mer | 1 | 1.946 | 0.00 | 0.02 | 1.96 |
| 6-mer | 2 | 1.915 | 0.03 | 0.05 | 1.95 |
| 6-mer | 3 | 1.884 | 0.10 | 0.18 | 1.93 |
| 6-mer | 5 | 1.862 | 0.31 | 0.50 | 1.92 |
| 6-mer | 8 | 1.899 | 0.80 | 1.06 | 1.97 |
| 6-mer | 12 | 2.018 | 1.53 | 1.73 | 2.11 |
| 6-mer | 20 | 2.249 | 2.31 | 2.32 | 2.35 |
| 6-mer | 30 | 2.347 | 2.45 | 2.45 | 2.46 |
| BPE-4096 | 1 | 2.031 | 0.01 | 0.04 | 2.03 |
| BPE-4096 | 2 | 1.950 | 0.04 | 0.17 | 1.99 |
| BPE-4096 | 3 | 1.893 | 0.11 | 0.48 | 1.95 |
| BPE-4096 | 5 | 1.878 | 0.32 | 1.13 | 1.95 |
| BPE-4096 | 8 | 1.980 | 0.91 | 1.73 | 2.07 |
| BPE-4096 | 12 | 2.225 | 1.80 | 2.20 | 2.33 |
| BPE-4096 | 20 | 2.541 | 2.61 | 2.65 | 2.67 |
| BPE-4096 | 30 | 2.681 | 2.81 | 2.82 | 2.82 |
