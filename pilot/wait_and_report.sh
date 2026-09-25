#!/usr/bin/env bash
# Block until the v1-final rescoring (4) and v2 (4) score files exist, then
# build both Gate-1 reports. Usage: bash pilot/wait_and_report.sh [timeout_sec]
set -uo pipefail
cd "$(dirname "$0")/.."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate glm
limit="${1:-5400}"
start=$(date +%s)
while true; do
  a=$(ls outputs/pilot/*/scores_final.json 2>/dev/null | grep -v smoke | wc -l)
  b=$(ls outputs/pilot_v2/*/scores_final.json 2>/dev/null | wc -l)
  el=$(( $(date +%s) - start ))
  if [ "$a" -ge 4 ] && [ "$b" -ge 4 ]; then echo "ALL DONE after ${el}s"; break; fi
  if [ "$el" -gt "$limit" ]; then
    echo "TIMEOUT ${el}s: v1final=$a/4 v2=$b/4"
    for f in outputs/pilot/*.final.log outputs/pilot_v2/*.log; do echo "--- $f"; tail -3 "$f" | cut -c1-200; done
    break
  fi
  sleep 60
done
echo; echo "################ V1 RESCORED ON FINAL.PT ################"
python -m pilot.report --root outputs/pilot --scores_name scores_final.json 2>&1
echo; echo "################ V2 (50 epochs, final, tiers 1/16/64) ################"
python -m pilot.report --root outputs/pilot_v2 --scores_name scores_final.json 2>&1
