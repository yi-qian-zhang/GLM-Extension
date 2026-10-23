# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | human | 3mer | ar | r=16 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=4 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=1 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=0 | 20 | 6.139 | 0.07 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.324 | 0.33 | 0% | 0.489 | 0.78 | 0.434 | **0%** | 35.6 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.575 | 0.17 | 0% | 1.018 | 0.49 | 0.080 | **0%** | 32.8 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.789 | 0.15 | 0% | 1.268 | 0.37 | 0.042 | **0%** | 32.8 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 20 | 1.994 | 0.09 | 0% | 2.007 | 0.11 | 0.000 | **0%** | 35.1 | 0% |
| 6mer_ar_s0 | human | 6mer | ar | r=16 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=4 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=1 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=0 | 20 | 3.122 | 0.01 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 20 | 1.856 | 0.04 | 0% | 1.743 | 0.05 | 0.000 | **0%** | 33.5 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 20 | 1.918 | 0.02 | 0% | 1.788 | 0.03 | 0.000 | **0%** | 32.7 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 20 | 1.933 | 0.03 | 0% | 1.842 | 0.03 | 0.000 | **0%** | 33.7 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 20 | 2.162 | 0.02 | 0% | 2.174 | 0.01 | 0.000 | **0%** | 35.1 | 0% |

Members: target surprise 0.866 b/nt against 3.354 for the matched non-member control; ICM extraction at worst nan%.
