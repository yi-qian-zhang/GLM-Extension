# Reconstruction audit — recon_audit

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | human | 6mer | ar | r=16 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | human | 6mer | ar | r=4 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | human | 6mer | ar | r=1 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s0 | human | 6mer | ar | r=0 | 25 | 3.554 | 0.03 | 0.000 | 0% | 34.6 | **nan%** | nan |
| 6mer_ar_s1 | human | 6mer | ar | r=16 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | human | 6mer | ar | r=4 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | human | 6mer | ar | r=1 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| 6mer_ar_s1 | human | 6mer | ar | r=0 | 25 | 3.447 | 0.02 | 0.000 | 0% | 34.4 | **nan%** | nan |
| char_ar_s0 | human | char | ar | r=16 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| char_ar_s0 | human | char | ar | r=4 | 25 | 0.001 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| char_ar_s0 | human | char | ar | r=1 | 25 | 0.001 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| char_ar_s0 | human | char | ar | r=0 | 25 | 11.342 | 0.34 | 0.000 | 0% | 32.6 | **nan%** | nan |
| char_ar_s1 | human | char | ar | r=16 | 25 | 0.000 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| char_ar_s1 | human | char | ar | r=4 | 25 | 0.001 | 1.00 | 1.000 | 100% | 0.0 | **nan%** | nan |
| char_ar_s1 | human | char | ar | r=1 | 25 | 0.004 | 1.00 | 0.975 | 96% | 0.1 | **nan%** | nan |
| char_ar_s1 | human | char | ar | r=0 | 25 | 11.161 | 0.36 | 0.000 | 0% | 32.5 | **nan%** | nan |

Members: target surprise 0.001 b/nt against 7.376 for the matched non-member control; ICM extraction at worst nan%.
