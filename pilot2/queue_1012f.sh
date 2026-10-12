#!/bin/bash
# 12 Oct. How far does the search budget take it, and does the 3-mer's harder search ever pay off?
#
# The attack rate against the 150-round 6-mer masked cell, 25 probes at r=16, rises with restarts
# and does not flatten:
#
#   restarts   1    2    4    8   16   32
#   r=16      12%  16%  20%  20%  24%  40%      (mean wrong nucleotides 26.4 -> 12.9 of 48)
#   r=1        0%   0%   0%   4%   4%   4%
#
# against a leave-one-out ceiling of 0.84, which is where the information in the model says a
# perfect search would land. Two things follow that this queue settles.
#
#   1. Any masked extraction number in the paper is a lower bound set by the compute we spent, so we
#      have to say where our curve was still climbing. 64 and 128 restarts say whether 40 % is near
#      a knee or still mid-slope.
#   2. The 3-mer cell holds just as much of the record (leave-one-out top-1 0.96 per token, 0.116
#      bits/nt, ceiling 0.72) and recovered nothing at eight restarts. Its target is 16 joint slots
#      against the 6-mer's 8, so if tokenisation acts on extraction through search difficulty rather
#      than through storage, the 3-mer should also break -- just later. 128 restarts tests exactly
#      that, and a null result there is as informative as a positive one, because it would mean the
#      slot count is a hard barrier and not a delay.
#
# No training. Card 0, which carries only queue_1012d's 12.6M cells beside this.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1012f.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
log "start"

C6=outputs/human_mlm_long/6mer_mlm0.15_s0
C3=outputs/human_mlm_long/3mer_mlm0.15_s0
A="--tiers 1,4,16 --max_probes 25 --sweeps 4 --gpu 0"

for R in 64 128; do
  run "6mer r=$R" python -m pilot2.recon_audit --root $C6 $A --restarts $R --name recon_r$R \
    > outputs/recon_r${R}_6mer150.log 2>&1
done
for R in 32 128; do
  run "3mer r=$R" python -m pilot2.recon_audit --root $C3 $A --restarts $R --name recon_r$R \
    > outputs/recon_r${R}_3mer150.log 2>&1
done
log Q1012F_DONE
