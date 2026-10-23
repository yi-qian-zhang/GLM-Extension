# Objective x tokenizer — ecoli, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | -0.00 | 3.273 (3.211-3.335) | 2.36 (2.35-2.36) | 0 (0-0)% | 2 |
| char (1 nt) | mlm@0.15 | — | 1.963 | -0.01 | 0% | 1 |
| 3-mer | next-token | -0.02 | 4.711 (4.688-4.733) | 5.17 (5.13-5.21) | 100 (100-100)% | 2 |
| 3-mer | mlm@0.15 | — | 1.855 | -0.00 | 0% | 1 |
| 4-mer | next-token | -0.01 | 3.420 (3.419-3.420) | 3.49 (3.48-3.50) | 100 (100-100)% | 2 |
| 4-mer | mlm@0.15 | — | 1.966 | 0.01 | 0% | 1 |
| 6-mer | next-token | +0.01 | 2.444 (2.442-2.446) | 2.51 (2.51-2.51) | 100 (100-100)% | 2 |
| 6-mer | mlm@0.15 | — | 1.957 | 0.04 | 0% | 1 |
