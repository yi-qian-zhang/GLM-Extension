#!/bin/bash
# 10 Oct: re-draw the member/non-member canary split.
#
# Why. Which canaries are members and which are controls is fixed by --data_seed, so in every arm so far
# it is the SAME split for every model and every model seed. With real human haplotype canaries the two
# groups of 50 segments differ by chance (GC, repeat content, variant count) and the pretrained models
# read the member group 0.30-0.45 bits/nt easier at round 0, before any fine-tuning. Averaging over
# model seeds cannot remove that; only re-drawing the split can. Subtracting each cell's round-0 excess
# (now the default in analyze_matched) is a correction, not a measurement.
#
# What. The six released models on chromosome 22, exactly the human_real3 configuration, with the split
# re-drawn three times (data_seed 2345 / 3456 / 4567), one model seed each. Together with human_real3
# (data_seed 1234) that gives four independent splits, so the chr22 ordering can be stated with an
# across-split spread instead of a single draw.
#
# Each root holds one split, because run directory names do not encode data_seed; analyze_matched takes
# several roots and treats same-named cells as repeats, which is the averaging we want.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_dseed.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
log "start"

# identical to queue_human3.sh apart from --data_seed and --out
R="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random"
B2="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random"
HY="--model hyenadna-medium-160k-seqlen-hf --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --snapshot_probes 50 --score_epoch0 --probe_offset random"

# one GPU per split: a dead GPU then costs one split, not one model across all splits
run_split(){            # $1 data_seed   $2 gpu
  local D=$1 G=$2 O=outputs/human_ds$1
  mkdir -p $O
  for k in 3 4 5 6; do
    python -m pilot2.dnabert --k $k --seed 0 --gpu $G --data_seed $D --out $O $R \
      > $O/k${k}.log 2>&1; log "ds=$D k=$k done"
  done
  python -m pilot2.dnabert2 --seed 0 --gpu $G --data_seed $D --out $O $B2 \
    > $O/bpe.log 2>&1; log "ds=$D dnabert2 done"
  python -m pilot2.hyena --seed 0 --gpu $G --data_seed $D --out $O $HY \
    > $O/hyena.log 2>&1; log "ds=$D hyena done"
}

run_split 2345 0 &
run_split 3456 2 &
run_split 4567 3 &
wait

ROOTS="outputs/human_ds2345 outputs/human_ds3456 outputs/human_ds4567"
python -m pilot2.analyze_matched --root $ROOTS --name human_ds > outputs/human_ds2345/matched.log 2>&1
python -m pilot2.analyze_matched --root $ROOTS --name human_ds_raw --raw > outputs/human_ds2345/matched_raw.log 2>&1
python -m pilot2.analyze_matched --root outputs/human_real3 $ROOTS --name human_all > outputs/human_ds2345/matched_all.log 2>&1
python -m pilot2.analyze_real --root $ROOTS --name human_ds > outputs/human_ds2345/analysis.log 2>&1
python -m pilot2.analyze_human --root $ROOTS --canary_npz $H --name human_ds > outputs/human_ds2345/human.log 2>&1
log "DSEED_DONE"
