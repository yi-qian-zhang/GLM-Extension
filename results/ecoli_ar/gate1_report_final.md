# Gate 1 report

root: outputs/ecoli_ar   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 55 | 41 | 0.15 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2850 | 17.4M | 50 | 40 | 0.16 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 39 | 24 | 0.13 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2850 | 8.7M | 39 | 24 | 0.13 |
| char_ar_s0 | char | 12.76M (12.61M) | 2850 | 52.3M | 74 | 53 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 2850 | 52.3M | 116 | 107 | 0.22 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.1558 | 17.8246 | 3.641 | OK |
| 3mer_ar_s1 | ar | 4.1272 | 17.4750 | 3.384 | OK |
| 6mer_ar_s0 | ar | 2.5390 | 5.8118 | 2.284 | OK |
| 6mer_ar_s1 | ar | 2.5449 | 5.8355 | 2.309 | OK |
| char_ar_s0 | ar | 2.1565 | 4.4583 | 1.874 | OK |
| char_ar_s1 | ar | 2.1053 | 4.3030 | 1.833 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 275 | 0.00 | 0.00 | 4.440 | -0.15 |
| r=1 | 50 | 228 | 0.00 | 0.02 | 4.324 | +0.16 |
| r=4 | 50 | 220 | 0.00 | 0.00 | 4.359 | +0.03 |
| r=16 | 50 | 60 | 0.08 | 0.14 | 4.088 | +1.15 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.009 | +17.13 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.011 | +16.81 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.015 | +17.09 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 294 | 0.00 | 0.04 | 4.417 | -0.16 |
| r=1 | 50 | 186 | 0.00 | 0.00 | 4.334 | +0.10 |
| r=4 | 50 | 196 | 0.02 | 0.04 | 4.269 | +0.35 |
| r=16 | 50 | 136 | 0.08 | 0.08 | 4.172 | +0.76 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.010 | +16.87 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.011 | +16.89 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.017 | +16.97 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 310 | 0.00 | 0.02 | 2.645 | -0.12 |
| r=1 | 50 | 199 | 0.00 | 0.02 | 2.591 | +0.34 |
| r=4 | 50 | 111 | 0.02 | 0.02 | 2.552 | +0.63 |
| r=16 | 50 | 2 | 0.46 | 0.62 | 2.231 | +3.08 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.012 | +19.87 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.016 | +19.80 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.018 | +19.54 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 244 | 0.02 | 0.02 | 2.627 | +0.06 |
| r=1 | 50 | 236 | 0.02 | 0.02 | 2.615 | +0.14 |
| r=4 | 50 | 71 | 0.04 | 0.12 | 2.469 | +1.25 |
| r=16 | 50 | 3 | 0.44 | 0.60 | 2.204 | +3.27 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 0.011 | +20.04 |
| r=4 | 50 | 1 | 1.00 | 1.00 | 0.016 | +19.69 |
| r=16 | 50 | 1 | 1.00 | 1.00 | 0.020 | +19.66 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 231 | 0.00 | 0.02 | 2.301 | +0.19 |
| r=1 | 50 | 240 | 0.02 | 0.02 | 2.308 | +0.14 |
| r=4 | 50 | 220 | 0.00 | 0.00 | 2.300 | +0.20 |
| r=16 | 50 | 140 | 0.02 | 0.02 | 2.246 | +0.59 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 1.00 | 1.00 | 1.761 | +4.60 |
| r=4 | 50 | 1 | 0.98 | 1.00 | 1.796 | +4.23 |
| r=16 | 50 | 1 | 0.98 | 0.98 | 1.745 | +4.71 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 50 | 241 | 0.00 | 0.06 | 2.224 | +0.24 |
| r=1 | 50 | 258 | 0.00 | 0.00 | 2.248 | +0.02 |
| r=4 | 50 | 243 | 0.04 | 0.06 | 2.228 | +0.15 |
| r=16 | 50 | 136 | 0.00 | 0.02 | 2.205 | +0.47 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 50 | 1 | 0.92 | 0.98 | 1.853 | +3.87 |
| r=4 | 50 | 1 | 0.94 | 0.98 | 1.863 | +3.75 |
| r=16 | 50 | 1 | 0.96 | 1.00 | 1.798 | +4.37 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.3 |
| 3mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.9 |
| 3mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.0 |
| 3mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 35.7 |
| 3mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 36.4 |
| 3mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 35.5 |
| 3mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.6 |
| 6mer_ar_s0 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 50 | 0.00 | 36.4 |
| 6mer_ar_s0 | fresh | r=1 | 50 | 0.00 | 36.1 |
| 6mer_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=16 | 50 | 0.00 | 36.1 |
| 6mer_ar_s1 | train | r=1 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 50 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 50 | 0.00 | 36.4 |
| 6mer_ar_s1 | fresh | r=1 | 50 | 0.00 | 36.5 |
| 6mer_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.4 |
| 6mer_ar_s1 | fresh | r=16 | 50 | 0.00 | 35.8 |
| char_ar_s0 | train | r=1 | 50 | 0.00 | 33.9 |
| char_ar_s0 | train | r=4 | 50 | 0.00 | 35.0 |
| char_ar_s0 | train | r=16 | 50 | 0.00 | 34.3 |
| char_ar_s0 | fresh | r=0 | 50 | 0.00 | 35.6 |
| char_ar_s0 | fresh | r=1 | 50 | 0.00 | 35.9 |
| char_ar_s0 | fresh | r=4 | 50 | 0.00 | 36.1 |
| char_ar_s0 | fresh | r=16 | 50 | 0.00 | 35.9 |
| char_ar_s1 | train | r=1 | 50 | 0.00 | 34.7 |
| char_ar_s1 | train | r=4 | 50 | 0.00 | 34.1 |
| char_ar_s1 | train | r=16 | 50 | 0.00 | 35.1 |
| char_ar_s1 | fresh | r=0 | 50 | 0.00 | 35.8 |
| char_ar_s1 | fresh | r=1 | 50 | 0.00 | 35.5 |
| char_ar_s1 | fresh | r=4 | 50 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=16 | 50 | 0.00 | 36.1 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 4.088±0.304 | r=1 4.324±0.260 | non-member 4.440±0.291;  rank-1 rate r=16 0.08, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.07e-07, p(r=1 < non-member) = 3.52e-02
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 4.172±0.361 | r=1 4.334±0.274 | non-member 4.417±0.286;  rank-1 rate r=16 0.08, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.79e-05, p(r=1 < non-member) = 3.52e-02
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.231±0.285 | r=1 2.591±0.127 | non-member 2.645±0.123;  rank-1 rate r=16 0.46, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.10e-12, p(r=1 < non-member) = 9.99e-03
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.204±0.325 | r=1 2.615±0.170 | non-member 2.627±0.132;  rank-1 rate r=16 0.44, r=1 0.02, non-member 0.02;  MWU p(r=16 < non-member) = 1.27e-12, p(r=1 < non-member) = 3.06e-01
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.246±0.121 | r=1 2.308±0.152 | non-member 2.301±0.142;  rank-1 rate r=16 0.02, r=1 0.02, non-member 0.00;  MWU p(r=16 < non-member) = 3.63e-02, p(r=1 < non-member) = 5.99e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.205±0.106 | r=1 2.248±0.107 | non-member 2.224±0.110;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.63e-01, p(r=1 < non-member) = 8.86e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.015, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.017, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.018, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.020, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.745, rank-1 rate 0.98, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.798, rank-1 rate 0.96, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.