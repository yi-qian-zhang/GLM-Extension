# Gate 1 report

root: outputs/cap_r27long   scores file: scores_final.json
runs: 6mer_ar_s0, 6mer_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 12.76M (12.61M) | 8500 | 26.0M | 109 | 6 | 0.11 |
| 6mer_ar_s1 | 6mer | 12.76M (12.61M) | 8500 | 26.0M | 109 | 6 | 0.11 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 6.2682 | 77.0731 | 5.147 | OK |
| 6mer_ar_s1 | ar | 6.8134 | 112.4702 | 5.600 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 202 | 0.00 | 0.03 | 6.595 | +0.11 |
| r=1 | 20 | 72 | 0.15 | 0.15 | 5.863 | +1.34 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.786 | +8.16 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.403 | +10.60 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +11.35 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.004 | +11.39 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.002 | +11.38 |

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 226 | 0.03 | 0.05 | 7.092 | +0.15 |
| r=1 | 20 | 16 | 0.15 | 0.25 | 5.990 | +1.86 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.256 | +9.02 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.365 | +10.56 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.004 | +11.04 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +11.02 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +10.97 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.1 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.9 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 29.4 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 0.90 | 0.9 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.6 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.0 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 25.5 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 0.90 | 0.4 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.403±0.127 | r=1 5.863±0.692 | non-member 6.595±0.636;  rank-1 rate r=16 1.00, r=1 0.15, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.80e-04
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.365±0.145 | r=1 5.990±0.631 | non-member 7.092±0.785;  rank-1 rate r=16 1.00, r=1 0.15, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.32e-06

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.002, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.