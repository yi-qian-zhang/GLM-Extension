# Training trajectory — outputs/human_mlm_300

floor = held-out bits/nt (2.000 = generalizes as well as possible on random data; higher = overfit). b/r/x = probe bits/nt / rank-1 / exact-extraction at tier r (training host). fp = non-member rank-1 (false positives).

| tok | obj | seed | epoch | floor | b1 | b4 | b16 | r1 | r4 | r16 | x1 | x4 | x16 | fp |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer | mlm0.15 | 0 | 150 | 2.353 | 0.342 | 0.233 | 0.065 | 0.88 | 0.98 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3mer | mlm0.15 | 0 | 200 | 2.873 | 0.101 | 0.066 | 0.012 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3mer | mlm0.15 | 0 | 250 | 3.210 | 0.024 | 0.018 | 0.004 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 3mer | mlm0.15 | 0 | 300 | 3.400 | 0.010 | 0.007 | 0.001 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 6mer | mlm0.15 | 0 | 150 | 2.590 | 0.051 | 0.049 | 0.031 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.00 | 0.02 |
| 6mer | mlm0.15 | 0 | 200 | 2.776 | 0.007 | 0.007 | 0.005 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 0.02 | 0.02 |
| 6mer | mlm0.15 | 0 | 250 | 2.839 | 0.001 | 0.002 | 0.001 | 1.00 | 1.00 | 1.00 | 0.02 | 0.02 | 0.02 | 0.02 |
| 6mer | mlm0.15 | 0 | 300 | 2.866 | 0.001 | 0.001 | 0.001 | 1.00 | 1.00 | 1.00 | 0.02 | 0.00 | 0.04 | 0.02 |

## Memorization at matched overfitting

probe bits/nt interpolated at each held-out floor (mean over seeds; — = curve never reaches that floor). Lower = more memorized; 2.000 = nothing memorized.

| tok | obj | tier | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | @3.00 |
|---|---|---|---|---|---|---|---|---|
| 3mer | mlm0.15 | r=1 | — | — | — | — | 0.320 | 0.072 |
| 3mer | mlm0.15 | r=4 | — | — | — | — | 0.218 | 0.048 |
| 3mer | mlm0.15 | r=16 | — | — | — | — | 0.060 | 0.009 |