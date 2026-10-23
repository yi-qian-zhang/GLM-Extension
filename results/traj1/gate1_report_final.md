# Gate 1 report

root: outputs/traj1   scores file: scores_final.json
runs: 3mer_ar_s0, 3mer_ar_s1, 6mer_ar_s0, 6mer_ar_s1, char_ar_s0, char_ar_s1

## Training and throughput

| run | tok | params (non-emb) | steps | supervised tok | train s | score s | MFU |
|---|---|---|---|---|---|---|---|
| 3mer_ar_s0 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 32 | 9 | 0.24 |
| 3mer_ar_s1 | 3mer | 12.69M (12.61M) | 2550 | 15.6M | 32 | 9 | 0.24 |
| 6mer_ar_s0 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 31 | 5 | 0.14 |
| 6mer_ar_s1 | 6mer | 14.73M (12.61M) | 2550 | 7.8M | 30 | 5 | 0.15 |
| char_ar_s0 | char | 12.76M (12.61M) | 2550 | 46.8M | 66 | 24 | 0.34 |
| char_ar_s1 | char | 12.76M (12.61M) | 2550 | 46.8M | 65 | 24 | 0.35 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| 3mer_ar_s0 | ar | 4.0614 | 16.6951 | 3.565 | OK |
| 3mer_ar_s1 | ar | 4.1222 | 17.4145 | 3.664 | OK |
| 6mer_ar_s0 | ar | 2.5259 | 5.7593 | 2.355 | OK |
| 6mer_ar_s1 | ar | 2.5183 | 5.7291 | 2.327 | OK |
| char_ar_s0 | ar | 2.0423 | 4.1191 | 1.987 | OK |
| char_ar_s1 | ar | 2.0425 | 4.1196 | 1.989 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### 3mer_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 321 | 0.00 | 0.03 | 4.236 | -0.21 |
| r=1 | 20 | 14 | 0.15 | 0.35 | 3.726 | +1.89 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 2.280 | +8.06 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.515 | +15.27 |

### 3mer_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.004 | +17.71 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.03 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +17.66 |

### 3mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 186 | 0.00 | 0.03 | 4.171 | +0.35 |
| r=1 | 20 | 52 | 0.10 | 0.20 | 3.882 | +1.54 |
| r=4 | 20 | 1 | 0.95 | 1.00 | 2.443 | +7.52 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.488 | +15.54 |

### 3mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.003 | +18.07 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.002 | +18.07 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +18.01 |

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

### 6mer_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 214 | 0.00 | 0.00 | 2.506 | +0.15 |
| r=1 | 20 | 1 | 0.90 | 0.95 | 1.991 | +4.43 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.711 | +15.07 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.138 | +19.88 |

### 6mer_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.005 | +21.20 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 0.003 | +21.18 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.001 | +21.44 |

### char_ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 188 | 0.00 | 0.00 | 2.029 | +0.16 |
| r=1 | 20 | 66 | 0.00 | 0.00 | 2.004 | +0.60 |
| r=4 | 20 | 1 | 0.80 | 0.90 | 1.915 | +1.68 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.534 | +17.02 |

### char_ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 31 | 0.15 | 0.30 | 1.975 | +0.73 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.830 | +2.73 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.417 | +19.10 |

### char_ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 180 | 0.00 | 0.00 | 2.043 | -0.05 |
| r=1 | 20 | 70 | 0.05 | 0.05 | 2.005 | +0.68 |
| r=4 | 20 | 1 | 0.80 | 0.95 | 1.893 | +2.64 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.505 | +21.60 |

### char_ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 16 | 0.20 | 0.20 | 1.964 | +1.29 |
| r=4 | 20 | 1 | 1.00 | 1.00 | 1.839 | +3.15 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.398 | +23.17 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (nt) |
|---|---|---|---|---|---|
| 3mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| 3mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 36.1 |
| 3mer_ar_s0 | fresh | r=4 | 20 | 0.00 | 33.0 |
| 3mer_ar_s0 | fresh | r=16 | 20 | 0.30 | 11.4 |
| 3mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 3mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 36.2 |
| 3mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 34.9 |
| 3mer_ar_s1 | fresh | r=4 | 20 | 0.00 | 35.5 |
| 3mer_ar_s1 | fresh | r=16 | 20 | 0.40 | 8.8 |
| 6mer_ar_s0 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| 6mer_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.2 |
| 6mer_ar_s0 | fresh | r=4 | 20 | 0.30 | 20.1 |
| 6mer_ar_s0 | fresh | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=1 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=4 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| 6mer_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.5 |
| 6mer_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.1 |
| 6mer_ar_s1 | fresh | r=4 | 20 | 0.30 | 19.2 |
| 6mer_ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | train | r=1 | 20 | 0.00 | 34.4 |
| char_ar_s0 | train | r=4 | 20 | 0.00 | 31.8 |
| char_ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| char_ar_s0 | fresh | r=0 | 40 | 0.00 | 36.3 |
| char_ar_s0 | fresh | r=1 | 20 | 0.00 | 35.3 |
| char_ar_s0 | fresh | r=4 | 20 | 0.00 | 32.5 |
| char_ar_s0 | fresh | r=16 | 20 | 0.50 | 2.2 |
| char_ar_s1 | train | r=1 | 20 | 0.00 | 33.7 |
| char_ar_s1 | train | r=4 | 20 | 0.00 | 31.8 |
| char_ar_s1 | train | r=16 | 20 | 0.90 | 0.1 |
| char_ar_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| char_ar_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| char_ar_s1 | fresh | r=4 | 20 | 0.00 | 31.4 |
| char_ar_s1 | fresh | r=16 | 20 | 0.50 | 1.8 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)


## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **3mer_ar_s0** (ar/fresh): bits/nt  r=16 0.515±0.164 | r=1 3.726±0.310 | non-member 4.236±0.274;  rank-1 rate r=16 1.00, r=1 0.15, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.13e-06
- **3mer_ar_s1** (ar/fresh): bits/nt  r=16 0.488±0.216 | r=1 3.882±0.291 | non-member 4.171±0.245;  rank-1 rate r=16 1.00, r=1 0.10, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.43e-04
- **6mer_ar_s0** (ar/fresh): bits/nt  r=16 0.157±0.024 | r=1 2.003±0.123 | non-member 2.509±0.132;  rank-1 rate r=16 1.00, r=1 0.85, non-member 0.03;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 3.08e-10
- **6mer_ar_s1** (ar/fresh): bits/nt  r=16 0.138±0.034 | r=1 1.991±0.114 | non-member 2.506±0.109;  rank-1 rate r=16 1.00, r=1 0.90, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **char_ar_s0** (ar/fresh): bits/nt  r=16 0.534±0.104 | r=1 2.004±0.022 | non-member 2.029±0.035;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 4.31e-03
- **char_ar_s1** (ar/fresh): bits/nt  r=16 0.505±0.099 | r=1 2.005±0.043 | non-member 2.043±0.137;  rank-1 rate r=16 1.00, r=1 0.05, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 5.75e-02

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **3mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **3mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s0**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **6mer_ar_s1**: r=16 probe bits/nt 0.001, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s0**: r=16 probe bits/nt 0.417, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **char_ar_s1**: r=16 probe bits/nt 0.398, rank-1 rate 1.00, exact-extraction rate 0.90

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.