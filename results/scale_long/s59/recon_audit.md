# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | human | 3mer | ar | r=16 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=4 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=1 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_ar_s0 | human | 3mer | ar | r=0 | 20 | 5.578 | 0.07 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 20 | 0.996 | 0.46 | 0% | 0.027 | 0.99 | 0.936 | **0%** | 32.4 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.437 | 0.26 | 0% | 0.258 | 0.87 | 0.418 | **0%** | 31.4 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.626 | 0.20 | 0% | 0.522 | 0.73 | 0.268 | **0%** | 32.9 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.204 | 0.09 | 0% | 2.481 | 0.10 | 0.000 | **0%** | 35.5 | 0% |
| 6mer_ar_s0 | human | 6mer | ar | r=16 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=4 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=1 | 20 | 0.000 | 1.00 | 100% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_ar_s0 | human | 6mer | ar | r=0 | 20 | 3.261 | 0.01 | 0% | nan | nan | nan | **nan%** | nan | nan% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 20 | 1.197 | 0.20 | 0% | 0.670 | 0.57 | 0.169 | **0%** | 32.7 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 20 | 1.521 | 0.09 | 0% | 0.942 | 0.40 | 0.007 | **0%** | 30.9 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 20 | 1.588 | 0.09 | 0% | 1.051 | 0.36 | 0.003 | **0%** | 33.1 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 20 | 2.207 | 0.01 | 0% | 2.205 | 0.02 | 0.000 | **0%** | 34.7 | 0% |

Members: target surprise 0.697 b/nt against 3.312 for the matched non-member control; ICM extraction at worst nan%.
