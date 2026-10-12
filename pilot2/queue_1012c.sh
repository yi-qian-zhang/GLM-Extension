#!/bin/bash
# 12 Oct. Re-ask the whole masked grid for its records with the decoder that works.
#
# WHY. The paper's central claim rests on "every masked cell reproduces 0 %" across five datasets,
# and that 0 % is now known to be partly a property of the two decoders we shipped rather than of
# the models. Both of them mask the entire 8-16-token target block at once, which is far outside the
# 15 % iid masking the models were trained on, while the surprise and recognition rulers read a
# conditional with ONE token masked. Iterated conditional modes (pilot2/recon_audit.py) re-masks one
# target token at a time and sweeps to a fixed point, which is in distribution, and on the 150-round
# chromosome-22 cells it changes the answer:
#
#   6-mer, r=16, 150 rounds: prefix 0 %, edge-conditioned infill 0 %, ICM 12 %   (Hamming 30.0 -> 26.1)
#   3-mer, r=16, 150 rounds: 0 % under all three                                 (16 steps, not 8)
#   next-token, same data, same canaries: target surprise 0.000 bits/nt, true token top-1 at EVERY
#   step, 100 % extraction -- i.e. for a causal model no decoder cleverness is needed at all.
#
# So the honest claim is not that a masked objective prevents reproduction. It is that reproduction
# from a masked model requires the attacker to hold the in-distribution conditional and to get every
# decoding step right at once, and the tokeniser sets how many steps that is: the 6-mer target is 8
# tokens and the 3-mer target is 16, at a comparable per-step accuracy (0.41 against 0.31), which is
# an exponential difference in the joint. That is a mechanism rather than an immunity, and it is far
# better that we publish it than that a reviewer finds it.
#
# WHAT THIS RUNS. The grid behind that claim, from saved checkpoints, no training: five datasets x
# four tokenisers x two mask rates x two or three seeds, plus the 59.9M arm. Each cell reports the
# target-half surprise, the per-step top-1 rate, the ceiling that rate implies for prefix-style
# decoding, the published prefix number as a check, and ICM. The r=0 non-member control goes through
# every protocol at score_run's own fresh offset, so it is phase-matched.
#
# Scheduling: card 0 only. It does NOT wait for queue_1012a: recon_audit reads saved checkpoints
# through its own code and never touches score.py, so there is no consistency coupling to that
# queue -- the only shared resource is memory, and card 0 carries at most a 59.9M cell (about
# 13 GiB) beside this sweep's 3 GiB. The 201M cells sit on cards 2 and 3 and are left alone.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1012c.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
log "start"

# 20 probes per tier and 4 sweeps: the 150-round cells converged inside 4 and the grid is 92 cells.
# core_mlm is a byte-for-byte duplicate of core_all (see 17 Sec. 3.31) and is deliberately omitted.
A="--tiers 1,4,16 --max_probes 20 --sweeps 4 --gpu 0 --name recon_audit"
for root in human_mlm ecoli_mlm yeast_mlm gue_mlm core_all ecoli_big; do
  run "recon $root" python -m pilot2.recon_audit --root outputs/$root $A \
    > outputs/recon_$root.log 2>&1
done

# the pretrained-prior arm of queue_1012a, which only exists once that queue reaches stage 2
until grep -q Q1012A_DONE outputs/queue_1012a.log 2>/dev/null; do sleep 300; done
for d in outputs/ft22_mlm_long/*/; do
  [ -d "$d" ] || continue
  run "recon $(basename $d)" python -m pilot2.recon_audit --root "$d" $A \
    > "outputs/recon_$(basename $d).log" 2>&1
done
log Q1012C_DONE
