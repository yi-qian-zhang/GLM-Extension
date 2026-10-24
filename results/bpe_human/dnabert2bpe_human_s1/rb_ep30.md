# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — rb_ep30

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_human_s1 | human | 1 | r=16 | 50 | 0.96 | 0.100 | 0.318 | **0%** | 34.2 | 0% |
| dnabert2bpe_human_s1 | human | 1 | r=1 | 50 | 0.61 | 1.147 | 0.002 | **0%** | 33.4 | 0% |
| dnabert2bpe_human_s1 | human | 1 | r=0 | 50 | 0.46 | 1.497 | 0.000 | **0%** | 34.6 | 0% |
