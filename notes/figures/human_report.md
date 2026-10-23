# Rare-allele recovery on real human canaries — human

Canaries: 400 haplotype segments of 96 nt from 1000 Genomes phase 3 (2,548 samples), chr22 (GRCh38), variants with AF <= 0.001 and <= 5 carriers.

`alt` = the individual's rare allele was produced, `ref` = the reference base was produced (the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.

| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |
|---|---|---|---|---|---|---|---|---|
| bpe4096_human_ar | 1 | r=0 | 104 | 0.346 | 0.144 | 0.510 | 2.035 | 0.000 |
| bpe4096_human_ar | 1 | r=1 | 81 | 0.346 | 0.160 | 0.494 | 2.026 | 0.000 |
| bpe4096_human_ar | 1 | r=4 | 83 | 0.386 | 0.108 | 0.506 | 1.990 | 0.000 |
| bpe4096_human_ar | 1 | r=16 | 97 | 0.340 | 0.134 | 0.526 | 1.994 | 0.000 |
| bpe4096_human_ar | 2 | r=0 | 105 | 0.286 | 0.210 | 0.505 | 2.000 | 0.000 |
| bpe4096_human_ar | 2 | r=1 | 81 | 0.272 | 0.259 | 0.469 | 1.961 | 0.000 |
| bpe4096_human_ar | 2 | r=4 | 83 | 0.289 | 0.205 | 0.506 | 1.887 | 0.000 |
| bpe4096_human_ar | 2 | r=16 | 97 | 0.268 | 0.165 | 0.567 | 1.838 | 0.000 |
| bpe4096_human_ar | 3 | r=0 | 105 | 0.219 | 0.295 | 0.486 | 1.970 | 0.000 |
| bpe4096_human_ar | 3 | r=1 | 81 | 0.309 | 0.309 | 0.383 | 1.855 | 0.000 |
| bpe4096_human_ar | 3 | r=4 | 83 | 0.265 | 0.229 | 0.506 | 1.723 | 0.000 |
| bpe4096_human_ar | 3 | r=16 | 97 | 0.320 | 0.237 | 0.443 | 1.513 | 0.000 |
| bpe4096_human_ar | 5 | r=0 | 105 | 0.276 | 0.343 | 0.381 | 1.961 | 0.000 |
| bpe4096_human_ar | 5 | r=1 | 81 | 0.296 | 0.284 | 0.420 | 1.645 | 0.000 |
| bpe4096_human_ar | 5 | r=4 | 83 | 0.398 | 0.241 | 0.361 | 1.393 | 0.000 |
| bpe4096_human_ar | 5 | r=16 | 97 | 0.629 | 0.206 | 0.165 | 0.848 | 0.120 |
| bpe4096_human_ar | 8 | r=0 | 105 | 0.276 | 0.333 | 0.390 | 2.057 | 0.000 |
| bpe4096_human_ar | 8 | r=1 | 81 | 0.259 | 0.395 | 0.346 | 1.174 | 0.000 |
| bpe4096_human_ar | 8 | r=4 | 83 | 0.458 | 0.205 | 0.337 | 0.856 | 0.000 |
| bpe4096_human_ar | 8 | r=16 | 97 | 0.907 | 0.000 | 0.093 | 0.341 | 0.560 |
| bpe4096_human_ar | 12 | r=0 | 105 | 0.238 | 0.295 | 0.467 | 2.308 | 0.000 |
| bpe4096_human_ar | 12 | r=1 | 81 | 0.580 | 0.148 | 0.272 | 0.556 | 0.020 |
| bpe4096_human_ar | 12 | r=4 | 83 | 0.675 | 0.108 | 0.217 | 0.376 | 0.200 |
| bpe4096_human_ar | 12 | r=16 | 97 | 0.979 | 0.010 | 0.010 | 0.137 | 0.800 |
| bpe4096_human_ar | 20 | r=0 | 105 | 0.314 | 0.314 | 0.371 | 2.632 | 0.000 |
| bpe4096_human_ar | 20 | r=1 | 81 | 0.988 | 0.000 | 0.012 | 0.057 | 0.980 |
| bpe4096_human_ar | 20 | r=4 | 83 | 1.000 | 0.000 | 0.000 | 0.040 | 1.000 |
| bpe4096_human_ar | 20 | r=16 | 97 | 1.000 | 0.000 | 0.000 | 0.019 | 1.000 |
| bpe4096_human_ar | 30 | r=0 | 210 | 0.314 | 0.276 | 0.410 | 2.784 | 0.000 |
| bpe4096_human_ar | 30 | r=1 | 162 | 1.000 | 0.000 | 0.000 | 0.009 | 1.000 |
| bpe4096_human_ar | 30 | r=4 | 166 | 1.000 | 0.000 | 0.000 | 0.010 | 1.000 |
| bpe4096_human_ar | 30 | r=16 | 194 | 1.000 | 0.000 | 0.000 | 0.007 | 1.000 |
| dnabert2bpe_causal_human | 0 | r=0 | 21 | 0.476 | 0.238 | 0.286 | 2.489 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=1 | 21 | 0.190 | 0.429 | 0.381 | 2.548 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=4 | 17 | 0.294 | 0.235 | 0.471 | 2.505 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=16 | 13 | 0.385 | 0.385 | 0.231 | 2.525 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=0 | 21 | 0.286 | 0.381 | 0.333 | 1.838 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=1 | 21 | 0.238 | 0.238 | 0.524 | 1.934 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=4 | 17 | 0.059 | 0.588 | 0.353 | 1.926 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=16 | 13 | 0.077 | 0.308 | 0.615 | 1.816 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=0 | 21 | 0.238 | 0.524 | 0.238 | 1.634 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=1 | 21 | 0.238 | 0.286 | 0.476 | 1.929 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=4 | 17 | 0.353 | 0.294 | 0.353 | 1.877 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=16 | 13 | 0.308 | 0.538 | 0.154 | 1.525 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=0 | 21 | 0.238 | 0.190 | 0.571 | 1.580 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=1 | 21 | 0.190 | 0.381 | 0.429 | 1.854 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=4 | 17 | 0.294 | 0.294 | 0.412 | 1.581 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=16 | 13 | 0.538 | 0.154 | 0.308 | 0.839 | 0.300 |
| dnabert2bpe_causal_human | 15 | r=0 | 21 | 0.238 | 0.333 | 0.429 | 1.617 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=1 | 21 | 0.238 | 0.286 | 0.476 | 1.739 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=4 | 17 | 0.294 | 0.294 | 0.412 | 1.299 | 0.100 |
| dnabert2bpe_causal_human | 15 | r=16 | 13 | 1.000 | 0.000 | 0.000 | 0.293 | 0.900 |
| dnabert2bpe_causal_human | 30 | r=0 | 21 | 0.238 | 0.333 | 0.429 | 1.812 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=1 | 21 | 0.571 | 0.333 | 0.095 | 1.148 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=4 | 17 | 0.882 | 0.000 | 0.118 | 0.466 | 0.400 |
| dnabert2bpe_causal_human | 30 | r=16 | 13 | 1.000 | 0.000 | 0.000 | 0.094 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=0 | 67 | 0.313 | 0.358 | 0.328 | 2.261 | 0.000 |
| dnabert2bpe_causal_human | 50 | r=1 | 38 | 0.816 | 0.053 | 0.132 | 0.194 | 0.550 |
| dnabert2bpe_causal_human | 50 | r=4 | 30 | 1.000 | 0.000 | 0.000 | 0.059 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=16 | 30 | 1.000 | 0.000 | 0.000 | 0.037 | 1.000 |
| dnabert3_causal_human | 0 | r=0 | 21 | 0.190 | 0.238 | 0.571 | 2.892 | 0.000 |
| dnabert3_causal_human | 0 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 2.590 | 0.000 |
| dnabert3_causal_human | 0 | r=4 | 17 | 0.176 | 0.353 | 0.471 | 2.916 | 0.000 |
| dnabert3_causal_human | 0 | r=16 | 13 | 0.308 | 0.308 | 0.385 | 2.721 | 0.000 |
| dnabert3_causal_human | 1 | r=0 | 21 | 0.381 | 0.095 | 0.524 | 1.941 | 0.000 |
| dnabert3_causal_human | 1 | r=1 | 21 | 0.381 | 0.143 | 0.476 | 1.965 | 0.000 |
| dnabert3_causal_human | 1 | r=4 | 17 | 0.294 | 0.176 | 0.529 | 1.974 | 0.000 |
| dnabert3_causal_human | 1 | r=16 | 13 | 0.308 | 0.231 | 0.462 | 1.986 | 0.000 |
| dnabert3_causal_human | 3 | r=0 | 21 | 0.333 | 0.190 | 0.476 | 1.871 | 0.000 |
| dnabert3_causal_human | 3 | r=1 | 21 | 0.190 | 0.238 | 0.571 | 1.919 | 0.000 |
| dnabert3_causal_human | 3 | r=4 | 17 | 0.118 | 0.294 | 0.588 | 1.939 | 0.000 |
| dnabert3_causal_human | 3 | r=16 | 13 | 0.231 | 0.077 | 0.692 | 1.922 | 0.000 |
| dnabert3_causal_human | 8 | r=0 | 21 | 0.286 | 0.429 | 0.286 | 1.630 | 0.000 |
| dnabert3_causal_human | 8 | r=1 | 21 | 0.286 | 0.143 | 0.571 | 1.984 | 0.000 |
| dnabert3_causal_human | 8 | r=4 | 17 | 0.118 | 0.353 | 0.529 | 1.876 | 0.000 |
| dnabert3_causal_human | 8 | r=16 | 13 | 0.385 | 0.462 | 0.154 | 1.652 | 0.000 |
| dnabert3_causal_human | 15 | r=0 | 21 | 0.381 | 0.429 | 0.190 | 1.625 | 0.000 |
| dnabert3_causal_human | 15 | r=1 | 21 | 0.190 | 0.238 | 0.571 | 1.960 | 0.000 |
| dnabert3_causal_human | 15 | r=4 | 17 | 0.176 | 0.471 | 0.353 | 1.791 | 0.000 |
| dnabert3_causal_human | 15 | r=16 | 13 | 0.385 | 0.385 | 0.231 | 1.385 | 0.000 |
| dnabert3_causal_human | 30 | r=0 | 21 | 0.333 | 0.476 | 0.190 | 1.676 | 0.000 |
| dnabert3_causal_human | 30 | r=1 | 21 | 0.381 | 0.238 | 0.381 | 1.907 | 0.000 |
| dnabert3_causal_human | 30 | r=4 | 17 | 0.118 | 0.353 | 0.529 | 1.631 | 0.000 |
| dnabert3_causal_human | 30 | r=16 | 13 | 0.769 | 0.077 | 0.154 | 0.767 | 0.300 |
| dnabert3_causal_human | 50 | r=0 | 67 | 0.209 | 0.418 | 0.373 | 1.747 | 0.000 |
| dnabert3_causal_human | 50 | r=1 | 38 | 0.368 | 0.316 | 0.316 | 1.535 | 0.000 |
| dnabert3_causal_human | 50 | r=4 | 30 | 0.433 | 0.167 | 0.400 | 1.272 | 0.100 |
| dnabert3_causal_human | 50 | r=16 | 29 | 0.966 | 0.000 | 0.034 | 0.379 | 0.800 |
| dnabert4_causal_human | 0 | r=0 | 21 | 0.286 | 0.143 | 0.571 | 2.579 | 0.000 |
| dnabert4_causal_human | 0 | r=1 | 21 | 0.238 | 0.095 | 0.667 | 2.602 | 0.000 |
| dnabert4_causal_human | 0 | r=4 | 17 | 0.176 | 0.235 | 0.588 | 2.330 | 0.000 |
| dnabert4_causal_human | 0 | r=16 | 13 | 0.308 | 0.154 | 0.538 | 2.571 | 0.000 |
| dnabert4_causal_human | 1 | r=0 | 21 | 0.381 | 0.000 | 0.619 | 1.998 | 0.000 |
| dnabert4_causal_human | 1 | r=1 | 21 | 0.333 | 0.095 | 0.571 | 1.972 | 0.000 |
| dnabert4_causal_human | 1 | r=4 | 17 | 0.118 | 0.118 | 0.765 | 2.007 | 0.000 |
| dnabert4_causal_human | 1 | r=16 | 13 | 0.462 | 0.154 | 0.385 | 1.965 | 0.000 |
| dnabert4_causal_human | 3 | r=0 | 21 | 0.238 | 0.238 | 0.524 | 1.853 | 0.000 |
| dnabert4_causal_human | 3 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.914 | 0.000 |
| dnabert4_causal_human | 3 | r=4 | 17 | 0.059 | 0.235 | 0.706 | 1.957 | 0.000 |
| dnabert4_causal_human | 3 | r=16 | 13 | 0.308 | 0.231 | 0.462 | 1.879 | 0.000 |
| dnabert4_causal_human | 8 | r=0 | 21 | 0.333 | 0.476 | 0.190 | 1.606 | 0.000 |
| dnabert4_causal_human | 8 | r=1 | 21 | 0.190 | 0.190 | 0.619 | 2.005 | 0.000 |
| dnabert4_causal_human | 8 | r=4 | 17 | 0.176 | 0.294 | 0.529 | 1.898 | 0.000 |
| dnabert4_causal_human | 8 | r=16 | 13 | 0.308 | 0.538 | 0.154 | 1.679 | 0.000 |
| dnabert4_causal_human | 15 | r=0 | 21 | 0.286 | 0.476 | 0.238 | 1.563 | 0.000 |
| dnabert4_causal_human | 15 | r=1 | 21 | 0.143 | 0.190 | 0.667 | 1.979 | 0.000 |
| dnabert4_causal_human | 15 | r=4 | 17 | 0.118 | 0.412 | 0.471 | 1.852 | 0.000 |
| dnabert4_causal_human | 15 | r=16 | 13 | 0.308 | 0.538 | 0.154 | 1.371 | 0.000 |
| dnabert4_causal_human | 30 | r=0 | 21 | 0.286 | 0.524 | 0.190 | 1.600 | 0.000 |
| dnabert4_causal_human | 30 | r=1 | 21 | 0.238 | 0.143 | 0.619 | 1.923 | 0.000 |
| dnabert4_causal_human | 30 | r=4 | 17 | 0.118 | 0.529 | 0.353 | 1.680 | 0.000 |
| dnabert4_causal_human | 30 | r=16 | 13 | 0.692 | 0.154 | 0.154 | 0.765 | 0.300 |
| dnabert4_causal_human | 50 | r=0 | 67 | 0.194 | 0.463 | 0.343 | 1.732 | 0.000 |
| dnabert4_causal_human | 50 | r=1 | 38 | 0.316 | 0.289 | 0.395 | 1.553 | 0.000 |
| dnabert4_causal_human | 50 | r=4 | 30 | 0.333 | 0.400 | 0.267 | 1.254 | 0.050 |
| dnabert4_causal_human | 50 | r=16 | 29 | 0.862 | 0.103 | 0.034 | 0.433 | 0.750 |
| dnabert5_causal_human | 0 | r=0 | 21 | 0.429 | 0.095 | 0.476 | 3.141 | 0.000 |
| dnabert5_causal_human | 0 | r=1 | 21 | 0.286 | 0.095 | 0.619 | 2.954 | 0.000 |
| dnabert5_causal_human | 0 | r=4 | 17 | 0.176 | 0.471 | 0.353 | 2.685 | 0.000 |
| dnabert5_causal_human | 0 | r=16 | 13 | 0.462 | 0.308 | 0.231 | 2.866 | 0.000 |
| dnabert5_causal_human | 1 | r=0 | 21 | 0.238 | 0.190 | 0.571 | 2.010 | 0.000 |
| dnabert5_causal_human | 1 | r=1 | 21 | 0.143 | 0.286 | 0.571 | 2.051 | 0.000 |
| dnabert5_causal_human | 1 | r=4 | 17 | 0.000 | 0.471 | 0.529 | 2.102 | 0.000 |
| dnabert5_causal_human | 1 | r=16 | 13 | 0.308 | 0.385 | 0.308 | 1.959 | 0.000 |
| dnabert5_causal_human | 3 | r=0 | 21 | 0.238 | 0.286 | 0.476 | 1.764 | 0.000 |
| dnabert5_causal_human | 3 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 1.938 | 0.000 |
| dnabert5_causal_human | 3 | r=4 | 17 | 0.000 | 0.353 | 0.647 | 1.960 | 0.000 |
| dnabert5_causal_human | 3 | r=16 | 13 | 0.308 | 0.385 | 0.308 | 1.753 | 0.000 |
| dnabert5_causal_human | 8 | r=0 | 21 | 0.286 | 0.381 | 0.333 | 1.651 | 0.000 |
| dnabert5_causal_human | 8 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.936 | 0.000 |
| dnabert5_causal_human | 8 | r=4 | 17 | 0.118 | 0.294 | 0.588 | 1.899 | 0.000 |
| dnabert5_causal_human | 8 | r=16 | 13 | 0.231 | 0.615 | 0.154 | 1.617 | 0.000 |
| dnabert5_causal_human | 15 | r=0 | 21 | 0.238 | 0.476 | 0.286 | 1.616 | 0.000 |
| dnabert5_causal_human | 15 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.949 | 0.000 |
| dnabert5_causal_human | 15 | r=4 | 17 | 0.059 | 0.294 | 0.647 | 1.832 | 0.000 |
| dnabert5_causal_human | 15 | r=16 | 13 | 0.462 | 0.385 | 0.154 | 1.350 | 0.000 |
| dnabert5_causal_human | 30 | r=0 | 21 | 0.238 | 0.524 | 0.238 | 1.611 | 0.000 |
| dnabert5_causal_human | 30 | r=1 | 21 | 0.238 | 0.143 | 0.619 | 1.910 | 0.000 |
| dnabert5_causal_human | 30 | r=4 | 17 | 0.176 | 0.412 | 0.412 | 1.692 | 0.000 |
| dnabert5_causal_human | 30 | r=16 | 13 | 0.538 | 0.231 | 0.231 | 0.848 | 0.200 |
| dnabert5_causal_human | 50 | r=0 | 67 | 0.179 | 0.373 | 0.448 | 1.764 | 0.000 |
| dnabert5_causal_human | 50 | r=1 | 38 | 0.421 | 0.237 | 0.342 | 1.602 | 0.000 |
| dnabert5_causal_human | 50 | r=4 | 30 | 0.433 | 0.267 | 0.300 | 1.262 | 0.100 |
| dnabert5_causal_human | 50 | r=16 | 29 | 0.793 | 0.069 | 0.138 | 0.485 | 0.650 |
| dnabert6_causal_human | 0 | r=0 | 21 | 0.143 | 0.238 | 0.619 | 4.900 | 0.000 |
| dnabert6_causal_human | 0 | r=1 | 21 | 0.429 | 0.143 | 0.429 | 4.226 | 0.000 |
| dnabert6_causal_human | 0 | r=4 | 17 | 0.059 | 0.294 | 0.647 | 4.211 | 0.000 |
| dnabert6_causal_human | 0 | r=16 | 13 | 0.154 | 0.154 | 0.692 | 4.362 | 0.000 |
| dnabert6_causal_human | 1 | r=0 | 21 | 0.381 | 0.190 | 0.429 | 1.946 | 0.000 |
| dnabert6_causal_human | 1 | r=1 | 21 | 0.333 | 0.238 | 0.429 | 2.073 | 0.000 |
| dnabert6_causal_human | 1 | r=4 | 17 | 0.176 | 0.235 | 0.588 | 1.998 | 0.000 |
| dnabert6_causal_human | 1 | r=16 | 13 | 0.231 | 0.231 | 0.538 | 1.902 | 0.000 |
| dnabert6_causal_human | 3 | r=0 | 21 | 0.333 | 0.381 | 0.286 | 1.660 | 0.000 |
| dnabert6_causal_human | 3 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.936 | 0.000 |
| dnabert6_causal_human | 3 | r=4 | 17 | 0.059 | 0.294 | 0.647 | 1.863 | 0.000 |
| dnabert6_causal_human | 3 | r=16 | 13 | 0.154 | 0.462 | 0.385 | 1.742 | 0.000 |
| dnabert6_causal_human | 8 | r=0 | 21 | 0.286 | 0.476 | 0.238 | 1.548 | 0.000 |
| dnabert6_causal_human | 8 | r=1 | 21 | 0.286 | 0.190 | 0.524 | 1.919 | 0.000 |
| dnabert6_causal_human | 8 | r=4 | 17 | 0.176 | 0.294 | 0.529 | 1.777 | 0.000 |
| dnabert6_causal_human | 8 | r=16 | 13 | 0.462 | 0.308 | 0.231 | 1.403 | 0.000 |
| dnabert6_causal_human | 15 | r=0 | 21 | 0.238 | 0.524 | 0.238 | 1.565 | 0.000 |
| dnabert6_causal_human | 15 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.913 | 0.000 |
| dnabert6_causal_human | 15 | r=4 | 17 | 0.118 | 0.118 | 0.765 | 1.738 | 0.000 |
| dnabert6_causal_human | 15 | r=16 | 13 | 0.769 | 0.077 | 0.154 | 1.110 | 0.300 |
| dnabert6_causal_human | 30 | r=0 | 21 | 0.286 | 0.524 | 0.190 | 1.669 | 0.000 |
| dnabert6_causal_human | 30 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.859 | 0.000 |
| dnabert6_causal_human | 30 | r=4 | 17 | 0.176 | 0.059 | 0.765 | 1.579 | 0.000 |
| dnabert6_causal_human | 30 | r=16 | 13 | 0.846 | 0.000 | 0.154 | 0.630 | 0.600 |
| dnabert6_causal_human | 50 | r=0 | 67 | 0.239 | 0.388 | 0.373 | 1.813 | 0.000 |
| dnabert6_causal_human | 50 | r=1 | 38 | 0.342 | 0.342 | 0.316 | 1.327 | 0.100 |
| dnabert6_causal_human | 50 | r=4 | 30 | 0.600 | 0.067 | 0.333 | 1.070 | 0.200 |
| dnabert6_causal_human | 50 | r=16 | 29 | 1.000 | 0.000 | 0.000 | 0.285 | 0.850 |
| hyena_medium-160k_human | 0 | r=0 | 36 | 0.222 | 0.444 | 0.333 | 1.679 | 0.000 |
| hyena_medium-160k_human | 0 | r=1 | 38 | 0.184 | 0.395 | 0.421 | 1.794 | 0.000 |
| hyena_medium-160k_human | 0 | r=4 | 30 | 0.167 | 0.333 | 0.500 | 1.763 | 0.000 |
| hyena_medium-160k_human | 0 | r=16 | 29 | 0.207 | 0.448 | 0.345 | 1.603 | 0.000 |
| hyena_medium-160k_human | 1 | r=0 | 36 | 0.278 | 0.417 | 0.306 | 1.662 | 0.000 |
| hyena_medium-160k_human | 1 | r=1 | 38 | 0.263 | 0.316 | 0.421 | 1.755 | 0.000 |
| hyena_medium-160k_human | 1 | r=4 | 30 | 0.167 | 0.300 | 0.533 | 1.715 | 0.000 |
| hyena_medium-160k_human | 1 | r=16 | 29 | 0.207 | 0.483 | 0.310 | 1.524 | 0.000 |
| hyena_medium-160k_human | 3 | r=0 | 36 | 0.306 | 0.361 | 0.333 | 1.631 | 0.000 |
| hyena_medium-160k_human | 3 | r=1 | 38 | 0.316 | 0.316 | 0.368 | 1.706 | 0.000 |
| hyena_medium-160k_human | 3 | r=4 | 30 | 0.167 | 0.333 | 0.500 | 1.623 | 0.000 |
| hyena_medium-160k_human | 3 | r=16 | 29 | 0.276 | 0.414 | 0.310 | 1.361 | 0.000 |
| hyena_medium-160k_human | 8 | r=0 | 36 | 0.361 | 0.361 | 0.278 | 1.648 | 0.000 |
| hyena_medium-160k_human | 8 | r=1 | 38 | 0.289 | 0.263 | 0.447 | 1.640 | 0.000 |
| hyena_medium-160k_human | 8 | r=4 | 30 | 0.400 | 0.267 | 0.333 | 1.463 | 0.000 |
| hyena_medium-160k_human | 8 | r=16 | 29 | 0.759 | 0.207 | 0.034 | 0.527 | 0.250 |
| hyena_medium-160k_human | 15 | r=0 | 36 | 0.333 | 0.361 | 0.306 | 1.672 | 0.000 |
| hyena_medium-160k_human | 15 | r=1 | 38 | 0.316 | 0.316 | 0.368 | 1.494 | 0.000 |
| hyena_medium-160k_human | 15 | r=4 | 30 | 0.433 | 0.233 | 0.333 | 1.167 | 0.000 |
| hyena_medium-160k_human | 15 | r=16 | 29 | 1.000 | 0.000 | 0.000 | 0.293 | 0.800 |
| hyena_medium-160k_human | 30 | r=0 | 36 | 0.306 | 0.278 | 0.417 | 1.857 | 0.000 |
| hyena_medium-160k_human | 30 | r=1 | 38 | 0.421 | 0.211 | 0.368 | 1.214 | 0.050 |
| hyena_medium-160k_human | 30 | r=4 | 30 | 0.567 | 0.200 | 0.233 | 0.661 | 0.150 |
| hyena_medium-160k_human | 30 | r=16 | 29 | 1.000 | 0.000 | 0.000 | 0.205 | 0.850 |
| hyena_medium-160k_human | 50 | r=0 | 67 | 0.269 | 0.299 | 0.433 | 2.397 | 0.000 |
| hyena_medium-160k_human | 50 | r=1 | 38 | 0.553 | 0.211 | 0.237 | 0.881 | 0.050 |
| hyena_medium-160k_human | 50 | r=4 | 30 | 0.767 | 0.133 | 0.100 | 0.373 | 0.100 |
| hyena_medium-160k_human | 50 | r=16 | 29 | 1.000 | 0.000 | 0.000 | 0.145 | 0.750 |

## Leakage: member minus non-member rare-allele recovery

| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |
|---|---|---|---|---|---|
| bpe4096_human_ar | 1 | 0.340 | 0.346 | 0.346 | -0.006 |
| bpe4096_human_ar | 2 | 0.268 | 0.272 | 0.286 | -0.018 |
| bpe4096_human_ar | 3 | 0.320 | 0.309 | 0.219 | +0.101 |
| bpe4096_human_ar | 5 | 0.629 | 0.296 | 0.276 | +0.353 |
| bpe4096_human_ar | 8 | 0.907 | 0.259 | 0.276 | +0.631 |
| bpe4096_human_ar | 12 | 0.979 | 0.580 | 0.238 | +0.741 |
| bpe4096_human_ar | 20 | 1.000 | 0.988 | 0.314 | +0.686 |
| bpe4096_human_ar | 30 | 1.000 | 1.000 | 0.314 | +0.686 |
| dnabert2bpe_causal_human | 0 | 0.385 | 0.190 | 0.476 | -0.092 |
| dnabert2bpe_causal_human | 1 | 0.077 | 0.238 | 0.286 | -0.209 |
| dnabert2bpe_causal_human | 3 | 0.308 | 0.238 | 0.238 | +0.070 |
| dnabert2bpe_causal_human | 8 | 0.538 | 0.190 | 0.238 | +0.300 |
| dnabert2bpe_causal_human | 15 | 1.000 | 0.238 | 0.238 | +0.762 |
| dnabert2bpe_causal_human | 30 | 1.000 | 0.571 | 0.238 | +0.762 |
| dnabert2bpe_causal_human | 50 | 1.000 | 0.816 | 0.313 | +0.687 |
| dnabert3_causal_human | 0 | 0.308 | 0.333 | 0.190 | +0.117 |
| dnabert3_causal_human | 1 | 0.308 | 0.381 | 0.381 | -0.073 |
| dnabert3_causal_human | 3 | 0.231 | 0.190 | 0.333 | -0.103 |
| dnabert3_causal_human | 8 | 0.385 | 0.286 | 0.286 | +0.099 |
| dnabert3_causal_human | 15 | 0.385 | 0.190 | 0.381 | +0.004 |
| dnabert3_causal_human | 30 | 0.769 | 0.381 | 0.333 | +0.436 |
| dnabert3_causal_human | 50 | 0.966 | 0.368 | 0.209 | +0.757 |
| dnabert4_causal_human | 0 | 0.308 | 0.238 | 0.286 | +0.022 |
| dnabert4_causal_human | 1 | 0.462 | 0.333 | 0.381 | +0.081 |
| dnabert4_causal_human | 3 | 0.308 | 0.238 | 0.238 | +0.070 |
| dnabert4_causal_human | 8 | 0.308 | 0.190 | 0.333 | -0.026 |
| dnabert4_causal_human | 15 | 0.308 | 0.143 | 0.286 | +0.022 |
| dnabert4_causal_human | 30 | 0.692 | 0.238 | 0.286 | +0.407 |
| dnabert4_causal_human | 50 | 0.862 | 0.316 | 0.194 | +0.668 |
| dnabert5_causal_human | 0 | 0.462 | 0.286 | 0.429 | +0.033 |
| dnabert5_causal_human | 1 | 0.308 | 0.143 | 0.238 | +0.070 |
| dnabert5_causal_human | 3 | 0.308 | 0.333 | 0.238 | +0.070 |
| dnabert5_causal_human | 8 | 0.231 | 0.238 | 0.286 | -0.055 |
| dnabert5_causal_human | 15 | 0.462 | 0.238 | 0.238 | +0.223 |
| dnabert5_causal_human | 30 | 0.538 | 0.238 | 0.238 | +0.300 |
| dnabert5_causal_human | 50 | 0.793 | 0.421 | 0.179 | +0.614 |
| dnabert6_causal_human | 0 | 0.154 | 0.429 | 0.143 | +0.011 |
| dnabert6_causal_human | 1 | 0.231 | 0.333 | 0.381 | -0.150 |
| dnabert6_causal_human | 3 | 0.154 | 0.238 | 0.333 | -0.179 |
| dnabert6_causal_human | 8 | 0.462 | 0.286 | 0.286 | +0.176 |
| dnabert6_causal_human | 15 | 0.769 | 0.238 | 0.238 | +0.531 |
| dnabert6_causal_human | 30 | 0.846 | 0.238 | 0.286 | +0.560 |
| dnabert6_causal_human | 50 | 1.000 | 0.342 | 0.239 | +0.761 |
| hyena_medium-160k_human | 0 | 0.207 | 0.184 | 0.222 | -0.015 |
| hyena_medium-160k_human | 1 | 0.207 | 0.263 | 0.278 | -0.071 |
| hyena_medium-160k_human | 3 | 0.276 | 0.316 | 0.306 | -0.030 |
| hyena_medium-160k_human | 8 | 0.759 | 0.289 | 0.361 | +0.398 |
| hyena_medium-160k_human | 15 | 1.000 | 0.316 | 0.333 | +0.667 |
| hyena_medium-160k_human | 30 | 1.000 | 0.421 | 0.306 | +0.694 |
| hyena_medium-160k_human | 50 | 1.000 | 0.553 | 0.269 | +0.731 |
