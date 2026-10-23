# Matched-utility memorisation — chk_yeast

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned, minus its own value at epoch 0, where nothing is memorised and the reading is the fixed offset between the two canary groups. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.929 to 1.935 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.929 | @1.931 | @1.933 | @1.935 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.23 (0.00) | 0.24 (0.00) | 0.25 (0.00) | 0.26 (0.00) |
| DNABERT 4-mer | 0.06 (0.00) | 0.07 (0.00) | 0.09 (0.00) | 0.11 (0.00) |
| DNABERT 5-mer | 0.07 (0.00) | 0.09 (0.00) | 0.10 (0.00) | 0.12 (0.00) |
| DNABERT 6-mer | 0.18 (0.00) | 0.22 (0.00) | 0.25 (0.00) | 0.28 (0.00) |
| DNABERT-2 BPE | 0.26 (0.00) | 0.27 (0.00) | 0.28 (0.00) | 0.29 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.929 | @1.931 | @1.933 | @1.935 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.93 (0.28) | 0.98 (0.30) | 1.02 (0.32) | 1.06 (0.34) |
| DNABERT 4-mer | 0.78 (0.21) | 0.86 (0.26) | 0.95 (0.30) | 1.03 (0.35) |
| DNABERT 5-mer | 0.95 (0.20) | 1.00 (0.24) | 1.06 (0.28) | 1.11 (0.31) |
| DNABERT 6-mer | 0.20 (0.00) | 0.42 (0.11) | 0.65 (0.21) | 0.87 (0.32) |
| DNABERT-2 BPE | 1.77 (0.84) | 1.78 (0.85) | 1.78 (0.85) | 1.79 (0.85) |

## Epoch-0 group offset subtracted above (excess that is present before any training)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer | -0.07 | -0.10 |
| DNABERT 4-mer | +0.03 | +0.04 |
| DNABERT 5-mer | +0.03 | -0.06 |
| DNABERT 6-mer | -0.16 | +0.11 |
| DNABERT-2 BPE | +0.01 | +0.01 |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer | 0 | 2.820 | 0.00 | 0.00 | 2.70 |
| DNABERT 3-mer | 1 | 1.996 | 0.04 | 0.09 | 2.10 |
| DNABERT 3-mer | 3 | 1.950 | 0.05 | 0.10 | 2.04 |
| DNABERT 3-mer | 8 | 1.936 | 0.04 | 0.10 | 2.05 |
| DNABERT 3-mer | 15 | 1.916 | 0.03 | 0.16 | 2.06 |
| DNABERT 3-mer | 30 | 1.905 | 0.09 | 0.42 | 2.08 |
| DNABERT 3-mer | 50 | 1.935 | 0.26 | 1.06 | 2.14 |
| DNABERT 4-mer | 0 | 2.691 | 0.00 | 0.00 | 2.70 |
| DNABERT 4-mer | 1 | 2.010 | -0.05 | -0.03 | 2.09 |
| DNABERT 4-mer | 3 | 1.943 | -0.07 | -0.04 | 2.05 |
| DNABERT 4-mer | 8 | 1.934 | -0.07 | -0.03 | 2.04 |
| DNABERT 4-mer | 15 | 1.926 | -0.06 | 0.04 | 2.07 |
| DNABERT 4-mer | 30 | 1.921 | -0.02 | 0.43 | 2.08 |
| DNABERT 4-mer | 50 | 1.943 | 0.20 | 1.41 | 2.16 |
| DNABERT 5-mer | 0 | 3.014 | 0.00 | 0.00 | 3.05 |
| DNABERT 5-mer | 1 | 2.117 | -0.09 | 0.09 | 2.24 |
| DNABERT 5-mer | 3 | 1.946 | -0.07 | 0.06 | 2.05 |
| DNABERT 5-mer | 8 | 1.935 | -0.07 | 0.09 | 2.05 |
| DNABERT 5-mer | 15 | 1.924 | -0.05 | 0.19 | 2.07 |
| DNABERT 5-mer | 30 | 1.923 | 0.03 | 0.79 | 2.12 |
| DNABERT 5-mer | 50 | 1.960 | 0.30 | 1.81 | 2.23 |
| DNABERT 6-mer | 0 | 4.748 | 0.00 | 0.00 | 4.81 |
| DNABERT 6-mer | 1 | 2.036 | 0.11 | -0.07 | 2.17 |
| DNABERT 6-mer | 3 | 1.939 | 0.13 | -0.04 | 2.07 |
| DNABERT 6-mer | 8 | 1.932 | 0.14 | 0.00 | 2.07 |
| DNABERT 6-mer | 15 | 1.929 | 0.18 | 0.20 | 2.09 |
| DNABERT 6-mer | 30 | 1.938 | 0.35 | 1.29 | 2.17 |
| DNABERT 6-mer | 50 | 2.010 | 0.78 | 1.95 | 2.31 |
| DNABERT-2 BPE | 0 | 2.571 | 0.00 | 0.00 | 2.64 |
| DNABERT-2 BPE | 1 | 1.927 | -0.02 | -0.00 | 2.04 |
| DNABERT-2 BPE | 3 | 1.901 | -0.01 | 0.09 | 2.03 |
| DNABERT-2 BPE | 8 | 1.900 | 0.05 | 0.94 | 2.05 |
| DNABERT-2 BPE | 15 | 1.924 | 0.23 | 1.76 | 2.09 |
| DNABERT-2 BPE | 30 | 2.100 | 1.17 | 2.19 | 2.32 |
| DNABERT-2 BPE | 50 | 2.459 | 2.31 | 2.73 | 2.79 |
