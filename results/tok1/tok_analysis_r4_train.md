# Tokenizer x objective — outputs/tok1

tier r=4, host=train; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | ar | 2 | ar | 1.837±0.012 | 0.97 | 0.00 | 2.0391 | 12.76M | 47M |
| char | mlm0.15 | 2 | pll | 1.998±0.000 | 0.08 | 0.00 | 2.0005 | 12.76M | 7M |
| char | mlm0.15 | 2 | prefix | 1.998±0.000 | 0.08 | 0.00 | 2.0004 | 12.76M | 7M |
| char | mlm0.50 | 1 | pll | 1.984±0.000 | 0.10 | 0.00 | 2.0050 | 12.76M | 23M |
| char | mlm0.50 | 1 | prefix | 1.991±0.000 | 0.00 | 0.00 | 2.0027 | 12.76M | 23M |
| 3mer | ar | 2 | ar | 0.002±0.000 | 1.00 | 1.00 | 4.0918 | 12.69M | 16M |
| 3mer | mlm0.15 | 2 | pll | 1.964±0.009 | 0.20 | 0.00 | 2.0037 | 12.69M | 2M |
| 3mer | mlm0.15 | 2 | prefix | 1.980±0.006 | 0.15 | 0.00 | 2.0044 | 12.69M | 2M |
| 3mer | mlm0.50 | 2 | pll | 1.963±0.002 | 0.57 | 0.00 | 2.0045 | 12.69M | 8M |
| 3mer | mlm0.50 | 2 | prefix | 1.980±0.004 | 0.22 | 0.00 | 2.0053 | 12.69M | 8M |
| 6mer | ar | 2 | ar | 0.003±0.000 | 1.00 | 1.00 | 2.5221 | 14.73M | 8M |
| 6mer | mlm0.15 | 2 | pll | 1.695±0.037 | 1.00 | 0.00 | 2.0354 | 14.73M | 1M |
| 6mer | mlm0.15 | 2 | prefix | 1.817±0.021 | 1.00 | 0.00 | 2.0268 | 14.73M | 1M |
| 6mer | mlm0.50 | 2 | pll | 1.025±0.010 | 1.00 | 0.00 | 2.0555 | 14.73M | 4M |
| 6mer | mlm0.50 | 2 | prefix | 1.105±0.051 | 1.00 | 0.00 | 2.0530 | 14.73M | 4M |

## Variance decomposition of r=4 probe bits/nt (natural scorer; n=17 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 2.8697 | **26.2%** |
| objective | 5.2632 | **48.1%** |
| tokenizer x objective | 2.7997 | **25.6%** |
| seed (residual) | 0.0035 | **0.0%** |
| total | 10.9361 | 100% |

> Grid is unbalanced (a cell is missing or has fewer seeds); shares are approximate.

Within masked models only: tokenizer explains **68.2%** of the variance (n=11).
Within causal models only: tokenizer explains **100.0%** of the variance (n=6).