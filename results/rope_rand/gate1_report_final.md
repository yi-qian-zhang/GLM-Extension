# Gate 1 report

root: outputs/rope_rand   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.64M (12.61M) | 2550 | 15.6M | 44 | 11 | 0.16 |
| 3mer_ar_s1 | 3mer | 12.64M (12.61M) | 2550 | 15.6M | 39 | 12 | 0.20 |
| 6mer_ar_s0 | 6mer | 14.71M (12.61M) | 2550 | 7.8M | 38 | 6 | 0.12 |
| 6mer_ar_s1 | 6mer | 14.71M (12.61M) | 2550 | 7.8M | 38 | 7 | 0.11 |
| char_ar_s0 | char | 12.61M (12.61M) | 2550 | 46.8M | 69 | 30 | 0.33 |
| char_ar_s1 | char | 12.61M (12.61M) | 2550 | 46.8M | 68 | 30 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.2615 | 19.1802 | 3.790 | OK |
| 3mer_ar_s1 | ar | 4.3134 | 19.8827 | 3.723 | OK |
| 6mer_ar_s0 | ar | 2.5068 | 5.6834 | 2.322 | OK |
| 6mer_ar_s1 | ar | 2.5057 | 5.6792 | 2.311 | OK |
| char_ar_s0 | ar | 2.0623 | 4.1766 | 1.988 | OK |
| char_ar_s1 | ar | 2.0388 | 4.1090 | 1.984 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 285 | 0.00 | 0.03 | 4.340 | +0.03 |
| r=1 | 20 | 188 | 0.00 | 0.00 | 4.226 | +0.39 |
| r=4 | 20 | 115 | 0.05 | 0.20 | 4.127 | +0.86 |
| r=16 | 20 | 22 | 0.30 | 0.40 | 3.821 | +2.10 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +17.99 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.013 | +17.66 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.009 | +17.96 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 292 | 0.00 | 0.00 | 4.375 | +0.07 |
| r=1 | 20 | 166 | 0.00 | 0.05 | 4.284 | +0.38 |
| r=4 | 20 | 151 | 0.05 | 0.05 | 4.138 | +0.73 |
| r=16 | 20 | 20 | 0.30 | 0.40 | 3.766 | +2.44 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +17.98 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.012 | +17.87 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.010 | +17.82 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 290 | 0.00 | 0.03 | 2.512 | +0.03 |
| r=1 | 20 | 226 | 0.00 | 0.00 | 2.500 | +0.11 |
| r=4 | 20 | 128 | 0.20 | 0.20 | 2.339 | +1.51 |
| r=16 | 20 | 1 | 0.85 | 0.90 | 1.696 | +6.97 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +21.23 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.018 | +21.10 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.011 | +21.14 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 256 | 0.00 | 0.00 | 2.514 | -0.03 |
| r=1 | 20 | 249 | 0.00 | 0.10 | 2.466 | +0.41 |
| r=4 | 20 | 22 | 0.20 | 0.40 | 2.323 | +1.66 |
| r=16 | 20 | 1 | 0.75 | 0.80 | 1.876 | +5.44 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +21.32 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.018 | +21.50 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.011 | +20.99 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 240 | 0.00 | 0.03 | 2.051 | +0.13 |
| r=1 | 20 | 191 | 0.00 | 0.00 | 2.045 | +0.25 |
| r=4 | 20 | 288 | 0.00 | 0.05 | 2.067 | -0.04 |
| r=16 | 20 | 160 | 0.00 | 0.05 | 2.046 | +0.26 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 3 | 0.25 | 0.60 | 1.951 | +2.43 |
| r=4 | 20 | 2 | 0.40 | 0.70 | 1.931 | +2.82 |
| r=16 | 20 | 2 | 0.50 | 0.65 | 1.921 | +3.08 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 270 | 0.00 | 0.00 | 2.038 | -0.07 |
| r=1 | 20 | 324 | 0.00 | 0.10 | 2.047 | -0.18 |
| r=4 | 20 | 204 | 0.00 | 0.05 | 2.026 | +0.22 |
| r=16 | 20 | 161 | 0.00 | 0.05 | 2.020 | +0.59 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 24 | 0.15 | 0.35 | 1.977 | +1.72 |
| r=4 | 20 | 6 | 0.40 | 0.50 | 1.953 | +2.37 |
| r=16 | 20 | 6 | 0.40 | 0.50 | 1.955 | +2.42 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.4 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.0 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.2 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 34.9 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.6 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.4 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.8 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.2 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.5 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.05 | 33.6 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.8 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 37.0 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.1 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 33.9 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 34.2 |
| char_ar_s0 | train | r=16 | 20 | 0.00 | 33.5 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.5 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 34.9 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 35.9 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 35.5 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 33.7 |
| char_ar_s1 | train | r=16 | 20 | 0.00 | 34.3 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.8 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.3 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 3.821±0.586 | r=1 4.226±0.272 | non-member 4.340±0.277;  rank-1 rate r=16 0.30, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.43e-04, p(r=1 < non-member) = 7.13e-02
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 3.766±0.882 | r=1 4.284±0.279 | non-member 4.375±0.235;  rank-1 rate r=16 0.30, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.01e-04, p(r=1 < non-member) = 1.52e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 1.696±0.458 | r=1 2.500±0.125 | non-member 2.512±0.121;  rank-1 rate r=16 0.85, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.28e-10, p(r=1 < non-member) = 2.23e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 1.876±0.393 | r=1 2.466±0.154 | non-member 2.514±0.117;  rank-1 rate r=16 0.75, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.48e-08, p(r=1 < non-member) = 1.84e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.046±0.052 | r=1 2.045±0.056 | non-member 2.051±0.053;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 3.92e-01, p(r=1 < non-member) = 2.63e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.020±0.033 | r=1 2.047±0.063 | non-member 2.038±0.031;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.82e-02, p(r=1 < non-member) = 4.28e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.009, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.010, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.921, rank-1 rate 0.50, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.955, rank-1 rate 0.40, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.