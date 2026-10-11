#!/bin/bash
# 11 Oct, arm A: does the effect need a planted record at all?
#
# Every number in the paper comes from canaries we inserted, and the sharpest objection to all of it
# is that insertion is the effect rather than repetition. Real genomes repeat sequence by themselves,
# so the objection is testable: find the 96-nt blocks that chromosome 22 repeats naturally, score
# them with the paper's rulers, and compare against single-occurrence blocks from the same corpus.
#
# The smoke test showed what the experiment needs. On 5000 windows the model memorises its training
# set wholesale -- singletons come back at 100 % extraction, so there is no contrast to measure --
# and E. coli has no exact 96-nt repeats at all (85,000 blocks, every one unique). Both are fixed by
# the corpus: chromosome 22 at 60,000 windows (17 Mb) holds 2,235 blocks that occur twice, 1,245
# three or four times, 717 five to eight and 68 nine or more, and at that size the model is far
# enough above capacity that it cannot store everything. That is the regime in which "what gets
# stored" is a question with an answer.
#
# The planted canaries stay in the training set, so the same runs let the two populations be read
# against each other: a block the corpus repeats 9+ times against a record we inserted 16 times.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_1011c.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_big
until grep -q Q1011B_DONE outputs/queue_1011b.log 2>/dev/null; do sleep 180; done
log "start"

T="--data human --canary_npz $H --n_train 60000 --n_val 500 --n_test 500 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --epochs 30 --objective ar"

( python -m pilot2.run_pilot --tokenizer char --seed 0 --gpu 0 $T --out outputs/human_big \
    > outputs/human_big/char_ar_s0.log 2>&1; log "char done" ) &
( python -m pilot2.run_pilot --tokenizer 3mer --seed 0 --gpu 1 $T --out outputs/human_big \
    > outputs/human_big/3mer_ar_s0.log 2>&1; log "3mer done" ) &
( python -m pilot2.run_pilot --tokenizer 4mer --seed 0 --gpu 2 $T --out outputs/human_big \
    > outputs/human_big/4mer_ar_s0.log 2>&1; log "4mer done" ) &
( python -m pilot2.run_pilot --tokenizer 6mer --seed 0 --gpu 3 $T --out outputs/human_big \
    > outputs/human_big/6mer_ar_s0.log 2>&1; log "6mer done" ) &
wait
log "training done, scoring natural duplicates"

python -m pilot2.natural_dups --root outputs/human_big --gpu 0 --max_rows 60000 --per_bin 40 \
  --name human_big > outputs/human_big/natural.log 2>&1
log "Q1011C_DONE"
