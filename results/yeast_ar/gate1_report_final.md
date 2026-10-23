# Gate 1 report

root: outputs/yeast_ar   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 62 | 54 | 0.14 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 47 | 38 | 0.18 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 44 | 33 | 0.11 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 47 | 36 | 0.11 |
| char_ar_s0 | char | 12.76M (12.61M) | 2850 | 52.3M | 183 | 207 | 0.11 |
| char_ar_s1 | char | 12.76M (12.61M) | 2850 | 52.3M | 183 | 166 | 0.13 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.0134 | 16.1495 | 2.571 | OK |
| 3mer_ar_s1 | ar | 3.9687 | 15.6567 | 2.863 | OK |
| 6mer_ar_s0 | ar | 2.5302 | 5.7766 | 2.259 | OK |
| 6mer_ar_s1 | ar | 2.5314 | 5.7812 | 2.119 | OK |
| char_ar_s0 | ar | 2.0022 | 4.0062 | 1.384 | OK |
| char_ar_s1 | ar | 1.9987 | 3.9964 | 1.442 | **VIOLATION** |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 258 | 0.00 | 0.02 | 4.154 | +0.01 |
| r=1 | 50 | 217 | 0.02 | 0.02 | 4.114 | +0.03 |
| r=4 | 50 | 176 | 0.00 | 0.00 | 4.056 | +0.29 |
| r=16 | 50 | 90 | 0.06 | 0.12 | 3.908 | +0.93 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.015 | +17.13 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.019 | +17.18 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.020 | +17.14 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 216 | 0.02 | 0.06 | 4.057 | +0.23 |
| r=1 | 50 | 258 | 0.00 | 0.04 | 4.090 | +0.04 |
| r=4 | 50 | 154 | 0.02 | 0.08 | 3.947 | +0.68 |
| r=16 | 50 | 76 | 0.02 | 0.08 | 3.904 | +0.93 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.015 | +17.13 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.023 | +17.06 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.023 | +17.03 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 280 | 0.00 | 0.00 | 2.601 | -0.02 |
| r=1 | 50 | 208 | 0.00 | 0.02 | 2.570 | +0.26 |
| r=4 | 50 | 114 | 0.08 | 0.16 | 2.480 | +0.91 |
| r=16 | 50 | 2 | 0.48 | 0.60 | 2.183 | +3.32 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.011 | +20.38 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.017 | +19.96 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.013 | +20.26 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 290 | 0.00 | 0.00 | 2.630 | -0.24 |
| r=1 | 50 | 154 | 0.00 | 0.02 | 2.546 | +0.36 |
| r=4 | 50 | 104 | 0.10 | 0.12 | 2.480 | +0.90 |
| r=16 | 50 | 2 | 0.48 | 0.56 | 2.173 | +3.33 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.010 | +20.37 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.017 | +20.22 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.013 | +20.41 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 244 | 0.00 | 0.02 | 2.093 | +0.07 |
| r=1 | 50 | 272 | 0.00 | 0.02 | 2.102 | -0.09 |
| r=4 | 50 | 290 | 0.00 | 0.00 | 2.106 | -0.19 |
| r=16 | 50 | 166 | 0.02 | 0.04 | 2.073 | +0.46 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 2 | 0.46 | 0.80 | 1.956 | +2.84 |
| r=4 | 50 | 3 | 0.40 | 0.68 | 1.963 | +2.74 |
| r=16 | 50 | 2 | 0.50 | 0.76 | 1.939 | +3.12 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 257 | 0.02 | 0.02 | 2.094 | -0.10 |
| r=1 | 50 | 260 | 0.00 | 0.00 | 2.092 | -0.05 |
| r=4 | 50 | 200 | 0.02 | 0.04 | 2.081 | +0.21 |
| r=16 | 50 | 192 | 0.00 | 0.00 | 2.074 | +0.38 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 5 | 0.26 | 0.56 | 1.974 | +2.54 |
| r=4 | 50 | 3 | 0.38 | 0.52 | 1.973 | +2.47 |
| r=16 | 50 | 2 | 0.40 | 0.70 | 1.950 | +2.86 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.2 |
| 3mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.8 |
| 3mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.4 |
| 3mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 36.1 |
| 3mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 35.9 |
| 3mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.9 |
| 6mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 34.7 |
| 6mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.6 |
| 6mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 35.7 |
| 6mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 35.3 |
| 6mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 35.8 |
| 6mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 35.9 |
| 6mer_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.5 |
| char_ar_s0 | train | r=1 | 50 | 0.00 | 34.7 |
| char_ar_s0 | train | r=4 | 50 | 0.00 | 34.6 |
| char_ar_s0 | train | r=16 | 50 | 0.00 | 34.4 |
| char_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.3 |
| char_ar_s0 | fresh | r=1 | 50 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.2 |
| char_ar_s0 | fresh | r=16 | 50 | 0.00 | 36.2 |
| char_ar_s1 | train | r=1 | 50 | 0.00 | 35.3 |
| char_ar_s1 | train | r=4 | 50 | 0.00 | 34.8 |
| char_ar_s1 | train | r=16 | 50 | 0.00 | 34.1 |
| char_ar_s1 | fresh | r=0 | 50 | 0.00 | 36.2 |
| char_ar_s1 | fresh | r=1 | 50 | 0.00 | 35.6 |
| char_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.5 |
| char_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.8 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 3.908±0.373 | r=1 4.114±0.251 | non-member 4.154±0.303;  rank-1 rate r=16 0.06, r=1 0.02, non-member 0.00;  MWU p(r=16 < non-member) = 1.18e-04, p(r=1 < non-member) = 2.19e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 3.904±0.264 | r=1 4.090±0.291 | non-member 4.057±0.256;  rank-1 rate r=16 0.02, r=1 0.00, non-member 0.02;  MWU p(r=16 < non-member) = 1.50e-03, p(r=1 < non-member) = 7.69e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.183±0.308 | r=1 2.570±0.160 | non-member 2.601±0.140;  rank-1 rate r=16 0.48, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.07e-12, p(r=1 < non-member) = 1.68e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.173±0.338 | r=1 2.546±0.146 | non-member 2.630±0.125;  rank-1 rate r=16 0.48, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.33e-13, p(r=1 < non-member) = 1.71e-03
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.073±0.056 | r=1 2.102±0.060 | non-member 2.093±0.053;  rank-1 rate r=16 0.02, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.73e-02, p(r=1 < non-member) = 7.89e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.074±0.048 | r=1 2.092±0.050 | non-member 2.094±0.054;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.02;  MWU p(r=16 < non-member) = 5.84e-02, p(r=1 < non-member) = 4.85e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.020, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.023, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.939, rank-1 rate 0.50, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.950, rank-1 rate 0.40, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.