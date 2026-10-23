# Random-offset control — outputs/ecoli_ar vs outputs/traj1

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=0 | random/fresh non-member | 4.429 | 0.00 | 0.00 | 100 |
| 3mer | ar | r=1 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/train | 0.010 | 1.00 | 1.00 | 100 |
| 3mer | ar | r=1 | random/fresh in-phase | 4.306 | 0.00 | 0.00 | 33 |
| 3mer | ar | r=1 | random/fresh out-of-phase | 4.341 | 0.00 | 0.00 | 67 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/train | 0.011 | 1.00 | 1.00 | 100 |
| 3mer | ar | r=4 | random/fresh in-phase | 4.284 | 0.01 | 0.00 | 83 |
| 3mer | ar | r=4 | random/fresh out-of-phase | 4.462 | 0.00 | 0.00 | 17 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/train | 0.016 | 1.00 | 1.00 | 100 |
| 3mer | ar | r=16 | random/fresh in-phase | 4.130 | 0.08 | 0.00 | 100 |
| 6mer | ar | r=0 | random/fresh non-member | 2.636 | 0.01 | 0.00 | 100 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/train | 0.012 | 1.00 | 1.00 | 100 |
| 6mer | ar | r=1 | random/fresh in-phase | 2.519 | 0.00 | 0.00 | 15 |
| 6mer | ar | r=1 | random/fresh out-of-phase | 2.618 | 0.01 | 0.00 | 85 |
| 6mer | ar | r=4 | fixed/train | 0.003 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/train | 0.016 | 1.00 | 1.00 | 100 |
| 6mer | ar | r=4 | random/fresh in-phase | 2.422 | 0.05 | 0.00 | 55 |
| 6mer | ar | r=4 | random/fresh out-of-phase | 2.618 | 0.00 | 0.00 | 45 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/train | 0.019 | 1.00 | 1.00 | 100 |
| 6mer | ar | r=16 | random/fresh in-phase | 2.192 | 0.48 | 0.00 | 94 |
| 6mer | ar | r=16 | random/fresh out-of-phase | 2.631 | 0.00 | 0.00 | 6 |
| char | ar | r=0 | random/fresh non-member | 2.262 | 0.00 | 0.00 | 100 |
| char | ar | r=1 | fixed/train | 1.969 | 0.17 | 0.00 | 40 |
| char | ar | r=1 | random/train | 1.807 | 0.96 | 0.00 | 100 |
| char | ar | r=1 | random/fresh in-phase | 2.278 | 0.01 | 0.00 | 100 |
| char | ar | r=4 | fixed/train | 1.835 | 1.00 | 0.00 | 40 |
| char | ar | r=4 | random/train | 1.830 | 0.96 | 0.00 | 100 |
| char | ar | r=4 | random/fresh in-phase | 2.264 | 0.02 | 0.00 | 100 |
| char | ar | r=16 | fixed/train | 0.407 | 1.00 | 0.95 | 40 |
| char | ar | r=16 | random/train | 1.771 | 0.97 | 0.00 | 100 |
| char | ar | r=16 | random/fresh in-phase | 2.225 | 0.01 | 0.00 | 100 |