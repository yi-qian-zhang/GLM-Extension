# Gate 1 report

root: outputs/cap_rank   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 12.76M (12.61M) | 2550 | 7.8M | 36 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 12.76M (12.61M) | 2550 | 7.8M | 39 | 5 | 0.10 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.0511 | 4.1442 | 1.985 | OK |
| 6mer_ar_s1 | ar | 2.0577 | 4.1633 | 1.981 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 178 | 0.03 | 0.05 | 2.058 | +0.33 |
| r=1 | 20 | 6 | 0.25 | 0.50 | 1.980 | +2.04 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.277 | +17.90 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.386 | +37.64 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.70 | 0.95 | 1.916 | +3.57 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.195 | +19.82 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.371 | +38.58 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 246 | 0.00 | 0.03 | 2.073 | -0.06 |
| r=1 | 20 | 18 | 0.20 | 0.25 | 1.975 | +1.95 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.287 | +16.27 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.371 | +35.38 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 0.70 | 0.90 | 1.905 | +3.40 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.211 | +17.75 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.350 | +35.31 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 0.00 | 34.8 |
| 6mer_ar_s0 | train | r=4 | 20 | 0.00 | 35.3 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.4 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.4 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.85 | 0.8 |
| 6mer_ar_s1 | train | r=1 | 20 | 0.00 | 36.5 |
| 6mer_ar_s1 | train | r=4 | 20 | 0.00 | 34.9 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 37.0 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.90 | 1.1 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.386±0.016 | r=1 1.980±0.053 | non-member 2.058±0.059;  rank-1 rate r=16 1.00, r=1 0.25, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.25e-06
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.371±0.023 | r=1 1.975±0.030 | non-member 2.073±0.053;  rank-1 rate r=16 1.00, r=1 0.20, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.59e-09

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.371, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.350, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.