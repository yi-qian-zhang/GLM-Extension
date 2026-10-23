# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | gue | 3mer | mlm@0.15 | r=16 | 20 | 2.042 | 0.03 | 0.000 | 0% | 35.7 | **0%** | 35.9 |
| 3mer_mlm0.15_s0 | gue | 3mer | mlm@0.15 | r=4 | 20 | 2.058 | 0.03 | 0.000 | 0% | 35.4 | **0%** | 35.8 |
| 3mer_mlm0.15_s0 | gue | 3mer | mlm@0.15 | r=1 | 20 | 2.067 | 0.03 | 0.000 | 0% | 35.5 | **0%** | 36.1 |
| 3mer_mlm0.15_s0 | gue | 3mer | mlm@0.15 | r=0 | 20 | 2.048 | 0.02 | 0.000 | 0% | 37.8 | **0%** | 35.3 |
| 3mer_mlm0.15_s1 | gue | 3mer | mlm@0.15 | r=16 | 20 | 2.051 | 0.04 | 0.000 | 0% | 35.5 | **0%** | 36.1 |
| 3mer_mlm0.15_s1 | gue | 3mer | mlm@0.15 | r=4 | 20 | 2.060 | 0.03 | 0.000 | 0% | 34.9 | **0%** | 35.6 |
| 3mer_mlm0.15_s1 | gue | 3mer | mlm@0.15 | r=1 | 20 | 2.077 | 0.02 | 0.000 | 0% | 35.5 | **0%** | 35.8 |
| 3mer_mlm0.15_s1 | gue | 3mer | mlm@0.15 | r=0 | 20 | 2.070 | 0.02 | 0.000 | 0% | 36.4 | **0%** | 36.9 |
| 3mer_mlm0.5_s0 | gue | 3mer | mlm@0.5 | r=16 | 20 | 2.048 | 0.03 | 0.000 | 0% | 35.6 | **0%** | 36.1 |
| 3mer_mlm0.5_s0 | gue | 3mer | mlm@0.5 | r=4 | 20 | 2.061 | 0.04 | 0.000 | 0% | 34.9 | **0%** | 34.6 |
| 3mer_mlm0.5_s0 | gue | 3mer | mlm@0.5 | r=1 | 20 | 2.070 | 0.01 | 0.000 | 0% | 35.8 | **0%** | 36.4 |
| 3mer_mlm0.5_s0 | gue | 3mer | mlm@0.5 | r=0 | 20 | 2.053 | 0.02 | 0.000 | 0% | 36.6 | **0%** | 34.9 |
| 3mer_mlm0.5_s1 | gue | 3mer | mlm@0.5 | r=16 | 20 | 2.042 | 0.03 | 0.000 | 0% | 34.7 | **0%** | 35.8 |
| 3mer_mlm0.5_s1 | gue | 3mer | mlm@0.5 | r=4 | 20 | 2.044 | 0.04 | 0.000 | 0% | 34.6 | **0%** | 35.9 |
| 3mer_mlm0.5_s1 | gue | 3mer | mlm@0.5 | r=1 | 20 | 2.066 | 0.03 | 0.000 | 0% | 35.1 | **0%** | 35.5 |
| 3mer_mlm0.5_s1 | gue | 3mer | mlm@0.5 | r=0 | 20 | 2.066 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 36.0 |
| 4mer_mlm0.15_s0 | gue | 4mer | mlm@0.15 | r=16 | 20 | 2.065 | 0.01 | 0.000 | 0% | 35.4 | **0%** | 36.4 |
| 4mer_mlm0.15_s0 | gue | 4mer | mlm@0.15 | r=4 | 20 | 2.064 | 0.00 | 0.000 | 0% | 35.8 | **0%** | 36.0 |
| 4mer_mlm0.15_s0 | gue | 4mer | mlm@0.15 | r=1 | 20 | 2.077 | 0.00 | 0.000 | 0% | 34.8 | **0%** | 35.3 |
| 4mer_mlm0.15_s0 | gue | 4mer | mlm@0.15 | r=0 | 20 | 2.074 | 0.01 | 0.000 | 0% | 35.8 | **0%** | 35.2 |
| 4mer_mlm0.15_s1 | gue | 4mer | mlm@0.15 | r=16 | 20 | 2.061 | 0.01 | 0.000 | 0% | 35.4 | **0%** | 35.9 |
| 4mer_mlm0.15_s1 | gue | 4mer | mlm@0.15 | r=4 | 20 | 2.057 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 35.1 |
| 4mer_mlm0.15_s1 | gue | 4mer | mlm@0.15 | r=1 | 20 | 2.075 | 0.00 | 0.000 | 0% | 35.0 | **0%** | 35.4 |
| 4mer_mlm0.15_s1 | gue | 4mer | mlm@0.15 | r=0 | 20 | 2.099 | 0.01 | 0.000 | 0% | 36.1 | **0%** | 36.2 |
| 4mer_mlm0.5_s0 | gue | 4mer | mlm@0.5 | r=16 | 20 | 2.055 | 0.01 | 0.000 | 0% | 34.5 | **0%** | 35.5 |
| 4mer_mlm0.5_s0 | gue | 4mer | mlm@0.5 | r=4 | 20 | 2.055 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 35.8 |
| 4mer_mlm0.5_s0 | gue | 4mer | mlm@0.5 | r=1 | 20 | 2.062 | 0.01 | 0.000 | 0% | 34.6 | **0%** | 36.2 |
| 4mer_mlm0.5_s0 | gue | 4mer | mlm@0.5 | r=0 | 20 | 2.084 | 0.01 | 0.000 | 0% | 35.6 | **0%** | 36.5 |
| 4mer_mlm0.5_s1 | gue | 4mer | mlm@0.5 | r=16 | 20 | 2.061 | 0.02 | 0.000 | 0% | 35.6 | **0%** | 36.5 |
| 4mer_mlm0.5_s1 | gue | 4mer | mlm@0.5 | r=4 | 20 | 2.047 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 35.7 |
| 4mer_mlm0.5_s1 | gue | 4mer | mlm@0.5 | r=1 | 20 | 2.077 | 0.01 | 0.000 | 0% | 35.2 | **0%** | 35.4 |
| 4mer_mlm0.5_s1 | gue | 4mer | mlm@0.5 | r=0 | 20 | 2.103 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 35.0 |
| 6mer_mlm0.15_s0 | gue | 6mer | mlm@0.15 | r=16 | 20 | 2.026 | 0.02 | 0.000 | 0% | 35.0 | **0%** | 36.0 |
| 6mer_mlm0.15_s0 | gue | 6mer | mlm@0.15 | r=4 | 20 | 2.068 | 0.01 | 0.000 | 0% | 35.3 | **0%** | 35.7 |
| 6mer_mlm0.15_s0 | gue | 6mer | mlm@0.15 | r=1 | 20 | 2.118 | 0.01 | 0.000 | 0% | 34.7 | **0%** | 35.8 |
| 6mer_mlm0.15_s0 | gue | 6mer | mlm@0.15 | r=0 | 20 | 2.121 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 35.5 |
| 6mer_mlm0.15_s1 | gue | 6mer | mlm@0.15 | r=16 | 20 | 2.038 | 0.04 | 0.000 | 0% | 35.5 | **0%** | 36.1 |
| 6mer_mlm0.15_s1 | gue | 6mer | mlm@0.15 | r=4 | 20 | 2.083 | 0.01 | 0.000 | 0% | 35.3 | **0%** | 36.0 |
| 6mer_mlm0.15_s1 | gue | 6mer | mlm@0.15 | r=1 | 20 | 2.131 | 0.00 | 0.000 | 0% | 35.9 | **0%** | 35.6 |
| 6mer_mlm0.15_s1 | gue | 6mer | mlm@0.15 | r=0 | 20 | 2.154 | 0.01 | 0.000 | 0% | 36.7 | **0%** | 34.8 |
| 6mer_mlm0.5_s0 | gue | 6mer | mlm@0.5 | r=16 | 20 | 1.949 | 0.03 | 0.000 | 0% | 34.5 | **0%** | 34.8 |
| 6mer_mlm0.5_s0 | gue | 6mer | mlm@0.5 | r=4 | 20 | 1.998 | 0.01 | 0.000 | 0% | 36.1 | **0%** | 35.8 |
| 6mer_mlm0.5_s0 | gue | 6mer | mlm@0.5 | r=1 | 20 | 2.066 | 0.00 | 0.000 | 0% | 34.5 | **0%** | 34.7 |
| 6mer_mlm0.5_s0 | gue | 6mer | mlm@0.5 | r=0 | 20 | 2.139 | 0.01 | 0.000 | 0% | 37.0 | **0%** | 35.9 |
| 6mer_mlm0.5_s1 | gue | 6mer | mlm@0.5 | r=16 | 20 | 1.930 | 0.03 | 0.000 | 0% | 34.1 | **0%** | 35.1 |
| 6mer_mlm0.5_s1 | gue | 6mer | mlm@0.5 | r=4 | 20 | 1.998 | 0.02 | 0.000 | 0% | 36.1 | **0%** | 36.9 |
| 6mer_mlm0.5_s1 | gue | 6mer | mlm@0.5 | r=1 | 20 | 2.074 | 0.01 | 0.000 | 0% | 34.4 | **0%** | 35.6 |
| 6mer_mlm0.5_s1 | gue | 6mer | mlm@0.5 | r=0 | 20 | 2.172 | 0.01 | 0.000 | 0% | 36.6 | **0%** | 35.5 |
| char_mlm0.15_s0 | gue | char | mlm@0.15 | r=16 | 20 | 2.016 | 0.28 | 0.000 | 0% | 35.4 | **0%** | 36.8 |
| char_mlm0.15_s0 | gue | char | mlm@0.15 | r=4 | 20 | 2.030 | 0.26 | 0.000 | 0% | 35.0 | **0%** | 35.5 |
| char_mlm0.15_s0 | gue | char | mlm@0.15 | r=1 | 20 | 2.025 | 0.24 | 0.000 | 0% | 34.9 | **0%** | 35.4 |
| char_mlm0.15_s0 | gue | char | mlm@0.15 | r=0 | 20 | 2.024 | 0.24 | 0.000 | 0% | 36.5 | **0%** | 35.8 |
| char_mlm0.15_s1 | gue | char | mlm@0.15 | r=16 | 20 | 2.025 | 0.27 | 0.000 | 0% | 35.2 | **0%** | 37.1 |
| char_mlm0.15_s1 | gue | char | mlm@0.15 | r=4 | 20 | 2.026 | 0.27 | 0.000 | 0% | 36.2 | **0%** | 36.0 |
| char_mlm0.15_s1 | gue | char | mlm@0.15 | r=1 | 20 | 2.029 | 0.26 | 0.000 | 0% | 35.5 | **0%** | 35.1 |
| char_mlm0.15_s1 | gue | char | mlm@0.15 | r=0 | 20 | 2.025 | 0.25 | 0.000 | 0% | 36.0 | **0%** | 36.2 |
| char_mlm0.5_s0 | gue | char | mlm@0.5 | r=16 | 20 | 2.011 | 0.27 | 0.000 | 0% | 35.4 | **0%** | 36.8 |
| char_mlm0.5_s0 | gue | char | mlm@0.5 | r=4 | 20 | 2.020 | 0.25 | 0.000 | 0% | 35.4 | **0%** | 35.3 |
| char_mlm0.5_s0 | gue | char | mlm@0.5 | r=1 | 20 | 2.016 | 0.25 | 0.000 | 0% | 35.4 | **0%** | 36.3 |
| char_mlm0.5_s0 | gue | char | mlm@0.5 | r=0 | 20 | 2.027 | 0.25 | 0.000 | 0% | 37.0 | **0%** | 36.0 |
| char_mlm0.5_s1 | gue | char | mlm@0.5 | r=16 | 20 | 2.011 | 0.27 | 0.000 | 0% | 35.3 | **0%** | 37.0 |
| char_mlm0.5_s1 | gue | char | mlm@0.5 | r=4 | 20 | 2.023 | 0.27 | 0.000 | 0% | 35.4 | **0%** | 36.2 |
| char_mlm0.5_s1 | gue | char | mlm@0.5 | r=1 | 20 | 2.012 | 0.28 | 0.000 | 0% | 35.5 | **0%** | 35.2 |
| char_mlm0.5_s1 | gue | char | mlm@0.5 | r=0 | 20 | 2.023 | 0.25 | 0.000 | 0% | 37.1 | **0%** | 37.2 |

Members: target surprise 2.045 b/nt against 2.080 for the matched non-member control; ICM extraction at worst 0%.
