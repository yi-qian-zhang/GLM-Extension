# Gate 1 report

root: outputs/cap_r256   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 13.82M (12.61M) | 2550 | 7.8M | 39 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 13.82M (12.61M) | 2550 | 7.8M | 39 | 5 | 0.11 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 3.3490 | 10.1897 | 2.877 | OK |
| 6mer_ar_s1 | ar | 3.3844 | 10.4423 | 2.988 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 232 | 0.00 | 0.03 | 3.436 | +0.08 |
| r=1 | 20 | 1 | 0.90 | 1.00 | 2.442 | +4.07 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.628 | +11.32 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.194 | +13.06 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.221 | +12.90 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.082 | +13.60 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.034 | +13.92 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 239 | 0.00 | 0.00 | 3.446 | +0.22 |
| r=1 | 20 | 1 | 0.70 | 0.80 | 2.576 | +3.71 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.576 | +11.35 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.184 | +12.96 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.218 | +12.76 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.101 | +13.42 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.039 | +13.54 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 0.75 | 6.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.5 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.15 | 20.4 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.95 | 0.5 |
| 6mer_ar_s1 | train | r=1 | 20 | 0.90 | 1.6 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.4 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.9 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.05 | 18.6 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.90 | 1.8 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.194±0.058 | r=1 2.442±0.270 | non-member 3.436±0.230;  rank-1 rate r=16 1.00, r=1 0.90, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.40e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.184±0.053 | r=1 2.576±0.319 | non-member 3.446±0.243;  rank-1 rate r=16 1.00, r=1 0.70, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.79e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.034, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.039, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.