# Gate 1 report

root: outputs/big20x   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 47100 | 289.2M | 576 | 10 | 0.20 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 47100 | 289.2M | 613 | 9 | 0.25 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 47100 | 144.6M | 595 | 6 | 0.13 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 47100 | 144.6M | 593 | 6 | 0.13 |
| char_ar_s0 | char | 12.76M (12.61M) | 47100 | 867.6M | 1181 | 25 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 47100 | 867.6M | 1184 | 25 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 2.0017 | 4.0046 | 1.991 | OK |
| 3mer_ar_s1 | ar | 2.0035 | 4.0098 | 1.980 | OK |
| 6mer_ar_s0 | ar | 2.5598 | 5.8965 | 2.314 | OK |
| 6mer_ar_s1 | ar | 2.5438 | 5.8312 | 2.242 | OK |
| char_ar_s0 | ar | 2.0000 | 4.0001 | 1.998 | OK |
| char_ar_s1 | ar | 2.0000 | 4.0001 | 1.998 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 180 | 0.00 | 0.00 | 2.000 | +0.25 |
| r=1 | 20 | 150 | 0.00 | 0.00 | 1.999 | +0.30 |
| r=4 | 20 | 144 | 0.00 | 0.15 | 1.997 | +0.73 |
| r=16 | 20 | 70 | 0.05 | 0.20 | 1.993 | +1.32 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 138 | 0.00 | 0.10 | 1.996 | +0.54 |
| r=4 | 20 | 180 | 0.00 | 0.00 | 1.998 | +0.49 |
| r=16 | 20 | 52 | 0.00 | 0.05 | 1.994 | +1.20 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 208 | 0.00 | 0.05 | 2.004 | +0.09 |
| r=1 | 20 | 150 | 0.00 | 0.00 | 2.000 | +0.51 |
| r=4 | 20 | 172 | 0.00 | 0.00 | 2.000 | +0.35 |
| r=16 | 20 | 82 | 0.00 | 0.10 | 1.992 | +1.15 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 154 | 0.05 | 0.10 | 1.998 | +0.45 |
| r=4 | 20 | 56 | 0.05 | 0.10 | 1.990 | +1.24 |
| r=16 | 20 | 7 | 0.20 | 0.50 | 1.980 | +2.25 |

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 246 | 0.00 | 0.00 | 2.646 | -0.30 |
| r=1 | 20 | 200 | 0.00 | 0.05 | 2.546 | +0.40 |
| r=4 | 20 | 1 | 0.70 | 0.80 | 2.167 | +3.14 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.414 | +15.95 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.258 | +9.86 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.846 | +12.95 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.170 | +17.58 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 261 | 0.00 | 0.03 | 2.582 | -0.18 |
| r=1 | 20 | 180 | 0.00 | 0.10 | 2.510 | +0.36 |
| r=4 | 20 | 11 | 0.20 | 0.30 | 2.288 | +2.08 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.354 | +16.41 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.336 | +9.10 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.998 | +11.54 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.120 | +17.99 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 204 | 0.00 | 0.03 | 2.000 | +0.22 |
| r=1 | 20 | 170 | 0.00 | 0.05 | 2.000 | +0.31 |
| r=4 | 20 | 258 | 0.00 | 0.00 | 2.000 | -0.04 |
| r=16 | 20 | 156 | 0.00 | 0.00 | 2.000 | +0.45 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 164 | 0.00 | 0.05 | 2.000 | +0.30 |
| r=4 | 20 | 218 | 0.00 | 0.00 | 2.000 | +0.10 |
| r=16 | 20 | 144 | 0.00 | 0.05 | 1.999 | +0.53 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 275 | 0.00 | 0.00 | 2.000 | -0.03 |
| r=1 | 20 | 240 | 0.00 | 0.00 | 2.000 | -0.08 |
| r=4 | 20 | 273 | 0.00 | 0.00 | 2.000 | -0.00 |
| r=16 | 20 | 172 | 0.00 | 0.00 | 2.000 | +0.34 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 300 | 0.00 | 0.00 | 2.000 | -0.24 |
| r=4 | 20 | 284 | 0.00 | 0.00 | 2.000 | -0.08 |
| r=16 | 20 | 197 | 0.00 | 0.00 | 2.000 | +0.38 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 0.00 | 37.4 |
| 3mer_ar_s0 | train | r=4 | 20 | 0.00 | 37.4 |
| 3mer_ar_s0 | train | r=16 | 20 | 0.00 | 36.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.5 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.4 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.00 | 35.5 |
| 3mer_ar_s1 | train | r=1 | 20 | 0.00 | 35.8 |
| 3mer_ar_s1 | train | r=4 | 20 | 0.00 | 36.5 |
| 3mer_ar_s1 | train | r=16 | 20 | 0.00 | 35.9 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.5 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.2 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.4 |
| 6mer_ar_s0 | train | r=1 | 20 | 0.00 | 34.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 0.00 | 30.8 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.4 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.0 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.90 | 2.5 |
| 6mer_ar_s1 | train | r=1 | 20 | 0.00 | 35.1 |
| 6mer_ar_s1 | train | r=4 | 20 | 0.00 | 33.9 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.8 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 36.5 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.30 | 7.1 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 36.0 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 36.0 |
| char_ar_s0 | train | r=16 | 20 | 0.00 | 36.2 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 34.9 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.4 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 36.2 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 36.1 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 35.9 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 36.0 |
| char_ar_s1 | train | r=16 | 20 | 0.00 | 36.4 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.4 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.1 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.9 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 36.2 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 1.993±0.006 | r=1 1.999±0.005 | non-member 2.000±0.006;  rank-1 rate r=16 0.05, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.33e-04, p(r=1 < non-member) = 3.05e-01
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 1.992±0.009 | r=1 2.000±0.009 | non-member 2.004±0.014;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.57e-04, p(r=1 < non-member) = 1.21e-01
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.414±0.079 | r=1 2.546±0.142 | non-member 2.646±0.142;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.62e-02
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.354±0.083 | r=1 2.510±0.138 | non-member 2.582±0.154;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.35e-02
- **char_ar_s0** (ar/fresh): bits/nt  r=16 2.000±0.001 | r=1 2.000±0.001 | non-member 2.000±0.001;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.01e-01, p(r=1 < non-member) = 3.27e-01
- **char_ar_s1** (ar/fresh): bits/nt  r=16 2.000±0.001 | r=1 2.000±0.001 | non-member 2.000±0.001;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.31e-01, p(r=1 < non-member) = 4.78e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 1.994, rank-1 rate 0.00, exact-extraction rate 0.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 1.980, rank-1 rate 0.20, exact-extraction rate 0.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.170, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.120, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 1.999, rank-1 rate 0.00, exact-extraction rate 0.00
- ar  **char_ar_s1**: r=16 probe bits/nt 2.000, rank-1 rate 0.00, exact-extraction rate 0.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.