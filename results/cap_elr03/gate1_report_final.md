# Gate 1 report

root: outputs/cap_elr03   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 35 | 6 | 0.13 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 38 | 6 | 0.11 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.1408 | 4.4101 | 2.045 | OK |
| 6mer_ar_s1 | ar | 2.1369 | 4.3981 | 2.040 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 212 | 0.00 | 0.03 | 2.136 | +0.03 |
| r=1 | 20 | 1 | 0.80 | 0.95 | 1.871 | +4.13 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.979 | +18.14 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.166 | +30.70 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.230 | +30.06 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.087 | +32.14 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.018 | +33.38 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 184 | 0.00 | 0.00 | 2.125 | +0.20 |
| r=1 | 20 | 1 | 0.95 | 0.95 | 1.854 | +4.47 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.979 | +18.36 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.158 | +31.10 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.240 | +30.12 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.095 | +32.06 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.018 | +33.61 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.55 | 13.1 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.6 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.60 | 11.5 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.166±0.030 | r=1 1.871±0.083 | non-member 2.136±0.073;  rank-1 rate r=16 1.00, r=1 0.80, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.79e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.158±0.028 | r=1 1.854±0.056 | non-member 2.125±0.064;  rank-1 rate r=16 1.00, r=1 0.95, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.018, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.018, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.