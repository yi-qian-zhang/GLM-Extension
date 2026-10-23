# Random-offset control — outputs/off2 vs outputs/traj1

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=0 | random/fresh non-member | 5.728 | 0.00 | 0.00 | 80 |
| 3mer | ar | r=1 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/train | 0.000 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/fresh in-phase | 5.785 | 0.00 | 0.00 | 13 |
| 3mer | ar | r=1 | random/fresh out-of-phase | 5.781 | 0.00 | 0.00 | 27 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/train | 0.007 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/fresh in-phase | 5.691 | 0.00 | 0.00 | 30 |
| 3mer | ar | r=4 | random/fresh out-of-phase | 5.911 | 0.00 | 0.00 | 10 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/train | 0.007 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/fresh in-phase | 5.682 | 0.05 | 0.00 | 40 |
| 6mer | ar | r=0 | random/fresh non-member | 3.262 | 0.00 | 0.00 | 80 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/train | 0.000 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/fresh in-phase | 3.007 | 0.00 | 0.00 | 7 |
| 6mer | ar | r=1 | random/fresh out-of-phase | 3.296 | 0.00 | 0.00 | 33 |
| 6mer | ar | r=4 | fixed/train | 0.003 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/train | 0.012 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/fresh in-phase | 3.066 | 0.00 | 0.00 | 17 |
| 6mer | ar | r=4 | random/fresh out-of-phase | 3.255 | 0.00 | 0.00 | 23 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/train | 0.006 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/fresh in-phase | 2.741 | 0.38 | 0.00 | 39 |
| 6mer | ar | r=16 | random/fresh out-of-phase | 3.409 | 0.00 | 0.00 | 1 |
| char | ar | r=0 | random/fresh non-member | 7.602 | 0.00 | 0.00 | 80 |
| char | ar | r=1 | fixed/train | 1.969 | 0.17 | 0.00 | 40 |
| char | ar | r=1 | random/train | 0.025 | 1.00 | 0.85 | 40 |
| char | ar | r=1 | random/fresh in-phase | 7.376 | 0.00 | 0.00 | 40 |
| char | ar | r=4 | fixed/train | 1.835 | 1.00 | 0.00 | 40 |
| char | ar | r=4 | random/train | 0.030 | 1.00 | 0.88 | 40 |
| char | ar | r=4 | random/fresh in-phase | 7.670 | 0.00 | 0.00 | 40 |
| char | ar | r=16 | fixed/train | 0.407 | 1.00 | 0.95 | 40 |
| char | ar | r=16 | random/train | 0.037 | 1.00 | 0.85 | 40 |
| char | ar | r=16 | random/fresh in-phase | 7.421 | 0.00 | 0.00 | 40 |