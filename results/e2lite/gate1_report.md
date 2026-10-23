# Gate 1 report

root: outputs/e2lite   scores file: scores_final.json
runs: ar_s0, ar_s1, mlm0.05_s0, mlm0.05_s1, mlm0.15_s0, mlm0.15_s1, mlm0.30_s0, mlm0.30_s1, mlm0.50_s0, mlm0.50_s1, mlm0.80_s0, mlm0.80_s1

## Training and throughput

| run | params | best val (bits/pred) | epoch | train s | score s | MFU (last epoch) |
|---|---|---|---|---|---|---|
| ar_s0 | 12.76M | 2.0012 | 1 | 66 | 25 | 0.34 |
| ar_s1 | 12.76M | 2.0002 | 3 | 66 | 24 | 0.35 |
| mlm0.05_s0 | 12.76M | 1.9999 | 20 | 71 | 2043 | 0.32 |
| mlm0.05_s1 | 12.76M | 1.9999 | 14 | 70 | 2035 | 0.33 |
| mlm0.15_s0 | 12.76M | 2.0000 | 27 | 71 | 2018 | 0.32 |
| mlm0.15_s1 | 12.76M | 2.0000 | 16 | 71 | 2006 | 0.32 |
| mlm0.30_s0 | 12.76M | 2.0002 | 11 | 72 | 2024 | 0.31 |
| mlm0.30_s1 | 12.76M | 2.0001 | 18 | 70 | 2033 | 0.32 |
| mlm0.50_s0 | 12.76M | 2.0002 | 12 | 71 | 2019 | 0.32 |
| mlm0.50_s1 | 12.76M | 2.0001 | 7 | 71 | 2006 | 0.32 |
| mlm0.80_s0 | 12.76M | 2.0002 | 6 | 72 | 2022 | 0.32 |
| mlm0.80_s1 | 12.76M | 2.0003 | 11 | 71 | 2003 | 0.31 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| ar_s0 | ar | 2.0436 | 4.1229 | 1.975 | OK |
| ar_s1 | ar | 2.0430 | 4.1210 | 1.988 | OK |
| mlm0.05_s0 | pll | 2.0002 | 4.0006 | 1.994 | OK |
| mlm0.05_s0 | prefix | 2.0002 | 4.0005 | 1.996 | OK |
| mlm0.05_s1 | pll | 2.0003 | 4.0007 | 1.997 | OK |
| mlm0.05_s1 | prefix | 2.0003 | 4.0007 | 1.996 | OK |
| mlm0.15_s0 | pll | 2.0005 | 4.0015 | 1.994 | OK |
| mlm0.15_s0 | prefix | 2.0004 | 4.0011 | 1.994 | OK |
| mlm0.15_s1 | pll | 2.0006 | 4.0016 | 1.994 | OK |
| mlm0.15_s1 | prefix | 2.0005 | 4.0014 | 1.995 | OK |
| mlm0.30_s0 | pll | 2.0017 | 4.0047 | 1.992 | OK |
| mlm0.30_s0 | prefix | 2.0012 | 4.0034 | 1.991 | OK |
| mlm0.30_s1 | pll | 2.0010 | 4.0029 | 1.991 | OK |
| mlm0.30_s1 | prefix | 2.0008 | 4.0022 | 1.993 | OK |
| mlm0.50_s0 | pll | 2.0040 | 4.0112 | 1.977 | OK |
| mlm0.50_s0 | prefix | 2.0039 | 4.0109 | 1.984 | OK |
| mlm0.50_s1 | pll | 2.0031 | 4.0085 | 1.982 | OK |
| mlm0.50_s1 | prefix | 2.0022 | 4.0062 | 1.987 | OK |
| mlm0.80_s0 | pll | 2.0015 | 4.0040 | 1.991 | OK |
| mlm0.80_s0 | prefix | 2.0014 | 4.0040 | 1.990 | OK |
| mlm0.80_s1 | pll | 2.0010 | 4.0028 | 1.990 | OK |
| mlm0.80_s1 | prefix | 2.0008 | 4.0022 | 1.988 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 213 | 0.00 | 0.00 | 2.032 | +0.13 |
| r=1 | 20 | 73 | 0.05 | 0.10 | 2.009 | +0.49 |
| r=4 | 20 | 1 | 0.75 | 0.80 | 1.905 | +1.93 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.509 | +21.07 |

### ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 2 | 0.50 | 0.60 | 1.946 | +1.36 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 1.813 | +2.60 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.337 | +17.38 |

### ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 258 | 0.00 | 0.00 | 2.088 | -1.07 |
| r=1 | 20 | 102 | 0.05 | 0.15 | 2.008 | +0.43 |
| r=4 | 20 | 1 | 0.60 | 0.85 | 1.913 | +1.92 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.575 | +24.56 |

### ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 3 | 0.25 | 0.55 | 1.957 | +1.34 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 1.857 | +2.98 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.462 | +17.98 |

### mlm0.05_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 232 | 0.03 | 0.03 | 2.000 | +0.15 |
| r=1 | 20 | 181 | 0.00 | 0.00 | 2.000 | +0.18 |
| r=4 | 20 | 132 | 0.00 | 0.00 | 1.998 | +0.66 |
| r=16 | 20 | 36 | 0.35 | 0.35 | 1.996 | +1.65 |

### mlm0.05_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 175 | 0.00 | 0.00 | 2.000 | +0.18 |
| r=4 | 20 | 123 | 0.00 | 0.00 | 1.998 | +0.69 |
| r=16 | 20 | 35 | 0.35 | 0.35 | 1.996 | +1.64 |

### mlm0.05_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 208 | 0.03 | 0.03 | 2.000 | +0.18 |
| r=1 | 20 | 173 | 0.00 | 0.00 | 2.000 | +0.24 |
| r=4 | 20 | 90 | 0.00 | 0.00 | 1.999 | +0.59 |
| r=16 | 20 | 48 | 0.10 | 0.15 | 1.997 | +1.45 |

### mlm0.05_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 172 | 0.00 | 0.00 | 2.000 | +0.25 |
| r=4 | 20 | 91 | 0.00 | 0.00 | 1.999 | +0.56 |
| r=16 | 20 | 50 | 0.05 | 0.10 | 1.997 | +1.45 |

### mlm0.05_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 310 | 0.00 | 0.05 | 2.001 | -0.21 |
| r=1 | 20 | 322 | 0.00 | 0.00 | 2.001 | -0.25 |
| r=4 | 20 | 188 | 0.05 | 0.05 | 1.999 | +0.34 |
| r=16 | 20 | 68 | 0.15 | 0.15 | 1.996 | +1.40 |

### mlm0.05_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 320 | 0.00 | 0.00 | 2.001 | -0.27 |
| r=4 | 20 | 190 | 0.05 | 0.05 | 1.999 | +0.31 |
| r=16 | 20 | 74 | 0.15 | 0.20 | 1.996 | +1.39 |

### mlm0.05_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 308 | 0.00 | 0.03 | 2.001 | -0.20 |
| r=1 | 20 | 341 | 0.00 | 0.00 | 2.001 | -0.29 |
| r=4 | 20 | 232 | 0.05 | 0.05 | 1.999 | +0.30 |
| r=16 | 20 | 79 | 0.15 | 0.25 | 1.997 | +1.29 |

### mlm0.05_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 354 | 0.00 | 0.00 | 2.001 | -0.29 |
| r=4 | 20 | 243 | 0.05 | 0.05 | 1.999 | +0.30 |
| r=16 | 20 | 77 | 0.15 | 0.15 | 1.997 | +1.26 |

### mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 240 | 0.00 | 0.03 | 2.001 | +0.07 |
| r=1 | 20 | 230 | 0.00 | 0.00 | 2.000 | +0.20 |
| r=4 | 20 | 114 | 0.05 | 0.05 | 1.997 | +0.77 |
| r=16 | 20 | 3 | 0.30 | 0.65 | 1.989 | +2.56 |

### mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 203 | 0.00 | 0.00 | 2.000 | +0.24 |
| r=4 | 20 | 112 | 0.05 | 0.10 | 1.997 | +0.75 |
| r=16 | 20 | 3 | 0.30 | 0.65 | 1.989 | +2.56 |

### mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 252 | 0.00 | 0.00 | 2.001 | +0.04 |
| r=1 | 20 | 230 | 0.00 | 0.00 | 2.000 | +0.23 |
| r=4 | 20 | 122 | 0.05 | 0.05 | 1.998 | +0.74 |
| r=16 | 20 | 7 | 0.20 | 0.35 | 1.992 | +2.31 |

### mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 237 | 0.00 | 0.00 | 2.000 | +0.20 |
| r=4 | 20 | 108 | 0.05 | 0.05 | 1.998 | +0.70 |
| r=16 | 20 | 6 | 0.25 | 0.40 | 1.992 | +2.29 |

### mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 263 | 0.00 | 0.03 | 2.001 | -0.03 |
| r=1 | 20 | 256 | 0.00 | 0.00 | 2.000 | +0.10 |
| r=4 | 20 | 150 | 0.05 | 0.10 | 1.998 | +0.62 |
| r=16 | 20 | 2 | 0.40 | 0.70 | 1.988 | +2.91 |

### mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 222 | 0.00 | 0.00 | 2.000 | +0.13 |
| r=4 | 20 | 160 | 0.05 | 0.10 | 1.998 | +0.61 |
| r=16 | 20 | 2 | 0.45 | 0.70 | 1.988 | +2.97 |

### mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 286 | 0.00 | 0.00 | 2.001 | -0.08 |
| r=1 | 20 | 214 | 0.00 | 0.00 | 2.000 | +0.05 |
| r=4 | 20 | 146 | 0.05 | 0.10 | 1.998 | +0.56 |
| r=16 | 20 | 2 | 0.45 | 0.65 | 1.991 | +2.56 |

### mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 184 | 0.00 | 0.00 | 2.000 | +0.09 |
| r=4 | 20 | 168 | 0.10 | 0.10 | 1.998 | +0.58 |
| r=16 | 20 | 2 | 0.45 | 0.65 | 1.991 | +2.58 |

### mlm0.30_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 262 | 0.00 | 0.05 | 2.004 | -0.18 |
| r=1 | 20 | 202 | 0.00 | 0.00 | 2.000 | +0.32 |
| r=4 | 20 | 62 | 0.05 | 0.05 | 1.994 | +1.07 |
| r=16 | 20 | 1 | 0.95 | 0.95 | 1.966 | +4.81 |

### mlm0.30_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 240 | 0.00 | 0.00 | 2.000 | +0.32 |
| r=4 | 20 | 65 | 0.05 | 0.15 | 1.993 | +1.18 |
| r=16 | 20 | 1 | 0.95 | 0.95 | 1.966 | +4.80 |

### mlm0.30_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 332 | 0.00 | 0.00 | 2.004 | -0.24 |
| r=1 | 20 | 216 | 0.00 | 0.00 | 2.001 | +0.19 |
| r=4 | 20 | 107 | 0.05 | 0.05 | 1.996 | +0.84 |
| r=16 | 20 | 1 | 0.65 | 0.85 | 1.977 | +3.62 |

### mlm0.30_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 172 | 0.00 | 0.00 | 2.000 | +0.25 |
| r=4 | 20 | 120 | 0.00 | 0.15 | 1.996 | +0.94 |
| r=16 | 20 | 1 | 0.75 | 0.85 | 1.975 | +3.86 |

### mlm0.30_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 262 | 0.00 | 0.03 | 2.001 | -0.00 |
| r=1 | 20 | 322 | 0.00 | 0.00 | 2.002 | -0.13 |
| r=4 | 20 | 110 | 0.00 | 0.10 | 1.997 | +0.77 |
| r=16 | 20 | 1 | 0.75 | 0.85 | 1.980 | +3.69 |

### mlm0.30_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 307 | 0.00 | 0.00 | 2.001 | -0.02 |
| r=4 | 20 | 78 | 0.05 | 0.10 | 1.996 | +0.87 |
| r=16 | 20 | 1 | 0.70 | 0.90 | 1.980 | +3.76 |

### mlm0.30_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 258 | 0.00 | 0.03 | 2.001 | +0.01 |
| r=1 | 20 | 272 | 0.00 | 0.00 | 2.002 | -0.21 |
| r=4 | 20 | 132 | 0.00 | 0.00 | 1.998 | +0.60 |
| r=16 | 20 | 2 | 0.50 | 0.70 | 1.985 | +2.98 |

### mlm0.30_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 256 | 0.00 | 0.00 | 2.001 | -0.04 |
| r=4 | 20 | 129 | 0.00 | 0.05 | 1.997 | +0.70 |
| r=16 | 20 | 2 | 0.50 | 0.75 | 1.984 | +3.15 |

### mlm0.50_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 320 | 0.00 | 0.00 | 2.007 | -0.23 |
| r=1 | 20 | 242 | 0.00 | 0.05 | 2.004 | +0.07 |
| r=4 | 20 | 65 | 0.00 | 0.15 | 1.993 | +0.96 |
| r=16 | 20 | 1 | 0.90 | 1.00 | 1.922 | +7.03 |

### mlm0.50_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 164 | 0.00 | 0.05 | 2.000 | +0.46 |
| r=4 | 20 | 50 | 0.00 | 0.15 | 1.988 | +1.43 |
| r=16 | 20 | 1 | 0.90 | 1.00 | 1.915 | +7.40 |

### mlm0.50_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 282 | 0.00 | 0.00 | 2.007 | -0.17 |
| r=1 | 20 | 198 | 0.00 | 0.00 | 2.005 | -0.04 |
| r=4 | 20 | 108 | 0.00 | 0.05 | 1.993 | +1.00 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.927 | +6.22 |

### mlm0.50_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 182 | 0.00 | 0.00 | 1.999 | +0.50 |
| r=4 | 20 | 38 | 0.00 | 0.15 | 1.986 | +1.50 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.919 | +6.78 |

### mlm0.50_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 316 | 0.00 | 0.00 | 2.004 | -0.17 |
| r=1 | 20 | 290 | 0.00 | 0.05 | 2.003 | -0.00 |
| r=4 | 20 | 54 | 0.05 | 0.05 | 1.991 | +1.20 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.953 | +5.25 |

### mlm0.50_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 220 | 0.00 | 0.00 | 1.999 | +0.36 |
| r=4 | 20 | 38 | 0.10 | 0.15 | 1.989 | +1.44 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.950 | +5.45 |

### mlm0.50_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 247 | 0.00 | 0.00 | 2.003 | -0.10 |
| r=1 | 20 | 218 | 0.00 | 0.00 | 2.001 | +0.10 |
| r=4 | 20 | 62 | 0.05 | 0.10 | 1.991 | +1.25 |
| r=16 | 20 | 1 | 0.90 | 1.00 | 1.964 | +4.46 |

### mlm0.50_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 131 | 0.00 | 0.00 | 1.998 | +0.44 |
| r=4 | 20 | 22 | 0.10 | 0.20 | 1.988 | +1.65 |
| r=16 | 20 | 1 | 0.95 | 1.00 | 1.962 | +4.56 |

### mlm0.80_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 300 | 0.03 | 0.03 | 2.003 | -0.17 |
| r=1 | 20 | 270 | 0.00 | 0.00 | 2.000 | +0.18 |
| r=4 | 20 | 102 | 0.00 | 0.10 | 1.993 | +1.11 |
| r=16 | 20 | 1 | 0.90 | 1.00 | 1.966 | +4.67 |

### mlm0.80_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 169 | 0.00 | 0.00 | 1.999 | +0.33 |
| r=4 | 20 | 84 | 0.00 | 0.15 | 1.992 | +1.22 |
| r=16 | 20 | 1 | 0.90 | 1.00 | 1.966 | +4.80 |

### mlm0.80_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 311 | 0.00 | 0.00 | 2.003 | -0.19 |
| r=1 | 20 | 213 | 0.00 | 0.00 | 2.001 | +0.17 |
| r=4 | 20 | 50 | 0.00 | 0.10 | 1.993 | +1.22 |
| r=16 | 20 | 1 | 0.95 | 1.00 | 1.967 | +4.92 |

### mlm0.80_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 153 | 0.00 | 0.00 | 2.000 | +0.29 |
| r=4 | 20 | 48 | 0.00 | 0.15 | 1.991 | +1.44 |
| r=16 | 20 | 1 | 0.85 | 1.00 | 1.965 | +5.08 |

### mlm0.80_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 302 | 0.00 | 0.00 | 2.002 | -0.14 |
| r=1 | 20 | 175 | 0.00 | 0.00 | 1.999 | +0.31 |
| r=4 | 20 | 50 | 0.00 | 0.10 | 1.995 | +1.10 |
| r=16 | 20 | 1 | 0.80 | 0.95 | 1.979 | +3.94 |

### mlm0.80_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 172 | 0.00 | 0.00 | 1.999 | +0.40 |
| r=4 | 20 | 70 | 0.15 | 0.20 | 1.994 | +1.19 |
| r=16 | 20 | 1 | 0.80 | 0.95 | 1.978 | +3.97 |

### mlm0.80_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 298 | 0.00 | 0.00 | 2.002 | -0.17 |
| r=1 | 20 | 188 | 0.00 | 0.00 | 1.999 | +0.31 |
| r=4 | 20 | 33 | 0.00 | 0.05 | 1.995 | +1.14 |
| r=16 | 20 | 1 | 0.65 | 0.85 | 1.982 | +3.51 |

### mlm0.80_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 153 | 0.00 | 0.00 | 1.999 | +0.39 |
| r=4 | 20 | 84 | 0.05 | 0.15 | 1.995 | +1.12 |
| r=16 | 20 | 1 | 0.55 | 0.80 | 1.981 | +3.48 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (of 48) |
|---|---|---|---|---|---|
| ar_s0 | train | r=1 | 20 | 0.00 | 35.1 |
| ar_s0 | train | r=4 | 20 | 0.00 | 31.5 |
| ar_s0 | train | r=16 | 20 | 0.95 | 0.1 |
| ar_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| ar_s0 | fresh | r=4 | 20 | 0.00 | 32.9 |
| ar_s0 | fresh | r=16 | 20 | 0.30 | 1.4 |
| ar_s1 | train | r=1 | 20 | 0.00 | 34.5 |
| ar_s1 | train | r=4 | 20 | 0.00 | 31.9 |
| ar_s1 | train | r=16 | 20 | 0.95 | 0.1 |
| ar_s1 | fresh | r=0 | 40 | 0.00 | 36.3 |
| ar_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| ar_s1 | fresh | r=4 | 20 | 0.00 | 32.9 |
| ar_s1 | fresh | r=16 | 20 | 0.55 | 1.1 |
| mlm0.05_s0 | train | r=1 | 20 | 0.00 | 35.8 |
| mlm0.05_s0 | train | r=4 | 20 | 0.00 | 35.0 |
| mlm0.05_s0 | train | r=16 | 20 | 0.00 | 34.7 |
| mlm0.05_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| mlm0.05_s0 | fresh | r=1 | 20 | 0.00 | 35.7 |
| mlm0.05_s0 | fresh | r=4 | 20 | 0.00 | 35.0 |
| mlm0.05_s0 | fresh | r=16 | 20 | 0.00 | 34.6 |
| mlm0.05_s1 | train | r=1 | 20 | 0.00 | 37.5 |
| mlm0.05_s1 | train | r=4 | 20 | 0.00 | 35.6 |
| mlm0.05_s1 | train | r=16 | 20 | 0.00 | 33.5 |
| mlm0.05_s1 | fresh | r=0 | 40 | 0.00 | 35.9 |
| mlm0.05_s1 | fresh | r=1 | 20 | 0.00 | 37.5 |
| mlm0.05_s1 | fresh | r=4 | 20 | 0.00 | 35.5 |
| mlm0.05_s1 | fresh | r=16 | 20 | 0.00 | 33.8 |
| mlm0.15_s0 | train | r=1 | 20 | 0.00 | 35.8 |
| mlm0.15_s0 | train | r=4 | 20 | 0.00 | 34.2 |
| mlm0.15_s0 | train | r=16 | 20 | 0.00 | 33.4 |
| mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| mlm0.15_s0 | fresh | r=4 | 20 | 0.00 | 33.9 |
| mlm0.15_s0 | fresh | r=16 | 20 | 0.00 | 32.9 |
| mlm0.15_s1 | train | r=1 | 20 | 0.00 | 36.1 |
| mlm0.15_s1 | train | r=4 | 20 | 0.00 | 34.0 |
| mlm0.15_s1 | train | r=16 | 20 | 0.00 | 33.5 |
| mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 35.6 |
| mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 36.6 |
| mlm0.15_s1 | fresh | r=4 | 20 | 0.00 | 34.0 |
| mlm0.15_s1 | fresh | r=16 | 20 | 0.00 | 33.2 |
| mlm0.30_s0 | train | r=1 | 20 | 0.00 | 35.5 |
| mlm0.30_s0 | train | r=4 | 20 | 0.00 | 34.6 |
| mlm0.30_s0 | train | r=16 | 20 | 0.00 | 31.9 |
| mlm0.30_s0 | fresh | r=0 | 40 | 0.00 | 36.9 |
| mlm0.30_s0 | fresh | r=1 | 20 | 0.00 | 35.8 |
| mlm0.30_s0 | fresh | r=4 | 20 | 0.00 | 35.1 |
| mlm0.30_s0 | fresh | r=16 | 20 | 0.00 | 31.4 |
| mlm0.30_s1 | train | r=1 | 20 | 0.00 | 36.5 |
| mlm0.30_s1 | train | r=4 | 20 | 0.00 | 34.4 |
| mlm0.30_s1 | train | r=16 | 20 | 0.00 | 32.8 |
| mlm0.30_s1 | fresh | r=0 | 40 | 0.00 | 36.4 |
| mlm0.30_s1 | fresh | r=1 | 20 | 0.00 | 36.1 |
| mlm0.30_s1 | fresh | r=4 | 20 | 0.00 | 34.4 |
| mlm0.30_s1 | fresh | r=16 | 20 | 0.00 | 32.8 |
| mlm0.50_s0 | train | r=1 | 20 | 0.00 | 35.6 |
| mlm0.50_s0 | train | r=4 | 20 | 0.00 | 34.3 |
| mlm0.50_s0 | train | r=16 | 20 | 0.00 | 27.5 |
| mlm0.50_s0 | fresh | r=0 | 40 | 0.00 | 35.6 |
| mlm0.50_s0 | fresh | r=1 | 20 | 0.00 | 36.5 |
| mlm0.50_s0 | fresh | r=4 | 20 | 0.00 | 34.6 |
| mlm0.50_s0 | fresh | r=16 | 20 | 0.00 | 28.9 |
| mlm0.50_s1 | train | r=1 | 20 | 0.00 | 35.6 |
| mlm0.50_s1 | train | r=4 | 20 | 0.00 | 33.9 |
| mlm0.50_s1 | train | r=16 | 20 | 0.00 | 28.9 |
| mlm0.50_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| mlm0.50_s1 | fresh | r=1 | 20 | 0.00 | 35.4 |
| mlm0.50_s1 | fresh | r=4 | 20 | 0.00 | 34.1 |
| mlm0.50_s1 | fresh | r=16 | 20 | 0.00 | 29.4 |
| mlm0.80_s0 | train | r=1 | 20 | 0.00 | 35.3 |
| mlm0.80_s0 | train | r=4 | 20 | 0.00 | 34.0 |
| mlm0.80_s0 | train | r=16 | 20 | 0.00 | 29.4 |
| mlm0.80_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| mlm0.80_s0 | fresh | r=1 | 20 | 0.00 | 36.4 |
| mlm0.80_s0 | fresh | r=4 | 20 | 0.00 | 34.4 |
| mlm0.80_s0 | fresh | r=16 | 20 | 0.00 | 29.6 |
| mlm0.80_s1 | train | r=1 | 20 | 0.00 | 36.4 |
| mlm0.80_s1 | train | r=4 | 20 | 0.00 | 33.9 |
| mlm0.80_s1 | train | r=16 | 20 | 0.00 | 31.4 |
| mlm0.80_s1 | fresh | r=0 | 40 | 0.00 | 36.5 |
| mlm0.80_s1 | fresh | r=1 | 20 | 0.00 | 36.4 |
| mlm0.80_s1 | fresh | r=4 | 20 | 0.00 | 33.7 |
| mlm0.80_s1 | fresh | r=16 | 20 | 0.00 | 30.6 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **mlm0.05_s0 / fresh**: n=100, Spearman(bits) = 0.865, Spearman(rank) = 0.870, rank-1 set Jaccard = 0.22 (8 vs 3 rank-1)
- **mlm0.05_s0 / train**: n=60, Spearman(bits) = 0.861, Spearman(rank) = 0.862, rank-1 set Jaccard = 0.14 (7 vs 1 rank-1)
- **mlm0.05_s1 / fresh**: n=100, Spearman(bits) = 0.972, Spearman(rank) = 0.972, rank-1 set Jaccard = 1.00 (4 vs 4 rank-1)
- **mlm0.05_s1 / train**: n=60, Spearman(bits) = 0.976, Spearman(rank) = 0.976, rank-1 set Jaccard = 1.00 (4 vs 4 rank-1)
- **mlm0.15_s0 / fresh**: n=100, Spearman(bits) = 0.975, Spearman(rank) = 0.973, rank-1 set Jaccard = 0.71 (7 vs 5 rank-1)
- **mlm0.15_s0 / train**: n=60, Spearman(bits) = 0.975, Spearman(rank) = 0.971, rank-1 set Jaccard = 0.86 (7 vs 6 rank-1)
- **mlm0.15_s1 / fresh**: n=100, Spearman(bits) = 0.971, Spearman(rank) = 0.969, rank-1 set Jaccard = 0.58 (9 vs 10 rank-1)
- **mlm0.15_s1 / train**: n=60, Spearman(bits) = 0.973, Spearman(rank) = 0.967, rank-1 set Jaccard = 0.62 (10 vs 11 rank-1)
- **mlm0.30_s0 / fresh**: n=100, Spearman(bits) = 0.898, Spearman(rank) = 0.891, rank-1 set Jaccard = 0.62 (20 vs 14 rank-1)
- **mlm0.30_s0 / train**: n=60, Spearman(bits) = 0.945, Spearman(rank) = 0.943, rank-1 set Jaccard = 0.75 (20 vs 15 rank-1)
- **mlm0.30_s1 / fresh**: n=100, Spearman(bits) = 0.957, Spearman(rank) = 0.955, rank-1 set Jaccard = 0.67 (15 vs 10 rank-1)
- **mlm0.30_s1 / train**: n=60, Spearman(bits) = 0.968, Spearman(rank) = 0.964, rank-1 set Jaccard = 0.67 (15 vs 10 rank-1)
- **mlm0.50_s0 / fresh**: n=100, Spearman(bits) = 0.860, Spearman(rank) = 0.870, rank-1 set Jaccard = 0.90 (18 vs 20 rank-1)
- **mlm0.50_s0 / train**: n=60, Spearman(bits) = 0.897, Spearman(rank) = 0.895, rank-1 set Jaccard = 0.90 (18 vs 20 rank-1)
- **mlm0.50_s1 / fresh**: n=100, Spearman(bits) = 0.859, Spearman(rank) = 0.853, rank-1 set Jaccard = 0.90 (21 vs 19 rank-1)
- **mlm0.50_s1 / train**: n=60, Spearman(bits) = 0.888, Spearman(rank) = 0.893, rank-1 set Jaccard = 0.95 (22 vs 21 rank-1)
- **mlm0.80_s0 / fresh**: n=100, Spearman(bits) = 0.903, Spearman(rank) = 0.901, rank-1 set Jaccard = 0.90 (19 vs 19 rank-1)
- **mlm0.80_s0 / train**: n=60, Spearman(bits) = 0.960, Spearman(rank) = 0.956, rank-1 set Jaccard = 0.94 (18 vs 17 rank-1)
- **mlm0.80_s1 / fresh**: n=100, Spearman(bits) = 0.948, Spearman(rank) = 0.947, rank-1 set Jaccard = 0.81 (16 vs 13 rank-1)
- **mlm0.80_s1 / train**: n=60, Spearman(bits) = 0.933, Spearman(rank) = 0.922, rank-1 set Jaccard = 0.55 (19 vs 12 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **ar_s0** (ar/fresh): bits/nt  r=16 0.509±0.088 | r=1 2.009±0.039 | non-member 2.032±0.040;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.68e-02
- **ar_s1** (ar/fresh): bits/nt  r=16 0.575±0.084 | r=1 2.008±0.041 | non-member 2.088±0.258;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.69e-03
- **mlm0.05_s0** (prefix/fresh): bits/nt  r=16 1.997±0.002 | r=1 2.000±0.003 | non-member 2.000±0.003;  rank-1 rate r=16 0.10, r=1 0.00, non-member 0.03;  MWU p(r=16 < non-member) = 2.88e-05, p(r=1 < non-member) = 3.80e-01
- **mlm0.05_s1** (prefix/fresh): bits/nt  r=16 1.997±0.003 | r=1 2.001±0.003 | non-member 2.001±0.003;  rank-1 rate r=16 0.15, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.79e-06, p(r=1 < non-member) = 6.78e-01
- **mlm0.15_s0** (prefix/fresh): bits/nt  r=16 1.992±0.004 | r=1 2.000±0.004 | non-member 2.001±0.004;  rank-1 rate r=16 0.20, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.56e-09, p(r=1 < non-member) = 4.91e-01
- **mlm0.15_s1** (prefix/fresh): bits/nt  r=16 1.991±0.003 | r=1 2.000±0.004 | non-member 2.001±0.004;  rank-1 rate r=16 0.45, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.95e-09, p(r=1 < non-member) = 2.58e-01
- **mlm0.30_s0** (prefix/fresh): bits/nt  r=16 1.977±0.008 | r=1 2.001±0.005 | non-member 2.004±0.008;  rank-1 rate r=16 0.65, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.15e-10, p(r=1 < non-member) = 4.75e-02
- **mlm0.30_s1** (prefix/fresh): bits/nt  r=16 1.985±0.006 | r=1 2.002±0.006 | non-member 2.001±0.005;  rank-1 rate r=16 0.50, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 9.98e-10, p(r=1 < non-member) = 6.50e-01
- **mlm0.50_s0** (prefix/fresh): bits/nt  r=16 1.927±0.022 | r=1 2.005±0.011 | non-member 2.007±0.013;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.38e-01
- **mlm0.50_s1** (prefix/fresh): bits/nt  r=16 1.964±0.009 | r=1 2.001±0.007 | non-member 2.003±0.007;  rank-1 rate r=16 0.90, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.10e-01
- **mlm0.80_s0** (prefix/fresh): bits/nt  r=16 1.967±0.007 | r=1 2.001±0.007 | non-member 2.003±0.008;  rank-1 rate r=16 0.95, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.07e-10, p(r=1 < non-member) = 8.02e-02
- **mlm0.80_s1** (prefix/fresh): bits/nt  r=16 1.982±0.007 | r=1 1.999±0.004 | non-member 2.002±0.006;  rank-1 rate r=16 0.65, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.79e-10, p(r=1 < non-member) = 1.38e-02

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **ar_s0**: r=16 probe bits/nt 0.337, rank-1 rate 1.00, exact-extraction rate 0.95
- ar  **ar_s1**: r=16 probe bits/nt 0.462, rank-1 rate 1.00, exact-extraction rate 0.95
- mlm **mlm0.05_s0**: r=16 probe bits/nt 1.997, rank-1 rate 0.05, exact-extraction rate 0.00
- mlm **mlm0.05_s1**: r=16 probe bits/nt 1.997, rank-1 rate 0.15, exact-extraction rate 0.00
- mlm **mlm0.15_s0**: r=16 probe bits/nt 1.992, rank-1 rate 0.25, exact-extraction rate 0.00
- mlm **mlm0.15_s1**: r=16 probe bits/nt 1.991, rank-1 rate 0.45, exact-extraction rate 0.00
- mlm **mlm0.30_s0**: r=16 probe bits/nt 1.975, rank-1 rate 0.75, exact-extraction rate 0.00
- mlm **mlm0.30_s1**: r=16 probe bits/nt 1.984, rank-1 rate 0.50, exact-extraction rate 0.00
- mlm **mlm0.50_s0**: r=16 probe bits/nt 1.919, rank-1 rate 1.00, exact-extraction rate 0.00
- mlm **mlm0.50_s1**: r=16 probe bits/nt 1.962, rank-1 rate 0.95, exact-extraction rate 0.00
- mlm **mlm0.80_s0**: r=16 probe bits/nt 1.965, rank-1 rate 0.85, exact-extraction rate 0.00
- mlm **mlm0.80_s1**: r=16 probe bits/nt 1.981, rank-1 rate 0.55, exact-extraction rate 0.00
- **Δ(MLM − AR) r=16 bits/nt = +1.577**  (seed spread: AR ±0.063, MLM ±0.022)

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.