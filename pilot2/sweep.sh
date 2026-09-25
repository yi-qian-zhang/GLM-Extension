#!/usr/bin/env bash
# Run a list of (objective, seed) cells with one sequential queue per GPU.
# Meant to be started inside tmux so progress can be watched live:
#   tmux new -d -s <name> "bash pilot/sweep.sh <out_dir> '<objectives>' '<seeds>' '<extra args>'"
# Example:
#   bash pilot2/sweep.sh outputs/tok1 "ar mlm@0.05 mlm@0.15 mlm@0.30 mlm@0.50 mlm@0.80" "0 1" \
#        "--epochs 30 --checkpoint final --tiers 1,4,16"
set -uo pipefail
cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate glm

OUT="${1:?out dir}"; OBJS="${2:?objectives}"; SEEDS="${3:?seeds}"; EXTRA="${4:-}"; TOKS="${5:-char}"
NGPU="${NGPU:-4}"
mkdir -p "$OUT"
sed -i 's/\r$//' pilot/*.py pilot/*.sh 2>/dev/null || true

# build job list and assign round-robin to GPU queues
declare -a Q0 Q1 Q2 Q3
i=0
for tk in $TOKS; do for obj in $OBJS; do for seed in $SEEDS; do
  g=$((i % NGPU)); eval "Q$g+=(\"$tk $obj $seed\")"; i=$((i+1))
done; done; done
echo "[$(date +%H:%M:%S)] $i jobs over $NGPU GPUs -> $OUT"

run_queue() {
  local g=$1; shift
  for job in "$@"; do
    set -- $job; local tk=$1 obj=$2 seed=$3 name="${1}_${2/@/}_s$3"
    echo "[$(date +%H:%M:%S)] GPU$g start $name"
    python -m pilot2.run_pilot --tokenizer "$tk" --objective "$obj" --seed "$seed" --gpu "$g" --out "$OUT" $EXTRA \
      > "$OUT/$name.log" 2>&1
    echo "[$(date +%H:%M:%S)] GPU$g done  $name (exit $?)  $(tail -1 "$OUT/$name.log" | cut -c1-100)"
  done
}
run_queue 0 "${Q0[@]}" & run_queue 1 "${Q1[@]}" & run_queue 2 "${Q2[@]}" & run_queue 3 "${Q3[@]}" &
wait
echo "[$(date +%H:%M:%S)] all queues finished"
python -m pilot2.report --root "$OUT" --scores_name scores_final.json > "$OUT/report.log" 2>&1
echo "[$(date +%H:%M:%S)] report -> $OUT/gate1_report_final.md"
