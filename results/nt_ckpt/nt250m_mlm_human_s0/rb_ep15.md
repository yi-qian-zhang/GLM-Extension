# Reconstruction audit — rb_ep15

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nt250m_mlm_human_s0 | human | 250m | mlm | r=16 | 50 | 1.145 | 0.34 | 6% | 0.876 | 0.51 | 0.179 | **6%** | 28.9 | 18% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=1 | 50 | 1.657 | 0.12 | 0% | 1.467 | 0.18 | 0.005 | **0%** | 34.0 | 0% |
| nt250m_mlm_human_s0 | human | 250m | mlm | r=0 | 50 | 1.771 | 0.08 | 0% | 1.736 | 0.10 | 0.001 | **0%** | 33.6 | 0% |

Members: target surprise 1.401 b/nt against 1.771 for the matched non-member control; ICM extraction at worst 6%.
