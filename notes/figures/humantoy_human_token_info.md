# Per-token accounting of the canary — human

A 96-nt canary is 192 bits for every tokenizer; what changes is how many token slots carry them.

| tokenizer | nt/token | slots per canary | vocab | bits/slot at chance | canary-token corpus count | unseen in corpus |
|---|---|---|---|---|---|---|
| char | 1.00 | 96.0 | 7 | 2.0 | 287916 | 0.00 |
| 3mer | 3.00 | 32.0 | 67 | 6.0 | 6026 | 0.00 |
| 6mer | 6.00 | 16.0 | 4099 | 12.0 | 48 | 0.00 |

## Memorisation at matched held-out loss: per nucleotide vs per token slot

Per-nucleotide values separate the tokenizers (the result of the paper). If a model stores a roughly fixed amount per slot, the per-slot values are closer together, and the residual spread is the part the tokenizer explains beyond slot counting.

### r=1

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | — | — | — | — | — | bits/nt |
| char | — | — | — | — | — | bits/slot |
| 3mer | 0.939 | 1.081 | 1.127 | 1.201 | 1.348 | bits/nt |
| 3mer | 2.817 | 3.244 | 3.381 | 3.602 | 4.045 | bits/slot |
| 6mer | 1.450 | 1.497 | 1.615 | 1.850 | — | bits/nt |
| 6mer | 8.700 | 8.983 | 9.689 | 11.102 | — | bits/slot |

### r=16

| tokenizer | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 | unit |
|---|---|---|---|---|---|---|
| char | — | — | — | — | — | bits/nt |
| char | — | — | — | — | — | bits/slot |
| 3mer | 1.262 | 1.455 | 1.489 | 1.533 | 1.621 | bits/nt |
| 3mer | 3.785 | 4.364 | 4.467 | 4.599 | 4.863 | bits/slot |
| 6mer | 1.638 | 1.669 | 1.745 | 1.898 | — | bits/nt |
| 6mer | 9.830 | 10.013 | 10.472 | 11.389 | — | bits/slot |

