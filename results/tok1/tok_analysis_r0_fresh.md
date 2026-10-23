# Tokenizer x objective — outputs/tok1

tier r=0, host=fresh; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | ar | 2 | ar | 2.023±0.005 | 0.00 | 0.00 | 2.0391 | 12.76M | 47M |
| char | mlm0.15 | 2 | pll | 2.001±0.000 | 0.01 | 0.00 | 2.0005 | 12.76M | 7M |
| char | mlm0.15 | 2 | prefix | 2.001±0.000 | 0.00 | 0.00 | 2.0004 | 12.76M | 7M |
| char | mlm0.50 | 1 | pll | 2.003±0.000 | 0.00 | 0.00 | 2.0050 | 12.76M | 23M |
| char | mlm0.50 | 1 | prefix | 2.002±0.000 | 0.00 | 0.00 | 2.0027 | 12.76M | 23M |
| 3mer | ar | 2 | ar | 4.204±0.032 | 0.00 | 0.00 | 4.0918 | 12.69M | 16M |
| 3mer | mlm0.15 | 2 | pll | 2.004±0.002 | 0.00 | 0.00 | 2.0037 | 12.69M | 2M |
| 3mer | mlm0.15 | 2 | prefix | 2.006±0.003 | 0.00 | 0.00 | 2.0044 | 12.69M | 2M |
| 3mer | mlm0.50 | 2 | pll | 2.004±0.001 | 0.00 | 0.00 | 2.0045 | 12.69M | 8M |
| 3mer | mlm0.50 | 2 | prefix | 2.004±0.000 | 0.00 | 0.00 | 2.0053 | 12.69M | 8M |
| 6mer | ar | 2 | ar | 2.507±0.001 | 0.01 | 0.00 | 2.5221 | 14.73M | 8M |
| 6mer | mlm0.15 | 2 | pll | 2.035±0.004 | 0.00 | 0.00 | 2.0354 | 14.73M | 1M |
| 6mer | mlm0.15 | 2 | prefix | 2.023±0.006 | 0.00 | 0.00 | 2.0268 | 14.73M | 1M |
| 6mer | mlm0.50 | 2 | pll | 2.051±0.000 | 0.00 | 0.00 | 2.0555 | 14.73M | 4M |
| 6mer | mlm0.50 | 2 | prefix | 2.051±0.001 | 0.00 | 0.00 | 2.0530 | 14.73M | 4M |

## Variance decomposition of r=0 probe bits/nt (natural scorer; n=17 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 1.6105 | **19.3%** |
| objective | 3.1035 | **37.2%** |
| tokenizer x objective | 3.6359 | **43.5%** |
| seed (residual) | 0.0022 | **0.0%** |
| total | 8.3522 | 100% |

> Grid is unbalanced (a cell is missing or has fewer seeds); shares are approximate.

Within masked models only: tokenizer explains **92.8%** of the variance (n=11).
Within causal models only: tokenizer explains **100.0%** of the variance (n=6).