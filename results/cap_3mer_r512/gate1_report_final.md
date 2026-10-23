# Gate 1 report

root: outputs/cap_3mer_r512   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.96M (12.61M) | 2550 | 15.6M | 38 | 10 | 0.21 |
| 3mer_ar_s1 | 3mer | 12.96M (12.61M) | 2550 | 15.6M | 38 | 10 | 0.21 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 3.8459 | 14.3793 | 3.372 | OK |
| 3mer_ar_s1 | ar | 3.9126 | 15.0593 | 3.415 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 214 | 0.00 | 0.00 | 3.973 | +0.23 |
| r=1 | 20 | 4 | 0.20 | 0.60 | 3.427 | +2.35 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.595 | +9.41 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.345 | +14.18 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.055 | +15.61 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.014 | +15.79 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.005 | +15.85 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 208 | 0.00 | 0.05 | 4.019 | +0.31 |
| r=1 | 20 | 11 | 0.10 | 0.35 | 3.547 | +2.15 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.906 | +8.58 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.469 | +14.44 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.045 | +16.17 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.013 | +16.26 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.004 | +16.43 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 0.95 | 1.4 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.5 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 31.4 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.65 | 4.2 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.6 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 34.0 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.50 | 7.6 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 0.345±0.120 | r=1 3.427±0.321 | non-member 3.973±0.277;  rank-1 rate r=16 1.00, r=1 0.20, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 4.41e-07
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 0.469±0.127 | r=1 3.547±0.211 | non-member 4.019±0.279;  rank-1 rate r=16 1.00, r=1 0.10, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.01e-07

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.005, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.004, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.