#!/bin/bash
# 11 Oct. Two of the four robustness arms a reviewer will ask for. Both on E. coli, which is the one
# dataset whose 30-round cells already share an overfitting band, so matched-utility reading needs no
# extra budget.
#
# C  MATCHED COMPUTE. Every comparison in the paper is at matched data and matched rounds, and a
#    character model processes 288 token slots per window where the 6-mer processes 48. Here the
#    round count is set so that every cell processes the SAME number of token slots as the 6-mer at
#    30 rounds (30 x 5000 x 48 = 7.2M): char 5 rounds, 3-mer 15, 4-mer 20, 6-mer 30. The wall clock
#    of each cell is recorded in its train_summary, so the same runs also answer the harsher version
#    of the question (attention is quadratic in the slot count, so equal slots is not equal seconds).
#
# D  SCALE. The controlled grid is a 12.9M backbone and the released models reach 117M, so the
#    obvious question is whether the ordering is a small-model artefact. This arm repeats the grid at
#    d=768, 8 layers, 12 heads: 59.9M parameters, 56.7M of them non-embedding, 4.5x the backbone the
#    paper uses. Next-token at two seeds, masked at one, because PLL scoring costs one forward pass
#    per masked position and is what makes the masked cells slow.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1011a.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/ecoli_mc outputs/ecoli_big
log "start"

BASE="--data ecoli --n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random"
BIG="--d_model 768 --n_layers 8 --n_heads 12"

# ---- C: equal token slots processed (GPU 0)
( for s in 0 1; do
    for cell in "char 5" "3mer 15" "4mer 20" "6mer 30"; do
      set -- $cell
      python -m pilot2.run_pilot --tokenizer $1 --objective ar --seed $s --gpu 0 $BASE \
        --epochs $2 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/ecoli_mc \
        > outputs/ecoli_mc/$1_ar_s$s.log 2>&1
      log "mc $1 ($2 rounds) s=$s done"
    done
  done ) &

# ---- D: the same grid at 59.9M (GPUs 1-3)
( for s in 0 1; do for t in char 3mer; do
    python -m pilot2.run_pilot --tokenizer $t --objective ar --seed $s --gpu 1 $BASE $BIG \
      --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/ecoli_big \
      > outputs/ecoli_big/${t}_ar_s$s.log 2>&1
    log "big $t ar s=$s done"
  done; done ) &
( for s in 0 1; do for t in 4mer 6mer; do
    python -m pilot2.run_pilot --tokenizer $t --objective ar --seed $s --gpu 2 $BASE $BIG \
      --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/ecoli_big \
      > outputs/ecoli_big/${t}_ar_s$s.log 2>&1
    log "big $t ar s=$s done"
  done; done ) &
( for t in 6mer 4mer 3mer char; do        # cheapest first: if this is cut short, char is the loss
    python -m pilot2.run_pilot --tokenizer $t --objective mlm@0.15 --seed 0 --gpu 3 $BASE $BIG \
      --epochs 30 --probes_per_tier 40 --n_nonmember 40 --pool 300 --out outputs/ecoli_big \
      > outputs/ecoli_big/${t}_mlm015_s0.log 2>&1
    log "big $t mlm@0.15 s=0 done"
  done ) &
wait

python -m pilot2.analyze_matched --root outputs/ecoli_mc --name ecoli_mc --tiers 1,16 > outputs/ecoli_mc/matched.log 2>&1
python -m pilot2.analyze_traj --root outputs/ecoli_mc > outputs/ecoli_mc/traj.log 2>&1
python -m pilot2.analyze_matched --root outputs/ecoli_big --name ecoli_big --tiers 1,16 > outputs/ecoli_big/matched.log 2>&1
python -m pilot2.analyze_objaxis --root outputs/ecoli_big --data ecoli --epoch 30 --name ecoli_big > outputs/ecoli_big/objaxis.log 2>&1
log "Q1011A_DONE"
