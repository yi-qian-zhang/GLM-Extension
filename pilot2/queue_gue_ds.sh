#!/bin/bash
# GUE rerun with the downstream promoter probe at every snapshot (DNABERT k=3..6 causal, DNABERT-2 BPE causal, HyenaDNA medium)
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
log(){ echo "$(date +%H:%M) $*" >> outputs/queue_gue_ds.log; }
R="--objective causal --data gue --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --downstream"
H="--model hyenadna-medium-160k-seqlen-hf --data gue --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random --downstream"
( python -m pilot2.dnabert --k 3 --seed 0 --gpu 0 --out outputs/dnabert_gue_ds $R --stride 3 > outputs/dnabert_gue_ds/k3_s0.log 2>&1; log "gue_ds k=3 done"
  python -m pilot2.dnabert2 --seed 0 --gpu 0 --out outputs/dnabert_gue_ds $R > outputs/dnabert_gue_ds/bpe_s0.log 2>&1; log "gue_ds bpe done" ) &
( python -m pilot2.dnabert --k 4 --seed 0 --gpu 1 --out outputs/dnabert_gue_ds $R --stride 3 > outputs/dnabert_gue_ds/k4_s0.log 2>&1; log "gue_ds k=4 done"
  python -m pilot2.hyena --seed 0 --gpu 1 --out outputs/hyena_gue_ds $H > outputs/hyena_gue_ds/medium_s0.log 2>&1; log "gue_ds hyena done" ) &
( python -m pilot2.dnabert --k 5 --seed 0 --gpu 2 --out outputs/dnabert_gue_ds $R --stride 3 > outputs/dnabert_gue_ds/k5_s0.log 2>&1; log "gue_ds k=5 done" ) &
( python -m pilot2.dnabert --k 6 --seed 0 --gpu 3 --out outputs/dnabert_gue_ds $R --stride 3 > outputs/dnabert_gue_ds/k6_s0.log 2>&1; log "gue_ds k=6 done" ) &
wait
python -m pilot2.analyze_real --root outputs/dnabert_gue_ds outputs/hyena_gue_ds --name gue_ds > outputs/dnabert_gue_ds/analysis.log 2>&1
log "GUE_DS_DONE"
