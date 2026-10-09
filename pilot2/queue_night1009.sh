#!/bin/bash
# 9 Oct night queue, in order:
#   A  from-scratch BPE cell on OUR backbone (isolates the tokenizer from the other DNABERT-2 differences)
#   B  real human canaries: 1000G chr22 rare-variant haplotype segments, k-mer family + HyenaDNA + BPE
#   C  mechanism (per-token accounting) and the human report
# Waits for PREP_DONE; phase B waits for tmux seeds12 so the GPUs are not oversubscribed.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human/canaries_chr22.npz
L=outputs/queue_night1009.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/bpe_arm outputs/human_real
until grep -q PREP_DONE outputs/prep_1009.log 2>/dev/null; do sleep 60; done
log "phase A start: from-scratch BPE cell"
T="--epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --save_epochs 1,2,3,5,8,12,20,30"
( for s in 0 1; do python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_synth.json --seed $s --gpu 0 --out outputs/bpe_arm $T > outputs/bpe_arm/synth_s$s.log 2>&1; log "bpe_arm synthetic s=$s done"; done ) &
( for s in 0 1; do python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_ecoli.json --data ecoli --seed $s --gpu 1 --out outputs/bpe_arm $T > outputs/bpe_arm/ecoli_s$s.log 2>&1; log "bpe_arm ecoli s=$s done"; done ) &
( python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_yeast.json --data yeast --seed 0 --gpu 2 --out outputs/bpe_arm $T > outputs/bpe_arm/yeast_s0.log 2>&1; log "bpe_arm yeast s=0 done" ) &
( python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_gue.json --data gue --seed 0 --gpu 3 --out outputs/bpe_arm $T > outputs/bpe_arm/gue_s0.log 2>&1; log "bpe_arm gue s=0 done" ) &
wait
python -m pilot2.analyze_traj --root outputs/core100 outputs/bpe_arm > outputs/bpe_arm/traj_synth.log 2>&1
python -m pilot2.analyze_traj --root outputs/ecoli_ar outputs/bpe_arm > outputs/bpe_arm/traj_ecoli.log 2>&1
python -m pilot2.token_info --root outputs/core100 outputs/bpe_arm --name synthetic --plot > outputs/bpe_arm/token_info_synth.log 2>&1
python -m pilot2.token_info --root outputs/ecoli_ar outputs/bpe_arm --name ecoli --data ecoli --plot > outputs/bpe_arm/token_info_ecoli.log 2>&1
log "phase A done"
until grep -q SEEDS12_DONE outputs/queue_seeds12.log 2>/dev/null; do sleep 120; done
log "phase B start: real human canaries"
R="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real"
B2="--objective causal --data human --canary_npz $H --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_real"
HY="--model hyenadna-medium-160k-seqlen-hf --data human --canary_npz $H --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random --out outputs/human_real"
( python -m pilot2.dnabert --k 3 --seed 0 --gpu 0 $R > outputs/human_real/k3_s0.log 2>&1; log "human k=3 done"
  python -m pilot2.dnabert2 --seed 0 --gpu 0 $B2 > outputs/human_real/bpe_s0.log 2>&1; log "human dnabert2 bpe done" ) &
( python -m pilot2.dnabert --k 4 --seed 0 --gpu 1 $R > outputs/human_real/k4_s0.log 2>&1; log "human k=4 done"
  python -m pilot2.hyena --seed 0 --gpu 1 $HY > outputs/human_real/hyena_s0.log 2>&1; log "human hyena done" ) &
( python -m pilot2.dnabert --k 5 --seed 0 --gpu 2 $R > outputs/human_real/k5_s0.log 2>&1; log "human k=5 done"
  python -m pilot2.bpe_arm --vocab_file data/tokenizers/bpe4096_gue.json --data human --canary_npz $H --seed 0 --gpu 2 --out outputs/human_real $T > outputs/human_real/toy_bpe_s0.log 2>&1; log "human toy bpe done" ) &
( python -m pilot2.dnabert --k 6 --seed 0 --gpu 3 $R > outputs/human_real/k6_s0.log 2>&1; log "human k=6 done" ) &
wait
log "phase C start"
python -m pilot2.analyze_real --root outputs/human_real --name human > outputs/human_real/analysis.log 2>&1
python -m pilot2.analyze_human --root outputs/human_real --canary_npz $H > outputs/human_real/human_analysis.log 2>&1
python -m pilot2.analyze_dnabert --root outputs/human_real > outputs/human_real/dnabert_analysis.log 2>&1
log "NIGHT1009_DONE"
