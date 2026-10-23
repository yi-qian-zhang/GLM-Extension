# Rare-allele recovery on real human canaries — human_all4

Canaries: 400 haplotype segments of 96 nt from 1000 Genomes phase 3 (2,548 samples), chr22 (GRCh38), variants with AF <= 0.001 and <= 5 carriers.

`alt` = the individual's rare allele was produced, `ref` = the reference base was produced (the null), `other` = neither. Members are scored in their training host, non-members (r=0) in a fresh host. `bits` = canary bits/nt, `exact` = whole 48-nt continuation correct.

| model | epoch | tier | trials | alt | ref | other | canary bits/nt | exact |
|---|---|---|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | r=0 | 146 | 0.240 | 0.338 | 0.422 | 2.558 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=1 | 125 | 0.215 | 0.366 | 0.419 | 2.518 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=4 | 111 | 0.250 | 0.373 | 0.377 | 2.500 | 0.000 |
| dnabert2bpe_causal_human | 0 | r=16 | 108 | 0.229 | 0.283 | 0.488 | 2.455 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=0 | 146 | 0.256 | 0.307 | 0.437 | 1.896 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=1 | 125 | 0.245 | 0.230 | 0.525 | 1.912 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=4 | 111 | 0.228 | 0.420 | 0.351 | 1.852 | 0.000 |
| dnabert2bpe_causal_human | 1 | r=16 | 108 | 0.263 | 0.322 | 0.415 | 1.858 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=0 | 146 | 0.239 | 0.303 | 0.457 | 1.778 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=1 | 125 | 0.287 | 0.230 | 0.482 | 1.847 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=4 | 111 | 0.213 | 0.324 | 0.463 | 1.682 | 0.000 |
| dnabert2bpe_causal_human | 3 | r=16 | 108 | 0.205 | 0.458 | 0.337 | 1.605 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=0 | 146 | 0.228 | 0.361 | 0.411 | 1.771 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=1 | 125 | 0.229 | 0.350 | 0.421 | 1.736 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=4 | 111 | 0.259 | 0.378 | 0.363 | 1.407 | 0.000 |
| dnabert2bpe_causal_human | 8 | r=16 | 108 | 0.732 | 0.138 | 0.130 | 0.841 | 0.333 |
| dnabert2bpe_causal_human | 15 | r=0 | 146 | 0.302 | 0.326 | 0.372 | 1.839 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=1 | 125 | 0.208 | 0.327 | 0.465 | 1.538 | 0.000 |
| dnabert2bpe_causal_human | 15 | r=4 | 111 | 0.485 | 0.185 | 0.329 | 1.082 | 0.117 |
| dnabert2bpe_causal_human | 15 | r=16 | 108 | 1.000 | 0.000 | 0.000 | 0.286 | 0.883 |
| dnabert2bpe_causal_human | 30 | r=0 | 146 | 0.249 | 0.300 | 0.451 | 2.053 | 0.000 |
| dnabert2bpe_causal_human | 30 | r=1 | 125 | 0.461 | 0.168 | 0.371 | 0.887 | 0.100 |
| dnabert2bpe_causal_human | 30 | r=4 | 111 | 0.831 | 0.048 | 0.122 | 0.340 | 0.550 |
| dnabert2bpe_causal_human | 30 | r=16 | 108 | 1.000 | 0.000 | 0.000 | 0.121 | 1.000 |
| dnabert2bpe_causal_human | 50 | r=0 | 596 | 0.265 | 0.332 | 0.403 | 2.406 | 0.000 |
| dnabert2bpe_causal_human | 50 | r=1 | 542 | 0.850 | 0.063 | 0.087 | 0.197 | 0.577 |
| dnabert2bpe_causal_human | 50 | r=4 | 528 | 1.000 | 0.000 | 0.000 | 0.055 | 0.997 |
| dnabert2bpe_causal_human | 50 | r=16 | 565 | 1.000 | 0.000 | 0.000 | 0.029 | 1.000 |
| dnabert3_causal_human | 0 | r=0 | 145 | 0.271 | 0.299 | 0.430 | 3.004 | 0.000 |
| dnabert3_causal_human | 0 | r=1 | 125 | 0.256 | 0.209 | 0.534 | 2.781 | 0.000 |
| dnabert3_causal_human | 0 | r=4 | 108 | 0.240 | 0.273 | 0.488 | 2.898 | 0.000 |
| dnabert3_causal_human | 0 | r=16 | 107 | 0.291 | 0.231 | 0.478 | 2.846 | 0.000 |
| dnabert3_causal_human | 1 | r=0 | 145 | 0.313 | 0.207 | 0.480 | 1.957 | 0.000 |
| dnabert3_causal_human | 1 | r=1 | 125 | 0.273 | 0.242 | 0.485 | 1.938 | 0.000 |
| dnabert3_causal_human | 1 | r=4 | 108 | 0.296 | 0.256 | 0.448 | 1.950 | 0.000 |
| dnabert3_causal_human | 1 | r=16 | 107 | 0.264 | 0.285 | 0.451 | 1.973 | 0.000 |
| dnabert3_causal_human | 3 | r=0 | 145 | 0.337 | 0.227 | 0.437 | 1.946 | 0.000 |
| dnabert3_causal_human | 3 | r=1 | 125 | 0.244 | 0.224 | 0.532 | 1.911 | 0.000 |
| dnabert3_causal_human | 3 | r=4 | 108 | 0.231 | 0.344 | 0.425 | 1.910 | 0.000 |
| dnabert3_causal_human | 3 | r=16 | 107 | 0.289 | 0.308 | 0.403 | 1.930 | 0.000 |
| dnabert3_causal_human | 8 | r=0 | 145 | 0.220 | 0.408 | 0.372 | 1.767 | 0.000 |
| dnabert3_causal_human | 8 | r=1 | 125 | 0.225 | 0.255 | 0.519 | 1.879 | 0.000 |
| dnabert3_causal_human | 8 | r=4 | 108 | 0.185 | 0.438 | 0.377 | 1.752 | 0.000 |
| dnabert3_causal_human | 8 | r=16 | 107 | 0.279 | 0.474 | 0.247 | 1.583 | 0.000 |
| dnabert3_causal_human | 15 | r=0 | 145 | 0.207 | 0.418 | 0.375 | 1.736 | 0.000 |
| dnabert3_causal_human | 15 | r=1 | 125 | 0.228 | 0.293 | 0.479 | 1.823 | 0.000 |
| dnabert3_causal_human | 15 | r=4 | 108 | 0.190 | 0.460 | 0.350 | 1.658 | 0.000 |
| dnabert3_causal_human | 15 | r=16 | 107 | 0.374 | 0.447 | 0.179 | 1.315 | 0.067 |
| dnabert3_causal_human | 30 | r=0 | 145 | 0.172 | 0.434 | 0.394 | 1.768 | 0.000 |
| dnabert3_causal_human | 30 | r=1 | 125 | 0.212 | 0.301 | 0.487 | 1.736 | 0.000 |
| dnabert3_causal_human | 30 | r=4 | 108 | 0.244 | 0.419 | 0.337 | 1.483 | 0.000 |
| dnabert3_causal_human | 30 | r=16 | 107 | 0.657 | 0.175 | 0.168 | 0.837 | 0.417 |
| dnabert3_causal_human | 50 | r=0 | 595 | 0.239 | 0.424 | 0.337 | 1.845 | 0.000 |
| dnabert3_causal_human | 50 | r=1 | 542 | 0.267 | 0.361 | 0.372 | 1.446 | 0.000 |
| dnabert3_causal_human | 50 | r=4 | 525 | 0.439 | 0.291 | 0.270 | 1.185 | 0.077 |
| dnabert3_causal_human | 50 | r=16 | 564 | 0.981 | 0.009 | 0.009 | 0.364 | 0.953 |
| dnabert4_causal_human | 0 | r=0 | 145 | 0.177 | 0.293 | 0.530 | 2.572 | 0.000 |
| dnabert4_causal_human | 0 | r=1 | 125 | 0.241 | 0.169 | 0.590 | 2.574 | 0.000 |
| dnabert4_causal_human | 0 | r=4 | 108 | 0.248 | 0.279 | 0.473 | 2.708 | 0.000 |
| dnabert4_causal_human | 0 | r=16 | 107 | 0.245 | 0.295 | 0.459 | 2.551 | 0.000 |
| dnabert4_causal_human | 1 | r=0 | 145 | 0.281 | 0.229 | 0.490 | 1.997 | 0.000 |
| dnabert4_causal_human | 1 | r=1 | 125 | 0.260 | 0.217 | 0.523 | 1.955 | 0.000 |
| dnabert4_causal_human | 1 | r=4 | 108 | 0.344 | 0.181 | 0.475 | 1.979 | 0.000 |
| dnabert4_causal_human | 1 | r=16 | 107 | 0.243 | 0.202 | 0.555 | 1.970 | 0.000 |
| dnabert4_causal_human | 3 | r=0 | 145 | 0.322 | 0.314 | 0.364 | 1.947 | 0.000 |
| dnabert4_causal_human | 3 | r=1 | 125 | 0.251 | 0.239 | 0.510 | 1.905 | 0.000 |
| dnabert4_causal_human | 3 | r=4 | 108 | 0.233 | 0.298 | 0.469 | 1.895 | 0.000 |
| dnabert4_causal_human | 3 | r=16 | 107 | 0.316 | 0.281 | 0.403 | 1.913 | 0.000 |
| dnabert4_causal_human | 8 | r=0 | 145 | 0.280 | 0.326 | 0.394 | 1.837 | 0.000 |
| dnabert4_causal_human | 8 | r=1 | 125 | 0.212 | 0.255 | 0.533 | 1.884 | 0.000 |
| dnabert4_causal_human | 8 | r=4 | 108 | 0.196 | 0.510 | 0.294 | 1.756 | 0.000 |
| dnabert4_causal_human | 8 | r=16 | 107 | 0.231 | 0.462 | 0.307 | 1.615 | 0.000 |
| dnabert4_causal_human | 15 | r=0 | 145 | 0.224 | 0.443 | 0.333 | 1.831 | 0.000 |
| dnabert4_causal_human | 15 | r=1 | 125 | 0.197 | 0.253 | 0.551 | 1.829 | 0.000 |
| dnabert4_causal_human | 15 | r=4 | 108 | 0.194 | 0.415 | 0.392 | 1.636 | 0.000 |
| dnabert4_causal_human | 15 | r=16 | 107 | 0.326 | 0.447 | 0.226 | 1.385 | 0.033 |
| dnabert4_causal_human | 30 | r=0 | 145 | 0.214 | 0.470 | 0.316 | 1.871 | 0.000 |
| dnabert4_causal_human | 30 | r=1 | 125 | 0.201 | 0.310 | 0.489 | 1.765 | 0.000 |
| dnabert4_causal_human | 30 | r=4 | 108 | 0.221 | 0.483 | 0.296 | 1.451 | 0.000 |
| dnabert4_causal_human | 30 | r=16 | 107 | 0.778 | 0.118 | 0.104 | 0.866 | 0.433 |
| dnabert4_causal_human | 50 | r=0 | 595 | 0.227 | 0.438 | 0.335 | 1.903 | 0.000 |
| dnabert4_causal_human | 50 | r=1 | 542 | 0.263 | 0.344 | 0.392 | 1.462 | 0.000 |
| dnabert4_causal_human | 50 | r=4 | 525 | 0.499 | 0.236 | 0.265 | 1.213 | 0.070 |
| dnabert4_causal_human | 50 | r=16 | 564 | 0.967 | 0.014 | 0.018 | 0.394 | 0.867 |
| dnabert5_causal_human | 0 | r=0 | 145 | 0.236 | 0.289 | 0.475 | 3.073 | 0.000 |
| dnabert5_causal_human | 0 | r=1 | 125 | 0.238 | 0.176 | 0.586 | 2.942 | 0.000 |
| dnabert5_causal_human | 0 | r=4 | 108 | 0.317 | 0.250 | 0.433 | 3.202 | 0.000 |
| dnabert5_causal_human | 0 | r=16 | 107 | 0.391 | 0.156 | 0.453 | 3.020 | 0.000 |
| dnabert5_causal_human | 1 | r=0 | 145 | 0.209 | 0.243 | 0.548 | 2.064 | 0.000 |
| dnabert5_causal_human | 1 | r=1 | 125 | 0.227 | 0.281 | 0.491 | 2.074 | 0.000 |
| dnabert5_causal_human | 1 | r=4 | 108 | 0.237 | 0.308 | 0.454 | 2.073 | 0.000 |
| dnabert5_causal_human | 1 | r=16 | 107 | 0.341 | 0.239 | 0.420 | 2.053 | 0.000 |
| dnabert5_causal_human | 3 | r=0 | 145 | 0.300 | 0.275 | 0.426 | 1.880 | 0.000 |
| dnabert5_causal_human | 3 | r=1 | 125 | 0.258 | 0.259 | 0.483 | 1.875 | 0.000 |
| dnabert5_causal_human | 3 | r=4 | 108 | 0.250 | 0.348 | 0.402 | 1.865 | 0.000 |
| dnabert5_causal_human | 3 | r=16 | 107 | 0.304 | 0.377 | 0.320 | 1.808 | 0.000 |
| dnabert5_causal_human | 8 | r=0 | 145 | 0.325 | 0.300 | 0.375 | 1.829 | 0.000 |
| dnabert5_causal_human | 8 | r=1 | 125 | 0.179 | 0.242 | 0.578 | 1.838 | 0.000 |
| dnabert5_causal_human | 8 | r=4 | 108 | 0.181 | 0.410 | 0.408 | 1.727 | 0.000 |
| dnabert5_causal_human | 8 | r=16 | 107 | 0.289 | 0.447 | 0.264 | 1.588 | 0.000 |
| dnabert5_causal_human | 15 | r=0 | 145 | 0.284 | 0.326 | 0.390 | 1.805 | 0.000 |
| dnabert5_causal_human | 15 | r=1 | 125 | 0.210 | 0.265 | 0.526 | 1.826 | 0.000 |
| dnabert5_causal_human | 15 | r=4 | 108 | 0.190 | 0.404 | 0.406 | 1.653 | 0.000 |
| dnabert5_causal_human | 15 | r=16 | 107 | 0.378 | 0.458 | 0.164 | 1.341 | 0.000 |
| dnabert5_causal_human | 30 | r=0 | 145 | 0.261 | 0.408 | 0.331 | 1.839 | 0.000 |
| dnabert5_causal_human | 30 | r=1 | 125 | 0.202 | 0.327 | 0.472 | 1.736 | 0.000 |
| dnabert5_causal_human | 30 | r=4 | 108 | 0.227 | 0.427 | 0.346 | 1.462 | 0.000 |
| dnabert5_causal_human | 30 | r=16 | 107 | 0.699 | 0.193 | 0.108 | 0.852 | 0.367 |
| dnabert5_causal_human | 50 | r=0 | 595 | 0.236 | 0.407 | 0.357 | 1.915 | 0.000 |
| dnabert5_causal_human | 50 | r=1 | 542 | 0.284 | 0.340 | 0.376 | 1.435 | 0.000 |
| dnabert5_causal_human | 50 | r=4 | 525 | 0.476 | 0.253 | 0.271 | 1.172 | 0.070 |
| dnabert5_causal_human | 50 | r=16 | 564 | 0.917 | 0.037 | 0.046 | 0.418 | 0.747 |
| dnabert6_causal_human | 0 | r=0 | 145 | 0.179 | 0.291 | 0.530 | 4.936 | 0.000 |
| dnabert6_causal_human | 0 | r=1 | 125 | 0.336 | 0.208 | 0.456 | 4.436 | 0.000 |
| dnabert6_causal_human | 0 | r=4 | 108 | 0.454 | 0.210 | 0.335 | 4.555 | 0.000 |
| dnabert6_causal_human | 0 | r=16 | 107 | 0.335 | 0.247 | 0.418 | 4.658 | 0.000 |
| dnabert6_causal_human | 1 | r=0 | 145 | 0.210 | 0.209 | 0.581 | 1.974 | 0.000 |
| dnabert6_causal_human | 1 | r=1 | 125 | 0.272 | 0.241 | 0.487 | 2.010 | 0.000 |
| dnabert6_causal_human | 1 | r=4 | 108 | 0.367 | 0.179 | 0.454 | 1.974 | 0.000 |
| dnabert6_causal_human | 1 | r=16 | 107 | 0.299 | 0.216 | 0.485 | 1.936 | 0.000 |
| dnabert6_causal_human | 3 | r=0 | 145 | 0.284 | 0.286 | 0.430 | 1.871 | 0.000 |
| dnabert6_causal_human | 3 | r=1 | 125 | 0.265 | 0.253 | 0.482 | 1.864 | 0.000 |
| dnabert6_causal_human | 3 | r=4 | 108 | 0.190 | 0.496 | 0.315 | 1.774 | 0.000 |
| dnabert6_causal_human | 3 | r=16 | 107 | 0.306 | 0.426 | 0.268 | 1.661 | 0.000 |
| dnabert6_causal_human | 8 | r=0 | 145 | 0.256 | 0.420 | 0.325 | 1.789 | 0.000 |
| dnabert6_causal_human | 8 | r=1 | 125 | 0.242 | 0.312 | 0.446 | 1.808 | 0.000 |
| dnabert6_causal_human | 8 | r=4 | 108 | 0.223 | 0.379 | 0.398 | 1.660 | 0.000 |
| dnabert6_causal_human | 8 | r=16 | 107 | 0.380 | 0.468 | 0.152 | 1.341 | 0.017 |
| dnabert6_causal_human | 15 | r=0 | 145 | 0.194 | 0.466 | 0.340 | 1.795 | 0.000 |
| dnabert6_causal_human | 15 | r=1 | 125 | 0.203 | 0.295 | 0.503 | 1.751 | 0.000 |
| dnabert6_causal_human | 15 | r=4 | 108 | 0.240 | 0.402 | 0.358 | 1.546 | 0.000 |
| dnabert6_causal_human | 15 | r=16 | 107 | 0.589 | 0.316 | 0.095 | 1.066 | 0.217 |
| dnabert6_causal_human | 30 | r=0 | 145 | 0.214 | 0.431 | 0.355 | 1.890 | 0.000 |
| dnabert6_causal_human | 30 | r=1 | 125 | 0.256 | 0.318 | 0.426 | 1.618 | 0.000 |
| dnabert6_causal_human | 30 | r=4 | 108 | 0.358 | 0.321 | 0.321 | 1.283 | 0.050 |
| dnabert6_causal_human | 30 | r=16 | 107 | 0.871 | 0.073 | 0.056 | 0.592 | 0.517 |
| dnabert6_causal_human | 50 | r=0 | 595 | 0.235 | 0.399 | 0.366 | 1.985 | 0.000 |
| dnabert6_causal_human | 50 | r=1 | 542 | 0.385 | 0.283 | 0.332 | 1.231 | 0.043 |
| dnabert6_causal_human | 50 | r=4 | 525 | 0.643 | 0.151 | 0.206 | 0.877 | 0.177 |
| dnabert6_causal_human | 50 | r=16 | 564 | 0.956 | 0.021 | 0.023 | 0.287 | 0.867 |
| hyena_medium-160k_human | 0 | r=0 | 595 | 0.239 | 0.351 | 0.410 | 1.763 | 0.000 |
| hyena_medium-160k_human | 0 | r=1 | 542 | 0.199 | 0.348 | 0.454 | 1.763 | 0.000 |
| hyena_medium-160k_human | 0 | r=4 | 525 | 0.244 | 0.321 | 0.435 | 1.729 | 0.000 |
| hyena_medium-160k_human | 0 | r=16 | 564 | 0.232 | 0.353 | 0.415 | 1.765 | 0.000 |
| hyena_medium-160k_human | 1 | r=0 | 595 | 0.242 | 0.367 | 0.391 | 1.743 | 0.000 |
| hyena_medium-160k_human | 1 | r=1 | 542 | 0.195 | 0.351 | 0.454 | 1.729 | 0.000 |
| hyena_medium-160k_human | 1 | r=4 | 525 | 0.271 | 0.356 | 0.374 | 1.684 | 0.000 |
| hyena_medium-160k_human | 1 | r=16 | 564 | 0.242 | 0.390 | 0.367 | 1.669 | 0.000 |
| hyena_medium-160k_human | 3 | r=0 | 595 | 0.227 | 0.389 | 0.384 | 1.733 | 0.000 |
| hyena_medium-160k_human | 3 | r=1 | 542 | 0.226 | 0.345 | 0.429 | 1.696 | 0.000 |
| hyena_medium-160k_human | 3 | r=4 | 525 | 0.268 | 0.355 | 0.378 | 1.614 | 0.000 |
| hyena_medium-160k_human | 3 | r=16 | 564 | 0.364 | 0.327 | 0.308 | 1.395 | 0.020 |
| hyena_medium-160k_human | 8 | r=0 | 595 | 0.220 | 0.407 | 0.373 | 1.730 | 0.000 |
| hyena_medium-160k_human | 8 | r=1 | 542 | 0.226 | 0.362 | 0.412 | 1.598 | 0.000 |
| hyena_medium-160k_human | 8 | r=4 | 525 | 0.348 | 0.332 | 0.320 | 1.389 | 0.007 |
| hyena_medium-160k_human | 8 | r=16 | 564 | 0.749 | 0.175 | 0.076 | 0.467 | 0.460 |
| hyena_medium-160k_human | 15 | r=0 | 595 | 0.227 | 0.388 | 0.385 | 1.773 | 0.000 |
| hyena_medium-160k_human | 15 | r=1 | 542 | 0.258 | 0.368 | 0.373 | 1.474 | 0.000 |
| hyena_medium-160k_human | 15 | r=4 | 525 | 0.531 | 0.232 | 0.237 | 1.037 | 0.043 |
| hyena_medium-160k_human | 15 | r=16 | 564 | 0.847 | 0.134 | 0.019 | 0.288 | 0.673 |
| hyena_medium-160k_human | 30 | r=0 | 595 | 0.253 | 0.373 | 0.374 | 1.961 | 0.000 |
| hyena_medium-160k_human | 30 | r=1 | 542 | 0.326 | 0.306 | 0.367 | 1.213 | 0.003 |
| hyena_medium-160k_human | 30 | r=4 | 525 | 0.654 | 0.185 | 0.161 | 0.624 | 0.143 |
| hyena_medium-160k_human | 30 | r=16 | 564 | 0.879 | 0.093 | 0.028 | 0.198 | 0.757 |
| hyena_medium-160k_human | 50 | r=0 | 595 | 0.242 | 0.353 | 0.404 | 2.528 | 0.000 |
| hyena_medium-160k_human | 50 | r=1 | 542 | 0.446 | 0.275 | 0.279 | 0.919 | 0.030 |
| hyena_medium-160k_human | 50 | r=4 | 525 | 0.726 | 0.160 | 0.115 | 0.373 | 0.260 |
| hyena_medium-160k_human | 50 | r=16 | 564 | 0.921 | 0.057 | 0.022 | 0.138 | 0.817 |

## Leakage: member minus non-member rare-allele recovery

| model | epoch | r=16 alt | r=1 alt | non-member alt | gap (r=16 - non-member) |
|---|---|---|---|---|---|
| dnabert2bpe_causal_human | 0 | 0.229 | 0.215 | 0.240 | -0.011 |
| dnabert2bpe_causal_human | 1 | 0.263 | 0.245 | 0.256 | +0.007 |
| dnabert2bpe_causal_human | 3 | 0.205 | 0.287 | 0.239 | -0.034 |
| dnabert2bpe_causal_human | 8 | 0.732 | 0.229 | 0.228 | +0.505 |
| dnabert2bpe_causal_human | 15 | 1.000 | 0.208 | 0.302 | +0.698 |
| dnabert2bpe_causal_human | 30 | 1.000 | 0.461 | 0.249 | +0.751 |
| dnabert2bpe_causal_human | 50 | 1.000 | 0.850 | 0.265 | +0.735 |
| dnabert3_causal_human | 0 | 0.291 | 0.256 | 0.271 | +0.020 |
| dnabert3_causal_human | 1 | 0.264 | 0.273 | 0.313 | -0.049 |
| dnabert3_causal_human | 3 | 0.289 | 0.244 | 0.337 | -0.048 |
| dnabert3_causal_human | 8 | 0.279 | 0.225 | 0.220 | +0.059 |
| dnabert3_causal_human | 15 | 0.374 | 0.228 | 0.207 | +0.167 |
| dnabert3_causal_human | 30 | 0.657 | 0.212 | 0.172 | +0.485 |
| dnabert3_causal_human | 50 | 0.981 | 0.267 | 0.239 | +0.743 |
| dnabert4_causal_human | 0 | 0.245 | 0.241 | 0.177 | +0.069 |
| dnabert4_causal_human | 1 | 0.243 | 0.260 | 0.281 | -0.038 |
| dnabert4_causal_human | 3 | 0.316 | 0.251 | 0.322 | -0.006 |
| dnabert4_causal_human | 8 | 0.231 | 0.212 | 0.280 | -0.049 |
| dnabert4_causal_human | 15 | 0.326 | 0.197 | 0.224 | +0.103 |
| dnabert4_causal_human | 30 | 0.778 | 0.201 | 0.214 | +0.564 |
| dnabert4_causal_human | 50 | 0.967 | 0.263 | 0.227 | +0.741 |
| dnabert5_causal_human | 0 | 0.391 | 0.238 | 0.236 | +0.155 |
| dnabert5_causal_human | 1 | 0.341 | 0.227 | 0.209 | +0.132 |
| dnabert5_causal_human | 3 | 0.304 | 0.258 | 0.300 | +0.004 |
| dnabert5_causal_human | 8 | 0.289 | 0.179 | 0.325 | -0.036 |
| dnabert5_causal_human | 15 | 0.378 | 0.210 | 0.284 | +0.095 |
| dnabert5_causal_human | 30 | 0.699 | 0.202 | 0.261 | +0.438 |
| dnabert5_causal_human | 50 | 0.917 | 0.284 | 0.236 | +0.681 |
| dnabert6_causal_human | 0 | 0.335 | 0.336 | 0.179 | +0.156 |
| dnabert6_causal_human | 1 | 0.299 | 0.272 | 0.210 | +0.090 |
| dnabert6_causal_human | 3 | 0.306 | 0.265 | 0.284 | +0.022 |
| dnabert6_causal_human | 8 | 0.380 | 0.242 | 0.256 | +0.125 |
| dnabert6_causal_human | 15 | 0.589 | 0.203 | 0.194 | +0.395 |
| dnabert6_causal_human | 30 | 0.871 | 0.256 | 0.214 | +0.657 |
| dnabert6_causal_human | 50 | 0.956 | 0.385 | 0.235 | +0.721 |
| hyena_medium-160k_human | 0 | 0.232 | 0.199 | 0.239 | -0.007 |
| hyena_medium-160k_human | 1 | 0.242 | 0.195 | 0.242 | +0.000 |
| hyena_medium-160k_human | 3 | 0.364 | 0.226 | 0.227 | +0.137 |
| hyena_medium-160k_human | 8 | 0.749 | 0.226 | 0.220 | +0.529 |
| hyena_medium-160k_human | 15 | 0.847 | 0.258 | 0.227 | +0.620 |
| hyena_medium-160k_human | 30 | 0.879 | 0.326 | 0.253 | +0.627 |
| hyena_medium-160k_human | 50 | 0.921 | 0.446 | 0.242 | +0.679 |
