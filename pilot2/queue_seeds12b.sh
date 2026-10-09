#!/bin/bash
# Remaining extra seeds for the yeast / GUE real-model arms, moved behind the human-canary phase
# (the seed-1 yeast k-mer runs were already in flight when queue_seeds12.sh was stopped at 08:45).
# Order per GPU: seed 1 BPE / HyenaDNA, then all of seed 2.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_seeds12b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
until grep -q NIGHT1009_DONE outputs/queue_night1009.log 2>/dev/null; do sleep 120; done
log "start"
R="--objective causal --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --downstream"
H="--model hyenadna-medium-160k-seqlen-hf --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random --downstream"
run_k(){ python -m pilot2.dnabert --k $1 --seed $2 --gpu $3 --data $4 --out outputs/dnabert_$4_ds $R --stride 3 > outputs/dnabert_$4_ds/k$1_s$2.log 2>&1; log "$4 k=$1 s=$2 done"; }
run_b(){ python -m pilot2.dnabert2 --seed $1 --gpu $2 --data $3 --out outputs/dnabert_$3_ds $R > outputs/dnabert_$3_ds/bpe_s$1.log 2>&1; log "$3 bpe s=$1 done"; }
run_h(){ python -m pilot2.hyena --seed $1 --gpu $2 --data $3 --out outputs/hyena_$3_ds $H > outputs/hyena_$3_ds/medium_s$1.log 2>&1; log "$3 hyena s=$1 done"; }
( run_b 1 0 gue;   for k in 3; do run_k $k 2 0 gue; run_k $k 2 0 yeast; done; run_b 2 0 gue ) &
( run_b 1 1 yeast; for k in 4; do run_k $k 2 1 gue; run_k $k 2 1 yeast; done; run_b 2 1 yeast ) &
( run_h 1 2 gue;   for k in 5; do run_k $k 2 2 gue; run_k $k 2 2 yeast; done; run_h 2 2 gue ) &
( run_h 1 3 yeast; for k in 6; do run_k $k 2 3 gue; run_k $k 2 3 yeast; done; run_h 2 3 yeast ) &
wait
python -m pilot2.analyze_real --root outputs/dnabert_gue_ds outputs/hyena_gue_ds --name gue_ds > outputs/dnabert_gue_ds/analysis.log 2>&1
python -m pilot2.analyze_real --root outputs/dnabert_yeast_ds outputs/hyena_yeast_ds --name yeast_ds > outputs/dnabert_yeast_ds/analysis.log 2>&1
python -m pilot2.analyze_real --root outputs/dnabert_gue_ds2 outputs/hyena_gue_ds2 --name gue_wide > outputs/dnabert_gue_ds2/analysis.log 2>&1
log "SEEDS12B_DONE"
