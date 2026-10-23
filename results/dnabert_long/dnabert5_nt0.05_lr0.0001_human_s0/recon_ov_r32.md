# Nucleotide-level re-masking on DNABERT's overlapping k-mers — recon_ov_r32

One TOKEN at a time is undefined on a stride-1 vocabulary: changing a token contradicts the ones overlapping it and decodes to no DNA string, and a token's letters are anyway visible in its neighbours. So the latent variable is the nucleotide string and the conditional is DNABERT's own: to re-mask nucleotide j, mask the k tokens covering j, marginalise onto the letter at j and renormalise over ACGT. `loo top1` is the per-position accuracy with every other target nucleotide at its true value, so it says whether the record is stored; `icm-nt` is the attack, choosing between fixed points by pseudo-log-likelihood, and `oracle` is the upper bound over the same restarts.

Hiding 48 nucleotides takes 48+(k-1) tokens here, i.e. about 48 slots for EVERY k, so the joint-slot mechanism predicts a FLAT profile across k. A large spread would refute it.

| run | k | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-nt exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dnabert5_nt0.05_lr0.0001_human_s0 | 5 | human | 0 | r=16 | 20 | 0.99 | 0.024 | 0.841 | **10%** | 29.1 | 10% |
| dnabert5_nt0.05_lr0.0001_human_s0 | 5 | human | 0 | r=4 | 20 | 0.80 | 0.742 | 0.071 | **0%** | 34.0 | 0% |
| dnabert5_nt0.05_lr0.0001_human_s0 | 5 | human | 0 | r=1 | 20 | 0.63 | 1.304 | 0.005 | **0%** | 33.0 | 0% |
| dnabert5_nt0.05_lr0.0001_human_s0 | 5 | human | 0 | r=0 | 20 | 0.48 | 1.736 | 0.000 | **0%** | 34.7 | 0% |

Best member extraction by k: k=5 10% (spread 0 points).
