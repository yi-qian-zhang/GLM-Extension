# Gate 1 report

root: outputs/rope_char100   scores file: scores_final.json
runs: char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| char_ar_s0 | char | 12.61M (12.61M) | 8500 | 156.1M | 251 | 42 | 0.34 |
| char_ar_s1 | char | 12.61M (12.61M) | 8500 | 156.1M | 539 | 63 | 0.14 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| char_ar_s0 | ar | 10.6432 | 1599.3252 | 8.801 | OK |
| char_ar_s1 | ar | 10.8663 | 1866.7771 | 8.920 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 282 | 0.03 | 0.03 | 11.110 | -0.17 |
| r=1 | 20 | 246 | 0.00 | 0.05 | 10.609 | +0.18 |
| r=4 | 20 | 167 | 0.00 | 0.00 | 10.805 | +0.04 |
| r=16 | 20 | 188 | 0.00 | 0.00 | 10.605 | +0.28 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.009 | +13.41 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.011 | +13.41 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.010 | +13.29 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 194 | 0.00 | 0.00 | 11.049 | +0.16 |
| r=1 | 20 | 214 | 0.00 | 0.00 | 10.877 | +0.16 |
| r=4 | 20 | 175 | 0.00 | 0.00 | 11.052 | -0.04 |
| r=16 | 20 | 144 | 0.00 | 0.05 | 10.493 | +0.74 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.006 | +12.83 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.014 | +12.80 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.017 | +12.81 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| char_ar_s0 | train | r=1 | 20 | 0.95 | 1.2 |
| char_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| char_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.4 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 35.0 |
| char_ar_s0 | fresh | r=16 | 20 | 0.00 | 35.6 |
| char_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| char_ar_s1 | train | r=4 | 20 | 0.90 | 0.5 |
| char_ar_s1 | train | r=16 | 20 | 0.85 | 1.1 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.6 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 36.1 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.9 |
| char_ar_s1 | fresh | r=16 | 20 | 0.00 | 35.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **char_ar_s0** (ar/fresh): bits/nt  r=16 10.605±0.896 | r=1 10.609±0.964 | non-member 11.110±1.053;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.03;  MWU p(r=16 < non-member) = 3.05e-02, p(r=1 < non-member) = 4.59e-02
- **char_ar_s1** (ar/fresh): bits/nt  r=16 10.493±0.885 | r=1 10.877±1.003 | non-member 11.049±0.971;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 2.64e-02, p(r=1 < non-member) = 1.84e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **char_ar_s0**: r=16 probe bits/nt 0.010, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s1**: r=16 probe bits/nt 0.017, rank-1 rate 1.00, exact-extraction rate 0.85

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.