# Reconstruction audit — recon_r128

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.083 | 0.47 | 0% | 0.001 | 1.00 | 1.000 | **0%** | 34.1 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.321 | 0.31 | 0% | 0.011 | 1.00 | 0.968 | **10%** | 26.4 | 10% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.513 | 0.25 | 0% | 0.008 | 1.00 | 1.000 | **0%** | 32.1 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.429 | 0.07 | 0% | 3.968 | 0.10 | 0.000 | **0%** | 33.2 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=16 | 20 | 0.993 | 0.49 | 0% | 0.001 | 1.00 | 1.000 | **0%** | 34.1 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.406 | 0.29 | 0% | 0.006 | 1.00 | 1.000 | **0%** | 31.4 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.511 | 0.24 | 0% | 0.007 | 1.00 | 1.000 | **0%** | 34.4 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.302 | 0.07 | 0% | 4.031 | 0.08 | 0.000 | **0%** | 31.6 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=16 | 20 | 0.920 | 0.51 | 0% | 0.001 | 1.00 | 1.000 | **0%** | 32.5 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.315 | 0.29 | 0% | 0.004 | 1.00 | 1.000 | **0%** | 31.0 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.507 | 0.24 | 0% | 0.010 | 1.00 | 1.000 | **0%** | 30.8 | 0% |
| 3mer_mlm0.15_s2 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.303 | 0.04 | 0% | 3.627 | 0.09 | 0.000 | **0%** | 32.9 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.434 | 0.65 | 10% | 0.001 | 1.00 | 1.000 | **95%** | 0.2 | 95% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 20 | 0.633 | 0.50 | 0% | 0.001 | 1.00 | 1.000 | **80%** | 5.9 | 80% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 20 | 0.660 | 0.54 | 0% | 0.001 | 1.00 | 1.000 | **95%** | 1.6 | 95% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 20 | 3.290 | 0.03 | 0% | 3.365 | 0.02 | 0.000 | **0%** | 35.6 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.386 | 0.69 | 15% | 0.001 | 1.00 | 1.000 | **95%** | 1.8 | 95% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=4 | 20 | 0.558 | 0.57 | 0% | 0.001 | 1.00 | 1.000 | **80%** | 3.0 | 80% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=1 | 20 | 0.741 | 0.51 | 15% | 0.001 | 1.00 | 1.000 | **100%** | 0.0 | 100% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=0 | 20 | 3.205 | 0.03 | 0% | 3.222 | 0.02 | 0.000 | **0%** | 35.4 | 0% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=16 | 20 | 0.354 | 0.72 | 5% | 0.001 | 1.00 | 1.000 | **90%** | 2.8 | 90% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=4 | 20 | 0.487 | 0.61 | 0% | 0.001 | 1.00 | 1.000 | **85%** | 3.0 | 85% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=1 | 20 | 0.769 | 0.51 | 5% | 0.001 | 1.00 | 1.000 | **95%** | 0.3 | 95% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=0 | 20 | 3.295 | 0.01 | 0% | 3.275 | 0.01 | 0.000 | **0%** | 34.7 | 0% |

Members: target surprise 0.922 b/nt against 2.804 for the matched non-member control; ICM extraction at worst 100%.
