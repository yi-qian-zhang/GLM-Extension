# Rare-allele recovery on real human canaries — chr21

Canaries: 400 haplotype segments of 96 nt from 1000 Genomes phase 3 (2,548 samples), chr22 (GRCh38), variants with AF <= 0.001 and <= 5 carriers.

`alt` = the individual's rare allele was produced, `ref` = the reference base was produced (the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.

| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |
|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | r=0 | 23 | 0.348 | 0.130 | 0.522 | 2.364 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=1 | 20 | 0.350 | 0.300 | 0.350 | 2.562 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=4 | 18 | 0.278 | 0.167 | 0.556 | 2.463 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=16 | 18 | 0.111 | 0.278 | 0.611 | 2.488 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=0 | 23 | 0.348 | 0.130 | 0.522 | 1.828 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=1 | 20 | 0.300 | 0.450 | 0.250 | 1.908 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=4 | 18 | 0.389 | 0.222 | 0.389 | 1.858 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=16 | 18 | 0.056 | 0.333 | 0.611 | 1.876 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=0 | 23 | 0.304 | 0.217 | 0.478 | 1.753 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=1 | 20 | 0.200 | 0.400 | 0.400 | 1.897 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=4 | 18 | 0.222 | 0.278 | 0.500 | 1.808 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=16 | 18 | 0.056 | 0.333 | 0.611 | 1.777 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=0 | 23 | 0.261 | 0.174 | 0.565 | 1.758 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=1 | 20 | 0.200 | 0.350 | 0.450 | 1.874 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=4 | 18 | 0.500 | 0.167 | 0.333 | 1.640 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=16 | 18 | 0.333 | 0.333 | 0.333 | 1.321 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=0 | 23 | 0.261 | 0.261 | 0.478 | 1.812 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=1 | 20 | 0.250 | 0.150 | 0.600 | 1.725 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=4 | 18 | 0.389 | 0.111 | 0.500 | 1.355 | 0.100 |
| dnabert2bpe_causal_human | 15 | r=16 | 18 | 1.000 | 0.000 | 0.000 | 0.312 | 1.000 |
| dnabert2bpe_causal_human | 30 | r=0 | 23 | 0.217 | 0.174 | 0.609 | 2.049 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=1 | 20 | 0.450 | 0.250 | 0.300 | 1.103 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=4 | 18 | 0.889 | 0.056 | 0.056 | 0.514 | 0.400 |
| dnabert2bpe_causal_human | 30 | r=16 | 18 | 1.000 | 0.000 | 0.000 | 0.153 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=0 | 118 | 0.271 | 0.237 | 0.492 | 2.491 | 0.000 |
| dnabert2bpe_causal_human | 50 | r=1 | 93 | 0.774 | 0.065 | 0.161 | 0.300 | 0.440 |
| dnabert2bpe_causal_human | 50 | r=4 | 81 | 1.000 | 0.000 | 0.000 | 0.074 | 0.960 |
| dnabert2bpe_causal_human | 50 | r=16 | 101 | 1.000 | 0.000 | 0.000 | 0.045 | 1.000 |
| dnabert3_causal_human | 0 | r=0 | 46 | 0.326 | 0.283 | 0.391 | 3.038 | 0.000 |
| dnabert3_causal_human | 0 | r=1 | 40 | 0.200 | 0.300 | 0.500 | 2.774 | 0.000 |
| dnabert3_causal_human | 0 | r=4 | 36 | 0.167 | 0.444 | 0.389 | 2.915 | 0.000 |
| dnabert3_causal_human | 0 | r=16 | 36 | 0.167 | 0.278 | 0.556 | 2.692 | 0.000 |
| dnabert3_causal_human | 1 | r=0 | 46 | 0.283 | 0.217 | 0.500 | 1.907 | 0.000 |
| dnabert3_causal_human | 1 | r=1 | 40 | 0.175 | 0.275 | 0.550 | 1.934 | 0.000 |
| dnabert3_causal_human | 1 | r=4 | 36 | 0.361 | 0.139 | 0.500 | 1.937 | 0.000 |
| dnabert3_causal_human | 1 | r=16 | 36 | 0.083 | 0.333 | 0.583 | 1.903 | 0.000 |
| dnabert3_causal_human | 3 | r=0 | 46 | 0.435 | 0.174 | 0.391 | 1.896 | 0.000 |
| dnabert3_causal_human | 3 | r=1 | 40 | 0.200 | 0.275 | 0.525 | 1.899 | 0.000 |
| dnabert3_causal_human | 3 | r=4 | 36 | 0.333 | 0.167 | 0.500 | 1.927 | 0.000 |
| dnabert3_causal_human | 3 | r=16 | 36 | 0.111 | 0.306 | 0.583 | 1.874 | 0.000 |
| dnabert3_causal_human | 8 | r=0 | 46 | 0.435 | 0.174 | 0.391 | 1.844 | 0.000 |
| dnabert3_causal_human | 8 | r=1 | 40 | 0.175 | 0.400 | 0.425 | 1.959 | 0.000 |
| dnabert3_causal_human | 8 | r=4 | 36 | 0.417 | 0.167 | 0.417 | 1.879 | 0.000 |
| dnabert3_causal_human | 8 | r=16 | 36 | 0.167 | 0.444 | 0.389 | 1.892 | 0.000 |
| dnabert3_causal_human | 15 | r=0 | 46 | 0.435 | 0.261 | 0.304 | 1.843 | 0.000 |
| dnabert3_causal_human | 15 | r=1 | 40 | 0.225 | 0.350 | 0.425 | 1.926 | 0.000 |
| dnabert3_causal_human | 15 | r=4 | 36 | 0.444 | 0.250 | 0.306 | 1.825 | 0.000 |
| dnabert3_causal_human | 15 | r=16 | 36 | 0.111 | 0.306 | 0.583 | 1.862 | 0.000 |
| dnabert3_causal_human | 30 | r=0 | 46 | 0.348 | 0.370 | 0.283 | 1.941 | 0.000 |
| dnabert3_causal_human | 30 | r=1 | 40 | 0.200 | 0.300 | 0.500 | 1.852 | 0.000 |
| dnabert3_causal_human | 30 | r=4 | 36 | 0.361 | 0.222 | 0.417 | 1.714 | 0.000 |
| dnabert3_causal_human | 30 | r=16 | 36 | 0.306 | 0.361 | 0.333 | 1.459 | 0.000 |
| dnabert3_causal_human | 50 | r=0 | 236 | 0.288 | 0.364 | 0.347 | 1.995 | 0.000 |
| dnabert3_causal_human | 50 | r=1 | 186 | 0.376 | 0.274 | 0.349 | 1.623 | 0.000 |
| dnabert3_causal_human | 50 | r=4 | 162 | 0.463 | 0.167 | 0.370 | 1.464 | 0.080 |
| dnabert3_causal_human | 50 | r=16 | 202 | 0.950 | 0.010 | 0.040 | 0.555 | 0.790 |
| dnabert4_causal_human | 0 | r=0 | 46 | 0.370 | 0.196 | 0.435 | 2.561 | 0.000 |
| dnabert4_causal_human | 0 | r=1 | 40 | 0.350 | 0.350 | 0.300 | 2.549 | 0.000 |
| dnabert4_causal_human | 0 | r=4 | 36 | 0.167 | 0.056 | 0.778 | 2.660 | 0.000 |
| dnabert4_causal_human | 0 | r=16 | 36 | 0.111 | 0.389 | 0.500 | 2.661 | 0.000 |
| dnabert4_causal_human | 1 | r=0 | 46 | 0.391 | 0.261 | 0.348 | 1.942 | 0.000 |
| dnabert4_causal_human | 1 | r=1 | 40 | 0.225 | 0.150 | 0.625 | 1.920 | 0.000 |
| dnabert4_causal_human | 1 | r=4 | 36 | 0.167 | 0.333 | 0.500 | 1.961 | 0.000 |
| dnabert4_causal_human | 1 | r=16 | 36 | 0.278 | 0.333 | 0.389 | 1.968 | 0.000 |
| dnabert4_causal_human | 3 | r=0 | 46 | 0.457 | 0.239 | 0.304 | 1.895 | 0.000 |
| dnabert4_causal_human | 3 | r=1 | 40 | 0.050 | 0.325 | 0.625 | 1.923 | 0.000 |
| dnabert4_causal_human | 3 | r=4 | 36 | 0.333 | 0.278 | 0.389 | 1.930 | 0.000 |
| dnabert4_causal_human | 3 | r=16 | 36 | 0.111 | 0.361 | 0.528 | 1.851 | 0.000 |
| dnabert4_causal_human | 8 | r=0 | 46 | 0.435 | 0.217 | 0.348 | 1.807 | 0.000 |
| dnabert4_causal_human | 8 | r=1 | 40 | 0.175 | 0.325 | 0.500 | 1.948 | 0.000 |
| dnabert4_causal_human | 8 | r=4 | 36 | 0.389 | 0.250 | 0.361 | 1.848 | 0.000 |
| dnabert4_causal_human | 8 | r=16 | 36 | 0.111 | 0.472 | 0.417 | 1.860 | 0.000 |
| dnabert4_causal_human | 15 | r=0 | 46 | 0.391 | 0.239 | 0.370 | 1.811 | 0.000 |
| dnabert4_causal_human | 15 | r=1 | 40 | 0.150 | 0.325 | 0.525 | 1.956 | 0.000 |
| dnabert4_causal_human | 15 | r=4 | 36 | 0.278 | 0.250 | 0.472 | 1.847 | 0.000 |
| dnabert4_causal_human | 15 | r=16 | 36 | 0.167 | 0.389 | 0.444 | 1.828 | 0.000 |
| dnabert4_causal_human | 30 | r=0 | 46 | 0.326 | 0.239 | 0.435 | 1.911 | 0.000 |
| dnabert4_causal_human | 30 | r=1 | 40 | 0.175 | 0.375 | 0.450 | 1.924 | 0.000 |
| dnabert4_causal_human | 30 | r=4 | 36 | 0.306 | 0.167 | 0.528 | 1.702 | 0.000 |
| dnabert4_causal_human | 30 | r=16 | 36 | 0.444 | 0.139 | 0.417 | 1.422 | 0.000 |
| dnabert4_causal_human | 50 | r=0 | 236 | 0.225 | 0.318 | 0.458 | 2.025 | 0.000 |
| dnabert4_causal_human | 50 | r=1 | 186 | 0.312 | 0.285 | 0.403 | 1.701 | 0.000 |
| dnabert4_causal_human | 50 | r=4 | 162 | 0.395 | 0.222 | 0.383 | 1.469 | 0.010 |
| dnabert4_causal_human | 50 | r=16 | 202 | 0.876 | 0.054 | 0.069 | 0.525 | 0.680 |
| dnabert5_causal_human | 0 | r=0 | 46 | 0.283 | 0.239 | 0.478 | 2.962 | 0.000 |
| dnabert5_causal_human | 0 | r=1 | 40 | 0.450 | 0.300 | 0.250 | 3.114 | 0.000 |
| dnabert5_causal_human | 0 | r=4 | 36 | 0.222 | 0.222 | 0.556 | 2.899 | 0.000 |
| dnabert5_causal_human | 0 | r=16 | 36 | 0.111 | 0.611 | 0.278 | 2.828 | 0.000 |
| dnabert5_causal_human | 1 | r=0 | 46 | 0.283 | 0.239 | 0.478 | 2.006 | 0.000 |
| dnabert5_causal_human | 1 | r=1 | 40 | 0.150 | 0.350 | 0.500 | 2.162 | 0.000 |
| dnabert5_causal_human | 1 | r=4 | 36 | 0.167 | 0.306 | 0.528 | 2.069 | 0.000 |
| dnabert5_causal_human | 1 | r=16 | 36 | 0.167 | 0.444 | 0.389 | 1.998 | 0.000 |
| dnabert5_causal_human | 3 | r=0 | 46 | 0.478 | 0.217 | 0.304 | 1.868 | 0.000 |
| dnabert5_causal_human | 3 | r=1 | 40 | 0.200 | 0.250 | 0.550 | 1.906 | 0.000 |
| dnabert5_causal_human | 3 | r=4 | 36 | 0.333 | 0.194 | 0.472 | 1.915 | 0.000 |
| dnabert5_causal_human | 3 | r=16 | 36 | 0.111 | 0.278 | 0.611 | 1.840 | 0.000 |
| dnabert5_causal_human | 8 | r=0 | 46 | 0.326 | 0.217 | 0.457 | 1.832 | 0.000 |
| dnabert5_causal_human | 8 | r=1 | 40 | 0.175 | 0.325 | 0.500 | 1.961 | 0.000 |
| dnabert5_causal_human | 8 | r=4 | 36 | 0.333 | 0.222 | 0.444 | 1.870 | 0.000 |
| dnabert5_causal_human | 8 | r=16 | 36 | 0.139 | 0.361 | 0.500 | 1.855 | 0.000 |
| dnabert5_causal_human | 15 | r=0 | 46 | 0.391 | 0.130 | 0.478 | 1.858 | 0.000 |
| dnabert5_causal_human | 15 | r=1 | 40 | 0.200 | 0.350 | 0.450 | 1.967 | 0.000 |
| dnabert5_causal_human | 15 | r=4 | 36 | 0.222 | 0.167 | 0.611 | 1.857 | 0.000 |
| dnabert5_causal_human | 15 | r=16 | 36 | 0.167 | 0.278 | 0.556 | 1.794 | 0.000 |
| dnabert5_causal_human | 30 | r=0 | 46 | 0.348 | 0.152 | 0.500 | 1.950 | 0.000 |
| dnabert5_causal_human | 30 | r=1 | 40 | 0.250 | 0.300 | 0.450 | 1.899 | 0.000 |
| dnabert5_causal_human | 30 | r=4 | 36 | 0.333 | 0.083 | 0.583 | 1.764 | 0.000 |
| dnabert5_causal_human | 30 | r=16 | 36 | 0.444 | 0.194 | 0.361 | 1.502 | 0.050 |
| dnabert5_causal_human | 50 | r=0 | 236 | 0.271 | 0.267 | 0.462 | 2.083 | 0.000 |
| dnabert5_causal_human | 50 | r=1 | 186 | 0.312 | 0.323 | 0.366 | 1.657 | 0.000 |
| dnabert5_causal_human | 50 | r=4 | 162 | 0.383 | 0.210 | 0.407 | 1.464 | 0.010 |
| dnabert5_causal_human | 50 | r=16 | 202 | 0.837 | 0.040 | 0.124 | 0.589 | 0.480 |
| dnabert6_causal_human | 0 | r=0 | 46 | 0.370 | 0.261 | 0.370 | 4.489 | 0.000 |
| dnabert6_causal_human | 0 | r=1 | 40 | 0.100 | 0.150 | 0.750 | 4.434 | 0.000 |
| dnabert6_causal_human | 0 | r=4 | 36 | 0.167 | 0.278 | 0.556 | 5.020 | 0.000 |
| dnabert6_causal_human | 0 | r=16 | 36 | 0.222 | 0.278 | 0.500 | 4.565 | 0.000 |
| dnabert6_causal_human | 1 | r=0 | 46 | 0.304 | 0.304 | 0.391 | 1.977 | 0.000 |
| dnabert6_causal_human | 1 | r=1 | 40 | 0.275 | 0.225 | 0.500 | 1.954 | 0.000 |
| dnabert6_causal_human | 1 | r=4 | 36 | 0.306 | 0.139 | 0.556 | 1.991 | 0.000 |
| dnabert6_causal_human | 1 | r=16 | 36 | 0.278 | 0.389 | 0.333 | 1.903 | 0.000 |
| dnabert6_causal_human | 3 | r=0 | 46 | 0.457 | 0.217 | 0.326 | 1.873 | 0.000 |
| dnabert6_causal_human | 3 | r=1 | 40 | 0.200 | 0.350 | 0.450 | 1.934 | 0.000 |
| dnabert6_causal_human | 3 | r=4 | 36 | 0.389 | 0.194 | 0.417 | 1.866 | 0.000 |
| dnabert6_causal_human | 3 | r=16 | 36 | 0.194 | 0.333 | 0.472 | 1.836 | 0.000 |
| dnabert6_causal_human | 8 | r=0 | 46 | 0.435 | 0.196 | 0.370 | 1.881 | 0.000 |
| dnabert6_causal_human | 8 | r=1 | 40 | 0.200 | 0.250 | 0.550 | 1.918 | 0.000 |
| dnabert6_causal_human | 8 | r=4 | 36 | 0.389 | 0.139 | 0.472 | 1.830 | 0.000 |
| dnabert6_causal_human | 8 | r=16 | 36 | 0.139 | 0.278 | 0.583 | 1.806 | 0.000 |
| dnabert6_causal_human | 15 | r=0 | 46 | 0.457 | 0.283 | 0.261 | 1.915 | 0.000 |
| dnabert6_causal_human | 15 | r=1 | 40 | 0.175 | 0.375 | 0.450 | 1.882 | 0.000 |
| dnabert6_causal_human | 15 | r=4 | 36 | 0.417 | 0.167 | 0.417 | 1.784 | 0.000 |
| dnabert6_causal_human | 15 | r=16 | 36 | 0.222 | 0.306 | 0.472 | 1.636 | 0.000 |
| dnabert6_causal_human | 30 | r=0 | 46 | 0.261 | 0.326 | 0.413 | 2.009 | 0.000 |
| dnabert6_causal_human | 30 | r=1 | 40 | 0.200 | 0.400 | 0.400 | 1.756 | 0.000 |
| dnabert6_causal_human | 30 | r=4 | 36 | 0.389 | 0.194 | 0.417 | 1.612 | 0.000 |
| dnabert6_causal_human | 30 | r=16 | 36 | 0.639 | 0.194 | 0.167 | 1.067 | 0.100 |
| dnabert6_causal_human | 50 | r=0 | 236 | 0.275 | 0.301 | 0.424 | 2.092 | 0.000 |
| dnabert6_causal_human | 50 | r=1 | 186 | 0.323 | 0.280 | 0.398 | 1.473 | 0.000 |
| dnabert6_causal_human | 50 | r=4 | 162 | 0.512 | 0.185 | 0.302 | 1.217 | 0.070 |
| dnabert6_causal_human | 50 | r=16 | 202 | 0.970 | 0.025 | 0.005 | 0.352 | 0.910 |
| hyena_medium-160k_human | 0 | r=0 | 118 | 0.288 | 0.263 | 0.449 | 1.790 | 0.000 |
| hyena_medium-160k_human | 0 | r=1 | 93 | 0.290 | 0.258 | 0.452 | 1.810 | 0.000 |
| hyena_medium-160k_human | 0 | r=4 | 81 | 0.235 | 0.185 | 0.580 | 1.838 | 0.000 |
| hyena_medium-160k_human | 0 | r=16 | 101 | 0.218 | 0.198 | 0.584 | 1.905 | 0.000 |
| hyena_medium-160k_human | 1 | r=0 | 118 | 0.254 | 0.280 | 0.466 | 1.778 | 0.000 |
| hyena_medium-160k_human | 1 | r=1 | 93 | 0.280 | 0.258 | 0.462 | 1.796 | 0.000 |
| hyena_medium-160k_human | 1 | r=4 | 81 | 0.272 | 0.235 | 0.494 | 1.809 | 0.000 |
| hyena_medium-160k_human | 1 | r=16 | 101 | 0.208 | 0.218 | 0.574 | 1.863 | 0.000 |
| hyena_medium-160k_human | 3 | r=0 | 118 | 0.271 | 0.297 | 0.432 | 1.790 | 0.000 |
| hyena_medium-160k_human | 3 | r=1 | 93 | 0.312 | 0.247 | 0.441 | 1.783 | 0.000 |
| hyena_medium-160k_human | 3 | r=4 | 81 | 0.309 | 0.235 | 0.457 | 1.764 | 0.000 |
| hyena_medium-160k_human | 3 | r=16 | 101 | 0.376 | 0.198 | 0.426 | 1.656 | 0.000 |
| hyena_medium-160k_human | 8 | r=0 | 118 | 0.246 | 0.331 | 0.424 | 1.801 | 0.000 |
| hyena_medium-160k_human | 8 | r=1 | 93 | 0.280 | 0.290 | 0.430 | 1.758 | 0.000 |
| hyena_medium-160k_human | 8 | r=4 | 81 | 0.309 | 0.198 | 0.494 | 1.586 | 0.000 |
| hyena_medium-160k_human | 8 | r=16 | 101 | 0.881 | 0.050 | 0.069 | 0.514 | 0.620 |
| hyena_medium-160k_human | 15 | r=0 | 118 | 0.254 | 0.322 | 0.424 | 1.851 | 0.000 |
| hyena_medium-160k_human | 15 | r=1 | 93 | 0.323 | 0.280 | 0.398 | 1.688 | 0.000 |
| hyena_medium-160k_human | 15 | r=4 | 81 | 0.506 | 0.148 | 0.346 | 1.264 | 0.040 |
| hyena_medium-160k_human | 15 | r=16 | 101 | 0.970 | 0.020 | 0.010 | 0.277 | 0.820 |
| hyena_medium-160k_human | 30 | r=0 | 118 | 0.305 | 0.305 | 0.390 | 2.043 | 0.000 |
| hyena_medium-160k_human | 30 | r=1 | 93 | 0.301 | 0.290 | 0.409 | 1.465 | 0.000 |
| hyena_medium-160k_human | 30 | r=4 | 81 | 0.642 | 0.136 | 0.222 | 0.802 | 0.100 |
| hyena_medium-160k_human | 30 | r=16 | 101 | 0.980 | 0.020 | 0.000 | 0.199 | 0.820 |
| hyena_medium-160k_human | 50 | r=0 | 118 | 0.254 | 0.263 | 0.483 | 2.555 | 0.000 |
| hyena_medium-160k_human | 50 | r=1 | 93 | 0.355 | 0.269 | 0.376 | 1.140 | 0.000 |
| hyena_medium-160k_human | 50 | r=4 | 81 | 0.704 | 0.111 | 0.185 | 0.519 | 0.180 |
| hyena_medium-160k_human | 50 | r=16 | 101 | 0.960 | 0.030 | 0.010 | 0.146 | 0.760 |

## Leakage: member minus non-member rare-allele recovery

| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |
|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | 0.111 | 0.350 | 0.348 | -0.237 |
| dnabert2bpe_causal_human | 1 | 0.056 | 0.300 | 0.348 | -0.292 |
| dnabert2bpe_causal_human | 3 | 0.056 | 0.200 | 0.304 | -0.249 |
| dnabert2bpe_causal_human | 8 | 0.333 | 0.200 | 0.261 | +0.072 |
| dnabert2bpe_causal_human | 15 | 1.000 | 0.250 | 0.261 | +0.739 |
| dnabert2bpe_causal_human | 30 | 1.000 | 0.450 | 0.217 | +0.783 |
| dnabert2bpe_causal_human | 50 | 1.000 | 0.774 | 0.271 | +0.729 |
| dnabert3_causal_human | 0 | 0.167 | 0.200 | 0.326 | -0.159 |
| dnabert3_causal_human | 1 | 0.083 | 0.175 | 0.283 | -0.199 |
| dnabert3_causal_human | 3 | 0.111 | 0.200 | 0.435 | -0.324 |
| dnabert3_causal_human | 8 | 0.167 | 0.175 | 0.435 | -0.268 |
| dnabert3_causal_human | 15 | 0.111 | 0.225 | 0.435 | -0.324 |
| dnabert3_causal_human | 30 | 0.306 | 0.200 | 0.348 | -0.042 |
| dnabert3_causal_human | 50 | 0.950 | 0.376 | 0.288 | +0.662 |
| dnabert4_causal_human | 0 | 0.111 | 0.350 | 0.370 | -0.258 |
| dnabert4_causal_human | 1 | 0.278 | 0.225 | 0.391 | -0.114 |
| dnabert4_causal_human | 3 | 0.111 | 0.050 | 0.457 | -0.345 |
| dnabert4_causal_human | 8 | 0.111 | 0.175 | 0.435 | -0.324 |
| dnabert4_causal_human | 15 | 0.167 | 0.150 | 0.391 | -0.225 |
| dnabert4_causal_human | 30 | 0.444 | 0.175 | 0.326 | +0.118 |
| dnabert4_causal_human | 50 | 0.876 | 0.312 | 0.225 | +0.652 |
| dnabert5_causal_human | 0 | 0.111 | 0.450 | 0.283 | -0.171 |
| dnabert5_causal_human | 1 | 0.167 | 0.150 | 0.283 | -0.116 |
| dnabert5_causal_human | 3 | 0.111 | 0.200 | 0.478 | -0.367 |
| dnabert5_causal_human | 8 | 0.139 | 0.175 | 0.326 | -0.187 |
| dnabert5_causal_human | 15 | 0.167 | 0.200 | 0.391 | -0.225 |
| dnabert5_causal_human | 30 | 0.444 | 0.250 | 0.348 | +0.097 |
| dnabert5_causal_human | 50 | 0.837 | 0.312 | 0.271 | +0.565 |
| dnabert6_causal_human | 0 | 0.222 | 0.100 | 0.370 | -0.147 |
| dnabert6_causal_human | 1 | 0.278 | 0.275 | 0.304 | -0.027 |
| dnabert6_causal_human | 3 | 0.194 | 0.200 | 0.457 | -0.262 |
| dnabert6_causal_human | 8 | 0.139 | 0.200 | 0.435 | -0.296 |
| dnabert6_causal_human | 15 | 0.222 | 0.175 | 0.457 | -0.234 |
| dnabert6_causal_human | 30 | 0.639 | 0.200 | 0.261 | +0.378 |
| dnabert6_causal_human | 50 | 0.970 | 0.323 | 0.275 | +0.695 |
| hyena_medium-160k_human | 0 | 0.218 | 0.290 | 0.288 | -0.070 |
| hyena_medium-160k_human | 1 | 0.208 | 0.280 | 0.254 | -0.046 |
| hyena_medium-160k_human | 3 | 0.376 | 0.312 | 0.271 | +0.105 |
| hyena_medium-160k_human | 8 | 0.881 | 0.280 | 0.246 | +0.635 |
| hyena_medium-160k_human | 15 | 0.970 | 0.323 | 0.254 | +0.716 |
| hyena_medium-160k_human | 30 | 0.980 | 0.301 | 0.305 | +0.675 |
| hyena_medium-160k_human | 50 | 0.960 | 0.355 | 0.254 | +0.706 |
