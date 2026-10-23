# Memorisation of natural duplicates — human_big

No canary is planted here. Blocks of 96\,nt that the training corpus repeats by itself are found by hashing every block at a fixed stride, scored in one of their own host windows with the paper's three rulers, and compared against single-occurrence blocks from the same corpus. Rows carrying a planted canary are excluded, so the two populations never mix.

## Corpus census (distinct 96-nt blocks by occurrence count)

| dataset | 1 (control) | 2 | 3-4 | 5-8 | 9+ |
|---|---|---|---|---|---|
| human | 1006401 | 2235 | 1245 | 717 | 68 |

## Scores

| dataset | tokeniser | objective | seed | occurrences | n | bits/nt | rank-1 | verbatim |
|---|---|---|---|---|---|---|---|---|
| human | 3mer | ar | 0 | 1 (control) | 40 | 0.591 | 65% | 20% |
| human | 3mer | ar | 0 | 2 | 40 | 0.084 | 100% | 85% |
| human | 3mer | ar | 0 | 3-4 | 40 | 0.027 | 100% | 92% |
| human | 3mer | ar | 0 | 5-8 | 40 | 0.020 | 100% | 100% |
| human | 3mer | ar | 0 | 9+ | 40 | 0.018 | 100% | 100% |
| human | 4mer | ar | 0 | 1 (control) | 40 | 0.499 | 68% | 15% |
| human | 4mer | ar | 0 | 2 | 40 | 0.045 | 100% | 90% |
| human | 4mer | ar | 0 | 3-4 | 40 | 0.034 | 100% | 95% |
| human | 4mer | ar | 0 | 5-8 | 40 | 0.009 | 100% | 100% |
| human | 4mer | ar | 0 | 9+ | 40 | 0.015 | 100% | 100% |
| human | 6mer | ar | 0 | 1 (control) | 40 | 0.353 | 75% | 38% |
| human | 6mer | ar | 0 | 2 | 40 | 0.024 | 100% | 98% |
| human | 6mer | ar | 0 | 3-4 | 40 | 0.023 | 100% | 100% |
| human | 6mer | ar | 0 | 5-8 | 40 | 0.021 | 100% | 100% |
| human | 6mer | ar | 0 | 9+ | 40 | 0.020 | 100% | 100% |
| human | char | ar | 0 | 1 (control) | 40 | 1.158 | 20% | 0% |
| human | char | ar | 0 | 2 | 40 | 0.153 | 92% | 68% |
| human | char | ar | 0 | 3-4 | 40 | 0.027 | 100% | 90% |
| human | char | ar | 0 | 5-8 | 40 | 0.046 | 95% | 95% |
| human | char | ar | 0 | 9+ | 40 | 0.021 | 100% | 100% |
