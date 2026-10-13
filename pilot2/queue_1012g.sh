#!/bin/bash
# 13 Oct. Is the slot count a barrier or only a delay? And repair the prior arm's audit.
#
# WHAT THE 300-ROUND CELLS SAID (queue_1012d, one restart only):
#
#   6-mer, r=16 : leave-one-out top-1 1.00, prefix protocol 10 %, ICM 40 %
#   6-mer, r=1  : leave-one-out top-1 1.00, prefix 0 %, ICM 20 %
#   3-mer, all  : leave-one-out top-1 1.00 at EVERY tier, 0.001-0.011 bits/nt, prefix 0 %, ICM 0 %
#   non-member  : leave-one-out top-1 0.02-0.10, everything 0 %
#
# Two things there are new. First, at 300 rounds the PUBLISHED prefix protocol extracts from a
# masked model by itself -- 10 % at r=16 -- so the paper's 0 % was a budget statement as well as an
# attack statement. Second, and sharper: both tokenisers now store the record PERFECTLY. A
# leave-one-out top-1 of 1.00 with 0.001 bits/nt means that given the other target tokens the model
# names the remaining one correctly every single time, at every multiplicity, including a canary
# inserted once. The 6-mer emits 20-40 % of that and the 3-mer emits nothing at all, and the only
# thing left between them is that the 3-mer target is 16 joint slots and the 6-mer's is 8.
#
# So the question this queue settles is whether 16 slots is a BARRIER or a DELAY. Perfect per-token
# knowledge plus 128 restarts is the strongest attack we can build; if the 3-mer still returns 0 %
# the slot count is a real obstruction and the paper can say a fine tokeniser keeps a perfectly
# memorised record unreachable, which is a much stronger recommendation than "memorises less". If it
# breaks, then tokenisation only buys search time and the recommendation has to be stated that way.
#
# Also here: the prior arm's audit, which queue_1012e recorded as FAIL(1) because its run
# directories are one level deeper than the sweep's other roots (outputs/ft22_mlm_long/<size>_<tok>/
# <tok>_mlm0.15_ft_s0), so nothing matched; and the restart attack on seeds 1 and 2, because the
# 12 % has so far been replicated only at one restart (15 % and 5 %).
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1012g.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
log "start"

B="--tiers 1,4,16 --max_probes 20 --sweeps 4"

# ---- card 0: the 300-round cells, where both tokenisers store the record perfectly -------------
( for R in 32 128; do
    run "300r 3mer r=$R" python -m pilot2.recon_audit --root outputs/human_mlm_300/3mer_mlm0.15_s0 \
      $B --restarts $R --gpu 0 --name recon_r$R > outputs/recon_r${R}_3mer300.log 2>&1
    run "300r 6mer r=$R" python -m pilot2.recon_audit --root outputs/human_mlm_300/6mer_mlm0.15_s0 \
      $B --restarts $R --gpu 0 --name recon_r$R > outputs/recon_r${R}_6mer300.log 2>&1
  done ) &

# ---- card 3: the prior arm at its real depth, then the seeds under the attack ------------------
( for d in outputs/ft22_mlm_long/*/; do
    [ -d "$d" ] || continue
    t=$(basename "$d")
    run "prior $t r=128" python -m pilot2.recon_audit --root "$d" $B --restarts 128 --gpu 3 \
      --name recon_r128 > "outputs/recon_r128_ft22_$t.log" 2>&1
  done
  run "150r seeds r=32" python -m pilot2.recon_audit --root outputs/human_mlm_long $B --restarts 32 \
    --gpu 3 --name recon_r32 > outputs/recon_r32_human_mlm_long.log 2>&1 ) &
wait
log Q1012G_DONE
