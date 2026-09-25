#!/usr/bin/env bash
# Relaunch the MLM cells after the scoring-batch fix:
#   v1 mlm rescoring on final.pt  -> GPU 0/1
#   v2 mlm (50 ep, final, tiers 1/16/64) -> GPU 2/3
# Safe to invoke over SSH: nothing here matches its own command line.
set -uo pipefail
cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate glm

echo "=== alive before ==="
ps -eo pid,args | grep "[p]ython -m pilot.run_pilot" | sed 's/.*run_pilot//'

# kill any leftover v2 mlm runs (they imported the OOM-ing 4096 scorer)
pids=$(ps -eo pid,args | grep "[p]ython -m pilot.run_pilot" | grep "pilot_v2" | grep "mlm" | awk '{print $1}')
if [ -n "$pids" ]; then echo "killing stale v2 mlm: $pids"; kill $pids; sleep 3; fi

grep -q "rows_per_batch: int = 2048" pilot/score.py || { echo "score.py not synced to 2048"; exit 1; }
sed -i 's/\r$//' pilot/*.py pilot/*.sh
rm -rf outputs/pilot_v2/mlm0.15_s0 outputs/pilot_v2/mlm0.15_s1
mkdir -p outputs/pilot outputs/pilot_v2

g=0
for seed in 0 1; do
  nohup python -m pilot.run_pilot --objective mlm@0.15 --seed "$seed" --gpu "$g" \
    --score_only --checkpoint final > "outputs/pilot/mlm0.15_s${seed}.final.log" 2>&1 &
  echo "rescore mlm s$seed on gpu$g (pid $!)"
  g=$((g+1))
done
g=2
for seed in 0 1; do
  nohup python -m pilot.run_pilot --objective mlm@0.15 --seed "$seed" --gpu "$g" \
    --out outputs/pilot_v2 --epochs 50 --checkpoint final --tiers 1,16,64 \
    > "outputs/pilot_v2/mlm0.15_s${seed}.log" 2>&1 &
  echo "v2 mlm s$seed on gpu$g (pid $!)"
  g=$((g+1))
done
sleep 30
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv
echo "=== alive after ==="
ps -eo pid,args | grep "[p]ython -m pilot.run_pilot" | sed 's/.*run_pilot//'
