# Gate 1 report

root: outputs/pilot_v2   scores file: scores_final.json
runs: ar_s0, ar_s1, mlm0.15_s0, mlm0.15_s1

## Training and throughput

| run | params | best val (bits/pred) | epoch | train s | score s | MFU (last epoch) |
|---|---|---|---|---|---|---|
| ar_s0 | 12.76M | 2.0020 | 9 | 147 | 58 | 0.34 |
| ar_s1 | 12.76M | 2.0029 | 12 | 146 | 56 | 0.35 |
| mlm0.15_s0 | 12.76M | 2.0002 | 22 | 144 | 2024 | 0.32 |
| mlm0.15_s1 | 12.76M | 2.0000 | 32 | 142 | 2025 | 0.32 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| ar_s0 | ar | 3.1425 | 8.8305 | 2.218 | OK |
| ar_s1 | ar | 2.8906 | 7.4158 | 2.159 | OK |
| mlm0.15_s0 | pll | 2.0008 | 4.0023 | 1.992 | OK |
| mlm0.15_s0 | prefix | 2.0366 | 4.1028 | 1.983 | OK |
| mlm0.15_s1 | pll | 2.0006 | 4.0017 | 1.991 | OK |
| mlm0.15_s1 | prefix | 2.0543 | 4.1535 | 1.984 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 268 | 0.00 | 0.00 | 4.625 | +0.05 |
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.488 | +3.35 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.114 | +4.75 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.078 | +4.80 |

### ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.736 | +4.08 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.081 | +4.76 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.064 | +4.84 |

### ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 251 | 0.00 | 0.00 | 4.399 | +0.05 |
| r=1 | 20 | 1 | 1.00 | 1.00 | 1.329 | +3.42 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.097 | +4.77 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.074 | +4.81 |

### ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 1 | 1.00 | 1.00 | 0.900 | +3.88 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.084 | +4.75 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.064 | +4.82 |

### mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 204 | 0.00 | 0.00 | 2.000 | +0.28 |
| r=1 | 20 | 161 | 0.00 | 0.10 | 1.999 | +0.47 |
| r=16 | 20 | 16 | 0.35 | 0.40 | 1.990 | +2.08 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.099 | +342.07 |

### mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 157 | 0.00 | 0.10 | 1.999 | +0.49 |
| r=16 | 20 | 14 | 0.30 | 0.40 | 1.990 | +2.09 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.099 | +341.99 |

### mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 325 | 0.00 | 0.00 | 2.100 | -0.30 |
| r=1 | 20 | 229 | 0.00 | 0.00 | 2.048 | +0.21 |
| r=16 | 20 | 331 | 0.00 | 0.05 | 2.100 | -0.31 |
| r=64 | 20 | 1 | 0.95 | 0.95 | 1.054 | +10.33 |

### mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 194 | 0.00 | 0.00 | 2.047 | +0.21 |
| r=16 | 20 | 331 | 0.00 | 0.00 | 2.097 | -0.32 |
| r=64 | 20 | 1 | 0.95 | 0.95 | 1.061 | +10.06 |

### mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 179 | 0.00 | 0.00 | 1.999 | +0.35 |
| r=1 | 20 | 304 | 0.00 | 0.00 | 2.001 | -0.04 |
| r=16 | 20 | 12 | 0.45 | 0.45 | 1.985 | +2.42 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.134 | +284.46 |

### mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 294 | 0.00 | 0.00 | 2.001 | -0.01 |
| r=16 | 20 | 14 | 0.45 | 0.45 | 1.985 | +2.39 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 0.133 | +284.80 |

### mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 236 | 0.00 | 0.00 | 2.138 | +0.15 |
| r=1 | 20 | 159 | 0.00 | 0.00 | 2.131 | +0.17 |
| r=16 | 20 | 290 | 0.00 | 0.00 | 2.252 | -0.31 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 1.236 | +3.72 |

### mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 156 | 0.00 | 0.00 | 2.132 | +0.19 |
| r=16 | 20 | 288 | 0.00 | 0.00 | 2.239 | -0.25 |
| r=64 | 20 | 1 | 1.00 | 1.00 | 1.225 | +3.75 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (of 48) |
|---|---|---|---|---|---|
| ar_s0 | train | r=1 | 20 | 0.05 | 25.8 |
| ar_s0 | train | r=16 | 20 | 1.00 | 0.0 |
| ar_s0 | train | r=64 | 20 | 1.00 | 0.0 |
| ar_s0 | fresh | r=0 | 40 | 0.00 | 35.4 |
| ar_s0 | fresh | r=1 | 20 | 0.00 | 30.1 |
| ar_s0 | fresh | r=16 | 20 | 0.95 | 0.1 |
| ar_s0 | fresh | r=64 | 20 | 1.00 | 0.0 |
| ar_s1 | train | r=1 | 20 | 0.05 | 27.6 |
| ar_s1 | train | r=16 | 20 | 1.00 | 0.0 |
| ar_s1 | train | r=64 | 20 | 1.00 | 0.0 |
| ar_s1 | fresh | r=0 | 40 | 0.00 | 35.5 |
| ar_s1 | fresh | r=1 | 20 | 0.00 | 28.8 |
| ar_s1 | fresh | r=16 | 20 | 1.00 | 0.0 |
| ar_s1 | fresh | r=64 | 20 | 1.00 | 0.0 |
| mlm0.15_s0 | train | r=1 | 20 | 0.00 | 34.8 |
| mlm0.15_s0 | train | r=16 | 20 | 0.00 | 34.1 |
| mlm0.15_s0 | train | r=64 | 20 | 0.20 | 3.5 |
| mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 35.0 |
| mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 34.6 |
| mlm0.15_s0 | fresh | r=16 | 20 | 0.00 | 34.1 |
| mlm0.15_s0 | fresh | r=64 | 20 | 0.15 | 3.4 |
| mlm0.15_s1 | train | r=1 | 20 | 0.00 | 35.5 |
| mlm0.15_s1 | train | r=16 | 20 | 0.00 | 32.9 |
| mlm0.15_s1 | train | r=64 | 20 | 0.15 | 5.9 |
| mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 35.7 |
| mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 35.5 |
| mlm0.15_s1 | fresh | r=16 | 20 | 0.00 | 32.8 |
| mlm0.15_s1 | fresh | r=64 | 20 | 0.15 | 5.8 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **mlm0.15_s0 / fresh**: n=100, Spearman(bits) = 0.437, Spearman(rank) = 0.397, rank-1 set Jaccard = 0.70 (27 vs 19 rank-1)
- **mlm0.15_s0 / train**: n=60, Spearman(bits) = 0.555, Spearman(rank) = 0.448, rank-1 set Jaccard = 0.73 (26 vs 19 rank-1)
- **mlm0.15_s1 / fresh**: n=100, Spearman(bits) = 0.476, Spearman(rank) = 0.423, rank-1 set Jaccard = 0.69 (29 vs 20 rank-1)
- **mlm0.15_s1 / train**: n=60, Spearman(bits) = 0.687, Spearman(rank) = 0.586, rank-1 set Jaccard = 0.69 (29 vs 20 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **ar_s0** (ar/fresh): bits/nt  r=16 0.114±0.025 | r=1 1.488±0.344 | non-member 4.625±1.183;  rank-1 rate r=16 1.00, r=1 1.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **ar_s1** (ar/fresh): bits/nt  r=16 0.097±0.018 | r=1 1.329±0.222 | non-member 4.399±0.871;  rank-1 rate r=16 1.00, r=1 1.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.87e-10
- **mlm0.15_s0** (prefix/fresh): bits/nt  r=16 2.100±0.123 | r=1 2.048±0.083 | non-member 2.100±0.122;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.97e-01, p(r=1 < non-member) = 4.59e-02
- **mlm0.15_s1** (prefix/fresh): bits/nt  r=16 2.252±0.321 | r=1 2.131±0.168 | non-member 2.138±0.195;  rank-1 rate r=16 0.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 8.48e-01, p(r=1 < non-member) = 2.43e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **ar_s0**: r=16 probe bits/nt 0.081, rank-1 rate 1.00, exact-extraction rate 1.00
- ar  **ar_s1**: r=16 probe bits/nt 0.084, rank-1 rate 1.00, exact-extraction rate 1.00
- mlm **mlm0.15_s0**: r=16 probe bits/nt 2.097, rank-1 rate 0.00, exact-extraction rate 0.00
- mlm **mlm0.15_s1**: r=16 probe bits/nt 2.239, rank-1 rate 0.00, exact-extraction rate 0.00
- **Δ(MLM − AR) r=16 bits/nt = +2.086**  (seed spread: AR ±0.001, MLM ±0.071)

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.