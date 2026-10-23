# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=16 | 20 | 2.071 | 0.04 | 0.000 | 0% | 36.4 | **0%** | 36.5 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=4 | 20 | 2.084 | 0.02 | 0.000 | 0% | 36.2 | **0%** | 36.1 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=1 | 20 | 2.113 | 0.02 | 0.000 | 0% | 34.6 | **0%** | 36.0 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=0 | 20 | 2.096 | 0.03 | 0.000 | 0% | 34.9 | **0%** | 35.1 |
| 3mer_mlm0.15_s1 | ecoli | 3mer | mlm@0.15 | r=16 | 20 | 2.090 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 36.6 |
| 3mer_mlm0.15_s1 | ecoli | 3mer | mlm@0.15 | r=4 | 20 | 2.078 | 0.02 | 0.000 | 0% | 37.2 | **0%** | 36.0 |
| 3mer_mlm0.15_s1 | ecoli | 3mer | mlm@0.15 | r=1 | 20 | 2.105 | 0.02 | 0.000 | 0% | 35.2 | **0%** | 35.3 |
| 3mer_mlm0.15_s1 | ecoli | 3mer | mlm@0.15 | r=0 | 20 | 2.098 | 0.02 | 0.000 | 0% | 35.1 | **0%** | 35.3 |
| 3mer_mlm0.5_s0 | ecoli | 3mer | mlm@0.5 | r=16 | 20 | 2.073 | 0.02 | 0.000 | 0% | 36.0 | **0%** | 36.4 |
| 3mer_mlm0.5_s0 | ecoli | 3mer | mlm@0.5 | r=4 | 20 | 2.094 | 0.02 | 0.000 | 0% | 34.7 | **0%** | 36.8 |
| 3mer_mlm0.5_s0 | ecoli | 3mer | mlm@0.5 | r=1 | 20 | 2.102 | 0.02 | 0.000 | 0% | 34.9 | **0%** | 36.0 |
| 3mer_mlm0.5_s0 | ecoli | 3mer | mlm@0.5 | r=0 | 20 | 2.103 | 0.02 | 0.000 | 0% | 35.3 | **0%** | 36.7 |
| 3mer_mlm0.5_s1 | ecoli | 3mer | mlm@0.5 | r=16 | 20 | 2.077 | 0.03 | 0.000 | 0% | 34.5 | **0%** | 35.5 |
| 3mer_mlm0.5_s1 | ecoli | 3mer | mlm@0.5 | r=4 | 20 | 2.099 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 35.9 |
| 3mer_mlm0.5_s1 | ecoli | 3mer | mlm@0.5 | r=1 | 20 | 2.100 | 0.03 | 0.000 | 0% | 35.0 | **0%** | 36.0 |
| 3mer_mlm0.5_s1 | ecoli | 3mer | mlm@0.5 | r=0 | 20 | 2.097 | 0.01 | 0.000 | 0% | 34.9 | **0%** | 36.0 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=16 | 20 | 2.066 | 0.01 | 0.000 | 0% | 36.1 | **0%** | 36.3 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=4 | 20 | 2.058 | 0.02 | 0.000 | 0% | 36.3 | **0%** | 36.1 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=1 | 20 | 2.079 | 0.01 | 0.000 | 0% | 35.2 | **0%** | 36.5 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=0 | 20 | 2.090 | 0.00 | 0.000 | 0% | 35.3 | **0%** | 35.3 |
| 4mer_mlm0.15_s1 | ecoli | 4mer | mlm@0.15 | r=16 | 20 | 2.070 | 0.00 | 0.000 | 0% | 36.6 | **0%** | 36.1 |
| 4mer_mlm0.15_s1 | ecoli | 4mer | mlm@0.15 | r=4 | 20 | 2.057 | 0.02 | 0.000 | 0% | 35.7 | **0%** | 36.1 |
| 4mer_mlm0.15_s1 | ecoli | 4mer | mlm@0.15 | r=1 | 20 | 2.078 | 0.01 | 0.000 | 0% | 35.0 | **0%** | 35.4 |
| 4mer_mlm0.15_s1 | ecoli | 4mer | mlm@0.15 | r=0 | 20 | 2.116 | 0.02 | 0.000 | 0% | 35.3 | **0%** | 34.9 |
| 4mer_mlm0.5_s0 | ecoli | 4mer | mlm@0.5 | r=16 | 20 | 2.084 | 0.02 | 0.000 | 0% | 36.5 | **0%** | 36.3 |
| 4mer_mlm0.5_s0 | ecoli | 4mer | mlm@0.5 | r=4 | 20 | 2.071 | 0.01 | 0.000 | 0% | 35.4 | **0%** | 36.2 |
| 4mer_mlm0.5_s0 | ecoli | 4mer | mlm@0.5 | r=1 | 20 | 2.099 | 0.01 | 0.000 | 0% | 35.3 | **0%** | 35.4 |
| 4mer_mlm0.5_s0 | ecoli | 4mer | mlm@0.5 | r=0 | 20 | 2.102 | 0.00 | 0.000 | 0% | 36.1 | **0%** | 37.0 |
| 4mer_mlm0.5_s1 | ecoli | 4mer | mlm@0.5 | r=16 | 20 | 2.072 | 0.01 | 0.000 | 0% | 36.6 | **0%** | 36.5 |
| 4mer_mlm0.5_s1 | ecoli | 4mer | mlm@0.5 | r=4 | 20 | 2.066 | 0.01 | 0.000 | 0% | 35.8 | **0%** | 36.0 |
| 4mer_mlm0.5_s1 | ecoli | 4mer | mlm@0.5 | r=1 | 20 | 2.077 | 0.02 | 0.000 | 0% | 35.2 | **0%** | 34.5 |
| 4mer_mlm0.5_s1 | ecoli | 4mer | mlm@0.5 | r=0 | 20 | 2.107 | 0.02 | 0.000 | 0% | 35.1 | **0%** | 34.8 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=16 | 20 | 2.100 | 0.00 | 0.000 | 0% | 36.3 | **0%** | 36.1 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=4 | 20 | 2.139 | 0.00 | 0.000 | 0% | 35.9 | **0%** | 36.0 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=1 | 20 | 2.167 | 0.00 | 0.000 | 0% | 35.0 | **0%** | 36.4 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=0 | 20 | 2.126 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 36.4 |
| 6mer_mlm0.15_s1 | ecoli | 6mer | mlm@0.15 | r=16 | 20 | 2.095 | 0.00 | 0.000 | 0% | 35.1 | **0%** | 36.8 |
| 6mer_mlm0.15_s1 | ecoli | 6mer | mlm@0.15 | r=4 | 20 | 2.136 | 0.00 | 0.000 | 0% | 36.2 | **0%** | 36.2 |
| 6mer_mlm0.15_s1 | ecoli | 6mer | mlm@0.15 | r=1 | 20 | 2.171 | 0.01 | 0.000 | 0% | 34.9 | **0%** | 36.0 |
| 6mer_mlm0.15_s1 | ecoli | 6mer | mlm@0.15 | r=0 | 20 | 2.212 | 0.02 | 0.000 | 0% | 34.6 | **0%** | 35.6 |
| 6mer_mlm0.5_s0 | ecoli | 6mer | mlm@0.5 | r=16 | 20 | 2.054 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 35.9 |
| 6mer_mlm0.5_s0 | ecoli | 6mer | mlm@0.5 | r=4 | 20 | 2.065 | 0.01 | 0.000 | 0% | 35.4 | **0%** | 35.6 |
| 6mer_mlm0.5_s0 | ecoli | 6mer | mlm@0.5 | r=1 | 20 | 2.089 | 0.02 | 0.000 | 0% | 35.2 | **0%** | 35.1 |
| 6mer_mlm0.5_s0 | ecoli | 6mer | mlm@0.5 | r=0 | 20 | 2.163 | 0.01 | 0.000 | 0% | 36.8 | **0%** | 34.6 |
| 6mer_mlm0.5_s1 | ecoli | 6mer | mlm@0.5 | r=16 | 20 | 2.014 | 0.01 | 0.000 | 0% | 36.6 | **0%** | 36.0 |
| 6mer_mlm0.5_s1 | ecoli | 6mer | mlm@0.5 | r=4 | 20 | 2.038 | 0.02 | 0.000 | 0% | 34.8 | **0%** | 36.4 |
| 6mer_mlm0.5_s1 | ecoli | 6mer | mlm@0.5 | r=1 | 20 | 2.062 | 0.02 | 0.000 | 0% | 36.2 | **0%** | 35.2 |
| 6mer_mlm0.5_s1 | ecoli | 6mer | mlm@0.5 | r=0 | 20 | 2.200 | 0.02 | 0.000 | 0% | 35.3 | **0%** | 36.0 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=16 | 20 | 2.033 | 0.22 | 0.000 | 0% | 36.1 | **0%** | 35.8 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=4 | 20 | 2.029 | 0.25 | 0.000 | 0% | 36.6 | **0%** | 36.8 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=1 | 20 | 2.022 | 0.25 | 0.000 | 0% | 35.5 | **0%** | 35.8 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=0 | 20 | 2.021 | 0.24 | 0.000 | 0% | 35.8 | **0%** | 36.2 |
| char_mlm0.15_s1 | ecoli | char | mlm@0.15 | r=16 | 20 | 2.034 | 0.24 | 0.000 | 0% | 36.6 | **0%** | 36.1 |
| char_mlm0.15_s1 | ecoli | char | mlm@0.15 | r=4 | 20 | 2.036 | 0.24 | 0.000 | 0% | 36.1 | **0%** | 37.0 |
| char_mlm0.15_s1 | ecoli | char | mlm@0.15 | r=1 | 20 | 2.024 | 0.26 | 0.000 | 0% | 35.7 | **0%** | 35.2 |
| char_mlm0.15_s1 | ecoli | char | mlm@0.15 | r=0 | 20 | 2.031 | 0.25 | 0.000 | 0% | 35.1 | **0%** | 34.9 |
| char_mlm0.5_s0 | ecoli | char | mlm@0.5 | r=16 | 20 | 2.037 | 0.26 | 0.000 | 0% | 36.1 | **0%** | 36.1 |
| char_mlm0.5_s0 | ecoli | char | mlm@0.5 | r=4 | 20 | 2.034 | 0.27 | 0.000 | 0% | 37.0 | **0%** | 36.5 |
| char_mlm0.5_s0 | ecoli | char | mlm@0.5 | r=1 | 20 | 2.037 | 0.26 | 0.000 | 0% | 35.3 | **0%** | 35.1 |
| char_mlm0.5_s0 | ecoli | char | mlm@0.5 | r=0 | 20 | 2.042 | 0.24 | 0.000 | 0% | 35.6 | **0%** | 35.7 |
| char_mlm0.5_s1 | ecoli | char | mlm@0.5 | r=16 | 20 | 2.038 | 0.27 | 0.000 | 0% | 36.0 | **0%** | 36.0 |
| char_mlm0.5_s1 | ecoli | char | mlm@0.5 | r=4 | 20 | 2.041 | 0.26 | 0.000 | 0% | 36.3 | **0%** | 36.4 |
| char_mlm0.5_s1 | ecoli | char | mlm@0.5 | r=1 | 20 | 2.039 | 0.27 | 0.000 | 0% | 36.0 | **0%** | 34.9 |
| char_mlm0.5_s1 | ecoli | char | mlm@0.5 | r=0 | 20 | 2.046 | 0.25 | 0.000 | 0% | 35.3 | **0%** | 34.9 |

Members: target surprise 2.073 b/nt against 2.103 for the matched non-member control; ICM extraction at worst 0%.
