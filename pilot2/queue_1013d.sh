#!/bin/bash
# 13 Oct. The released tokenisation panel, with the weights kept this time.
#
# CORRECTING MYSELF. I wrote that a released checkpoint cannot be used to vary tokenisation. That is
# wrong: DNABERT ships FOUR pretrained models, k=3, 4, 5 and 6, and all four are on this machine
# (/data/wh/yqdata/models/DNABERT/DNA_bert_{3,4,5,6}). So the tokeniser axis does exist among
# released models, we have already measured it with the standard protocol, and it has to be measured
# with the new decoder too.
#
# BUT THE DECODER DOES NOT TRANSFER UNCHANGED, AND THAT IS THE INTERESTING PART. DNABERT's k-mers
# OVERLAP: a 288-nt window becomes ~283 tokens whatever k is, and neighbouring tokens share k-1
# nucleotides. Two consequences:
#   - Re-masking ONE token and leaving its neighbours is degenerate. Five of a 6-mer's six letters
#     are still visible in the adjacent tokens, so the model reconstructs it from context alone and
#     a leave-one-out accuracy near 1.00 would mean nothing at all.
#   - Hiding 48 nucleotides requires masking every token that overlaps them, i.e. 48 + (k-1) tokens,
#     which is about 48 FOR EVERY k. The joint-slot count is pinned to the nucleotide count.
# Our mechanism claim is that the number of joint slots sets the price of recovery: 8 slots for the
# non-overlapping 6-mer against 16 for the 3-mer, which is 95 % against 0 %. If that claim is right,
# then DNABERT k=3..6 should show NO comparable spread, because every k has the same ~48 slots. So
# the released DNABERT family is the NEGATIVE CONTROL for the mechanism and NT, whose 4096
# non-overlapping 6-mers are exactly our own axis, is the positive case. A flat profile across
# DNABERT's k beside a 0-to-95 split on the non-overlapping axis is stronger evidence for the
# mechanism than either alone.
#
# The correct analogue of the decoder here is one NUCLEOTIDE at a time rather than one token: re-mask
# every token covering a single position, let the model fill them, read that nucleotide, sweep. That
# is implemented separately; this queue produces the checkpoints it needs, because until today every
# DNABERT run deleted its weights after scoring and so could never be asked at all.
#
# 150 rounds with snapshots throughout: these models are pretrained, so they should memorise sooner
# than our from-scratch backbone needed 300 rounds to, and the kept snapshots let the decoder be run
# at every round without retraining.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1013d.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/dnabert_long
log "start"

# the masked configuration the family was already measured with (Sec. 3.13), extended in rounds, and
# --mask_nt_rate fixes the fraction of hidden NUCLEOTIDES so the pressure is comparable across k
A="--objective mlm --mask_nt_rate 0.05 --lr 1e-4 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --epochs 150 --save_epochs 15,30,50,80,120,150 --stride 3 --out outputs/dnabert_long"

for pair in "3 2" "4 3"; do
  set -- $pair
  ( run "dnabert k=$1 ecoli" python -m pilot2.dnabert --k $1 --data ecoli --seed 0 --gpu $2 $A \
      > outputs/dnabert_long/k$1_ecoli.log 2>&1 ) &
done
wait
for pair in "5 2" "6 3"; do
  set -- $pair
  ( run "dnabert k=$1 ecoli" python -m pilot2.dnabert --k $1 --data ecoli --seed 0 --gpu $2 $A \
      > outputs/dnabert_long/k$1_ecoli.log 2>&1 ) &
done
wait
log "ecoli panel done"

# chromosome 22, where the canaries are real rare haplotype segments
for pair in "3 2" "6 3"; do
  set -- $pair
  ( run "dnabert k=$1 chr22" python -m pilot2.dnabert --k $1 --data human \
      --canary_npz $H/canaries_chr22.npz --seed 0 --gpu $2 $A \
      > outputs/dnabert_long/k$1_human.log 2>&1 ) &
done
wait
log "chr22 pair done"

# DNABERT-2's BPE is NON-overlapping, so the token-level decoder applies to it unchanged, which
# makes it the second positive case beside NT
run "dnabert2 bpe ecoli" python -m pilot2.dnabert2 --data ecoli --seed 0 --gpu 2 \
  --objective mlm --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --epochs 150 \
  --save_epochs 15,30,50,80,120,150 --out outputs/dnabert_long \
  > outputs/dnabert_long/bpe_ecoli.log 2>&1
du -sh outputs/dnabert_long >> $L
log Q1013D_DONE
