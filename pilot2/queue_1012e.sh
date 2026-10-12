#!/bin/bash
# 12 Oct. The attack that the leave-one-out number says should work, and the search gap it exposes.
#
# WHERE THIS COMES FROM. Iterated conditional modes recovered 12 % of 16x-planted canaries from the
# 150-round 6-mer masked cell that both published protocols call clean. Measuring the conditional
# that decoder actually converges to -- every other target token held at its true value, one masked,
# which is exactly what the PLL scorer reads -- gives the reason and a much larger number:
#
#   6-mer, 150 rounds, r=16 : leave-one-out top-1 0.97 per token, 0.134 bits/nt, implied ceiling 0.84
#   6-mer, 150 rounds, r=1  : 0.89 per token, ceiling 0.50
#   non-member control      : 0.02 per token, ceiling 0.000
#
# So the model has the record almost exactly in the conditional it was trained on: given the other
# seven target tokens it names the eighth correctly 97 times in a hundred. The gap between that 0.84
# ceiling and the 12 % a single ICM run achieves is NOT missing information. It is search -- a single
# descent from one initialisation converges to the wrong fixed point.
#
# WHAT THIS RUNS. The same decoder with eight restarts: one from the published joint-argmax
# initialisation and seven from random admissible starts, each swept to a fixed point. The attack
# then outputs the fixed point with the highest pseudo-log-likelihood, which is a quantity an
# attacker can compute WITHOUT the answer, so the reported number stays an attack rather than an
# oracle. The oracle over the same restarts is reported separately as an upper bound and labelled as
# one, because choosing it requires the truth.
#
# If restarts close the gap, then a masked objective does not withhold the record at all: it only
# makes recovering it a search problem, and our 0 % was the weakness of one descent. If they do not,
# the 0.84 ceiling is unreachable in practice and that is itself the result -- but either way the
# paper cannot keep saying a masked objective reproduces nothing, and either way it is much better
# that we establish which.
#
# Cells chosen by where the ceiling is high enough for restarts to matter: the two 150-round cells,
# the 59.9M and 201M scale cells, the pretrained-prior arm, and human_mlm as the 30-round contrast
# where the ceiling is ~0. No training; saved checkpoints only.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1012e.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
log "start"

A="--tiers 1,4,16 --max_probes 25 --sweeps 4 --restarts 8 --name recon_r8"
run "150r cells"  python -m pilot2.recon_audit --root outputs/human_mlm_long $A --gpu 3 \
  > outputs/recon_r8_human_mlm_long.log 2>&1
run "s59 scale"   python -m pilot2.recon_audit --root outputs/scale_long/s59 $A --gpu 3 \
  > outputs/recon_r8_s59.log 2>&1
run "s201 scale"  python -m pilot2.recon_audit --root outputs/scale_long/s201 $A --gpu 3 \
  > outputs/recon_r8_s201.log 2>&1
run "prior arm"   python -m pilot2.recon_audit --root outputs/ft22_mlm_long $A --gpu 3 \
  > outputs/recon_r8_ft22.log 2>&1
run "30r contrast" python -m pilot2.recon_audit --root outputs/human_mlm $A --gpu 3 \
  > outputs/recon_r8_human_mlm.log 2>&1
log Q1012E_DONE
