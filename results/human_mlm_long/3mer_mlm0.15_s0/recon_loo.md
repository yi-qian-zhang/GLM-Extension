# Reconstruction audit — recon_loo

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters. `LOO` is the predictor that matches THAT decoder rather than left-to-right decoding: every other target token held at its true value, one masked, which is the conditional ICM converges to and the one the PLL scorer reads. `LOO bound` is its per-token top-1 rate raised to the number of target tokens, so it is the rate at which a fixed point can be the true string, and it is the column to read against `ICM exact`.

| run | data | tok | obj | tier | n | steps | target b/nt | top1 | bound | prefix | LOO b/nt | LOO top1 | LOO bound | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=16 | 25 |  | 1.296 | 0.31 | 0.000 | 0% | 0.116 | 0.96 | 0.718 | **0%** | 35.4 |
| 3mer_mlm0.15_s0 | human | 3mer | mlm@0.15 | r=0 | 25 |  | 2.160 | 0.09 | 0.000 | 0% | 2.400 | 0.11 | 0.000 | **0%** | 34.3 |

Members: target surprise 1.296 b/nt against 2.160 for the matched non-member control; ICM extraction at worst 0%.
