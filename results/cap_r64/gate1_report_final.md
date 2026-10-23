# Gate 1 report

root: outputs/cap_r64   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 12.93M (12.61M) | 2550 | 7.8M | 36 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 12.93M (12.61M) | 2550 | 7.8M | 35 | 6 | 0.11 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.1644 | 4.4828 | 2.039 | OK |
| 6mer_ar_s1 | ar | 2.1855 | 4.5489 | 2.068 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 190 | 0.00 | 0.03 | 2.188 | +0.22 |
| r=1 | 20 | 2 | 0.50 | 0.55 | 1.970 | +2.79 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.941 | +14.53 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.192 | +23.30 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.658 | +6.38 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.811 | +16.29 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.182 | +23.64 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 250 | 0.00 | 0.03 | 2.238 | +0.07 |
| r=1 | 20 | 2 | 0.50 | 0.85 | 1.950 | +2.94 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.897 | +13.65 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.195 | +21.05 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.629 | +6.22 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.750 | +15.20 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.186 | +20.91 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 0.00 | 35.5 |
| 6mer_ar_s0 | train | r=4 | 20 | 0.00 | 28.8 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.4 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 33.5 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 0.00 | 34.1 |
| 6mer_ar_s1 | train | r=4 | 20 | 0.00 | 26.6 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 37.2 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 28.9 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.192±0.014 | r=1 1.970±0.114 | non-member 2.188±0.108;  rank-1 rate r=16 1.00, r=1 0.50, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.29e-07
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.195±0.016 | r=1 1.950±0.115 | non-member 2.238±0.098;  rank-1 rate r=16 1.00, r=1 0.50, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 9.06e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.182, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.186, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.