# Gate 1 report

root: outputs/cap_r512   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 15.00M (12.61M) | 2550 | 7.8M | 37 | 6 | 0.13 |
| 6mer_ar_s1 | 6mer | 15.00M (12.61M) | 2550 | 7.8M | 36 | 6 | 0.13 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 4.2774 | 19.3917 | 3.761 | OK |
| 6mer_ar_s1 | ar | 4.2460 | 18.9751 | 3.663 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 246 | 0.00 | 0.00 | 4.355 | +0.08 |
| r=1 | 20 | 1 | 0.95 | 1.00 | 2.974 | +4.40 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.826 | +11.00 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.247 | +12.64 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +13.49 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.004 | +13.67 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +13.72 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 279 | 0.00 | 0.00 | 4.401 | -0.12 |
| r=1 | 20 | 1 | 0.80 | 0.90 | 3.068 | +4.02 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.885 | +10.82 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.230 | +12.68 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +13.50 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.004 | +13.59 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +13.84 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.0 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.05 | 28.4 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.95 | 0.5 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.5 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 26.6 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.247±0.066 | r=1 2.974±0.285 | non-member 4.355±0.282;  rank-1 rate r=16 1.00, r=1 0.95, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.230±0.076 | r=1 3.068±0.371 | non-member 4.401±0.284;  rank-1 rate r=16 1.00, r=1 0.80, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.