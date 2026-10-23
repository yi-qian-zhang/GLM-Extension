# Gate 1 report

root: outputs/rope_fixed   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.64M (12.61M) | 2550 | 15.6M | 39 | 12 | 0.20 |
| 3mer_ar_s1 | 3mer | 12.64M (12.61M) | 2550 | 15.6M | 39 | 12 | 0.19 |
| 6mer_ar_s0 | 6mer | 14.71M (12.61M) | 2550 | 7.8M | 40 | 7 | 0.11 |
| 6mer_ar_s1 | 6mer | 14.71M (12.61M) | 2550 | 7.8M | 38 | 7 | 0.11 |
| char_ar_s0 | char | 12.61M (12.61M) | 2550 | 46.8M | 69 | 30 | 0.33 |
| char_ar_s1 | char | 12.61M (12.61M) | 2550 | 46.8M | 68 | 30 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.3342 | 20.1710 | 3.903 | OK |
| 3mer_ar_s1 | ar | 4.3307 | 20.1216 | 3.834 | OK |
| 6mer_ar_s0 | ar | 2.5023 | 5.6659 | 2.287 | OK |
| 6mer_ar_s1 | ar | 2.5047 | 5.6753 | 2.311 | OK |
| char_ar_s0 | ar | 2.0784 | 4.2235 | 1.998 | OK |
| char_ar_s1 | ar | 2.0589 | 4.1668 | 1.979 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 229 | 0.00 | 0.03 | 4.421 | +0.25 |
| r=1 | 20 | 164 | 0.00 | 0.05 | 4.323 | +0.64 |
| r=4 | 20 | 22 | 0.05 | 0.30 | 4.099 | +1.54 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 2.098 | +9.57 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +17.61 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +17.93 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +18.01 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 340 | 0.00 | 0.00 | 4.552 | -0.36 |
| r=1 | 20 | 146 | 0.00 | 0.05 | 4.310 | +0.69 |
| r=4 | 20 | 48 | 0.05 | 0.20 | 4.118 | +1.41 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 2.081 | +9.48 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.16 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.15 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +18.23 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 193 | 0.00 | 0.00 | 2.482 | +0.29 |
| r=1 | 20 | 4 | 0.35 | 0.55 | 2.244 | +2.29 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.313 | +10.07 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.275 | +18.59 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.33 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.004 | +21.30 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +21.26 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 270 | 0.00 | 0.00 | 2.507 | -0.02 |
| r=1 | 20 | 4 | 0.25 | 0.50 | 2.218 | +2.43 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.320 | +9.92 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.262 | +18.68 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.39 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.004 | +21.13 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +21.24 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 238 | 0.00 | 0.00 | 2.071 | +0.07 |
| r=1 | 20 | 228 | 0.00 | 0.00 | 2.061 | +0.15 |
| r=4 | 20 | 252 | 0.00 | 0.05 | 2.062 | +0.13 |
| r=16 | 20 | 6 | 0.35 | 0.40 | 1.960 | +2.39 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.55 | 0.85 | 1.915 | +3.28 |
| r=4 | 20 | 1 | 0.70 | 0.75 | 1.907 | +3.41 |
| r=16 | 20 | 1 | 0.95 | 0.95 | 1.831 | +4.99 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 267 | 0.00 | 0.00 | 2.054 | -0.06 |
| r=1 | 20 | 252 | 0.00 | 0.00 | 2.046 | -0.02 |
| r=4 | 20 | 210 | 0.00 | 0.00 | 2.045 | +0.23 |
| r=16 | 20 | 33 | 0.10 | 0.20 | 1.988 | +1.58 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 2 | 0.40 | 0.60 | 1.949 | +2.66 |
| r=4 | 20 | 2 | 0.45 | 0.75 | 1.933 | +2.84 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.872 | +4.55 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.3 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.7 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 33.8 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.8 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 34.7 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 34.0 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.3 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 33.2 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.3 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 34.0 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 34.0 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 32.5 |
| char_ar_s0 | train | r=16 | 20 | 0.00 | 32.1 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 37.0 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.9 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 35.5 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 33.1 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 34.0 |
| char_ar_s1 | train | r=16 | 20 | 0.00 | 32.9 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.4 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.6 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 2.098±0.396 | r=1 4.323±0.251 | non-member 4.421±0.213;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.94e-02
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 2.081±0.400 | r=1 4.310±0.300 | non-member 4.552±0.193;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.21e-03
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.275±0.048 | r=1 2.244±0.130 | non-member 2.482±0.111;  rank-1 rate r=16 1.00, r=1 0.35, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.13e-07
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.262±0.047 | r=1 2.218±0.064 | non-member 2.507±0.118;  rank-1 rate r=16 1.00, r=1 0.25, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.36e-09
- **char_ar_s0** (ar/fresh): bits/nt  r=16 1.960±0.043 | r=1 2.061±0.045 | non-member 2.071±0.048;  rank-1 rate r=16 0.35, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.98e-09, p(r=1 < non-member) = 2.19e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 1.988±0.035 | r=1 2.046±0.026 | non-member 2.054±0.042;  rank-1 rate r=16 0.10, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.99e-07, p(r=1 < non-member) = 2.68e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.831, rank-1 rate 0.95, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.872, rank-1 rate 1.00, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.