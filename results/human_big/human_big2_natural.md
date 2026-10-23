# Memorisation of natural duplicates — human_big2

No canary is planted here. Blocks of 96\,nt that the training corpus repeats by itself are found by hashing every block at a fixed stride, scored in one of their own host windows with the paper's three rulers, and compared against single-occurrence blocks from the same corpus. Rows carrying a planted canary are excluded, so the two populations never mix.

## Corpus census (distinct 96-nt blocks by occurrence count)

| dataset | 1 (control) | 2 | 3-4 | 5-8 | 9+ |
|---|---|---|---|---|---|
| human | 1006401 | 2235 | 1245 | 717 | 68 |

## Scores

| dataset | tokeniser | population | seed | occurrences | n | bits/nt | rank-1 | verbatim |
|---|---|---|---|---|---|---|---|---|
| human | 3mer | trained | 0 | 1 (control) | 30 | 0.616 | 60% | 23% |
| human | 3mer | trained | 0 | 2 | 30 | 0.064 | 100% | 87% |
| human | 3mer | trained | 0 | 3-4 | 30 | 0.025 | 100% | 97% |
| human | 3mer | trained | 0 | 5-8 | 30 | 0.018 | 100% | 100% |
| human | 3mer | trained | 0 | 9+ | 30 | 0.020 | 100% | 100% |
| human | 3mer | held-out | 0 | 1 (control) | 30 | 2.659 | 13% | 0% |
| human | 3mer | held-out | 0 | 2 | 30 | 0.871 | 73% | 10% |
| human | 3mer | held-out | 0 | 3-4 | 30 | 0.191 | 87% | 27% |
| human | 3mer | held-out | 0 | 5-8 | 30 | 0.118 | 90% | 60% |
| human | 4mer | trained | 0 | 1 (control) | 30 | 0.512 | 70% | 23% |
| human | 4mer | trained | 0 | 2 | 30 | 0.034 | 100% | 87% |
| human | 4mer | trained | 0 | 3-4 | 30 | 0.026 | 100% | 100% |
| human | 4mer | trained | 0 | 5-8 | 30 | 0.024 | 100% | 97% |
| human | 4mer | trained | 0 | 9+ | 30 | 0.012 | 100% | 100% |
| human | 4mer | held-out | 0 | 1 (control) | 30 | 2.688 | 10% | 3% |
| human | 4mer | held-out | 0 | 2 | 30 | 1.014 | 63% | 10% |
| human | 4mer | held-out | 0 | 3-4 | 30 | 0.217 | 93% | 27% |
| human | 4mer | held-out | 0 | 5-8 | 30 | 0.183 | 90% | 57% |
| human | 6mer | trained | 0 | 1 (control) | 30 | 0.356 | 87% | 30% |
| human | 6mer | trained | 0 | 2 | 30 | 0.066 | 93% | 93% |
| human | 6mer | trained | 0 | 3-4 | 30 | 0.027 | 100% | 100% |
| human | 6mer | trained | 0 | 5-8 | 30 | 0.020 | 97% | 100% |
| human | 6mer | trained | 0 | 9+ | 30 | 0.020 | 100% | 100% |
| human | 6mer | held-out | 0 | 1 (control) | 30 | 2.956 | 3% | 0% |
| human | 6mer | held-out | 0 | 2 | 30 | 1.096 | 53% | 23% |
| human | 6mer | held-out | 0 | 3-4 | 30 | 0.284 | 90% | 23% |
| human | 6mer | held-out | 0 | 5-8 | 30 | 0.133 | 90% | 43% |
| human | char | trained | 0 | 1 (control) | 30 | 1.158 | 20% | 3% |
| human | char | trained | 0 | 2 | 30 | 0.111 | 93% | 63% |
| human | char | trained | 0 | 3-4 | 30 | 0.132 | 90% | 83% |
| human | char | trained | 0 | 5-8 | 30 | 0.027 | 100% | 97% |
| human | char | trained | 0 | 9+ | 30 | 0.021 | 100% | 100% |
| human | char | held-out | 0 | 1 (control) | 30 | 2.227 | 3% | 0% |
| human | char | held-out | 0 | 2 | 30 | 0.811 | 63% | 23% |
| human | char | held-out | 0 | 3-4 | 30 | 0.075 | 93% | 50% |
| human | char | held-out | 0 | 5-8 | 30 | 0.092 | 93% | 73% |
