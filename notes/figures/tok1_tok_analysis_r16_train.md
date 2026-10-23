# Tokenizer x objective — outputs/tok1

tier r=16, host=train; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | ar | 2 | ar | 0.432±0.002 | 1.00 | 0.95 | 2.0391 | 12.76M | 47M |
| char | mlm0.15 | 2 | pll | 1.990±0.000 | 0.35 | 0.00 | 2.0005 | 12.76M | 7M |
| char | mlm0.15 | 2 | prefix | 1.991±0.000 | 0.32 | 0.00 | 2.0004 | 12.76M | 7M |
| char | mlm0.50 | 2 | pll | 1.934±0.009 | 0.90 | 0.00 | 2.0043 | 12.76M | 23M |
| char | mlm0.50 | 2 | prefix | 1.946±0.006 | 0.97 | 0.00 | 2.0030 | 12.76M | 23M |
| 3mer | ar | 2 | ar | 0.001±0.000 | 1.00 | 1.00 | 4.0918 | 12.69M | 16M |
| 3mer | mlm0.15 | 2 | pll | 0.450±0.067 | 1.00 | 0.15 | 2.0037 | 12.69M | 2M |
| 3mer | mlm0.15 | 2 | prefix | 1.149±0.174 | 0.97 | 0.15 | 2.0044 | 12.69M | 2M |
| 3mer | mlm0.50 | 2 | pll | 0.156±0.048 | 1.00 | 0.75 | 2.0045 | 12.69M | 8M |
| 3mer | mlm0.50 | 2 | prefix | 0.572±0.012 | 1.00 | 0.75 | 2.0053 | 12.69M | 8M |
| 6mer | ar | 2 | ar | 0.001±0.000 | 1.00 | 1.00 | 2.5221 | 14.73M | 8M |
| 6mer | mlm0.15 | 2 | pll | 0.721±0.169 | 1.00 | 0.12 | 2.0354 | 14.73M | 1M |
| 6mer | mlm0.15 | 2 | prefix | 1.075±0.200 | 1.00 | 0.12 | 2.0268 | 14.73M | 1M |
| 6mer | mlm0.50 | 2 | pll | 0.105±0.044 | 1.00 | 1.00 | 2.0555 | 14.73M | 4M |
| 6mer | mlm0.50 | 2 | prefix | 0.219±0.040 | 1.00 | 1.00 | 2.0530 | 14.73M | 4M |

## Variance decomposition of r=16 probe bits/nt (natural scorer; n=18 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 5.9022 | **59.5%** |
| objective | 2.5511 | **25.7%** |
| tokenizer x objective | 1.3888 | **14.0%** |
| seed (residual) | 0.0749 | **0.8%** |
| total | 9.9170 | 100% |

Within masked models only: tokenizer explains **92.7%** of the variance (n=12).
Within causal models only: tokenizer explains **100.0%** of the variance (n=6).