# Experiment Log — Week 1 (22–26 September 2026)

**Project:** Isolating tokenization and pretraining objective in GLM memorization
**Owner:** Spencer Zong
**Branch:** `glmex` (GLM-Extension), commits `0591682` → `7a327f9`
**Compute:** TJU_6004 server, 4 × RTX 4090 24 GB, conda env `glm` (Python 3.10.18, torch 2.1.1+cu121)
**Raw reports:** `claude_notes/07_gate1_raw_reports.md`; server `outputs/pilot/`, `outputs/pilot_v2/`

---

## 1. Objective of the week

Gate 1 of the plan (`04_experiment_plan.md`): before committing to the ~90-run grid, establish that

- **Q1** the scorers are calibrated (return the analytic value on data with a known answer) and, for the masked model, agree with each other;
- **Q2** planted probes are measurable at all — r=16 > r=1 > never-seen beyond seed noise;
- **Q3** the two pretraining objectives differ under matched conditioning.

Secondary: measure real throughput (MFU) on the 4090s to replace the plan's 10–260 GPU-hour uncertainty.

---

## 2. Infrastructure

| Item | Result |
|---|---|
| SSH | key auth works; `TJU_6004` alias carries a RemoteForward that collides (port 17890) → use `TJU_6004_sync` |
| Sync | Mutagen session `glm-ext`, local ↔ `/data/wh/yqdata/GLM-Extension`, verified with a probe file (same-minute propagation). `.git`, `outputs/`, `__pycache__` excluded |
| conda | `source ~/.bashrc` is a no-op in non-interactive SSH (`$PS1` guard); use `source ~/miniconda3/etc/profile.d/conda.sh && conda activate glm` |
| GPU smoke | bf16 4096² matmul: 86–89 TFLOPS on GPUs 1–3 (GPU 0 lower on first call: warm-up) |
| Disk | `/data` 43 TB, 87% used, 5.4 TB free (shared server) |
| Git | branch `glmex` cut from `main`, upstream set; rule recorded in CLAUDE.md: never push `main` |

---

## 3. Pilot harness (`pilot/`, 8 files)

Standalone, pure PyTorch, no dependency on `src/`.

| File | Purpose |
|---|---|
| `data.py` | iid uniform DNA (GC = 0.5 exactly), 288-nt windows; 96-nt probes embedded at offset 96 inside distinct host windows, one host per repetition; **tags carried through the shuffle permutation** (construction-time tagging, asserted 1.0 precision/recall); val/test splits never contain probes |
| `model.py` | 4-layer pre-LN transformer, d=512, 8 heads, tied embeddings, 12.76M params; `causal=True/False` differs **only** in the attention mask |
| `train.py` | AdamW 3e-4, warmup 100, cosine to 10%, batch 64, bf16 autocast, grad clip 1.0; AR = CE over all 288 positions; MLM = CE only on masked positions (pure masking, no 80/10/10); val loss each epoch on the validation split; saves `best.pt` (lowest val) and `final.pt`; logs tokens/s and MFU vs 165 TFLOPS peak |
| `score.py` | scorers `ar`, `pll` (one masked copy per position), `prefix` (mask every position ≥ i, read i); all per-nucleotide log2; held-out floor check (`≥ 1.999` bits/nt); ranking vs a shared random pool with exact chance p = rank/(n+1); Carlini-2023 exact-match extraction from a 48-nt prefix (AR greedy / MLM strict left-to-right unmasking, both restricted to ACGT) |
| `run_pilot.py` | one cell end to end; `--checkpoint best\|final`, `--score_only`, `--smoke` |
| `report.py` | aggregates `scores*.json` → Gate-1 markdown (Q1/Q2/Q3, Mann-Whitney, Spearman) |
| `compare_ckpt.py` | best.pt vs final.pt side by side |
| `launch.sh`, `relaunch_mlm.sh`, `wait_and_report.sh` | server-side launchers; keep process patterns out of the SSH command line |

Design invariants: no padding anywhere (fixed length); no positional bookkeeping of probes; every metric per nucleotide; the 4.0 floor asserted for every scorer on every run.

---

## 4. Runs

### 4.1 Smoke (GPU 1/2, ~20 s each)
`--smoke`: 400 windows, 2 epochs, pool 30. Both paths ran; floors 2.013 (ar), 2.026 (pll/prefix). Steady-state MFU 0.33.

### 4.2 Pilot v1 — 4 cells, 20 epochs, scored at `best.pt`
Config: N_train = 5,000 (+340 probe hosts = 5,340), val 500, test 500; 20 probes × r ∈ {1, 16} + 40 non-member; pool 500; seeds 0/1.

| run | best epoch | train s | score s | MFU |
|---|---|---|---|---|
| ar_s0 | 3 | 43 | 19 | 0.34 |
| ar_s1 | 2 | 43 | 19 | 0.35 |
| mlm0.15_s0 | 13 | 47 | 1522 | 0.32 |
| mlm0.15_s1 | 13 | 46 | 1507 | 0.33 |

Floors: ar 2.0006–2.0010; pll 2.0002–2.0006; prefix 2.0002–2.0006. All OK.
Q1: pll vs prefix Spearman 0.960–0.991 (n = 80). Q2: r=16 vs non-member MWU p = 6e-8 … 9e-8 in all four runs, **but** effect tiny: r=16 bits/nt 1.992–1.995 vs 2.001; rank-1 0–20%; extraction 0/20 everywhere, Hamming ≈ 35/48 (chance 36). Q3: Δ = +0.001 bit — uninformative.

**Diagnosis.** On iid random data validation loss reaches its floor (2.000 bits) within 2–3 epochs; further training only memorizes the train set and nudges val loss up, so "lowest val loss" selects the **least memorized** checkpoint. `best.pt` at epoch 2–3 (AR) had barely trained.

### 4.3 Pilot v1 rescored at `final.pt` (score-only, no retraining)

| run / r=16 | median rank | rank-1 | bits/nt | exact 48-nt | Hamming |
|---|---|---|---|---|---|
| ar_s0 best → final | 39 → **1** | 0.05 → **1.00** | 1.992 → **0.586** | 0.00 → **0.65** | 35.2 → **2.0** |
| ar_s1 best → final | 34 → **1** | 0.20 → **1.00** | 1.993 → **0.664** | 0.00 → **0.70** | 35.0 → **1.8** |
| mlm0.15_s0 (prefix/train) | — → 12 | 0.00 | 1.994 | 0.00 | 31.2 |
| mlm0.15_s1 (prefix/train) | — → 32 | 0.00 | 1.993 | 0.00 | 31.1 |

r=1 (AR, final): median rank 48–77, rank-1 5–10%, MWU p vs non-member 0.007–0.012. Non-member: median rank 252–290 (chance), no false positives. Floors: ar 2.021–2.022 (slight overfit, still ≥ 2.0); pll/prefix 2.0004–2.0005.

### 4.4 Pilot v2 — 4 cells, 50 epochs, tiers r ∈ {1, 16, 64}, scored at `final.pt`
N_train = 5,000 + 1,620 hosts = 6,620 (24% of windows carry a probe — noted).

**Causal (ar_s0 / ar_s1):** held-out floor 3.14 / 2.89 bits (heavily overfit, still ≥ 2.0). r=1: rank-1 100%, bits 0.74 / 0.90 (train host), 1.49 / 1.33 (fresh host), exact extraction 5%. r=16: bits 0.08, rank-1 100%, exact 100%. r=64: bits 0.06, exact 100%. Non-member: rank 251–268, bits 4.4–4.6 (model assigns *below*-chance likelihood to unseen data).

**Masked@0.15 (s0 / s1):**
- `pll`: floor 2.0006–2.0008. r=1 nothing (rank 157–304). r=16 rank 12–16, rank-1 30–45%, bits 1.985–1.990. r=64 rank 1, rank-1 100%, bits 0.099 / 0.134, z ≈ +285…+342. Exact extraction: r=64 **15–20%**, r≤16 0%.
- `prefix`: floor **2.037 / 2.054** (off calibration); non-member bits 2.10 / 2.14; r=16 bits 2.10 / 2.25 (**worse than chance**, rank 288–331); r=64 bits 1.05 / 1.24, rank-1 95–100%.
- Q1 at 50 ep: pll vs prefix Spearman **0.40–0.69** (was 0.96–0.99 at 20 ep when both were at floor).

### 4.5 Q3 under matched conditioning (`ar/train` vs `prefix/train`, r=16)
AR 0.081 / 0.084 bits, 100% verbatim; MLM 2.097 / 2.239 bits, 0% verbatim. Δ = +2.09 bits (seed spread AR ±0.001, MLM ±0.07). Caveat: prefix scorer is off-calibration on the MLM (above); under `pll` the MLM r=16 value is 1.985–1.990, still ≈ 2 bits above AR.

---

## 5. Findings

1. **Checkpoint-selection hazard (confirmed decisively).** Val-loss selection on iid data picks the least memorized epoch. Same weights trajectory, scored at final.pt: rank-1 5–20% → 100%, extraction 0% → 65–70%. Rule for the grid: **score `final.pt` on every synthetic cell**; report both where a validation split is meaningful (real genomes). The reference pipeline selects the same way, on the test split — to raise with Alex as a plausible third contributor to its near-chance low-repetition tiers.
2. **Scorer disagreement on low-mask MLMs.** `pll` stays on the floor (2.0006); `prefix` drifts (2.04–2.05) and ranks r=16 probes below chance on a 15%-mask model. **Decision (user): keep both scorers everywhere, each with its own floor check; flag, don't drop.** The mask rate at which they re-converge is an E2 result; `prefix` remains the matched-conditioning instrument for E3.
3. **Objective effect is large.** Same data, same epochs: causal fully memorizes r=16; masked@0.15 needs r=64 to reach rank-1 100% and even then only 15–20% is extractable verbatim → "present but not extractable", measurable. Masked sees 6.7× fewer supervised tokens per epoch → **dual budget (fixed epochs AND fixed supervised tokens) is mandatory**.
4. **Saturation.** AR at 50 epochs is a lookup table (held-out 2.9–3.1 bits). Epoch count is a real experimental knob, not a nuisance.
5. **Throughput.** MFU 0.32–0.35; training for the full 90-run grid < 1 h. Scoring dominates: MLM PLL ≈ 25 min/run at 2048 rows/batch (4096 OOMs at ~20 GB). Optimize scoring next.
6. **Non-member probes never false-positive** in any run, any scorer, any checkpoint.

---

## 6. Problems hit and fixes

| Problem | Fix |
|---|---|
| Bash heredoc broke on quotes in source files | write source with the file tool, not heredocs |
| `conda: command not found` over SSH | source `conda.sh` directly |
| numpy segfaults in the local Git-Bash Python | never run project code locally; server only |
| Val-loss checkpoint selection hid the signal | `--checkpoint final`, `--score_only`; rescore without retraining |
| PLL scoring OOM at 4096 rows/batch | 2048 rows (~10 GB) |
| `pkill -f <pattern>` and `grep <pattern>` killed the invoking SSH shell (its own command line matched) — twice, also killing a background monitor | all server-side logic moved into repo scripts (`relaunch_mlm.sh`, `wait_and_report.sh`); SSH command line contains only `bash pilot/x.sh` |
| Plan's Q1 as written was a null test (PLL on a causal model ≡ AR scoring) | Q1 redefined on the MLM model's two scorers |

---

## 7. Decisions taken

- Score `final.pt` on all synthetic cells (documented as an instrument hazard in E0, golden test to add).
- Keep both MLM scorers; per-scorer floor column in every results table.
- Dual optimization budget is mandatory for E1/E2.
- E2 (mask-rate sweep) promoted to run alongside E1 in week 4.
- Venue stance unchanged: build to NeurIPS, expect SaTML, decide at Gate 3.

## 8. Open items

- Faster MLM scoring (batching across probes; fewer masked copies via position subsampling with correction).
- Golden tests: padding fraction = 0 (already true by construction), probe precision/recall = 1.0 (asserted), floor ≥ 1.999 per scorer per run (report flag → CI assert), `final.pt` used on synthetic cells.
- Alex 1:1 (harness walkthrough, coauthorship, checkpoint-selection observation).
- Confirm NeurIPS 2027 / SaTML 2028 deadlines; HPC request as backstop.
- v2 has 24% probe-carrying windows — fine for a pilot, not for the grid (plan: 5.8%).
