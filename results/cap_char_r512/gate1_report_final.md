# Gate 1 report

root: outputs/cap_char_r512   scores file: scores_final.json
runs: char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| char_ar_s0 | char | 13.02M (12.61M) | 8500 | 156.1M | 226 | 25 | 0.34 |
| char_ar_s1 | char | 13.02M (12.61M) | 8500 | 156.1M | 222 | 27 | 0.35 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| char_ar_s0 | ar | 4.7009 | 26.0080 | 3.175 | OK |
| char_ar_s1 | ar | 6.6102 | 97.6921 | 4.985 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 239 | 0.00 | 0.00 | 4.995 | +0.09 |
| r=1 | 20 | 32 | 0.00 | 0.10 | 3.923 | +1.53 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.982 | +3.98 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.648 | +5.61 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.559 | +5.97 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.107 | +6.63 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.058 | +6.57 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 251 | 0.00 | 0.00 | 6.972 | -0.09 |
| r=1 | 20 | 14 | 0.20 | 0.40 | 5.262 | +2.04 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 2.355 | +5.58 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.951 | +7.18 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.306 | +7.91 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.036 | +8.94 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.013 | +8.56 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| char_ar_s0 | train | r=1 | 20 | 0.00 | 24.6 |
| char_ar_s0 | train | r=4 | 20 | 0.85 | 1.2 |
| char_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.5 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 33.4 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 21.6 |
| char_ar_s0 | fresh | r=16 | 20 | 0.65 | 2.1 |
| char_ar_s1 | train | r=1 | 20 | 0.15 | 24.9 |
| char_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| char_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 33.5 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 18.9 |
| char_ar_s1 | fresh | r=16 | 20 | 0.60 | 1.8 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **char_ar_s0** (ar/fresh): bits/nt  r=16 0.648±0.175 | r=1 3.923±0.506 | non-member 4.995±0.798;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.79e-06
- **char_ar_s1** (ar/fresh): bits/nt  r=16 0.951±0.433 | r=1 5.262±0.733 | non-member 6.972±0.873;  rank-1 rate r=16 1.00, r=1 0.20, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.92e-08

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **char_ar_s0**: r=16 probe bits/nt 0.058, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s1**: r=16 probe bits/nt 0.013, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.