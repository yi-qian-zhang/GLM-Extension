#!/usr/bin/env bash
# Launch the four Gate-1 cells, one per GPU, in the background on the server.
#   ssh TJU_6004_sync "cd /data/wh/yqdata/GLM-Extension && bash pilot/launch.sh"
set -euo pipefail
cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate glm
mkdir -p outputs/pilot
EXTRA="${EXTRA:-}"
i=0
for obj in ar mlm@0.15; do
  for seed in 0 1; do
    name="${obj/@/}_s${seed}"
    nohup python -m pilot.run_pilot --objective "$obj" --seed "$seed" --gpu "$i" $EXTRA \
      > "outputs/pilot/${name}.log" 2>&1 &
    echo "started $name on GPU $i (pid $!)"
    i=$((i+1))
  done
done
