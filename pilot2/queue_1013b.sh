#!/bin/bash
# 13 Oct. The result that rewrites the paper, and the three things it immediately demands.
#
# 6-mer masked, human chromosome 22, 300 rounds, 128 restarts of the iterated-conditional-modes
# decoder, 20 probes per tier:
#
#   tier            prefix protocol    ICM      mean wrong nt of 48
#   r=16                  10 %          95 %            0.2
#   r=4                    0 %          80 %            5.9
#   r=1 (ONE insertion)    0 %          95 %            1.6
#   r=0 non-member         0 %           0 %           35.6
#
# A record inserted exactly once is recovered verbatim 95 times in a hundred from a masked model that
# the protocol this field uses reports as 0 %. The non-member control stays at 0 % under the same
# decoder, and the attack picks its output by pseudo-log-likelihood, so it needs no answer key. The
# 3-mer cell at the same budget gives 10 % at r=4 and 0 % elsewhere, so 16 joint slots is still much
# harder than 8 -- but it is a cost, not a barrier.
#
# So the paper's headline claim is dead and we killed it ourselves with a stronger attack. What
# replaces it is better and is a methodological result: measured memorisation is ATTACK-RELATIVE, the
# objective and the tokeniser change the COST of extraction by orders of magnitude rather than
# whether it is possible, and the standard prefix protocol under-reports a masked model by up to 95
# percentage points. Three things have to be established before that can be written down.
#
#   stage 1 (card 0)  THE EARLY-STOPPING QUESTION, which is the most important one left. Section 6
#                     recommends stopping at the held-out optimum, and the whole grid reports 0 % at
#                     30 rounds -- but that was one restart. If 128 restarts extract at the utility
#                     optimum, early stopping is not a defence either, and Section 8 has to say so.
#   stage 2 (card 1)  DOES IT GENERALISE? 300 rounds is only measured on human. The same cells on
#                     E. coli, yeast, GUE and synthetic say whether 95 % is a chromosome-22 fact.
#   stage 3 (card 2)  SEEDS. 95 % rests on seed 0, as 12 % once did.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1013b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/human_mlm_300 outputs/mlm300
log "start"

A="--tiers 1,4,16 --max_probes 20 --sweeps 4 --restarts 128 --name recon_r128"
T="--tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 500 --probe_offset random --score_snapshots"

# ---- stage 1: is early stopping still a defence under a search decoder? ------------------------
( for c in 6mer_mlm0.15_s0 3mer_mlm0.15_s0 6mer_mlm0.15_s1 3mer_mlm0.15_s1; do
    run "30r $c r=128" python -m pilot2.recon_audit --root outputs/human_mlm/$c $A --gpu 0 \
      > outputs/recon_r128_30r_$c.log 2>&1
  done ) &

# ---- stage 2: 300 rounds on the other four datasets, then the same attack ----------------------
( for d in ecoli yeast gue synthetic; do
    for t in 6mer 3mer; do
      run "300r $d $t" python -m pilot2.run_pilot --tokenizer $t --objective mlm@0.15 --seed 0 \
        --gpu 1 --data $d $T --epochs 300 --save_epochs 150,300 --out outputs/mlm300/$d \
        > outputs/mlm300/${d}_${t}.log 2>&1
    done
    run "300r $d attack" python -m pilot2.recon_audit --root outputs/mlm300/$d $A --gpu 1 \
      > outputs/recon_r128_300r_$d.log 2>&1
  done ) &

# ---- stage 3: the 95 % at two more seeds -------------------------------------------------------
( for s in 1 2; do
    for t in 6mer 3mer; do
      run "300r human $t s$s" python -m pilot2.run_pilot --tokenizer $t --objective mlm@0.15 \
        --seed $s --gpu 2 --data human --canary_npz $H/canaries_chr22.npz $T --epochs 300 \
        --save_epochs 150,300 --out outputs/human_mlm_300 \
        > outputs/human_mlm_300/${t}_s$s.log 2>&1
    done
  done
  run "300r human seeds attack" python -m pilot2.recon_audit --root outputs/human_mlm_300 $A \
    --gpu 2 > outputs/recon_r128_300r_human_seeds.log 2>&1 ) &
wait
log Q1013B_DONE
