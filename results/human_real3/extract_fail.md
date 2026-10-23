# Where greedy extraction fails — tier r=16, round 50

`exact` is the headline all-or-nothing rate. `wrong nt` counts only the failures, so it says how close a failure was. `at variant` is how many of those wrong letters sit on a rare-variant position, and `-> reference` how many of those produced the reference base instead of the carrier's allele.

| model | n | exact | mean wrong nt (failures) | median wrong nt | first wrong position | wrong at variant | of which -> reference |
|---|---|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 150 | 1.00 | — | — | — | — | — |
| dnabert3_causal_human | 150 | 0.97 | 17.00 | 20.00 | 13.25 | 0.25 | 0.00 |
| dnabert4_causal_human | 150 | 0.86 | 16.38 | 15.00 | 23.00 | 0.24 | 0.40 |
| dnabert5_causal_human | 150 | 0.67 | 24.84 | 29.00 | 12.37 | 0.61 | 0.40 |
| dnabert6_causal_human | 150 | 0.85 | 21.65 | 25.00 | 17.35 | 0.52 | 0.67 |
| hyena_medium-160k_human | 150 | 0.82 | 10.11 | 5.00 | 23.07 | 0.78 | 0.76 |
