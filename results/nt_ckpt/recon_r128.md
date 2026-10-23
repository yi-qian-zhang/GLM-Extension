# Reconstruction audit — recon_r128

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nt250m_mlm_ecoli_s0 | ecoli | 250m | mlm | r=16 | 20 | 0.297 | 0.78 | 35% | 0.021 | 0.98 | 0.869 | **70%** | 7.4 | 80% |
| nt250m_mlm_ecoli_s0 | ecoli | 250m | mlm | r=4 | 20 | 1.460 | 0.17 | 0% | 0.253 | 0.77 | 0.245 | **0%** | 35.0 | 0% |
| nt250m_mlm_ecoli_s0 | ecoli | 250m | mlm | r=1 | 20 | 1.982 | 0.03 | 0% | 0.959 | 0.43 | 0.010 | **0%** | 36.1 | 0% |
| nt250m_mlm_ecoli_s0 | ecoli | 250m | mlm | r=0 | 20 | 2.200 | 0.00 | 0% | 2.437 | 0.01 | 0.000 | **0%** | 36.2 | 0% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=16 | 20 | 0.428 | 0.66 | 25% | 0.031 | 0.98 | 0.902 | **65%** | 10.5 | 75% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=4 | 20 | 1.291 | 0.24 | 0% | 0.433 | 0.70 | 0.310 | **10%** | 29.9 | 15% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=1 | 20 | 1.486 | 0.17 | 5% | 0.529 | 0.62 | 0.137 | **10%** | 28.6 | 15% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=0 | 20 | 1.926 | 0.05 | 0% | 2.091 | 0.07 | 0.000 | **0%** | 35.6 | 0% |

Members: target surprise 1.157 b/nt against 2.063 for the matched non-member control; ICM extraction at worst 70%.
