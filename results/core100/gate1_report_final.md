# Gate 1 report

root: outputs/core100   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 3mer_ar_s2, 6mer_ar_s0, 6mer_ar_s1, 6mer_ar_s2, char_ar_s0, char_ar_s1, char_ar_s2

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 48 | 41 | 0.22 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 61 | 81 | 0.17 |
| 3mer_ar_s2 | 3mer | 12.69M (12.61M) | 3330 | 20.4M | 59 | 79 | 0.17 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 46 | 47 | 0.12 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 38 | 23 | 0.15 |
| 6mer_ar_s2 | 6mer | 14.73M (12.61M) | 3330 | 10.2M | 50 | 50 | 0.12 |
| char_ar_s0 | char | 12.76M (12.61M) | 3330 | 61.3M | 88 | 108 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 3330 | 61.3M | 87 | 106 | 0.34 |
| char_ar_s2 | char | 12.76M (12.61M) | 3330 | 61.3M | 88 | 109 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.1124 | 17.2958 | 3.606 | OK |
| 3mer_ar_s1 | ar | 4.1871 | 18.2152 | 3.726 | OK |
| 3mer_ar_s2 | ar | 4.2208 | 18.6464 | 3.758 | OK |
| 6mer_ar_s0 | ar | 2.6338 | 6.2066 | 2.397 | OK |
| 6mer_ar_s1 | ar | 2.6299 | 6.1896 | 2.434 | OK |
| 6mer_ar_s2 | ar | 2.4429 | 5.4374 | 2.232 | OK |
| char_ar_s0 | ar | 2.0450 | 4.1267 | 1.978 | OK |
| char_ar_s1 | ar | 2.0350 | 4.0981 | 1.985 | OK |
| char_ar_s2 | ar | 2.0438 | 4.1234 | 1.983 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 231 | 0.00 | 0.00 | 4.185 | +0.03 |
| r=1 | 100 | 269 | 0.00 | 0.00 | 4.203 | +0.00 |
| r=4 | 100 | 232 | 0.01 | 0.02 | 4.213 | +0.08 |
| r=16 | 100 | 142 | 0.03 | 0.08 | 4.063 | +0.63 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.023 | +17.47 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.016 | +17.54 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.023 | +17.53 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 227 | 0.02 | 0.03 | 4.251 | +0.12 |
| r=1 | 100 | 227 | 0.01 | 0.04 | 4.226 | +0.18 |
| r=4 | 100 | 314 | 0.00 | 0.02 | 4.324 | -0.16 |
| r=16 | 100 | 221 | 0.01 | 0.04 | 4.228 | +0.20 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +17.72 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.012 | +17.73 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.014 | +17.65 |

### 3mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 226 | 0.01 | 0.01 | 4.303 | +0.08 |
| r=1 | 100 | 269 | 0.00 | 0.01 | 4.313 | +0.02 |
| r=4 | 100 | 191 | 0.01 | 0.03 | 4.267 | +0.16 |
| r=16 | 100 | 180 | 0.02 | 0.05 | 4.228 | +0.33 |

### 3mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.010 | +17.66 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.010 | +17.70 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.014 | +17.64 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 268 | 0.00 | 0.00 | 2.651 | -0.04 |
| r=1 | 100 | 213 | 0.00 | 0.02 | 2.624 | +0.17 |
| r=4 | 100 | 134 | 0.05 | 0.11 | 2.547 | +0.75 |
| r=16 | 100 | 4 | 0.41 | 0.52 | 2.275 | +2.79 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.81 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.62 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.013 | +19.63 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 237 | 0.00 | 0.01 | 2.626 | +0.12 |
| r=1 | 100 | 220 | 0.00 | 0.00 | 2.629 | +0.05 |
| r=4 | 100 | 173 | 0.01 | 0.05 | 2.591 | +0.39 |
| r=16 | 100 | 8 | 0.37 | 0.48 | 2.310 | +2.50 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.72 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.011 | +19.84 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.013 | +19.74 |

### 6mer_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 233 | 0.00 | 0.03 | 2.441 | +0.13 |
| r=1 | 100 | 195 | 0.00 | 0.01 | 2.432 | +0.23 |
| r=4 | 100 | 132 | 0.06 | 0.15 | 2.372 | +0.75 |
| r=16 | 100 | 8 | 0.34 | 0.45 | 2.172 | +2.51 |

### 6mer_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 1 | 1.00 | 1.00 | 0.072 | +20.77 |
| r=4 | 100 | 1 | 1.00 | 1.00 | 0.068 | +20.80 |
| r=16 | 100 | 1 | 1.00 | 1.00 | 0.063 | +20.87 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 247 | 0.00 | 0.00 | 2.045 | +0.05 |
| r=1 | 100 | 242 | 0.02 | 0.02 | 2.046 | +0.04 |
| r=4 | 100 | 190 | 0.01 | 0.01 | 2.036 | +0.34 |
| r=16 | 100 | 224 | 0.01 | 0.01 | 2.044 | +0.10 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 3 | 0.35 | 0.60 | 1.949 | +2.59 |
| r=4 | 100 | 3 | 0.39 | 0.66 | 1.947 | +2.64 |
| r=16 | 100 | 3 | 0.32 | 0.61 | 1.945 | +2.69 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 250 | 0.01 | 0.03 | 2.032 | +0.13 |
| r=1 | 100 | 262 | 0.00 | 0.01 | 2.034 | +0.07 |
| r=4 | 100 | 238 | 0.01 | 0.04 | 2.036 | +0.01 |
| r=16 | 100 | 242 | 0.00 | 0.00 | 2.033 | +0.09 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 4 | 0.22 | 0.54 | 1.958 | +2.32 |
| r=4 | 100 | 8 | 0.20 | 0.47 | 1.962 | +2.21 |
| r=16 | 100 | 6 | 0.29 | 0.50 | 1.957 | +2.35 |

### char_ar_s2 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 100 | 263 | 0.00 | 0.02 | 2.044 | +0.00 |
| r=1 | 100 | 283 | 0.00 | 0.01 | 2.046 | -0.06 |
| r=4 | 100 | 273 | 0.00 | 0.00 | 2.042 | +0.06 |
| r=16 | 100 | 218 | 0.00 | 0.00 | 2.040 | +0.11 |

### char_ar_s2 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 100 | 2 | 0.41 | 0.65 | 1.945 | +2.67 |
| r=4 | 100 | 2 | 0.30 | 0.62 | 1.949 | +2.58 |
| r=16 | 100 | 2 | 0.34 | 0.62 | 1.946 | +2.66 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 100 | 0.99 | 0.1 |
| 3mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.2 |
| 3mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 36.6 |
| 3mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.9 |
| 3mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 3mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 35.6 |
| 3mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.4 |
| 3mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.5 |
| 3mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.5 |
| 3mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 3mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.6 |
| 3mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 36.2 |
| 3mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.0 |
| 3mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 35.5 |
| 6mer_ar_s0 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 100 | 0.00 | 36.3 |
| 6mer_ar_s0 | fresh | r=1 | 100 | 0.00 | 35.7 |
| 6mer_ar_s0 | fresh | r=4 | 100 | 0.00 | 36.4 |
| 6mer_ar_s0 | fresh | r=16 | 100 | 0.00 | 35.5 |
| 6mer_ar_s1 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=1 | 100 | 0.00 | 35.6 |
| 6mer_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=16 | 100 | 0.00 | 35.9 |
| 6mer_ar_s2 | train | r=1 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=4 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | train | r=16 | 100 | 1.00 | 0.0 |
| 6mer_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.6 |
| 6mer_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.5 |
| 6mer_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.1 |
| 6mer_ar_s2 | fresh | r=16 | 100 | 0.00 | 36.0 |
| char_ar_s0 | train | r=1 | 100 | 0.00 | 34.4 |
| char_ar_s0 | train | r=4 | 100 | 0.00 | 34.8 |
| char_ar_s0 | train | r=16 | 100 | 0.00 | 34.5 |
| char_ar_s0 | fresh | r=0 | 100 | 0.00 | 35.9 |
| char_ar_s0 | fresh | r=1 | 100 | 0.00 | 35.9 |
| char_ar_s0 | fresh | r=4 | 100 | 0.00 | 35.0 |
| char_ar_s0 | fresh | r=16 | 100 | 0.00 | 36.1 |
| char_ar_s1 | train | r=1 | 100 | 0.00 | 34.3 |
| char_ar_s1 | train | r=4 | 100 | 0.00 | 34.1 |
| char_ar_s1 | train | r=16 | 100 | 0.00 | 34.1 |
| char_ar_s1 | fresh | r=0 | 100 | 0.00 | 36.4 |
| char_ar_s1 | fresh | r=1 | 100 | 0.00 | 36.3 |
| char_ar_s1 | fresh | r=4 | 100 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=16 | 100 | 0.00 | 36.3 |
| char_ar_s2 | train | r=1 | 100 | 0.00 | 33.8 |
| char_ar_s2 | train | r=4 | 100 | 0.00 | 34.7 |
| char_ar_s2 | train | r=16 | 100 | 0.00 | 34.1 |
| char_ar_s2 | fresh | r=0 | 100 | 0.00 | 35.7 |
| char_ar_s2 | fresh | r=1 | 100 | 0.00 | 35.8 |
| char_ar_s2 | fresh | r=4 | 100 | 0.00 | 36.3 |
| char_ar_s2 | fresh | r=16 | 100 | 0.00 | 36.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 4.063±0.429 | r=1 4.203±0.276 | non-member 4.185±0.246;  rank-1 rate r=16 0.03, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.84e-02, p(r=1 < non-member) = 6.70e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 4.228±0.269 | r=1 4.226±0.286 | non-member 4.251±0.279;  rank-1 rate r=16 0.01, r=1 0.01, non-member 0.02;  MWU p(r=16 < non-member) = 3.11e-01, p(r=1 < non-member) = 3.20e-01
- **3mer_ar_s2** (ar/fresh): bits/nt  r=16 4.228±0.319 | r=1 4.313±0.274 | non-member 4.303±0.265;  rank-1 rate r=16 0.02, r=1 0.00, non-member 0.01;  MWU p(r=16 < non-member) = 6.54e-02, p(r=1 < non-member) = 6.59e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.275±0.302 | r=1 2.624±0.148 | non-member 2.651±0.114;  rank-1 rate r=16 0.41, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.52e-22, p(r=1 < non-member) = 7.28e-02
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.310±0.262 | r=1 2.629±0.130 | non-member 2.626±0.140;  rank-1 rate r=16 0.37, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.71e-19, p(r=1 < non-member) = 4.99e-01
- **6mer_ar_s2** (ar/fresh): bits/nt  r=16 2.172±0.222 | r=1 2.432±0.130 | non-member 2.441±0.115;  rank-1 rate r=16 0.34, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.92e-19, p(r=1 < non-member) = 3.18e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.044±0.043 | r=1 2.046±0.037 | non-member 2.045±0.039;  rank-1 rate r=16 0.01, r=1 0.02, non-member 0.00;  MWU p(r=16 < non-member) = 3.21e-01, p(r=1 < non-member) = 5.67e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.033±0.032 | r=1 2.034±0.033 | non-member 2.032±0.032;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.01;  MWU p(r=16 < non-member) = 3.51e-01, p(r=1 < non-member) = 5.47e-01
- **char_ar_s2** (ar/fresh): bits/nt  r=16 2.040±0.035 | r=1 2.046±0.037 | non-member 2.044±0.034;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.25e-01, p(r=1 < non-member) = 6.37e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.023, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.014, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s2**: r=16 probe bits/nt 0.014, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s2**: r=16 probe bits/nt 0.063, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.945, rank-1 rate 0.32, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.957, rank-1 rate 0.29, exact-extraction rate 0.00
- ar  **char_ar_s2**: r=16 probe bits/nt 1.946, rank-1 rate 0.34, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.