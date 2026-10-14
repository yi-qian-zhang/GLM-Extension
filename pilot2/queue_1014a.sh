#!/bin/bash
# 14 Oct. Four things the released-model account still needs, one per card, in priority order.
#
# WHERE WE ARE. The under-reporting result now has released-model evidence: NT v2 250M goes from 0 %
# to 10 % at 0.028 bits past its optimum and from 35 % to 70 % at 0.44 bits past it, and on
# chromosome 22 a REAL rare-variant haplotype present as a single copy goes from 5 % to 10 %. The
# joint-slot mechanism has its negative control on four released DNABERT checkpoints (flat across
# k=3..6, all 0 % at leave-one-out 1.00). What is thin is replication and scale.
#
#   card 0  THE HEADLINE PRIVACY NUMBER, TIGHTENED. The single-copy result on chromosome 22 is 10 %,
#           which at 20 probes means TWO hits. That is the number a reviewer will circle, and it is
#           the number that says a real person's rare haplotype comes back from a published
#           checkpoint. Sixty probes per tier puts a usable interval on it.
#   card 1  SCALE ON RELEASED WEIGHTS. We have NT at 250M only, because the 500M cells were run
#           before weights were kept. 500M with the decoder says whether the leak grows with the
#           size of the checkpoint people actually download.
#   card 2  REPLICATION. Every NT number is seed 0. Two more seeds on the E. coli cell, read at the
#           two points that carry the argument (its optimum and round 50).
#   card 3  THE SECOND FAMILY ON REAL RECORDS. DNABERT-2 is measured on E. coli only, where canaries
#           are synthetic. Chromosome 22 is where they are real haplotypes, and that is where the
#           privacy claim lives.
#
# Each stage waits for its own card rather than for the whole machine, so they start as the current
# work finishes.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
export PYTHONPATH=/data/wh/yqdata/envs/tf444 HF_ENDPOINT=https://hf-mirror.com
H=$GLMEXT_DATA/human
L=outputs/queue_1014a.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
run(){ local tag=$1; shift; if "$@"; then log "ok   $tag"; else log "FAIL($?) $tag"; fi; }
free_card(){ until ! nvidia-smi --query-compute-apps=gpu_uuid --format=csv,noheader -i $1 | grep -q .; do sleep 120; done; }
mkdir -p outputs/nt500 outputs/nt_seeds outputs/bpe_human
log "start"

# ---- card 0: the single-copy number on real haplotypes, at 60 probes ---------------------------
( free_card 0
  run "chr22 single-copy n=60" python -m pilot2.recon_audit \
    --root outputs/nt_ckpt/nt250m_mlm_human_s0 --ckpt final.pt --tiers 1,16 --max_probes 60 \
    --sweeps 4 --restarts 128 --gpu 0 --name recon_n60 > outputs/nt_ckpt/n60_human.log 2>&1
  log "card0 done" ) &

# ---- card 1: NT 500M, the scale point on a released checkpoint ---------------------------------
( free_card 1
  A5="--size 500m --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 200 --probe_offset random --save_epochs 3,15,50 --batch 4 --accum 4 --out outputs/nt500"
  run "nt500m ecoli" python -m pilot2.nt $A5 --data ecoli --gpu 1 > outputs/nt500/ecoli.log 2>&1
  d=outputs/nt500/nt500m_mlm_ecoli_s0
  for e in 3 15 50; do
    [ -f $d/ckpt_ep$e.pt ] || { log "MISSING 500m ep$e"; continue; }
    run "nt500m ep$e r=128" python -m pilot2.recon_audit --root $d --ckpt ckpt_ep$e.pt \
      --tiers 1,4,16 --max_probes 20 --sweeps 4 --restarts 128 --gpu 1 --name recon_r128_ep$e \
      > outputs/nt500/recon_ep$e.log 2>&1
  done
  log "card1 done" ) &

# ---- card 2: two more seeds for every NT number ------------------------------------------------
( free_card 2
  A2="--size 250m --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --floor_n 200 --probe_offset random --save_epochs 3,15,50 --batch 8 --accum 2 --out outputs/nt_seeds"
  for s in 1 2; do
    run "nt250m s$s" python -m pilot2.nt $A2 --data ecoli --seed $s --gpu 2 \
      > outputs/nt_seeds/ecoli_s$s.log 2>&1
    d=outputs/nt_seeds/nt250m_mlm_ecoli_s$s
    for e in 15 50; do
      [ -f $d/ckpt_ep$e.pt ] || { log "MISSING s$s ep$e"; continue; }
      run "nt s$s ep$e r=128" python -m pilot2.recon_audit --root $d --ckpt ckpt_ep$e.pt \
        --tiers 1,4,16 --max_probes 20 --sweeps 4 --restarts 128 --gpu 2 --name recon_r128_ep$e \
        > outputs/nt_seeds/recon_s${s}_ep$e.log 2>&1
    done
  done
  log "card2 done" ) &

# ---- card 3: DNABERT-2 on chromosome 22, where the records are real ----------------------------
( free_card 3
  run "bpe chr22 train" python -m pilot2.dnabert2 --data human --canary_npz $H/canaries_chr22.npz \
    --objective mlm --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 100 --epochs 150 \
    --save_epochs 15,30,50,80,120,150 --seed 0 --gpu 3 --out outputs/bpe_human \
    > outputs/bpe_human/train.log 2>&1
  d=outputs/bpe_human/dnabert2bpe_human_s0
  for c in ep30.pt final.pt; do
    [ -f $d/$c ] || { log "MISSING bpe chr22 $c"; continue; }
    run "bpe chr22 $c r=32" python -m pilot2.recon_bpe --root $d --ckpt $c \
      --tiers 1,4,16 --max_probes 20 --restarts 32 --sweeps 4 --gpu 3 --name recon_bpe_${c%.pt} \
      > outputs/bpe_human/recon_${c%.pt}.log 2>&1
  done
  log "card3 done" ) &
wait
log Q1014A_DONE
