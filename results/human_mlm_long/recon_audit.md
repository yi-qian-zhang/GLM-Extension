# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.239 | 0.33 | 0% | 0.065 | 0.99 | 0.839 | **0%** | 35.3 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.522 | 0.23 | 0% | 0.456 | 0.76 | 0.144 | **0%** | 36.5 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.723 | 0.19 | 0% | 0.579 | 0.70 | 0.181 | **0%** | 35.0 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.152 | 0.09 | 0% | 2.358 | 0.10 | 0.000 | **0%** | 35.0 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.135 | 0.40 | 0% | 0.066 | 0.98 | 0.839 | **0%** | 33.7 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.501 | 0.25 | 0% | 0.429 | 0.77 | 0.294 | **0%** | 34.7 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.691 | 0.19 | 0% | 0.572 | 0.73 | 0.209 | **0%** | 35.3 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.129 | 0.07 | 0% | 2.423 | 0.09 | 0.000 | **0%** | 35.4 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.141 | 0.43 | 0% | 0.088 | 0.97 | 0.842 | **0%** | 34.3 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.488 | 0.23 | 0% | 0.439 | 0.79 | 0.340 | **0%** | 34.9 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.707 | 0.17 | 0% | 0.606 | 0.71 | 0.169 | **0%** | 33.8 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.117 | 0.07 | 0% | 2.321 | 0.12 | 0.000 | **0%** | 35.4 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.824 | 0.44 | 0% | 0.129 | 0.98 | 0.869 | **15%** | 25.4 | 15% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 20 | 1.130 | 0.25 | 0% | 0.308 | 0.85 | 0.350 | **0%** | 33.5 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 20 | 1.203 | 0.24 | 0% | 0.286 | 0.88 | 0.444 | **0%** | 31.1 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 20 | 2.504 | 0.02 | 0% | 2.529 | 0.02 | 0.000 | **0%** | 33.1 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.741 | 0.47 | 0% | 0.105 | 0.98 | 0.869 | **15%** | 26.2 | 15% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=4 | 20 | 1.063 | 0.31 | 0% | 0.272 | 0.85 | 0.343 | **0%** | 29.6 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=1 | 20 | 1.179 | 0.25 | 0% | 0.234 | 0.92 | 0.640 | **0%** | 32.9 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=0 | 20 | 2.451 | 0.02 | 0% | 2.470 | 0.04 | 0.000 | **0%** | 34.9 | 0% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.765 | 0.50 | 0% | 0.119 | 0.97 | 0.804 | **5%** | 23.9 | 5% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=4 | 20 | 1.118 | 0.29 | 0% | 0.269 | 0.87 | 0.449 | **5%** | 31.9 | 5% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=1 | 20 | 1.309 | 0.22 | 0% | 0.310 | 0.87 | 0.498 | **0%** | 33.5 | 0% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=0 | 20 | 2.465 | 0.02 | 0% | 2.497 | 0.01 | 0.000 | **0%** | 33.0 | 0% |

Members: target surprise 1.249 b/nt against 2.303 for the matched non-member control; ICM extraction at worst 15%.
