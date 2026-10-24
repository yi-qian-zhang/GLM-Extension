# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — rb_ep120

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_human_s2 | human | 2 | r=16 | 50 | 0.99 | 0.004 | 0.801 | **0%** | 33.9 | 0% |
| dnabert2bpe_human_s2 | human | 2 | r=1 | 50 | 0.92 | 0.240 | 0.185 | **0%** | 33.8 | 0% |
| dnabert2bpe_human_s2 | human | 2 | r=0 | 50 | 0.41 | 1.844 | 0.000 | **0%** | 35.1 | 0% |
