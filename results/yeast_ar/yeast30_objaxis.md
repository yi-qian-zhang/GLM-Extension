# Objective x tokenizer — yeast, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | +0.00 | 2.000 (1.999-2.002) | 0.15 (0.14-0.15) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.15 | — | 1.927 (1.927-1.927) | -0.01 (-0.01--0.01) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.5 | — | 1.923 (1.922-1.924) | 0.00 (0.00-0.01) | 0 (0-0)% | 2 |
| 3-mer | next-token | -0.00 | 3.991 (3.969-4.013) | 4.08 (4.03-4.13) | 100 (100-100)% | 2 |
| 3-mer | mlm@0.15 | — | 1.905 (1.904-1.906) | 0.00 (0.00-0.00) | 0 (0-0)% | 2 |
| 3-mer | mlm@0.5 | — | 1.928 (1.928-1.928) | 0.02 (0.02-0.02) | 0 (0-0)% | 2 |
| 4-mer | next-token | +0.02 | 3.250 (3.248-3.252) | 3.36 (3.34-3.37) | 100 (100-100)% | 2 |
| 4-mer | mlm@0.15 | — | 1.937 (1.937-1.937) | 0.02 (0.02-0.02) | 0 (0-0)% | 2 |
| 4-mer | mlm@0.5 | — | 1.945 (1.943-1.948) | 0.03 (0.03-0.04) | 0 (0-0)% | 2 |
| 6-mer | next-token | +0.03 | 2.531 (2.530-2.531) | 2.60 (2.59-2.62) | 100 (100-100)% | 2 |
| 6-mer | mlm@0.15 | — | 1.965 (1.965-1.965) | 0.14 (0.13-0.15) | 0 (0-0)% | 2 |
| 6-mer | mlm@0.5 | — | 1.971 (1.964-1.977) | 0.20 (0.13-0.27) | 0 (0-0)% | 2 |
