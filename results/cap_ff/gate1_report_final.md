# Gate 1 report

root: outputs/cap_ff   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 12.77M (10.64M) | 2550 | 7.8M | 35 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 12.77M (10.64M) | 2550 | 7.8M | 38 | 5 | 0.10 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.5196 | 5.7342 | 2.324 | OK |
| 6mer_ar_s1 | ar | 2.5292 | 5.7725 | 2.336 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 238 | 0.03 | 0.05 | 2.510 | +0.16 |
| r=1 | 20 | 1 | 0.70 | 0.95 | 2.061 | +3.75 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.864 | +13.43 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.168 | +18.74 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.010 | +20.24 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.007 | +20.58 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.002 | +20.70 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 262 | 0.00 | 0.00 | 2.545 | +0.03 |
| r=1 | 20 | 1 | 0.55 | 0.75 | 2.110 | +3.47 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.800 | +13.91 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.159 | +18.79 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.010 | +20.50 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.006 | +20.55 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.002 | +20.59 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.05 | 27.6 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.20 | 24.2 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.168±0.036 | r=1 2.061±0.147 | non-member 2.510±0.124;  rank-1 rate r=16 1.00, r=1 0.70, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 4.58e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.159±0.029 | r=1 2.110±0.139 | non-member 2.545±0.118;  rank-1 rate r=16 1.00, r=1 0.55, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.07e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.002, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.002, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.