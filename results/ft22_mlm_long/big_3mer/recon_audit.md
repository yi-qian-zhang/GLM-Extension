# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_ft_s0 | human | 3mer | mlm@0.15 | r=16 | 20 | 1.197 | 0.35 | 0% | 0.084 | 0.97 | 0.790 | **0%** | 33.7 | 0% |
| 3mer_mlm0.15_ft_s0 | human | 3mer | mlm@0.15 | r=4 | 20 | 1.478 | 0.25 | 0% | 0.410 | 0.80 | 0.391 | **0%** | 32.0 | 0% |
| 3mer_mlm0.15_ft_s0 | human | 3mer | mlm@0.15 | r=1 | 20 | 1.704 | 0.20 | 0% | 0.527 | 0.74 | 0.213 | **0%** | 33.5 | 0% |
| 3mer_mlm0.15_ft_s0 | human | 3mer | mlm@0.15 | r=0 | 20 | 2.149 | 0.05 | 0% | 2.517 | 0.10 | 0.000 | **0%** | 34.3 | 0% |

Members: target surprise 1.460 b/nt against 2.149 for the matched non-member control; ICM extraction at worst 0%.
