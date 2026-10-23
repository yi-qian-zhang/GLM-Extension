# Objective x tokenizer — ecoli, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | -0.00 | 2.131 (2.105-2.157) | 0.49 (0.43-0.56) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.15 | — | 1.962 (1.961-1.963) | -0.01 (-0.01--0.01) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.5 | — | 1.910 (1.909-1.911) | -0.01 (-0.01--0.00) | 0 (0-0)% | 2 |
| 3-mer | next-token | -0.02 | 4.142 (4.127-4.156) | 4.41 (4.40-4.43) | 100 (100-100)% | 2 |
| 3-mer | mlm@0.15 | — | 1.860 (1.859-1.860) | -0.01 (-0.01--0.01) | 0 (0-0)% | 2 |
| 3-mer | mlm@0.5 | — | 1.856 (1.855-1.857) | 0.00 (0.00-0.00) | 0 (0-0)% | 2 |
| 4-mer | next-token | -0.01 | 3.295 (3.294-3.295) | 3.35 (3.34-3.36) | 100 (100-100)% | 2 |
| 4-mer | mlm@0.15 | — | 1.968 (1.967-1.969) | 0.02 (0.01-0.02) | 0 (0-0)% | 2 |
| 4-mer | mlm@0.5 | — | 1.939 (1.927-1.950) | 0.00 (-0.00-0.01) | 0 (0-0)% | 2 |
| 6-mer | next-token | +0.01 | 2.542 (2.539-2.545) | 2.62 (2.61-2.63) | 100 (100-100)% | 2 |
| 6-mer | mlm@0.15 | — | 1.949 (1.948-1.950) | 0.06 (0.05-0.07) | 0 (0-0)% | 2 |
| 6-mer | mlm@0.5 | — | 1.945 (1.942-1.948) | 0.12 (0.09-0.14) | 0 (0-0)% | 2 |
