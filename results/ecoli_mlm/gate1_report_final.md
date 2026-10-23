# Gate 1 report

root: outputs/ecoli_mlm   scores file: scores_final.json
runs: 3mer_mlm0.15_s0, 3mer_mlm0.5_s0, 6mer_mlm0.15_s0, 6mer_mlm0.5_s0, char_mlm0.15_s0, char_mlm0.5_s0

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | 3mer | 12.69M (12.61M) | 2760 | 2.5M | 59 | 383 | 0.16 |
| 3mer_mlm0.5_s0 | 3mer | 12.69M (12.61M) | 2760 | 8.4M | 61 | 387 | 0.13 |
| 6mer_mlm0.15_s0 | 6mer | 14.73M (12.61M) | 2760 | 1.3M | 53 | 121 | 0.09 |
| 6mer_mlm0.5_s0 | 6mer | 14.73M (12.61M) | 2760 | 4.2M | 53 | 120 | 0.09 |
| char_mlm0.15_s0 | char | 12.76M (12.61M) | 2760 | 7.6M | 127 | 3240 | 0.20 |
| char_mlm0.5_s0 | char | 12.76M (12.61M) | 2760 | 25.2M | 127 | 3558 | 0.19 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | pll | 1.8605 | 3.6313 | 1.633 | **VIOLATION** |
| 3mer_mlm0.15_s0 | prefix | 1.9170 | 3.7765 | 1.702 | **VIOLATION** |
| 3mer_mlm0.5_s0 | pll | 1.8551 | 3.6177 | 1.648 | **VIOLATION** |
| 3mer_mlm0.5_s0 | prefix | 1.9064 | 3.7487 | 1.698 | **VIOLATION** |
| 6mer_mlm0.15_s0 | pll | 1.9476 | 3.8572 | 1.786 | **VIOLATION** |
| 6mer_mlm0.15_s0 | prefix | 1.9631 | 3.8991 | 1.785 | **VIOLATION** |
| 6mer_mlm0.5_s0 | pll | 1.9484 | 3.8593 | 1.764 | **VIOLATION** |
| 6mer_mlm0.5_s0 | prefix | 1.9600 | 3.8907 | 1.787 | **VIOLATION** |
| char_mlm0.15_s0 | pll | 1.9607 | 3.8924 | 1.808 | **VIOLATION** |
| char_mlm0.15_s0 | prefix | 2.7691 | 6.8168 | 2.339 | OK |
| char_mlm0.5_s0 | pll | 1.9092 | 3.7559 | 1.734 | **VIOLATION** |
| char_mlm0.5_s0 | prefix | 1.9540 | 3.8745 | 1.807 | **VIOLATION** |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 184 | 0.00 | 0.00 | 2.061 | -0.04 |
| r=1 | 40 | 156 | 0.00 | 0.03 | 2.048 | +0.21 |
| r=4 | 40 | 152 | 0.00 | 0.00 | 2.060 | -0.00 |
| r=16 | 40 | 110 | 0.03 | 0.03 | 2.039 | +0.32 |

### 3mer_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 94 | 0.00 | 0.05 | 2.065 | +0.39 |
| r=4 | 40 | 110 | 0.00 | 0.00 | 2.072 | +0.34 |
| r=16 | 40 | 125 | 0.03 | 0.05 | 2.071 | +0.40 |

### 3mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 181 | 0.00 | 0.00 | 2.058 | -0.10 |
| r=1 | 40 | 146 | 0.00 | 0.03 | 2.046 | +0.22 |
| r=4 | 40 | 140 | 0.00 | 0.00 | 2.054 | +0.09 |
| r=16 | 40 | 130 | 0.00 | 0.00 | 2.042 | +0.21 |

### 3mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 126 | 0.03 | 0.05 | 2.060 | +0.31 |
| r=4 | 40 | 128 | 0.00 | 0.00 | 2.065 | +0.25 |
| r=16 | 40 | 122 | 0.05 | 0.05 | 2.058 | +0.33 |

### 3mer_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 178 | 0.00 | 0.00 | 2.069 | -0.11 |
| r=1 | 40 | 145 | 0.00 | 0.03 | 2.053 | +0.19 |
| r=4 | 40 | 160 | 0.03 | 0.03 | 2.062 | +0.04 |
| r=16 | 40 | 102 | 0.03 | 0.05 | 2.036 | +0.40 |

### 3mer_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 84 | 0.00 | 0.03 | 2.068 | +0.55 |
| r=4 | 40 | 109 | 0.00 | 0.00 | 2.068 | +0.44 |
| r=16 | 40 | 101 | 0.05 | 0.07 | 2.067 | +0.62 |

### 3mer_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 164 | 0.00 | 0.00 | 2.063 | -0.15 |
| r=1 | 40 | 137 | 0.00 | 0.07 | 2.047 | +0.22 |
| r=4 | 40 | 148 | 0.00 | 0.00 | 2.058 | +0.03 |
| r=16 | 40 | 114 | 0.00 | 0.03 | 2.041 | +0.32 |

### 3mer_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 81 | 0.05 | 0.05 | 2.056 | +0.65 |
| r=4 | 40 | 134 | 0.00 | 0.00 | 2.065 | +0.33 |
| r=16 | 40 | 74 | 0.05 | 0.05 | 2.053 | +0.70 |

### 6mer_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 136 | 0.03 | 0.03 | 2.042 | +0.20 |
| r=1 | 40 | 116 | 0.03 | 0.03 | 2.043 | +0.16 |
| r=4 | 40 | 112 | 0.00 | 0.03 | 2.039 | +0.26 |
| r=16 | 40 | 90 | 0.00 | 0.00 | 2.032 | +0.43 |

### 6mer_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 56 | 0.05 | 0.10 | 2.017 | +1.01 |
| r=4 | 40 | 36 | 0.10 | 0.15 | 2.013 | +1.14 |
| r=16 | 40 | 22 | 0.12 | 0.17 | 1.996 | +1.56 |

### 6mer_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 166 | 0.00 | 0.03 | 2.053 | +0.12 |
| r=1 | 40 | 113 | 0.00 | 0.00 | 2.051 | +0.13 |
| r=4 | 40 | 112 | 0.00 | 0.00 | 2.047 | +0.29 |
| r=16 | 40 | 85 | 0.00 | 0.00 | 2.039 | +0.37 |

### 6mer_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 82 | 0.05 | 0.05 | 2.028 | +0.79 |
| r=4 | 40 | 68 | 0.00 | 0.05 | 2.033 | +0.66 |
| r=16 | 40 | 34 | 0.15 | 0.17 | 2.005 | +1.30 |

### 6mer_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 164 | 0.00 | 0.05 | 2.065 | +0.00 |
| r=1 | 40 | 122 | 0.00 | 0.05 | 2.055 | +0.25 |
| r=4 | 40 | 138 | 0.03 | 0.07 | 2.055 | +0.23 |
| r=16 | 40 | 99 | 0.00 | 0.05 | 2.041 | +0.56 |

### 6mer_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 4 | 0.35 | 0.47 | 1.966 | +2.48 |
| r=4 | 40 | 4 | 0.33 | 0.50 | 1.976 | +2.33 |
| r=16 | 40 | 4 | 0.28 | 0.45 | 1.974 | +2.39 |

### 6mer_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 171 | 0.03 | 0.05 | 2.075 | -0.09 |
| r=1 | 40 | 143 | 0.00 | 0.05 | 2.063 | +0.14 |
| r=4 | 40 | 136 | 0.03 | 0.05 | 2.057 | +0.34 |
| r=16 | 40 | 94 | 0.00 | 0.05 | 2.048 | +0.47 |

### 6mer_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 4 | 0.33 | 0.42 | 1.977 | +2.24 |
| r=4 | 40 | 6 | 0.17 | 0.45 | 1.984 | +2.06 |
| r=16 | 40 | 4 | 0.23 | 0.42 | 1.972 | +2.34 |

### char_mlm0.15_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 125 | 0.00 | 0.00 | 2.017 | -0.05 |
| r=1 | 40 | 167 | 0.00 | 0.00 | 2.019 | -0.12 |
| r=4 | 40 | 158 | 0.00 | 0.00 | 2.018 | -0.12 |
| r=16 | 40 | 165 | 0.00 | 0.00 | 2.019 | -0.13 |

### char_mlm0.15_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 95 | 0.00 | 0.00 | 2.021 | +0.36 |
| r=4 | 40 | 136 | 0.00 | 0.03 | 2.021 | +0.28 |
| r=16 | 40 | 105 | 0.00 | 0.00 | 2.024 | +0.30 |

### char_mlm0.15_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 132 | 0.00 | 0.00 | 2.036 | +0.13 |
| r=1 | 40 | 132 | 0.00 | 0.00 | 2.194 | +0.08 |
| r=4 | 40 | 154 | 0.00 | 0.00 | 2.153 | -0.08 |
| r=16 | 40 | 168 | 0.00 | 0.03 | 2.097 | -0.11 |

### char_mlm0.15_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 104 | 0.00 | 0.00 | 2.035 | +0.40 |
| r=4 | 40 | 116 | 0.00 | 0.00 | 2.160 | +0.25 |
| r=16 | 40 | 101 | 0.00 | 0.00 | 2.070 | +0.35 |

### char_mlm0.5_s0 — scorer `pll/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 184 | 0.00 | 0.00 | 2.034 | -0.10 |
| r=1 | 40 | 163 | 0.00 | 0.00 | 2.036 | -0.17 |
| r=4 | 40 | 158 | 0.00 | 0.00 | 2.031 | -0.07 |
| r=16 | 40 | 154 | 0.00 | 0.03 | 2.031 | -0.01 |

### char_mlm0.5_s0 — scorer `pll/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 100 | 0.00 | 0.00 | 2.030 | +0.45 |
| r=4 | 40 | 114 | 0.00 | 0.00 | 2.039 | +0.29 |
| r=16 | 40 | 82 | 0.05 | 0.05 | 2.035 | +0.43 |

### char_mlm0.5_s0 — scorer `prefix/fresh`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 158 | 0.00 | 0.00 | 2.045 | -0.10 |
| r=1 | 40 | 150 | 0.00 | 0.03 | 2.042 | -0.01 |
| r=4 | 40 | 145 | 0.00 | 0.03 | 2.038 | +0.11 |
| r=16 | 40 | 173 | 0.03 | 0.03 | 2.046 | -0.20 |

### char_mlm0.5_s0 — scorer `prefix/train`  (pool n=300, chance rank-1 = 0.0033)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 40 | 105 | 0.00 | 0.05 | 2.038 | +0.49 |
| r=4 | 40 | 106 | 0.00 | 0.03 | 2.043 | +0.39 |
| r=16 | 40 | 106 | 0.05 | 0.05 | 2.043 | +0.38 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 34.8 |
| 3mer_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 36.9 |
| 3mer_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 36.1 |
| 3mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 34.9 |
| 3mer_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 35.9 |
| 3mer_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 36.5 |
| 3mer_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 36.2 |
| 3mer_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 35.1 |
| 3mer_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 35.4 |
| 3mer_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 35.4 |
| 3mer_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 35.6 |
| 3mer_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 36.1 |
| 3mer_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 36.5 |
| 3mer_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 35.5 |
| 6mer_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 35.5 |
| 6mer_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 35.3 |
| 6mer_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 36.0 |
| 6mer_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 36.4 |
| 6mer_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 36.4 |
| 6mer_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 36.1 |
| 6mer_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 35.6 |
| 6mer_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 36.2 |
| 6mer_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 36.3 |
| 6mer_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 34.7 |
| 6mer_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 35.7 |
| 6mer_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 36.2 |
| char_mlm0.15_s0 | train | r=1 | 40 | 0.00 | 36.1 |
| char_mlm0.15_s0 | train | r=4 | 40 | 0.00 | 36.2 |
| char_mlm0.15_s0 | train | r=16 | 40 | 0.00 | 35.9 |
| char_mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 35.7 |
| char_mlm0.15_s0 | fresh | r=1 | 40 | 0.00 | 35.5 |
| char_mlm0.15_s0 | fresh | r=4 | 40 | 0.00 | 35.4 |
| char_mlm0.15_s0 | fresh | r=16 | 40 | 0.00 | 36.3 |
| char_mlm0.5_s0 | train | r=1 | 40 | 0.00 | 35.5 |
| char_mlm0.5_s0 | train | r=4 | 40 | 0.00 | 36.5 |
| char_mlm0.5_s0 | train | r=16 | 40 | 0.00 | 35.9 |
| char_mlm0.5_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| char_mlm0.5_s0 | fresh | r=1 | 40 | 0.00 | 36.4 |
| char_mlm0.5_s0 | fresh | r=4 | 40 | 0.00 | 35.2 |
| char_mlm0.5_s0 | fresh | r=16 | 40 | 0.00 | 36.2 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **3mer_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.773, Spearman(rank) = 0.876, rank-1 set Jaccard = 0.00 (1 vs 0 rank-1)
- **3mer_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.759, Spearman(rank) = 0.815, rank-1 set Jaccard = 0.33 (1 vs 3 rank-1)
- **3mer_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.798, Spearman(rank) = 0.837, rank-1 set Jaccard = 0.00 (2 vs 0 rank-1)
- **3mer_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.703, Spearman(rank) = 0.819, rank-1 set Jaccard = 0.50 (2 vs 4 rank-1)
- **6mer_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.835, Spearman(rank) = 0.821, rank-1 set Jaccard = 0.00 (2 vs 0 rank-1)
- **6mer_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.868, Spearman(rank) = 0.860, rank-1 set Jaccard = 0.58 (11 vs 8 rank-1)
- **6mer_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.849, Spearman(rank) = 0.845, rank-1 set Jaccard = 0.50 (1 vs 2 rank-1)
- **6mer_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.854, Spearman(rank) = 0.842, rank-1 set Jaccard = 0.56 (38 vs 29 rank-1)
- **char_mlm0.15_s0 / fresh**: n=160, Spearman(bits) = 0.518, Spearman(rank) = 0.724, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.15_s0 / train**: n=120, Spearman(bits) = 0.608, Spearman(rank) = 0.758, rank-1 set Jaccard = 0.00 (0 vs 0 rank-1)
- **char_mlm0.5_s0 / fresh**: n=160, Spearman(bits) = 0.764, Spearman(rank) = 0.860, rank-1 set Jaccard = 0.00 (0 vs 1 rank-1)
- **char_mlm0.5_s0 / train**: n=120, Spearman(bits) = 0.765, Spearman(rank) = 0.785, rank-1 set Jaccard = 1.00 (2 vs 2 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.042±0.032 | r=1 2.046±0.044 | non-member 2.058±0.036;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.73e-02, p(r=1 < non-member) = 5.89e-02
- **3mer_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.041±0.033 | r=1 2.047±0.045 | non-member 2.063±0.043;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.36e-02, p(r=1 < non-member) = 7.24e-02
- **6mer_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.039±0.039 | r=1 2.051±0.043 | non-member 2.053±0.046;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 9.13e-02, p(r=1 < non-member) = 3.88e-01
- **6mer_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.048±0.046 | r=1 2.063±0.051 | non-member 2.075±0.049;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.03;  MWU p(r=16 < non-member) = 4.37e-03, p(r=1 < non-member) = 1.19e-01
- **char_mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.097±0.374 | r=1 2.194±0.514 | non-member 2.036±0.039;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.50e-01, p(r=1 < non-member) = 6.41e-01
- **char_mlm0.5_s0** (prefix/fresh): bits/nt  r=16 2.046±0.038 | r=1 2.042±0.037 | non-member 2.045±0.029;  rank-1 rate r=16 0.03, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.34e-01, p(r=1 < non-member) = 2.90e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- mlm **3mer_mlm0.15_s0**: r=16 probe bits/nt 2.058, rank-1 rate 0.05, exact-extraction rate 0.00
- mlm **3mer_mlm0.5_s0**: r=16 probe bits/nt 2.053, rank-1 rate 0.05, exact-extraction rate 0.00
- mlm **6mer_mlm0.15_s0**: r=16 probe bits/nt 2.005, rank-1 rate 0.15, exact-extraction rate 0.00
- mlm **6mer_mlm0.5_s0**: r=16 probe bits/nt 1.972, rank-1 rate 0.23, exact-extraction rate 0.00
- mlm **char_mlm0.15_s0**: r=16 probe bits/nt 2.070, rank-1 rate 0.00, exact-extraction rate 0.00
- mlm **char_mlm0.5_s0**: r=16 probe bits/nt 2.043, rank-1 rate 0.05, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.