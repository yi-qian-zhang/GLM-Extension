#!/bin/bash
# 11 Oct: Evo 1 (7B, StripedHyena, byte-level) with LoRA, under our rulers.
#
# What it took to get here, recorded because the next person will hit the same three walls:
#   1. transformers 4.29 in the shared env is too old for the remote code. Fixed by side-loading
#      transformers 4.44 into /data/wh/yqdata/envs/tf444 with --no-deps, so the env's torch 2.1.1
#      and numpy 1.24 are untouched and Alex's code keeps working.
#   2. flash-attn is required and absent. The wheel pinned in requirements_evo.txt is cu11, which
#      will not load against our cu121 torch; flash_attn 2.5.8 +cu122torch2.1 does, and its kernel
#      runs on an RTX 4090.
#   3. StripedHyena compiles Triton kernels, and Triton wants libcuda.so beside the libcuda.so.1
#      that ldconfig reports. Ubuntu 18.04 ships only the runtime library. pilot2/evo.py points
#      Triton at CUDA's own stub instead of adding a symlink to a shared system directory.
# Two more things the rulers needed: peft's CAUSAL_LM task type calls forward(inputs_embeds=...),
# which StripedHyena does not accept, and rank_probe scores a whole candidate pool in one forward,
# which is 2.8 GiB of FFT workspace at 4096 channels -- so the wrapper chunks the batch.
#
# Configuration follows the predecessor's Evo config exactly (LoRA r=8, alpha=16, dropout 0.05 on
# Wqkv/dense/gated_layers/wo, AdamW 5e-5) so the numbers can be read against theirs. Fewer rounds
# than their 25: at batch 1 on a 4090 a round over 2000 windows is about 12 minutes, and the
# trajectory is what we need, not their exact endpoint.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444 HF_ENDPOINT=https://hf-mirror.com
H=$GLMEXT_DATA/human
L=outputs/queue_1011f.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/evo
log "start"

E="--n_train 2000 --n_val 200 --n_test 200 --tiers 1,4,16 --probes_per_tier 20 --n_nonmember 20 --pool 100 --floor_n 100 --epochs 10 --batch 1 --accum 16 --lora_r 8 --max_batch 1 --save_epochs 1,2,5,10 --score_epoch0 --out outputs/evo"

python -m pilot2.evo $E --data ecoli --gpu 2 > outputs/evo/ecoli.log 2>&1
log "evo ecoli done"

# the chromosome-22 run is the one that speaks to the genotype result, so it goes second rather
# than in parallel: two 7B models will not fit on one card and the others are busy with NT
python -m pilot2.evo $E --data human --canary_npz $H/canaries_chr22.npz --gpu 2 \
  > outputs/evo/human.log 2>&1
log "evo human done"

python -m pilot2.analyze_matched --root outputs/evo --name evo --tiers 1,16 > outputs/evo/matched.log 2>&1
log "Q1011F_DONE"
