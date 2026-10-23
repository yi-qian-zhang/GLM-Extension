# Reconstruction audit — recon_r8

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`. `ICM exact` is the attack: several restarts, each swept to a fixed point, and the one with the best pseudo-log-likelihood is output, which an attacker can compute without the truth. `any-restart` is the oracle over the same restarts and is an upper bound, not an attack, because choosing it needs the answer.

| run | data | tok | obj | tier | n | target b/nt | top1 | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 25 | 1.296 | 0.31 | 0% | 0.116 | 0.96 | 0.718 | **0%** | 34.3 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=4 | 25 | 1.548 | 0.23 | 0% | 0.451 | 0.78 | 0.176 | **0%** | 32.6 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=1 | 25 | 1.755 | 0.17 | 0% | 0.583 | 0.70 | 0.230 | **0%** | 34.0 | 0% |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 25 | 2.160 | 0.09 | 0% | 2.400 | 0.11 | 0.000 | **0%** | 33.6 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=16 | 25 | 1.185 | 0.39 | 0% | 0.096 | 0.96 | 0.793 | **0%** | 34.4 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=4 | 25 | 1.551 | 0.24 | 0% | 0.418 | 0.78 | 0.317 | **0%** | 33.5 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=1 | 25 | 1.743 | 0.17 | 0% | 0.550 | 0.73 | 0.187 | **0%** | 34.4 | 0% |
| 3mer_mlm0.15_s1 | human | 3mer | mlm@0.15 | r=0 | 25 | 2.187 | 0.07 | 0% | 2.476 | 0.09 | 0.000 | **0%** | 34.5 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 25 | 0.851 | 0.41 | 0% | 0.134 | 0.97 | 0.843 | **20%** | 21.0 | 20% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.168 | 0.26 | 0% | 0.303 | 0.87 | 0.428 | **0%** | 31.2 | 0% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.219 | 0.23 | 0% | 0.271 | 0.89 | 0.503 | **4%** | 30.6 | 4% |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.454 | 0.02 | 0% | 2.490 | 0.02 | 0.000 | **0%** | 34.5 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=16 | 25 | 0.764 | 0.47 | 0% | 0.112 | 0.97 | 0.843 | **24%** | 21.2 | 24% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.096 | 0.29 | 0% | 0.259 | 0.87 | 0.412 | **0%** | 28.8 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.218 | 0.24 | 0% | 0.222 | 0.92 | 0.660 | **0%** | 30.6 | 0% |
| 6mer_mlm0.15_s1 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.457 | 0.02 | 0% | 2.512 | 0.04 | 0.000 | **0%** | 34.1 | 0% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=16 | 25 | 0.784 | 0.50 | 0% | 0.122 | 0.96 | 0.791 | **20%** | 18.8 | 20% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=4 | 25 | 1.142 | 0.28 | 0% | 0.256 | 0.89 | 0.533 | **4%** | 27.6 | 4% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=1 | 25 | 1.303 | 0.22 | 0% | 0.328 | 0.85 | 0.458 | **4%** | 32.7 | 4% |
| 6mer_mlm0.15_s2 | human | 6mer | mlm@0.15 | r=0 | 25 | 2.491 | 0.02 | 0% | 2.519 | 0.01 | 0.000 | **0%** | 34.8 | 0% |

Members: target surprise 1.242 b/nt against 2.350 for the matched non-member control; ICM extraction at worst 24%.
