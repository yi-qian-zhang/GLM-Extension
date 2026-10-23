# Tokenizer x objective — outputs/ecoli_mlm

tier r=16, host=train; mean over seeds (n per cell shown). bits/nt: chance = 2.000

| tokenizer | objective | n | scorer | probe bits/nt | rank-1 | exact 48-nt | floor | params | supervised tok |
|---|---|---|---|---|---|---|---|---|---|
| char | mlm0.15 | 1 | pll | 2.024±0.000 | 0.00 | 0.00 | 1.9607 | 12.76M | 8M |
| char | mlm0.15 | 1 | prefix | 2.070±0.000 | 0.00 | 0.00 | 2.7691 | 12.76M | 8M |
| char | mlm0.5 | 1 | pll | 2.035±0.000 | 0.05 | 0.00 | 1.9092 | 12.76M | 25M |
| char | mlm0.5 | 1 | prefix | 2.043±0.000 | 0.05 | 0.00 | 1.9540 | 12.76M | 25M |
| 3mer | mlm0.15 | 1 | pll | 2.071±0.000 | 0.03 | 0.00 | 1.8605 | 12.69M | 3M |
| 3mer | mlm0.15 | 1 | prefix | 2.058±0.000 | 0.05 | 0.00 | 1.9170 | 12.69M | 3M |
| 3mer | mlm0.5 | 1 | pll | 2.067±0.000 | 0.05 | 0.00 | 1.8551 | 12.69M | 8M |
| 3mer | mlm0.5 | 1 | prefix | 2.053±0.000 | 0.05 | 0.00 | 1.9064 | 12.69M | 8M |
| 6mer | mlm0.15 | 1 | pll | 1.996±0.000 | 0.12 | 0.00 | 1.9476 | 14.73M | 1M |
| 6mer | mlm0.15 | 1 | prefix | 2.005±0.000 | 0.15 | 0.00 | 1.9631 | 14.73M | 1M |
| 6mer | mlm0.5 | 1 | pll | 1.974±0.000 | 0.28 | 0.00 | 1.9484 | 14.73M | 4M |
| 6mer | mlm0.5 | 1 | prefix | 1.972±0.000 | 0.23 | 0.00 | 1.9600 | 14.73M | 4M |

## Variance decomposition of r=16 probe bits/nt (natural scorer; n=6 runs)

| source | SS | share of total |
|---|---|---|
| tokenizer | 0.0071 | **95.8%** |
| objective | 0.0000 | **0.4%** |
| tokenizer x objective | 0.0003 | **3.8%** |
| seed (residual) | 0.0000 | **0.0%** |
| total | 0.0074 | 100% |

Within masked models only: tokenizer explains **95.8%** of the variance (n=6).