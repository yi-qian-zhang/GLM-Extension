# Random-offset control — outputs/core100 vs outputs/traj1

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=0 | random/fresh non-member | 4.246 | 0.01 | 0.00 | 300 |
| 3mer | ar | r=1 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/train | 0.015 | 1.00 | 1.00 | 300 |
| 3mer | ar | r=1 | random/fresh in-phase | 4.232 | 0.00 | 0.00 | 101 |
| 3mer | ar | r=1 | random/fresh out-of-phase | 4.255 | 0.01 | 0.00 | 199 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/train | 0.013 | 1.00 | 1.00 | 300 |
| 3mer | ar | r=4 | random/fresh in-phase | 4.267 | 0.01 | 0.00 | 247 |
| 3mer | ar | r=4 | random/fresh out-of-phase | 4.274 | 0.00 | 0.00 | 53 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/train | 0.017 | 1.00 | 1.00 | 300 |
| 3mer | ar | r=16 | random/fresh in-phase | 4.173 | 0.02 | 0.00 | 300 |
| 6mer | ar | r=0 | random/fresh non-member | 2.573 | 0.00 | 0.00 | 300 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/train | 0.031 | 1.00 | 1.00 | 300 |
| 6mer | ar | r=1 | random/fresh in-phase | 2.449 | 0.00 | 0.00 | 48 |
| 6mer | ar | r=1 | random/fresh out-of-phase | 2.583 | 0.00 | 0.00 | 252 |
| 6mer | ar | r=4 | fixed/train | 0.003 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/train | 0.030 | 1.00 | 1.00 | 300 |
| 6mer | ar | r=4 | random/fresh in-phase | 2.427 | 0.08 | 0.00 | 151 |
| 6mer | ar | r=4 | random/fresh out-of-phase | 2.581 | 0.00 | 0.00 | 149 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/train | 0.030 | 1.00 | 1.00 | 300 |
| 6mer | ar | r=16 | random/fresh in-phase | 2.238 | 0.39 | 0.00 | 285 |
| 6mer | ar | r=16 | random/fresh out-of-phase | 2.534 | 0.00 | 0.00 | 15 |
| char | ar | r=0 | random/fresh non-member | 2.040 | 0.00 | 0.00 | 300 |
| char | ar | r=1 | fixed/train | 1.969 | 0.17 | 0.00 | 40 |
| char | ar | r=1 | random/train | 1.951 | 0.33 | 0.00 | 300 |
| char | ar | r=1 | random/fresh in-phase | 2.042 | 0.01 | 0.00 | 300 |
| char | ar | r=4 | fixed/train | 1.835 | 1.00 | 0.00 | 40 |
| char | ar | r=4 | random/train | 1.953 | 0.30 | 0.00 | 300 |
| char | ar | r=4 | random/fresh in-phase | 2.038 | 0.01 | 0.00 | 300 |
| char | ar | r=16 | fixed/train | 0.407 | 1.00 | 0.95 | 40 |
| char | ar | r=16 | random/train | 1.949 | 0.32 | 0.00 | 300 |
| char | ar | r=16 | random/fresh in-phase | 2.039 | 0.00 | 0.00 | 300 |