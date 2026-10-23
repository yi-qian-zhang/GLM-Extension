# Per-token accounting of the canary — synthetic

A 96-nt canary is 192 bits for every tokenizer; what changes is how many token slots carry them.

| tokenizer | nt/token | slots per canary | vocab | bits/slot at chance | canary-token corpus count | unseen in corpus |
|---|---|---|---|---|---|---|
| char | 1.00 | 96.0 | 7 | 2.0 | 287997 | 0.00 |
| 3mer | 3.00 | 32.0 | 67 | 6.0 | 5998 | 0.00 |
| bpe4096 | 4.67 | 20.6 | 4096 | 9.3 | 441 | 0.00 |
| 6mer | 6.00 | 16.0 | 4099 | 12.0 | 47 | 0.00 |

## Memorisation at matched held-out loss: per nucleotide vs per token slot

Per-nucleotide values separate the tokenizers (the result of the paper). If a model stores a roughly fixed amount per slot, the per-slot values are closer together, and the residual spread is the part the tokenizer explains beyond slot counting.

### r=1

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | 0.038 | — | — | — | — | bits/nt |
| char | 0.038 | — | — | — | — | bits/slot |
| 3mer | 0.056 | 0.096 | 0.189 | 0.367 | 0.686 | bits/nt |
| 3mer | 0.169 | 0.288 | 0.568 | 1.101 | 2.059 | bits/slot |
| bpe4096 | — | — | -0.081 | 0.421 | 0.945 | bits/nt |
| bpe4096 | — | — | -0.379 | 1.966 | 4.414 | bits/slot |
| 6mer | 0.152 | 0.303 | 0.654 | 1.186 | 1.794 | bits/nt |
| 6mer | 0.911 | 1.820 | 3.923 | 7.115 | 10.764 | bits/slot |

### r=16

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | 0.038 | — | — | — | — | bits/nt |
| char | 0.038 | — | — | — | — | bits/slot |
| 3mer | 0.087 | 0.136 | 0.243 | 0.433 | 0.764 | bits/nt |
| 3mer | 0.262 | 0.408 | 0.728 | 1.298 | 2.292 | bits/slot |
| bpe4096 | — | — | -0.035 | 1.339 | 1.688 | bits/nt |
| bpe4096 | — | — | -0.162 | 6.255 | 7.883 | bits/slot |
| 6mer | 0.219 | 0.413 | 0.825 | 1.362 | 1.842 | bits/nt |
| 6mer | 1.312 | 2.477 | 4.948 | 8.170 | 11.052 | bits/slot |

