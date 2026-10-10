#!/bin/bash
# Definitive human-canary arm: real fresh hosts for the controls (the earlier passes scored non-members
# inside random DNA, which confounds membership with host type), three seeds for error bars, and the
# matched-utility analysis Erman asked for. Six published models, 50 rounds, 50 canaries per tier.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_human3.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_real3
until grep -q SEEDS12B_DONE outputs/queue_seeds12b.log 2>/dev/null; do sleep 120; done
log "start"
R="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real3"
B2="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real3"
HY="--model hyenadna-medium-160k-seqlen-hf --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --snapshot_probes 50 --score_epoch0 --probe_offset random --out outputs/human_real3"
( for s in 0 1 2; do python -m pilot2.dnabert --k 3 --seed $s --gpu 0 $R > outputs/human_real3/k3_s$s.log 2>&1; log "k=3 s=$s done"; done
  for s in 0 1; do python -m pilot2.dnabert2 --seed $s --gpu 0 $B2 > outputs/human_real3/bpe_s$s.log 2>&1; log "dnabert2 s=$s done"; done ) &
( for s in 0 1 2; do python -m pilot2.dnabert --k 4 --seed $s --gpu 1 $R > outputs/human_real3/k4_s$s.log 2>&1; log "k=4 s=$s done"; done
  for s in 0 1; do python -m pilot2.hyena --seed $s --gpu 1 $HY > outputs/human_real3/hyena_s$s.log 2>&1; log "hyena s=$s done"; done ) &
( for s in 0 1 2; do python -m pilot2.dnabert --k 5 --seed $s --gpu 2 $R > outputs/human_real3/k5_s$s.log 2>&1; log "k=5 s=$s done"; done
  python -m pilot2.dnabert2 --seed 2 --gpu 2 $B2 > outputs/human_real3/bpe_s2.log 2>&1; log "dnabert2 s=2 done" ) &
( for s in 0 1 2; do python -m pilot2.dnabert --k 6 --seed $s --gpu 3 $R > outputs/human_real3/k6_s$s.log 2>&1; log "k=6 s=$s done"; done
  python -m pilot2.hyena --seed 2 --gpu 3 $HY > outputs/human_real3/hyena_s2.log 2>&1; log "hyena s=2 done" ) &
wait
python -m pilot2.analyze_real --root outputs/human_real3 --name human3 > outputs/human_real3/analysis.log 2>&1
python -m pilot2.analyze_human --root outputs/human_real3 --canary_npz $H --name human3 > outputs/human_real3/human_analysis.log 2>&1
python -m pilot2.analyze_matched --root outputs/human_real3 --name human3 > outputs/human_real3/matched.log 2>&1
log "HUMAN3_DONE"
