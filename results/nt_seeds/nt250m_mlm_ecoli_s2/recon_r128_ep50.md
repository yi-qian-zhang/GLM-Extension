# Reconstruction audit — recon_r128_ep50

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nt250m_mlm_ecoli_s2 | ecoli | 250m | mlm | r=16 | 20 | 0.282 | 0.79 | 35% | 0.014 | 0.99 | 0.967 | **70%** | 8.6 | 85% |
| nt250m_mlm_ecoli_s2 | ecoli | 250m | mlm | r=4 | 20 | 1.453 | 0.16 | 0% | 0.352 | 0.72 | 0.243 | **0%** | 34.9 | 0% |
| nt250m_mlm_ecoli_s2 | ecoli | 250m | mlm | r=1 | 20 | 1.977 | 0.02 | 0% | 1.073 | 0.30 | 0.006 | **0%** | 36.5 | 0% |
| nt250m_mlm_ecoli_s2 | ecoli | 250m | mlm | r=0 | 20 | 2.194 | 0.02 | 0% | 2.421 | 0.01 | 0.000 | **0%** | 36.4 | 0% |

Members: target surprise 1.237 b/nt against 2.194 for the matched non-member control; ICM extraction at worst 70%.
