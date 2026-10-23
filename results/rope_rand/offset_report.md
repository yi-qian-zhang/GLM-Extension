# Random-offset control — outputs/rope_rand vs outputs/rope_fixed

bits/nt / rank-1 / exact extraction, mean over seeds (n = probes pooled over seeds). 2.000 bits = nothing memorized; rank-1 chance 0.002.

| tok | obj | tier | condition | bits/nt | rank-1 | exact | n |
|---|---|---|---|---|---|---|---|
| 3mer | ar | r=0 | random/fresh non-member | 4.357 | 0.00 | 0.00 | 80 |
| 3mer | ar | r=1 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/train | 0.003 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=1 | random/fresh in-phase | 4.260 | 0.00 | 0.00 | 13 |
| 3mer | ar | r=1 | random/fresh out-of-phase | 4.253 | 0.00 | 0.00 | 27 |
| 3mer | ar | r=4 | fixed/train | 0.002 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/train | 0.013 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=4 | random/fresh in-phase | 4.099 | 0.07 | 0.00 | 30 |
| 3mer | ar | r=4 | random/fresh out-of-phase | 4.234 | 0.00 | 0.00 | 10 |
| 3mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/train | 0.009 | 1.00 | 1.00 | 40 |
| 3mer | ar | r=16 | random/fresh in-phase | 3.793 | 0.30 | 0.00 | 40 |
| 6mer | ar | r=0 | random/fresh non-member | 2.513 | 0.00 | 0.00 | 80 |
| 6mer | ar | r=1 | fixed/train | 0.005 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/train | 0.006 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=1 | random/fresh in-phase | 2.314 | 0.00 | 0.00 | 7 |
| 6mer | ar | r=1 | random/fresh out-of-phase | 2.519 | 0.00 | 0.00 | 33 |
| 6mer | ar | r=4 | fixed/train | 0.004 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/train | 0.018 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=4 | random/fresh in-phase | 2.081 | 0.47 | 0.00 | 17 |
| 6mer | ar | r=4 | random/fresh out-of-phase | 2.516 | 0.00 | 0.00 | 23 |
| 6mer | ar | r=16 | fixed/train | 0.001 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/train | 0.011 | 1.00 | 1.00 | 40 |
| 6mer | ar | r=16 | random/fresh in-phase | 1.766 | 0.82 | 0.03 | 39 |
| 6mer | ar | r=16 | random/fresh out-of-phase | 2.570 | 0.00 | 0.00 | 1 |
| char | ar | r=0 | random/fresh non-member | 2.045 | 0.00 | 0.00 | 80 |
| char | ar | r=1 | fixed/train | 1.932 | 0.47 | 0.00 | 40 |
| char | ar | r=1 | random/train | 1.964 | 0.20 | 0.00 | 40 |
| char | ar | r=1 | random/fresh in-phase | 2.046 | 0.00 | 0.00 | 40 |
| char | ar | r=4 | fixed/train | 1.920 | 0.57 | 0.00 | 40 |
| char | ar | r=4 | random/train | 1.942 | 0.40 | 0.00 | 40 |
| char | ar | r=4 | random/fresh in-phase | 2.046 | 0.00 | 0.00 | 40 |
| char | ar | r=16 | fixed/train | 1.851 | 0.97 | 0.00 | 40 |
| char | ar | r=16 | random/train | 1.938 | 0.45 | 0.00 | 40 |
| char | ar | r=16 | random/fresh in-phase | 2.033 | 0.00 | 0.00 | 40 |