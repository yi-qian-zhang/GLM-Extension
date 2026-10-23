# Matched-utility memorisation — human_dnabert_mlm

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned, minus its own value at epoch 0, where nothing is memorised and the reading is the fixed offset between the two canary groups. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch.

Common range of held-out loss: 1.390 to 1.430 bits/nt.

## Canary planted 1x — excess bits/nt (verbatim extraction in brackets)

| model | @1.390 | @1.403 | @1.416 | @1.430 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.05 (0.00) | 0.06 (0.00) | 0.07 (0.00) | 0.08 (0.00) |
| DNABERT 4-mer | -0.02 (0.00) | 0.01 (0.00) | 0.09 (0.00) | 0.44 (0.00) |
| DNABERT 5-mer | -0.06 (0.00) | -0.07 (0.00) | -0.01 (0.00) | 0.51 (0.00) |
| DNABERT 6-mer | 0.00 (0.00) | 0.04 (0.00) | -0.05 (0.00) | -0.05 (0.00) |

## Canary planted 16x — excess bits/nt (verbatim extraction in brackets)

| model | @1.390 | @1.403 | @1.416 | @1.430 |
|---|---|---|---|---|
| DNABERT 3-mer | 0.71 (0.00) | 0.72 (0.00) | 0.69 (0.00) | 0.66 (0.00) |
| DNABERT 4-mer | 0.03 (0.00) | 0.21 (0.00) | 0.62 (0.00) | 0.95 (0.00) |
| DNABERT 5-mer | 0.01 (0.00) | 0.12 (0.00) | 0.44 (0.00) | 0.87 (0.00) |
| DNABERT 6-mer | 0.10 (0.00) | 0.34 (0.00) | 0.27 (0.00) | 0.36 (0.03) |

## Epoch-0 group offset subtracted above (excess that is present before any training)

| model | r=1 | r=16 |
|---|---|---|
| DNABERT 3-mer | -0.31 | +0.45 |
| DNABERT 4-mer | -0.37 | +0.32 |
| DNABERT 5-mer | -0.33 | +0.41 |
| DNABERT 6-mer | -0.36 | +0.34 |

## Per-model trajectory (seed means, epoch > 0)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| DNABERT 3-mer | 0 | 1.349 | 0.00 | 0.00 | 1.53 |
| DNABERT 3-mer | 1 | 1.352 | -0.02 | 0.02 | 1.51 |
| DNABERT 3-mer | 3 | 1.369 | -0.05 | 0.10 | 1.53 |
| DNABERT 3-mer | 8 | 1.371 | -0.05 | 0.23 | 1.47 |
| DNABERT 3-mer | 15 | 1.381 | -0.05 | 0.43 | 1.46 |
| DNABERT 3-mer | 30 | 1.391 | 0.06 | 0.74 | 1.51 |
| DNABERT 3-mer | 50 | 1.933 | 0.30 | -0.44 | 1.94 |
| DNABERT 4-mer | 0 | 1.387 | 0.00 | 0.00 | 1.45 |
| DNABERT 4-mer | 1 | 1.390 | -0.02 | 0.03 | 1.44 |
| DNABERT 4-mer | 3 | 1.392 | -0.01 | 0.05 | 1.42 |
| DNABERT 4-mer | 8 | 1.408 | 0.01 | 0.28 | 1.46 |
| DNABERT 4-mer | 15 | 1.410 | 0.04 | 0.42 | 1.48 |
| DNABERT 4-mer | 30 | 1.415 | 0.05 | 0.58 | 1.47 |
| DNABERT 4-mer | 50 | 1.433 | 0.54 | 1.05 | 1.56 |
| DNABERT 5-mer | 0 | 1.385 | 0.00 | 0.00 | 1.55 |
| DNABERT 5-mer | 1 | 1.379 | 0.02 | 0.04 | 1.55 |
| DNABERT 5-mer | 3 | 1.400 | -0.13 | -0.02 | 1.43 |
| DNABERT 5-mer | 8 | 1.404 | -0.05 | 0.17 | 1.48 |
| DNABERT 5-mer | 15 | 1.405 | -0.00 | 0.34 | 1.53 |
| DNABERT 5-mer | 30 | 1.427 | -0.02 | 0.53 | 1.52 |
| DNABERT 5-mer | 50 | 1.430 | 0.51 | 0.87 | 1.61 |
| DNABERT 6-mer | 0 | 1.379 | 0.00 | 0.00 | 1.48 |
| DNABERT 6-mer | 1 | 1.376 | -0.01 | -0.01 | 1.44 |
| DNABERT 6-mer | 3 | 1.394 | 0.01 | 0.12 | 1.48 |
| DNABERT 6-mer | 8 | 1.417 | -0.07 | 0.24 | 1.44 |
| DNABERT 6-mer | 15 | 1.409 | 0.06 | 0.47 | 1.50 |
| DNABERT 6-mer | 30 | 1.458 | -0.00 | 0.63 | 1.51 |
| DNABERT 6-mer | 50 | 1.460 | 0.59 | 0.91 | 1.65 |
