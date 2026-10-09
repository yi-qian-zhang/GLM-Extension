#!/bin/bash
# Seeds 1 and 2 for yeast and GUE real-model runs (DNABERT 3/4/5/6 causal, DNABERT-2 BPE causal, HyenaDNA medium), no downstream
# probe (seed 0 carries it). Waits for queue ds2 to finish.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
log(){ echo "$(date +%H:%M) $*" >> outputs/queue_seeds.log; }
until grep -q DS2_DONE outputs/queue_ds2.log 2>/dev/null; do sleep 120; done
log "start"
R="--objective causal --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random"
H="--model hyenadna-medium-160k-seqlen-hf --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random"
run_k(){ python -m pilot2.dnabert --k $1 --seed $2 --gpu $3 --data $4 --out outputs/dnabert_$4 $R --stride 3 > outputs/dnabert_$4/k$1_s$2.log 2>&1; log "$4 k=$1 s=$2 done"; }
run_b(){ python -m pilot2.dnabert2 --seed $1 --gpu $2 --data $3 --out outputs/dnabert_$3 $R > outputs/dnabert_$3/bpe_s$1.log 2>&1; log "$3 bpe s=$1 done"; }
run_h(){ python -m pilot2.hyena --seed $1 --gpu $2 --data $3 --out outputs/hyena_$3 $H > outputs/hyena_$3/medium_s$1.log 2>&1; log "$3 hyena s=$1 done"; }
( for s in 1 2; do run_k 3 $s 0 yeast; run_k 3 $s 0 gue; run_b $s 0 yeast; done ) &
( for s in 1 2; do run_k 4 $s 1 yeast; run_k 4 $s 1 gue; run_h $s 1 yeast; done ) &
( for s in 1 2; do run_k 5 $s 2 yeast; run_k 5 $s 2 gue; run_b $s 2 gue; done ) &
( for s in 1 2; do run_k 6 $s 3 yeast; run_k 6 $s 3 gue; run_h $s 3 gue; done ) &
wait
python -m pilot2.analyze_real --root outputs/dnabert_yeast outputs/hyena_yeast --name yeast > outputs/dnabert_yeast/analysis.log 2>&1
python -m pilot2.analyze_real --root outputs/dnabert_gue outputs/hyena_gue --name gue > outputs/dnabert_gue/analysis.log 2>&1
log "SEEDS_DONE"
