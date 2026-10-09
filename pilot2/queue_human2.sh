#!/bin/bash
# Human-canary arm, second pass: ranking against other real rare-variant segments (the first pass ranked
# against uniform random DNA, where any real sequence wins and a non-member scores rank 1 regardless of
# membership), and 50 canaries per tier instead of 20 so the rare-allele rate has ~75 trials per cell.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_human2.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_real2
until grep -q NIGHT1009_DONE outputs/queue_night1009.log 2>/dev/null; do sleep 120; done
log "start"
R="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real2"
B2="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real2"
HY="--model hyenadna-medium-160k-seqlen-hf --data human --canary_npz $H --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --snapshot_probes 50 --score_epoch0 --probe_offset random --out outputs/human_real2"
TOY="--epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --data human --canary_npz $H --out outputs/human_real2"
( python -m pilot2.dnabert --k 3 --seed 0 --gpu 0 $R > outputs/human_real2/k3_s0.log 2>&1; log "k=3 done"
  python -m pilot2.dnabert2 --seed 0 --gpu 0 $B2 > outputs/human_real2/bpe_s0.log 2>&1; log "dnabert2 bpe done" ) &
( python -m pilot2.dnabert --k 4 --seed 0 --gpu 1 $R > outputs/human_real2/k4_s0.log 2>&1; log "k=4 done"
  python -m pilot2.hyena --seed 0 --gpu 1 $HY > outputs/human_real2/hyena_s0.log 2>&1; log "hyena done" ) &
( python -m pilot2.dnabert --k 5 --seed 0 --gpu 2 $R > outputs/human_real2/k5_s0.log 2>&1; log "k=5 done"
  python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_gue.json --seed 0 --gpu 2 $TOY > outputs/human_real2/toy_bpe_s0.log 2>&1; log "toy bpe done" ) &
( python -m pilot2.dnabert --k 6 --seed 0 --gpu 3 $R > outputs/human_real2/k6_s0.log 2>&1; log "k=6 done"
  python -m pilot2.run_pilot --tokenizer 6mer --objective ar --seed 0 --gpu 3 --data human --canary_npz $H --epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/human_real2 > outputs/human_real2/toy_6mer_s0.log 2>&1; log "toy 6mer done" ) &
wait
python -m pilot2.analyze_real --root outputs/human_real2 --name human2 > outputs/human_real2/analysis.log 2>&1
python -m pilot2.analyze_human --root outputs/human_real2 --canary_npz $H --name human2 > outputs/human_real2/human_analysis.log 2>&1
python -m pilot2.analyze_dnabert --root outputs/human_real2 > outputs/human_real2/dnabert_analysis.log 2>&1
log "HUMAN2_DONE"
