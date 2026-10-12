#!/bin/bash
# 12 Oct. The experiment that decides how the paper's headline claim is phrased.
#
# WHAT queue_1011h SETTLED. Our masked cells were reported as "0 % extraction at every snapshot",
# and the worry was that this only reflected the 30-round budget: their held-out loss was still
# improving, so they had never entered the overfitting regime at all. Pushed to 150 rounds on human
# chromosome 22 they now go far past it (3-mer floor 1.675 -> 2.074, 6-mer 1.828 -> 2.176, both
# worse than the 2.000 chance level), and by the other two rulers they are thoroughly memorised:
# r=16 canary surprise falls to 0.12 bits/nt and rank-1 reaches 0.98 (3-mer) and 1.00 (6-mer, at
# EVERY tier including a single insertion). Verbatim extraction is 0.00 in all 30 cells. So the
# budget explanation is dead: a masked model can hold a record well enough to pick one copy of it
# out of a hundred candidates and still never emit it.
#
# WHAT IS STILL OPEN. The Nucleotide Transformer, 250M parameters, the same masked objective and
# OUR OWN extraction code, reaches 28 % on E. coli and 18 % on human. That also rules out a broken
# scorer -- the same code path does produce exact matches -- so the dissociation is real, and the
# remaining candidates are the two things NT has and our backbone does not: scale (250M against
# 12.6M) and a pretrained prior. NT confounds them. This arm separates them.
#
#   stage 1  scale, from scratch: 59.9M (768/8/12) and 201M (1024/16/16), both tokenisers, 150
#            rounds, to be read against the 12.6M cells queue_1011h already has. A CAUSAL cell at
#            each size and tokeniser runs beside each masked one, because without it a reviewer can
#            answer "everything extracts at 201M" and we could not contradict them.
#   stage 2  the prior: masked pretraining on 60,000 chromosome-21 windows, then the same 150-round
#            fine-tune on chromosome 22. Masked only -- the question is whether a prior turns masked
#            extraction on, not whether it changes the causal side, which Sec. 5 already measures.
#
# Everything matches queue_1011h exactly except the knob under test (same probe counts, pool, floor
# sample, random offsets, snapshot rounds, and the default absolute position encoding), so the new
# cells can be read directly against the 12.6M ones.
#
# Note on logging: queue_1011e and _1011f recorded "done" for two cells that had in fact died (NT
# 500M had no weights on disk, the GUE cell was killed to free a card), because log() ran whatever
# the exit status was. run() below records the status.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1012a.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/scale_long outputs/pretrain21_mlm outputs/ft22_mlm_long
log "start"

S59="--d_model 768  --n_layers 8  --n_heads 12"
S201="--d_model 1024 --n_layers 16 --n_heads 16"
# identical to queue_1011h's T, minus --out and --objective
T="--data human --canary_npz $H/canaries_chr22.npz --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --score_snapshots --epochs 150 --save_epochs 30,50,80,110,150"

# ---- stage 1: scale from scratch, masked then causal -------------------------------------------
for obj in mlm@0.15 ar; do
  o=${obj%%@*}
  ( run "s59 3mer $obj"  python -m pilot2.run_pilot --tokenizer 3mer --objective $obj --seed 0 --gpu 0 \
      $T $S59  --out outputs/scale_long/s59  > outputs/scale_long/s59_3mer_$o.log  2>&1 ) &
  ( run "s59 6mer $obj"  python -m pilot2.run_pilot --tokenizer 6mer --objective $obj --seed 0 --gpu 1 \
      $T $S59  --out outputs/scale_long/s59  > outputs/scale_long/s59_6mer_$o.log  2>&1 ) &
  ( run "s201 3mer $obj" python -m pilot2.run_pilot --tokenizer 3mer --objective $obj --seed 0 --gpu 2 \
      $T $S201 --out outputs/scale_long/s201 > outputs/scale_long/s201_3mer_$o.log 2>&1 ) &
  ( run "s201 6mer $obj" python -m pilot2.run_pilot --tokenizer 6mer --objective $obj --seed 0 --gpu 3 \
      $T $S201 --out outputs/scale_long/s201 > outputs/scale_long/s201_6mer_$o.log 2>&1 ) &
  wait
  log "stage1 $obj done"
done
python -m pilot2.analyze_traj --root outputs/scale_long/s59  > outputs/scale_long/traj_s59.log  2>&1
python -m pilot2.analyze_traj --root outputs/scale_long/s201 > outputs/scale_long/traj_s201.log 2>&1
log "stage1 analysed"

# ---- stage 2: the pretrained prior, masked ------------------------------------------------------
# chromosome 21, no canaries: the backbone gets what every released checkpoint has and ours never did
PRE="--data human --fasta $H/chr21.fa --n_train 60000 --n_val 500 --n_test 500 --probes_per_tier 2 --n_nonmember 2 --pool 50 --floor_n 300 --probe_offset random --objective mlm@0.15 --epochs 10"
( run "pre small 3mer" python -m pilot2.run_pilot --tokenizer 3mer --seed 0 --gpu 0 $PRE \
    --out outputs/pretrain21_mlm/small > outputs/pretrain21_mlm/small_3mer.log 2>&1 ) &
( run "pre small 6mer" python -m pilot2.run_pilot --tokenizer 6mer --seed 0 --gpu 1 $PRE \
    --out outputs/pretrain21_mlm/small > outputs/pretrain21_mlm/small_6mer.log 2>&1 ) &
( run "pre big 3mer"   python -m pilot2.run_pilot --tokenizer 3mer --seed 0 --gpu 2 $PRE $S201 \
    --out outputs/pretrain21_mlm/big   > outputs/pretrain21_mlm/big_3mer.log 2>&1 ) &
( run "pre big 6mer"   python -m pilot2.run_pilot --tokenizer 6mer --seed 0 --gpu 3 $PRE $S201 \
    --out outputs/pretrain21_mlm/big   > outputs/pretrain21_mlm/big_6mer.log 2>&1 ) &
wait
log "stage2 pretrain done"

# fine-tune each pretrained checkpoint for 150 rounds on chromosome 22, canaries planted
ft(){ # $1 tag  $2 tokenizer  $3 checkpoint  $4 gpu  $5.. size flags
  local tag=$1 tok=$2 ck=$3 gpu=$4; shift 4
  if [ -f "$ck" ]; then
    run "ft $tag" python -m pilot2.run_pilot --tokenizer $tok --objective mlm@0.15 --seed 0 --gpu $gpu \
      $T "$@" --init_from "$ck" --out outputs/ft22_mlm_long/$tag \
      > outputs/ft22_mlm_long/$tag.log 2>&1
  else
    log "MISSING $ck ($tag)"
  fi
}
( ft small_3mer 3mer outputs/pretrain21_mlm/small/3mer_mlm0.15_s0/final.pt 0 ) &
( ft small_6mer 6mer outputs/pretrain21_mlm/small/6mer_mlm0.15_s0/final.pt 1 ) &
( ft big_3mer   3mer outputs/pretrain21_mlm/big/3mer_mlm0.15_s0/final.pt   2 $S201 ) &
( ft big_6mer   6mer outputs/pretrain21_mlm/big/6mer_mlm0.15_s0/final.pt   3 $S201 ) &
wait
for d in outputs/ft22_mlm_long/*/; do
  python -m pilot2.analyze_traj --root "$d" > "${d%/}_traj.log" 2>&1
done
log "Q1012A_DONE"
