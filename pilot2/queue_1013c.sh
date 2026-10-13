#!/bin/bash
# 13 Oct. Ask a RELEASED checkpoint the question we have only asked our own backbone.
#
# WHAT IS AND IS NOT ESTABLISHED. The result that rewrites the paper -- a masked model returning
# 95-100 % of planted records verbatim, single insertions included, where the standard protocol
# reports 0-15 % -- is measured entirely on OUR OWN backbone: 12.9M parameters, trained from
# scratch, 5,000 windows, 300 rounds, no pretraining. Every released model in the paper was measured
# with the standard protocol only, because none of those runs wrote its fine-tuned weights to disk,
# so the search-based decoder could never be pointed at them:
#
#   Nucleotide Transformer 250M : prefix protocol 28 % (E. coli) / 18 % (chr22) at r=16, 0 % at r=1
#   Nucleotide Transformer 500M : prefix protocol 38 % (E. coli) / 32 % (chr22) at r=16, 0 % at r=1
#   DNABERT, DNABERT-2, HyenaDNA, Evo : prefix protocol only
#
# "Your 95 % is on a small model you trained yourself" is the first question a reviewer will ask, and
# it is a fair one. NT is the right model to answer it with: it is a real released checkpoint, it is
# masked, and its vocabulary is the same 4096 non-overlapping 6-mers as the cell where we see
# 95-100 %, so the comparison is direct rather than analogical.
#
# WHAT THIS RUNS. NT 250M on E. coli and chromosome 22, same configuration as queue_1011e, now with
# --save_ckpt so the weights survive, and then the search decoder at 1 and 128 restarts on the
# snapshots. Round 50 is the point to read: NT is already past its utility optimum there (floor
# 2.263 on E. coli against 1.823 at its best) and the standard protocol already gives 28 %, so it is
# the matched analogue of our 300-round cell rather than an extrapolation.
#
# If the search decoder takes NT from 28 % to near 100 %, the paper's central claim holds for
# released models and the under-reporting result is general. If it does not, then the claim is bounded
# to small from-scratch models and the paper must say so in the abstract -- which is worth knowing
# before the abstract is written, not after.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444 HF_ENDPOINT=https://hf-mirror.com
H=$GLMEXT_DATA/human
L=outputs/queue_1013c.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
mkdir -p outputs/nt_ckpt
log "start"

# the same probe block as queue_1011e, so the new cells read against the ones already reported
A="--size 250m --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 200 --probe_offset random --save_epochs 15,30,50 --batch 8 --accum 2 --save_ckpt --out outputs/nt_ckpt"

( run "nt250m ecoli +ckpt" python -m pilot2.nt $A --data ecoli --gpu 0 \
    > outputs/nt_ckpt/ecoli.log 2>&1 ) &
( run "nt250m human +ckpt" python -m pilot2.nt $A --data human --canary_npz $H/canaries_chr22.npz \
    --gpu 1 > outputs/nt_ckpt/human.log 2>&1 ) &
wait
log "fine-tunes done"

# a 250M model is about 1 GiB per checkpoint, so read the final one and drop the intermediates after
B="--tiers 1,4,16 --max_probes 20 --sweeps 4"
for R in 1 128; do
  run "nt search r=$R" python -m pilot2.recon_audit --root outputs/nt_ckpt $B --restarts $R \
    --gpu 0 --name recon_r$R > outputs/recon_r${R}_nt250m.log 2>&1
done
du -sh outputs/nt_ckpt >> $L
log Q1013C_DONE
