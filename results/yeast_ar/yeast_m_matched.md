# Matched-utility memorisation — yeast_m

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 2.047, highest 2.000), so no matched-utility comparison is possible; report the per-model trajectories instead.

- char (1 nt) [ar]: held-out loss 1.931 to 2.000
- 3-mer [ar]: held-out loss 1.921 to 3.991
- 4-mer [ar]: held-out loss 1.943 to 3.250
- 6-mer [ar]: held-out loss 1.951 to 2.531
- BPE-4096 [ar]: held-out loss 2.047 to 2.867
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
| char (1 nt) [ar] | 1 | 1.951 | 0.00 ±0.00 | 2.03 |
| char (1 nt) [ar] | 2 | 1.944 | 0.00 ±0.00 | 2.03 |
| char (1 nt) [ar] | 3 | 1.942 | 0.00 ±0.00 | 2.04 |
| char (1 nt) [ar] | 5 | 1.931 | 0.00 ±0.00 | 2.03 |
| char (1 nt) [ar] | 8 | 1.931 | 0.01 ±0.00 | 2.03 |
| char (1 nt) [ar] | 12 | 1.938 | 0.03 ±0.00 | 2.04 |
| char (1 nt) [ar] | 20 | 1.958 | 0.08 ±0.00 | 2.07 |
| char (1 nt) [ar] | 30 | 2.000 | 0.15 ±0.00 | 2.09 |
| 3-mer [ar] | 1 | 1.930 | -0.00 ±0.00 | 2.04 |
| 3-mer [ar] | 2 | 1.923 | 0.01 ±0.00 | 2.03 |
| 3-mer [ar] | 3 | 1.921 | 0.02 ±0.00 | 2.04 |
| 3-mer [ar] | 5 | 1.926 | 0.07 ±0.00 | 2.05 |
| 3-mer [ar] | 8 | 1.969 | 0.31 ±0.01 | 2.13 |
| 3-mer [ar] | 12 | 2.199 | 1.14 ±0.00 | 2.39 |
| 3-mer [ar] | 20 | 3.124 | 3.05 ±0.05 | 3.26 |
| 3-mer [ar] | 30 | 3.991 | 4.08 ±0.05 | 4.11 |
| 4-mer [ar] | 1 | 1.951 | 0.02 ±0.00 | 2.05 |
| 4-mer [ar] | 2 | 1.944 | 0.01 ±0.00 | 2.03 |
| 4-mer [ar] | 3 | 1.943 | 0.03 ±0.00 | 2.04 |
| 4-mer [ar] | 5 | 1.969 | 0.23 ±0.01 | 2.08 |
| 4-mer [ar] | 8 | 2.058 | 0.71 ±0.00 | 2.17 |
| 4-mer [ar] | 12 | 2.285 | 1.61 ±0.01 | 2.37 |
| 4-mer [ar] | 20 | 2.893 | 2.92 ±0.01 | 2.98 |
| 4-mer [ar] | 30 | 3.250 | 3.36 ±0.01 | 3.37 |
| 6-mer [ar] | 1 | 1.954 | 0.03 ±0.00 | 2.06 |
| 6-mer [ar] | 2 | 1.951 | 0.03 ±0.00 | 2.04 |
| 6-mer [ar] | 3 | 1.960 | 0.14 ±0.00 | 2.05 |
| 6-mer [ar] | 5 | 1.980 | 0.45 ±0.00 | 2.07 |
| 6-mer [ar] | 8 | 2.033 | 0.97 ±0.00 | 2.13 |
| 6-mer [ar] | 12 | 2.153 | 1.65 ±0.00 | 2.24 |
| 6-mer [ar] | 20 | 2.398 | 2.42 ±0.01 | 2.48 |
| 6-mer [ar] | 30 | 2.531 | 2.60 ±0.01 | 2.62 |
| BPE-4096 [ar] | 1 | 2.074 | 0.04 ±0.01 | 2.12 |
| BPE-4096 [ar] | 2 | 2.055 | 0.07 ±0.01 | 2.11 |
| BPE-4096 [ar] | 3 | 2.047 | 0.17 ±0.04 | 2.10 |
| BPE-4096 [ar] | 5 | 2.062 | 0.74 ±0.10 | 2.13 |
| BPE-4096 [ar] | 8 | 2.144 | 1.61 ±0.11 | 2.22 |
| BPE-4096 [ar] | 12 | 2.371 | 2.22 ±0.08 | 2.47 |
| BPE-4096 [ar] | 20 | 2.705 | 2.76 ±0.03 | 2.81 |
| BPE-4096 [ar] | 30 | 2.867 | 2.96 ±0.02 | 2.98 |
