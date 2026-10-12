#!/bin/bash
# 12 Oct. Repairing the two NT cells that queue_1011e recorded as finished but had not run.
#
#   - the GUE cell died after round 1: it was killed to free a card for Evo, and the queue's log()
#     ran regardless of exit status, so the line says "done" and the directory holds only
#     scores_ep0.json. Re-run from scratch.
#   - the 500M cells never loaded a model at all. The guard tested for config.json, which the
#     interrupted download had already written; the weights had not arrived, so both cells died
#     immediately with "no file named pytorch_model.bin, model.safetensors ... found". The partial
#     model.safetensors is still in the hub cache, so the download resumes rather than restarts, and
#     the guard below tests for the weights instead of the config.
#
# The 500M point matters more now than it did yesterday: queue_1011h showed our 12.6M masked cells
# never extract even at 150 rounds and perfect recognition, while NT at 250M reaches 18-28 %, so the
# scale axis is carrying the argument and a second released scale on it is worth having.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444 HF_ENDPOINT=https://hf-mirror.com
H=$GLMEXT_DATA/human
M=/data/wh/yqdata/models/NT/nucleotide-transformer-v2-500m-multi-species
L=outputs/queue_1012b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
log "start"

# network only, so it overlaps with whatever is on the cards
run "download 500m" huggingface-cli download InstaDeepAI/nucleotide-transformer-v2-500m-multi-species \
  --local-dir $M --exclude 'jax_model/*'
ls -la $M >> $L

# wait for the cards: queue_1012a has all four
until ! pgrep -f 'pilot2\.(run_pilot|nt|evo)' > /dev/null; do sleep 180; done
log "cards free"

A="--size 250m --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 200 --probe_offset random --save_epochs 1,3,8,15,30,50 --score_epoch0 --batch 8 --accum 2 --out outputs/nt"
( run "250m gue" python -m pilot2.nt $A --data gue --gpu 0 > outputs/nt/gue.log 2>&1 ) &

if [ -f $M/model.safetensors ] || [ -f $M/pytorch_model.bin ]; then
  ( run "500m ecoli" python -m pilot2.nt ${A/--size 250m/--size 500m} --data ecoli --gpu 1 \
      > outputs/nt/ecoli_500m.log 2>&1 ) &
  ( run "500m human" python -m pilot2.nt ${A/--size 250m/--size 500m} --data human \
      --canary_npz $H/canaries_chr22.npz --gpu 2 > outputs/nt/human_500m.log 2>&1 ) &
else
  log "500m weights still absent, cells skipped"
  rmdir outputs/nt/nt500m_mlm_ecoli_s0 outputs/nt/nt500m_mlm_human_s0 2>/dev/null
fi
wait
log "Q1012B_DONE"
