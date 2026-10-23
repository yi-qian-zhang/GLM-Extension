# Objective x tokenizer — human, canary planted 16x, round 30

`excess` = non-member bits/nt − member bits/nt (higher = more memorised). `ep1 excess` is the same statistic before anything is memorised: for a from-scratch backbone it must be ~0, and whatever it reads is the fixed offset between the two canary groups. Mean over model seeds, with the across-seed range where there is more than one seed.

**Read this table down a tokeniser's rows, not across tokenisers.** Within a tokeniser the objectives share a schedule and the masked cells reach the same or a better held-out loss, so the comparison is sound. Across tokenisers the held-out losses differ by more than a bit/nt at the same round, which confounds the excess; the tokeniser axis is read at matched held-out loss (`analyze_matched`, `analyze_traj`), never from this table.

| tokenizer | objective | ep1 excess | held-out loss | excess | verbatim extraction | seeds |
|---|---|---|---|---|---|---|
| char (1 nt) | next-token | +0.00 | 1.789 (1.778-1.800) | 0.31 (0.27-0.36) | 0 (0-0)% | 3 |
| char (1 nt) | mlm@0.15 | +0.01 | 1.866 (1.854-1.875) | 0.02 (0.01-0.02) | 0 (0-0)% | 3 |
| char (1 nt) | mlm@0.50 | -0.01 | 1.833 (1.832-1.835) | 0.03 (0.03-0.04) | 0 (0-0)% | 3 |
| 3-mer | next-token | +0.02 | 3.921 (3.911-3.940) | 4.24 (4.17-4.28) | 100 (100-100)% | 3 |
| 3-mer | mlm@0.15 | +0.01 | 1.721 (1.705-1.729) | 0.12 (0.10-0.14) | 0 (0-0)% | 3 |
| 3-mer | mlm@0.50 | +0.01 | 1.667 (1.661-1.672) | 0.15 (0.15-0.15) | 0 (0-0)% | 3 |
| 4-mer | next-token | +0.01 | 3.051 (3.041-3.068) | 3.23 (3.21-3.25) | 100 (100-100)% | 3 |
| 4-mer | mlm@0.15 | +0.00 | 1.729 (1.720-1.743) | 0.16 (0.15-0.17) | 0 (0-0)% | 3 |
| 4-mer | mlm@0.50 | +0.00 | 1.688 (1.682-1.695) | 0.23 (0.21-0.25) | 0 (0-0)% | 3 |
| 6-mer | next-token | +0.02 | 2.348 (2.345-2.350) | 2.45 (2.44-2.46) | 100 (100-100)% | 3 |
| 6-mer | mlm@0.15 | +0.01 | 1.839 (1.836-1.841) | 0.16 (0.16-0.17) | 0 (0-0)% | 3 |
| 6-mer | mlm@0.50 | +0.01 | 1.807 (1.805-1.809) | 0.29 (0.28-0.30) | 0 (0-0)% | 3 |
| BPE-4096 | next-token | +0.04 | 2.675 (2.671-2.681) | 2.80 (2.79-2.82) | 100 (100-100)% | 3 |
