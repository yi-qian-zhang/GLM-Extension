#!/bin/bash
# 10 Oct, GPUs 0 and 3 (their queue_1010a branches finished at 05:18; GPU 1 is on the slow character
# cells and GPU 2 on queue_1010b).
#
# The objective claim now leads the mitigation section, so it should hold on every dataset in the
# paper, not on three of five. Inventory before this queue:
#   synthetic  AR + masked (core_all)        E. coli  AR + masked (queue_1010b finished it)
#   human      AR + masked (queue_1009b/a)   yeast    AR only       GUE  AR only
# So yeast and GUE get their masked cells here, two mask rates and two seeds, plus the 4-mer on both
# objectives so all four real datasets share the same tokeniser axis (char / 3-mer / 4-mer / 6-mer;
# there is no 5-mer on a 288-nt window, see 3.29).
#
# Masked arms are configured as in core_mlm and ecoli_mlm -- 40 canaries per tier, ranking pool 300,
# final checkpoint only -- so the new cells are comparable with the masked arms already in the log.
# Snapshots would multiply the PLL scoring cost by eight (it is one forward pass per masked position,
# so 288 for the character tokeniser), which is why that arm has never carried them.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1010c.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/yeast_mlm outputs/gue_mlm
log "start"

arm(){                  # $1 dataset  $2 gpu
  local D=$1 G=$2
  local A="--data $D --n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/${D}_ar"
  local M="--data $D --n_train 5000 --tiers 1,4,16 --probes_per_tier 40 --n_nonmember 40 --pool 300 --floor_n 500 --probe_offset random --epochs 30 --out outputs/${D}_mlm"
  # cheap tokenisers first: if the queue is cut short, the character cell is the one left unfinished
  for t in 6mer 3mer 4mer char; do
    if [ "$t" = "4mer" ]; then
      for s in 0 1; do
        python -m pilot2.run_pilot --tokenizer 4mer --objective ar --seed $s --gpu $G $A \
          > outputs/${D}_ar/4mer_ar_s$s.log 2>&1; log "$D ar 4mer s=$s done"
      done
    fi
    for o in mlm@0.15 mlm@0.5; do for s in 0 1; do
      python -m pilot2.run_pilot --tokenizer $t --objective $o --seed $s --gpu $G $M \
        > outputs/${D}_mlm/${t}_${o/@/}_s$s.log 2>&1; log "$D mlm $t $o s=$s done"
    done; done
  done
  python -m pilot2.analyze_objaxis --root outputs/${D}_ar outputs/${D}_mlm --data $D --epoch 30 \
    --name ${D}30 > outputs/${D}_mlm/objaxis.log 2>&1
  python -m pilot2.analyze_traj --root outputs/${D}_ar outputs/${D}_mlm > outputs/${D}_mlm/traj.log 2>&1
  log "$D done"
}

arm yeast 0 &
arm gue 3 &
wait
log "Q1010C_DONE"
