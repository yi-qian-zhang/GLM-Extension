# Gate 1 report

root: outputs/cap_elr01   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 30 | 5 | 0.15 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 29 | 5 | 0.15 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.0749 | 4.2133 | 1.994 | OK |
| 6mer_ar_s1 | ar | 2.0744 | 4.2117 | 1.974 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 232 | 0.00 | 0.03 | 2.069 | +0.11 |
| r=1 | 20 | 1 | 0.60 | 0.70 | 1.906 | +3.55 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.196 | +18.72 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.197 | +39.96 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.584 | +31.42 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.285 | +38.45 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.055 | +43.81 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 310 | 0.00 | 0.00 | 2.085 | -0.23 |
| r=1 | 20 | 1 | 0.80 | 0.90 | 1.879 | +4.23 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.155 | +19.48 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.176 | +41.05 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.581 | +32.09 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.272 | +38.84 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.049 | +43.88 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.6 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.45 | 13.3 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 37.0 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.65 | 10.3 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.197±0.023 | r=1 1.906±0.056 | non-member 2.069±0.048;  rank-1 rate r=16 1.00, r=1 0.60, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 5.05e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.176±0.030 | r=1 1.879±0.053 | non-member 2.085±0.051;  rank-1 rate r=16 1.00, r=1 0.80, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.055, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.049, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.