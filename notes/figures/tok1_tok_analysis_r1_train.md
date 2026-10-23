# Tokenizer x objective — outputs/tok1

tier r=1, host=train; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | ar | 2 | ar | 1.970±0.006 | 0.15 | 0.00 | 2.0391 | 12.76M | 47M |
| char | mlm0.15 | 2 | pll | 2.000±0.000 | 0.00 | 0.00 | 2.0005 | 12.76M | 7M |
| char | mlm0.15 | 2 | prefix | 2.000±0.000 | 0.00 | 0.00 | 2.0004 | 12.76M | 7M |
| char | mlm0.50 | 1 | pll | 1.997±0.000 | 0.00 | 0.00 | 2.0050 | 12.76M | 23M |
| char | mlm0.50 | 1 | prefix | 1.998±0.000 | 0.05 | 0.00 | 2.0027 | 12.76M | 23M |
| 3mer | ar | 2 | ar | 0.004±0.001 | 1.00 | 1.00 | 4.0918 | 12.69M | 16M |
| 3mer | mlm0.15 | 2 | pll | 1.996±0.002 | 0.00 | 0.00 | 2.0037 | 12.69M | 2M |
| 3mer | mlm0.15 | 2 | prefix | 2.000±0.001 | 0.00 | 0.00 | 2.0044 | 12.69M | 2M |
| 3mer | mlm0.50 | 2 | pll | 1.993±0.002 | 0.03 | 0.00 | 2.0045 | 12.69M | 8M |
| 3mer | mlm0.50 | 2 | prefix | 2.001±0.005 | 0.00 | 0.00 | 2.0053 | 12.69M | 8M |
| 6mer | ar | 2 | ar | 0.005±0.000 | 1.00 | 1.00 | 2.5221 | 14.73M | 8M |
| 6mer | mlm0.15 | 2 | pll | 1.949±0.012 | 0.22 | 0.00 | 2.0354 | 14.73M | 1M |
| 6mer | mlm0.15 | 2 | prefix | 1.975±0.004 | 0.08 | 0.00 | 2.0268 | 14.73M | 1M |
| 6mer | mlm0.50 | 2 | pll | 1.854±0.025 | 0.95 | 0.00 | 2.0555 | 14.73M | 4M |
| 6mer | mlm0.50 | 2 | prefix | 1.886±0.016 | 0.88 | 0.00 | 2.0530 | 14.73M | 4M |

## Variance decomposition of r=1 probe bits/nt (natural scorer; n=17 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 1.6785 | **14.3%** |
| objective | 6.5896 | **56.0%** |
| tokenizer x objective | 3.4972 | **29.7%** |
| seed (residual) | 0.0016 | **0.0%** |
| total | 11.7670 | 100% |

> Grid is unbalanced (a cell is missing or has fewer seeds); shares are approximate.

Within masked models only: tokenizer explains **68.4%** of the variance (n=11).
Within causal models only: tokenizer explains **100.0%** of the variance (n=6).