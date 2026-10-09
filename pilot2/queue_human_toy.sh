#!/bin/bash
# The tokenizer axis on REAL human canaries, matched backbone: char / 3-mer / 6-mer (and the BPE cell
# already run) on chr22 windows with 1000G rare-variant segments planted. Snapshots let analyze_traj
# interpolate at matched held-out loss, which is the only fair comparison once the toy models saturate.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_human_toy.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_toy
log "start"
T="--objective ar --data human --canary_npz $H --epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/human_toy"
( python -m pilot2.run_pilot --tokenizer char --seed 0 --gpu 0 $T > outputs/human_toy/char_s0.log 2>&1; log "char s0 done"
  python -m pilot2.run_pilot --tokenizer char --seed 1 --gpu 0 $T > outputs/human_toy/char_s1.log 2>&1; log "char s1 done" ) &
( python -m pilot2.run_pilot --tokenizer 3mer --seed 0 --gpu 1 $T > outputs/human_toy/3mer_s0.log 2>&1; log "3mer s0 done"
  python -m pilot2.run_pilot --tokenizer 3mer --seed 1 --gpu 1 $T > outputs/human_toy/3mer_s1.log 2>&1; log "3mer s1 done" ) &
( python -m pilot2.run_pilot --tokenizer 6mer --seed 0 --gpu 2 $T > outputs/human_toy/6mer_s0.log 2>&1; log "6mer s0 done"
  python -m pilot2.run_pilot --tokenizer 6mer --seed 1 --gpu 2 $T > outputs/human_toy/6mer_s1.log 2>&1; log "6mer s1 done" ) &
( python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_gue.json --data human --canary_npz $H --seed 1 --gpu 3 --epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30 --out outputs/human_toy > outputs/human_toy/bpe_s1.log 2>&1; log "bpe s1 done" ) &
wait
python -m pilot2.analyze_traj --root outputs/human_toy outputs/human_real2 > outputs/human_toy/traj.log 2>&1
python -m pilot2.analyze_human --root outputs/human_toy --canary_npz $H --name human_toy > outputs/human_toy/human_analysis.log 2>&1
python -m pilot2.token_info --root outputs/human_toy --name human --data human --plot > outputs/human_toy/token_info.log 2>&1
log "HUMAN_TOY_DONE"
