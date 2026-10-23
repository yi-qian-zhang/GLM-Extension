# Gate 1 report

root: outputs/tok1   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 3mer_mlm0.15_s0, 3mer_mlm0.15_s1, 3mer_mlm0.50_s0, 3mer_mlm0.50_s1, 6mer_ar_s0, 6mer_ar_s1, 6mer_mlm0.15_s0, 6mer_mlm0.15_s1, 6mer_mlm0.50_s0, 6mer_mlm0.50_s1, char_ar_s0, char_ar_s1, char_mlm0.15_s0, char_mlm0.15_s1, char_mlm0.50_s0, char_mlm0.50_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 30 | 9 | 0.26 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 29 | 9 | 0.26 |
| 3mer_mlm0.15_s0 | 3mer | 12.69M (12.61M) | 2550 | 2.3M | 69 | 417 | 0.11 |
| 3mer_mlm0.15_s1 | 3mer | 12.69M (12.61M) | 2550 | 2.3M | 31 | 221 | 0.25 |
| 3mer_mlm0.50_s0 | 3mer | 12.69M (12.61M) | 2550 | 7.8M | 32 | 223 | 0.23 |
| 3mer_mlm0.50_s1 | 3mer | 12.69M (12.61M) | 2550 | 7.8M | 31 | 222 | 0.25 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 36 | 13 | 0.12 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 31 | 5 | 0.14 |
| 6mer_mlm0.15_s0 | 6mer | 14.73M (12.61M) | 2550 | 1.2M | 34 | 64 | 0.13 |
| 6mer_mlm0.15_s1 | 6mer | 14.73M (12.61M) | 2550 | 1.2M | 32 | 63 | 0.14 |
| 6mer_mlm0.50_s0 | 6mer | 14.73M (12.61M) | 2550 | 3.9M | 53 | 125 | 0.08 |
| 6mer_mlm0.50_s1 | 6mer | 14.73M (12.61M) | 2550 | 3.9M | 31 | 63 | 0.14 |
| char_ar_s0 | char | 12.76M (12.61M) | 2550 | 46.8M | 119 | 58 | 0.20 |
| char_ar_s1 | char | 12.76M (12.61M) | 2550 | 46.8M | 65 | 25 | 0.35 |
| char_mlm0.15_s0 | char | 12.76M (12.61M) | 2550 | 7.0M | 71 | 2025 | 0.32 |
| char_mlm0.15_s1 | char | 12.76M (12.61M) | 2550 | 7.0M | 70 | 2031 | 0.33 |
| char_mlm0.50_s0 | char | 12.76M (12.61M) | 2550 | 23.4M | 74 | 2004 | 0.32 |
| char_mlm0.50_s1 | char | 12.76M (12.61M) | 2550 | 23.4M | 71 | 2006 | 0.32 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.0614 | 16.6951 | 3.565 | OK |
| 3mer_ar_s1 | ar | 4.1222 | 17.4145 | 3.664 | OK |
| 3mer_mlm0.15_s0 | pll | 2.0043 | 4.0118 | 1.986 | OK |
| 3mer_mlm0.15_s0 | prefix | 2.0050 | 4.0139 | 1.983 | OK |
| 3mer_mlm0.15_s1 | pll | 2.0032 | 4.0088 | 1.986 | OK |
| 3mer_mlm0.15_s1 | prefix | 2.0037 | 4.0103 | 1.988 | OK |
| 3mer_mlm0.50_s0 | pll | 2.0049 | 4.0137 | 1.985 | OK |
| 3mer_mlm0.50_s0 | prefix | 2.0043 | 4.0120 | 1.987 | OK |
| 3mer_mlm0.50_s1 | pll | 2.0041 | 4.0113 | 1.986 | OK |
| 3mer_mlm0.50_s1 | prefix | 2.0062 | 4.0174 | 1.989 | OK |
| 6mer_ar_s0 | ar | 2.5259 | 5.7593 | 2.355 | OK |
| 6mer_ar_s1 | ar | 2.5183 | 5.7291 | 2.327 | OK |
| 6mer_mlm0.15_s0 | pll | 2.0336 | 4.0942 | 1.983 | OK |
| 6mer_mlm0.15_s0 | prefix | 2.0238 | 4.0667 | 1.980 | OK |
| 6mer_mlm0.15_s1 | pll | 2.0372 | 4.1045 | 1.968 | OK |
| 6mer_mlm0.15_s1 | prefix | 2.0297 | 4.0832 | 1.970 | OK |
| 6mer_mlm0.50_s0 | pll | 2.0583 | 4.1650 | 1.979 | OK |
| 6mer_mlm0.50_s0 | prefix | 2.0556 | 4.1571 | 1.984 | OK |
| 6mer_mlm0.50_s1 | pll | 2.0527 | 4.1488 | 1.978 | OK |
| 6mer_mlm0.50_s1 | prefix | 2.0503 | 4.1421 | 1.987 | OK |
| char_ar_s0 | ar | 2.0409 | 4.1149 | 1.979 | OK |
| char_ar_s1 | ar | 2.0374 | 4.1050 | 1.984 | OK |
| char_mlm0.15_s0 | pll | 2.0005 | 4.0013 | 1.994 | OK |
| char_mlm0.15_s0 | prefix | 2.0004 | 4.0011 | 1.995 | OK |
| char_mlm0.15_s1 | pll | 2.0005 | 4.0015 | 1.994 | OK |
| char_mlm0.15_s1 | prefix | 2.0005 | 4.0014 | 1.994 | OK |
| char_mlm0.50_s0 | pll | 2.0037 | 4.0103 | 1.983 | OK |
| char_mlm0.50_s0 | prefix | 2.0032 | 4.0088 | 1.989 | OK |
| char_mlm0.50_s1 | pll | 2.0050 | 4.0138 | 1.984 | OK |
| char_mlm0.50_s1 | prefix | 2.0027 | 4.0076 | 1.986 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 321 | 0.00 | 0.03 | 4.236 | -0.21 |
| r=1 | 20 | 14 | 0.15 | 0.35 | 3.726 | +1.89 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 2.280 | +8.06 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.515 | +15.27 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.004 | +17.71 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.03 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +17.66 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 186 | 0.00 | 0.03 | 4.171 | +0.35 |
| r=1 | 20 | 52 | 0.10 | 0.20 | 3.882 | +1.54 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 2.443 | +7.52 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.488 | +15.54 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +18.07 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.07 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +18.01 |

### 3mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 219 | 0.00 | 0.00 | 2.005 | +0.02 |
| r=1 | 20 | 138 | 0.00 | 0.00 | 1.997 | +0.62 |
| r=4 | 20 | 6 | 0.25 | 0.45 | 1.957 | +3.49 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.390 | +114.25 |

### 3mer_mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 140 | 0.00 | 0.00 | 1.997 | +0.60 |
| r=4 | 20 | 3 | 0.35 | 0.60 | 1.955 | +3.57 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.383 | +114.28 |

### 3mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 232 | 0.00 | 0.00 | 2.009 | -0.06 |
| r=1 | 20 | 164 | 0.05 | 0.05 | 2.001 | +0.39 |
| r=4 | 20 | 18 | 0.15 | 0.20 | 1.978 | +1.75 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.984 | +65.03 |

### 3mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 179 | 0.00 | 0.05 | 2.001 | +0.39 |
| r=4 | 20 | 14 | 0.20 | 0.40 | 1.975 | +2.00 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.976 | +65.06 |

### 3mer_mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 226 | 0.00 | 0.00 | 2.002 | +0.10 |
| r=1 | 20 | 126 | 0.00 | 0.10 | 1.996 | +0.55 |
| r=4 | 20 | 12 | 0.05 | 0.35 | 1.974 | +2.21 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.532 | +113.14 |

### 3mer_mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 108 | 0.00 | 0.05 | 1.994 | +0.75 |
| r=4 | 20 | 6 | 0.05 | 0.40 | 1.974 | +2.33 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.518 | +111.87 |

### 3mer_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 226 | 0.00 | 0.00 | 2.003 | +0.15 |
| r=1 | 20 | 170 | 0.00 | 0.00 | 2.000 | +0.32 |
| r=4 | 20 | 62 | 0.15 | 0.20 | 1.984 | +1.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.337 | +37.65 |

### 3mer_mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 136 | 0.00 | 0.05 | 1.998 | +0.47 |
| r=4 | 20 | 38 | 0.10 | 0.20 | 1.986 | +1.11 |
| r=16 | 20 | 1 | 0.95 | 1.00 | 1.323 | +39.58 |

### 3mer_mlm0.50_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 252 | 0.00 | 0.00 | 2.005 | -0.02 |
| r=1 | 20 | 80 | 0.00 | 0.05 | 1.994 | +0.90 |
| r=4 | 20 | 1 | 0.55 | 0.90 | 1.962 | +3.72 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.109 | +164.46 |

### 3mer_mlm0.50_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 95 | 0.00 | 0.05 | 1.995 | +0.85 |
| r=4 | 20 | 1 | 0.65 | 0.90 | 1.961 | +3.77 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.108 | +165.54 |

### 3mer_mlm0.50_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 220 | 0.00 | 0.00 | 2.004 | +0.02 |
| r=1 | 20 | 104 | 0.00 | 0.00 | 1.996 | +0.77 |
| r=4 | 20 | 8 | 0.20 | 0.40 | 1.977 | +2.70 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.613 | +137.87 |

### 3mer_mlm0.50_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 170 | 0.00 | 0.00 | 1.996 | +0.72 |
| r=4 | 20 | 6 | 0.30 | 0.45 | 1.976 | +2.81 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.584 | +140.57 |

### 3mer_mlm0.50_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 246 | 0.00 | 0.00 | 2.004 | +0.02 |
| r=1 | 20 | 96 | 0.00 | 0.10 | 1.992 | +0.94 |
| r=4 | 20 | 1 | 0.55 | 0.70 | 1.967 | +3.10 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.210 | +148.57 |

### 3mer_mlm0.50_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 75 | 0.05 | 0.10 | 1.990 | +1.14 |
| r=4 | 20 | 2 | 0.50 | 0.70 | 1.965 | +3.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.204 | +149.31 |

### 3mer_mlm0.50_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 227 | 0.00 | 0.00 | 2.004 | +0.19 |
| r=1 | 20 | 228 | 0.00 | 0.00 | 2.012 | -0.09 |
| r=4 | 20 | 12 | 0.15 | 0.40 | 1.984 | +1.21 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.570 | +69.93 |

### 3mer_mlm0.50_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 168 | 0.00 | 0.00 | 2.006 | +0.22 |
| r=4 | 20 | 9 | 0.15 | 0.35 | 1.984 | +1.23 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.560 | +74.45 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 220 | 0.03 | 0.03 | 2.509 | +0.17 |
| r=1 | 20 | 1 | 0.85 | 0.95 | 2.003 | +4.31 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.695 | +14.99 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.157 | +19.56 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.06 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.003 | +21.18 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +20.98 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 214 | 0.00 | 0.00 | 2.506 | +0.15 |
| r=1 | 20 | 1 | 0.90 | 0.95 | 1.991 | +4.43 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.711 | +15.07 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.138 | +19.88 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.20 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.003 | +21.18 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +21.44 |

### 6mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 256 | 0.00 | 0.00 | 2.031 | +0.12 |
| r=1 | 20 | 16 | 0.10 | 0.15 | 1.981 | +1.63 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.743 | +9.06 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.894 | +35.49 |

### 6mer_mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 10 | 0.15 | 0.40 | 1.961 | +2.28 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.732 | +9.24 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.890 | +35.39 |

### 6mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 202 | 0.00 | 0.00 | 2.018 | +0.31 |
| r=1 | 20 | 58 | 0.00 | 0.00 | 1.993 | +1.17 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.847 | +6.43 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.294 | +26.02 |

### 6mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 36 | 0.05 | 0.20 | 1.979 | +1.68 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.838 | +6.70 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.276 | +26.78 |

### 6mer_mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 268 | 0.00 | 0.00 | 2.039 | -0.01 |
| r=1 | 20 | 4 | 0.25 | 0.55 | 1.948 | +2.69 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.662 | +11.23 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.558 | +44.16 |

### 6mer_mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 2 | 0.30 | 0.70 | 1.936 | +3.05 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.657 | +11.37 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.552 | +44.06 |

### 6mer_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 231 | 0.00 | 0.00 | 2.029 | +0.11 |
| r=1 | 20 | 16 | 0.10 | 0.30 | 1.974 | +1.78 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.799 | +6.93 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.884 | +33.98 |

### 6mer_mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 14 | 0.10 | 0.25 | 1.971 | +1.86 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.796 | +7.01 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.875 | +34.05 |

### 6mer_mlm0.50_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 196 | 0.00 | 0.05 | 2.050 | +0.21 |
| r=1 | 20 | 1 | 0.95 | 1.00 | 1.845 | +5.15 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.026 | +24.91 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.062 | +48.13 |

### 6mer_mlm0.50_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.829 | +5.51 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.015 | +25.14 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.060 | +48.16 |

### 6mer_mlm0.50_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 202 | 0.00 | 0.03 | 2.052 | +0.18 |
| r=1 | 20 | 1 | 0.90 | 0.90 | 1.882 | +4.28 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.166 | +21.39 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.272 | +42.82 |

### 6mer_mlm0.50_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.95 | 1.00 | 1.871 | +4.52 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.156 | +21.64 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.259 | +43.18 |

### 6mer_mlm0.50_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 239 | 0.00 | 0.00 | 2.051 | +0.16 |
| r=1 | 20 | 1 | 0.85 | 0.95 | 1.886 | +4.10 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.036 | +24.37 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.142 | +45.54 |

### 6mer_mlm0.50_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.90 | 0.95 | 1.879 | +4.27 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.036 | +24.27 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.149 | +45.35 |

### 6mer_mlm0.50_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 192 | 0.00 | 0.00 | 2.050 | +0.30 |
| r=1 | 20 | 1 | 0.80 | 0.95 | 1.909 | +3.71 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.071 | +23.93 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.194 | +45.10 |

### 6mer_mlm0.50_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.80 | 0.95 | 1.902 | +3.89 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.054 | +24.32 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.179 | +45.24 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 244 | 0.00 | 0.03 | 2.029 | +0.20 |
| r=1 | 20 | 96 | 0.00 | 0.05 | 1.997 | +0.53 |
| r=4 | 20 | 1 | 0.75 | 0.85 | 1.890 | +1.56 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.575 | +16.15 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 21 | 0.20 | 0.35 | 1.964 | +0.82 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.825 | +1.89 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.434 | +13.97 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 154 | 0.00 | 0.00 | 2.018 | +0.25 |
| r=1 | 20 | 124 | 0.00 | 0.10 | 2.023 | +0.27 |
| r=4 | 20 | 1 | 0.85 | 0.95 | 1.884 | +1.67 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.512 | +16.77 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 24 | 0.10 | 0.30 | 1.975 | +0.73 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 1.849 | +2.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.430 | +14.60 |

### char_mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 264 | 0.00 | 0.03 | 2.001 | +0.02 |
| r=1 | 20 | 208 | 0.00 | 0.00 | 2.000 | +0.22 |
| r=4 | 20 | 156 | 0.05 | 0.05 | 1.998 | +0.72 |
| r=16 | 20 | 6 | 0.35 | 0.50 | 1.990 | +2.43 |

### char_mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 200 | 0.00 | 0.05 | 2.000 | +0.25 |
| r=4 | 20 | 143 | 0.05 | 0.05 | 1.998 | +0.69 |
| r=16 | 20 | 5 | 0.40 | 0.50 | 1.990 | +2.50 |

### char_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 250 | 0.00 | 0.00 | 2.001 | +0.03 |
| r=1 | 20 | 212 | 0.00 | 0.05 | 2.000 | +0.20 |
| r=4 | 20 | 138 | 0.05 | 0.05 | 1.998 | +0.74 |
| r=16 | 20 | 8 | 0.30 | 0.40 | 1.991 | +2.34 |

### char_mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 213 | 0.00 | 0.05 | 2.000 | +0.22 |
| r=4 | 20 | 134 | 0.05 | 0.05 | 1.998 | +0.66 |
| r=16 | 20 | 6 | 0.35 | 0.50 | 1.991 | +2.41 |

### char_mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 286 | 0.03 | 0.05 | 2.001 | -0.11 |
| r=1 | 20 | 292 | 0.00 | 0.05 | 2.000 | -0.05 |
| r=4 | 20 | 98 | 0.10 | 0.15 | 1.997 | +0.74 |
| r=16 | 20 | 4 | 0.30 | 0.50 | 1.990 | +2.56 |

### char_mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 286 | 0.00 | 0.10 | 2.000 | -0.01 |
| r=4 | 20 | 100 | 0.10 | 0.10 | 1.997 | +0.74 |
| r=16 | 20 | 4 | 0.30 | 0.55 | 1.990 | +2.56 |

### char_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 318 | 0.00 | 0.03 | 2.001 | -0.12 |
| r=1 | 20 | 246 | 0.00 | 0.05 | 2.000 | +0.08 |
| r=4 | 20 | 168 | 0.05 | 0.15 | 1.997 | +0.72 |
| r=16 | 20 | 8 | 0.30 | 0.40 | 1.991 | +2.35 |

### char_mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 246 | 0.00 | 0.00 | 2.000 | +0.06 |
| r=4 | 20 | 146 | 0.10 | 0.15 | 1.997 | +0.74 |
| r=16 | 20 | 10 | 0.30 | 0.40 | 1.991 | +2.37 |

### char_mlm0.50_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 241 | 0.00 | 0.00 | 2.004 | +0.03 |
| r=1 | 20 | 339 | 0.00 | 0.00 | 2.006 | -0.04 |
| r=4 | 20 | 60 | 0.00 | 0.15 | 1.991 | +1.19 |
| r=16 | 20 | 1 | 0.70 | 1.00 | 1.926 | +6.68 |

### char_mlm0.50_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 220 | 0.00 | 0.00 | 2.002 | +0.24 |
| r=4 | 20 | 56 | 0.00 | 0.10 | 1.990 | +1.30 |
| r=16 | 20 | 1 | 0.85 | 1.00 | 1.925 | +6.99 |

### char_mlm0.50_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 162 | 0.00 | 0.00 | 2.001 | +0.30 |
| r=1 | 20 | 198 | 0.00 | 0.00 | 2.002 | +0.19 |
| r=4 | 20 | 55 | 0.00 | 0.05 | 1.993 | +1.03 |
| r=16 | 20 | 1 | 0.85 | 0.95 | 1.942 | +5.65 |

### char_mlm0.50_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 168 | 0.00 | 0.00 | 2.001 | +0.26 |
| r=4 | 20 | 60 | 0.05 | 0.05 | 1.992 | +1.10 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.940 | +5.90 |

### char_mlm0.50_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 192 | 0.00 | 0.03 | 2.003 | +0.13 |
| r=1 | 20 | 148 | 0.00 | 0.00 | 1.998 | +0.55 |
| r=4 | 20 | 59 | 0.05 | 0.15 | 1.989 | +1.22 |
| r=16 | 20 | 1 | 0.95 | 1.00 | 1.947 | +4.24 |

### char_mlm0.50_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 156 | 0.00 | 0.00 | 1.997 | +0.57 |
| r=4 | 20 | 29 | 0.10 | 0.30 | 1.984 | +1.57 |
| r=16 | 20 | 1 | 0.95 | 0.95 | 1.943 | +4.66 |

### char_mlm0.50_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 270 | 0.00 | 0.03 | 2.002 | +0.06 |
| r=1 | 20 | 160 | 0.00 | 0.05 | 1.997 | +0.54 |
| r=4 | 20 | 76 | 0.00 | 0.05 | 1.994 | +0.88 |
| r=16 | 20 | 1 | 0.90 | 0.95 | 1.957 | +4.83 |

### char_mlm0.50_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 165 | 0.05 | 0.05 | 1.998 | +0.48 |
| r=4 | 20 | 76 | 0.00 | 0.20 | 1.991 | +1.23 |
| r=16 | 20 | 1 | 0.95 | 0.95 | 1.953 | +5.32 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.1 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 33.0 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.30 | 11.4 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.9 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.40 | 8.8 |
| 3mer_mlm0.15_s0 | train | r=1 | 20 | 0.00 | 37.1 |
| 3mer_mlm0.15_s0 | train | r=4 | 20 | 0.00 | 35.0 |
| 3mer_mlm0.15_s0 | train | r=16 | 20 | 0.25 | 6.5 |
| 3mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 35.5 |
| 3mer_mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 36.9 |
| 3mer_mlm0.15_s0 | fresh | r=4 | 20 | 0.00 | 34.0 |
| 3mer_mlm0.15_s0 | fresh | r=16 | 20 | 0.25 | 6.7 |
| 3mer_mlm0.15_s1 | train | r=1 | 20 | 0.00 | 35.6 |
| 3mer_mlm0.15_s1 | train | r=4 | 20 | 0.00 | 35.4 |
| 3mer_mlm0.15_s1 | train | r=16 | 20 | 0.05 | 21.8 |
| 3mer_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 3mer_mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 34.9 |
| 3mer_mlm0.15_s1 | fresh | r=4 | 20 | 0.00 | 34.4 |
| 3mer_mlm0.15_s1 | fresh | r=16 | 20 | 0.05 | 21.2 |
| 3mer_mlm0.50_s0 | train | r=1 | 20 | 0.00 | 35.4 |
| 3mer_mlm0.50_s0 | train | r=4 | 20 | 0.00 | 35.2 |
| 3mer_mlm0.50_s0 | train | r=16 | 20 | 0.80 | 2.0 |
| 3mer_mlm0.50_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 3mer_mlm0.50_s0 | fresh | r=1 | 20 | 0.00 | 35.6 |
| 3mer_mlm0.50_s0 | fresh | r=4 | 20 | 0.00 | 34.9 |
| 3mer_mlm0.50_s0 | fresh | r=16 | 20 | 0.90 | 1.5 |
| 3mer_mlm0.50_s1 | train | r=1 | 20 | 0.00 | 36.6 |
| 3mer_mlm0.50_s1 | train | r=4 | 20 | 0.00 | 37.1 |
| 3mer_mlm0.50_s1 | train | r=16 | 20 | 0.70 | 2.3 |
| 3mer_mlm0.50_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 3mer_mlm0.50_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| 3mer_mlm0.50_s1 | fresh | r=4 | 20 | 0.00 | 35.8 |
| 3mer_mlm0.50_s1 | fresh | r=16 | 20 | 0.65 | 2.6 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.30 | 20.1 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.1 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.30 | 19.2 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_mlm0.15_s0 | train | r=1 | 20 | 0.00 | 36.0 |
| 6mer_mlm0.15_s0 | train | r=4 | 20 | 0.00 | 35.6 |
| 6mer_mlm0.15_s0 | train | r=16 | 20 | 0.00 | 18.4 |
| 6mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 36.1 |
| 6mer_mlm0.15_s0 | fresh | r=4 | 20 | 0.00 | 36.0 |
| 6mer_mlm0.15_s0 | fresh | r=16 | 20 | 0.00 | 18.1 |
| 6mer_mlm0.15_s1 | train | r=1 | 20 | 0.00 | 34.9 |
| 6mer_mlm0.15_s1 | train | r=4 | 20 | 0.00 | 36.2 |
| 6mer_mlm0.15_s1 | train | r=16 | 20 | 0.25 | 6.8 |
| 6mer_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 6mer_mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 35.9 |
| 6mer_mlm0.15_s1 | fresh | r=4 | 20 | 0.00 | 37.2 |
| 6mer_mlm0.15_s1 | fresh | r=16 | 20 | 0.25 | 5.8 |
| 6mer_mlm0.50_s0 | train | r=1 | 20 | 0.00 | 35.8 |
| 6mer_mlm0.50_s0 | train | r=4 | 20 | 0.00 | 27.1 |
| 6mer_mlm0.50_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_mlm0.50_s0 | fresh | r=0 | 40 | 0.00 | 36.3 |
| 6mer_mlm0.50_s0 | fresh | r=1 | 20 | 0.00 | 35.8 |
| 6mer_mlm0.50_s0 | fresh | r=4 | 20 | 0.00 | 27.4 |
| 6mer_mlm0.50_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_mlm0.50_s1 | train | r=1 | 20 | 0.00 | 36.2 |
| 6mer_mlm0.50_s1 | train | r=4 | 20 | 0.00 | 28.4 |
| 6mer_mlm0.50_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_mlm0.50_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.50_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| 6mer_mlm0.50_s1 | fresh | r=4 | 20 | 0.00 | 25.9 |
| 6mer_mlm0.50_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 34.5 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 31.7 |
| char_ar_s0 | train | r=16 | 20 | 0.90 | 0.7 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.9 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.3 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 32.4 |
| char_ar_s0 | fresh | r=16 | 20 | 0.35 | 1.9 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 34.5 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 31.2 |
| char_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.1 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.0 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 32.8 |
| char_ar_s1 | fresh | r=16 | 20 | 0.65 | 1.6 |
| char_mlm0.15_s0 | train | r=1 | 20 | 0.00 | 36.1 |
| char_mlm0.15_s0 | train | r=4 | 20 | 0.00 | 33.8 |
| char_mlm0.15_s0 | train | r=16 | 20 | 0.00 | 32.9 |
| char_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 35.9 |
| char_mlm0.15_s0 | fresh | r=4 | 20 | 0.00 | 33.9 |
| char_mlm0.15_s0 | fresh | r=16 | 20 | 0.00 | 33.0 |
| char_mlm0.15_s1 | train | r=1 | 20 | 0.00 | 36.3 |
| char_mlm0.15_s1 | train | r=4 | 20 | 0.00 | 34.1 |
| char_mlm0.15_s1 | train | r=16 | 20 | 0.00 | 32.8 |
| char_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 35.8 |
| char_mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 36.0 |
| char_mlm0.15_s1 | fresh | r=4 | 20 | 0.00 | 34.1 |
| char_mlm0.15_s1 | fresh | r=16 | 20 | 0.00 | 33.0 |
| char_mlm0.50_s0 | train | r=1 | 20 | 0.00 | 36.6 |
| char_mlm0.50_s0 | train | r=4 | 20 | 0.00 | 35.0 |
| char_mlm0.50_s0 | train | r=16 | 20 | 0.00 | 29.5 |
| char_mlm0.50_s0 | fresh | r=0 | 40 | 0.00 | 35.6 |
| char_mlm0.50_s0 | fresh | r=1 | 20 | 0.00 | 37.0 |
| char_mlm0.50_s0 | fresh | r=4 | 20 | 0.00 | 34.5 |
| char_mlm0.50_s0 | fresh | r=16 | 20 | 0.00 | 29.1 |
| char_mlm0.50_s1 | train | r=1 | 20 | 0.00 | 35.3 |
| char_mlm0.50_s1 | train | r=4 | 20 | 0.00 | 35.1 |
| char_mlm0.50_s1 | train | r=16 | 20 | 0.00 | 28.9 |
| char_mlm0.50_s1 | fresh | r=0 | 40 | 0.00 | 35.4 |
| char_mlm0.50_s1 | fresh | r=1 | 20 | 0.00 | 34.5 |
| char_mlm0.50_s1 | fresh | r=4 | 20 | 0.00 | 35.5 |
| char_mlm0.50_s1 | fresh | r=16 | 20 | 0.00 | 29.6 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **3mer_mlm0.15_s0 / fresh**: n=100, Spearman(bits) = 0.886, Spearman(rank) = 0.887, rank-1 set Jaccard = 0.88 (25 vs 24 rank-1)
- **3mer_mlm0.15_s0 / train**: n=60, Spearman(bits) = 0.930, Spearman(rank) = 0.909, rank-1 set Jaccard = 0.89 (27 vs 24 rank-1)
- **3mer_mlm0.15_s1 / fresh**: n=100, Spearman(bits) = 0.860, Spearman(rank) = 0.866, rank-1 set Jaccard = 0.91 (21 vs 23 rank-1)
- **3mer_mlm0.15_s1 / train**: n=60, Spearman(bits) = 0.901, Spearman(rank) = 0.906, rank-1 set Jaccard = 0.91 (21 vs 21 rank-1)
- **3mer_mlm0.50_s0 / fresh**: n=100, Spearman(bits) = 0.959, Spearman(rank) = 0.953, rank-1 set Jaccard = 0.77 (31 vs 24 rank-1)
- **3mer_mlm0.50_s0 / train**: n=60, Spearman(bits) = 0.955, Spearman(rank) = 0.931, rank-1 set Jaccard = 0.79 (33 vs 26 rank-1)
- **3mer_mlm0.50_s1 / fresh**: n=100, Spearman(bits) = 0.791, Spearman(rank) = 0.789, rank-1 set Jaccard = 0.69 (31 vs 23 rank-1)
- **3mer_mlm0.50_s1 / train**: n=60, Spearman(bits) = 0.880, Spearman(rank) = 0.807, rank-1 set Jaccard = 0.74 (31 vs 23 rank-1)
- **6mer_mlm0.15_s0 / fresh**: n=100, Spearman(bits) = 0.914, Spearman(rank) = 0.905, rank-1 set Jaccard = 0.95 (42 vs 40 rank-1)
- **6mer_mlm0.15_s0 / train**: n=60, Spearman(bits) = 0.940, Spearman(rank) = 0.820, rank-1 set Jaccard = 0.91 (43 vs 41 rank-1)
- **6mer_mlm0.15_s1 / fresh**: n=100, Spearman(bits) = 0.956, Spearman(rank) = 0.946, rank-1 set Jaccard = 0.93 (45 vs 42 rank-1)
- **6mer_mlm0.15_s1 / train**: n=60, Spearman(bits) = 0.972, Spearman(rank) = 0.878, rank-1 set Jaccard = 0.91 (46 vs 42 rank-1)
- **6mer_mlm0.50_s0 / fresh**: n=100, Spearman(bits) = 0.968, Spearman(rank) = 0.968, rank-1 set Jaccard = 0.98 (59 vs 58 rank-1)
- **6mer_mlm0.50_s0 / train**: n=60, Spearman(bits) = 0.950, Spearman(rank) = nan, rank-1 set Jaccard = 0.98 (60 vs 59 rank-1)
- **6mer_mlm0.50_s1 / fresh**: n=100, Spearman(bits) = 0.970, Spearman(rank) = 0.945, rank-1 set Jaccard = 0.92 (57 vs 56 rank-1)
- **6mer_mlm0.50_s1 / train**: n=60, Spearman(bits) = 0.950, Spearman(rank) = 0.304, rank-1 set Jaccard = 0.93 (58 vs 56 rank-1)
- **char_mlm0.15_s0 / fresh**: n=100, Spearman(bits) = 0.984, Spearman(rank) = 0.985, rank-1 set Jaccard = 0.88 (8 vs 7 rank-1)
- **char_mlm0.15_s0 / train**: n=60, Spearman(bits) = 0.987, Spearman(rank) = 0.985, rank-1 set Jaccard = 0.89 (9 vs 8 rank-1)
- **char_mlm0.15_s1 / fresh**: n=100, Spearman(bits) = 0.964, Spearman(rank) = 0.964, rank-1 set Jaccard = 0.78 (9 vs 7 rank-1)
- **char_mlm0.15_s1 / train**: n=60, Spearman(bits) = 0.965, Spearman(rank) = 0.963, rank-1 set Jaccard = 1.00 (8 vs 8 rank-1)
- **char_mlm0.50_s0 / fresh**: n=100, Spearman(bits) = 0.848, Spearman(rank) = 0.855, rank-1 set Jaccard = 0.82 (14 vs 17 rank-1)
- **char_mlm0.50_s0 / train**: n=60, Spearman(bits) = 0.941, Spearman(rank) = 0.936, rank-1 set Jaccard = 0.81 (17 vs 21 rank-1)
- **char_mlm0.50_s1 / fresh**: n=100, Spearman(bits) = 0.775, Spearman(rank) = 0.774, rank-1 set Jaccard = 0.90 (20 vs 18 rank-1)
- **char_mlm0.50_s1 / train**: n=60, Spearman(bits) = 0.843, Spearman(rank) = 0.828, rank-1 set Jaccard = 0.86 (21 vs 20 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 0.515±0.164 | r=1 3.726±0.310 | non-member 4.236±0.274;  rank-1 rate r=16 1.00, r=1 0.15, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.13e-06
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 0.488±0.216 | r=1 3.882±0.291 | non-member 4.171±0.245;  rank-1 rate r=16 1.00, r=1 0.10, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.43e-04
- **3mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 0.984±0.360 | r=1 2.001±0.012 | non-member 2.009±0.017;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.28e-01
- **3mer_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 1.337±0.237 | r=1 2.000±0.011 | non-member 2.003±0.009;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.84e-01
- **3mer_mlm0.50_s0** (prefix/fresh): bits/nt  r=16 0.613±0.325 | r=1 1.996±0.009 | non-member 2.004±0.011;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.22e-02
- **3mer_mlm0.50_s1** (prefix/fresh): bits/nt  r=16 0.570±0.336 | r=1 2.012±0.030 | non-member 2.004±0.015;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.77e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.157±0.024 | r=1 2.003±0.123 | non-member 2.509±0.132;  rank-1 rate r=16 1.00, r=1 0.85, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.08e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.138±0.034 | r=1 1.991±0.114 | non-member 2.506±0.109;  rank-1 rate r=16 1.00, r=1 0.90, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **6mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 1.294±0.076 | r=1 1.993±0.018 | non-member 2.018±0.026;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.57e-04
- **6mer_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 0.884±0.076 | r=1 1.974±0.034 | non-member 2.029±0.029;  rank-1 rate r=16 1.00, r=1 0.10, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.11e-07
- **6mer_mlm0.50_s0** (prefix/fresh): bits/nt  r=16 0.272±0.050 | r=1 1.882±0.040 | non-member 2.052±0.040;  rank-1 rate r=16 1.00, r=1 0.90, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.79e-10
- **6mer_mlm0.50_s1** (prefix/fresh): bits/nt  r=16 0.194±0.040 | r=1 1.909±0.039 | non-member 2.050±0.038;  rank-1 rate r=16 1.00, r=1 0.80, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.08e-10
- **char_ar_s0** (ar/fresh): bits/nt  r=16 0.575±0.117 | r=1 1.997±0.022 | non-member 2.029±0.038;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.48e-03
- **char_ar_s1** (ar/fresh): bits/nt  r=16 0.512±0.103 | r=1 2.023±0.052 | non-member 2.018±0.021;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.86e-01
- **char_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 1.991±0.004 | r=1 2.000±0.004 | non-member 2.001±0.004;  rank-1 rate r=16 0.30, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.63e-09, p(r=1 < non-member) = 3.50e-01
- **char_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 1.991±0.004 | r=1 2.000±0.004 | non-member 2.001±0.004;  rank-1 rate r=16 0.30, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.63e-09, p(r=1 < non-member) = 2.38e-01
- **char_mlm0.50_s0** (prefix/fresh): bits/nt  r=16 1.942±0.025 | r=1 2.002±0.010 | non-member 2.001±0.008;  rank-1 rate r=16 0.85, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.11e-01
- **char_mlm0.50_s1** (prefix/fresh): bits/nt  r=16 1.957±0.012 | r=1 1.997±0.008 | non-member 2.002±0.009;  rank-1 rate r=16 0.90, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.07e-10, p(r=1 < non-member) = 1.89e-02

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 0.434, rank-1 rate 1.00, exact-extraction rate 0.90
- ar  **char_ar_s1**: r=16 probe bits/nt 0.430, rank-1 rate 1.00, exact-extraction rate 1.00
- mlm **3mer_mlm0.15_s0**: r=16 probe bits/nt 0.976, rank-1 rate 1.00, exact-extraction rate 0.25
- mlm **3mer_mlm0.15_s1**: r=16 probe bits/nt 1.323, rank-1 rate 0.95, exact-extraction rate 0.05
- mlm **3mer_mlm0.50_s0**: r=16 probe bits/nt 0.584, rank-1 rate 1.00, exact-extraction rate 0.80
- mlm **3mer_mlm0.50_s1**: r=16 probe bits/nt 0.560, rank-1 rate 1.00, exact-extraction rate 0.70
- mlm **6mer_mlm0.15_s0**: r=16 probe bits/nt 1.276, rank-1 rate 1.00, exact-extraction rate 0.00
- mlm **6mer_mlm0.15_s1**: r=16 probe bits/nt 0.875, rank-1 rate 1.00, exact-extraction rate 0.25
- mlm **6mer_mlm0.50_s0**: r=16 probe bits/nt 0.259, rank-1 rate 1.00, exact-extraction rate 1.00
- mlm **6mer_mlm0.50_s1**: r=16 probe bits/nt 0.179, rank-1 rate 1.00, exact-extraction rate 1.00
- mlm **char_mlm0.15_s0**: r=16 probe bits/nt 1.991, rank-1 rate 0.35, exact-extraction rate 0.00
- mlm **char_mlm0.15_s1**: r=16 probe bits/nt 1.991, rank-1 rate 0.30, exact-extraction rate 0.00
- mlm **char_mlm0.50_s0**: r=16 probe bits/nt 1.940, rank-1 rate 1.00, exact-extraction rate 0.00
- mlm **char_mlm0.50_s1**: r=16 probe bits/nt 1.953, rank-1 rate 0.95, exact-extraction rate 0.00
- **Δ(MLM − AR) r=16 bits/nt = +1.014**  (seed spread: AR ±0.203, MLM ±0.661)

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.