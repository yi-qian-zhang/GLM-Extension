#!/bin/bash
# 10 Oct, GPU 2 only. The 5-mer branch of queue_1010a died on an assertion that is a real constraint,
# not a bug: non-overlapping k-mers need window % k == 0 and the window is 288 nt, so k=5 does not
# exist on our backbone (288 = 2^5 * 3^2; legal k are 1,2,3,4,6,8,9,12). DNABERT's own 5-mer is
# unaffected, because its k-mers overlap at stride 1. That freed GPU 2, and this queue uses it for the
# two gaps on the E. coli arm, which is the second real genome behind the objective claim:
#   * the masked cells have one model seed where the next-token cells have two;
#   * the 4-mer is missing on both, so the E. coli tokeniser axis has three points like human did.
# Arguments are copied from the existing cells of each root (they differ: the next-token arm scores
# snapshots with 50 canaries per tier and a 500-sequence ranking pool, the masked arm does not and
# uses 40 and 300), because the point is to put an error bar on numbers already in the log, and a
# re-run with different settings would not do that.
source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm
cd /data/wh/yqdata/GLM-Extension
export GLMEXT_DATA=/data/wh/yqdata/glm_data
L=outputs/queue_1010b.log
log(){ echo "$(date +%H:%M) $*" >> $L; }
log "start"

A="--data ecoli --n_train 5000 --tiers 1,4,16 --probes_per_tier 50 --n_nonmember 50 --pool 500 --floor_n 500 --probe_offset random --epochs 30 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --out outputs/ecoli_ar"
M="--data ecoli --n_train 5000 --tiers 1,4,16 --probes_per_tier 40 --n_nonmember 40 --pool 300 --floor_n 500 --probe_offset random --epochs 30 --out outputs/ecoli_mlm"

# second seed for the masked cells (char ~60 min, 3-mer ~8, 6-mer ~3)
for t in 6mer 3mer char; do for o in mlm@0.15 mlm@0.5; do
  python -m pilot2.run_pilot --tokenizer $t --objective $o --seed 1 --gpu 2 $M \
    > outputs/ecoli_mlm/${t}_${o/@/}_s1.log 2>&1; log "mlm $t $o s=1 done"
done; done

# the 4-mer, both objectives, two seeds
for s in 0 1; do
  python -m pilot2.run_pilot --tokenizer 4mer --objective ar --seed $s --gpu 2 $A \
    > outputs/ecoli_ar/4mer_ar_s$s.log 2>&1; log "ar 4mer s=$s done"
  for o in mlm@0.15 mlm@0.5; do
    python -m pilot2.run_pilot --tokenizer 4mer --objective $o --seed $s --gpu 2 $M \
      > outputs/ecoli_mlm/4mer_${o/@/}_s$s.log 2>&1; log "mlm 4mer $o s=$s done"
  done
done

python -m pilot2.analyze_objaxis --root outputs/ecoli_ar outputs/ecoli_mlm --data ecoli --epoch 30 --name ecoli30 \
  > outputs/ecoli_mlm/objaxis.log 2>&1
python -m pilot2.analyze_traj --root outputs/ecoli_ar outputs/ecoli_mlm > outputs/ecoli_mlm/traj.log 2>&1
log "Q1010B_DONE"
