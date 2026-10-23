# Reconstruction audit — recon_n50_ep190

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 50 | 0.568 | 0.57 | 0% | 0.007 | 1.00 | 0.974 | **74%** | 5.6 | 74% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 50 | 0.920 | 0.38 | 0% | 0.010 | 1.00 | 0.987 | **58%** | 11.1 | 58% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 50 | 3.160 | 0.02 | 0% | 3.212 | 0.02 | 0.000 | **0%** | 34.3 | 0% |

Members: target surprise 0.744 b/nt against 3.160 for the matched non-member control; ICM extraction at worst 74%.
