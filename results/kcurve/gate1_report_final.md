# Gate 1 report

root: outputs/kcurve   scores file: scores_final.json
runs: 2mer_ar_s0, 2mer_ar_s1, 2mer_ar_s2, 3mer_ar_s0, 3mer_ar_s1, 3mer_ar_s2, 4mer_ar_s0, 4mer_ar_s1, 4mer_ar_s2, 6mer_ar_s0, 6mer_ar_s1, 6mer_ar_s2, char_ar_s0, char_ar_s1, char_ar_s2

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 2mer_ar_s0 | 2mer | 12.69M (12.61M) | 3330 | 30.7M | 50 | 59 | 0.30 |
| 2mer_ar_s1 | 2mer | 12.69M (12.61M) | 3330 | 30.7M | 42 | 55 | 0.36 |
| 2mer_ar_s2 | 2mer | 12.69M (12.61M) | 3330 | 30.7M | 41 | 56 | 0.36 |
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 41 | 38 | 0.24 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 39 | 38 | 0.25 |
| 3mer_ar_s2 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 41 | 39 | 0.24 |
| 4mer_ar_s0 | 4mer | 12.78M (12.61M) | 3330 | 15.3M | 41 | 30 | 0.18 |
| 4mer_ar_s1 | 4mer | 12.78M (12.61M) | 3330 | 15.3M | 39 | 29 | 0.19 |
| 4mer_ar_s2 | 4mer | 12.78M (12.61M) | 3330 | 15.3M | 40 | 31 | 0.19 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 39 | 23 | 0.15 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 38 | 23 | 0.15 |
| 6mer_ar_s2 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 41 | 22 | 0.14 |
| char_ar_s0 | char | 12.76M (12.61M) | 3330 | 61.3M | 87 | 106 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 3330 | 61.3M | 86 | 106 | 0.35 |
| char_ar_s2 | char | 12.76M (12.61M) | 3330 | 61.3M | 87 | 105 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 2mer_ar_s0 | ar | 3.1728 | 9.0179 | 2.701 | OK |
| 2mer_ar_s1 | ar | 3.1516 | 8.8866 | 2.666 | OK |
| 2mer_ar_s2 | ar | 3.0101 | 8.0562 | 2.409 | OK |
| 3mer_ar_s0 | ar | 4.1222 | 17.4145 | 3.736 | OK |
| 3mer_ar_s1 | ar | 4.1377 | 17.6023 | 3.638 | OK |
| 3mer_ar_s2 | ar | 4.1754 | 18.0690 | 3.651 | OK |
| 4mer_ar_s0 | ar | 3.3949 | 10.5190 | 3.104 | OK |
| 4mer_ar_s1 | ar | 3.4063 | 10.6024 | 3.073 | OK |
| 4mer_ar_s2 | ar | 3.3812 | 10.4196 | 3.053 | OK |
| 6mer_ar_s0 | ar | 2.6377 | 6.2235 | 2.373 | OK |
| 6mer_ar_s1 | ar | 2.6094 | 6.1026 | 2.349 | OK |
| 6mer_ar_s2 | ar | 2.6306 | 6.1928 | 2.388 | OK |
| char_ar_s0 | ar | 2.0420 | 4.1183 | 1.981 | OK |
| char_ar_s1 | ar | 2.0412 | 4.1159 | 1.981 | OK |
| char_ar_s2 | ar | 2.0441 | 4.1241 | 1.976 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 2mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 272 | 0.00 | 0.01 | 3.235 | +0.00 |
| r=1 | 100 | 189 | 0.00 | 0.02 | 3.187 | +0.25 |
| r=4 | 100 | 267 | 0.01 | 0.02 | 3.242 | -0.02 |
| r=16 | 100 | 216 | 0.04 | 0.06 | 3.223 | +0.19 |

### 2mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.843 | +11.56 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.860 | +11.54 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.804 | +11.86 |

### 2mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 254 | 0.00 | 0.00 | 3.239 | -0.05 |
| r=1 | 100 | 286 | 0.01 | 0.01 | 3.232 | -0.06 |
| r=4 | 100 | 254 | 0.00 | 0.00 | 3.240 | -0.09 |
| r=16 | 100 | 221 | 0.00 | 0.01 | 3.198 | +0.04 |

### 2mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.813 | +11.92 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.804 | +11.95 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.806 | +11.89 |

### 2mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 238 | 0.00 | 0.00 | 3.058 | +0.08 |
| r=1 | 100 | 273 | 0.00 | 0.00 | 3.104 | -0.11 |
| r=4 | 100 | 226 | 0.01 | 0.03 | 3.055 | +0.18 |
| r=16 | 100 | 206 | 0.00 | 0.00 | 3.023 | +0.18 |

### 2mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.921 | +10.66 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.926 | +10.63 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.883 | +10.93 |

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 220 | 0.00 | 0.00 | 4.155 | +0.20 |
| r=1 | 100 | 282 | 0.00 | 0.00 | 4.227 | -0.09 |
| r=4 | 100 | 188 | 0.00 | 0.00 | 4.195 | +0.15 |
| r=16 | 100 | 160 | 0.03 | 0.04 | 4.148 | +0.32 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.016 | +17.60 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.019 | +17.53 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.018 | +17.65 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 258 | 0.00 | 0.02 | 4.215 | +0.01 |
| r=1 | 100 | 216 | 0.00 | 0.02 | 4.182 | +0.10 |
| r=4 | 100 | 233 | 0.00 | 0.00 | 4.181 | +0.17 |
| r=16 | 100 | 192 | 0.01 | 0.04 | 4.126 | +0.36 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.013 | +17.54 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.019 | +17.45 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.016 | +17.65 |

### 3mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 233 | 0.02 | 0.02 | 4.259 | +0.08 |
| r=1 | 100 | 202 | 0.01 | 0.02 | 4.210 | +0.20 |
| r=4 | 100 | 238 | 0.00 | 0.00 | 4.262 | -0.01 |
| r=16 | 100 | 249 | 0.00 | 0.04 | 4.261 | +0.09 |

### 3mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.013 | +17.71 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.016 | +17.59 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.013 | +17.71 |

### 4mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 307 | 0.00 | 0.01 | 3.458 | -0.08 |
| r=1 | 100 | 287 | 0.01 | 0.02 | 3.440 | -0.01 |
| r=4 | 100 | 232 | 0.02 | 0.03 | 3.423 | +0.09 |
| r=16 | 100 | 70 | 0.06 | 0.15 | 3.187 | +1.38 |

### 4mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.006 | +18.40 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.009 | +18.36 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.35 |

### 4mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 265 | 0.00 | 0.00 | 3.462 | -0.03 |
| r=1 | 100 | 297 | 0.00 | 0.02 | 3.479 | -0.17 |
| r=4 | 100 | 194 | 0.01 | 0.04 | 3.411 | +0.25 |
| r=16 | 100 | 94 | 0.07 | 0.15 | 3.261 | +1.01 |

### 4mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.006 | +18.43 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.009 | +18.45 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.36 |

### 4mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 192 | 0.00 | 0.02 | 3.394 | +0.18 |
| r=1 | 100 | 272 | 0.01 | 0.01 | 3.411 | +0.03 |
| r=4 | 100 | 215 | 0.02 | 0.05 | 3.364 | +0.30 |
| r=16 | 100 | 102 | 0.08 | 0.15 | 3.232 | +1.00 |

### 4mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.007 | +18.38 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.010 | +18.22 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.42 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 259 | 0.00 | 0.00 | 2.654 | -0.07 |
| r=1 | 100 | 232 | 0.00 | 0.02 | 2.649 | +0.01 |
| r=4 | 100 | 160 | 0.06 | 0.09 | 2.580 | +0.53 |
| r=16 | 100 | 6 | 0.37 | 0.49 | 2.300 | +2.64 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.010 | +19.72 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.012 | +19.72 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.57 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 237 | 0.01 | 0.04 | 2.602 | +0.14 |
| r=1 | 100 | 256 | 0.00 | 0.01 | 2.609 | +0.10 |
| r=4 | 100 | 147 | 0.03 | 0.09 | 2.543 | +0.57 |
| r=16 | 100 | 13 | 0.31 | 0.42 | 2.291 | +2.55 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.012 | +19.86 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.013 | +19.77 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.83 |

### 6mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 254 | 0.00 | 0.00 | 2.640 | -0.01 |
| r=1 | 100 | 246 | 0.00 | 0.00 | 2.636 | +0.03 |
| r=4 | 100 | 117 | 0.06 | 0.13 | 2.533 | +0.83 |
| r=16 | 100 | 3 | 0.45 | 0.58 | 2.269 | +2.79 |

### 6mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.73 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.013 | +19.69 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.68 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 239 | 0.00 | 0.03 | 2.041 | +0.13 |
| r=1 | 100 | 228 | 0.00 | 0.00 | 2.043 | +0.04 |
| r=4 | 100 | 296 | 0.01 | 0.03 | 2.048 | -0.06 |
| r=16 | 100 | 268 | 0.00 | 0.00 | 2.045 | +0.00 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 3 | 0.30 | 0.59 | 1.950 | +2.56 |
| r=4 | 100 | 4 | 0.30 | 0.53 | 1.954 | +2.47 |
| r=16 | 100 | 2 | 0.41 | 0.62 | 1.947 | +2.65 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 238 | 0.00 | 0.00 | 2.042 | +0.03 |
| r=1 | 100 | 244 | 0.00 | 0.01 | 2.043 | -0.04 |
| r=4 | 100 | 272 | 0.00 | 0.00 | 2.050 | -0.19 |
| r=16 | 100 | 290 | 0.01 | 0.02 | 2.044 | -0.03 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 4 | 0.28 | 0.54 | 1.954 | +2.46 |
| r=4 | 100 | 6 | 0.29 | 0.48 | 1.960 | +2.30 |
| r=16 | 100 | 7 | 0.22 | 0.49 | 1.961 | +2.29 |

### char_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 269 | 0.00 | 0.01 | 2.046 | -0.01 |
| r=1 | 100 | 272 | 0.00 | 0.00 | 2.051 | -0.15 |
| r=4 | 100 | 296 | 0.02 | 0.03 | 2.048 | -0.09 |
| r=16 | 100 | 184 | 0.02 | 0.03 | 2.037 | +0.22 |

### char_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 4 | 0.29 | 0.51 | 1.957 | +2.37 |
| r=4 | 100 | 3 | 0.40 | 0.67 | 1.946 | +2.67 |
| r=16 | 100 | 2 | 0.40 | 0.63 | 1.948 | +2.61 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 2mer_ar_s0 | train | r=1 | 100 | 0.00 | 30.3 |
| 2mer_ar_s0 | train | r=4 | 100 | 0.00 | 30.3 |
| 2mer_ar_s0 | train | r=16 | 100 | 0.00 | 30.8 |
| 2mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 2mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.4 |
| 2mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 36.3 |
| 2mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.8 |
| 2mer_ar_s1 | train | r=1 | 100 | 0.00 | 29.6 |
| 2mer_ar_s1 | train | r=4 | 100 | 0.00 | 30.4 |
| 2mer_ar_s1 | train | r=16 | 100 | 0.00 | 29.4 |
| 2mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 2mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.4 |
| 2mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.3 |
| 2mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.2 |
| 2mer_ar_s2 | train | r=1 | 100 | 0.00 | 31.3 |
| 2mer_ar_s2 | train | r=4 | 100 | 0.00 | 31.8 |
| 2mer_ar_s2 | train | r=16 | 100 | 0.00 | 30.2 |
| 2mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.3 |
| 2mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.4 |
| 2mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 2mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.7 |
| 3mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.6 |
| 3mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 35.4 |
| 3mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 3mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.2 |
| 3mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.0 |
| 3mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.7 |
| 3mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 3mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.0 |
| 3mer_ar_s2 | train | r=1 | 100 | 0.99 | 0.3 |
| 3mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.1 |
| 3mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 36.1 |
| 3mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.5 |
| 3mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 4mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.1 |
| 4mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.2 |
| 4mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.6 |
| 4mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.7 |
| 4mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.5 |
| 4mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.5 |
| 4mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.2 |
| 4mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.1 |
| 4mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.2 |
| 4mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 36.0 |
| 4mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.5 |
| 4mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 6mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 6mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 35.7 |
| 6mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.7 |
| 6mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.8 |
| 6mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.4 |
| 6mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 35.2 |
| 6mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 35.6 |
| 6mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.4 |
| 6mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.4 |
| 6mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 6mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.7 |
| char_ar_s0 | train | r=1 | 100 | 0.00 | 34.2 |
| char_ar_s0 | train | r=4 | 100 | 0.00 | 34.5 |
| char_ar_s0 | train | r=16 | 100 | 0.00 | 34.1 |
| char_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.4 |
| char_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=4 | 100 | 0.00 | 36.1 |
| char_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.2 |
| char_ar_s1 | train | r=1 | 100 | 0.00 | 34.0 |
| char_ar_s1 | train | r=4 | 100 | 0.00 | 34.0 |
| char_ar_s1 | train | r=16 | 100 | 0.00 | 34.7 |
| char_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.9 |
| char_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.3 |
| char_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.3 |
| char_ar_s2 | train | r=1 | 100 | 0.00 | 34.6 |
| char_ar_s2 | train | r=4 | 100 | 0.00 | 34.5 |
| char_ar_s2 | train | r=16 | 100 | 0.00 | 34.2 |
| char_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.0 |
| char_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.6 |
| char_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.1 |
| char_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.5 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **2mer_ar_s0** (ar/fresh): bits/nt  r=16 3.223±0.327 | r=1 3.187±0.285 | non-member 3.235±0.267;  rank-1 rate r=16 0.04, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.68e-01, p(r=1 < non-member) = 9.79e-02
- **2mer_ar_s1** (ar/fresh): bits/nt  r=16 3.198±0.219 | r=1 3.232±0.256 | non-member 3.239±0.250;  rank-1 rate r=16 0.00, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 1.27e-01, p(r=1 < non-member) = 5.54e-01
- **2mer_ar_s2** (ar/fresh): bits/nt  r=16 3.023±0.288 | r=1 3.104±0.259 | non-member 3.058±0.245;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.49e-01, p(r=1 < non-member) = 8.40e-01
- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 4.148±0.355 | r=1 4.227±0.236 | non-member 4.155±0.247;  rank-1 rate r=16 0.03, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 5.25e-01, p(r=1 < non-member) = 9.74e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 4.126±0.303 | r=1 4.182±0.287 | non-member 4.215±0.271;  rank-1 rate r=16 0.01, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.09e-02, p(r=1 < non-member) = 2.13e-01
- **3mer_ar_s2** (ar/fresh): bits/nt  r=16 4.261±0.289 | r=1 4.210±0.253 | non-member 4.259±0.273;  rank-1 rate r=16 0.00, r=1 0.01, non-member 0.02;  MWU p(r=16 < non-member) = 5.67e-01, p(r=1 < non-member) = 9.25e-02
- **4mer_ar_s0** (ar/fresh): bits/nt  r=16 3.187±0.366 | r=1 3.440±0.187 | non-member 3.458±0.207;  rank-1 rate r=16 0.06, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 2.81e-12, p(r=1 < non-member) = 1.70e-01
- **4mer_ar_s1** (ar/fresh): bits/nt  r=16 3.261±0.239 | r=1 3.479±0.201 | non-member 3.462±0.175;  rank-1 rate r=16 0.07, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.76e-10, p(r=1 < non-member) = 7.17e-01
- **4mer_ar_s2** (ar/fresh): bits/nt  r=16 3.232±0.274 | r=1 3.411±0.188 | non-member 3.394±0.177;  rank-1 rate r=16 0.08, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 8.86e-06, p(r=1 < non-member) = 8.47e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.300±0.294 | r=1 2.649±0.157 | non-member 2.654±0.125;  rank-1 rate r=16 0.37, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.64e-21, p(r=1 < non-member) = 4.40e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.291±0.267 | r=1 2.609±0.142 | non-member 2.602±0.141;  rank-1 rate r=16 0.31, r=1 0.00, non-member 0.01;  MWU p(r=16 < non-member) = 2.80e-20, p(r=1 < non-member) = 6.35e-01
- **6mer_ar_s2** (ar/fresh): bits/nt  r=16 2.269±0.237 | r=1 2.636±0.133 | non-member 2.640±0.119;  rank-1 rate r=16 0.45, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.84e-24, p(r=1 < non-member) = 4.60e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.045±0.038 | r=1 2.043±0.036 | non-member 2.041±0.037;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 7.57e-01, p(r=1 < non-member) = 5.18e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.044±0.039 | r=1 2.043±0.037 | non-member 2.042±0.040;  rank-1 rate r=16 0.01, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.24e-01, p(r=1 < non-member) = 6.04e-01
- **char_ar_s2** (ar/fresh): bits/nt  r=16 2.037±0.039 | r=1 2.051±0.042 | non-member 2.046±0.037;  rank-1 rate r=16 0.02, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.95e-02, p(r=1 < non-member) = 7.63e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **2mer_ar_s0**: r=16 probe bits/nt 0.804, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **2mer_ar_s1**: r=16 probe bits/nt 0.806, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **2mer_ar_s2**: r=16 probe bits/nt 0.883, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.018, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.016, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s2**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s0**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s1**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s2**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s2**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.947, rank-1 rate 0.41, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.961, rank-1 rate 0.22, exact-extraction rate 0.00
- ar  **char_ar_s2**: r=16 probe bits/nt 1.948, rank-1 rate 0.40, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.