# Gate 1 report

root: outputs/off2   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 8500 | 52.0M | 119 | 9 | 0.24 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 8500 | 52.0M | 132 | 10 | 0.25 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 8500 | 26.0M | 123 | 6 | 0.14 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 8500 | 26.0M | 112 | 6 | 0.13 |
| char_ar_s0 | char | 12.76M (12.61M) | 8500 | 156.1M | 221 | 25 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 8500 | 156.1M | 219 | 25 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 5.6136 | 48.9619 | 4.952 | OK |
| 3mer_ar_s1 | ar | 5.6452 | 50.0461 | 4.982 | OK |
| 6mer_ar_s0 | ar | 3.2397 | 9.4461 | 2.936 | OK |
| 6mer_ar_s1 | ar | 3.2499 | 9.5131 | 2.930 | OK |
| char_ar_s0 | ar | 7.1007 | 137.2514 | 6.142 | OK |
| char_ar_s1 | ar | 7.6790 | 204.9320 | 6.621 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 234 | 0.00 | 0.00 | 5.739 | +0.07 |
| r=1 | 20 | 252 | 0.00 | 0.00 | 5.752 | -0.01 |
| r=4 | 20 | 264 | 0.00 | 0.05 | 5.753 | -0.10 |
| r=16 | 20 | 332 | 0.00 | 0.05 | 5.837 | -0.10 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.000 | +16.20 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.007 | +16.29 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.007 | +16.31 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 210 | 0.00 | 0.00 | 5.717 | +0.17 |
| r=1 | 20 | 277 | 0.00 | 0.00 | 5.813 | +0.02 |
| r=4 | 20 | 256 | 0.00 | 0.05 | 5.738 | +0.13 |
| r=16 | 20 | 166 | 0.10 | 0.10 | 5.527 | +0.63 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.000 | +16.34 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.007 | +16.23 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.006 | +16.31 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 295 | 0.00 | 0.00 | 3.290 | -0.15 |
| r=1 | 20 | 254 | 0.00 | 0.00 | 3.292 | -0.14 |
| r=4 | 20 | 228 | 0.00 | 0.00 | 3.206 | +0.20 |
| r=16 | 20 | 3 | 0.50 | 0.60 | 2.688 | +3.03 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.000 | +17.60 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.013 | +17.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.006 | +17.21 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 251 | 0.00 | 0.00 | 3.233 | +0.16 |
| r=1 | 20 | 211 | 0.00 | 0.05 | 3.198 | +0.29 |
| r=4 | 20 | 91 | 0.00 | 0.00 | 3.144 | +0.62 |
| r=16 | 20 | 13 | 0.25 | 0.30 | 2.827 | +2.26 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.000 | +17.64 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.012 | +17.44 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.006 | +17.30 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 292 | 0.00 | 0.00 | 7.383 | -0.28 |
| r=1 | 20 | 224 | 0.00 | 0.00 | 7.228 | +0.01 |
| r=4 | 20 | 250 | 0.00 | 0.00 | 7.283 | -0.13 |
| r=16 | 20 | 141 | 0.00 | 0.00 | 7.128 | +0.38 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.029 | +14.91 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.033 | +14.65 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.047 | +14.55 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 206 | 0.00 | 0.00 | 7.822 | +0.04 |
| r=1 | 20 | 116 | 0.00 | 0.00 | 7.525 | +0.55 |
| r=4 | 20 | 388 | 0.00 | 0.00 | 8.058 | -0.56 |
| r=16 | 20 | 226 | 0.00 | 0.05 | 7.714 | +0.18 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.020 | +14.52 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.026 | +14.49 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.027 | +14.48 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.9 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 35.8 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.8 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.6 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.9 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.3 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.9 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 36.1 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 37.0 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.4 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.4 |
| char_ar_s0 | train | r=1 | 20 | 0.75 | 1.1 |
| char_ar_s0 | train | r=4 | 20 | 0.85 | 2.1 |
| char_ar_s0 | train | r=16 | 20 | 0.70 | 5.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.9 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.1 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 34.9 |
| char_ar_s1 | train | r=1 | 20 | 0.95 | 0.4 |
| char_ar_s1 | train | r=4 | 20 | 0.90 | 0.3 |
| char_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.4 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.9 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.5 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 5.837±0.546 | r=1 5.752±0.314 | non-member 5.739±0.431;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.51e-01, p(r=1 < non-member) = 5.16e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 5.527±0.571 | r=1 5.813±0.341 | non-member 5.717±0.369;  rank-1 rate r=16 0.10, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.34e-01, p(r=1 < non-member) = 7.95e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.688±0.499 | r=1 3.292±0.214 | non-member 3.290±0.208;  rank-1 rate r=16 0.50, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.57e-07, p(r=1 < non-member) = 5.09e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.827±0.368 | r=1 3.198±0.216 | non-member 3.233±0.197;  rank-1 rate r=16 0.25, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 7.26e-06, p(r=1 < non-member) = 3.22e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 7.128±0.450 | r=1 7.228±0.494 | non-member 7.383±0.481;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.75e-02, p(r=1 < non-member) = 9.79e-02
- **char_ar_s1** (ar/fresh): bits/nt  r=16 7.714±0.631 | r=1 7.525±0.529 | non-member 7.822±0.618;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.84e-01, p(r=1 < non-member) = 5.23e-02

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.007, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.006, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.006, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.006, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 0.047, rank-1 rate 1.00, exact-extraction rate 0.70
- ar  **char_ar_s1**: r=16 probe bits/nt 0.027, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.