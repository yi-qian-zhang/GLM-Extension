# Gate 1 report

root: outputs/cap_regress   scores file: scores_final.json
runs: 6mer_ar_s0

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 29 | 5 | 0.15 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 6mer_ar_s0 | ar | 2.5259 | 5.7593 | 2.355 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 6mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 220 | 0.03 | 0.03 | 2.509 | +0.17 |
| r=1 | 20 | 1 | 0.85 | 0.95 | 2.003 | +4.31 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.695 | +14.99 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.157 | +19.56 |

### 6mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.06 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.003 | +21.18 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +20.98 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.30 | 20.1 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.157±0.024 | r=1 2.003±0.123 | non-member 2.509±0.132;  rank-1 rate r=16 1.00, r=1 0.85, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.08e-10

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.