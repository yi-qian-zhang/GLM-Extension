# Objective x tokenizer — gue, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | -0.01 | 2.001 (1.999-2.003) | 0.13 (0.12-0.15) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.15 | — | 1.923 (1.923-1.924) | -0.01 (-0.01--0.01) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.5 | — | 1.915 (1.913-1.917) | 0.00 (-0.00-0.01) | 0 (0-0)% | 2 |
| 3-mer | next-token | -0.01 | 3.942 (3.917-3.967) | 4.05 (3.99-4.12) | 100 (100-100)% | 2 |
| 3-mer | mlm@0.15 | — | 1.911 (1.911-1.911) | 0.00 (-0.00-0.00) | 0 (0-0)% | 2 |
| 3-mer | mlm@0.5 | — | 1.925 (1.923-1.927) | -0.00 (-0.01-0.00) | 0 (0-0)% | 2 |
| 4-mer | next-token | -0.01 | 3.216 (3.214-3.217) | 3.25 (3.23-3.27) | 100 (100-100)% | 2 |
| 4-mer | mlm@0.15 | — | 1.916 (1.916-1.917) | 0.00 (0.00-0.01) | 0 (0-0)% | 2 |
| 4-mer | mlm@0.5 | — | 1.926 (1.925-1.927) | 0.02 (0.02-0.03) | 0 (0-0)% | 2 |
| 6-mer | next-token | +0.02 | 2.497 (2.496-2.499) | 2.53 (2.53-2.54) | 100 (100-100)% | 2 |
| 6-mer | mlm@0.15 | — | 1.953 (1.952-1.953) | 0.12 (0.11-0.13) | 0 (0-0)% | 2 |
| 6-mer | mlm@0.5 | — | 1.963 (1.963-1.963) | 0.23 (0.22-0.23) | 0 (0-0)% | 2 |
