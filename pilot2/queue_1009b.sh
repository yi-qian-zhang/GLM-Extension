#!/bin/bash
# 9 Oct evening: close the two holes the completed runs leave in the mitigation section.
#   A  does the character tokeniser only DELAY leakage? 150 rounds instead of 30, real human canaries.
#      Without this we can only say "no leakage in 30 rounds"; with it we can say "delays it by Nx".
#   B  the objective axis on REAL HUMAN data. Everything masked so far is synthetic or E. coli, yet the
#      mitigation section recommends a masked objective, so it needs human evidence.
#   C  the released k-mer family under its own masked objective at equal hidden-nucleotide rate, on
#      human data: the objective claim for published models rather than for our backbone.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_1009b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_long outputs/human_mlm outputs/human_dnabert_mlm
log "start"

T="--data human --canary_npz $H --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --score_snapshots"

# A: character tokeniser, 150 rounds, two seeds (GPU 0)
( for s in 0 1; do
    python -m pilot2.run_pilot --tokenizer char --objective ar --seed $s --gpu 0 $T \
      --epochs 150 --save_epochs 20,30,50,80,110,150 --out outputs/human_long \
      > outputs/human_long/char_ar_s$s.log 2>&1; log "long char ar s=$s done"
  done
  # the 6-mer at 150 rounds as the reference curve it has to be compared against
  python -m pilot2.run_pilot --tokenizer 6mer --objective ar --seed 0 --gpu 0 $T \
    --epochs 150 --save_epochs 20,30,50,80,110,150 --out outputs/human_long \
    > outputs/human_long/6mer_ar_s0.log 2>&1; log "long 6mer ar s=0 done" ) &

# B: objective axis on human, our backbone (GPU 1 and 2)
( for s in 0 1; do for o in mlm@0.15 mlm@0.50; do
    python -m pilot2.run_pilot --tokenizer char --objective $o --seed $s --gpu 1 $T \
      --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --out outputs/human_mlm \
      > outputs/human_mlm/char_${o/@/}_s$s.log 2>&1; log "mlm char $o s=$s done"
  done; done ) &
( for s in 0 1; do for o in mlm@0.15 mlm@0.50; do
    python -m pilot2.run_pilot --tokenizer 6mer --objective $o --seed $s --gpu 2 $T \
      --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --out outputs/human_mlm \
      > outputs/human_mlm/6mer_${o/@/}_s$s.log 2>&1; log "mlm 6mer $o s=$s done"
  done; done
  for s in 0 1; do for o in mlm@0.15 mlm@0.50; do
    python -m pilot2.run_pilot --tokenizer 3mer --objective $o --seed $s --gpu 2 $T \
      --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --out outputs/human_mlm \
      > outputs/human_mlm/3mer_${o/@/}_s$s.log 2>&1; log "mlm 3mer $o s=$s done"
  done; done ) &

# C: released DNABERT under its native masked objective at equal hidden-nucleotide rate (GPU 3)
( for k in 3 4 5 6; do
    python -m pilot2.dnabert --k $k --seed 0 --gpu 3 --objective mlm --mask_nt_rate 0.05 --lr 1e-4 \
      --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 \
      --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random \
      --out outputs/human_dnabert_mlm > outputs/human_dnabert_mlm/k${k}_s0.log 2>&1
    log "dnabert mlm k=$k done"
  done ) &
wait
python -m pilot2.analyze_traj --root outputs/human_long > outputs/human_long/traj.log 2>&1
python -m pilot2.analyze_human --root outputs/human_long --canary_npz $H --name human_long > outputs/human_long/human.log 2>&1
python -m pilot2.analyze_traj --root outputs/human_mlm outputs/human_toy > outputs/human_mlm/traj.log 2>&1
python -m pilot2.analyze_human --root outputs/human_mlm --canary_npz $H --name human_mlm > outputs/human_mlm/human.log 2>&1
python -m pilot2.analyze_dnabert --root outputs/human_dnabert_mlm > outputs/human_dnabert_mlm/analysis.log 2>&1
python -m pilot2.analyze_human --root outputs/human_dnabert_mlm --canary_npz $H --name human_dnabert_mlm > outputs/human_dnabert_mlm/human.log 2>&1
log "Q1009B_DONE"
