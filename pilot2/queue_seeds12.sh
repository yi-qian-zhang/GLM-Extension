#!/bin/bash
# Seeds 1 and 2 for the yeast and GUE real-model arms (with the default downstream tasks), one serial queue per GPU,
# sharing GPUs with tmux ds2. Joins the seed-0 dirs in outputs/{dnabert,hyena}_{gue,yeast}_ds.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
log(){ echo "$(date +%H:%M) $*" >> outputs/queue_seeds12.log; }
R="--objective causal --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --downstream"
H="--model hyenadna-medium-160k-seqlen-hf --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random --downstream"
run_k(){ python -m pilot2.dnabert --k $1 --seed $2 --gpu $3 --data $4 --out outputs/dnabert_$4_ds $R --stride 3 > outputs/dnabert_$4_ds/k$1_s$2.log 2>&1; log "$4 k=$1 s=$2 done"; }
run_b(){ python -m pilot2.dnabert2 --seed $1 --gpu $2 --data $3 --out outputs/dnabert_$3_ds $R > outputs/dnabert_$3_ds/bpe_s$1.log 2>&1; log "$3 bpe s=$1 done"; }
run_h(){ python -m pilot2.hyena --seed $1 --gpu $2 --data $3 --out outputs/hyena_$3_ds $H > outputs/hyena_$3_ds/medium_s$1.log 2>&1; log "$3 hyena s=$1 done"; }
log "start"
( for s in 1 2; do run_k 3 $s 0 gue; run_k 3 $s 0 yeast; run_b $s 0 gue; done ) &
( for s in 1 2; do run_k 4 $s 1 gue; run_k 4 $s 1 yeast; run_b $s 1 yeast; done ) &
( for s in 1 2; do run_k 5 $s 2 gue; run_k 5 $s 2 yeast; run_h $s 2 gue; done ) &
( for s in 1 2; do run_k 6 $s 3 gue; run_k 6 $s 3 yeast; run_h $s 3 yeast; done ) &
wait
python -m pilot2.analyze_real --root outputs/dnabert_gue_ds outputs/hyena_gue_ds --name gue_ds > outputs/dnabert_gue_ds/analysis.log 2>&1
python -m pilot2.analyze_real --root outputs/dnabert_yeast_ds outputs/hyena_yeast_ds --name yeast_ds > outputs/dnabert_yeast_ds/analysis.log 2>&1
log "SEEDS12_DONE"
