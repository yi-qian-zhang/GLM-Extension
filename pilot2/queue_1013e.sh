#!/bin/bash
# 13 Oct. The number the headline is missing: at what HELD-OUT LOSS does recovery begin?
#
# THE PROBLEM, found by audit and then verified. The 95-100 % reconstruction is measured at 300
# rounds, and the held-out loss of those cells is 2.866 bits/nt on chromosome 22 and 3.164 on
# E. coli. The best this backbone reaches on chromosome 22 is 1.675, and a uniform predictor scores
# 2.000. So the cells where every record comes back are WORSE THAN A COIN at predicting held-out
# sequence. Nobody would ship them, and this paper's own rule (Sec. 3) is to compare at matched
# held-out loss, so quoting 95 % without that number beside it is the first thing a reviewer will
# attack -- and they would be right.
#
# That does not make the result wrong, it makes it unquantified. The question the paper has to answer
# is not "what happens at 300 rounds" but "at what utility does recovery start", and the answer is a
# curve, not a point. We already know two of its points, both from cells whose snapshots were
# deleted before checkpoint retention became the default:
#
#   round 30   floor 1.675 (the optimum)   128 restarts -> 0 %
#   round 150  floor 2.176                 128 restarts -> 48 % at r=16, 4 % at r=1
#   round 300  floor 2.866                 128 restarts -> 95 % at r=16, 95 % at r=1
#
# The interesting region is entirely between the first two and has never been measured with the
# decoder. If recovery only begins past 2.0 -- past the point where the model is worse than uniform
# -- then the practical risk is small and the paper must say so plainly. If it begins at 1.75 or
# 1.80, where a model is still perfectly usable, then it is a real privacy result. Those two
# readings support opposite recommendations, so this is the most important measurement left.
#
# WHAT THIS RUNS. One cell per tokeniser, retrained with twelve snapshots kept, then the decoder at
# every snapshot. Two tiers only (16 copies and a single copy) and 20 probes, because the point is
# the shape of the curve against held-out loss rather than another endpoint. Checkpoint retention is
# now the default, so this is the first run that can produce the curve without retraining per point.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1013e.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/curve
log "start"

E="15,30,45,60,80,100,120,150,190,230,265,300"
T="--data human --canary_npz $H/canaries_chr22.npz --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --score_snapshots --epochs 300 --out outputs/curve"

( run "curve 6mer train" python -m pilot2.run_pilot --tokenizer 6mer --objective mlm@0.15 --seed 0 \
    --gpu 3 $T --save_epochs $E > outputs/curve/6mer.log 2>&1 ) &
( run "curve 3mer train" python -m pilot2.run_pilot --tokenizer 3mer --objective mlm@0.15 --seed 0 \
    --gpu 2 $T --save_epochs $E > outputs/curve/3mer.log 2>&1 ) &
wait
log "training done, snapshots kept"

# the decoder at every snapshot, so each point carries its own held-out loss
for tok in 6mer 3mer; do
  d=outputs/curve/${tok}_mlm0.15_s0
  for e in $(echo $E | tr ',' ' '); do
    [ -f "$d/ep$e.pt" ] || { log "MISSING $d/ep$e.pt"; continue; }
    run "decode $tok ep$e" python -m pilot2.recon_audit --root $d --ckpt ep$e.pt \
      --tiers 1,16 --max_probes 20 --sweeps 4 --restarts 128 --gpu 3 --name recon_ep$e \
      > outputs/curve/recon_${tok}_ep$e.log 2>&1
  done
done
log Q1013E_DONE
