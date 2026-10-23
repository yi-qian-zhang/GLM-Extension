# Matched-utility memorisation — syn_m

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 2.047, highest 2.040), so no matched-utility comparison is possible; report the per-model trajectories instead.

- char (1 nt) [ar]: held-out loss 2.001 to 2.040
- 3-mer [ar]: held-out loss 2.003 to 4.150
- 4-mer [ar]: held-out loss 2.003 to 3.294
- 6-mer [ar]: held-out loss 2.007 to 2.632
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
| char (1 nt) [ar] | 1 | 2.003 | -0.00 ±0.00 | 2.00 |
| char (1 nt) [ar] | 2 | 2.001 | -0.00 ±0.00 | 2.00 |
| char (1 nt) [ar] | 3 | 2.001 | 0.00 ±0.00 | 2.00 |
| char (1 nt) [ar] | 5 | 2.001 | 0.00 ±0.00 | 2.00 |
| char (1 nt) [ar] | 8 | 2.002 | 0.00 ±0.00 | 2.00 |
| char (1 nt) [ar] | 12 | 2.006 | 0.02 ±0.00 | 2.01 |
| char (1 nt) [ar] | 20 | 2.021 | 0.05 ±0.01 | 2.02 |
| char (1 nt) [ar] | 30 | 2.040 | 0.09 ±0.01 | 2.04 |
| 3-mer [ar] | 1 | 2.003 | 0.00 ±0.00 | 2.00 |
| 3-mer [ar] | 2 | 2.003 | 0.00 ±0.00 | 2.00 |
| 3-mer [ar] | 3 | 2.004 | 0.02 ±0.00 | 2.00 |
| 3-mer [ar] | 5 | 2.015 | 0.07 ±0.00 | 2.02 |
| 3-mer [ar] | 8 | 2.074 | 0.27 ±0.02 | 2.08 |
| 3-mer [ar] | 12 | 2.324 | 1.00 ±0.05 | 2.33 |
| 3-mer [ar] | 20 | 3.210 | 3.00 ±0.06 | 3.25 |
| 3-mer [ar] | 30 | 4.150 | 4.20 ±0.04 | 4.22 |
| 4-mer [ar] | 1 | 2.004 | 0.00 ±0.00 | 2.00 |
| 4-mer [ar] | 2 | 2.003 | 0.01 ±0.00 | 2.00 |
| 4-mer [ar] | 3 | 2.006 | 0.03 ±0.00 | 2.01 |
| 4-mer [ar] | 5 | 2.046 | 0.24 ±0.01 | 2.04 |
| 4-mer [ar] | 8 | 2.138 | 0.75 ±0.00 | 2.14 |
| 4-mer [ar] | 12 | 2.359 | 1.74 ±0.01 | 2.38 |
| 4-mer [ar] | 20 | 2.972 | 2.99 ±0.02 | 3.02 |
| 4-mer [ar] | 30 | 3.294 | 3.34 ±0.01 | 3.35 |
| 6-mer [ar] | 1 | 2.008 | 0.01 ±0.00 | 2.01 |
| 6-mer [ar] | 2 | 2.007 | 0.03 ±0.00 | 2.01 |
| 6-mer [ar] | 3 | 2.024 | 0.15 ±0.01 | 2.02 |
| 6-mer [ar] | 5 | 2.047 | 0.43 ±0.00 | 2.04 |
| 6-mer [ar] | 8 | 2.095 | 0.94 ±0.01 | 2.09 |
| 6-mer [ar] | 12 | 2.205 | 1.69 ±0.01 | 2.20 |
| 6-mer [ar] | 20 | 2.483 | 2.45 ±0.01 | 2.49 |
| 6-mer [ar] | 30 | 2.632 | 2.63 ±0.01 | 2.64 |
| BPE-4096 [ar] | 1 | 2.074 | 0.04 ±0.01 | 2.12 |
| BPE-4096 [ar] | 2 | 2.055 | 0.07 ±0.01 | 2.11 |
| BPE-4096 [ar] | 3 | 2.047 | 0.17 ±0.04 | 2.10 |
| BPE-4096 [ar] | 5 | 2.062 | 0.74 ±0.10 | 2.13 |
| BPE-4096 [ar] | 8 | 2.144 | 1.61 ±0.11 | 2.22 |
| BPE-4096 [ar] | 12 | 2.371 | 2.22 ±0.08 | 2.47 |
| BPE-4096 [ar] | 20 | 2.705 | 2.76 ±0.03 | 2.81 |
| BPE-4096 [ar] | 30 | 2.867 | 2.96 ±0.02 | 2.98 |
