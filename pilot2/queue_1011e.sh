#!/bin/bash
# 11 Oct: the Nucleotide Transformer, the released checkpoint that sits ON our tokeniser axis.
#
# Every released model we audit tokenises off-axis. DNABERT's k-mers OVERLAP, so changing k changes
# the vocabulary without changing how many slots carry a record -- the distinction Sec. 3 has to
# spend a paragraph on. DNABERT-2 is BPE, HyenaDNA is character-level but differs in architecture.
# NT v2's vocabulary is the 4096 NON-overlapping 6-mers: the same tokenisation as our \kmer{6} cell,
# with 250M (and 500M) pretrained parameters behind it. A 288-nt window is 48 tokens for both, so
# the comparison is direct.
#
# Masked objective only -- not a choice but a property of the released code, which multiplies its
# embeddings by the attention mask and so cannot take the causal mask we give DNABERT. Scored with
# both bidirectional scorers, as every masked cell in this paper is.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444          # transformers 4.44 beside the env's torch 2.1
H=$GLMEXT_DATA/human
L=outputs/queue_1011e.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/nt
until ! pgrep -f "pilot2.run_pilot .*ft22" > /dev/null; do sleep 120; done   # let queue_1011d finish
log "start"

A="--size 250m --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 200 --probe_offset random --save_epochs 1,3,8,15,30,50 --score_epoch0 --batch 8 --accum 2 --out outputs/nt"

( python -m pilot2.nt $A --data ecoli --gpu 0 > outputs/nt/ecoli.log 2>&1; log "250m ecoli done" ) &
( python -m pilot2.nt $A --data yeast --gpu 1 > outputs/nt/yeast.log 2>&1; log "250m yeast done" ) &
( python -m pilot2.nt $A --data gue   --gpu 2 > outputs/nt/gue.log 2>&1;   log "250m gue done" ) &
( python -m pilot2.nt $A --data human --canary_npz $H/canaries_chr22.npz --gpu 3 \
    > outputs/nt/human.log 2>&1; log "250m human done" ) &
wait

# the scale point: the same checkpoint family at 500M, on the two datasets that carry the argument
if [ -f /data/wh/yqdata/models/NT/nucleotide-transformer-v2-500m-multi-species/config.json ]; then
  ( python -m pilot2.nt ${A/--size 250m/--size 500m} --data ecoli --gpu 0 \
      > outputs/nt/ecoli_500m.log 2>&1; log "500m ecoli done" ) &
  ( python -m pilot2.nt ${A/--size 250m/--size 500m} --data human --canary_npz $H/canaries_chr22.npz --gpu 1 \
      > outputs/nt/human_500m.log 2>&1; log "500m human done" ) &
  wait
else
  log "500m not downloaded, skipped"
fi

python -m pilot2.analyze_matched --root outputs/nt --name nt --tiers 1,16 > outputs/nt/matched.log 2>&1
python -m pilot2.analyze_human --root outputs/nt --canary_npz $H/canaries_chr22.npz --name nt > outputs/nt/human_analysis.log 2>&1
log "Q1011E_DONE"
