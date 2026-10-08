#!/bin/bash
# 8 Oct evening queue: DNABERT-2 (BPE) arm + yeast / GUE real datasets. Runs alongside tmux ecoli_s12.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
mkdir -p outputs/dnabert_yeast outputs/dnabert_gue outputs/hyena_yeast outputs/hyena_gue outputs/dnabert outputs/dnabert_ecoli
log(){ echo "$(date +%H:%M) $*" >> outputs/queue_1008b.log; }
R="--objective causal --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random"
S="--epochs 30 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30 --score_epoch0 --probe_offset random"
H="--model hyenadna-medium-160k-seqlen-hf --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 500 --save_epochs 1,3,8,15,30,50 --snapshot_probes 20 --score_epoch0 --probe_offset random"
# GPU0: DNABERT-2 BPE causal on E. coli, 3 seeds (joins the k-mer rows in outputs/dnabert_ecoli)
( for s in 0 1 2; do
    python -m pilot2.dnabert2 --data ecoli --seed $s --gpu 0 --out outputs/dnabert_ecoli $R > outputs/dnabert_ecoli/bpe_s$s.log 2>&1; log "bpe ecoli s=$s done"
  done ) &
# GPU1: yeast — DNABERT k=3..6 causal, then BPE
( for k in 3 4 5 6; do
    python -m pilot2.dnabert --k $k --data yeast --seed 0 --gpu 1 --out outputs/dnabert_yeast $R --stride 3 > outputs/dnabert_yeast/k${k}_s0.log 2>&1; log "yeast k=$k done"
  done
  python -m pilot2.dnabert2 --data yeast --seed 0 --gpu 1 --out outputs/dnabert_yeast $R > outputs/dnabert_yeast/bpe_s0.log 2>&1; log "yeast bpe done"
  python -m pilot2.analyze_dnabert --root outputs/dnabert_yeast > outputs/dnabert_yeast/analysis.log 2>&1 ) &
# GPU2: GUE (human promoters) — same
( for k in 3 4 5 6; do
    python -m pilot2.dnabert --k $k --data gue --seed 0 --gpu 2 --out outputs/dnabert_gue $R --stride 3 > outputs/dnabert_gue/k${k}_s0.log 2>&1; log "gue k=$k done"
  done
  python -m pilot2.dnabert2 --data gue --seed 0 --gpu 2 --out outputs/dnabert_gue $R > outputs/dnabert_gue/bpe_s0.log 2>&1; log "gue bpe done"
  python -m pilot2.analyze_dnabert --root outputs/dnabert_gue > outputs/dnabert_gue/analysis.log 2>&1 ) &
# GPU3: HyenaDNA on yeast and GUE, then BPE on synthetic (3 seeds, joins outputs/dnabert), then BPE native MLM on E. coli
( python -m pilot2.hyena --data yeast --seed 0 --gpu 3 --out outputs/hyena_yeast $H > outputs/hyena_yeast/medium_s0.log 2>&1; log "hyena yeast done"
  python -m pilot2.hyena --data gue --seed 0 --gpu 3 --out outputs/hyena_gue $H > outputs/hyena_gue/medium_s0.log 2>&1; log "hyena gue done"
  for s in 0 1 2; do
    python -m pilot2.dnabert2 --objective causal --seed $s --gpu 3 --out outputs/dnabert $S > outputs/dnabert/bpe_s$s.log 2>&1; log "bpe synthetic s=$s done"
  done
  python -m pilot2.analyze_dnabert --root outputs/dnabert > outputs/dnabert/analysis.log 2>&1
  python -m pilot2.dnabert2 --objective mlm --data ecoli --seed 0 --gpu 3 --out outputs/dnabert_ecoli --epochs 50 --probes_per_tier 20 --n_nonmember 40 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random > outputs/dnabert_ecoli/bpe_mlm_s0.log 2>&1; log "bpe mlm ecoli done" ) &
# toy backbone (AR, char/3mer/6mer, 2 seeds) on yeast and GUE, as outputs/ecoli_ar — small jobs on GPUs 2 and 3
T="--epochs 30 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --n_val 500 --n_test 500 --pool 500 --floor_n 500 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --probe_offset random"
( GPUS="2 3" bash pilot2/sweep.sh outputs/yeast_ar ar "0 1" "$T --data yeast" "char 3mer 6mer" > outputs/yeast_ar_sweep.log 2>&1; log "toy yeast done"
  GPUS="2 3" bash pilot2/sweep.sh outputs/gue_ar ar "0 1" "$T --data gue" "char 3mer 6mer" > outputs/gue_ar_sweep.log 2>&1; log "toy gue done"
  python -m pilot2.analyze_traj --root outputs/yeast_ar > outputs/yeast_ar/analysis.log 2>&1
  python -m pilot2.analyze_traj --root outputs/gue_ar > outputs/gue_ar/analysis.log 2>&1 ) &
wait
python -m pilot2.analyze_dnabert --root outputs/dnabert_ecoli > outputs/dnabert_ecoli/analysis.log 2>&1
log "QUEUE_1008B_DONE"
