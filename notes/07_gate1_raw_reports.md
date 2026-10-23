# Gate 1 raw reports (generated on server 2026-09-25)

Source: outputs/pilot/gate1_report_final.md and outputs/pilot_v2/gate1_report_final.md on TJU_6004.

################ V1 RESCORED ON FINAL.PT ################
# Gate 1 report

root: outputs/pilot   scores file: scores_final.json
runs: ar_s0, ar_s1, mlm0.15_s0, mlm0.15_s1

## Training and throughput

| run | params | best val (bits/pred) | epoch | train s | score s | MFU (last epoch) |
|---|---|---|---|---|---|---|
| ar_s0 | 12.76M | 2.0009 | 3 | 43 | 46 | 0.34 |
| ar_s1 | 12.76M | 2.0004 | 2 | 43 | 46 | 0.35 |
| mlm0.15_s0 | 12.76M | 2.0000 | 13 | 47 | 1541 | 0.32 |
| mlm0.15_s1 | 12.76M | 1.9999 | 13 | 46 | 1529 | 0.33 |

## Held-out entropy floor (uniform DNA; must be >= 1.999 bits/nt)

| run | scorer | bits/nt | perplexity | min window | ok |
|---|---|---|---|---|---|
| ar_s0 | ar | 2.0220 | 4.0615 | 1.981 | OK |
| ar_s1 | ar | 2.0214 | 4.0596 | 1.975 | OK |
| mlm0.15_s0 | pll | 2.0004 | 4.0012 | 1.995 | OK |
| mlm0.15_s0 | prefix | 2.0005 | 4.0013 | 1.995 | OK |
| mlm0.15_s1 | pll | 2.0005 | 4.0014 | 1.995 | OK |
| mlm0.15_s1 | prefix | 2.0005 | 4.0013 | 1.996 | OK |

## Ranking against the random pool, by tier (host = training window for members, fresh for all)

### ar_s0 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 252 | 0.00 | 0.00 | 2.036 | -0.32 |
| r=1 | 20 | 129 | 0.00 | 0.00 | 2.007 | +0.55 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.697 | +39.99 |

### ar_s0 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 48 | 0.10 | 0.15 | 1.987 | +1.12 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.586 | +35.76 |

### ar_s1 — scorer `ar/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 290 | 0.00 | 0.00 | 2.023 | +0.05 |
| r=1 | 20 | 136 | 0.00 | 0.00 | 2.009 | +0.22 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.777 | +14.14 |

### ar_s1 — scorer `ar/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 77 | 0.05 | 0.15 | 1.989 | +0.43 |
| r=16 | 20 | 1 | 1.00 | 1.00 | 0.664 | +13.42 |

### mlm0.15_s0 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 221 | 0.03 | 0.05 | 2.001 | +0.12 |
| r=1 | 20 | 270 | 0.00 | 0.00 | 2.002 | -0.14 |
| r=16 | 20 | 2 | 0.30 | 0.65 | 1.991 | +2.59 |

### mlm0.15_s0 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 272 | 0.00 | 0.00 | 2.001 | -0.08 |
| r=16 | 20 | 3 | 0.40 | 0.65 | 1.991 | +2.62 |

### mlm0.15_s0 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 218 | 0.00 | 0.03 | 2.000 | +0.19 |
| r=1 | 20 | 277 | 0.00 | 0.00 | 2.002 | -0.19 |
| r=16 | 20 | 6 | 0.15 | 0.50 | 1.991 | +2.50 |

### mlm0.15_s0 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 280 | 0.00 | 0.00 | 2.002 | -0.20 |
| r=16 | 20 | 5 | 0.15 | 0.55 | 1.991 | +2.53 |

### mlm0.15_s1 — scorer `pll/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 263 | 0.00 | 0.00 | 2.001 | -0.08 |
| r=1 | 20 | 270 | 0.00 | 0.00 | 2.001 | -0.14 |
| r=16 | 20 | 2 | 0.10 | 0.60 | 1.990 | +2.64 |

### mlm0.15_s1 — scorer `pll/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 286 | 0.00 | 0.00 | 2.001 | -0.13 |
| r=16 | 20 | 3 | 0.15 | 0.55 | 1.990 | +2.59 |

### mlm0.15_s1 — scorer `prefix/fresh`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=0 | 40 | 274 | 0.00 | 0.00 | 2.001 | -0.11 |
| r=1 | 20 | 272 | 0.00 | 0.00 | 2.001 | -0.07 |
| r=16 | 20 | 4 | 0.10 | 0.55 | 1.990 | +2.57 |

### mlm0.15_s1 — scorer `prefix/train`  (pool n=500, chance rank-1 = 0.0020)

| tier | n | median rank | rank-1 rate | p<=0.01 rate | bits/nt | mean z |
|---|---|---|---|---|---|---|
| r=1 | 20 | 285 | 0.00 | 0.00 | 2.001 | -0.06 |
| r=16 | 20 | 4 | 0.15 | 0.50 | 1.991 | +2.52 |

## Exact-match extraction from a 48-nt prefix (Carlini-2023 definition)

| run | host | tier | n | exact rate | mean hamming (of 48) |
|---|---|---|---|---|---|
| ar_s0 | train | r=1 | 20 | 0.00 | 35.5 |
| ar_s0 | train | r=16 | 20 | 0.65 | 2.0 |
| ar_s0 | fresh | r=0 | 40 | 0.00 | 35.8 |
| ar_s0 | fresh | r=1 | 20 | 0.00 | 35.1 |
| ar_s0 | fresh | r=16 | 20 | 0.25 | 5.1 |
| ar_s1 | train | r=1 | 20 | 0.00 | 34.4 |
| ar_s1 | train | r=16 | 20 | 0.70 | 1.8 |
| ar_s1 | fresh | r=0 | 40 | 0.00 | 36.4 |
| ar_s1 | fresh | r=1 | 20 | 0.00 | 36.1 |
| ar_s1 | fresh | r=16 | 20 | 0.15 | 3.5 |
| mlm0.15_s0 | train | r=1 | 20 | 0.00 | 37.0 |
| mlm0.15_s0 | train | r=16 | 20 | 0.00 | 31.2 |
| mlm0.15_s0 | fresh | r=0 | 40 | 0.00 | 36.0 |
| mlm0.15_s0 | fresh | r=1 | 20 | 0.00 | 36.9 |
| mlm0.15_s0 | fresh | r=16 | 20 | 0.00 | 31.6 |
| mlm0.15_s1 | train | r=1 | 20 | 0.00 | 36.7 |
| mlm0.15_s1 | train | r=16 | 20 | 0.00 | 31.1 |
| mlm0.15_s1 | fresh | r=0 | 40 | 0.00 | 35.8 |
| mlm0.15_s1 | fresh | r=1 | 20 | 0.00 | 36.6 |
| mlm0.15_s1 | fresh | r=16 | 20 | 0.00 | 30.7 |

## Q1 — scorer consistency on the MLM model (pll vs prefix)

- **mlm0.15_s0 / fresh**: n=80, Spearman(bits) = 0.957, Spearman(rank) = 0.957, rank-1 set Jaccard = 0.43 (7 vs 3 rank-1)
- **mlm0.15_s0 / train**: n=40, Spearman(bits) = 0.965, Spearman(rank) = 0.957, rank-1 set Jaccard = 0.38 (8 vs 3 rank-1)
- **mlm0.15_s1 / fresh**: n=80, Spearman(bits) = 0.989, Spearman(rank) = 0.988, rank-1 set Jaccard = 1.00 (2 vs 2 rank-1)
- **mlm0.15_s1 / train**: n=40, Spearman(bits) = 0.991, Spearman(rank) = 0.987, rank-1 set Jaccard = 0.50 (3 vs 3 rank-1)

## Q2 — dynamic range (r=16 vs r=1 vs non-member), natural scorer, fresh host

- **ar_s0** (ar/fresh): bits/nt  r=16 0.697±0.105 | r=1 2.007±0.018 | non-member 2.036±0.080;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 7.06e-03
- **ar_s1** (ar/fresh): bits/nt  r=16 0.777±0.176 | r=1 2.009±0.029 | non-member 2.023±0.026;  rank-1 rate r=16 1.00, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 1.87e-10, p(r=1 < non-member) = 1.17e-02
- **mlm0.15_s0** (prefix/fresh): bits/nt  r=16 1.991±0.004 | r=1 2.002±0.003 | non-member 2.000±0.004;  rank-1 rate r=16 0.15, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 7.19e-09, p(r=1 < non-member) = 9.39e-01
- **mlm0.15_s1** (prefix/fresh): bits/nt  r=16 1.990±0.004 | r=1 2.001±0.004 | non-member 2.001±0.003;  rank-1 rate r=16 0.10, r=1 0.00, non-member 0.00;  MWU p(r=16 < non-member) = 4.58e-10, p(r=1 < non-member) = 4.91e-01

## Q3 — objective signal under matched conditioning (ar/train on AR runs vs prefix/train on MLM runs)

- ar  **ar_s0**: r=16 probe bits/nt 0.586, rank-1 rate 1.00, exact-extraction rate 0.65
- ar  **ar_s1**: r=16 probe bits/nt 0.664, rank-1 rate 1.00, exact-extraction rate 0.70
- mlm **mlm0.15_s0**: r=16 probe bits/nt 1.991, rank-1 rate 0.15, exact-extraction rate 0.00
- mlm **mlm0.15_s1**: r=16 probe bits/nt 1.991, rank-1 rate 0.15, exact-extraction rate 0.00
- **Δ(MLM − AR) r=16 bits/nt = +1.366**  (seed spread: AR ±0.039, MLM ±0.000)

> Note on Q1 as originally planned: applying PLL to a *causal* model is a null check — the causal mask already hides every position to the right, so masking the target changes nothing and PLL reduces exactly to AR scoring. The consistency check is therefore run on the MLM model between its two scorers.

################ V2 (50 epochs, final, tiers 1/16/64) ################
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

[exited with code 0]
