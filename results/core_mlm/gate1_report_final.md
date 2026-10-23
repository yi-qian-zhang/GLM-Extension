# Gate 1 report

root: outputs/core_mlm   scores file: scores_final.json
runs: 3mer_mlm0.15_s0, 3mer_mlm0.15_s1, 3mer_mlm0.5_s0, 3mer_mlm0.5_s1, 6mer_mlm0.15_s0, 6mer_mlm0.15_s1, 6mer_mlm0.5_s0, 6mer_mlm0.5_s1, char_mlm0.15_s0, char_mlm0.15_s1, char_mlm0.5_s0, char_mlm0.5_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | 3mer | 12.69M (12.61M) | 2760 | 2.5M | 36 | 241 | 0.23 |
| 3mer_mlm0.15_s1 | 3mer | 12.69M (12.61M) | 2760 | 2.5M | 36 | 243 | 0.22 |
| 3mer_mlm0.5_s0 | 3mer | 12.69M (12.61M) | 2760 | 8.4M | 33 | 241 | 0.25 |
| 3mer_mlm0.5_s1 | 3mer | 12.69M (12.61M) | 2760 | 8.4M | 34 | 243 | 0.25 |
| 6mer_mlm0.15_s0 | 6mer | 14.73M (12.61M) | 2760 | 1.3M | 34 | 72 | 0.14 |
| 6mer_mlm0.15_s1 | 6mer | 14.73M (12.61M) | 2760 | 1.3M | 34 | 73 | 0.14 |
| 6mer_mlm0.5_s0 | 6mer | 14.73M (12.61M) | 2760 | 4.2M | 34 | 72 | 0.14 |
| 6mer_mlm0.5_s1 | 6mer | 14.73M (12.61M) | 2760 | 4.2M | 34 | 73 | 0.14 |
| char_mlm0.15_s0 | char | 12.76M (12.61M) | 2760 | 7.6M | 76 | 2116 | 0.32 |
| char_mlm0.15_s1 | char | 12.76M (12.61M) | 2760 | 7.6M | 77 | 2135 | 0.32 |
| char_mlm0.5_s0 | char | 12.76M (12.61M) | 2760 | 25.2M | 77 | 2117 | 0.32 |
| char_mlm0.5_s1 | char | 12.76M (12.61M) | 2760 | 25.2M | 77 | 2135 | 0.32 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | pll | 2.0066 | 4.0184 | 1.982 | OK |
| 3mer_mlm0.15_s0 | prefix | 2.0037 | 4.0102 | 1.986 | OK |
| 3mer_mlm0.15_s1 | pll | 2.0057 | 4.0160 | 1.981 | OK |
| 3mer_mlm0.15_s1 | prefix | 2.0043 | 4.0120 | 1.983 | OK |
| 3mer_mlm0.5_s0 | pll | 2.0179 | 4.0500 | 1.971 | OK |
| 3mer_mlm0.5_s0 | prefix | 2.0113 | 4.0316 | 1.980 | OK |
| 3mer_mlm0.5_s1 | pll | 2.0117 | 4.0327 | 1.978 | OK |
| 3mer_mlm0.5_s1 | prefix | 2.0083 | 4.0230 | 1.979 | OK |
| 6mer_mlm0.15_s0 | pll | 2.0316 | 4.0885 | 1.981 | OK |
| 6mer_mlm0.15_s0 | prefix | 2.0236 | 4.0659 | 1.977 | OK |
| 6mer_mlm0.15_s1 | pll | 2.0328 | 4.0919 | 1.979 | OK |
| 6mer_mlm0.15_s1 | prefix | 2.0277 | 4.0776 | 1.984 | OK |
| 6mer_mlm0.5_s0 | pll | 2.0438 | 4.1234 | 1.990 | OK |
| 6mer_mlm0.5_s0 | prefix | 2.0420 | 4.1182 | 1.988 | OK |
| 6mer_mlm0.5_s1 | pll | 2.0448 | 4.1263 | 1.970 | OK |
| 6mer_mlm0.5_s1 | prefix | 2.0431 | 4.1213 | 1.988 | OK |
| char_mlm0.15_s0 | pll | 2.0004 | 4.0010 | 1.995 | OK |
| char_mlm0.15_s0 | prefix | 2.0003 | 4.0008 | 1.995 | OK |
| char_mlm0.15_s1 | pll | 2.0003 | 4.0009 | 1.994 | OK |
| char_mlm0.15_s1 | prefix | 2.0003 | 4.0009 | 1.993 | OK |
| char_mlm0.5_s0 | pll | 2.0011 | 4.0032 | 1.991 | OK |
| char_mlm0.5_s0 | prefix | 2.0011 | 4.0031 | 1.990 | OK |
| char_mlm0.5_s1 | pll | 2.0016 | 4.0045 | 1.990 | OK |
| char_mlm0.5_s1 | prefix | 2.0016 | 4.0045 | 1.991 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 125 | 0.00 | 0.00 | 2.004 | +0.17 |
| r=1 | 40 | 130 | 0.00 | 0.00 | 2.007 | -0.00 |
| r=4 | 40 | 136 | 0.00 | 0.00 | 2.008 | -0.08 |
| r=16 | 40 | 152 | 0.00 | 0.03 | 2.008 | -0.09 |

### 3mer_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 49 | 0.05 | 0.10 | 1.993 | +0.95 |
| r=4 | 40 | 38 | 0.07 | 0.10 | 1.992 | +1.01 |
| r=16 | 40 | 50 | 0.03 | 0.05 | 1.993 | +0.97 |

### 3mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 134 | 0.00 | 0.03 | 2.002 | +0.17 |
| r=1 | 40 | 140 | 0.00 | 0.00 | 2.004 | -0.01 |
| r=4 | 40 | 152 | 0.00 | 0.00 | 2.006 | -0.24 |
| r=16 | 40 | 168 | 0.00 | 0.00 | 2.003 | +0.12 |

### 3mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 90 | 0.03 | 0.07 | 1.997 | +0.62 |
| r=4 | 40 | 84 | 0.03 | 0.03 | 1.998 | +0.59 |
| r=16 | 40 | 64 | 0.03 | 0.03 | 1.997 | +0.66 |

### 3mer_mlm0.15_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 108 | 0.00 | 0.00 | 2.002 | +0.24 |
| r=1 | 40 | 178 | 0.00 | 0.00 | 2.009 | -0.22 |
| r=4 | 40 | 166 | 0.00 | 0.03 | 2.005 | +0.01 |
| r=16 | 40 | 140 | 0.00 | 0.00 | 2.007 | -0.10 |

### 3mer_mlm0.15_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 47 | 0.00 | 0.10 | 1.994 | +0.86 |
| r=4 | 40 | 60 | 0.05 | 0.10 | 1.995 | +0.86 |
| r=16 | 40 | 65 | 0.03 | 0.07 | 1.995 | +0.81 |

### 3mer_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 120 | 0.00 | 0.00 | 2.002 | +0.19 |
| r=1 | 40 | 160 | 0.00 | 0.00 | 2.006 | -0.15 |
| r=4 | 40 | 166 | 0.00 | 0.00 | 2.005 | -0.08 |
| r=16 | 40 | 139 | 0.00 | 0.00 | 2.005 | -0.03 |

### 3mer_mlm0.15_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 99 | 0.00 | 0.00 | 2.000 | +0.41 |
| r=4 | 40 | 70 | 0.05 | 0.07 | 1.997 | +0.69 |
| r=16 | 40 | 94 | 0.03 | 0.05 | 1.998 | +0.61 |

### 3mer_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 157 | 0.00 | 0.03 | 2.021 | -0.14 |
| r=1 | 40 | 170 | 0.00 | 0.00 | 2.021 | -0.15 |
| r=4 | 40 | 147 | 0.00 | 0.00 | 2.019 | -0.04 |
| r=16 | 40 | 132 | 0.03 | 0.05 | 2.017 | +0.07 |

### 3mer_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 20 | 0.05 | 0.12 | 1.984 | +1.50 |
| r=4 | 40 | 14 | 0.12 | 0.23 | 1.987 | +1.35 |
| r=16 | 40 | 23 | 0.15 | 0.30 | 1.980 | +1.67 |

### 3mer_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 152 | 0.00 | 0.00 | 2.015 | -0.22 |
| r=1 | 40 | 143 | 0.00 | 0.03 | 2.011 | +0.03 |
| r=4 | 40 | 174 | 0.00 | 0.00 | 2.013 | -0.15 |
| r=16 | 40 | 126 | 0.00 | 0.03 | 2.009 | +0.15 |

### 3mer_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 29 | 0.05 | 0.20 | 1.991 | +1.09 |
| r=4 | 40 | 52 | 0.07 | 0.10 | 1.993 | +0.98 |
| r=16 | 40 | 29 | 0.05 | 0.15 | 1.988 | +1.28 |

### 3mer_mlm0.5_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 178 | 0.00 | 0.00 | 2.013 | -0.05 |
| r=1 | 40 | 146 | 0.00 | 0.00 | 2.011 | +0.03 |
| r=4 | 40 | 111 | 0.00 | 0.00 | 2.007 | +0.24 |
| r=16 | 40 | 146 | 0.00 | 0.00 | 2.012 | +0.01 |

### 3mer_mlm0.5_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 20 | 0.07 | 0.12 | 1.986 | +1.39 |
| r=4 | 40 | 28 | 0.17 | 0.17 | 1.984 | +1.51 |
| r=16 | 40 | 25 | 0.10 | 0.23 | 1.986 | +1.39 |

### 3mer_mlm0.5_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 142 | 0.00 | 0.03 | 2.008 | +0.02 |
| r=1 | 40 | 149 | 0.00 | 0.00 | 2.009 | -0.04 |
| r=4 | 40 | 125 | 0.00 | 0.00 | 2.005 | +0.16 |
| r=16 | 40 | 154 | 0.00 | 0.00 | 2.008 | +0.02 |

### 3mer_mlm0.5_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 33 | 0.07 | 0.10 | 1.989 | +1.20 |
| r=4 | 40 | 58 | 0.05 | 0.12 | 1.993 | +0.96 |
| r=16 | 40 | 38 | 0.05 | 0.12 | 1.992 | +1.00 |

### 6mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 148 | 0.00 | 0.00 | 2.030 | +0.05 |
| r=1 | 40 | 172 | 0.00 | 0.03 | 2.034 | -0.14 |
| r=4 | 40 | 102 | 0.00 | 0.00 | 2.022 | +0.31 |
| r=16 | 40 | 104 | 0.03 | 0.05 | 2.025 | +0.21 |

### 6mer_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 4 | 0.38 | 0.50 | 1.960 | +2.39 |
| r=4 | 40 | 2 | 0.50 | 0.75 | 1.942 | +3.02 |
| r=16 | 40 | 1 | 0.55 | 0.68 | 1.931 | +3.33 |

### 6mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 164 | 0.00 | 0.00 | 2.023 | -0.10 |
| r=1 | 40 | 142 | 0.00 | 0.00 | 2.020 | +0.05 |
| r=4 | 40 | 174 | 0.00 | 0.03 | 2.025 | -0.14 |
| r=16 | 40 | 84 | 0.00 | 0.05 | 2.008 | +0.53 |

### 6mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 28 | 0.12 | 0.20 | 1.987 | +1.41 |
| r=4 | 40 | 14 | 0.15 | 0.25 | 1.977 | +1.73 |
| r=16 | 40 | 4 | 0.33 | 0.45 | 1.963 | +2.30 |

### 6mer_mlm0.15_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 162 | 0.00 | 0.00 | 2.033 | -0.03 |
| r=1 | 40 | 134 | 0.00 | 0.00 | 2.029 | +0.07 |
| r=4 | 40 | 162 | 0.00 | 0.00 | 2.039 | -0.25 |
| r=16 | 40 | 133 | 0.00 | 0.00 | 2.030 | +0.11 |

### 6mer_mlm0.15_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 2 | 0.50 | 0.65 | 1.945 | +2.89 |
| r=4 | 40 | 1 | 0.62 | 0.75 | 1.935 | +3.20 |
| r=16 | 40 | 1 | 0.60 | 0.78 | 1.922 | +3.63 |

### 6mer_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 112 | 0.03 | 0.03 | 2.024 | +0.07 |
| r=1 | 40 | 140 | 0.00 | 0.03 | 2.023 | +0.16 |
| r=4 | 40 | 134 | 0.00 | 0.00 | 2.025 | +0.07 |
| r=16 | 40 | 116 | 0.00 | 0.00 | 2.018 | +0.42 |

### 6mer_mlm0.15_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 23 | 0.17 | 0.28 | 1.988 | +1.32 |
| r=4 | 40 | 8 | 0.17 | 0.28 | 1.973 | +1.96 |
| r=16 | 40 | 14 | 0.30 | 0.40 | 1.964 | +2.22 |

### 6mer_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 156 | 0.00 | 0.00 | 2.041 | +0.10 |
| r=1 | 40 | 170 | 0.00 | 0.03 | 2.052 | -0.19 |
| r=4 | 40 | 123 | 0.05 | 0.07 | 2.035 | +0.25 |
| r=16 | 40 | 80 | 0.07 | 0.17 | 2.016 | +0.80 |

### 6mer_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 1 | 0.72 | 0.82 | 1.923 | +3.40 |
| r=4 | 40 | 1 | 0.62 | 0.78 | 1.933 | +3.17 |
| r=16 | 40 | 1 | 0.72 | 0.78 | 1.914 | +3.58 |

### 6mer_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 149 | 0.00 | 0.00 | 2.038 | +0.14 |
| r=1 | 40 | 158 | 0.00 | 0.00 | 2.044 | -0.04 |
| r=4 | 40 | 140 | 0.03 | 0.07 | 2.036 | +0.16 |
| r=16 | 40 | 83 | 0.07 | 0.12 | 2.019 | +0.67 |

### 6mer_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 1 | 0.62 | 0.75 | 1.937 | +3.03 |
| r=4 | 40 | 1 | 0.55 | 0.72 | 1.942 | +2.90 |
| r=16 | 40 | 1 | 0.60 | 0.78 | 1.923 | +3.35 |

### 6mer_mlm0.5_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 138 | 0.00 | 0.00 | 2.040 | +0.14 |
| r=1 | 40 | 182 | 0.00 | 0.03 | 2.049 | -0.13 |
| r=4 | 40 | 130 | 0.00 | 0.00 | 2.044 | +0.00 |
| r=16 | 40 | 153 | 0.00 | 0.03 | 2.044 | +0.07 |

### 6mer_mlm0.5_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 1 | 0.65 | 0.82 | 1.926 | +3.30 |
| r=4 | 40 | 1 | 0.70 | 0.82 | 1.924 | +3.37 |
| r=16 | 40 | 1 | 0.72 | 0.80 | 1.916 | +3.59 |

### 6mer_mlm0.5_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 108 | 0.00 | 0.00 | 2.041 | +0.07 |
| r=1 | 40 | 173 | 0.00 | 0.03 | 2.046 | -0.08 |
| r=4 | 40 | 144 | 0.00 | 0.00 | 2.043 | -0.00 |
| r=16 | 40 | 148 | 0.00 | 0.00 | 2.041 | +0.08 |

### 6mer_mlm0.5_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 1 | 0.55 | 0.75 | 1.935 | +3.06 |
| r=4 | 40 | 1 | 0.70 | 0.80 | 1.933 | +3.17 |
| r=16 | 40 | 1 | 0.65 | 0.75 | 1.920 | +3.46 |

### char_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 186 | 0.00 | 0.03 | 2.000 | -0.05 |
| r=1 | 40 | 190 | 0.00 | 0.00 | 2.000 | -0.03 |
| r=4 | 40 | 143 | 0.00 | 0.00 | 2.000 | +0.13 |
| r=16 | 40 | 152 | 0.00 | 0.03 | 2.001 | -0.12 |

### char_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 128 | 0.03 | 0.03 | 1.999 | +0.26 |
| r=4 | 40 | 122 | 0.00 | 0.00 | 2.000 | +0.08 |
| r=16 | 40 | 85 | 0.00 | 0.05 | 1.999 | +0.46 |

### char_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 186 | 0.00 | 0.03 | 2.000 | -0.08 |
| r=1 | 40 | 178 | 0.00 | 0.00 | 2.000 | -0.04 |
| r=4 | 40 | 142 | 0.00 | 0.00 | 2.000 | +0.08 |
| r=16 | 40 | 163 | 0.00 | 0.00 | 2.001 | -0.13 |

### char_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 130 | 0.03 | 0.03 | 1.999 | +0.27 |
| r=4 | 40 | 124 | 0.00 | 0.00 | 2.000 | +0.15 |
| r=16 | 40 | 87 | 0.00 | 0.00 | 1.999 | +0.40 |

### char_mlm0.15_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 127 | 0.00 | 0.00 | 2.000 | +0.20 |
| r=1 | 40 | 154 | 0.00 | 0.00 | 2.000 | -0.01 |
| r=4 | 40 | 153 | 0.00 | 0.03 | 2.001 | -0.00 |
| r=16 | 40 | 174 | 0.00 | 0.00 | 2.001 | -0.12 |

### char_mlm0.15_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 109 | 0.00 | 0.05 | 1.999 | +0.43 |
| r=4 | 40 | 138 | 0.00 | 0.05 | 2.000 | +0.27 |
| r=16 | 40 | 127 | 0.00 | 0.00 | 2.000 | +0.24 |

### char_mlm0.15_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 158 | 0.00 | 0.03 | 2.000 | +0.03 |
| r=1 | 40 | 157 | 0.00 | 0.00 | 2.000 | -0.01 |
| r=4 | 40 | 166 | 0.00 | 0.05 | 2.001 | -0.06 |
| r=16 | 40 | 174 | 0.00 | 0.00 | 2.001 | -0.08 |

### char_mlm0.15_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 107 | 0.00 | 0.00 | 1.999 | +0.33 |
| r=4 | 40 | 148 | 0.00 | 0.03 | 2.000 | +0.17 |
| r=16 | 40 | 128 | 0.00 | 0.00 | 2.000 | +0.18 |

### char_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 159 | 0.00 | 0.03 | 2.002 | -0.07 |
| r=1 | 40 | 162 | 0.00 | 0.00 | 2.001 | -0.04 |
| r=4 | 40 | 142 | 0.00 | 0.03 | 2.001 | +0.08 |
| r=16 | 40 | 144 | 0.00 | 0.00 | 2.000 | +0.09 |

### char_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 94 | 0.00 | 0.00 | 1.999 | +0.39 |
| r=4 | 40 | 113 | 0.00 | 0.05 | 1.998 | +0.45 |
| r=16 | 40 | 74 | 0.05 | 0.07 | 1.997 | +0.75 |

### char_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 167 | 0.00 | 0.00 | 2.002 | -0.05 |
| r=1 | 40 | 127 | 0.00 | 0.00 | 2.001 | +0.01 |
| r=4 | 40 | 135 | 0.00 | 0.00 | 2.001 | +0.04 |
| r=16 | 40 | 134 | 0.00 | 0.05 | 2.000 | +0.28 |

### char_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 106 | 0.03 | 0.03 | 1.999 | +0.36 |
| r=4 | 40 | 149 | 0.00 | 0.03 | 2.000 | +0.23 |
| r=16 | 40 | 80 | 0.03 | 0.05 | 1.998 | +0.60 |

### char_mlm0.5_s1 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 155 | 0.00 | 0.00 | 2.000 | +0.30 |
| r=1 | 40 | 156 | 0.00 | 0.00 | 2.002 | -0.01 |
| r=4 | 40 | 124 | 0.00 | 0.00 | 2.002 | +0.03 |
| r=16 | 40 | 150 | 0.00 | 0.00 | 2.002 | +0.03 |

### char_mlm0.5_s1 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 69 | 0.00 | 0.07 | 1.997 | +0.70 |
| r=4 | 40 | 62 | 0.03 | 0.03 | 1.998 | +0.65 |
| r=16 | 40 | 64 | 0.03 | 0.03 | 1.998 | +0.63 |

### char_mlm0.5_s1 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 154 | 0.00 | 0.00 | 2.001 | +0.08 |
| r=1 | 40 | 135 | 0.00 | 0.00 | 2.001 | +0.08 |
| r=4 | 40 | 145 | 0.00 | 0.00 | 2.002 | -0.09 |
| r=16 | 40 | 168 | 0.00 | 0.00 | 2.001 | +0.05 |

### char_mlm0.5_s1 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 79 | 0.00 | 0.05 | 1.998 | +0.58 |
| r=4 | 40 | 78 | 0.00 | 0.00 | 1.998 | +0.47 |
| r=16 | 40 | 82 | 0.03 | 0.05 | 1.998 | +0.57 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 35.4 |
| 3mer_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 36.5 |
| 3mer_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 36.2 |
| 3mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 35.4 |
| 3mer_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 36.0 |
| 3mer_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 36.5 |
| 3mer_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 36.4 |
| 3mer_mlm0.15_s1 | train | r=1 | 40 | 0.00 | 36.4 |
| 3mer_mlm0.15_s1 | train | r=4 | 40 | 0.00 | 35.8 |
| 3mer_mlm0.15_s1 | train | r=16 | 40 | 0.00 | 36.0 |
| 3mer_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 3mer_mlm0.15_s1 | fresh | r=1 | 40 | 0.00 | 35.4 |
| 3mer_mlm0.15_s1 | fresh | r=4 | 40 | 0.00 | 37.3 |
| 3mer_mlm0.15_s1 | fresh | r=16 | 40 | 0.00 | 36.3 |
| 3mer_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 35.3 |
| 3mer_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 35.5 |
| 3mer_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 35.8 |
| 3mer_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 36.4 |
| 3mer_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 35.9 |
| 3mer_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 36.1 |
| 3mer_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 36.4 |
| 3mer_mlm0.5_s1 | train | r=1 | 40 | 0.00 | 35.5 |
| 3mer_mlm0.5_s1 | train | r=4 | 40 | 0.00 | 36.0 |
| 3mer_mlm0.5_s1 | train | r=16 | 40 | 0.00 | 36.2 |
| 3mer_mlm0.5_s1 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 3mer_mlm0.5_s1 | fresh | r=1 | 40 | 0.00 | 36.3 |
| 3mer_mlm0.5_s1 | fresh | r=4 | 40 | 0.00 | 36.4 |
| 3mer_mlm0.5_s1 | fresh | r=16 | 40 | 0.00 | 37.0 |
| 6mer_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 35.9 |
| 6mer_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 37.3 |
| 6mer_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 36.6 |
| 6mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 34.7 |
| 6mer_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 35.8 |
| 6mer_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 36.5 |
| 6mer_mlm0.15_s1 | train | r=1 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.15_s1 | train | r=4 | 40 | 0.00 | 36.4 |
| 6mer_mlm0.15_s1 | train | r=16 | 40 | 0.00 | 35.5 |
| 6mer_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 36.3 |
| 6mer_mlm0.15_s1 | fresh | r=1 | 40 | 0.00 | 35.4 |
| 6mer_mlm0.15_s1 | fresh | r=4 | 40 | 0.00 | 36.8 |
| 6mer_mlm0.15_s1 | fresh | r=16 | 40 | 0.00 | 36.1 |
| 6mer_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 35.6 |
| 6mer_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 35.6 |
| 6mer_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 35.5 |
| 6mer_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 36.8 |
| 6mer_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 35.3 |
| 6mer_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 35.9 |
| 6mer_mlm0.5_s1 | train | r=1 | 40 | 0.00 | 36.8 |
| 6mer_mlm0.5_s1 | train | r=4 | 40 | 0.00 | 35.3 |
| 6mer_mlm0.5_s1 | train | r=16 | 40 | 0.00 | 35.1 |
| 6mer_mlm0.5_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.5_s1 | fresh | r=1 | 40 | 0.00 | 35.4 |
| 6mer_mlm0.5_s1 | fresh | r=4 | 40 | 0.00 | 35.1 |
| 6mer_mlm0.5_s1 | fresh | r=16 | 40 | 0.00 | 36.2 |
| char_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 35.4 |
| char_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 35.0 |
| char_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 35.8 |
| char_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 36.0 |
| char_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 35.6 |
| char_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 35.5 |
| char_mlm0.15_s1 | train | r=1 | 40 | 0.00 | 35.4 |
| char_mlm0.15_s1 | train | r=4 | 40 | 0.00 | 35.1 |
| char_mlm0.15_s1 | train | r=16 | 40 | 0.00 | 35.8 |
| char_mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 36.4 |
| char_mlm0.15_s1 | fresh | r=1 | 40 | 0.00 | 36.0 |
| char_mlm0.15_s1 | fresh | r=4 | 40 | 0.00 | 36.4 |
| char_mlm0.15_s1 | fresh | r=16 | 40 | 0.00 | 36.8 |
| char_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 35.5 |
| char_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 35.6 |
| char_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 35.1 |
| char_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 37.2 |
| char_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 35.5 |
| char_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 35.6 |
| char_mlm0.5_s1 | train | r=1 | 40 | 0.00 | 34.9 |
| char_mlm0.5_s1 | train | r=4 | 40 | 0.00 | 35.5 |
| char_mlm0.5_s1 | train | r=16 | 40 | 0.00 | 35.4 |
| char_mlm0.5_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_mlm0.5_s1 | fresh | r=1 | 40 | 0.00 | 35.8 |
| char_mlm0.5_s1 | fresh | r=4 | 40 | 0.00 | 36.1 |
| char_mlm0.5_s1 | fresh | r=16 | 40 | 0.00 | 36.4 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **3mer_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.652, Spearman(rank) = 0.653, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **3mer_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.648, Spearman(rank) = 0.650, rank-1 set Jaccard = 0.29 (6 vs 3 rank-1)
- **3mer_mlm0.15_s1 / fresh**: n=160, Spearman(bits) = 0.651, Spearman(rank) = 0.642, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **3mer_mlm0.15_s1 / train**: n=120, Spearman(bits) = 0.602, Spearman(rank) = 0.597, rank-1 set Jaccard = 0.50 (3 vs 3 rank-1)
- **3mer_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.769, Spearman(rank) = 0.784, rank-1 set Jaccard = 0.00 (1 vs 0 rank-1)
- **3mer_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.619, Spearman(rank) = 0.620, rank-1 set Jaccard = 0.18 (13 vs 7 rank-1)
- **3mer_mlm0.5_s1 / fresh**: n=160, Spearman(bits) = 0.725, Spearman(rank) = 0.730, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **3mer_mlm0.5_s1 / train**: n=120, Spearman(bits) = 0.647, Spearman(rank) = 0.648, rank-1 set Jaccard = 0.17 (14 vs 7 rank-1)
- **6mer_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.534, Spearman(rank) = 0.548, rank-1 set Jaccard = 0.00 (1 vs 0 rank-1)
- **6mer_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.552, Spearman(rank) = 0.467, rank-1 set Jaccard = 0.35 (57 vs 24 rank-1)
- **6mer_mlm0.15_s1 / fresh**: n=160, Spearman(bits) = 0.536, Spearman(rank) = 0.518, rank-1 set Jaccard = 0.00 (0 vs 1 rank-1)
- **6mer_mlm0.15_s1 / train**: n=120, Spearman(bits) = 0.511, Spearman(rank) = 0.479, rank-1 set Jaccard = 0.36 (69 vs 26 rank-1)
- **6mer_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.865, Spearman(rank) = 0.872, rank-1 set Jaccard = 0.29 (5 vs 4 rank-1)
- **6mer_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.864, Spearman(rank) = 0.705, rank-1 set Jaccard = 0.75 (83 vs 71 rank-1)
- **6mer_mlm0.5_s1 / fresh**: n=160, Spearman(bits) = 0.910, Spearman(rank) = 0.903, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **6mer_mlm0.5_s1 / train**: n=120, Spearman(bits) = 0.881, Spearman(rank) = 0.706, rank-1 set Jaccard = 0.77 (83 vs 76 rank-1)
- **char_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.944, Spearman(rank) = 0.944, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.938, Spearman(rank) = 0.934, rank-1 set Jaccard = 1.00 (1 vs 1 rank-1)
- **char_mlm0.15_s1 / fresh**: n=160, Spearman(bits) = 0.893, Spearman(rank) = 0.898, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.15_s1 / train**: n=120, Spearman(bits) = 0.945, Spearman(rank) = 0.940, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.707, Spearman(rank) = 0.721, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.720, Spearman(rank) = 0.725, rank-1 set Jaccard = 0.33 (2 vs 2 rank-1)
- **char_mlm0.5_s1 / fresh**: n=160, Spearman(bits) = 0.746, Spearman(rank) = 0.747, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.5_s1 / train**: n=120, Spearman(bits) = 0.739, Spearman(rank) = 0.728, rank-1 set Jaccard = 0.50 (2 vs 1 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.003±0.011 | r=1 2.004±0.012 | non-member 2.002±0.010;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.73e-01, p(r=1 < non-member) = 7.60e-01
- **3mer_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 2.005±0.011 | r=1 2.006±0.012 | non-member 2.002±0.010;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.33e-01, p(r=1 < non-member) = 9.10e-01
- **3mer_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.009±0.022 | r=1 2.011±0.020 | non-member 2.015±0.018;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.07e-02, p(r=1 < non-member) = 2.03e-01
- **3mer_mlm0.5_s1** (prefix/fresh): bits/nt  r=16 2.008±0.013 | r=1 2.009±0.015 | non-member 2.008±0.016;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.67e-01, p(r=1 < non-member) = 5.25e-01
- **6mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.008±0.030 | r=1 2.020±0.025 | non-member 2.023±0.022;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.26e-03, p(r=1 < non-member) = 2.05e-01
- **6mer_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 2.018±0.026 | r=1 2.023±0.033 | non-member 2.024±0.028;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.03;  MWU p(r=16 < non-member) = 1.06e-01, p(r=1 < non-member) = 4.67e-01
- **6mer_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.019±0.053 | r=1 2.044±0.035 | non-member 2.038±0.032;  rank-1 rate r=16 0.07, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.56e-02, p(r=1 < non-member) = 7.84e-01
- **6mer_mlm0.5_s1** (prefix/fresh): bits/nt  r=16 2.041±0.042 | r=1 2.046±0.036 | non-member 2.041±0.041;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 5.25e-01, p(r=1 < non-member) = 7.54e-01
- **char_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.001±0.003 | r=1 2.000±0.003 | non-member 2.000±0.003;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 5.25e-01, p(r=1 < non-member) = 3.38e-01
- **char_mlm0.15_s1** (prefix/fresh): bits/nt  r=16 2.001±0.003 | r=1 2.000±0.003 | non-member 2.000±0.003;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.69e-01, p(r=1 < non-member) = 5.33e-01
- **char_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.000±0.006 | r=1 2.001±0.005 | non-member 2.002±0.005;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.27e-02, p(r=1 < non-member) = 3.20e-01
- **char_mlm0.5_s1** (prefix/fresh): bits/nt  r=16 2.001±0.008 | r=1 2.001±0.006 | non-member 2.001±0.005;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.41e-01, p(r=1 < non-member) = 3.85e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- mlm **3mer_mlm0.15_s0**: r=16 probe bits/nt 1.997, rank-1 rate 0.03, exact-extraction rate 0.00
- mlm **3mer_mlm0.15_s1**: r=16 probe bits/nt 1.998, rank-1 rate 0.03, exact-extraction rate 0.00
- mlm **3mer_mlm0.5_s0**: r=16 probe bits/nt 1.988, rank-1 rate 0.05, exact-extraction rate 0.00
- mlm **3mer_mlm0.5_s1**: r=16 probe bits/nt 1.992, rank-1 rate 0.05, exact-extraction rate 0.00
- mlm **6mer_mlm0.15_s0**: r=16 probe bits/nt 1.963, rank-1 rate 0.33, exact-extraction rate 0.00
- mlm **6mer_mlm0.15_s1**: r=16 probe bits/nt 1.964, rank-1 rate 0.30, exact-extraction rate 0.00
- mlm **6mer_mlm0.5_s0**: r=16 probe bits/nt 1.923, rank-1 rate 0.60, exact-extraction rate 0.00
- mlm **6mer_mlm0.5_s1**: r=16 probe bits/nt 1.920, rank-1 rate 0.65, exact-extraction rate 0.00
- mlm **char_mlm0.15_s0**: r=16 probe bits/nt 1.999, rank-1 rate 0.00, exact-extraction rate 0.00
- mlm **char_mlm0.15_s1**: r=16 probe bits/nt 2.000, rank-1 rate 0.00, exact-extraction rate 0.00
- mlm **char_mlm0.5_s0**: r=16 probe bits/nt 1.998, rank-1 rate 0.03, exact-extraction rate 0.00
- mlm **char_mlm0.5_s1**: r=16 probe bits/nt 1.998, rank-1 rate 0.03, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.