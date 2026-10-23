# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | ecoli | 3mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s0 | ecoli | 3mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s0 | ecoli | 3mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s0 | ecoli | 3mer | ar | r=0 | 20 | 5.325 | 0.02 | 0.000 | 0% | 37.2 | **nan%** | nan |
| 3mer_ar_s1 | ecoli | 3mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s1 | ecoli | 3mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s1 | ecoli | 3mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 3mer_ar_s1 | ecoli | 3mer | ar | r=0 | 20 | 5.198 | 0.01 | 0.000 | 0% | 35.8 | **nan%** | nan |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=16 | 20 | 2.086 | 0.02 | 0.000 | 0% | 35.9 | **0%** | 35.5 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=4 | 20 | 2.090 | 0.02 | 0.000 | 0% | 36.4 | **0%** | 36.2 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=1 | 20 | 2.106 | 0.03 | 0.000 | 0% | 34.5 | **0%** | 35.9 |
| 3mer_mlm0.15_s0 | ecoli | 3mer | mlm@0.15 | r=0 | 20 | 2.109 | 0.02 | 0.000 | 0% | 35.1 | **0%** | 36.4 |
| 4mer_ar_s0 | ecoli | 4mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s0 | ecoli | 4mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s0 | ecoli | 4mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s0 | ecoli | 4mer | ar | r=0 | 20 | 3.675 | 0.01 | 0.000 | 0% | 35.4 | **nan%** | nan |
| 4mer_ar_s1 | ecoli | 4mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s1 | ecoli | 4mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s1 | ecoli | 4mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 4mer_ar_s1 | ecoli | 4mer | ar | r=0 | 20 | 3.547 | 0.01 | 0.000 | 0% | 36.2 | **nan%** | nan |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=16 | 20 | 2.067 | 0.01 | 0.000 | 0% | 36.2 | **0%** | 37.1 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=4 | 20 | 2.056 | 0.01 | 0.000 | 0% | 36.0 | **0%** | 36.9 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=1 | 20 | 2.081 | 0.01 | 0.000 | 0% | 36.5 | **0%** | 36.1 |
| 4mer_mlm0.15_s0 | ecoli | 4mer | mlm@0.15 | r=0 | 20 | 2.096 | 0.00 | 0.000 | 0% | 36.1 | **0%** | 36.9 |
| 6mer_ar_s0 | ecoli | 6mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | ecoli | 6mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | ecoli | 6mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | ecoli | 6mer | ar | r=0 | 20 | 2.652 | 0.01 | 0.000 | 0% | 35.5 | **nan%** | nan |
| 6mer_ar_s1 | ecoli | 6mer | ar | r=16 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | ecoli | 6mer | ar | r=4 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | ecoli | 6mer | ar | r=1 | 20 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | ecoli | 6mer | ar | r=0 | 20 | 2.593 | 0.01 | 0.000 | 0% | 35.1 | **nan%** | nan |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=16 | 20 | 2.111 | 0.00 | 0.000 | 0% | 36.6 | **0%** | 36.0 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=4 | 20 | 2.157 | 0.00 | 0.000 | 0% | 35.6 | **0%** | 36.2 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=1 | 20 | 2.183 | 0.00 | 0.000 | 0% | 37.5 | **0%** | 36.8 |
| 6mer_mlm0.15_s0 | ecoli | 6mer | mlm@0.15 | r=0 | 20 | 2.165 | 0.00 | 0.000 | 0% | 36.4 | **0%** | 36.4 |
| char_ar_s0 | ecoli | char | ar | r=16 | 20 | 1.043 | 0.70 | 0.000 | 0% | 32.3 | **nan%** | nan |
| char_ar_s0 | ecoli | char | ar | r=4 | 20 | 1.139 | 0.68 | 0.000 | 0% | 33.4 | **nan%** | nan |
| char_ar_s0 | ecoli | char | ar | r=1 | 20 | 1.187 | 0.67 | 0.000 | 0% | 33.2 | **nan%** | nan |
| char_ar_s0 | ecoli | char | ar | r=0 | 20 | 3.244 | 0.25 | 0.000 | 0% | 36.0 | **nan%** | nan |
| char_ar_s1 | ecoli | char | ar | r=16 | 20 | 0.926 | 0.76 | 0.000 | 0% | 30.3 | **nan%** | nan |
| char_ar_s1 | ecoli | char | ar | r=4 | 20 | 1.070 | 0.70 | 0.003 | 0% | 31.9 | **nan%** | nan |
| char_ar_s1 | ecoli | char | ar | r=1 | 20 | 1.124 | 0.70 | 0.000 | 0% | 33.2 | **nan%** | nan |
| char_ar_s1 | ecoli | char | ar | r=0 | 20 | 3.388 | 0.25 | 0.000 | 0% | 35.9 | **nan%** | nan |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=16 | 20 | 2.040 | 0.22 | 0.000 | 0% | 36.3 | **0%** | 35.9 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=4 | 20 | 2.038 | 0.23 | 0.000 | 0% | 36.5 | **0%** | 36.8 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=1 | 20 | 2.026 | 0.26 | 0.000 | 0% | 35.9 | **0%** | 35.2 |
| char_mlm0.15_s0 | ecoli | char | mlm@0.15 | r=0 | 20 | 2.022 | 0.27 | 0.000 | 0% | 35.6 | **0%** | 35.9 |

Members: target surprise 0.876 b/nt against 3.168 for the matched non-member control; ICM extraction at worst nan%.
