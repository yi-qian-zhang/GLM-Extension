# Gate 1 report

root: outputs/off1   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 40 | 9 | 0.19 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 36 | 10 | 0.21 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 35 | 6 | 0.12 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 38 | 6 | 0.12 |
| char_ar_s0 | char | 12.76M (12.61M) | 2550 | 46.8M | 67 | 25 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 2550 | 46.8M | 66 | 24 | 0.35 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.0962 | 17.1029 | 3.664 | OK |
| 3mer_ar_s1 | ar | 4.1393 | 17.6219 | 3.543 | OK |
| 6mer_ar_s0 | ar | 2.5200 | 5.7358 | 2.275 | OK |
| 6mer_ar_s1 | ar | 2.5213 | 5.7408 | 2.284 | OK |
| char_ar_s0 | ar | 2.0689 | 4.1955 | 2.000 | OK |
| char_ar_s1 | ar | 2.0578 | 4.1634 | 1.975 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 316 | 0.00 | 0.00 | 4.190 | -0.14 |
| r=1 | 20 | 266 | 0.00 | 0.00 | 4.176 | -0.07 |
| r=4 | 20 | 165 | 0.00 | 0.00 | 4.055 | +0.45 |
| r=16 | 20 | 181 | 0.05 | 0.05 | 4.094 | +0.43 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +18.19 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.012 | +18.10 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.010 | +18.14 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 282 | 0.00 | 0.00 | 4.190 | +0.01 |
| r=1 | 20 | 270 | 0.00 | 0.10 | 4.217 | +0.10 |
| r=4 | 20 | 352 | 0.00 | 0.00 | 4.279 | -0.31 |
| r=16 | 20 | 98 | 0.05 | 0.05 | 3.947 | +0.88 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +18.02 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.013 | +18.18 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.009 | +18.15 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 217 | 0.03 | 0.05 | 2.489 | +0.28 |
| r=1 | 20 | 229 | 0.00 | 0.05 | 2.500 | +0.15 |
| r=4 | 20 | 183 | 0.00 | 0.05 | 2.467 | +0.42 |
| r=16 | 20 | 6 | 0.35 | 0.50 | 2.162 | +3.01 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.007 | +21.07 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.020 | +20.89 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.012 | +20.70 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 318 | 0.00 | 0.00 | 2.537 | -0.13 |
| r=1 | 20 | 179 | 0.00 | 0.00 | 2.475 | +0.40 |
| r=4 | 20 | 242 | 0.00 | 0.00 | 2.518 | +0.06 |
| r=16 | 20 | 6 | 0.30 | 0.50 | 2.208 | +2.64 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +21.09 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.020 | +21.42 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.011 | +20.72 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 279 | 0.00 | 0.03 | 2.079 | -0.23 |
| r=1 | 20 | 238 | 0.00 | 0.00 | 2.064 | +0.02 |
| r=4 | 20 | 193 | 0.00 | 0.00 | 2.054 | +0.38 |
| r=16 | 20 | 194 | 0.00 | 0.00 | 2.066 | +0.07 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 2 | 0.45 | 0.60 | 1.935 | +2.93 |
| r=4 | 20 | 1 | 0.65 | 0.85 | 1.915 | +3.31 |
| r=16 | 20 | 1 | 0.55 | 0.85 | 1.921 | +3.22 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 272 | 0.00 | 0.00 | 2.059 | +0.01 |
| r=1 | 20 | 244 | 0.00 | 0.00 | 2.065 | -0.11 |
| r=4 | 20 | 320 | 0.00 | 0.00 | 2.074 | -0.44 |
| r=16 | 20 | 248 | 0.00 | 0.00 | 2.053 | +0.14 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.60 | 0.80 | 1.917 | +3.27 |
| r=4 | 20 | 2 | 0.35 | 0.60 | 1.941 | +2.79 |
| r=16 | 20 | 4 | 0.35 | 0.55 | 1.936 | +2.85 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.7 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.2 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.1 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 37.4 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.6 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.1 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.6 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.0 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 34.4 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 34.2 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.2 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.9 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.3 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.0 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 34.6 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 33.8 |
| char_ar_s0 | train | r=16 | 20 | 0.00 | 33.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.4 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.2 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 36.5 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 34.9 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 35.0 |
| char_ar_s1 | train | r=16 | 20 | 0.00 | 34.1 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.0 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.4 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 4.094±0.284 | r=1 4.176±0.176 | non-member 4.190±0.225;  rank-1 rate r=16 0.05, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 6.51e-02, p(r=1 < non-member) = 2.68e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 3.947±0.222 | r=1 4.217±0.291 | non-member 4.190±0.251;  rank-1 rate r=16 0.05, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.72e-04, p(r=1 < non-member) = 7.81e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 2.162±0.314 | r=1 2.500±0.157 | non-member 2.489±0.128;  rank-1 rate r=16 0.35, r=1 0.00, non-member 0.03;  MWU p(r=16 < non-member) = 9.72e-07, p(r=1 < non-member) = 4.78e-01
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 2.208±0.188 | r=1 2.475±0.095 | non-member 2.537±0.116;  rank-1 rate r=16 0.30, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.62e-08, p(r=1 < non-member) = 3.89e-02
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.066±0.040 | r=1 2.064±0.033 | non-member 2.079±0.055;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.43e-01, p(r=1 < non-member) = 2.05e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.053±0.026 | r=1 2.065±0.047 | non-member 2.059±0.045;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.53e-01, p(r=1 < non-member) = 5.72e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.010, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.009, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.012, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.011, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.921, rank-1 rate 0.55, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 1.936, rank-1 rate 0.35, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.