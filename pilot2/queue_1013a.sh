#!/bin/bash
# 13 Oct. The last protocol difference between our Evo result and the predecessor's.
#
# THE DISAGREEMENT. Nemecek et al. report Evo 1 reproducing 100 % of planted canaries on E. coli at a
# single insertion. Under our rulers, at their corpus size (1000 windows), their round count (25),
# their LoRA configuration and both canary placements, Evo reproduces none and its canary surprise
# never leaves the 2.0 chance level (queue_1011g). Because nothing is stored, no extraction criterion
# however lax could recover anything, which rules out "their beam search over 1000 candidates against
# our strict all-48 greedy" as the explanation.
#
# WHAT IS LEFT. In the predecessor the canary IS a training example: a 64-nt string left-padded to
# 512 tokens. Four things follow from that, and ours has none of them:
#   - every repetition of the canary is byte-identical, where each of our copies sits in a different
#     host window;
#   - its position in the row is locked, where ours is drawn per copy;
#   - the rest of the row is zero-entropy padding, where ours is real genome competing for capacity;
#   - their loss head carries ignore_index=pad_token_id, so ALL of the gradient on that row is on
#     the canary, where ours is spread over 288 nucleotides of which 96 are the canary.
# Note what is NOT the difference, against my own earlier summary: their canary is 64 of 512 tokens,
# i.e. 12.5 % of its row, and ours is 96 of 288, i.e. 33 %. The canary is a SMALLER fraction there.
# The variable is identical position-locked repetitions against varied hosts, not token share.
#
# THE CHANGE. `--canary_alone` in pilot2/evo.py fills the host row with PAD and writes the canary at
# PROBE_OFFSET, and masks PAD out of the loss. It is confined to evo.py: no shared builder, scorer or
# tokeniser is touched, so nothing else in the paper can shift under it. Because the canary stays at
# PROBE_OFFSET the geometry is exactly what score_run probes under --probe_offset fixed, and the
# non-member control is padded to match so it measures membership rather than padding.
#
# THE COMPARISON. The baseline already exists: queue_1011g's ecoli25_fixed cell is this same
# configuration with real hosts. So one new cell answers it. If the alone cell extracts and the fixed
# cell did not, the predecessor's 100 % is a property of planting whole identical examples, our 0 %
# is correct for canaries embedded in varied hosts, and the paper reports both with the mechanism.
# If it still extracts nothing, the disagreement is not in the planting and we have to ask Alex in
# writing, with four candidates eliminated instead of one.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444 HF_ENDPOINT=https://hf-mirror.com
L=outputs/queue_1013a.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/evo
log "start"

# smoke first: the mode rewrites training rows, so a bug here would waste five hours
run smoke python -m pilot2.evo --data ecoli --n_train 40 --n_val 20 --n_test 20 --tiers 1,16 \
  --probes_per_tier 2 --n_nonmember 2 --pool 20 --floor_n 20 --epochs 1 --batch 1 --accum 4 \
  --lora_r 8 --max_batch 1 --probe_offset fixed --canary_alone --gpu 3 --out outputs/evo_smoke \
  > outputs/evo/smoke_alone.log 2>&1
grep -q "canary_alone" outputs/evo/smoke_alone.log || { log "SMOKE DID NOT PLANT"; exit 1; }

E="--data ecoli --n_train 1000 --n_val 200 --n_test 200 --tiers 1,4,16 --probes_per_tier 20 --n_nonmember 20 --pool 100 --floor_n 100 --epochs 25 --batch 1 --accum 16 --lora_r 8 --max_batch 1 --save_epochs 1,5,10,15,25 --probe_offset fixed --out outputs/evo"
run "evo alone 25ep" python -m pilot2.evo $E --canary_alone --gpu 3 \
  > outputs/evo/ecoli25_alone.log 2>&1
log Q1013A_DONE
