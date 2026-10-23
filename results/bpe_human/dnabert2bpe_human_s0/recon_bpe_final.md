# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — recon_bpe_final

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_human_s0 | human | 0 | r=16 | 20 | 0.99 | 0.002 | 0.818 | **0%** | 35.1 | 0% |
| dnabert2bpe_human_s0 | human | 0 | r=4 | 20 | 0.99 | 0.011 | 0.724 | **0%** | 33.9 | 0% |
| dnabert2bpe_human_s0 | human | 0 | r=1 | 20 | 0.95 | 0.065 | 0.277 | **0%** | 33.0 | 0% |
| dnabert2bpe_human_s0 | human | 0 | r=0 | 20 | 0.39 | 2.091 | 0.000 | **0%** | 34.9 | 0% |
