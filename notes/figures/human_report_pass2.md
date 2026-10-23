# Rare-allele recovery on real human canaries — human2

Canaries: 400 haplotype segments of 96 nt from 1000 Genomes phase 3 (2,548 samples), chr22 (GRCh38), variants with AF <= 0.001 and <= 5 carriers.

`alt` = the individual's rare allele was produced, `ref` = the reference base was produced (the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.

| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |
|---|---|---|---|---|---|---|---|---|
| 6mer_ar | 1 | r=0 | 0 | — | — | — | 1.957 | 0.000 |
| 6mer_ar | 1 | r=1 | 0 | — | — | — | 1.955 | 0.000 |
| 6mer_ar | 1 | r=4 | 0 | — | — | — | 1.940 | 0.000 |
| 6mer_ar | 1 | r=16 | 0 | — | — | — | 1.935 | 0.000 |
| 6mer_ar | 2 | r=0 | 0 | — | — | — | 1.945 | 0.000 |
| 6mer_ar | 2 | r=1 | 0 | — | — | — | 1.920 | 0.000 |
| 6mer_ar | 2 | r=4 | 0 | — | — | — | 1.888 | 0.000 |
| 6mer_ar | 2 | r=16 | 0 | — | — | — | 1.893 | 0.000 |
| 6mer_ar | 3 | r=0 | 0 | — | — | — | 1.925 | 0.000 |
| 6mer_ar | 3 | r=1 | 0 | — | — | — | 1.825 | 0.000 |
| 6mer_ar | 3 | r=4 | 0 | — | — | — | 1.767 | 0.000 |
| 6mer_ar | 3 | r=16 | 0 | — | — | — | 1.743 | 0.000 |
| 6mer_ar | 5 | r=0 | 0 | — | — | — | 1.920 | 0.000 |
| 6mer_ar | 5 | r=1 | 0 | — | — | — | 1.605 | 0.000 |
| 6mer_ar | 5 | r=4 | 0 | — | — | — | 1.504 | 0.000 |
| 6mer_ar | 5 | r=16 | 0 | — | — | — | 1.416 | 0.000 |
| 6mer_ar | 8 | r=0 | 0 | — | — | — | 1.971 | 0.000 |
| 6mer_ar | 8 | r=1 | 0 | — | — | — | 1.167 | 0.000 |
| 6mer_ar | 8 | r=4 | 0 | — | — | — | 1.074 | 0.000 |
| 6mer_ar | 8 | r=16 | 0 | — | — | — | 0.908 | 0.040 |
| 6mer_ar | 12 | r=0 | 0 | — | — | — | 2.117 | 0.000 |
| 6mer_ar | 12 | r=1 | 0 | — | — | — | 0.570 | 0.100 |
| 6mer_ar | 12 | r=4 | 0 | — | — | — | 0.512 | 0.220 |
| 6mer_ar | 12 | r=16 | 0 | — | — | — | 0.377 | 0.460 |
| 6mer_ar | 20 | r=0 | 0 | — | — | — | 2.361 | 0.000 |
| 6mer_ar | 20 | r=1 | 0 | — | — | — | 0.034 | 1.000 |
| 6mer_ar | 20 | r=4 | 0 | — | — | — | 0.034 | 1.000 |
| 6mer_ar | 20 | r=16 | 0 | — | — | — | 0.027 | 1.000 |
| 6mer_ar | 30 | r=0 | 0 | — | — | — | 2.461 | 0.000 |
| 6mer_ar | 30 | r=1 | 0 | — | — | — | 0.008 | 1.000 |
| 6mer_ar | 30 | r=4 | 0 | — | — | — | 0.011 | 1.000 |
| 6mer_ar | 30 | r=16 | 0 | — | — | — | 0.009 | 1.000 |
| bpe4096_human_ar | 1 | r=0 | 105 | 0.257 | 0.171 | 0.571 | 2.037 | 0.000 |
| bpe4096_human_ar | 1 | r=1 | 81 | 0.296 | 0.296 | 0.407 | 2.026 | 0.000 |
| bpe4096_human_ar | 1 | r=4 | 83 | 0.313 | 0.145 | 0.542 | 1.990 | 0.000 |
| bpe4096_human_ar | 1 | r=16 | 97 | 0.258 | 0.216 | 0.526 | 1.992 | 0.000 |
| bpe4096_human_ar | 2 | r=0 | 105 | 0.276 | 0.257 | 0.467 | 1.997 | 0.000 |
| bpe4096_human_ar | 2 | r=1 | 81 | 0.284 | 0.259 | 0.457 | 1.949 | 0.000 |
| bpe4096_human_ar | 2 | r=4 | 83 | 0.253 | 0.193 | 0.554 | 1.873 | 0.000 |
| bpe4096_human_ar | 2 | r=16 | 97 | 0.206 | 0.330 | 0.464 | 1.829 | 0.000 |
| bpe4096_human_ar | 3 | r=0 | 105 | 0.238 | 0.267 | 0.495 | 1.969 | 0.000 |
| bpe4096_human_ar | 3 | r=1 | 81 | 0.185 | 0.222 | 0.593 | 1.843 | 0.000 |
| bpe4096_human_ar | 3 | r=4 | 83 | 0.301 | 0.253 | 0.446 | 1.711 | 0.000 |
| bpe4096_human_ar | 3 | r=16 | 97 | 0.299 | 0.258 | 0.443 | 1.489 | 0.000 |
| bpe4096_human_ar | 5 | r=0 | 105 | 0.295 | 0.267 | 0.438 | 1.964 | 0.000 |
| bpe4096_human_ar | 5 | r=1 | 81 | 0.284 | 0.259 | 0.457 | 1.626 | 0.000 |
| bpe4096_human_ar | 5 | r=4 | 83 | 0.373 | 0.277 | 0.349 | 1.363 | 0.000 |
| bpe4096_human_ar | 5 | r=16 | 97 | 0.722 | 0.134 | 0.144 | 0.814 | 0.100 |
| bpe4096_human_ar | 8 | r=0 | 105 | 0.248 | 0.257 | 0.495 | 2.070 | 0.000 |
| bpe4096_human_ar | 8 | r=1 | 81 | 0.494 | 0.235 | 0.272 | 1.150 | 0.000 |
| bpe4096_human_ar | 8 | r=4 | 83 | 0.494 | 0.193 | 0.313 | 0.824 | 0.000 |
| bpe4096_human_ar | 8 | r=16 | 97 | 0.969 | 0.031 | 0.000 | 0.321 | 0.620 |
| bpe4096_human_ar | 12 | r=0 | 105 | 0.257 | 0.267 | 0.476 | 2.321 | 0.000 |
| bpe4096_human_ar | 12 | r=1 | 81 | 0.593 | 0.148 | 0.259 | 0.545 | 0.020 |
| bpe4096_human_ar | 12 | r=4 | 83 | 0.807 | 0.060 | 0.133 | 0.357 | 0.260 |
| bpe4096_human_ar | 12 | r=16 | 97 | 0.979 | 0.000 | 0.021 | 0.124 | 0.740 |
| bpe4096_human_ar | 20 | r=0 | 105 | 0.248 | 0.371 | 0.381 | 2.646 | 0.000 |
| bpe4096_human_ar | 20 | r=1 | 81 | 1.000 | 0.000 | 0.000 | 0.053 | 0.980 |
| bpe4096_human_ar | 20 | r=4 | 83 | 1.000 | 0.000 | 0.000 | 0.037 | 0.980 |
| bpe4096_human_ar | 20 | r=16 | 97 | 1.000 | 0.000 | 0.000 | 0.019 | 1.000 |
| bpe4096_human_ar | 30 | r=0 | 210 | 0.238 | 0.305 | 0.457 | 2.792 | 0.000 |
| bpe4096_human_ar | 30 | r=1 | 162 | 1.000 | 0.000 | 0.000 | 0.009 | 1.000 |
| bpe4096_human_ar | 30 | r=4 | 166 | 1.000 | 0.000 | 0.000 | 0.009 | 1.000 |
| bpe4096_human_ar | 30 | r=16 | 194 | 1.000 | 0.000 | 0.000 | 0.007 | 1.000 |
| dnabert2bpe_causal_human | 0 | r=0 | 28 | 0.179 | 0.393 | 0.429 | 2.628 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=1 | 21 | 0.190 | 0.429 | 0.381 | 2.548 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=4 | 17 | 0.118 | 0.412 | 0.471 | 2.486 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=16 | 16 | 0.250 | 0.250 | 0.500 | 2.429 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=0 | 28 | 0.250 | 0.321 | 0.429 | 1.901 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=1 | 21 | 0.190 | 0.286 | 0.524 | 1.934 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=4 | 17 | 0.176 | 0.412 | 0.412 | 1.813 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=16 | 16 | 0.250 | 0.312 | 0.438 | 1.827 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=0 | 28 | 0.286 | 0.357 | 0.357 | 1.769 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=1 | 21 | 0.238 | 0.143 | 0.619 | 1.930 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=4 | 17 | 0.176 | 0.353 | 0.471 | 1.618 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=16 | 16 | 0.250 | 0.438 | 0.312 | 1.584 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=0 | 28 | 0.214 | 0.321 | 0.464 | 1.672 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=1 | 21 | 0.190 | 0.381 | 0.429 | 1.849 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=4 | 17 | 0.294 | 0.353 | 0.353 | 1.349 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=16 | 16 | 0.750 | 0.125 | 0.125 | 0.740 | 0.500 |
| dnabert2bpe_causal_human | 15 | r=0 | 28 | 0.286 | 0.357 | 0.357 | 1.713 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=1 | 21 | 0.143 | 0.238 | 0.619 | 1.709 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=4 | 17 | 0.412 | 0.176 | 0.412 | 1.030 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=16 | 16 | 1.000 | 0.000 | 0.000 | 0.287 | 0.900 |
| dnabert2bpe_causal_human | 30 | r=0 | 28 | 0.179 | 0.429 | 0.393 | 1.879 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 1.045 | 0.100 |
| dnabert2bpe_causal_human | 30 | r=4 | 17 | 0.765 | 0.059 | 0.176 | 0.299 | 0.500 |
| dnabert2bpe_causal_human | 30 | r=16 | 16 | 1.000 | 0.000 | 0.000 | 0.121 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=0 | 105 | 0.286 | 0.390 | 0.324 | 2.325 | 0.000 |
| dnabert2bpe_causal_human | 50 | r=1 | 81 | 0.840 | 0.049 | 0.111 | 0.176 | 0.560 |
| dnabert2bpe_causal_human | 50 | r=4 | 84 | 1.000 | 0.000 | 0.000 | 0.059 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=16 | 97 | 1.000 | 0.000 | 0.000 | 0.028 | 1.000 |
| dnabert3_causal_human | 0 | r=0 | 28 | 0.214 | 0.250 | 0.536 | 2.890 | 0.000 |
| dnabert3_causal_human | 0 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 2.590 | 0.000 |
| dnabert3_causal_human | 0 | r=4 | 16 | 0.312 | 0.312 | 0.375 | 2.967 | 0.000 |
| dnabert3_causal_human | 0 | r=16 | 16 | 0.375 | 0.250 | 0.375 | 2.984 | 0.000 |
| dnabert3_causal_human | 1 | r=0 | 28 | 0.250 | 0.107 | 0.643 | 1.968 | 0.000 |
| dnabert3_causal_human | 1 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 1.947 | 0.000 |
| dnabert3_causal_human | 1 | r=4 | 16 | 0.250 | 0.312 | 0.438 | 1.963 | 0.000 |
| dnabert3_causal_human | 1 | r=16 | 16 | 0.375 | 0.312 | 0.312 | 1.984 | 0.000 |
| dnabert3_causal_human | 3 | r=0 | 28 | 0.214 | 0.179 | 0.607 | 1.954 | 0.000 |
| dnabert3_causal_human | 3 | r=1 | 21 | 0.286 | 0.238 | 0.476 | 1.919 | 0.000 |
| dnabert3_causal_human | 3 | r=4 | 16 | 0.250 | 0.438 | 0.312 | 1.929 | 0.000 |
| dnabert3_causal_human | 3 | r=16 | 16 | 0.375 | 0.312 | 0.312 | 1.945 | 0.000 |
| dnabert3_causal_human | 8 | r=0 | 28 | 0.179 | 0.286 | 0.536 | 1.657 | 0.000 |
| dnabert3_causal_human | 8 | r=1 | 21 | 0.286 | 0.143 | 0.571 | 1.963 | 0.000 |
| dnabert3_causal_human | 8 | r=4 | 16 | 0.188 | 0.438 | 0.375 | 1.751 | 0.000 |
| dnabert3_causal_human | 8 | r=16 | 16 | 0.375 | 0.375 | 0.250 | 1.443 | 0.000 |
| dnabert3_causal_human | 15 | r=0 | 28 | 0.179 | 0.464 | 0.357 | 1.590 | 0.000 |
| dnabert3_causal_human | 15 | r=1 | 21 | 0.286 | 0.190 | 0.524 | 1.929 | 0.000 |
| dnabert3_causal_human | 15 | r=4 | 16 | 0.188 | 0.438 | 0.375 | 1.661 | 0.000 |
| dnabert3_causal_human | 15 | r=16 | 16 | 0.500 | 0.438 | 0.062 | 1.085 | 0.200 |
| dnabert3_causal_human | 30 | r=0 | 28 | 0.143 | 0.536 | 0.321 | 1.632 | 0.000 |
| dnabert3_causal_human | 30 | r=1 | 21 | 0.190 | 0.286 | 0.524 | 1.891 | 0.000 |
| dnabert3_causal_human | 30 | r=4 | 16 | 0.250 | 0.375 | 0.375 | 1.481 | 0.000 |
| dnabert3_causal_human | 30 | r=16 | 16 | 0.875 | 0.062 | 0.062 | 0.651 | 0.600 |
| dnabert3_causal_human | 50 | r=0 | 105 | 0.248 | 0.419 | 0.333 | 1.784 | 0.000 |
| dnabert3_causal_human | 50 | r=1 | 81 | 0.272 | 0.358 | 0.370 | 1.445 | 0.000 |
| dnabert3_causal_human | 50 | r=4 | 83 | 0.434 | 0.289 | 0.277 | 1.173 | 0.040 |
| dnabert3_causal_human | 50 | r=16 | 97 | 0.990 | 0.000 | 0.010 | 0.326 | 0.960 |
| dnabert4_causal_human | 0 | r=0 | 28 | 0.179 | 0.429 | 0.393 | 2.691 | 0.000 |
| dnabert4_causal_human | 0 | r=1 | 21 | 0.238 | 0.095 | 0.667 | 2.602 | 0.000 |
| dnabert4_causal_human | 0 | r=4 | 16 | 0.312 | 0.375 | 0.312 | 2.725 | 0.000 |
| dnabert4_causal_human | 0 | r=16 | 16 | 0.312 | 0.250 | 0.438 | 2.529 | 0.000 |
| dnabert4_causal_human | 1 | r=0 | 28 | 0.357 | 0.214 | 0.429 | 2.014 | 0.000 |
| dnabert4_causal_human | 1 | r=1 | 21 | 0.286 | 0.190 | 0.524 | 1.958 | 0.000 |
| dnabert4_causal_human | 1 | r=4 | 16 | 0.438 | 0.250 | 0.312 | 1.996 | 0.000 |
| dnabert4_causal_human | 1 | r=16 | 16 | 0.188 | 0.250 | 0.562 | 1.961 | 0.000 |
| dnabert4_causal_human | 3 | r=0 | 28 | 0.250 | 0.250 | 0.500 | 1.973 | 0.000 |
| dnabert4_causal_human | 3 | r=1 | 21 | 0.238 | 0.286 | 0.476 | 1.904 | 0.000 |
| dnabert4_causal_human | 3 | r=4 | 16 | 0.250 | 0.375 | 0.375 | 1.911 | 0.000 |
| dnabert4_causal_human | 3 | r=16 | 16 | 0.375 | 0.250 | 0.375 | 1.915 | 0.000 |
| dnabert4_causal_human | 8 | r=0 | 28 | 0.214 | 0.393 | 0.393 | 1.795 | 0.000 |
| dnabert4_causal_human | 8 | r=1 | 21 | 0.190 | 0.190 | 0.619 | 1.991 | 0.000 |
| dnabert4_causal_human | 8 | r=4 | 16 | 0.250 | 0.562 | 0.188 | 1.746 | 0.000 |
| dnabert4_causal_human | 8 | r=16 | 16 | 0.312 | 0.438 | 0.250 | 1.519 | 0.000 |
| dnabert4_causal_human | 15 | r=0 | 28 | 0.250 | 0.500 | 0.250 | 1.651 | 0.000 |
| dnabert4_causal_human | 15 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.951 | 0.000 |
| dnabert4_causal_human | 15 | r=4 | 16 | 0.188 | 0.438 | 0.375 | 1.616 | 0.000 |
| dnabert4_causal_human | 15 | r=16 | 16 | 0.375 | 0.438 | 0.188 | 1.269 | 0.000 |
| dnabert4_causal_human | 30 | r=0 | 28 | 0.036 | 0.643 | 0.321 | 1.658 | 0.000 |
| dnabert4_causal_human | 30 | r=1 | 21 | 0.190 | 0.238 | 0.571 | 1.922 | 0.000 |
| dnabert4_causal_human | 30 | r=4 | 16 | 0.188 | 0.562 | 0.250 | 1.435 | 0.000 |
| dnabert4_causal_human | 30 | r=16 | 16 | 0.875 | 0.062 | 0.062 | 0.743 | 0.600 |
| dnabert4_causal_human | 50 | r=0 | 105 | 0.267 | 0.333 | 0.400 | 1.769 | 0.000 |
| dnabert4_causal_human | 50 | r=1 | 81 | 0.259 | 0.346 | 0.395 | 1.461 | 0.000 |
| dnabert4_causal_human | 50 | r=4 | 83 | 0.518 | 0.265 | 0.217 | 1.215 | 0.060 |
| dnabert4_causal_human | 50 | r=16 | 97 | 0.979 | 0.010 | 0.010 | 0.401 | 0.860 |
| dnabert5_causal_human | 0 | r=0 | 28 | 0.214 | 0.179 | 0.607 | 3.086 | 0.000 |
| dnabert5_causal_human | 0 | r=1 | 21 | 0.286 | 0.095 | 0.619 | 2.954 | 0.000 |
| dnabert5_causal_human | 0 | r=4 | 16 | 0.250 | 0.250 | 0.500 | 3.403 | 0.000 |
| dnabert5_causal_human | 0 | r=16 | 16 | 0.562 | 0.062 | 0.375 | 2.996 | 0.000 |
| dnabert5_causal_human | 1 | r=0 | 28 | 0.286 | 0.143 | 0.571 | 2.030 | 0.000 |
| dnabert5_causal_human | 1 | r=1 | 21 | 0.238 | 0.286 | 0.476 | 2.081 | 0.000 |
| dnabert5_causal_human | 1 | r=4 | 16 | 0.312 | 0.312 | 0.375 | 2.084 | 0.000 |
| dnabert5_causal_human | 1 | r=16 | 16 | 0.375 | 0.250 | 0.375 | 2.044 | 0.000 |
| dnabert5_causal_human | 3 | r=0 | 28 | 0.286 | 0.179 | 0.536 | 1.882 | 0.000 |
| dnabert5_causal_human | 3 | r=1 | 21 | 0.286 | 0.143 | 0.571 | 1.926 | 0.000 |
| dnabert5_causal_human | 3 | r=4 | 16 | 0.188 | 0.500 | 0.312 | 1.852 | 0.000 |
| dnabert5_causal_human | 3 | r=16 | 16 | 0.250 | 0.375 | 0.375 | 1.767 | 0.000 |
| dnabert5_causal_human | 8 | r=0 | 28 | 0.179 | 0.321 | 0.500 | 1.774 | 0.000 |
| dnabert5_causal_human | 8 | r=1 | 21 | 0.190 | 0.143 | 0.667 | 1.926 | 0.000 |
| dnabert5_causal_human | 8 | r=4 | 16 | 0.125 | 0.500 | 0.375 | 1.687 | 0.000 |
| dnabert5_causal_human | 8 | r=16 | 16 | 0.312 | 0.438 | 0.250 | 1.508 | 0.000 |
| dnabert5_causal_human | 15 | r=0 | 28 | 0.143 | 0.536 | 0.321 | 1.720 | 0.000 |
| dnabert5_causal_human | 15 | r=1 | 21 | 0.143 | 0.190 | 0.667 | 1.954 | 0.000 |
| dnabert5_causal_human | 15 | r=4 | 16 | 0.125 | 0.375 | 0.500 | 1.618 | 0.000 |
| dnabert5_causal_human | 15 | r=16 | 16 | 0.375 | 0.500 | 0.125 | 1.201 | 0.000 |
| dnabert5_causal_human | 30 | r=0 | 28 | 0.179 | 0.571 | 0.250 | 1.744 | 0.000 |
| dnabert5_causal_human | 30 | r=1 | 21 | 0.333 | 0.143 | 0.524 | 1.913 | 0.000 |
| dnabert5_causal_human | 30 | r=4 | 16 | 0.188 | 0.438 | 0.375 | 1.406 | 0.000 |
| dnabert5_causal_human | 30 | r=16 | 16 | 0.875 | 0.125 | 0.000 | 0.753 | 0.600 |
| dnabert5_causal_human | 50 | r=0 | 105 | 0.219 | 0.476 | 0.305 | 1.817 | 0.000 |
| dnabert5_causal_human | 50 | r=1 | 81 | 0.309 | 0.296 | 0.395 | 1.448 | 0.000 |
| dnabert5_causal_human | 50 | r=4 | 83 | 0.494 | 0.277 | 0.229 | 1.142 | 0.100 |
| dnabert5_causal_human | 50 | r=16 | 97 | 0.876 | 0.052 | 0.072 | 0.429 | 0.660 |
| dnabert6_causal_human | 0 | r=0 | 28 | 0.143 | 0.143 | 0.714 | 4.842 | 0.000 |
| dnabert6_causal_human | 0 | r=1 | 21 | 0.429 | 0.143 | 0.429 | 4.226 | 0.000 |
| dnabert6_causal_human | 0 | r=4 | 16 | 0.625 | 0.188 | 0.188 | 4.703 | 0.000 |
| dnabert6_causal_human | 0 | r=16 | 16 | 0.312 | 0.250 | 0.438 | 4.766 | 0.000 |
| dnabert6_causal_human | 1 | r=0 | 28 | 0.214 | 0.286 | 0.500 | 1.984 | 0.000 |
| dnabert6_causal_human | 1 | r=1 | 21 | 0.286 | 0.238 | 0.476 | 2.060 | 0.000 |
| dnabert6_causal_human | 1 | r=4 | 16 | 0.438 | 0.188 | 0.375 | 1.932 | 0.000 |
| dnabert6_causal_human | 1 | r=16 | 16 | 0.438 | 0.188 | 0.375 | 1.930 | 0.000 |
| dnabert6_causal_human | 3 | r=0 | 28 | 0.143 | 0.250 | 0.607 | 1.829 | 0.000 |
| dnabert6_causal_human | 3 | r=1 | 21 | 0.238 | 0.190 | 0.571 | 1.937 | 0.000 |
| dnabert6_causal_human | 3 | r=4 | 16 | 0.125 | 0.562 | 0.312 | 1.723 | 0.000 |
| dnabert6_causal_human | 3 | r=16 | 16 | 0.375 | 0.438 | 0.188 | 1.548 | 0.000 |
| dnabert6_causal_human | 8 | r=0 | 28 | 0.214 | 0.464 | 0.321 | 1.692 | 0.000 |
| dnabert6_causal_human | 8 | r=1 | 21 | 0.333 | 0.190 | 0.476 | 1.902 | 0.000 |
| dnabert6_causal_human | 8 | r=4 | 16 | 0.188 | 0.375 | 0.438 | 1.625 | 0.000 |
| dnabert6_causal_human | 8 | r=16 | 16 | 0.500 | 0.438 | 0.062 | 1.181 | 0.000 |
| dnabert6_causal_human | 15 | r=0 | 28 | 0.250 | 0.500 | 0.250 | 1.682 | 0.000 |
| dnabert6_causal_human | 15 | r=1 | 21 | 0.190 | 0.143 | 0.667 | 1.899 | 0.000 |
| dnabert6_causal_human | 15 | r=4 | 16 | 0.188 | 0.312 | 0.500 | 1.537 | 0.000 |
| dnabert6_causal_human | 15 | r=16 | 16 | 0.750 | 0.250 | 0.000 | 0.885 | 0.400 |
| dnabert6_causal_human | 30 | r=0 | 28 | 0.143 | 0.536 | 0.321 | 1.722 | 0.000 |
| dnabert6_causal_human | 30 | r=1 | 21 | 0.286 | 0.143 | 0.571 | 1.837 | 0.000 |
| dnabert6_causal_human | 30 | r=4 | 16 | 0.312 | 0.375 | 0.312 | 1.284 | 0.000 |
| dnabert6_causal_human | 30 | r=16 | 16 | 0.875 | 0.062 | 0.062 | 0.568 | 0.600 |
| dnabert6_causal_human | 50 | r=0 | 105 | 0.257 | 0.390 | 0.352 | 1.831 | 0.000 |
| dnabert6_causal_human | 50 | r=1 | 81 | 0.358 | 0.272 | 0.370 | 1.238 | 0.060 |
| dnabert6_causal_human | 50 | r=4 | 83 | 0.651 | 0.145 | 0.205 | 0.848 | 0.140 |
| dnabert6_causal_human | 50 | r=16 | 97 | 0.948 | 0.021 | 0.031 | 0.278 | 0.840 |
| hyena_medium-160k_human | 0 | r=0 | 105 | 0.267 | 0.352 | 0.381 | 1.756 | 0.000 |
| hyena_medium-160k_human | 0 | r=1 | 81 | 0.173 | 0.346 | 0.481 | 1.758 | 0.000 |
| hyena_medium-160k_human | 0 | r=4 | 83 | 0.253 | 0.337 | 0.410 | 1.658 | 0.000 |
| hyena_medium-160k_human | 0 | r=16 | 97 | 0.175 | 0.381 | 0.443 | 1.745 | 0.000 |
| hyena_medium-160k_human | 1 | r=0 | 105 | 0.238 | 0.390 | 0.371 | 1.751 | 0.000 |
| hyena_medium-160k_human | 1 | r=1 | 81 | 0.210 | 0.284 | 0.506 | 1.727 | 0.000 |
| hyena_medium-160k_human | 1 | r=4 | 83 | 0.301 | 0.313 | 0.386 | 1.617 | 0.000 |
| hyena_medium-160k_human | 1 | r=16 | 97 | 0.237 | 0.381 | 0.381 | 1.649 | 0.000 |
| hyena_medium-160k_human | 3 | r=0 | 105 | 0.238 | 0.333 | 0.429 | 1.731 | 0.000 |
| hyena_medium-160k_human | 3 | r=1 | 81 | 0.210 | 0.358 | 0.432 | 1.687 | 0.000 |
| hyena_medium-160k_human | 3 | r=4 | 83 | 0.277 | 0.361 | 0.361 | 1.543 | 0.000 |
| hyena_medium-160k_human | 3 | r=16 | 97 | 0.351 | 0.351 | 0.299 | 1.381 | 0.000 |
| hyena_medium-160k_human | 8 | r=0 | 105 | 0.276 | 0.362 | 0.362 | 1.706 | 0.000 |
| hyena_medium-160k_human | 8 | r=1 | 81 | 0.222 | 0.383 | 0.395 | 1.607 | 0.000 |
| hyena_medium-160k_human | 8 | r=4 | 83 | 0.361 | 0.325 | 0.313 | 1.326 | 0.000 |
| hyena_medium-160k_human | 8 | r=16 | 97 | 0.680 | 0.227 | 0.093 | 0.444 | 0.420 |
| hyena_medium-160k_human | 15 | r=0 | 105 | 0.229 | 0.352 | 0.419 | 1.738 | 0.000 |
| hyena_medium-160k_human | 15 | r=1 | 81 | 0.235 | 0.321 | 0.444 | 1.480 | 0.000 |
| hyena_medium-160k_human | 15 | r=4 | 83 | 0.578 | 0.181 | 0.241 | 0.982 | 0.040 |
| hyena_medium-160k_human | 15 | r=16 | 97 | 0.845 | 0.144 | 0.010 | 0.288 | 0.680 |
| hyena_medium-160k_human | 30 | r=0 | 105 | 0.219 | 0.352 | 0.429 | 1.874 | 0.000 |
| hyena_medium-160k_human | 30 | r=1 | 81 | 0.358 | 0.296 | 0.346 | 1.266 | 0.000 |
| hyena_medium-160k_human | 30 | r=4 | 83 | 0.614 | 0.217 | 0.169 | 0.616 | 0.040 |
| hyena_medium-160k_human | 30 | r=16 | 97 | 0.835 | 0.093 | 0.072 | 0.213 | 0.660 |
| hyena_medium-160k_human | 50 | r=0 | 105 | 0.143 | 0.390 | 0.467 | 2.404 | 0.000 |
| hyena_medium-160k_human | 50 | r=1 | 81 | 0.432 | 0.259 | 0.309 | 0.975 | 0.000 |
| hyena_medium-160k_human | 50 | r=4 | 83 | 0.699 | 0.145 | 0.157 | 0.350 | 0.300 |
| hyena_medium-160k_human | 50 | r=16 | 97 | 0.928 | 0.062 | 0.010 | 0.135 | 0.860 |

## Leakage: member minus non-member rare-allele recovery

| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |
|---|---|---|---|---|---|
| 6mer_ar | 1 | — | — | — | — |
| 6mer_ar | 2 | — | — | — | — |
| 6mer_ar | 3 | — | — | — | — |
| 6mer_ar | 5 | — | — | — | — |
| 6mer_ar | 8 | — | — | — | — |
| 6mer_ar | 12 | — | — | — | — |
| 6mer_ar | 20 | — | — | — | — |
| 6mer_ar | 30 | — | — | — | — |
| bpe4096_human_ar | 1 | 0.258 | 0.296 | 0.257 | +0.001 |
| bpe4096_human_ar | 2 | 0.206 | 0.284 | 0.276 | -0.070 |
| bpe4096_human_ar | 3 | 0.299 | 0.185 | 0.238 | +0.061 |
| bpe4096_human_ar | 5 | 0.722 | 0.284 | 0.295 | +0.426 |
| bpe4096_human_ar | 8 | 0.969 | 0.494 | 0.248 | +0.721 |
| bpe4096_human_ar | 12 | 0.979 | 0.593 | 0.257 | +0.722 |
| bpe4096_human_ar | 20 | 1.000 | 1.000 | 0.248 | +0.752 |
| bpe4096_human_ar | 30 | 1.000 | 1.000 | 0.238 | +0.762 |
| dnabert2bpe_causal_human | 0 | 0.250 | 0.190 | 0.179 | +0.071 |
| dnabert2bpe_causal_human | 1 | 0.250 | 0.190 | 0.250 | +0.000 |
| dnabert2bpe_causal_human | 3 | 0.250 | 0.238 | 0.286 | -0.036 |
| dnabert2bpe_causal_human | 8 | 0.750 | 0.190 | 0.214 | +0.536 |
| dnabert2bpe_causal_human | 15 | 1.000 | 0.143 | 0.286 | +0.714 |
| dnabert2bpe_causal_human | 30 | 1.000 | 0.333 | 0.179 | +0.821 |
| dnabert2bpe_causal_human | 50 | 1.000 | 0.840 | 0.286 | +0.714 |
| dnabert3_causal_human | 0 | 0.375 | 0.333 | 0.214 | +0.161 |
| dnabert3_causal_human | 1 | 0.375 | 0.333 | 0.250 | +0.125 |
| dnabert3_causal_human | 3 | 0.375 | 0.286 | 0.214 | +0.161 |
| dnabert3_causal_human | 8 | 0.375 | 0.286 | 0.179 | +0.196 |
| dnabert3_causal_human | 15 | 0.500 | 0.286 | 0.179 | +0.321 |
| dnabert3_causal_human | 30 | 0.875 | 0.190 | 0.143 | +0.732 |
| dnabert3_causal_human | 50 | 0.990 | 0.272 | 0.248 | +0.742 |
| dnabert4_causal_human | 0 | 0.312 | 0.238 | 0.179 | +0.134 |
| dnabert4_causal_human | 1 | 0.188 | 0.286 | 0.357 | -0.170 |
| dnabert4_causal_human | 3 | 0.375 | 0.238 | 0.250 | +0.125 |
| dnabert4_causal_human | 8 | 0.312 | 0.190 | 0.214 | +0.098 |
| dnabert4_causal_human | 15 | 0.375 | 0.238 | 0.250 | +0.125 |
| dnabert4_causal_human | 30 | 0.875 | 0.190 | 0.036 | +0.839 |
| dnabert4_causal_human | 50 | 0.979 | 0.259 | 0.267 | +0.713 |
| dnabert5_causal_human | 0 | 0.562 | 0.286 | 0.214 | +0.348 |
| dnabert5_causal_human | 1 | 0.375 | 0.238 | 0.286 | +0.089 |
| dnabert5_causal_human | 3 | 0.250 | 0.286 | 0.286 | -0.036 |
| dnabert5_causal_human | 8 | 0.312 | 0.190 | 0.179 | +0.134 |
| dnabert5_causal_human | 15 | 0.375 | 0.143 | 0.143 | +0.232 |
| dnabert5_causal_human | 30 | 0.875 | 0.333 | 0.179 | +0.696 |
| dnabert5_causal_human | 50 | 0.876 | 0.309 | 0.219 | +0.657 |
| dnabert6_causal_human | 0 | 0.312 | 0.429 | 0.143 | +0.170 |
| dnabert6_causal_human | 1 | 0.438 | 0.286 | 0.214 | +0.223 |
| dnabert6_causal_human | 3 | 0.375 | 0.238 | 0.143 | +0.232 |
| dnabert6_causal_human | 8 | 0.500 | 0.333 | 0.214 | +0.286 |
| dnabert6_causal_human | 15 | 0.750 | 0.190 | 0.250 | +0.500 |
| dnabert6_causal_human | 30 | 0.875 | 0.286 | 0.143 | +0.732 |
| dnabert6_causal_human | 50 | 0.948 | 0.358 | 0.257 | +0.691 |
| hyena_medium-160k_human | 0 | 0.175 | 0.173 | 0.267 | -0.091 |
| hyena_medium-160k_human | 1 | 0.237 | 0.210 | 0.238 | -0.001 |
| hyena_medium-160k_human | 3 | 0.351 | 0.210 | 0.238 | +0.112 |
| hyena_medium-160k_human | 8 | 0.680 | 0.222 | 0.276 | +0.404 |
| hyena_medium-160k_human | 15 | 0.845 | 0.235 | 0.229 | +0.617 |
| hyena_medium-160k_human | 30 | 0.835 | 0.358 | 0.219 | +0.616 |
| hyena_medium-160k_human | 50 | 0.928 | 0.432 | 0.143 | +0.785 |
