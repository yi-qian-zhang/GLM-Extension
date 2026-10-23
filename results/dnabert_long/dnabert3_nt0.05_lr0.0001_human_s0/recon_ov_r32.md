# Nucleotide-level re-masking on DNABERT's overlapping k-mers — recon_ov_r32

One TOKEN at a time is undefined on a stride-1 vocabulary: changing a token contradicts the ones overlapping it and decodes to no DNA string, and a token's letters are anyway visible in its neighbours. So the latent variable is the nucleotide string and the conditional is DNABERT's own: to re-mask nucleotide j, mask the k tokens covering j, marginalise onto the letter at j and renormalise over ACGT. `loo top1` is the per-position accuracy with every other target nucleotide at its true value, so it says whether the record is stored; `icm-nt` is the attack, choosing between fixed points by pseudo-log-likelihood, and `oracle` is the upper bound over the same restarts.

Hiding 48 nucleotides takes 48+(k-1) tokens here, i.e. about 48 slots for EVERY k, so the joint-slot mechanism predicts a FLAT profile across k. A large spread would refute it.

| run | k | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-nt exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dnabert3_nt0.05_lr0.0001_human_s0 | 3 | human | 0 | r=16 | 20 | 1.00 | 0.013 | 0.968 | **10%** | 30.8 | 10% |
| dnabert3_nt0.05_lr0.0001_human_s0 | 3 | human | 0 | r=4 | 20 | 0.87 | 0.519 | 0.233 | **0%** | 32.3 | 0% |
| dnabert3_nt0.05_lr0.0001_human_s0 | 3 | human | 0 | r=1 | 20 | 0.66 | 1.185 | 0.026 | **0%** | 31.9 | 0% |
| dnabert3_nt0.05_lr0.0001_human_s0 | 3 | human | 0 | r=0 | 20 | 0.47 | 1.856 | 0.000 | **0%** | 34.5 | 0% |

Best member extraction by k: k=3 10% (spread 0 points).
