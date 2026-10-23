# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | yeast | 3mer | mlm@0.15 | r=16 | 20 | 2.046 | 0.03 | 0.000 | 0% | 37.1 | **0%** | 36.5 |
| 3mer_mlm0.15_s0 | yeast | 3mer | mlm@0.15 | r=4 | 20 | 2.091 | 0.02 | 0.000 | 0% | 36.8 | **0%** | 35.9 |
| 3mer_mlm0.15_s0 | yeast | 3mer | mlm@0.15 | r=1 | 20 | 2.088 | 0.01 | 0.000 | 0% | 35.9 | **0%** | 35.6 |
| 3mer_mlm0.15_s0 | yeast | 3mer | mlm@0.15 | r=0 | 20 | 2.051 | 0.03 | 0.000 | 0% | 35.3 | **0%** | 35.5 |
| 3mer_mlm0.15_s1 | yeast | 3mer | mlm@0.15 | r=16 | 20 | 2.050 | 0.03 | 0.000 | 0% | 37.7 | **0%** | 37.0 |
| 3mer_mlm0.15_s1 | yeast | 3mer | mlm@0.15 | r=4 | 20 | 2.096 | 0.02 | 0.000 | 0% | 36.6 | **0%** | 35.6 |
| 3mer_mlm0.15_s1 | yeast | 3mer | mlm@0.15 | r=1 | 20 | 2.090 | 0.01 | 0.000 | 0% | 35.9 | **0%** | 35.0 |
| 3mer_mlm0.15_s1 | yeast | 3mer | mlm@0.15 | r=0 | 20 | 2.073 | 0.03 | 0.000 | 0% | 36.0 | **0%** | 36.5 |
| 3mer_mlm0.5_s0 | yeast | 3mer | mlm@0.5 | r=16 | 20 | 2.041 | 0.03 | 0.000 | 0% | 37.2 | **0%** | 36.0 |
| 3mer_mlm0.5_s0 | yeast | 3mer | mlm@0.5 | r=4 | 20 | 2.090 | 0.02 | 0.000 | 0% | 36.4 | **0%** | 34.9 |
| 3mer_mlm0.5_s0 | yeast | 3mer | mlm@0.5 | r=1 | 20 | 2.082 | 0.01 | 0.000 | 0% | 35.7 | **0%** | 36.3 |
| 3mer_mlm0.5_s0 | yeast | 3mer | mlm@0.5 | r=0 | 20 | 2.045 | 0.03 | 0.000 | 0% | 35.5 | **0%** | 36.2 |
| 3mer_mlm0.5_s1 | yeast | 3mer | mlm@0.5 | r=16 | 20 | 2.055 | 0.03 | 0.000 | 0% | 37.3 | **0%** | 36.3 |
| 3mer_mlm0.5_s1 | yeast | 3mer | mlm@0.5 | r=4 | 20 | 2.090 | 0.03 | 0.000 | 0% | 35.5 | **0%** | 35.5 |
| 3mer_mlm0.5_s1 | yeast | 3mer | mlm@0.5 | r=1 | 20 | 2.088 | 0.01 | 0.000 | 0% | 35.1 | **0%** | 36.0 |
| 3mer_mlm0.5_s1 | yeast | 3mer | mlm@0.5 | r=0 | 20 | 2.076 | 0.03 | 0.000 | 0% | 35.5 | **0%** | 36.6 |
| 4mer_mlm0.15_s0 | yeast | 4mer | mlm@0.15 | r=16 | 20 | 2.068 | 0.01 | 0.000 | 0% | 36.9 | **0%** | 36.5 |
| 4mer_mlm0.15_s0 | yeast | 4mer | mlm@0.15 | r=4 | 20 | 2.078 | 0.00 | 0.000 | 0% | 35.6 | **0%** | 36.6 |
| 4mer_mlm0.15_s0 | yeast | 4mer | mlm@0.15 | r=1 | 20 | 2.067 | 0.01 | 0.000 | 0% | 34.7 | **0%** | 36.1 |
| 4mer_mlm0.15_s0 | yeast | 4mer | mlm@0.15 | r=0 | 20 | 2.076 | 0.02 | 0.000 | 0% | 34.7 | **0%** | 35.1 |
| 4mer_mlm0.15_s1 | yeast | 4mer | mlm@0.15 | r=16 | 20 | 2.073 | 0.02 | 0.000 | 0% | 37.4 | **0%** | 37.1 |
| 4mer_mlm0.15_s1 | yeast | 4mer | mlm@0.15 | r=4 | 20 | 2.089 | 0.00 | 0.000 | 0% | 35.5 | **0%** | 36.6 |
| 4mer_mlm0.15_s1 | yeast | 4mer | mlm@0.15 | r=1 | 20 | 2.082 | 0.01 | 0.000 | 0% | 36.1 | **0%** | 36.2 |
| 4mer_mlm0.15_s1 | yeast | 4mer | mlm@0.15 | r=0 | 20 | 2.110 | 0.01 | 0.000 | 0% | 35.6 | **0%** | 36.8 |
| 4mer_mlm0.5_s0 | yeast | 4mer | mlm@0.5 | r=16 | 20 | 2.066 | 0.01 | 0.000 | 0% | 36.7 | **0%** | 37.1 |
| 4mer_mlm0.5_s0 | yeast | 4mer | mlm@0.5 | r=4 | 20 | 2.083 | 0.01 | 0.000 | 0% | 35.8 | **0%** | 35.8 |
| 4mer_mlm0.5_s0 | yeast | 4mer | mlm@0.5 | r=1 | 20 | 2.071 | 0.02 | 0.000 | 0% | 35.5 | **0%** | 35.2 |
| 4mer_mlm0.5_s0 | yeast | 4mer | mlm@0.5 | r=0 | 20 | 2.081 | 0.01 | 0.000 | 0% | 35.4 | **0%** | 35.2 |
| 4mer_mlm0.5_s1 | yeast | 4mer | mlm@0.5 | r=16 | 20 | 2.072 | 0.00 | 0.000 | 0% | 37.2 | **0%** | 36.5 |
| 4mer_mlm0.5_s1 | yeast | 4mer | mlm@0.5 | r=4 | 20 | 2.085 | 0.01 | 0.000 | 0% | 35.2 | **0%** | 35.8 |
| 4mer_mlm0.5_s1 | yeast | 4mer | mlm@0.5 | r=1 | 20 | 2.066 | 0.02 | 0.000 | 0% | 35.9 | **0%** | 35.9 |
| 4mer_mlm0.5_s1 | yeast | 4mer | mlm@0.5 | r=0 | 20 | 2.106 | 0.02 | 0.000 | 0% | 35.3 | **0%** | 35.3 |
| 6mer_mlm0.15_s0 | yeast | 6mer | mlm@0.15 | r=16 | 20 | 2.059 | 0.01 | 0.000 | 0% | 35.5 | **0%** | 36.4 |
| 6mer_mlm0.15_s0 | yeast | 6mer | mlm@0.15 | r=4 | 20 | 2.090 | 0.01 | 0.000 | 0% | 35.5 | **0%** | 34.2 |
| 6mer_mlm0.15_s0 | yeast | 6mer | mlm@0.15 | r=1 | 20 | 2.167 | 0.00 | 0.000 | 0% | 35.6 | **0%** | 36.5 |
| 6mer_mlm0.15_s0 | yeast | 6mer | mlm@0.15 | r=0 | 20 | 2.134 | 0.02 | 0.000 | 0% | 35.8 | **0%** | 36.0 |
| 6mer_mlm0.15_s1 | yeast | 6mer | mlm@0.15 | r=16 | 20 | 2.033 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 36.7 |
| 6mer_mlm0.15_s1 | yeast | 6mer | mlm@0.15 | r=4 | 20 | 2.115 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 35.6 |
| 6mer_mlm0.15_s1 | yeast | 6mer | mlm@0.15 | r=1 | 20 | 2.161 | 0.00 | 0.000 | 0% | 36.0 | **0%** | 36.2 |
| 6mer_mlm0.15_s1 | yeast | 6mer | mlm@0.15 | r=0 | 20 | 2.190 | 0.02 | 0.000 | 0% | 35.1 | **0%** | 35.2 |
| 6mer_mlm0.5_s0 | yeast | 6mer | mlm@0.5 | r=16 | 20 | 1.887 | 0.02 | 0.000 | 0% | 36.0 | **0%** | 35.5 |
| 6mer_mlm0.5_s0 | yeast | 6mer | mlm@0.5 | r=4 | 20 | 2.016 | 0.02 | 0.000 | 0% | 34.9 | **0%** | 35.9 |
| 6mer_mlm0.5_s0 | yeast | 6mer | mlm@0.5 | r=1 | 20 | 2.095 | 0.02 | 0.000 | 0% | 35.6 | **0%** | 35.4 |
| 6mer_mlm0.5_s0 | yeast | 6mer | mlm@0.5 | r=0 | 20 | 2.156 | 0.02 | 0.000 | 0% | 35.7 | **0%** | 36.7 |
| 6mer_mlm0.5_s1 | yeast | 6mer | mlm@0.5 | r=16 | 20 | 2.038 | 0.01 | 0.000 | 0% | 37.0 | **0%** | 36.2 |
| 6mer_mlm0.5_s1 | yeast | 6mer | mlm@0.5 | r=4 | 20 | 2.085 | 0.00 | 0.000 | 0% | 36.0 | **0%** | 35.6 |
| 6mer_mlm0.5_s1 | yeast | 6mer | mlm@0.5 | r=1 | 20 | 2.135 | 0.00 | 0.000 | 0% | 35.0 | **0%** | 35.9 |
| 6mer_mlm0.5_s1 | yeast | 6mer | mlm@0.5 | r=0 | 20 | 2.188 | 0.02 | 0.000 | 0% | 36.0 | **0%** | 36.0 |
| char_mlm0.15_s0 | yeast | char | mlm@0.15 | r=16 | 20 | 2.043 | 0.25 | 0.000 | 0% | 36.6 | **0%** | 36.9 |
| char_mlm0.15_s0 | yeast | char | mlm@0.15 | r=4 | 20 | 2.046 | 0.25 | 0.000 | 0% | 37.0 | **0%** | 36.5 |
| char_mlm0.15_s0 | yeast | char | mlm@0.15 | r=1 | 20 | 2.040 | 0.26 | 0.000 | 0% | 35.2 | **0%** | 36.6 |
| char_mlm0.15_s0 | yeast | char | mlm@0.15 | r=0 | 20 | 2.024 | 0.27 | 0.000 | 0% | 35.7 | **0%** | 35.9 |
| char_mlm0.15_s1 | yeast | char | mlm@0.15 | r=16 | 20 | 2.039 | 0.25 | 0.000 | 0% | 37.0 | **0%** | 37.0 |
| char_mlm0.15_s1 | yeast | char | mlm@0.15 | r=4 | 20 | 2.045 | 0.23 | 0.000 | 0% | 36.8 | **0%** | 37.0 |
| char_mlm0.15_s1 | yeast | char | mlm@0.15 | r=1 | 20 | 2.032 | 0.26 | 0.000 | 0% | 35.0 | **0%** | 36.1 |
| char_mlm0.15_s1 | yeast | char | mlm@0.15 | r=0 | 20 | 2.025 | 0.25 | 0.000 | 0% | 35.5 | **0%** | 35.5 |
| char_mlm0.5_s0 | yeast | char | mlm@0.5 | r=16 | 20 | 2.020 | 0.27 | 0.000 | 0% | 36.6 | **0%** | 37.0 |
| char_mlm0.5_s0 | yeast | char | mlm@0.5 | r=4 | 20 | 2.023 | 0.27 | 0.000 | 0% | 35.3 | **0%** | 35.5 |
| char_mlm0.5_s0 | yeast | char | mlm@0.5 | r=1 | 20 | 2.031 | 0.26 | 0.000 | 0% | 35.9 | **0%** | 35.7 |
| char_mlm0.5_s0 | yeast | char | mlm@0.5 | r=0 | 20 | 2.001 | 0.28 | 0.000 | 0% | 35.2 | **0%** | 36.1 |
| char_mlm0.5_s1 | yeast | char | mlm@0.5 | r=16 | 20 | 2.022 | 0.28 | 0.000 | 0% | 36.8 | **0%** | 36.4 |
| char_mlm0.5_s1 | yeast | char | mlm@0.5 | r=4 | 20 | 2.034 | 0.25 | 0.000 | 0% | 35.7 | **0%** | 36.5 |
| char_mlm0.5_s1 | yeast | char | mlm@0.5 | r=1 | 20 | 2.031 | 0.27 | 0.000 | 0% | 34.8 | **0%** | 35.8 |
| char_mlm0.5_s1 | yeast | char | mlm@0.5 | r=0 | 20 | 2.022 | 0.27 | 0.000 | 0% | 35.8 | **0%** | 35.6 |

Members: target surprise 2.064 b/nt against 2.085 for the matched non-member control; ICM extraction at worst 0%.
