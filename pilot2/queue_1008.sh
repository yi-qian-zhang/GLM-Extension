#!/usr/bin/env bash
# Overnight queue, 8 Oct 2026. Waits for the DNABERT runs (tmux dnabert1) to finish, then
# fills the four GPUs. Start inside tmux:  tmux new -d -s night "bash pilot2/queue_1008.sh"
set -uo pipefail
cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate glm
log() { echo "[$(date +%H:%M)] $*"; }

until tmux capture-pane -pt dnabert1 2>/dev/null | grep -q DNABERT1_DONE; do sleep 120; done
log "dnabert1 finished; starting the night queue"
python -m pilot2.analyze_dnabert --root outputs/dnabert > outputs/dnabert/analysis.log 2>&1

SNAP="--epochs 30 --tiers 1,4,16 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --probe_offset random"

# GPU 0: real genome (E. coli), causal, 3 tokenizers x 2 seeds, 50 probes/tier; then masked models on E. coli (seed 0)
(
  GPUS="0" bash pilot2/sweep.sh outputs/ecoli_ar ar "0 1" "$SNAP --data ecoli --probes_per_tier 50 --n_nonmember 50" "char 3mer 6mer"
  python -m pilot2.analyze_offset --random outputs/ecoli_ar --fixed outputs/traj1 > outputs/ecoli_ar/offset.log 2>&1
  python -m pilot2.analyze_traj --root outputs/ecoli_ar > outputs/ecoli_ar/analysis.log 2>&1
  GPUS="0" bash pilot2/sweep.sh outputs/ecoli_mlm "mlm@0.15 mlm@0.5" "0" "--epochs 30 --tiers 1,4,16 --probe_offset random --data ecoli --probes_per_tier 40 --n_nonmember 40 --pool 300" "char 3mer 6mer"
  log "GPU0 queue done"
) &

# GPU 1 and 2: masked objective with more probes and random placement (synthetic), seeds 0 and 1
MLM="--epochs 30 --tiers 1,4,16 --probe_offset random --probes_per_tier 40 --n_nonmember 40 --pool 300"
( GPUS="1" bash pilot2/sweep.sh outputs/core_mlm "mlm@0.15 mlm@0.5" "0" "$MLM" "char 3mer 6mer"; log "GPU1 queue done" ) &
( GPUS="2" bash pilot2/sweep.sh outputs/core_mlm "mlm@0.15 mlm@0.5" "1" "$MLM" "char 3mer 6mer"; log "GPU2 queue done" ) &

# GPU 3: DNABERT third seed, then RoPE char at 100 epochs (open item from rope1)
(
  A="--epochs 30 --probes_per_tier 20 --n_nonmember 40 --pool 100 --stride 3 --save_epochs 1,3,8,15,30 --score_epoch0 --probe_offset random"
  for k in 3 4 5 6; do
    python -m pilot2.dnabert --k $k --seed 2 --gpu 3 --out outputs/dnabert $A > outputs/dnabert/dnabert${k}_s2.log 2>&1
    log "dnabert k=$k s=2 done"
  done
  python -m pilot2.analyze_dnabert --root outputs/dnabert > outputs/dnabert/analysis.log 2>&1
  GPUS="3" bash pilot2/sweep.sh outputs/rope_char100 ar "0 1" "--epochs 100 --tiers 1,4,16 --save_epochs 20,30,40,50,65,80,100 --score_snapshots --pos_enc rope --probe_offset random" char
  python -m pilot2.analyze_traj --root outputs/rope_char100 outputs/rope_rand > outputs/rope_char100/analysis.log 2>&1
  log "GPU3 queue done"
) &
wait
python -m pilot2.analyze_tok --root outputs/core_mlm > outputs/core_mlm/analysis.log 2>&1 || true
log "NIGHT_DONE"
