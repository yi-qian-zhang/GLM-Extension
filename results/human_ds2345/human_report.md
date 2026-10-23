# Rare-allele recovery on real human canaries — human_ds

Canaries: 400 haplotype segments of 96 nt from 1000 Genomes phase 3 (2,548 samples), chr22 (GRCh38), variants with AF <= 0.001 and <= 5 carriers.

`alt` = the individual's rare allele was produced, `ref` = the reference base was produced (the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.

| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |
|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | r=0 | 62 | 0.254 | 0.283 | 0.463 | 2.537 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=1 | 62 | 0.240 | 0.303 | 0.456 | 2.489 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=4 | 60 | 0.383 | 0.333 | 0.283 | 2.513 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=16 | 60 | 0.207 | 0.316 | 0.477 | 2.481 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=0 | 62 | 0.238 | 0.341 | 0.421 | 1.883 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=1 | 62 | 0.316 | 0.206 | 0.478 | 1.891 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=4 | 60 | 0.300 | 0.350 | 0.350 | 1.886 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=16 | 60 | 0.276 | 0.331 | 0.393 | 1.883 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=0 | 62 | 0.229 | 0.392 | 0.379 | 1.732 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=1 | 62 | 0.289 | 0.317 | 0.394 | 1.766 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=4 | 60 | 0.250 | 0.333 | 0.417 | 1.751 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=16 | 60 | 0.182 | 0.478 | 0.340 | 1.619 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=0 | 62 | 0.205 | 0.496 | 0.299 | 1.722 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=1 | 62 | 0.203 | 0.351 | 0.445 | 1.621 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=4 | 60 | 0.283 | 0.383 | 0.333 | 1.475 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=16 | 60 | 0.715 | 0.109 | 0.176 | 0.939 | 0.167 |
| dnabert2bpe_causal_human | 15 | r=0 | 62 | 0.259 | 0.403 | 0.339 | 1.790 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=1 | 62 | 0.211 | 0.431 | 0.358 | 1.360 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=4 | 60 | 0.500 | 0.233 | 0.267 | 1.129 | 0.167 |
| dnabert2bpe_causal_human | 15 | r=16 | 60 | 1.000 | 0.000 | 0.000 | 0.283 | 0.900 |
| dnabert2bpe_causal_human | 30 | r=0 | 62 | 0.284 | 0.362 | 0.354 | 2.004 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=1 | 62 | 0.541 | 0.145 | 0.313 | 0.740 | 0.167 |
| dnabert2bpe_causal_human | 30 | r=4 | 60 | 0.917 | 0.017 | 0.067 | 0.386 | 0.567 |
| dnabert2bpe_causal_human | 30 | r=16 | 60 | 1.000 | 0.000 | 0.000 | 0.113 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=0 | 281 | 0.266 | 0.334 | 0.400 | 2.364 | 0.000 |
| dnabert2bpe_causal_human | 50 | r=1 | 299 | 0.844 | 0.076 | 0.080 | 0.215 | 0.580 |
| dnabert2bpe_causal_human | 50 | r=4 | 276 | 1.000 | 0.000 | 0.000 | 0.054 | 0.993 |
| dnabert2bpe_causal_human | 50 | r=16 | 274 | 1.000 | 0.000 | 0.000 | 0.031 | 1.000 |
| dnabert3_causal_human | 0 | r=0 | 61 | 0.269 | 0.300 | 0.431 | 3.012 | 0.000 |
| dnabert3_causal_human | 0 | r=1 | 62 | 0.179 | 0.276 | 0.545 | 2.971 | 0.000 |
| dnabert3_causal_human | 0 | r=4 | 60 | 0.167 | 0.233 | 0.600 | 2.830 | 0.000 |
| dnabert3_causal_human | 0 | r=16 | 59 | 0.208 | 0.211 | 0.581 | 2.707 | 0.000 |
| dnabert3_causal_human | 1 | r=0 | 61 | 0.352 | 0.248 | 0.400 | 1.933 | 0.000 |
| dnabert3_causal_human | 1 | r=1 | 62 | 0.229 | 0.309 | 0.462 | 1.930 | 0.000 |
| dnabert3_causal_human | 1 | r=4 | 60 | 0.300 | 0.200 | 0.500 | 1.936 | 0.000 |
| dnabert3_causal_human | 1 | r=16 | 59 | 0.174 | 0.278 | 0.548 | 1.960 | 0.000 |
| dnabert3_causal_human | 3 | r=0 | 61 | 0.340 | 0.251 | 0.409 | 1.925 | 0.000 |
| dnabert3_causal_human | 3 | r=1 | 62 | 0.218 | 0.225 | 0.556 | 1.904 | 0.000 |
| dnabert3_causal_human | 3 | r=4 | 60 | 0.233 | 0.250 | 0.517 | 1.893 | 0.000 |
| dnabert3_causal_human | 3 | r=16 | 59 | 0.224 | 0.241 | 0.535 | 1.917 | 0.000 |
| dnabert3_causal_human | 8 | r=0 | 61 | 0.214 | 0.495 | 0.292 | 1.711 | 0.000 |
| dnabert3_causal_human | 8 | r=1 | 62 | 0.165 | 0.320 | 0.515 | 1.785 | 0.000 |
| dnabert3_causal_human | 8 | r=4 | 60 | 0.183 | 0.417 | 0.400 | 1.750 | 0.000 |
| dnabert3_causal_human | 8 | r=16 | 59 | 0.224 | 0.490 | 0.286 | 1.712 | 0.000 |
| dnabert3_causal_human | 15 | r=0 | 61 | 0.248 | 0.371 | 0.382 | 1.719 | 0.000 |
| dnabert3_causal_human | 15 | r=1 | 62 | 0.202 | 0.363 | 0.435 | 1.708 | 0.000 |
| dnabert3_causal_human | 15 | r=4 | 60 | 0.150 | 0.483 | 0.367 | 1.657 | 0.000 |
| dnabert3_causal_human | 15 | r=16 | 59 | 0.248 | 0.457 | 0.295 | 1.533 | 0.000 |
| dnabert3_causal_human | 30 | r=0 | 61 | 0.165 | 0.440 | 0.395 | 1.758 | 0.000 |
| dnabert3_causal_human | 30 | r=1 | 62 | 0.202 | 0.411 | 0.387 | 1.583 | 0.000 |
| dnabert3_causal_human | 30 | r=4 | 60 | 0.300 | 0.400 | 0.300 | 1.494 | 0.000 |
| dnabert3_causal_human | 30 | r=16 | 59 | 0.502 | 0.245 | 0.253 | 1.005 | 0.267 |
| dnabert3_causal_human | 50 | r=0 | 280 | 0.214 | 0.423 | 0.363 | 1.813 | 0.000 |
| dnabert3_causal_human | 50 | r=1 | 299 | 0.241 | 0.365 | 0.394 | 1.456 | 0.000 |
| dnabert3_causal_human | 50 | r=4 | 276 | 0.456 | 0.290 | 0.254 | 1.192 | 0.113 |
| dnabert3_causal_human | 50 | r=16 | 273 | 0.966 | 0.019 | 0.015 | 0.400 | 0.933 |
| dnabert4_causal_human | 0 | r=0 | 61 | 0.151 | 0.265 | 0.584 | 2.561 | 0.000 |
| dnabert4_causal_human | 0 | r=1 | 62 | 0.244 | 0.243 | 0.513 | 2.545 | 0.000 |
| dnabert4_causal_human | 0 | r=4 | 60 | 0.183 | 0.183 | 0.633 | 2.692 | 0.000 |
| dnabert4_causal_human | 0 | r=16 | 59 | 0.178 | 0.340 | 0.481 | 2.572 | 0.000 |
| dnabert4_causal_human | 1 | r=0 | 61 | 0.277 | 0.303 | 0.421 | 1.979 | 0.000 |
| dnabert4_causal_human | 1 | r=1 | 62 | 0.250 | 0.244 | 0.507 | 1.953 | 0.000 |
| dnabert4_causal_human | 1 | r=4 | 60 | 0.250 | 0.133 | 0.617 | 1.961 | 0.000 |
| dnabert4_causal_human | 1 | r=16 | 59 | 0.278 | 0.154 | 0.569 | 1.980 | 0.000 |
| dnabert4_causal_human | 3 | r=0 | 61 | 0.204 | 0.402 | 0.394 | 1.923 | 0.000 |
| dnabert4_causal_human | 3 | r=1 | 62 | 0.280 | 0.240 | 0.481 | 1.901 | 0.000 |
| dnabert4_causal_human | 3 | r=4 | 60 | 0.217 | 0.200 | 0.583 | 1.879 | 0.000 |
| dnabert4_causal_human | 3 | r=16 | 59 | 0.257 | 0.249 | 0.494 | 1.909 | 0.000 |
| dnabert4_causal_human | 8 | r=0 | 61 | 0.321 | 0.403 | 0.276 | 1.754 | 0.000 |
| dnabert4_causal_human | 8 | r=1 | 62 | 0.186 | 0.320 | 0.494 | 1.778 | 0.000 |
| dnabert4_causal_human | 8 | r=4 | 60 | 0.183 | 0.500 | 0.317 | 1.759 | 0.000 |
| dnabert4_causal_human | 8 | r=16 | 59 | 0.191 | 0.444 | 0.365 | 1.718 | 0.000 |
| dnabert4_causal_human | 15 | r=0 | 61 | 0.209 | 0.482 | 0.309 | 1.771 | 0.000 |
| dnabert4_causal_human | 15 | r=1 | 62 | 0.171 | 0.331 | 0.498 | 1.701 | 0.000 |
| dnabert4_causal_human | 15 | r=4 | 60 | 0.200 | 0.433 | 0.367 | 1.648 | 0.000 |
| dnabert4_causal_human | 15 | r=16 | 59 | 0.257 | 0.457 | 0.286 | 1.508 | 0.000 |
| dnabert4_causal_human | 30 | r=0 | 61 | 0.178 | 0.488 | 0.334 | 1.840 | 0.000 |
| dnabert4_causal_human | 30 | r=1 | 62 | 0.180 | 0.382 | 0.438 | 1.610 | 0.000 |
| dnabert4_causal_human | 30 | r=4 | 60 | 0.233 | 0.467 | 0.300 | 1.481 | 0.000 |
| dnabert4_causal_human | 30 | r=16 | 59 | 0.681 | 0.154 | 0.166 | 0.978 | 0.267 |
| dnabert4_causal_human | 50 | r=0 | 280 | 0.222 | 0.434 | 0.344 | 1.896 | 0.000 |
| dnabert4_causal_human | 50 | r=1 | 299 | 0.263 | 0.347 | 0.390 | 1.465 | 0.000 |
| dnabert4_causal_human | 50 | r=4 | 276 | 0.484 | 0.227 | 0.288 | 1.220 | 0.080 |
| dnabert4_causal_human | 50 | r=16 | 273 | 0.952 | 0.022 | 0.026 | 0.393 | 0.873 |
| dnabert5_causal_human | 0 | r=0 | 61 | 0.235 | 0.268 | 0.498 | 3.091 | 0.000 |
| dnabert5_causal_human | 0 | r=1 | 62 | 0.191 | 0.256 | 0.553 | 2.930 | 0.000 |
| dnabert5_causal_human | 0 | r=4 | 60 | 0.383 | 0.250 | 0.367 | 3.000 | 0.000 |
| dnabert5_causal_human | 0 | r=16 | 59 | 0.220 | 0.249 | 0.531 | 3.044 | 0.000 |
| dnabert5_causal_human | 1 | r=0 | 61 | 0.227 | 0.248 | 0.525 | 2.046 | 0.000 |
| dnabert5_causal_human | 1 | r=1 | 62 | 0.248 | 0.309 | 0.443 | 2.065 | 0.000 |
| dnabert5_causal_human | 1 | r=4 | 60 | 0.183 | 0.283 | 0.533 | 2.072 | 0.000 |
| dnabert5_causal_human | 1 | r=16 | 59 | 0.307 | 0.248 | 0.444 | 2.049 | 0.000 |
| dnabert5_causal_human | 3 | r=0 | 61 | 0.326 | 0.335 | 0.339 | 1.824 | 0.000 |
| dnabert5_causal_human | 3 | r=1 | 62 | 0.199 | 0.358 | 0.442 | 1.820 | 0.000 |
| dnabert5_causal_human | 3 | r=4 | 60 | 0.250 | 0.300 | 0.450 | 1.867 | 0.000 |
| dnabert5_causal_human | 3 | r=16 | 59 | 0.295 | 0.399 | 0.306 | 1.845 | 0.000 |
| dnabert5_causal_human | 8 | r=0 | 61 | 0.293 | 0.432 | 0.274 | 1.737 | 0.000 |
| dnabert5_causal_human | 8 | r=1 | 62 | 0.168 | 0.294 | 0.538 | 1.741 | 0.000 |
| dnabert5_causal_human | 8 | r=4 | 60 | 0.217 | 0.383 | 0.400 | 1.762 | 0.000 |
| dnabert5_causal_human | 8 | r=16 | 59 | 0.286 | 0.457 | 0.257 | 1.677 | 0.000 |
| dnabert5_causal_human | 15 | r=0 | 61 | 0.258 | 0.390 | 0.351 | 1.741 | 0.000 |
| dnabert5_causal_human | 15 | r=1 | 62 | 0.197 | 0.355 | 0.448 | 1.701 | 0.000 |
| dnabert5_causal_human | 15 | r=4 | 60 | 0.233 | 0.433 | 0.333 | 1.690 | 0.000 |
| dnabert5_causal_human | 15 | r=16 | 59 | 0.340 | 0.436 | 0.224 | 1.490 | 0.000 |
| dnabert5_causal_human | 30 | r=0 | 61 | 0.319 | 0.388 | 0.293 | 1.778 | 0.000 |
| dnabert5_causal_human | 30 | r=1 | 62 | 0.134 | 0.447 | 0.419 | 1.558 | 0.000 |
| dnabert5_causal_human | 30 | r=4 | 60 | 0.267 | 0.417 | 0.317 | 1.497 | 0.000 |
| dnabert5_causal_human | 30 | r=16 | 59 | 0.543 | 0.241 | 0.216 | 0.963 | 0.167 |
| dnabert5_causal_human | 50 | r=0 | 280 | 0.244 | 0.395 | 0.361 | 1.904 | 0.000 |
| dnabert5_causal_human | 50 | r=1 | 299 | 0.256 | 0.420 | 0.324 | 1.425 | 0.000 |
| dnabert5_causal_human | 50 | r=4 | 276 | 0.458 | 0.229 | 0.313 | 1.199 | 0.067 |
| dnabert5_causal_human | 50 | r=16 | 273 | 0.937 | 0.033 | 0.029 | 0.402 | 0.820 |
| dnabert6_causal_human | 0 | r=0 | 61 | 0.167 | 0.343 | 0.490 | 4.900 | 0.000 |
| dnabert6_causal_human | 0 | r=1 | 62 | 0.244 | 0.273 | 0.483 | 4.646 | 0.000 |
| dnabert6_causal_human | 0 | r=4 | 60 | 0.283 | 0.233 | 0.483 | 4.407 | 0.000 |
| dnabert6_causal_human | 0 | r=16 | 59 | 0.357 | 0.245 | 0.398 | 4.549 | 0.000 |
| dnabert6_causal_human | 1 | r=0 | 61 | 0.181 | 0.216 | 0.602 | 1.941 | 0.000 |
| dnabert6_causal_human | 1 | r=1 | 62 | 0.211 | 0.260 | 0.529 | 1.965 | 0.000 |
| dnabert6_causal_human | 1 | r=4 | 60 | 0.317 | 0.150 | 0.533 | 2.007 | 0.000 |
| dnabert6_causal_human | 1 | r=16 | 59 | 0.224 | 0.245 | 0.532 | 1.942 | 0.000 |
| dnabert6_causal_human | 3 | r=0 | 61 | 0.270 | 0.358 | 0.372 | 1.759 | 0.000 |
| dnabert6_causal_human | 3 | r=1 | 62 | 0.277 | 0.331 | 0.392 | 1.791 | 0.000 |
| dnabert6_causal_human | 3 | r=4 | 60 | 0.233 | 0.450 | 0.317 | 1.829 | 0.000 |
| dnabert6_causal_human | 3 | r=16 | 59 | 0.236 | 0.457 | 0.307 | 1.765 | 0.000 |
| dnabert6_causal_human | 8 | r=0 | 61 | 0.297 | 0.375 | 0.328 | 1.740 | 0.000 |
| dnabert6_causal_human | 8 | r=1 | 62 | 0.167 | 0.450 | 0.383 | 1.710 | 0.000 |
| dnabert6_causal_human | 8 | r=4 | 60 | 0.217 | 0.383 | 0.400 | 1.679 | 0.000 |
| dnabert6_causal_human | 8 | r=16 | 59 | 0.302 | 0.478 | 0.220 | 1.499 | 0.033 |
| dnabert6_causal_human | 15 | r=0 | 61 | 0.221 | 0.456 | 0.323 | 1.749 | 0.000 |
| dnabert6_causal_human | 15 | r=1 | 62 | 0.167 | 0.447 | 0.386 | 1.602 | 0.000 |
| dnabert6_causal_human | 15 | r=4 | 60 | 0.250 | 0.450 | 0.300 | 1.541 | 0.000 |
| dnabert6_causal_human | 15 | r=16 | 59 | 0.407 | 0.403 | 0.191 | 1.259 | 0.033 |
| dnabert6_causal_human | 30 | r=0 | 61 | 0.237 | 0.422 | 0.341 | 1.851 | 0.000 |
| dnabert6_causal_human | 30 | r=1 | 62 | 0.179 | 0.462 | 0.359 | 1.399 | 0.000 |
| dnabert6_causal_human | 30 | r=4 | 60 | 0.467 | 0.267 | 0.267 | 1.271 | 0.100 |
| dnabert6_causal_human | 30 | r=16 | 59 | 0.826 | 0.083 | 0.091 | 0.631 | 0.400 |
| dnabert6_causal_human | 50 | r=0 | 280 | 0.254 | 0.412 | 0.334 | 1.963 | 0.000 |
| dnabert6_causal_human | 50 | r=1 | 299 | 0.379 | 0.307 | 0.315 | 1.218 | 0.027 |
| dnabert6_causal_human | 50 | r=4 | 276 | 0.623 | 0.150 | 0.227 | 0.896 | 0.207 |
| dnabert6_causal_human | 50 | r=16 | 273 | 0.953 | 0.014 | 0.032 | 0.295 | 0.887 |
| hyena_medium-160k_human | 0 | r=0 | 280 | 0.247 | 0.333 | 0.420 | 1.728 | 0.000 |
| hyena_medium-160k_human | 0 | r=1 | 299 | 0.225 | 0.350 | 0.426 | 1.768 | 0.000 |
| hyena_medium-160k_human | 0 | r=4 | 276 | 0.235 | 0.305 | 0.460 | 1.801 | 0.000 |
| hyena_medium-160k_human | 0 | r=16 | 273 | 0.289 | 0.325 | 0.386 | 1.784 | 0.000 |
| hyena_medium-160k_human | 1 | r=0 | 280 | 0.252 | 0.368 | 0.379 | 1.707 | 0.000 |
| hyena_medium-160k_human | 1 | r=1 | 299 | 0.192 | 0.374 | 0.435 | 1.739 | 0.000 |
| hyena_medium-160k_human | 1 | r=4 | 276 | 0.244 | 0.383 | 0.374 | 1.751 | 0.000 |
| hyena_medium-160k_human | 1 | r=16 | 273 | 0.254 | 0.393 | 0.354 | 1.698 | 0.000 |
| hyena_medium-160k_human | 3 | r=0 | 280 | 0.206 | 0.397 | 0.397 | 1.702 | 0.000 |
| hyena_medium-160k_human | 3 | r=1 | 299 | 0.225 | 0.381 | 0.394 | 1.712 | 0.000 |
| hyena_medium-160k_human | 3 | r=4 | 276 | 0.250 | 0.368 | 0.382 | 1.683 | 0.000 |
| hyena_medium-160k_human | 3 | r=16 | 273 | 0.378 | 0.304 | 0.318 | 1.421 | 0.020 |
| hyena_medium-160k_human | 8 | r=0 | 280 | 0.202 | 0.416 | 0.382 | 1.708 | 0.000 |
| hyena_medium-160k_human | 8 | r=1 | 299 | 0.226 | 0.395 | 0.379 | 1.592 | 0.000 |
| hyena_medium-160k_human | 8 | r=4 | 276 | 0.326 | 0.331 | 0.343 | 1.443 | 0.007 |
| hyena_medium-160k_human | 8 | r=16 | 273 | 0.783 | 0.144 | 0.073 | 0.478 | 0.480 |
| hyena_medium-160k_human | 15 | r=0 | 280 | 0.231 | 0.392 | 0.377 | 1.759 | 0.000 |
| hyena_medium-160k_human | 15 | r=1 | 299 | 0.262 | 0.412 | 0.327 | 1.466 | 0.000 |
| hyena_medium-160k_human | 15 | r=4 | 276 | 0.508 | 0.236 | 0.256 | 1.072 | 0.053 |
| hyena_medium-160k_human | 15 | r=16 | 273 | 0.882 | 0.114 | 0.004 | 0.288 | 0.693 |
| hyena_medium-160k_human | 30 | r=0 | 280 | 0.242 | 0.394 | 0.365 | 1.955 | 0.000 |
| hyena_medium-160k_human | 30 | r=1 | 299 | 0.328 | 0.324 | 0.348 | 1.190 | 0.007 |
| hyena_medium-160k_human | 30 | r=4 | 276 | 0.674 | 0.174 | 0.152 | 0.634 | 0.213 |
| hyena_medium-160k_human | 30 | r=16 | 273 | 0.882 | 0.103 | 0.015 | 0.194 | 0.767 |
| hyena_medium-160k_human | 50 | r=0 | 280 | 0.227 | 0.370 | 0.403 | 2.530 | 0.000 |
| hyena_medium-160k_human | 50 | r=1 | 299 | 0.426 | 0.304 | 0.270 | 0.889 | 0.013 |
| hyena_medium-160k_human | 50 | r=4 | 276 | 0.745 | 0.143 | 0.113 | 0.386 | 0.280 |
| hyena_medium-160k_human | 50 | r=16 | 273 | 0.915 | 0.059 | 0.026 | 0.138 | 0.813 |

## Leakage: member minus non-member rare-allele recovery

| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |
|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | 0.207 | 0.240 | 0.254 | -0.047 |
| dnabert2bpe_causal_human | 1 | 0.276 | 0.316 | 0.238 | +0.038 |
| dnabert2bpe_causal_human | 3 | 0.182 | 0.289 | 0.229 | -0.047 |
| dnabert2bpe_causal_human | 8 | 0.715 | 0.203 | 0.205 | +0.510 |
| dnabert2bpe_causal_human | 15 | 1.000 | 0.211 | 0.259 | +0.741 |
| dnabert2bpe_causal_human | 30 | 1.000 | 0.541 | 0.284 | +0.716 |
| dnabert2bpe_causal_human | 50 | 1.000 | 0.844 | 0.266 | +0.734 |
| dnabert3_causal_human | 0 | 0.208 | 0.179 | 0.269 | -0.061 |
| dnabert3_causal_human | 1 | 0.174 | 0.229 | 0.352 | -0.178 |
| dnabert3_causal_human | 3 | 0.224 | 0.218 | 0.340 | -0.116 |
| dnabert3_causal_human | 8 | 0.224 | 0.165 | 0.214 | +0.010 |
| dnabert3_causal_human | 15 | 0.248 | 0.202 | 0.248 | +0.001 |
| dnabert3_causal_human | 30 | 0.502 | 0.202 | 0.165 | +0.337 |
| dnabert3_causal_human | 50 | 0.966 | 0.241 | 0.214 | +0.753 |
| dnabert4_causal_human | 0 | 0.178 | 0.244 | 0.151 | +0.027 |
| dnabert4_causal_human | 1 | 0.278 | 0.250 | 0.277 | +0.001 |
| dnabert4_causal_human | 3 | 0.257 | 0.280 | 0.204 | +0.052 |
| dnabert4_causal_human | 8 | 0.191 | 0.186 | 0.321 | -0.130 |
| dnabert4_causal_human | 15 | 0.257 | 0.171 | 0.209 | +0.048 |
| dnabert4_causal_human | 30 | 0.681 | 0.180 | 0.178 | +0.503 |
| dnabert4_causal_human | 50 | 0.952 | 0.263 | 0.222 | +0.730 |
| dnabert5_causal_human | 0 | 0.220 | 0.191 | 0.235 | -0.015 |
| dnabert5_causal_human | 1 | 0.307 | 0.248 | 0.227 | +0.080 |
| dnabert5_causal_human | 3 | 0.295 | 0.199 | 0.326 | -0.031 |
| dnabert5_causal_human | 8 | 0.286 | 0.168 | 0.293 | -0.007 |
| dnabert5_causal_human | 15 | 0.340 | 0.197 | 0.258 | +0.082 |
| dnabert5_causal_human | 30 | 0.543 | 0.134 | 0.319 | +0.224 |
| dnabert5_causal_human | 50 | 0.937 | 0.256 | 0.244 | +0.693 |
| dnabert6_causal_human | 0 | 0.357 | 0.244 | 0.167 | +0.190 |
| dnabert6_causal_human | 1 | 0.224 | 0.211 | 0.181 | +0.042 |
| dnabert6_causal_human | 3 | 0.236 | 0.277 | 0.270 | -0.034 |
| dnabert6_causal_human | 8 | 0.302 | 0.167 | 0.297 | +0.006 |
| dnabert6_causal_human | 15 | 0.407 | 0.167 | 0.221 | +0.186 |
| dnabert6_causal_human | 30 | 0.826 | 0.179 | 0.237 | +0.589 |
| dnabert6_causal_human | 50 | 0.953 | 0.379 | 0.254 | +0.699 |
| hyena_medium-160k_human | 0 | 0.289 | 0.225 | 0.247 | +0.042 |
| hyena_medium-160k_human | 1 | 0.254 | 0.192 | 0.252 | +0.002 |
| hyena_medium-160k_human | 3 | 0.378 | 0.225 | 0.206 | +0.172 |
| hyena_medium-160k_human | 8 | 0.783 | 0.226 | 0.202 | +0.581 |
| hyena_medium-160k_human | 15 | 0.882 | 0.262 | 0.231 | +0.652 |
| hyena_medium-160k_human | 30 | 0.882 | 0.328 | 0.242 | +0.641 |
| hyena_medium-160k_human | 50 | 0.915 | 0.426 | 0.227 | +0.688 |
