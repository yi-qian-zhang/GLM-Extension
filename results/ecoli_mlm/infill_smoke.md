# Edge-conditioned extraction audit of the masked cells — infill_smoke

`prefix` is the protocol the paper reports: reveal 48\,nt and mask everything after it. `infill` reveals the same 48\,nt and leaves the host AFTER the canary visible, decoding the 48 masked nucleotides in confidence order -- the geometry that recovers up to 3x more from diffusion language models (Wang and Asokan, arXiv:2605.24173). Same checkpoints, same canaries, same hosts. `ham` is the mean number of wrong nucleotides out of 48.

| dataset | tokeniser | objective | seed | tier | n | prefix exact | prefix ham | infill exact | infill ham |
|---|---|---|---|---|---|---|---|---|---|
| ecoli | 3mer | mlm@0.15 | 0 | r=16 | 5 | 0% | 37.2 | **0%** | 36.2 |
| ecoli | 3mer | mlm@0.15 | 0 | r=1 | 5 | 0% | 35.2 | **0%** | 35.8 |
| ecoli | 3mer | mlm@0.15 | 0 | r=0 | 5 | 0% | 34.4 | **0%** | 35.6 |
| ecoli | 3mer | mlm@0.15 | 1 | r=16 | 5 | 0% | 35.6 | **0%** | 36.4 |
| ecoli | 3mer | mlm@0.15 | 1 | r=1 | 5 | 0% | 36.0 | **0%** | 36.2 |
| ecoli | 3mer | mlm@0.15 | 1 | r=0 | 5 | 0% | 36.0 | **0%** | 37.2 |
| ecoli | 3mer | mlm@0.5 | 0 | r=16 | 5 | 0% | 35.4 | **0%** | 36.8 |
| ecoli | 3mer | mlm@0.5 | 0 | r=1 | 5 | 0% | 34.8 | **0%** | 35.6 |
| ecoli | 3mer | mlm@0.5 | 0 | r=0 | 5 | 0% | 35.0 | **0%** | 36.0 |
| ecoli | 3mer | mlm@0.5 | 1 | r=16 | 5 | 0% | 34.2 | **0%** | 36.8 |
| ecoli | 3mer | mlm@0.5 | 1 | r=1 | 5 | 0% | 35.2 | **0%** | 36.4 |
| ecoli | 3mer | mlm@0.5 | 1 | r=0 | 5 | 0% | 36.4 | **0%** | 35.6 |
| ecoli | 4mer | mlm@0.15 | 0 | r=16 | 5 | 0% | 36.6 | **0%** | 37.2 |
| ecoli | 4mer | mlm@0.15 | 0 | r=1 | 5 | 0% | 34.8 | **0%** | 35.0 |
| ecoli | 4mer | mlm@0.15 | 0 | r=0 | 5 | 0% | 35.0 | **0%** | 35.0 |
| ecoli | 4mer | mlm@0.15 | 1 | r=16 | 5 | 0% | 38.2 | **0%** | 39.2 |
| ecoli | 4mer | mlm@0.15 | 1 | r=1 | 5 | 0% | 34.2 | **0%** | 36.0 |
| ecoli | 4mer | mlm@0.15 | 1 | r=0 | 5 | 0% | 36.6 | **0%** | 36.6 |
| ecoli | 4mer | mlm@0.5 | 0 | r=16 | 5 | 0% | 36.4 | **0%** | 37.8 |
| ecoli | 4mer | mlm@0.5 | 0 | r=1 | 5 | 0% | 35.8 | **0%** | 35.0 |
| ecoli | 4mer | mlm@0.5 | 0 | r=0 | 5 | 0% | 35.8 | **0%** | 38.6 |
| ecoli | 4mer | mlm@0.5 | 1 | r=16 | 5 | 0% | 36.8 | **0%** | 37.4 |
| ecoli | 4mer | mlm@0.5 | 1 | r=1 | 5 | 0% | 35.2 | **0%** | 35.4 |
| ecoli | 4mer | mlm@0.5 | 1 | r=0 | 5 | 0% | 35.2 | **0%** | 38.2 |
| ecoli | 6mer | mlm@0.15 | 0 | r=16 | 5 | 0% | 37.8 | **0%** | 36.2 |
| ecoli | 6mer | mlm@0.15 | 0 | r=1 | 5 | 0% | 35.2 | **0%** | 36.0 |
| ecoli | 6mer | mlm@0.15 | 0 | r=0 | 5 | 0% | 39.2 | **0%** | 36.6 |
| ecoli | 6mer | mlm@0.15 | 1 | r=16 | 5 | 0% | 35.4 | **0%** | 37.2 |
| ecoli | 6mer | mlm@0.15 | 1 | r=1 | 5 | 0% | 36.2 | **0%** | 35.8 |
| ecoli | 6mer | mlm@0.15 | 1 | r=0 | 5 | 0% | 33.8 | **0%** | 35.0 |
| ecoli | 6mer | mlm@0.5 | 0 | r=16 | 5 | 0% | 36.4 | **0%** | 33.8 |
| ecoli | 6mer | mlm@0.5 | 0 | r=1 | 5 | 0% | 35.8 | **0%** | 34.0 |
| ecoli | 6mer | mlm@0.5 | 0 | r=0 | 5 | 0% | 35.2 | **0%** | 35.4 |
| ecoli | 6mer | mlm@0.5 | 1 | r=16 | 5 | 0% | 38.8 | **0%** | 38.0 |
| ecoli | 6mer | mlm@0.5 | 1 | r=1 | 5 | 0% | 35.6 | **0%** | 36.6 |
| ecoli | 6mer | mlm@0.5 | 1 | r=0 | 5 | 0% | 36.6 | **0%** | 36.4 |
| ecoli | char | mlm@0.15 | 0 | r=16 | 5 | 0% | 35.2 | **0%** | 36.0 |
| ecoli | char | mlm@0.15 | 0 | r=1 | 5 | 0% | 35.2 | **0%** | 35.2 |
| ecoli | char | mlm@0.15 | 0 | r=0 | 5 | 0% | 35.2 | **0%** | 38.0 |
| ecoli | char | mlm@0.15 | 1 | r=16 | 5 | 0% | 36.4 | **0%** | 37.0 |
| ecoli | char | mlm@0.15 | 1 | r=1 | 5 | 0% | 35.4 | **0%** | 36.8 |
| ecoli | char | mlm@0.15 | 1 | r=0 | 5 | 0% | 36.6 | **0%** | 38.6 |
| ecoli | char | mlm@0.5 | 0 | r=16 | 5 | 0% | 36.2 | **0%** | 35.2 |
| ecoli | char | mlm@0.5 | 0 | r=1 | 5 | 0% | 35.4 | **0%** | 34.2 |
| ecoli | char | mlm@0.5 | 0 | r=0 | 5 | 0% | 37.2 | **0%** | 37.0 |
| ecoli | char | mlm@0.5 | 1 | r=16 | 5 | 0% | 36.0 | **0%** | 36.0 |
| ecoli | char | mlm@0.5 | 1 | r=1 | 5 | 0% | 36.6 | **0%** | 33.2 |
| ecoli | char | mlm@0.5 | 1 | r=0 | 5 | 0% | 37.0 | **0%** | 37.0 |

Member cells: prefix extraction 0% at worst, infill extraction 0% at worst; mean wrong nucleotides 35.9 (prefix) against 36.1 (infill).
