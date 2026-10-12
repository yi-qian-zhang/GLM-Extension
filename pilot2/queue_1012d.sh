#!/bin/bash
# 12 Oct. Replicate the one number that changes the paper's claim, and see whether it is a trend.
#
# The new result is that iterated conditional modes recovers 12 % of 16x-planted canaries verbatim
# from a 150-round masked cell that both published protocols call clean (prefix 0 %, edge-conditioned
# infill 0 %, non-member control 0 % under ICM with its Hamming moving the wrong way). It rests on
# ONE cell: 6-mer, mlm@0.15, human chromosome 22, seed 0, three of twenty-five probes. That is not
# enough to put in an abstract, and it is cheap to fix -- a 150-round cell on this backbone is about
# four minutes of training plus its snapshot scoring.
#
# Two questions, both answered by training alone:
#   seeds   does the 12 % survive re-drawing the corpus split and the initialisation? Seeds 1 and 2
#           for both tokenisers, everything else identical to queue_1011h.
#   trend   is 150 rounds the end of it? The 6-mer cell's per-step top-1 accuracy was 0.41 and
#           all-48-exact needs eight consecutive steps, so the extraction rate should climb steeply
#           with per-step accuracy. 300 rounds tests that, and tells us whether the number we quote
#           is a plateau or a point on a rising curve.
#
# Nothing here edits a file any running queue imports: queue_1012a is in its last two fine-tunes and
# queue_1012b and _1012c are both parked waiting for it, so new processes running the SAME unmodified
# run_pilot are the only safe thing to start. The --canary_alone flag for the Evo replication still
# waits, because it touches data.py, real_data.py, tokenizers.py and score.py.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1012d.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/human_mlm_long outputs/human_mlm_300
log "start"

# identical to queue_1011h's T
T="--data human --canary_npz $H/canaries_chr22.npz --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --score_snapshots"

# ---- seeds 1 and 2 at 150 rounds, both tokenisers ----------------------------------------------
S150="--epochs 150 --save_epochs 30,50,80,110,150 --out outputs/human_mlm_long"
( for s in 1 2; do
    run "6mer s$s 150r" python -m pilot2.run_pilot --tokenizer 6mer --objective mlm@0.15 --seed $s \
      --gpu 0 $T $S150 > outputs/human_mlm_long/6mer_s$s.log 2>&1
  done ) &
( for s in 1 2; do
    run "3mer s$s 150r" python -m pilot2.run_pilot --tokenizer 3mer --objective mlm@0.15 --seed $s \
      --gpu 1 $T $S150 > outputs/human_mlm_long/3mer_s$s.log 2>&1
  done ) &
wait
log "seeds done"

# ---- 300 rounds, seed 0, to see whether 150 is a plateau or a point on a rising curve -----------
S300="--epochs 300 --save_epochs 150,200,250,300 --out outputs/human_mlm_300"
( run "6mer s0 300r" python -m pilot2.run_pilot --tokenizer 6mer --objective mlm@0.15 --seed 0 \
    --gpu 0 $T $S300 > outputs/human_mlm_300/6mer.log 2>&1 ) &
( run "3mer s0 300r" python -m pilot2.run_pilot --tokenizer 3mer --objective mlm@0.15 --seed 0 \
    --gpu 1 $T $S300 > outputs/human_mlm_300/3mer.log 2>&1 ) &
wait
log "300 rounds done"

python -m pilot2.analyze_traj --root outputs/human_mlm_long > outputs/human_mlm_long/traj.log 2>&1
python -m pilot2.analyze_traj --root outputs/human_mlm_300  > outputs/human_mlm_300/traj.log  2>&1

# the three decoders on everything this queue produced, at the sweep's settings
A="--tiers 1,4,16 --max_probes 20 --sweeps 4 --name recon_audit"
run "recon 150r seeds" python -m pilot2.recon_audit --root outputs/human_mlm_long $A --gpu 0 \
  > outputs/recon_human_mlm_long.log 2>&1
run "recon 300r"       python -m pilot2.recon_audit --root outputs/human_mlm_300  $A --gpu 1 \
  > outputs/recon_human_mlm_300.log 2>&1
log Q1012D_DONE
