#!/bin/bash
# 10 Oct, after the split re-draw: finish the objective x tokenizer grid on real human canaries.
#
# What is missing. The grid behind the headline claim of the mitigation section has char / 3-mer /
# 6-mer under next-token and two mask rates, with two model seeds. Three holes:
#   1. the 4-mer and 5-mer are absent on human, so the tokeniser axis has three points where the
#      synthetic grid has five, and the ordering claim on real human data rests on three;
#   2. every other table in the paper is three seeds, this one is two;
#   3. the BPE next-token cell has one seed, because its seed-0 run was never launched.
# Masked BPE is deliberately not run: with right-padding a bidirectional objective leaks through the
# pads (pilot2/bpe_arm.py), so that cell would not measure what it appears to.
# Also one symmetry fix: the 150-round delay claim has two seeds for char and one for the 6-mer.
#
# These cells are cheap (1-17 min each; the char cells are the slow ones at 96 token slots), so the
# whole queue is about an hour of GPU time. It waits for the two running queues so nothing contends.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_1010a.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_toy outputs/human_mlm outputs/human_long

# identical to queue_human_toy.sh and queue_1009b.sh, so new cells are comparable with the old ones
T="--data human --canary_npz $H --epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots"

cell(){                 # $1 tokenizer  $2 objective  $3 seed  $4 gpu
  local O=outputs/human_mlm
  [ "$2" = "ar" ] && O=outputs/human_toy
  python -m pilot2.run_pilot --tokenizer $1 --objective $2 --seed $3 --gpu $4 $T --out $O \
    > $O/$1_${2/@/}_s$3.log 2>&1
  log "$1 $2 s=$3 done"
}

# GPU 1 is free as soon as the last 1009b cell lands; GPUs 0/2/3 are held by the split re-draw
( until grep -q Q1009B_DONE outputs/queue_1009b.log 2>/dev/null; do sleep 60; done
  log "gpu1 start"
  for s in 2; do for o in ar mlm@0.15 mlm@0.50; do cell char $o $s 1; done; done
  for s in 0 1 2; do cell 4mer ar $s 1; done
  for s in 0 1 2; do cell 4mer mlm@0.15 $s 1; done ) &

( until grep -q DSEED_DONE outputs/queue_dseed.log 2>/dev/null; do sleep 60; done
  log "gpu0 start"
  for s in 0 1 2; do cell 4mer mlm@0.50 $s 0; done ) &   # no 5-mer: see the note below

# The GPU 2 branch asked for 5-mer cells and they cannot exist: non-overlapping k-mers need
# window % k == 0, the window is 288 nt, and 5 does not divide 288 (legal k: 1,2,3,4,6,8,9,12).
# tokenizers.py asserts it, so those six runs died in under a minute. DNABERT's 5-mer is unaffected --
# its k-mers overlap at stride 1 -- which is the same distinction that keeps the released family off
# the clean tokeniser axis. GPU 2 was given queue_1010b.sh instead.

( until grep -q DSEED_DONE outputs/queue_dseed.log 2>/dev/null; do sleep 60; done
  log "gpu3 start"
  for o in ar mlm@0.15 mlm@0.50; do cell 3mer $o 2 3; done
  for o in ar mlm@0.15 mlm@0.50; do cell 6mer $o 2 3; done
  B="--vocab_file data/tokenizers/bpe4096_gue.json --data human --canary_npz $H --epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --out outputs/human_toy"
  for s in 0 2; do
    python -m pilot2.bpe_arm --seed $s --gpu 3 $B > outputs/human_toy/bpe_s$s.log 2>&1
    log "bpe ar s=$s done"
  done
  # the 150-round reference curve for the delay claim, second seed
  python -m pilot2.run_pilot --tokenizer 6mer --objective ar --seed 1 --gpu 3 $T \
    --epochs 150 --save_epochs 20,30,50,80,110,150 --out outputs/human_long \
    > outputs/human_long/6mer_ar_s1.log 2>&1; log "long 6mer ar s=1 done" ) &
wait

R="outputs/human_toy outputs/human_mlm"
python -m pilot2.analyze_objaxis --root $R --data human --epoch 30 --name human30 > outputs/human_mlm/objaxis.log 2>&1
python -m pilot2.analyze_traj --root $R > outputs/human_mlm/traj.log 2>&1
python -m pilot2.analyze_matched --root $R --name human_obj > outputs/human_mlm/matched.log 2>&1
python -m pilot2.analyze_human --root $R --canary_npz $H --name human_obj > outputs/human_mlm/human.log 2>&1
python -m pilot2.analyze_traj --root outputs/human_long > outputs/human_long/traj.log 2>&1
log "Q1010A_DONE"
