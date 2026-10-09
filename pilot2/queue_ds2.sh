#!/bin/bash
# Downstream-utility arms, queued behind tmux gue_ds: (A) GUE human-wide panel (prom_core_all, human_tf_0, splice) for
# DNABERT 3/4/5/6 causal + DNABERT-2 BPE + HyenaDNA; (B) yeast with histone-mark tasks emp_H3 + emp_H3K4me3, same six models.
# Starts only when outputs/DS2_GO exists (smoke test passed) and GUE_DS_DONE is logged.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
log(){ echo "$(date +%H:%M) $*" >> outputs/queue_ds2.log; }
until [ -f outputs/DS2_GO ] && grep -q GUE_DS_DONE outputs/queue_gue_ds.log 2>/dev/null; do sleep 60; done
log "start"
HW="prom_core_all,human_tf_0,splice_reconstructed"; YT="emp_H3,emp_H3K4me3"
R="--objective causal --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --downstream"
H="--model hyenadna-medium-160k-seqlen-hf --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random --downstream"
run_k(){ python -m pilot2.dnabert --k $1 --seed 0 --gpu $2 --data $3 --downstream_tasks $4 --out $5 $R --stride 3 > $5/k$1_s0.log 2>&1; log "$3 k=$1 done"; }
run_b(){ python -m pilot2.dnabert2 --seed 0 --gpu $1 --data $2 --downstream_tasks $3 --out $4 $R > $4/bpe_s0.log 2>&1; log "$2 bpe done"; }
run_h(){ python -m pilot2.hyena --seed 0 --gpu $1 --data $2 --downstream_tasks $3 --out $4 $H > $4/medium_s0.log 2>&1; log "$2 hyena done"; }
( run_k 3 0 gue $HW outputs/dnabert_gue_ds2; run_k 3 0 yeast $YT outputs/dnabert_yeast_ds; run_b 0 yeast $YT outputs/dnabert_yeast_ds ) &
( run_k 4 1 gue $HW outputs/dnabert_gue_ds2; run_k 4 1 yeast $YT outputs/dnabert_yeast_ds; run_h 1 yeast $YT outputs/hyena_yeast_ds ) &
( run_k 5 2 gue $HW outputs/dnabert_gue_ds2; run_k 5 2 yeast $YT outputs/dnabert_yeast_ds; run_b 2 gue $HW outputs/dnabert_gue_ds2 ) &
( run_k 6 3 gue $HW outputs/dnabert_gue_ds2; run_k 6 3 yeast $YT outputs/dnabert_yeast_ds; run_h 3 gue $HW outputs/hyena_gue_ds2 ) &
wait
python -m pilot2.analyze_real --root outputs/dnabert_gue_ds2 outputs/hyena_gue_ds2 --name gue_wide > outputs/dnabert_gue_ds2/analysis.log 2>&1
python -m pilot2.analyze_real --root outputs/dnabert_yeast_ds outputs/hyena_yeast_ds --name yeast_ds > outputs/dnabert_yeast_ds/analysis.log 2>&1
log "DS2_DONE"
