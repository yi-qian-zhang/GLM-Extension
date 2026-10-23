# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — recon_bpe_ep15

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=16 | 20 | 0.84 | 0.765 | 0.079 | **0%** | 35.8 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=4 | 20 | 0.42 | 1.832 | 0.000 | **0%** | 36.6 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=1 | 20 | 0.33 | 1.943 | 0.000 | **0%** | 36.2 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=0 | 20 | 0.26 | 1.970 | 0.000 | **0%** | 36.4 | 0% |
