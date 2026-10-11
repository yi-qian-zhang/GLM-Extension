#!/bin/bash
# 11 Oct, arm B of the robustness set: a SECOND human chromosome.
#
# "One human chromosome and one cohort" is the first limitation the paper lists, and it is the first
# thing a reviewer will ask about, because chromosome 22 is small, gene-dense and unusually repetitive.
# Chromosome 21 is the natural second: same cohort, same pipeline, independently built canaries.
# Data prep runs immediately; the GPU work waits for queue_1011a so nothing contends.
#
# Sources (both public, same release as the chr22 files already on disk):
#   hg38 chr21 reference  UCSC goldenPath
#   1000 Genomes phase 3 GRCh38 phased SNV+INDEL  EBI 20190312_biallelic_SNV_and_INDEL
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
H=$GLMEXT_DATA/human
L=outputs/queue_1011b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
mkdir -p outputs/human_chr21
log "start: fetching chr21"

if [ ! -f $H/chr21.fa ]; then
  curl -sL --retry 3 -o $H/chr21.fa.gz \
    https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr21.fa.gz && gunzip -f $H/chr21.fa.gz
  log "chr21.fa $(du -h $H/chr21.fa | cut -f1)"
fi
if [ ! -f $H/ALL.chr21.GRCh38.phased.vcf.gz ]; then
  curl -sL --retry 3 -o $H/ALL.chr21.GRCh38.phased.vcf.gz \
    http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/data_collections/1000_genomes_project/release/20190312_biallelic_SNV_and_INDEL/ALL.chr21.shapeit2_integrated_snvindels_v2a_27022019.GRCh38.phased.vcf.gz
  log "chr21 vcf $(du -h $H/ALL.chr21.GRCh38.phased.vcf.gz | cut -f1)"
fi

if [ ! -f $H/canaries_chr21.npz ]; then
  python -m pilot2.human_canary --vcf $H/ALL.chr21.GRCh38.phased.vcf.gz --fasta $H/chr21.fa \
    --out $H/canaries_chr21.npz > outputs/human_chr21/canary_build.log 2>&1
  log "canaries built: $(python -c "
import numpy as np; d=np.load('$H/canaries_chr21.npz'); print(d['seqs'].shape)" 2>/dev/null || echo '?')"
fi

until grep -q Q1011A_DONE outputs/queue_1011a.log 2>/dev/null; do sleep 120; done
log "gpus free, starting the released panel"

# identical to queue_human3.sh except for the chromosome: two seeds for the k-mer family, one for the
# two models that are not on the tokeniser axis
R="--objective causal --data human --fasta $H/chr21.fa --canary_npz $H/canaries_chr21.npz --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --stride 3 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_chr21"
B2="--objective causal --data human --fasta $H/chr21.fa --canary_npz $H/canaries_chr21.npz --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --score_epoch0 --probe_offset random --out outputs/human_chr21"
HY="--model hyenadna-medium-160k-seqlen-hf --data human --fasta $H/chr21.fa --canary_npz $H/canaries_chr21.npz --epochs 50 --probes_per_tier 50 --n_nonmember 50 --pool 100 --save_epochs 1,3,8,15,30,50 --snapshot_probes 50 --score_epoch0 --probe_offset random --out outputs/human_chr21"

( for s in 0 1; do python -m pilot2.dnabert --k 3 --seed $s --gpu 0 $R > outputs/human_chr21/k3_s$s.log 2>&1; log "k=3 s=$s done"; done ) &
( for s in 0 1; do python -m pilot2.dnabert --k 4 --seed $s --gpu 1 $R > outputs/human_chr21/k4_s$s.log 2>&1; log "k=4 s=$s done"; done
  python -m pilot2.dnabert2 --seed 0 --gpu 1 $B2 > outputs/human_chr21/bpe_s0.log 2>&1; log "dnabert2 s=0 done" ) &
( for s in 0 1; do python -m pilot2.dnabert --k 5 --seed $s --gpu 2 $R > outputs/human_chr21/k5_s$s.log 2>&1; log "k=5 s=$s done"; done ) &
( for s in 0 1; do python -m pilot2.dnabert --k 6 --seed $s --gpu 3 $R > outputs/human_chr21/k6_s$s.log 2>&1; log "k=6 s=$s done"; done
  python -m pilot2.hyena --seed 0 --gpu 3 $HY > outputs/human_chr21/hyena_s0.log 2>&1; log "hyena s=0 done" ) &
wait

python -m pilot2.analyze_real --root outputs/human_chr21 --name chr21 > outputs/human_chr21/analysis.log 2>&1
python -m pilot2.analyze_human --root outputs/human_chr21 --canary_npz $H/canaries_chr21.npz --name chr21 > outputs/human_chr21/human.log 2>&1
python -m pilot2.analyze_matched --root outputs/human_chr21 --name chr21 > outputs/human_chr21/matched.log 2>&1
log "Q1011B_DONE"
