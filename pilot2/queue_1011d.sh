#!/bin/bash
# 11 Oct. The variable the predecessor study could not separate: FINE-TUNING STRATEGY.
#
# Nemecek et al. evaluate four models, and the headline is Evo -- 7B, StripedHyena, byte-level,
# adapted with LoRA -- recovering 100 % of planted canaries on all three real genomes even at a
# single insertion, where DNABERT-2 resists extraction entirely. Their own reading is that the
# pretrained parameters already hold the distribution, so a low-rank update has nothing to learn
# except the specific examples. But Evo differs from the rest of their panel in scale, architecture,
# tokenisation, objective AND fine-tuning strategy at once, so the explanation is a hypothesis, not a
# measurement. It also looks like a contradiction of our own result: Evo is byte-level, which is the
# finest tokenisation there is, and our grid says fine tokenisation memorises least.
#
# This arm isolates the one variable that is cheap to isolate. Two stages, same backbone throughout:
#   1. PRETRAIN on 60,000 chromosome-21 windows, no canaries, 10 rounds. This gives our backbone the
#      thing the released models have and ours never had: weights that already know the distribution.
#   2. FINE-TUNE each pretrained model on 5,000 chromosome-22 windows carrying the planted canaries,
#      once with all parameters and once with a LoRA adapter of rank 8 on qkv/proj/ff1/ff2 -- the
#      analogue of the ["Wqkv", "dense", "gated_layers", "wo"] set used for Evo -- with everything
#      else identical. RoPE throughout, because the fused in-projection of the default blocks is a
#      raw Parameter and cannot be adapted.
#
# If LoRA memorises more at matched utility, the predecessor's hypothesis holds and Evo's behaviour
# is about adaptation strategy rather than about byte-level tokenisation, which removes the apparent
# contradiction. If it memorises less, the contradiction is real and belongs in the discussion.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1011d.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/pretrain21 outputs/ft22
log "start"

PRE="--data human --fasta $H/chr21.fa --n_train 60000 --n_val 500 --n_test 500 --probes_per_tier 2 --n_nonmember 2 --pool 50 --floor_n 300 --probe_offset random --objective ar --pos_enc rope --epochs 10 --out outputs/pretrain21"
FT="--data human --canary_npz $H/canaries_chr22.npz --n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --objective ar --pos_enc rope --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/ft22"

# stage 1: two tokenisers, the two ends of the axis
( python -m pilot2.run_pilot --tokenizer char --seed 0 --gpu 0 $PRE > outputs/pretrain21/char.log 2>&1
  log "pretrain char done" ) &
( python -m pilot2.run_pilot --tokenizer 6mer --seed 0 --gpu 1 $PRE > outputs/pretrain21/6mer.log 2>&1
  log "pretrain 6mer done" ) &
wait

# stage 2: full against LoRA, from the same pretrained weights, two seeds each
for t in char 6mer; do
  CK=outputs/pretrain21/${t}_ar_s0/final.pt
  [ -f $CK ] || { log "MISSING $CK"; continue; }
  ( for s in 0 1; do
      python -m pilot2.run_pilot --tokenizer $t --seed $s --gpu 0 $FT --init_from $CK \
        > outputs/ft22/${t}_full_s$s.log 2>&1; log "ft $t full s=$s done"
    done ) &
  ( for s in 0 1; do
      python -m pilot2.run_pilot --tokenizer $t --seed $s --gpu 1 $FT --init_from $CK --lora_r 8 \
        > outputs/ft22/${t}_lora_s$s.log 2>&1; log "ft $t lora s=$s done"
    done ) &
  wait
done

python -m pilot2.analyze_matched --root outputs/ft22 --name ft22 --tiers 1,16 > outputs/ft22/matched.log 2>&1
python -m pilot2.analyze_traj --root outputs/ft22 > outputs/ft22/traj.log 2>&1
python -m pilot2.analyze_human --root outputs/ft22 --canary_npz $H/canaries_chr22.npz --name ft22 > outputs/ft22/human.log 2>&1
log "Q1011D_DONE"
