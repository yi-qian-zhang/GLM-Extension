# Matched-utility memorisation — ft22

`excess` = non-member bits/nt − member bits/nt at the same checkpoint: the part of the canary score that is the planted record rather than biology the model legitimately learned. Higher = more memorised. Every model is interpolated onto the same held-out-loss values, on the overfitting branch. No epoch-0 subtraction: that offset does not propagate into the fine-tuned statistic (see the module docstring), so it is reported below as a diagnostic only.

**No common range.** The models' overfitting branches do not overlap (lowest common loss 1.681, highest 1.650), so no matched-utility comparison is possible; report the per-model trajectories instead.

- char (1 nt) [arft]: held-out loss 1.607 to 7.848
- char (1 nt) [arlora8]: held-out loss 1.601 to 1.650
- 6-mer [arft]: held-out loss 1.681 to 2.464
- 6-mer [arlora8]: held-out loss 1.681 to 1.693
## Epoch-0 excess — the pretrained model's prior over the two canary groups (diagnostic only, not subtracted)

| model | r=1 | r=16 |
|---|---|---|
| char (1 nt) [arft] | +0.00 | +0.00 |
| char (1 nt) [arlora8] | +0.00 | +0.00 |
| 6-mer [arft] | +0.00 | +0.00 |
| 6-mer [arlora8] | +0.00 | +0.00 |

## Per-model trajectory (means over runs, epoch > 0; ± is the spread over runs)

| model | epoch | held-out loss | r=1 excess | r=16 excess | control bits |
|---|---|---|---|---|---|
| char (1 nt) [arft] | 1 | 1.607 | 0.08 ±0.01 | 0.44 ±0.02 | 1.74 |
| char (1 nt) [arft] | 2 | 1.614 | 0.17 ±0.00 | 1.07 ±0.00 | 1.76 |
| char (1 nt) [arft] | 3 | 1.625 | 0.28 ±0.01 | 1.37 ±0.00 | 1.78 |
| char (1 nt) [arft] | 5 | 1.694 | 0.61 ±0.01 | 1.64 ±0.01 | 1.90 |
| char (1 nt) [arft] | 8 | 2.009 | 1.48 ±0.01 | 2.19 ±0.00 | 2.35 |
| char (1 nt) [arft] | 12 | 3.113 | 3.28 ±0.05 | 3.59 ±0.06 | 3.67 |
| char (1 nt) [arft] | 20 | 6.061 | 6.80 ±0.04 | 6.86 ±0.04 | 6.87 |
| char (1 nt) [arft] | 30 | 7.848 | 8.79 ±0.03 | 8.80 ±0.03 | 8.80 |
| char (1 nt) [arlora8] | 1 | 1.605 | 0.01 ±0.01 | 0.10 ±0.00 | 1.78 |
| char (1 nt) [arlora8] | 2 | 1.602 | 0.03 ±0.00 | 0.17 ±0.00 | 1.75 |
| char (1 nt) [arlora8] | 3 | 1.601 | 0.04 ±0.00 | 0.24 ±0.00 | 1.75 |
| char (1 nt) [arlora8] | 5 | 1.603 | 0.07 ±0.00 | 0.35 ±0.00 | 1.75 |
| char (1 nt) [arlora8] | 8 | 1.608 | 0.12 ±0.00 | 0.56 ±0.00 | 1.77 |
| char (1 nt) [arlora8] | 12 | 1.619 | 0.17 ±0.00 | 0.82 ±0.00 | 1.79 |
| char (1 nt) [arlora8] | 20 | 1.636 | 0.25 ±0.02 | 1.10 ±0.03 | 1.83 |
| char (1 nt) [arlora8] | 30 | 1.650 | 0.29 ±0.02 | 1.20 ±0.02 | 1.86 |
| 6-mer [arft] | 1 | 1.681 | 0.10 ±0.01 | 0.16 ±0.02 | 1.82 |
| 6-mer [arft] | 2 | 1.690 | 0.30 ±0.01 | 0.49 ±0.00 | 1.83 |
| 6-mer [arft] | 3 | 1.735 | 0.62 ±0.01 | 0.96 ±0.01 | 1.89 |
| 6-mer [arft] | 5 | 1.874 | 1.30 ±0.01 | 1.61 ±0.01 | 2.02 |
| 6-mer [arft] | 8 | 2.051 | 1.97 ±0.01 | 2.08 ±0.00 | 2.21 |
| 6-mer [arft] | 12 | 2.239 | 2.38 ±0.01 | 2.38 ±0.01 | 2.41 |
| 6-mer [arft] | 20 | 2.409 | 2.61 ±0.02 | 2.61 ±0.02 | 2.61 |
| 6-mer [arft] | 30 | 2.464 | 2.66 ±0.02 | 2.66 ±0.02 | 2.67 |
| 6-mer [arlora8] | 1 | 1.699 | 0.01 ±0.00 | 0.03 ±0.00 | 1.88 |
| 6-mer [arlora8] | 2 | 1.686 | 0.01 ±0.00 | 0.04 ±0.00 | 1.85 |
| 6-mer [arlora8] | 3 | 1.683 | 0.02 ±0.00 | 0.06 ±0.00 | 1.84 |
| 6-mer [arlora8] | 5 | 1.681 | 0.04 ±0.00 | 0.08 ±0.00 | 1.83 |
| 6-mer [arlora8] | 8 | 1.681 | 0.06 ±0.00 | 0.12 ±0.01 | 1.83 |
| 6-mer [arlora8] | 12 | 1.684 | 0.09 ±0.00 | 0.17 ±0.00 | 1.84 |
| 6-mer [arlora8] | 20 | 1.690 | 0.13 ±0.00 | 0.24 ±0.00 | 1.85 |
| 6-mer [arlora8] | 30 | 1.693 | 0.15 ±0.00 | 0.26 ±0.00 | 1.85 |
