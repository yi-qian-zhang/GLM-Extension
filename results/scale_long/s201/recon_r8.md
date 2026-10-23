# Reconstruction audit — recon_r8

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | human | 3mer | ar | r=16 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=4 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=1 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=0 | 25 | 6.020 | 0.07 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 25 | 1.365 | 0.32 | 0% | 0.610 | 0.72 | 0.387 | **0%** | 33.8 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 25 | 1.604 | 0.18 | 0% | 1.011 | 0.51 | 0.073 | **0%** | 32.4 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 25 | 1.815 | 0.14 | 0% | 1.246 | 0.38 | 0.036 | **0%** | 34.3 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 25 | 2.007 | 0.08 | 0% | 2.021 | 0.12 | 0.000 | **0%** | 34.8 | 0% |
| 6mer_ar_s0 | human | 6mer | ar | r=16 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=4 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=1 | 25 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=0 | 25 | 3.069 | 0.01 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 25 | 1.862 | 0.03 | 0% | 1.762 | 0.05 | 0.000 | **0%** | 34.1 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.903 | 0.02 | 0% | 1.782 | 0.04 | 0.000 | **0%** | 34.0 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.942 | 0.03 | 0% | 1.847 | 0.02 | 0.000 | **0%** | 34.0 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.131 | 0.02 | 0% | 2.148 | 0.01 | 0.000 | **0%** | 35.3 | 0% |

Members: target surprise 0.874 b/nt against 3.307 for the matched non-member control; ICM extraction at worst nan%.
