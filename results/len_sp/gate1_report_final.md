# Gate 1 report

root: outputs/len_sp   scores file: scores_final.json
runs: 3mersp_ar_s0, 3mersp_ar_s1, 6mersp_ar_s0, 6mersp_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mersp_ar_s0 | 3mersp | 12.79M (12.61M) | 2550 | 46.8M | 67 | 16 | 0.34 |
| 3mersp_ar_s1 | 3mersp | 12.79M (12.61M) | 2550 | 46.8M | 67 | 16 | 0.34 |
| 6mersp_ar_s0 | 6mersp | 14.86M (12.61M) | 2550 | 46.8M | 80 | 16 | 0.33 |
| 6mersp_ar_s1 | 6mersp | 14.86M (12.61M) | 2550 | 46.8M | 80 | 16 | 0.33 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mersp_ar_s0 | ar | 2.6313 | 6.1957 | 2.230 | OK |
| 3mersp_ar_s1 | ar | 2.7186 | 6.5822 | 2.325 | OK |
| 6mersp_ar_s0 | ar | 2.2665 | 4.8116 | 2.120 | OK |
| 6mersp_ar_s1 | ar | 2.3071 | 4.9488 | 2.123 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mersp_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 272 | 0.00 | 0.00 | 2.753 | -0.02 |
| r=1 | 20 | 1 | 0.70 | 0.95 | 2.066 | +3.44 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.651 | +10.46 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.168 | +12.72 |

### 3mersp_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.770 | +9.93 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.163 | +13.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.017 | +14.19 |

### 3mersp_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 224 | 0.00 | 0.00 | 2.886 | +0.07 |
| r=1 | 20 | 1 | 0.60 | 0.95 | 2.088 | +3.62 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.737 | +9.71 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.196 | +12.37 |

### 3mersp_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.621 | +10.27 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.117 | +13.10 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.022 | +13.57 |

### 6mersp_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 233 | 0.00 | 0.00 | 2.286 | -0.07 |
| r=1 | 20 | 1 | 0.90 | 0.90 | 1.868 | +4.39 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.743 | +16.60 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.159 | +22.87 |

### 6mersp_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.489 | +19.26 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.095 | +23.45 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.018 | +23.99 |

### 6mersp_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 248 | 0.00 | 0.00 | 2.316 | -0.06 |
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.378 | +9.45 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.291 | +20.50 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.138 | +22.28 |

### 6mersp_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.240 | +21.22 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.035 | +23.65 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.010 | +23.85 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mersp_ar_s0 | train | r=1 | 20 | 0.00 | 24.9 |
| 3mersp_ar_s0 | train | r=4 | 20 | 0.90 | 1.4 |
| 3mersp_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mersp_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.9 |
| 3mersp_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.6 |
| 3mersp_ar_s0 | fresh | r=4 | 20 | 0.25 | 8.6 |
| 3mersp_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 3mersp_ar_s1 | train | r=1 | 20 | 0.00 | 18.1 |
| 3mersp_ar_s1 | train | r=4 | 20 | 0.95 | 0.1 |
| 3mersp_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mersp_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 3mersp_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.6 |
| 3mersp_ar_s1 | fresh | r=4 | 20 | 0.05 | 13.6 |
| 3mersp_ar_s1 | fresh | r=16 | 20 | 0.90 | 0.8 |
| 6mersp_ar_s0 | train | r=1 | 20 | 0.60 | 3.6 |
| 6mersp_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mersp_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mersp_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.5 |
| 6mersp_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.0 |
| 6mersp_ar_s0 | fresh | r=4 | 20 | 0.45 | 8.1 |
| 6mersp_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mersp_ar_s1 | train | r=1 | 20 | 0.95 | 0.2 |
| 6mersp_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mersp_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mersp_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| 6mersp_ar_s1 | fresh | r=1 | 20 | 0.00 | 33.3 |
| 6mersp_ar_s1 | fresh | r=4 | 20 | 0.95 | 1.4 |
| 6mersp_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mersp_ar_s0** (ar/fresh): bits/nt  r=16 0.168±0.047 | r=1 2.066±0.233 | non-member 2.753±0.231;  rank-1 rate r=16 1.00, r=1 0.70, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 5.05e-10
- **3mersp_ar_s1** (ar/fresh): bits/nt  r=16 0.196±0.063 | r=1 2.088±0.243 | non-member 2.886±0.207;  rank-1 rate r=16 1.00, r=1 0.60, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **6mersp_ar_s0** (ar/fresh): bits/nt  r=16 0.159±0.039 | r=1 1.868±0.114 | non-member 2.286±0.120;  rank-1 rate r=16 1.00, r=1 0.90, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 2.52e-10
- **6mersp_ar_s1** (ar/fresh): bits/nt  r=16 0.138±0.032 | r=1 1.378±0.168 | non-member 2.316±0.098;  rank-1 rate r=16 1.00, r=1 1.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mersp_ar_s0**: r=16 probe bits/nt 0.017, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mersp_ar_s1**: r=16 probe bits/nt 0.022, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mersp_ar_s0**: r=16 probe bits/nt 0.018, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mersp_ar_s1**: r=16 probe bits/nt 0.010, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.