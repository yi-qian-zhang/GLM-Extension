# Reconstruction audit — recon_smoke

`target` is the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, in bits per target nucleotide: the conditional extraction has to invert, with the revealed half excluded. `top1` is the fraction of decoding steps whose argmax is the true token and `bound` = top1^steps is the implied ceiling on all-48-exact extraction, so a cell whose bound is ~0 cannot be rescued by any decoder. `icm` re-masks one target token at a time and sweeps to a fixed point, which is the in-distribution conditional the surprise and recognition rulers read and neither shipped protocol enters; `seed` is the confidence-ordered edge-conditioned decode it starts from.

| run | data | tok | obj | tier | n | target b/nt | top1 | bound | prefix exact | prefix ham | ICM exact | ICM ham |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=16 | 2 | 0.452 | 0.61 | 0.052 | 0% | 20.5 | **0%** | 21.0 |
| 6mer_mlm0.15_s0 | human | 6mer | mlm@0.15 | r=0 | 2 | 2.664 | 0.00 | 0.000 | 0% | 35.0 | **0%** | 37.0 |

Members: target surprise 0.452 b/nt against 2.664 for the matched non-member control; ICM extraction at worst 0%.
