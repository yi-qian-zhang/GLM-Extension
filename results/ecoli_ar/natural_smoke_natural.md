# Memorisation of natural duplicates — natural_smoke

No canary is planted here. Blocks of 96\,nt that the training corpus repeats by itself are found by hashing every block at a fixed stride, scored in one of their own host windows with the paper's three rulers, and compared against single-occurrence blocks from the same corpus. Rows carrying a planted canary are excluded, so the two populations never mix.

## Corpus census (distinct 96-nt blocks by occurrence count)

| dataset | 1 (control) | 2 | 3-4 | 5-8 | 9+ |
|---|---|---|---|---|---|
| ecoli | 85000 | 0 | 0 | 0 | 0 |

## Scores

| dataset | tokeniser | objective | seed | occurrences | n | bits/nt | rank-1 | verbatim |
|---|---|---|---|---|---|---|---|---|
| ecoli | 3mer | ar | 0 | 1 (control) | 8 | 0.013 | 100% | 100% |
| ecoli | 3mer | ar | 1 | 1 (control) | 8 | 0.033 | 88% | 100% |
| ecoli | 4mer | ar | 0 | 1 (control) | 8 | 0.002 | 100% | 100% |
| ecoli | 4mer | ar | 1 | 1 (control) | 8 | 0.002 | 100% | 100% |
| ecoli | 6mer | ar | 0 | 1 (control) | 8 | 0.008 | 100% | 100% |
| ecoli | 6mer | ar | 1 | 1 (control) | 8 | 0.026 | 88% | 100% |
| ecoli | char | ar | 0 | 1 (control) | 8 | 1.584 | 88% | 0% |
| ecoli | char | ar | 1 | 1 (control) | 8 | 1.577 | 100% | 0% |
