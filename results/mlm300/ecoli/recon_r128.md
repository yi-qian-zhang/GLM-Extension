# Reconstruction audit — recon_r128

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=16 | 20 | 1.750 | 0.15 | 0% | 0.082 | 0.98 | 0.783 | **0%** | 34.7 | 0% |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=4 | 20 | 1.754 | 0.14 | 0% | 0.155 | 0.95 | 0.573 | **0%** | 34.3 | 0% |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=1 | 20 | 1.778 | 0.14 | 0% | 0.185 | 0.91 | 0.383 | **0%** | 34.0 | 0% |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=0 | 20 | 2.382 | 0.02 | 0% | 4.153 | 0.02 | 0.000 | **0%** | 36.6 | 0% |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=16 | 20 | 0.748 | 0.59 | 15% | 0.013 | 1.00 | 1.000 | **100%** | 0.0 | 100% |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=4 | 20 | 1.253 | 0.43 | 20% | 0.010 | 1.00 | 1.000 | **100%** | 0.0 | 100% |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=1 | 20 | 0.949 | 0.47 | 15% | 0.011 | 1.00 | 1.000 | **100%** | 0.0 | 100% |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=0 | 20 | 3.413 | 0.01 | 0% | 3.528 | 0.00 | 0.000 | **0%** | 36.1 | 0% |

Members: target surprise 1.372 b/nt against 2.897 for the matched non-member control; ICM extraction at worst 100%.
