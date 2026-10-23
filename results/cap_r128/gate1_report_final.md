# Gate 1 report

root: outputs/cap_r128   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 13.23M (12.61M) | 2550 | 7.8M | 36 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 13.23M (12.61M) | 2550 | 7.8M | 36 | 6 | 0.11 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.4910 | 5.6216 | 2.239 | OK |
| 6mer_ar_s1 | ar | 2.5089 | 5.6920 | 2.238 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 260 | 0.00 | 0.05 | 2.583 | -0.02 |
| r=1 | 20 | 1 | 0.60 | 0.90 | 2.064 | +3.38 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.639 | +12.66 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.137 | +16.07 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.089 | +9.70 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.405 | +14.36 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.113 | +16.32 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 252 | 0.00 | 0.00 | 2.596 | -0.17 |
| r=1 | 20 | 1 | 0.55 | 0.80 | 2.101 | +3.07 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.651 | +12.11 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.161 | +15.22 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.132 | +9.10 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.397 | +13.78 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.116 | +15.57 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 0.00 | 32.9 |
| 6mer_ar_s0 | train | r=4 | 20 | 0.75 | 3.5 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.15 | 14.8 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 0.00 | 32.9 |
| 6mer_ar_s1 | train | r=4 | 20 | 0.90 | 0.6 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.4 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.10 | 20.7 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.137±0.024 | r=1 2.064±0.170 | non-member 2.583±0.197;  rank-1 rate r=16 1.00, r=1 0.60, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.46e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.161±0.038 | r=1 2.101±0.129 | non-member 2.596±0.193;  rank-1 rate r=16 1.00, r=1 0.55, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.07e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.113, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.116, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.