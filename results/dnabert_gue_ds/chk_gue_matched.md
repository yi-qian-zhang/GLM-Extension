# Matched-utility memorisation — chk_gue

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned, minus its own value at epoch 0, where nothing is memorised and the reading is the fixed offset between the two canary groups. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.919 to 1.932 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.919 | @1.923 | @1.928 | @1.932 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.23 (0.00) | 0.25 (0.00) | 0.26 (0.00) | 0.28 (0.00) |
| DNABERT 4-mer | 0.03 (0.00) | 0.05 (0.00) | 0.08 (0.00) | 0.11 (0.00) |
| DNABERT 5-mer | 0.29 (0.00) | 0.31 (0.00) | 0.34 (0.00) | 0.36 (0.00) |
| DNABERT 6-mer | 0.47 (0.00) | 0.51 (0.00) | 0.54 (0.00) | 0.56 (0.00) |
| DNABERT-2 BPE | 0.19 (0.00) | 0.21 (0.00) | 0.23 (0.00) | 0.24 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.919 | @1.923 | @1.928 | @1.932 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.52 (0.02) | 0.57 (0.02) | 0.63 (0.02) | 0.68 (0.03) |
| DNABERT 4-mer | 0.30 (0.00) | 0.45 (0.05) | 0.59 (0.09) | 0.74 (0.14) |
| DNABERT 5-mer | 0.58 (0.07) | 0.73 (0.15) | 0.87 (0.23) | 1.02 (0.30) |
| DNABERT 6-mer | 0.88 (0.12) | 1.18 (0.18) | 1.30 (0.23) | 1.34 (0.27) |
| DNABERT-2 BPE | 1.82 (0.84) | 1.83 (0.84) | 1.84 (0.85) | 1.85 (0.85) |

## Epoch-0 group offset subtracted above (excess that is present before any training)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer | -0.15 | -0.14 |
| DNABERT 4-mer | -0.01 | -0.01 |
| DNABERT 5-mer | -0.23 | -0.00 |
| DNABERT 6-mer | -0.36 | -0.06 |
| DNABERT-2 BPE | -0.01 | -0.07 |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer | 0 | 2.901 | 0.00 | 0.00 | 2.69 |
| DNABERT 3-mer | 1 | 1.996 | 0.15 | 0.16 | 2.10 |
| DNABERT 3-mer | 3 | 1.942 | 0.14 | 0.14 | 2.04 |
| DNABERT 3-mer | 8 | 1.928 | 0.12 | 0.14 | 2.04 |
| DNABERT 3-mer | 15 | 1.911 | 0.11 | 0.17 | 2.05 |
| DNABERT 3-mer | 30 | 1.899 | 0.16 | 0.27 | 2.07 |
| DNABERT 3-mer | 50 | 1.932 | 0.28 | 0.68 | 2.11 |
| DNABERT 4-mer | 0 | 2.713 | 0.00 | 0.00 | 2.70 |
| DNABERT 4-mer | 1 | 2.018 | -0.03 | 0.00 | 2.09 |
| DNABERT 4-mer | 3 | 1.940 | -0.02 | -0.00 | 2.05 |
| DNABERT 4-mer | 8 | 1.928 | -0.02 | 0.02 | 2.04 |
| DNABERT 4-mer | 15 | 1.922 | -0.02 | 0.06 | 2.05 |
| DNABERT 4-mer | 30 | 1.919 | 0.03 | 0.30 | 2.07 |
| DNABERT 4-mer | 50 | 1.946 | 0.20 | 1.20 | 2.13 |
| DNABERT 5-mer | 0 | 3.219 | 0.00 | 0.00 | 3.09 |
| DNABERT 5-mer | 1 | 2.118 | 0.21 | 0.08 | 2.27 |
| DNABERT 5-mer | 3 | 1.939 | 0.20 | 0.01 | 2.04 |
| DNABERT 5-mer | 8 | 1.929 | 0.20 | 0.04 | 2.05 |
| DNABERT 5-mer | 15 | 1.919 | 0.21 | 0.10 | 2.05 |
| DNABERT 5-mer | 30 | 1.915 | 0.26 | 0.44 | 2.09 |
| DNABERT 5-mer | 50 | 1.949 | 0.47 | 1.62 | 2.17 |
| DNABERT 6-mer | 0 | 4.620 | 0.00 | 0.00 | 4.67 |
| DNABERT 6-mer | 1 | 2.027 | 0.28 | 0.01 | 2.12 |
| DNABERT 6-mer | 3 | 1.931 | 0.35 | 0.12 | 2.06 |
| DNABERT 6-mer | 8 | 1.920 | 0.35 | 0.16 | 2.06 |
| DNABERT 6-mer | 15 | 1.910 | 0.37 | 0.28 | 2.07 |
| DNABERT 6-mer | 30 | 1.925 | 0.53 | 1.27 | 2.16 |
| DNABERT 6-mer | 50 | 2.005 | 0.88 | 2.03 | 2.28 |
| DNABERT-2 BPE | 0 | 2.618 | 0.00 | 0.00 | 2.61 |
| DNABERT-2 BPE | 1 | 1.920 | 0.01 | 0.08 | 2.04 |
| DNABERT-2 BPE | 3 | 1.893 | 0.01 | 0.17 | 2.02 |
| DNABERT-2 BPE | 8 | 1.891 | 0.06 | 0.99 | 2.04 |
| DNABERT-2 BPE | 15 | 1.916 | 0.18 | 1.82 | 2.07 |
| DNABERT-2 BPE | 30 | 2.114 | 0.93 | 2.23 | 2.28 |
| DNABERT-2 BPE | 50 | 2.486 | 2.14 | 2.72 | 2.69 |
