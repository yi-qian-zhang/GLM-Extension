# Re-masking in nucleotide space on DNABERT-2's BPE vocabulary — recon_bpe_final

BPE tokens have no fixed length or boundaries, so changing one nucleotide re-segments the window and there is no persistent token grid to iterate over. The latent variable is the nucleotide string: for each candidate letter the window is re-tokenised, every token whose span covers that position is masked, and the score is the summed log-probability of those tokens divided by the nucleotides they cover -- per nucleotide, because candidates re-segment differently and raw BPE log-probabilities carry a length bias.

| run | data | seed | tier | n | LOO top1 | LOO b/nt | LOO bound | ICM-bpe exact | ham | any-restart |
|---|---|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=16 | 20 | 1.00 | 0.001 | 0.936 | **0%** | 35.1 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=4 | 20 | 1.00 | 0.004 | 0.873 | **0%** | 35.6 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=1 | 20 | 0.91 | 0.315 | 0.260 | **0%** | 35.4 | 0% |
| dnabert2bpe_ecoli_s0 | ecoli | 0 | r=0 | 20 | 0.30 | 2.482 | 0.000 | **0%** | 36.5 | 0% |
