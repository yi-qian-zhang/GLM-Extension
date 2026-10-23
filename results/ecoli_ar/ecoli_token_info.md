# Per-token accounting of the canary — ecoli

A 96-nt canary is 192 bits for every tokenizer; what changes is how many token slots carry them.

| tokenizer | nt/token | slots per canary | vocab | bits/slot at chance | canary-token corpus count | unseen in corpus |
|---|---|---|---|---|---|---|
| char | 1.00 | 96.0 | 7 | 2.0 | 287995 | 0.00 |
| 3mer | 3.00 | 32.0 | 67 | 6.0 | 6014 | 0.00 |
| 4mer | 4.00 | 24.0 | 259 | 8.0 | 1130 | 0.00 |
| bpe4096 | 4.61 | 20.8 | 4096 | 9.2 | 400 | 0.00 |
| 6mer | 6.00 | 16.0 | 4099 | 12.0 | 47 | 0.00 |

## Memorisation at matched held-out loss: per nucleotide vs per token slot

Per-nucleotide values separate the tokenizers (the result of the paper). If a model stores a roughly fixed amount per slot, the per-slot values are closer together, and the residual spread is the part the tokenizer explains beyond slot counting.

### r=1

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | 0.037 | 0.068 | 0.145 | — | — | bits/nt |
| char | 0.037 | 0.068 | 0.145 | — | — | bits/slot |
| 3mer | 0.264 | 0.308 | 0.420 | 0.643 | 0.910 | bits/nt |
| 3mer | 0.791 | 0.925 | 1.259 | 1.929 | 2.730 | bits/slot |
| 4mer | 0.255 | 0.358 | 0.505 | 0.798 | 1.208 | bits/nt |
| 4mer | 1.022 | 1.432 | 2.018 | 3.190 | 4.831 | bits/slot |
| bpe4096 | — | -0.128 | 0.257 | 0.633 | 1.200 | bits/nt |
| bpe4096 | — | -0.592 | 1.186 | 2.919 | 5.533 | bits/slot |
| 6mer | 0.625 | 0.718 | 0.951 | 1.325 | 1.891 | bits/nt |
| 6mer | 3.749 | 4.309 | 5.708 | 7.950 | 11.348 | bits/slot |

### r=16

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | 0.047 | 0.083 | 0.173 | — | — | bits/nt |
| char | 0.047 | 0.083 | 0.173 | — | — | bits/slot |
| 3mer | 0.367 | 0.417 | 0.542 | 0.793 | 1.053 | bits/nt |
| 3mer | 1.101 | 1.251 | 1.627 | 2.378 | 3.158 | bits/slot |
| 4mer | 0.360 | 0.498 | 0.651 | 0.956 | 1.349 | bits/nt |
| 4mer | 1.442 | 1.992 | 2.603 | 3.826 | 5.396 | bits/slot |
| bpe4096 | — | -0.075 | 1.051 | 1.519 | 1.789 | bits/nt |
| bpe4096 | — | -0.348 | 4.846 | 7.006 | 8.249 | bits/slot |
| 6mer | 0.854 | 0.950 | 1.189 | 1.525 | 1.915 | bits/nt |
| 6mer | 5.124 | 5.699 | 7.136 | 9.149 | 11.490 | bits/slot |

