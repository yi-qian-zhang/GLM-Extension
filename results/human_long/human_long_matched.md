# Matched-utility memorisation — human_long

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 2.393 to 3.190 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @2.393 | @2.659 | @2.925 | @3.190 |
|---|---|---|---|---|
| char (1 nt) | 1.53 (0.02) | 2.04 (0.03) | 2.54 (0.04) | 3.05 (0.04) |
| 6-mer | 2.50 (1.00) | 2.81 (1.00) | 3.11 (1.00) | 3.36 (1.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @2.393 | @2.659 | @2.925 | @3.190 |
|---|---|---|---|---|
| char (1 nt) | 1.98 (0.28) | 2.46 (0.37) | 2.94 (0.46) | 3.42 (0.55) |
| 6-mer | 2.50 (1.00) | 2.81 (1.00) | 3.10 (1.00) | 3.36 (1.00) |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| char (1 nt) | 20 | 1.773 | 0.09 | 0.17 | 1.91 |
| char (1 nt) | 30 | 1.761 | 0.32 | 0.83 | 1.94 |
| char (1 nt) | 50 | 3.410 | 3.47 | 3.82 | 3.96 |
| char (1 nt) | 80 | 7.064 | 7.96 | 7.99 | 8.02 |
| char (1 nt) | 110 | 8.956 | 10.19 | 10.20 | 10.21 |
| char (1 nt) | 150 | 10.233 | 11.63 | 11.63 | 11.63 |
| 6-mer | 20 | 2.393 | 2.50 | 2.50 | 2.52 |
| 6-mer | 30 | 2.668 | 2.82 | 2.82 | 2.83 |
| 6-mer | 50 | 2.967 | 3.15 | 3.15 | 3.16 |
| 6-mer | 80 | 3.172 | 3.36 | 3.35 | 3.36 |
| 6-mer | 110 | 3.190 | 3.36 | 3.36 | 3.36 |
| 6-mer | 150 | 3.168 | 3.35 | 3.35 | 3.35 |
