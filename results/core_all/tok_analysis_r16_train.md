# Tokenizer x objective — outputs/core_all

tier r=16, host=train; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | ar | 2 | ar | 1.951±0.006 | 0.30 | 0.00 | 2.0400 | 12.76M | 61M |
| char | mlm0.15 | 2 | pll | 1.999±0.000 | 0.00 | 0.00 | 2.0003 | 12.76M | 8M |
| char | mlm0.15 | 2 | prefix | 1.999±0.000 | 0.00 | 0.00 | 2.0003 | 12.76M | 8M |
| char | mlm0.5 | 2 | pll | 1.997±0.001 | 0.04 | 0.00 | 2.0014 | 12.76M | 25M |
| char | mlm0.5 | 2 | prefix | 1.998±0.000 | 0.03 | 0.00 | 2.0014 | 12.76M | 25M |
| 3mer | ar | 2 | ar | 0.019±0.004 | 1.00 | 1.00 | 4.1497 | 12.69M | 20M |
| 3mer | mlm0.15 | 2 | pll | 1.994±0.001 | 0.03 | 0.00 | 2.0062 | 12.69M | 3M |
| 3mer | mlm0.15 | 2 | prefix | 1.997±0.000 | 0.03 | 0.00 | 2.0040 | 12.69M | 3M |
| 3mer | mlm0.5 | 2 | pll | 1.983±0.003 | 0.12 | 0.00 | 2.0148 | 12.69M | 8M |
| 3mer | mlm0.5 | 2 | prefix | 1.990±0.002 | 0.05 | 0.00 | 2.0098 | 12.69M | 8M |
| 6mer | ar | 2 | ar | 0.013±0.000 | 1.00 | 1.00 | 2.6318 | 14.73M | 10M |
| 6mer | mlm0.15 | 2 | pll | 1.926±0.005 | 0.57 | 0.00 | 2.0322 | 14.73M | 1M |
| 6mer | mlm0.15 | 2 | prefix | 1.964±0.000 | 0.31 | 0.00 | 2.0256 | 14.73M | 1M |
| 6mer | mlm0.5 | 2 | pll | 1.915±0.001 | 0.72 | 0.00 | 2.0443 | 14.73M | 4M |
| 6mer | mlm0.5 | 2 | prefix | 1.922±0.001 | 0.62 | 0.00 | 2.0426 | 14.73M | 4M |

## Variance decomposition of r=16 probe bits/nt (natural scorer; n=24 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 2.0536 | **12.0%** |
| objective | 11.5101 | **67.1%** |
| tokenizer x objective | 3.5990 | **21.0%** |
| seed (residual) | 0.0003 | **0.0%** |
| total | 17.1629 | 100% |

Within masked models only: tokenizer explains **84.4%** of the variance (n=16).
Within causal models only: tokenizer explains **100.0%** of the variance (n=8).