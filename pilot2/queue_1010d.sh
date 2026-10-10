#!/bin/bash
# 10 Oct, GPUs 0 and 3 after queue_1010c. Last gap in the grid: the synthetic arm (core_all /
# core_mlm) has char / 3-mer / 6-mer, while the four real datasets now have the 4-mer too, so the
# tokeniser axis is five points everywhere except on the dataset the mechanism section uses most.
# Six runs, the cheapest cells in the project.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1010d.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
log "start"

# copied from core_all / core_mlm (synthetic = the default --data)
A="--n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/core_all"
M="--n_train 5000 --tiers 1,4,16 --probes_per_tier 40 --n_nonmember 40 --pool 300 --floor_n 500 --probe_offset random --epochs 30 --out outputs/core_all"

( for s in 0 1; do
    python -m pilot2.run_pilot --tokenizer 4mer --objective ar --seed $s --gpu 0 $A \
      > outputs/core_all/4mer_ar_s$s.log 2>&1; log "ar 4mer s=$s done"
  done ) &
( for s in 0 1; do for o in mlm@0.15 mlm@0.5; do
    python -m pilot2.run_pilot --tokenizer 4mer --objective $o --seed $s --gpu 3 $M \
      > outputs/core_all/4mer_${o/@/}_s$s.log 2>&1; log "mlm 4mer $o s=$s done"
  done; done ) &
wait
# one root only: outputs/core_mlm is a duplicate of core_all's masked cells (same files, same
# md5), and passing both would count every synthetic masked cell twice
python -m pilot2.analyze_objaxis --root outputs/core_all --data synthetic --epoch 30 \
  --name synthetic30 > outputs/core_mlm/objaxis.log 2>&1
log "Q1010D_DONE"
