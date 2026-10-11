#!/bin/bash
# 10 Oct, the one gap the paper audit found. The tokeniser claim is stated for all five datasets, but
# at MATCHED HELD-OUT LOSS it can only be made on E. coli and human: on synthetic, yeast and GUE the
# 30-round next-token runs have no common overfitting band, because the character cell barely overfits
# there (it tops out at 2.000-2.001 bits where the 6-mer reaches 2.5 and the 3-mer 4.0, and BPE does
# not start until 2.047). With no overlap there is nothing to interpolate onto, so analyze_matched
# correctly refuses.
#
# The fix is more rounds, not more models: 150 rounds on those three datasets, exactly the schedule
# the human delay arm used, so every cell reaches the band the others pass through. 30 runs, and the
# cheap ones at that -- a 30-round character AR cell takes about two minutes on these datasets, and AR
# scoring is one forward pass per probe rather than the per-position PLL the masked cells pay.
#
# Everything else in the audit was already covered: BPE exists on all five datasets, spaced k-mers
# (len_sp) cover the length conjecture, off1/rope_rand cover placement, and the masked column is
# near-matched by construction (all cells within 0.05-0.17 bits on the same budget).
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1010e.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/synthetic_long outputs/yeast_long outputs/gue_long
log "start"

# each dataset's own next-token arguments, with the 150-round schedule of queue_1009b branch A
E150="--n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --score_snapshots --epochs 150 --save_epochs 20,30,50,80,110,150"

cell(){                 # $1 dataset  $2 tokenizer  $3 seed  $4 gpu
  local D=$1 O=outputs/$1_long EXTRA=""
  [ "$1" != "synthetic" ] && EXTRA="--data $1"
  python -m pilot2.run_pilot --tokenizer $2 --objective ar --seed $3 --gpu $4 $E150 $EXTRA --out $O \
    > $O/$2_ar_s$3.log 2>&1; log "$1 $2 s=$3 done"
}

bpe(){                  # $1 dataset  $2 seed  $3 gpu
  local O=outputs/$1_long EXTRA=""
  [ "$1" != "synthetic" ] && EXTRA="--data $1"
  python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_gue.json --seed $2 --gpu $3 \
    --n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 \
    --probe_offset random --epochs 150 --save_epochs 20,30,50,80,110,150 $EXTRA --out $O \
    > $O/bpe_s$2.log 2>&1; log "$1 bpe s=$2 done"
}

# one dataset per GPU for the slow character and 3-mer cells; the 4-mer and 6-mer cells are fast
# enough to share a card
( for s in 0 1; do cell synthetic char $s 0; done
  for s in 0 1; do cell synthetic 3mer $s 0; done
  for s in 0 1; do bpe synthetic $s 0; done ) &
( for s in 0 1; do cell yeast char $s 1; done
  for s in 0 1; do cell yeast 3mer $s 1; done
  for s in 0 1; do bpe yeast $s 1; done ) &
( for s in 0 1; do cell gue char $s 2; done
  for s in 0 1; do cell gue 3mer $s 2; done
  for s in 0 1; do bpe gue $s 2; done ) &
( for d in synthetic yeast gue; do for t in 4mer 6mer; do for s in 0 1; do cell $d $t $s 3; done; done; done ) &
wait

for d in synthetic yeast gue; do
  python -m pilot2.analyze_matched --root outputs/${d}_long --name ${d}_long --tiers 1,16 \
    > outputs/${d}_long/matched.log 2>&1
  python -m pilot2.analyze_traj --root outputs/${d}_long > outputs/${d}_long/traj.log 2>&1
done
log "Q1010E_DONE"
