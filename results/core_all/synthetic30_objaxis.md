# Objective x tokenizer — synthetic, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | -0.00 | 2.040 (2.035-2.045) | 0.09 (0.08-0.10) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.15 | — | 2.000 (2.000-2.000) | 0.00 (0.00-0.00) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.5 | — | 2.001 (2.001-2.002) | 0.00 (0.00-0.00) | 0 (0-0)% | 2 |
| 3-mer | next-token | +0.00 | 4.150 (4.112-4.187) | 4.20 (4.16-4.24) | 100 (100-100)% | 2 |
| 3-mer | mlm@0.15 | — | 2.006 (2.006-2.007) | 0.01 (0.01-0.01) | 0 (0-0)% | 2 |
| 3-mer | mlm@0.5 | — | 2.015 (2.012-2.018) | 0.03 (0.03-0.04) | 0 (0-0)% | 2 |
| 4-mer | next-token | +0.00 | 3.294 (3.291-3.297) | 3.34 (3.33-3.36) | 100 (100-100)% | 2 |
| 4-mer | mlm@0.15 | — | 2.012 (2.009-2.016) | 0.03 (0.02-0.04) | 0 (0-0)% | 2 |
| 4-mer | mlm@0.5 | — | 2.046 (2.038-2.055) | 0.11 (0.09-0.12) | 0 (0-0)% | 2 |
| 6-mer | next-token | +0.01 | 2.632 (2.630-2.634) | 2.63 (2.61-2.64) | 100 (100-100)% | 2 |
| 6-mer | mlm@0.15 | — | 2.032 (2.032-2.033) | 0.11 (0.10-0.11) | 0 (0-0)% | 2 |
| 6-mer | mlm@0.5 | — | 2.044 (2.044-2.045) | 0.13 (0.12-0.13) | 0 (0-0)% | 2 |
