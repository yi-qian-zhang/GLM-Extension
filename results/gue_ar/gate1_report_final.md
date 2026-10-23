# Gate 1 report

root: outputs/gue_ar   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 61 | 54 | 0.14 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 46 | 31 | 0.19 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 44 | 25 | 0.13 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 35 | 16 | 0.14 |
| char_ar_s0 | char | 12.76M (12.61M) | 2850 | 52.3M | 173 | 143 | 0.14 |
| char_ar_s1 | char | 12.76M (12.61M) | 2850 | 52.3M | 197 | 167 | 0.13 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 3.9666 | 15.6335 | 0.102 | OK |
| 3mer_ar_s1 | ar | 3.9174 | 15.1093 | 0.097 | OK |
| 6mer_ar_s0 | ar | 2.4989 | 5.6525 | 0.058 | OK |
| 6mer_ar_s1 | ar | 2.4961 | 5.6414 | 0.064 | OK |
| char_ar_s0 | ar | 2.0029 | 4.0082 | 1.560 | OK |
| char_ar_s1 | ar | 1.9986 | 3.9962 | 1.549 | **VIOLATION** |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 306 | 0.00 | 0.00 | 4.138 | -0.18 |
| r=1 | 50 | 240 | 0.00 | 0.00 | 4.048 | +0.08 |
| r=4 | 50 | 217 | 0.00 | 0.02 | 4.005 | +0.26 |
| r=16 | 50 | 96 | 0.06 | 0.08 | 3.854 | +0.88 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.014 | +17.23 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.017 | +17.15 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.019 | +17.24 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 246 | 0.00 | 0.00 | 4.008 | +0.01 |
| r=1 | 50 | 303 | 0.00 | 0.00 | 4.049 | -0.22 |
| r=4 | 50 | 236 | 0.02 | 0.04 | 3.923 | +0.34 |
| r=16 | 50 | 142 | 0.08 | 0.08 | 3.836 | +0.82 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.017 | +17.12 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.017 | +16.96 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.020 | +16.98 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 264 | 0.02 | 0.04 | 2.544 | +0.08 |
| r=1 | 50 | 210 | 0.04 | 0.06 | 2.521 | +0.34 |
| r=4 | 50 | 200 | 0.08 | 0.20 | 2.480 | +0.60 |
| r=16 | 50 | 2 | 0.48 | 0.56 | 2.170 | +3.14 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.013 | +20.56 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.014 | +20.27 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.015 | +20.78 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 282 | 0.00 | 0.00 | 2.552 | -0.02 |
| r=1 | 50 | 155 | 0.00 | 0.02 | 2.517 | +0.30 |
| r=4 | 50 | 106 | 0.14 | 0.14 | 2.432 | +0.95 |
| r=16 | 50 | 1 | 0.58 | 0.66 | 2.120 | +3.55 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.013 | +20.64 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.014 | +20.39 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.014 | +20.50 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 266 | 0.00 | 0.00 | 2.089 | +0.01 |
| r=1 | 50 | 277 | 0.02 | 0.04 | 2.085 | +0.03 |
| r=4 | 50 | 293 | 0.00 | 0.00 | 2.087 | -0.10 |
| r=16 | 50 | 313 | 0.00 | 0.00 | 2.090 | -0.07 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 0.52 | 0.78 | 1.938 | +3.00 |
| r=4 | 50 | 3 | 0.32 | 0.68 | 1.957 | +2.60 |
| r=16 | 50 | 1 | 0.58 | 0.70 | 1.939 | +2.93 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 200 | 0.00 | 0.02 | 2.061 | +0.34 |
| r=1 | 50 | 264 | 0.00 | 0.04 | 2.083 | -0.08 |
| r=4 | 50 | 183 | 0.00 | 0.00 | 2.076 | +0.06 |
| r=16 | 50 | 251 | 0.00 | 0.02 | 2.084 | -0.03 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 2 | 0.50 | 0.76 | 1.946 | +2.81 |
| r=4 | 50 | 2 | 0.42 | 0.64 | 1.956 | +2.60 |
| r=16 | 50 | 1 | 0.52 | 0.76 | 1.942 | +2.84 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.4 |
| 3mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.6 |
| 3mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 35.9 |
| 3mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 36.4 |
| 3mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 35.9 |
| 3mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 36.5 |
| 3mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=16 | 50 | 0.00 | 36.1 |
| 6mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.4 |
| 6mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.4 |
| 6mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.1 |
| 6mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 34.6 |
| 6mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.3 |
| 6mer_ar_s1 | fresh | r=16 | 50 | 0.02 | 33.5 |
| char_ar_s0 | train | r=1 | 50 | 0.00 | 34.9 |
| char_ar_s0 | train | r=4 | 50 | 0.00 | 34.2 |
| char_ar_s0 | train | r=16 | 50 | 0.00 | 35.7 |
| char_ar_s0 | fresh | r=0 | 50 | 0.00 | 35.7 |
| char_ar_s0 | fresh | r=1 | 50 | 0.00 | 36.1 |
| char_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=16 | 50 | 0.00 | 36.3 |
| char_ar_s1 | train | r=1 | 50 | 0.00 | 34.5 |
| char_ar_s1 | train | r=4 | 50 | 0.00 | 34.3 |
| char_ar_s1 | train | r=16 | 50 | 0.00 | 35.4 |
| char_ar_s1 | fresh | r=0 | 50 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=1 | 50 | 0.00 | 35.5 |
| char_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.4 |
| char_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.4 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 3.854±0.268 | r=1 4.048±0.260 | non-member 4.138±0.223;  rank-1 rate r=16 0.06, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.06e-07, p(r=1 < non-member) = 2.37e-02
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 3.836±0.333 | r=1 4.049±0.207 | non-member 4.008±0.257;  rank-1 rate r=16 0.08, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.86e-03, p(r=1 < non-member) = 8.57e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.170±0.271 | r=1 2.521±0.144 | non-member 2.544±0.118;  rank-1 rate r=16 0.48, r=1 0.04, non-member 0.02;  MWU p(r=16 < non-member) = 4.72e-13, p(r=1 < non-member) = 2.27e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.120±0.342 | r=1 2.517±0.136 | non-member 2.552±0.122;  rank-1 rate r=16 0.58, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 9.95e-13, p(r=1 < non-member) = 7.83e-02
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.090±0.047 | r=1 2.085±0.058 | non-member 2.089±0.052;  rank-1 rate r=16 0.00, r=1 0.02, non-member 0.00;  MWU p(r=16 < non-member) = 5.99e-01, p(r=1 < non-member) = 4.99e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.084±0.058 | r=1 2.083±0.056 | non-member 2.061±0.051;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 9.81e-01, p(r=1 < non-member) = 9.82e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.019, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.020, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.015, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.014, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.939, rank-1 rate 0.58, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.942, rank-1 rate 0.52, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.