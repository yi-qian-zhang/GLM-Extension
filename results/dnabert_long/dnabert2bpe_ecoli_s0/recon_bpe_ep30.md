# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — recon_bpe_ep30

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=16 | 20 | 0.99 | 0.033 | 0.734 | **0%** | 35.9 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=4 | 20 | 0.73 | 1.177 | 0.023 | **0%** | 36.6 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=1 | 20 | 0.41 | 1.795 | 0.000 | **0%** | 36.4 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=0 | 20 | 0.27 | 2.007 | 0.000 | **0%** | 36.0 | 0% |
