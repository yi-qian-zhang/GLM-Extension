# Reconstruction audit — recon_r8

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | human | 3mer | ar | r=16 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=4 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=1 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=0 | 25 | 5.591 | 0.07 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 25 | 1.044 | 0.44 | 0% | 0.042 | 0.99 | 0.862 | **0%** | 32.8 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 25 | 1.477 | 0.25 | 0% | 0.265 | 0.87 | 0.429 | **0%** | 30.1 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 25 | 1.674 | 0.18 | 0% | 0.512 | 0.73 | 0.299 | **0%** | 31.8 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 25 | 2.263 | 0.08 | 0% | 2.480 | 0.11 | 0.000 | **0%** | 33.6 | 0% |
| 6mer_ar_s0 | human | 6mer | ar | r=16 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=4 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=1 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=0 | 25 | 3.248 | 0.01 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 25 | 1.237 | 0.19 | 0% | 0.692 | 0.55 | 0.140 | **0%** | 33.1 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.586 | 0.09 | 0% | 0.977 | 0.38 | 0.006 | **0%** | 30.6 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.627 | 0.09 | 0% | 1.061 | 0.36 | 0.003 | **0%** | 34.9 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.188 | 0.01 | 0% | 2.187 | 0.01 | 0.000 | **0%** | 36.4 | 0% |

Members: target surprise 0.720 b/nt against 3.322 for the matched non-member control; ICM extraction at worst nan%.
