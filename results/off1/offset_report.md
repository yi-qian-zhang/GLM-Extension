# Random-offset control — outputs/off1 vs outputs/traj1

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=0 | random/fresh non-member | 4.190 | 0.00 | 0.00 | 80 |
| 3mer | ar | r=1 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/train | 0.003 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/fresh in-phase | 4.184 | 0.00 | 0.00 | 13 |
| 3mer | ar | r=1 | random/fresh out-of-phase | 4.203 | 0.00 | 0.00 | 27 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/train | 0.012 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/fresh in-phase | 4.142 | 0.00 | 0.00 | 30 |
| 3mer | ar | r=4 | random/fresh out-of-phase | 4.241 | 0.00 | 0.00 | 10 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/train | 0.009 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/fresh in-phase | 4.021 | 0.05 | 0.00 | 40 |
| 6mer | ar | r=0 | random/fresh non-member | 2.513 | 0.01 | 0.00 | 80 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/train | 0.007 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/fresh in-phase | 2.360 | 0.00 | 0.00 | 7 |
| 6mer | ar | r=1 | random/fresh out-of-phase | 2.515 | 0.00 | 0.00 | 33 |
| 6mer | ar | r=4 | fixed/train | 0.003 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/train | 0.020 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/fresh in-phase | 2.433 | 0.00 | 0.00 | 17 |
| 6mer | ar | r=4 | random/fresh out-of-phase | 2.537 | 0.00 | 0.00 | 23 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/train | 0.012 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/fresh in-phase | 2.177 | 0.33 | 0.00 | 39 |
| 6mer | ar | r=16 | random/fresh out-of-phase | 2.491 | 0.00 | 0.00 | 1 |
| char | ar | r=0 | random/fresh non-member | 2.069 | 0.00 | 0.00 | 80 |
| char | ar | r=1 | fixed/train | 1.969 | 0.17 | 0.00 | 40 |
| char | ar | r=1 | random/train | 1.926 | 0.53 | 0.00 | 40 |
| char | ar | r=1 | random/fresh in-phase | 2.065 | 0.00 | 0.00 | 40 |
| char | ar | r=4 | fixed/train | 1.835 | 1.00 | 0.00 | 40 |
| char | ar | r=4 | random/train | 1.928 | 0.50 | 0.00 | 40 |
| char | ar | r=4 | random/fresh in-phase | 2.064 | 0.00 | 0.00 | 40 |
| char | ar | r=16 | fixed/train | 0.407 | 1.00 | 0.95 | 40 |
| char | ar | r=16 | random/train | 1.928 | 0.45 | 0.00 | 40 |
| char | ar | r=16 | random/fresh in-phase | 2.060 | 0.00 | 0.00 | 40 |