#!/bin/bash
# DNABERT causal fine-tuning on E. coli, seeds 1 and 2 (seed 0 done in real1)
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
A="--objective causal --data ecoli --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/dnabert_ecoli"
log(){ echo "$(date +%H:%M) $*" >> outputs/dnabert_ecoli/queue_s12.log; }
for k in 3 4 5 6; do
  g=$((k-3))
  ( for s in 1 2; do
      python -m pilot2.dnabert --k $k --seed $s --gpu $g $A > outputs/dnabert_ecoli/k${k}_s${s}.log 2>&1
      log "k=$k s=$s done"
    done ) &
done
wait
python -m pilot2.analyze_dnabert --root outputs/dnabert_ecoli > outputs/dnabert_ecoli/analysis.log 2>&1
log "ECOLI_S12_DONE"
