# Matched-utility memorisation — gue_ar_matched

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 2.047, highest 2.001), so no matched-utility comparison is possible; report the per-model trajectories instead.

- char (1 nt) [ar]: held-out loss 1.932 to 2.001
- 3-mer [ar]: held-out loss 1.927 to 3.942
- 4-mer [ar]: held-out loss 1.931 to 3.216
- 6-mer [ar]: held-out loss 1.949 to 2.497
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
| char (1 nt) [ar] | 1 | 1.949 | -0.01 ±0.01 | 2.03 |
| char (1 nt) [ar] | 2 | 1.938 | -0.02 ±0.00 | 2.02 |
| char (1 nt) [ar] | 3 | 1.936 | -0.00 ±0.00 | 2.02 |
| char (1 nt) [ar] | 5 | 1.932 | -0.00 ±0.00 | 2.03 |
| char (1 nt) [ar] | 8 | 1.934 | 0.00 ±0.00 | 2.02 |
| char (1 nt) [ar] | 12 | 1.939 | 0.02 ±0.00 | 2.03 |
| char (1 nt) [ar] | 20 | 1.963 | 0.07 ±0.01 | 2.05 |
| char (1 nt) [ar] | 30 | 2.001 | 0.13 ±0.02 | 2.07 |
| 3-mer [ar] | 1 | 1.941 | -0.01 ±0.00 | 2.02 |
| 3-mer [ar] | 2 | 1.929 | -0.00 ±0.00 | 2.02 |
| 3-mer [ar] | 3 | 1.927 | 0.01 ±0.00 | 2.02 |
| 3-mer [ar] | 5 | 1.933 | 0.04 ±0.00 | 2.03 |
| 3-mer [ar] | 8 | 1.968 | 0.19 ±0.00 | 2.06 |
| 3-mer [ar] | 12 | 2.184 | 0.96 ±0.01 | 2.30 |
| 3-mer [ar] | 20 | 3.067 | 2.98 ±0.06 | 3.22 |
| 3-mer [ar] | 30 | 3.942 | 4.05 ±0.07 | 4.07 |
| 4-mer [ar] | 1 | 1.948 | -0.01 ±0.00 | 2.03 |
| 4-mer [ar] | 2 | 1.935 | -0.00 ±0.00 | 2.02 |
| 4-mer [ar] | 3 | 1.931 | 0.03 ±0.00 | 2.02 |
| 4-mer [ar] | 5 | 1.951 | 0.16 ±0.00 | 2.05 |
| 4-mer [ar] | 8 | 2.030 | 0.62 ±0.01 | 2.13 |
| 4-mer [ar] | 12 | 2.247 | 1.51 ±0.01 | 2.33 |
| 4-mer [ar] | 20 | 2.844 | 2.82 ±0.01 | 2.89 |
| 4-mer [ar] | 30 | 3.216 | 3.25 ±0.02 | 3.26 |
| 6-mer [ar] | 1 | 1.970 | 0.02 ±0.00 | 2.04 |
| 6-mer [ar] | 2 | 1.949 | 0.02 ±0.00 | 2.02 |
| 6-mer [ar] | 3 | 1.954 | 0.12 ±0.00 | 2.04 |
| 6-mer [ar] | 5 | 1.973 | 0.44 ±0.01 | 2.06 |
| 6-mer [ar] | 8 | 2.033 | 0.95 ±0.01 | 2.11 |
| 6-mer [ar] | 12 | 2.144 | 1.62 ±0.00 | 2.21 |
| 6-mer [ar] | 20 | 2.366 | 2.35 ±0.00 | 2.42 |
| 6-mer [ar] | 30 | 2.497 | 2.53 ±0.00 | 2.55 |
| BPE-4096 [ar] | 1 | 2.074 | 0.04 ±0.01 | 2.12 |
| BPE-4096 [ar] | 2 | 2.055 | 0.07 ±0.01 | 2.11 |
| BPE-4096 [ar] | 3 | 2.047 | 0.17 ±0.04 | 2.10 |
| BPE-4096 [ar] | 5 | 2.062 | 0.74 ±0.10 | 2.13 |
| BPE-4096 [ar] | 8 | 2.144 | 1.61 ±0.11 | 2.22 |
| BPE-4096 [ar] | 12 | 2.371 | 2.22 ±0.08 | 2.47 |
| BPE-4096 [ar] | 20 | 2.705 | 2.76 ±0.03 | 2.81 |
| BPE-4096 [ar] | 30 | 2.867 | 2.96 ±0.02 | 2.98 |
