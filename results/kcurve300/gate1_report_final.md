# Gate 1 report

root: outputs/kcurve300   scores file: scores_final.json
runs: 2mer_ar_s0, 2mer_ar_s1, 2mer_ar_s2, 3mer_ar_s0, 3mer_ar_s1, 3mer_ar_s2, 4mer_ar_s0, 4mer_ar_s1, 4mer_ar_s2, 5mer_ar_s0, 5mer_ar_s1, 5mer_ar_s2, 6mer_ar_s0, 6mer_ar_s1, 6mer_ar_s2, char_ar_s0, char_ar_s1, char_ar_s2

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 2mer_ar_s0 | 2mer | 12.70M (12.61M) | 3330 | 31.9M | 46 | 57 | 0.33 |
| 2mer_ar_s1 | 2mer | 12.70M (12.61M) | 3330 | 31.9M | 47 | 58 | 0.32 |
| 2mer_ar_s2 | 2mer | 12.70M (12.61M) | 3330 | 31.9M | 45 | 58 | 0.33 |
| 3mer_ar_s0 | 3mer | 12.70M (12.61M) | 3330 | 21.3M | 40 | 40 | 0.27 |
| 3mer_ar_s1 | 3mer | 12.70M (12.61M) | 3330 | 21.3M | 40 | 41 | 0.26 |
| 3mer_ar_s2 | 3mer | 12.70M (12.61M) | 3330 | 21.3M | 41 | 40 | 0.25 |
| 4mer_ar_s0 | 4mer | 12.78M (12.61M) | 3330 | 16.0M | 40 | 30 | 0.20 |
| 4mer_ar_s1 | 4mer | 12.78M (12.61M) | 3330 | 16.0M | 39 | 31 | 0.20 |
| 4mer_ar_s2 | 4mer | 12.78M (12.61M) | 3330 | 16.0M | 41 | 31 | 0.19 |
| 5mer_ar_s0 | 5mer | 13.17M (12.61M) | 3330 | 12.8M | 37 | 26 | 0.17 |
| 5mer_ar_s1 | 5mer | 13.17M (12.61M) | 3330 | 12.8M | 39 | 25 | 0.16 |
| 5mer_ar_s2 | 5mer | 13.17M (12.61M) | 3330 | 12.8M | 40 | 26 | 0.16 |
| 6mer_ar_s0 | 6mer | 14.74M (12.61M) | 3330 | 10.7M | 41 | 24 | 0.14 |
| 6mer_ar_s1 | 6mer | 14.74M (12.61M) | 3330 | 10.7M | 42 | 24 | 0.15 |
| 6mer_ar_s2 | 6mer | 14.74M (12.61M) | 3330 | 10.7M | 39 | 23 | 0.15 |
| char_ar_s0 | char | 12.77M (12.61M) | 3330 | 63.9M | 93 | 107 | 0.32 |
| char_ar_s1 | char | 12.77M (12.61M) | 3330 | 63.9M | 92 | 108 | 0.33 |
| char_ar_s2 | char | 12.77M (12.61M) | 3330 | 63.9M | 92 | 107 | 0.33 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 2mer_ar_s0 | ar | 3.0707 | 8.4019 | 2.506 | OK |
| 2mer_ar_s1 | ar | 3.1386 | 8.8064 | 2.645 | OK |
| 2mer_ar_s2 | ar | 3.1678 | 8.9867 | 2.598 | OK |
| 3mer_ar_s0 | ar | 4.0048 | 16.0532 | 3.519 | OK |
| 3mer_ar_s1 | ar | 4.0904 | 17.0351 | 3.712 | OK |
| 3mer_ar_s2 | ar | 4.1031 | 17.1851 | 3.683 | OK |
| 4mer_ar_s0 | ar | 3.4016 | 10.5675 | 3.045 | OK |
| 4mer_ar_s1 | ar | 3.4076 | 10.6121 | 3.115 | OK |
| 4mer_ar_s2 | ar | 3.3846 | 10.4439 | 3.022 | OK |
| 5mer_ar_s0 | ar | 2.8414 | 7.1673 | 2.554 | OK |
| 5mer_ar_s1 | ar | 2.8558 | 7.2389 | 2.559 | OK |
| 5mer_ar_s2 | ar | 2.8404 | 7.1624 | 2.592 | OK |
| 6mer_ar_s0 | ar | 2.6288 | 6.1849 | 2.373 | OK |
| 6mer_ar_s1 | ar | 2.6269 | 6.1770 | 2.363 | OK |
| 6mer_ar_s2 | ar | 2.6200 | 6.1475 | 2.343 | OK |
| char_ar_s0 | ar | 2.0412 | 4.1159 | 1.983 | OK |
| char_ar_s1 | ar | 2.0411 | 4.1157 | 1.978 | OK |
| char_ar_s2 | ar | 2.0437 | 4.1229 | 1.982 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 2mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 300 | 0.02 | 0.02 | 3.166 | -0.14 |
| r=1 | 100 | 289 | 0.00 | 0.01 | 3.136 | -0.08 |
| r=4 | 100 | 213 | 0.01 | 0.02 | 3.109 | +0.14 |
| r=16 | 100 | 200 | 0.01 | 0.04 | 3.103 | +0.18 |

### 2mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.881 | +11.08 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.886 | +11.18 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.893 | +10.92 |

### 2mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 248 | 0.00 | 0.01 | 3.207 | +0.05 |
| r=1 | 100 | 212 | 0.01 | 0.06 | 3.126 | +0.26 |
| r=4 | 100 | 244 | 0.01 | 0.01 | 3.212 | +0.01 |
| r=16 | 100 | 219 | 0.00 | 0.00 | 3.194 | +0.11 |

### 2mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.857 | +11.45 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.858 | +11.61 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.834 | +11.61 |

### 2mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 280 | 0.00 | 0.01 | 3.257 | -0.04 |
| r=1 | 100 | 246 | 0.01 | 0.01 | 3.218 | +0.06 |
| r=4 | 100 | 255 | 0.00 | 0.00 | 3.202 | +0.00 |
| r=16 | 100 | 219 | 0.00 | 0.01 | 3.205 | +0.15 |

### 2mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.823 | +11.73 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.824 | +11.71 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.806 | +11.82 |

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 343 | 0.00 | 0.00 | 4.187 | -0.37 |
| r=1 | 100 | 266 | 0.00 | 0.00 | 4.112 | -0.06 |
| r=4 | 100 | 254 | 0.00 | 0.02 | 4.114 | +0.07 |
| r=16 | 100 | 178 | 0.02 | 0.03 | 4.009 | +0.45 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.027 | +17.49 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.017 | +17.56 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.027 | +17.46 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 229 | 0.00 | 0.00 | 4.152 | +0.04 |
| r=1 | 100 | 250 | 0.00 | 0.00 | 4.179 | -0.18 |
| r=4 | 100 | 208 | 0.01 | 0.01 | 4.134 | +0.10 |
| r=16 | 100 | 217 | 0.00 | 0.00 | 4.146 | +0.02 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.017 | +17.58 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.014 | +17.70 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.020 | +17.66 |

### 3mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 288 | 0.00 | 0.00 | 4.193 | -0.06 |
| r=1 | 100 | 240 | 0.00 | 0.02 | 4.151 | +0.08 |
| r=4 | 100 | 222 | 0.00 | 0.01 | 4.180 | +0.03 |
| r=16 | 100 | 210 | 0.00 | 0.02 | 4.126 | +0.25 |

### 3mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.018 | +17.54 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.014 | +17.71 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.017 | +17.62 |

### 4mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 271 | 0.01 | 0.02 | 3.439 | -0.02 |
| r=1 | 100 | 206 | 0.01 | 0.02 | 3.418 | +0.09 |
| r=4 | 100 | 210 | 0.00 | 0.02 | 3.403 | +0.20 |
| r=16 | 100 | 82 | 0.11 | 0.20 | 3.197 | +1.33 |

### 4mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.006 | +18.37 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.004 | +18.35 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.34 |

### 4mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 286 | 0.00 | 0.00 | 3.478 | -0.12 |
| r=1 | 100 | 244 | 0.00 | 0.00 | 3.456 | -0.08 |
| r=4 | 100 | 194 | 0.01 | 0.01 | 3.385 | +0.36 |
| r=16 | 100 | 72 | 0.06 | 0.15 | 3.244 | +1.10 |

### 4mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.006 | +18.44 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.004 | +18.33 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.41 |

### 4mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 256 | 0.01 | 0.01 | 3.439 | -0.00 |
| r=1 | 100 | 253 | 0.00 | 0.02 | 3.432 | -0.02 |
| r=4 | 100 | 189 | 0.00 | 0.00 | 3.371 | +0.34 |
| r=16 | 100 | 89 | 0.09 | 0.21 | 3.224 | +1.14 |

### 4mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.007 | +18.42 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.004 | +18.33 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.35 |

### 5mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 232 | 0.00 | 0.00 | 2.848 | +0.05 |
| r=1 | 100 | 218 | 0.00 | 0.00 | 2.828 | +0.20 |
| r=4 | 100 | 197 | 0.02 | 0.04 | 2.815 | +0.28 |
| r=16 | 100 | 17 | 0.23 | 0.36 | 2.532 | +2.17 |

### 5mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.85 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.007 | +18.73 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +18.78 |

### 5mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 284 | 0.00 | 0.00 | 2.899 | -0.20 |
| r=1 | 100 | 218 | 0.00 | 0.01 | 2.841 | +0.17 |
| r=4 | 100 | 184 | 0.01 | 0.06 | 2.810 | +0.39 |
| r=16 | 100 | 34 | 0.21 | 0.34 | 2.599 | +1.77 |

### 5mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.008 | +18.76 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.007 | +18.77 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +18.71 |

### 5mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 200 | 0.00 | 0.01 | 2.841 | +0.11 |
| r=1 | 100 | 239 | 0.00 | 0.01 | 2.849 | +0.06 |
| r=4 | 100 | 172 | 0.03 | 0.04 | 2.796 | +0.42 |
| r=16 | 100 | 32 | 0.19 | 0.32 | 2.589 | +1.77 |

### 5mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.009 | +18.88 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.007 | +18.77 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +18.72 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 248 | 0.00 | 0.00 | 2.637 | -0.04 |
| r=1 | 100 | 212 | 0.00 | 0.01 | 2.610 | +0.17 |
| r=4 | 100 | 125 | 0.01 | 0.04 | 2.549 | +0.64 |
| r=16 | 100 | 7 | 0.36 | 0.48 | 2.295 | +2.58 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.71 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.008 | +19.71 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.71 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 258 | 0.00 | 0.01 | 2.647 | -0.09 |
| r=1 | 100 | 254 | 0.02 | 0.03 | 2.631 | +0.02 |
| r=4 | 100 | 138 | 0.05 | 0.08 | 2.553 | +0.65 |
| r=16 | 100 | 8 | 0.36 | 0.48 | 2.302 | +2.53 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.62 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.009 | +19.83 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.012 | +19.63 |

### 6mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 256 | 0.01 | 0.02 | 2.640 | -0.05 |
| r=1 | 100 | 252 | 0.01 | 0.02 | 2.616 | +0.11 |
| r=4 | 100 | 117 | 0.05 | 0.10 | 2.528 | +0.77 |
| r=16 | 100 | 14 | 0.30 | 0.42 | 2.342 | +2.19 |

### 6mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.012 | +19.64 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.009 | +19.71 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.012 | +19.54 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 293 | 0.00 | 0.01 | 2.051 | -0.19 |
| r=1 | 100 | 281 | 0.00 | 0.01 | 2.047 | -0.09 |
| r=4 | 100 | 274 | 0.00 | 0.01 | 2.046 | -0.04 |
| r=16 | 100 | 234 | 0.01 | 0.03 | 2.041 | +0.10 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 2 | 0.38 | 0.61 | 1.948 | +2.62 |
| r=4 | 100 | 5 | 0.27 | 0.51 | 1.956 | +2.41 |
| r=16 | 100 | 3 | 0.34 | 0.63 | 1.946 | +2.69 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 241 | 0.00 | 0.01 | 2.045 | -0.09 |
| r=1 | 100 | 275 | 0.01 | 0.02 | 2.042 | +0.03 |
| r=4 | 100 | 258 | 0.00 | 0.01 | 2.042 | +0.03 |
| r=16 | 100 | 226 | 0.01 | 0.01 | 2.041 | +0.05 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 4 | 0.29 | 0.53 | 1.957 | +2.37 |
| r=4 | 100 | 5 | 0.35 | 0.56 | 1.952 | +2.52 |
| r=16 | 100 | 3 | 0.34 | 0.60 | 1.950 | +2.55 |

### char_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 266 | 0.00 | 0.02 | 2.046 | -0.05 |
| r=1 | 100 | 250 | 0.00 | 0.01 | 2.046 | -0.02 |
| r=4 | 100 | 226 | 0.00 | 0.01 | 2.043 | +0.09 |
| r=16 | 100 | 212 | 0.00 | 0.02 | 2.038 | +0.19 |

### char_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 4 | 0.36 | 0.58 | 1.952 | +2.50 |
| r=4 | 100 | 4 | 0.28 | 0.55 | 1.954 | +2.45 |
| r=16 | 100 | 3 | 0.38 | 0.61 | 1.949 | +2.57 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 2mer_ar_s0 | train | r=1 | 100 | 0.00 | 30.4 |
| 2mer_ar_s0 | train | r=4 | 100 | 0.00 | 30.1 |
| 2mer_ar_s0 | train | r=16 | 100 | 0.00 | 30.4 |
| 2mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.9 |
| 2mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.1 |
| 2mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 36.6 |
| 2mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.0 |
| 2mer_ar_s1 | train | r=1 | 100 | 0.00 | 30.3 |
| 2mer_ar_s1 | train | r=4 | 100 | 0.00 | 29.9 |
| 2mer_ar_s1 | train | r=16 | 100 | 0.00 | 29.9 |
| 2mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.0 |
| 2mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.2 |
| 2mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 35.9 |
| 2mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.1 |
| 2mer_ar_s2 | train | r=1 | 100 | 0.00 | 30.2 |
| 2mer_ar_s2 | train | r=4 | 100 | 0.00 | 30.0 |
| 2mer_ar_s2 | train | r=16 | 100 | 0.00 | 29.4 |
| 2mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 2mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.8 |
| 2mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.9 |
| 2mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 3mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.4 |
| 3mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.5 |
| 3mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 3mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.8 |
| 3mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 3mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.3 |
| 3mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 35.7 |
| 3mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.4 |
| 3mer_ar_s2 | train | r=1 | 100 | 0.99 | 0.2 |
| 3mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.0 |
| 3mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 36.0 |
| 3mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.0 |
| 3mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 4mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.5 |
| 4mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 35.9 |
| 4mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.9 |
| 4mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.6 |
| 4mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 4mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.1 |
| 4mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.3 |
| 4mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.2 |
| 4mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 4mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.8 |
| 4mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 36.1 |
| 4mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.3 |
| 4mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 5mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 5mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 5mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 5mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.9 |
| 5mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.2 |
| 5mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 36.2 |
| 5mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.1 |
| 5mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 5mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 5mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 5mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.9 |
| 5mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.7 |
| 5mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.4 |
| 5mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 5mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 5mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 5mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 5mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 36.1 |
| 5mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.7 |
| 5mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.7 |
| 5mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 6mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.6 |
| 6mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.9 |
| 6mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.1 |
| 6mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.8 |
| 6mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.6 |
| 6mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.0 |
| 6mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.9 |
| 6mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.9 |
| 6mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.8 |
| 6mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.9 |
| char_ar_s0 | train | r=1 | 100 | 0.00 | 34.7 |
| char_ar_s0 | train | r=4 | 100 | 0.00 | 34.4 |
| char_ar_s0 | train | r=16 | 100 | 0.00 | 34.0 |
| char_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.6 |
| char_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.2 |
| char_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.7 |
| char_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.9 |
| char_ar_s1 | train | r=1 | 100 | 0.00 | 34.0 |
| char_ar_s1 | train | r=4 | 100 | 0.00 | 34.6 |
| char_ar_s1 | train | r=16 | 100 | 0.00 | 33.8 |
| char_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.6 |
| char_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.8 |
| char_ar_s1 | fresh | r=4 | 100 | 0.00 | 35.5 |
| char_ar_s1 | fresh | r=16 | 100 | 0.00 | 35.8 |
| char_ar_s2 | train | r=1 | 100 | 0.00 | 34.3 |
| char_ar_s2 | train | r=4 | 100 | 0.00 | 34.2 |
| char_ar_s2 | train | r=16 | 100 | 0.00 | 34.5 |
| char_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.9 |
| char_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.9 |
| char_ar_s2 | fresh | r=4 | 100 | 0.00 | 35.8 |
| char_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.4 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **2mer_ar_s0** (ar/fresh): bits/nt  r=16 3.103±0.349 | r=1 3.136±0.280 | non-member 3.166±0.297;  rank-1 rate r=16 0.01, r=1 0.00, non-member 0.02;  MWU p(r=16 < non-member) = 1.92e-01, p(r=1 < non-member) = 3.03e-01
- **2mer_ar_s1** (ar/fresh): bits/nt  r=16 3.194±0.193 | r=1 3.126±0.259 | non-member 3.207±0.224;  rank-1 rate r=16 0.00, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 3.17e-01, p(r=1 < non-member) = 1.53e-02
- **2mer_ar_s2** (ar/fresh): bits/nt  r=16 3.205±0.240 | r=1 3.218±0.257 | non-member 3.257±0.254;  rank-1 rate r=16 0.00, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 1.21e-01, p(r=1 < non-member) = 2.16e-01
- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 4.009±0.408 | r=1 4.112±0.284 | non-member 4.187±0.240;  rank-1 rate r=16 0.02, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.33e-05, p(r=1 < non-member) = 1.68e-02
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 4.146±0.271 | r=1 4.179±0.260 | non-member 4.152±0.266;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.94e-01, p(r=1 < non-member) = 7.53e-01
- **3mer_ar_s2** (ar/fresh): bits/nt  r=16 4.126±0.284 | r=1 4.151±0.254 | non-member 4.193±0.227;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.85e-02, p(r=1 < non-member) = 1.09e-01
- **4mer_ar_s0** (ar/fresh): bits/nt  r=16 3.197±0.385 | r=1 3.418±0.216 | non-member 3.439±0.202;  rank-1 rate r=16 0.11, r=1 0.01, non-member 0.01;  MWU p(r=16 < non-member) = 4.85e-09, p(r=1 < non-member) = 2.14e-01
- **4mer_ar_s1** (ar/fresh): bits/nt  r=16 3.244±0.256 | r=1 3.456±0.198 | non-member 3.478±0.182;  rank-1 rate r=16 0.06, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.26e-11, p(r=1 < non-member) = 1.79e-01
- **4mer_ar_s2** (ar/fresh): bits/nt  r=16 3.224±0.265 | r=1 3.432±0.189 | non-member 3.439±0.196;  rank-1 rate r=16 0.09, r=1 0.00, non-member 0.01;  MWU p(r=16 < non-member) = 3.00e-09, p(r=1 < non-member) = 4.28e-01
- **5mer_ar_s0** (ar/fresh): bits/nt  r=16 2.532±0.329 | r=1 2.828±0.125 | non-member 2.848±0.144;  rank-1 rate r=16 0.23, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 9.28e-19, p(r=1 < non-member) = 2.28e-01
- **5mer_ar_s1** (ar/fresh): bits/nt  r=16 2.599±0.229 | r=1 2.841±0.166 | non-member 2.899±0.165;  rank-1 rate r=16 0.21, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.17e-18, p(r=1 < non-member) = 1.52e-02
- **5mer_ar_s2** (ar/fresh): bits/nt  r=16 2.589±0.242 | r=1 2.849±0.161 | non-member 2.841±0.145;  rank-1 rate r=16 0.19, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.93e-15, p(r=1 < non-member) = 6.31e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.295±0.324 | r=1 2.610±0.137 | non-member 2.637±0.112;  rank-1 rate r=16 0.36, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.29e-19, p(r=1 < non-member) = 4.92e-02
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.302±0.269 | r=1 2.631±0.157 | non-member 2.647±0.124;  rank-1 rate r=16 0.36, r=1 0.02, non-member 0.00;  MWU p(r=16 < non-member) = 1.84e-22, p(r=1 < non-member) = 1.36e-01
- **6mer_ar_s2** (ar/fresh): bits/nt  r=16 2.342±0.237 | r=1 2.616±0.144 | non-member 2.640±0.151;  rank-1 rate r=16 0.30, r=1 0.01, non-member 0.01;  MWU p(r=16 < non-member) = 1.31e-18, p(r=1 < non-member) = 1.21e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.041±0.037 | r=1 2.047±0.038 | non-member 2.051±0.036;  rank-1 rate r=16 0.01, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.51e-02, p(r=1 < non-member) = 1.84e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.041±0.039 | r=1 2.042±0.037 | non-member 2.045±0.035;  rank-1 rate r=16 0.01, r=1 0.01, non-member 0.00;  MWU p(r=16 < non-member) = 1.47e-01, p(r=1 < non-member) = 3.80e-01
- **char_ar_s2** (ar/fresh): bits/nt  r=16 2.038±0.037 | r=1 2.046±0.040 | non-member 2.046±0.037;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.05e-02, p(r=1 < non-member) = 3.78e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **2mer_ar_s0**: r=16 probe bits/nt 0.893, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **2mer_ar_s1**: r=16 probe bits/nt 0.834, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **2mer_ar_s2**: r=16 probe bits/nt 0.806, rank-1 rate 1.00, exact-extraction rate 0.00
- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.027, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.020, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s2**: r=16 probe bits/nt 0.017, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s0**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s1**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **4mer_ar_s2**: r=16 probe bits/nt 0.008, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **5mer_ar_s0**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **5mer_ar_s1**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **5mer_ar_s2**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.012, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s2**: r=16 probe bits/nt 0.012, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.946, rank-1 rate 0.34, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.950, rank-1 rate 0.34, exact-extraction rate 0.00
- ar  **char_ar_s2**: r=16 probe bits/nt 1.949, rank-1 rate 0.38, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.