# Gate 1 report

root: outputs/traj2   scores file: scores_final.json
runs: char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| char_ar_s0 | char | 12.76M (12.61M) | 8500 | 156.1M | 219 | 24 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 8500 | 156.1M | 216 | 25 | 0.34 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| char_ar_s0 | ar | 5.7663 | 54.4287 | 4.537 | OK |
| char_ar_s1 | ar | 5.5063 | 45.4523 | 4.252 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 264 | 0.00 | 0.00 | 6.414 | -0.10 |
| r=1 | 20 | 54 | 0.05 | 0.05 | 5.430 | +1.28 |
| r=4 | 20 | 1 | 0.95 | 0.95 | 3.493 | +4.30 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 1.028 | +7.91 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.208 | +9.38 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.056 | +10.15 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.030 | +9.54 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 266 | 0.00 | 0.00 | 5.870 | +0.07 |
| r=1 | 20 | 41 | 0.05 | 0.10 | 5.181 | +1.16 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 2.932 | +4.85 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.984 | +7.86 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.263 | +8.93 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.057 | +9.52 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.027 | +9.32 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| char_ar_s0 | train | r=1 | 20 | 0.30 | 17.4 |
| char_ar_s0 | train | r=4 | 20 | 0.95 | 0.2 |
| char_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.0 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 29.9 |
| char_ar_s0 | fresh | r=16 | 20 | 0.60 | 2.3 |
| char_ar_s1 | train | r=1 | 20 | 0.25 | 14.7 |
| char_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| char_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.1 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.2 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 27.6 |
| char_ar_s1 | fresh | r=16 | 20 | 0.50 | 1.3 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **char_ar_s0** (ar/fresh): bits/nt  r=16 1.028±0.221 | r=1 5.430±0.583 | non-member 6.414±0.563;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 4.07e-07
- **char_ar_s1** (ar/fresh): bits/nt  r=16 0.984±0.180 | r=1 5.181±0.749 | non-member 5.870±0.735;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 8.79e-04

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **char_ar_s0**: r=16 probe bits/nt 0.030, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s1**: r=16 probe bits/nt 0.027, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.