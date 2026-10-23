# Reconstruction audit — recon_r64

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 25 | 0.851 | 0.41 | 0% | 0.134 | 0.97 | 0.843 | **44%** | 11.3 | 44% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.168 | 0.26 | 0% | 0.303 | 0.87 | 0.428 | **4%** | 28.2 | 4% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.219 | 0.23 | 0% | 0.271 | 0.89 | 0.503 | **4%** | 30.6 | 4% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.454 | 0.02 | 0% | 2.490 | 0.02 | 0.000 | **0%** | 34.2 | 0% |

Members: target surprise 1.080 b/nt against 2.454 for the matched non-member control; ICM extraction at worst 44%.
