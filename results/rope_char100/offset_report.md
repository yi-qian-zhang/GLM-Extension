# Random-offset control — outputs/rope_char100 vs outputs/traj1

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=1 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | fixed/train | 0.003 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| char | ar | r=0 | random/fresh non-member | 11.080 | 0.01 | 0.00 | 80 |
| char | ar | r=1 | fixed/train | 1.969 | 0.17 | 0.00 | 40 |
| char | ar | r=1 | random/train | 0.008 | 1.00 | 0.97 | 40 |
| char | ar | r=1 | random/fresh in-phase | 10.743 | 0.00 | 0.00 | 40 |
| char | ar | r=4 | fixed/train | 1.835 | 1.00 | 0.00 | 40 |
| char | ar | r=4 | random/train | 0.012 | 1.00 | 0.95 | 40 |
| char | ar | r=4 | random/fresh in-phase | 10.929 | 0.00 | 0.00 | 40 |
| char | ar | r=16 | fixed/train | 0.407 | 1.00 | 0.95 | 40 |
| char | ar | r=16 | random/train | 0.014 | 1.00 | 0.93 | 40 |
| char | ar | r=16 | random/fresh in-phase | 10.549 | 0.00 | 0.00 | 40 |