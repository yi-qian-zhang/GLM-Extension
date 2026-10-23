# Experiment Log — Week 2 (25–28 September 2026)

**Project:** Architecture Was Not the Variable — isolating tokenizer and pretraining objective in GLM memorization
**Owner:** Spencer Zong
**Branch:** `glmex` (GLM-Extension), commits `7b3f0f9` → `a3907fe`
**Compute:** TJU_6004 server, 4 × RTX 4090 24 GB, conda env `glm`
**Harness:** `pilot2/` (new; `pilot/` frozen as the week-1 version; Alex's `src/`, `experiments/`, `config/` untouched)
**Figures and tables:** `claude_notes/figures/`; raw outputs on the server under `outputs/<run>/`

---

## 0. The idea, in one paragraph

The BCB'26 paper compares four genomic language models and attributes their memorization differences to architecture. Those four models also differ in tokenizer, pretraining objective and size, so the attribution is not identified — the paper's own Discussion (L567–570) says a controlled ablation is needed. We build that ablation: one fixed 12.9M-parameter Transformer backbone (d=512, 4 layers, 8 heads, pre-LN, tied embeddings), and vary only **tokenizer granularity** (char / 3-mer / 6-mer / BPE) and **pretraining objective** (causal AR vs masked MLM at several mask rates). Models are trained on synthetic iid uniform DNA (exact entropy 2.000 bits/nt, so the chance floor is known analytically) with planted canary probes at repetition tiers r ∈ {0, 1, 4, 16}. The deliverable is a variance decomposition of measured memorization into tokenizer / objective / interaction / seed. Every outcome is publishable. Alex's extension #2 is the core, #3 (bounded-prior membership privacy) is the reporting standard, #1 (corpus scaling) is a control.

Memorization is measured three ways, all per nucleotide: probe bits/nt (2.000 = nothing memorized), rank-1 rate of the probe against a 500-sequence random pool, and exact 48-nt prefix extraction (Carlini 2023). "Held-out floor" = bits/nt on never-seen data; above 2.000 means the model is overfit.

---

## 1. Objectives of the week

1. Extend the harness from one tokenizer to the tokenizer axis (`pilot2/`) with identical non-embedding parameters.
2. Build the E0 null battery (does the instrument produce signal where there is none?).
3. First look at E2 (mask-rate dose-response).
4. First full tokenizer × objective grid (tok1) and a first variance decomposition.
5. Answer the question tok1 raised: do coarse tokenizers memorize **more**, or only **sooner**? (traj1, traj2)
6. Rule out the obvious alternative explanation: the 6-mer embedding table has ~2M extra parameters. (cap1–cap4)

---

## 2. Harness changes (`pilot2/`)

| File / flag | What it does | Commit |
|---|---|---|
| `tokenizers.py` | char / k-mer tokenizers; non-embedding params identical (12.61M) across all | `ff0bc97` |
| `null_battery.py` | untrained-model rank uniformity (KS test), blind surface-statistics baseline | `df41cd4` |
| `real_data.py` | E. coli K-12 MG1655 window loader, probes embedded as in synthetic (not yet smoke-tested) | `4d471ca` |
| `train_bpe.py` | BPE-4096 over {A,C,G,T}, measures nt/token k on each corpus | `a3e3d67`, `4ae8ca0` |
| `analyze_e2.py` | E2 dose-response table + figure | `d91d221` |
| `analyze_tok.py` | tokenizer × objective table + two-way sum-of-squares decomposition | `f5e5e50` |
| `--save_epochs --score_snapshots` | trajectory snapshots, scored and then deleted (shared disk) | `5dd3d80` |
| `analyze_traj.py` | trajectory table, 4-panel figure, several roots overlaid, **matched-overfitting interpolation table** | `dfa0095`, `ee53add`, `bdb5428` |
| `--d_ff`, `--emb_rank` | capacity controls: slimmer body; factorized tied embedding (ALBERT-style) | `0021e20` |
| `--emb_lr_mult` | learning-rate multiplier on the token embedding only | `a3907fe` |
| `report.py` fix | read `hamming_nt` (pilot2 field name); the missing field had silently blocked two reports | `3422e92` |

All new flags default to off; a regression rerun with the latest code reproduces traj1 digit for digit (§4.7).

---

## 3. Runs (all on `final.pt`; tmux session names in brackets)

| Run | Grid | Wall time |
|---|---|---|
| E0 null battery [`null1`] | untrained char / 3mer / 6mer, AR + MLM scorers | ~20 min each |
| E2-lite (`outputs/e2lite`) | char × {AR, MLM m=0.05/0.15/0.30/0.50/0.80} × 2 seeds, 30 ep, r ∈ {1,4,16} | 1.75 h |
| tok1 (`outputs/tok1`; last cell [`tok1fix`]) | {char, 3mer, 6mer} × {AR, MLM 0.15, MLM 0.50} × 2 seeds = 18, 30 ep | — |
| traj1 [`traj1`] | AR × {char, 3mer, 6mer} × 2 seeds, 30 ep, snapshots at 1,2,3,5,8,12,20,30 | 8 min |
| traj2 [`traj2`] | char AR × 2 seeds, 100 ep, snapshots at 20…100 | ~10 min |
| cap1 [`cap1`] | 6mer AR × 2 seeds: `--emb_rank 27`, `--d_ff 1568` | 8 min |
| cap2 [`cap2`] | 6mer AR: `--emb_rank 64/128/256` (30 ep), `--emb_rank 27` (100 ep) | ~15 min |
| cap3 [`cap3`] | 6mer `--emb_rank 512` (30 ep); char `--emb_rank 512` (100 ep) | ~8 min |
| cap4 [`cap4`] | 6mer `--emb_lr_mult 0.3/0.1`; 3mer `--emb_rank 512`; 6mer default regression (seed 0) | ~10 min |

Data for every run: 5,000 training windows of 288 nt, 500 val, 500 test, 20 probes per tier, 40 non-member probes, pool 500, data seed 1234.

---

## 4. Results

### 4.1 E0 null battery — PASS for all three tokenizers

| tokenizer | untrained model: rank distribution | rank-1 (expected 0.002) | blind baseline AUC |
|---|---|---|---|
| char | uniform (KS 0.045–0.087 < 0.136) | 0.000 | 0.552 ± 0.075 |
| 3mer | uniform (KS 0.057–0.119 < 0.136) | 0.000 | 0.552 ± 0.075 |
| 6mer | uniform (KS passed) | 0.005 | 0.55 |

The instrument produces no signal where none exists, for every scorer. The blind AUC is identical across tokenizers because it only sees the (shared) data.

### 4.2 BPE granularity is corpus-dependent

BPE-4096 trained on E. coli: **k = 5.01** nt/token on E. coli, **4.71** on uniform random DNA. So "BPE" is not one granularity — k must be measured per corpus, and DNABERT-2's own k has never been published.

### 4.3 E2-lite — mask-rate dose-response (char, r=16, fresh host, pll scorer)

| objective | probe bits/nt | rank-1 | exact extraction |
|---|---|---|---|
| MLM m=0.05 | 1.996 | 0.25 | 0 |
| MLM m=0.15 | 1.989 | 0.35 | 0 |
| MLM m=0.30 | 1.973 | 0.85 | 0 |
| MLM m=0.50 | **1.937** | 0.95 | 0 |
| MLM m=0.80 | 1.972 | 0.85 | 0 |
| AR | **0.542** | 1.00 | 0.43 (0.95 on the training host) |

MLM memorization rises and then falls with mask rate (peak at 0.5). AR is not on the MLM curve at all. Every MLM model is at 0% exact extraction: "present but not extractable".

### 4.4 tok1 — full 18-cell grid (r=16, training host, natural scorer)

| tokenizer | objective | probe bits/nt | rank-1 | exact | held-out floor |
|---|---|---|---|---|---|
| char | AR | 0.432 | 1.00 | 0.95 | 2.039 |
| char | MLM 0.15 | pll 1.990 / prefix 1.991 | 0.35 | 0 | 2.000 |
| char | MLM 0.50 | pll 1.934 / prefix 1.946 | 0.90 | 0 | 2.004 |
| 3mer | AR | 0.001 | 1.00 | 1.00 | 4.092 |
| 3mer | MLM 0.15 | pll 0.450 / prefix 1.149 | 1.00 | 0.15 | 2.004 |
| 3mer | MLM 0.50 | pll 0.156 / prefix 0.572 | 1.00 | 0.75 | 2.005 |
| 6mer | AR | 0.001 | 1.00 | 1.00 | 2.522 |
| 6mer | MLM 0.15 | pll 0.721 / prefix 1.075 | 1.00 | 0.12 | 2.035 |
| 6mer | MLM 0.50 | pll 0.105 / prefix 0.219 | 1.00 | 1.00 | 2.056 |

**Variance decomposition of r=16 probe bits/nt (n = 18):**

| source | share |
|---|---|
| tokenizer | **59.5%** |
| objective | 25.7% |
| tokenizer × objective | 14.0% |
| seed | 0.8% |

Within masked models the tokenizer explains 92.7%; within causal models, 100%. Coarser tokens memorize far more; "present but not extractable" holds only for char; pll and prefix scorers diverge more on coarse tokens. No false positives on non-member probes.

### 4.5 traj1 + traj2 — more, or only sooner?

**Sooner: confirmed.**

| milestone | 6mer | 3mer | char |
|---|---|---|---|
| r=16 probe rank-1 reaches 100% | epoch 2 | epoch 3–5 | epoch 8 |
| r=16 probe first exactly extractable | epoch 3 | epoch 5 | epoch 20–30 |

**More: also confirmed.** Aligning runs by held-out floor (equal generalization cost) instead of by epoch. Probe bits/nt interpolated at each floor, mean of 2 seeds (lower = more memorized):

| held-out floor | 2.05 | 2.10 | 2.20 | 2.40 |
|---|---|---|---|---|
| r=1: 6mer / 3mer / char | 1.65 / 1.87 / 1.95 | 1.21 / 1.74 / 1.89 | **0.61 / 1.52 / 1.77** | 0.04 / 1.14 / 1.60 |
| r=4 | 1.21 / 1.46 / 1.70 | 0.55 / 1.14 / 1.37 | 0.15 / 0.86 / 0.94 | 0.02 / 0.46 / 0.77 |
| r=16 | 0.22 / 0.31 / 0.33 | 0.07 / 0.19 / 0.27 | 0.02 / 0.16 / 0.23 | 0.004 / 0.11 / 0.20 |

- Ordering 6mer > 3mer > char in memorization holds at every tier across 2.05–2.40.
- Only exception: r=16 at floor 2.03, where 6mer is still in its first 3 epochs.
- char needs a held-out floor of 5.5–5.8 (100 epochs) to memorize what 6mer memorizes at 2.5.
- **The memorization-vs-floor curve is schedule-invariant:** char under a 30-epoch and a 100-epoch cosine schedule traces the same curve. This justifies floor-matching as the second axis of the dual budget.
- Seeds nearly coincide; false positives ≤ 5%.

Figure: `figures/traj12_trajectory.png`.

### 4.6 cap1–cap4 — is it the extra parameters?

char has 12.762M parameters; 6mer 14.734M (its 4096-row embedding table). Non-embedding parameters are identical (12.61M).

r=1 probe bits/nt at matched held-out floor (mean of 2 seeds):

| variant | total params | @2.05 | @2.10 | @2.20 | @2.40 |
|---|---|---|---|---|---|
| 6mer, default | 14.73M | 1.65 | 1.21 | 0.61 | 0.04 |
| 6mer, **slimmer body** `--d_ff 1568` | 12.77M | 1.65 | 1.24 | 0.67 | 0.06 |
| 6mer, factorized embedding rank 27 | 12.76M | 1.92 | — | — | — |
| 6mer, factorized rank 27, 100 ep | 12.76M | 1.91 | 1.80 | 1.63 | 1.32 |
| 6mer, factorized rank 64 / 128 / 256 | 12.9–13.8M | 1.90 / 1.88 / 1.86 | 1.79 / 1.76 / 1.71 | — / 1.52 / 1.49 | — / 1.24 / 1.19 |
| 6mer, **factorized rank 512** (same function class) | 15.00M | 1.83 | 1.68 | **1.44** | 1.03 |
| 6mer, embedding LR × 0.3 | 14.73M | 1.40 | 0.62 | — | — |
| 6mer, embedding LR × 0.1 | 14.73M | **1.18** | — | — | — |
| 3mer, default | 12.69M | 1.87 | 1.74 | 1.52 | 1.14 |
| 3mer, factorized rank 512 | — | 1.87 | 1.74 | 1.53 | 1.22 |
| char, default | 12.76M | 1.95 | 1.89 | 1.77 | 1.60 |
| char, factorized rank 512 | 13.02M | 1.96 | 1.89 | 1.77 | 1.58 |

Reading:

1. **Total parameter count is not the explanation.** Removing 2M parameters from the body (slimmer body) leaves 6mer unchanged.
2. **The 6mer excess over 3mer is implementation-sensitive.**
   - The rank-512 factorization is a pure reparametrization. Input embedding E' = E·Wᵀ and output head x·W·Eᵀ = x·E'ᵀ, so it is the same function class with the same tie. Yet it drops 6mer to about the 3mer level (0.61 → 1.44 at 2.20).
   - Ranks 27–256 behave the same as 512. So this is not a dose-response in embedding parameters.
3. **The obvious mechanism is refuted.** The hypothesis was "the embedding rows get a high effective learning rate". Lowering only the embedding LR makes 6mer memorize *more* per unit of overfitting, not less.
4. **char < 3mer is robust.** Factorization leaves char and 3mer unchanged, and their tables are tiny and parameter counts nearly equal. This part of the tokenizer effect is capacity-clean and parametrization-invariant.
5. **Regression check:** 6mer default rerun with the latest code (all new flags at defaults) reproduces traj1 exactly.

Figure: `figures/cap_all_trajectory.png`; full table `figures/cap_all_trajectory.md`.

### 4.7 lenbig (a) — Kharitonov's sequence-length hypothesis: REFUTED in this regime

`3mersp` / `6mersp` = the k-mer vocabulary, with k−1 unscored FILL tokens after each content token, so every window is 288 positions long (the same as char). The information per content token is unchanged. AR, 2 seeds, 30 epochs (commit `1464f5b`, tmux `lenbig`).

Probe bits/nt at matched held-out floor:

| variant | seq length | r=1 @2.10 | r=1 @2.20 | r=4 @2.20 | r=16 @2.20 |
|---|---|---|---|---|---|
| char | 288 | 1.89 | 1.77 | 0.94 | 0.23 |
| 3mer | 96 | 1.74 | 1.52 | 0.86 | 0.16 |
| **3mer spaced** | **288** | 1.74 | **1.48** | 0.71 | 0.08 |
| 6mer | 48 | 1.21 | 0.61 | 0.15 | 0.02 |
| **6mer spaced** | **288** | 1.38 | **0.70** | 0.12 | 0.02 |

Stretching the sequence 3–6× to char length leaves memorization essentially where the k-mer model was, and far from char. **What drives the effect is the granularity of the prediction unit (k nucleotides predicted jointly by one softmax), not the token-sequence length.** In NLP, BPE couples length, vocabulary and frequency, so Kharitonov et al. could only conjecture by exclusion. Here the two are decoupled cleanly.

Caveat: the spaced model has extra (deterministic) positions it can attend to. A reviewer may call this "extra compute slots", but it cuts against the finding, since more slots did not reduce memorization.

### 4.8 lenbig (b) — above model capacity (big20x), 2 seeds

Training set ×20: 100,000 windows ≈ 57.6M bits, above the ~45M-bit capacity estimate of Morris et al. (3.6 bits/param × 12.6M). AR, seeds 0 and 1, 30 epochs (47,100 steps). Scored at epoch 30.

Each cell reads bits/nt / rank-1 / exact extraction; the two values in a cell are seed 0 / seed 1.

| tokenizer | held-out floor | r=1 | r=4 | r=16 | false positives |
|---|---|---|---|---|---|
| char | 2.000 / 2.000 | 2.000 / 0 / 0 | 2.000 / 0 / 0 | **1.999–2.000 / 0 / 0** | 0 |
| 3mer | 2.002 / 2.004 | 1.996–1.998 / 0–0.05 / 0 | 1.990–1.998 / 0–0.05 / 0 | 1.980–1.994 / 0–0.20 / 0 | 0 |
| 6mer | 2.560 / 2.544 | 1.26–1.34 / **1.00** / 0 | 0.85–1.00 / **1.00** / 0 | **0.12–0.17 / 1.00 / 1.00** | 0 |

**Reading.**

- Above capacity the tokenizer effect becomes **qualitative**, and it replicates across seeds.
- char memorizes *nothing*: every canary is at chance, including those seen 16 × 30 = 480 times. The model does not overfit.
- 3mer is essentially at chance.
- 6mer recognizes every member canary, including those seen only once per epoch (r=1: rank-1 100%). It extracts every 16× canary verbatim (from epoch 8), and it overfits to 2.55 held-out bits.
- No false positives anywhere.
- Real GLMs are pretrained far above capacity, which is this regime, and the 6-mer tokenizer is the one DNABERT and Nucleotide Transformer use.

**Hypothesis to test.** 6mer overfits although the data exceed the capacity estimate. This suggests that *effective* capacity (bits stored per parameter) depends on the tokenizer. Morris et al. measured 3.6 bits/param at a single tokenization. It is measurable directly: train-set bits saved relative to 2.000, summed over the corpus.

**Caveat.** 20× data at a fixed epoch count also means 20× more steps and 20× more non-canary updates between canary exposures, so "capacity" and "interference / forgetting between exposures" are not yet separated. A smaller-model point at 1× data would separate them.

At matched held-out floor, 6mer-big20x memorizes less than 6mer at 1× data (r=1 @2.20: 1.66 vs 0.61), so the memorization-vs-floor curve depends on corpus size. Floor-matching is comparable only within one corpus size.

### 4.9 off1 — random probe offsets: the repetition effect was largely POSITION-ANCHORED

**Why.** In every run so far, each probe copy sat at nt 96 of its host. That offset is token-aligned for k = 3 and 6, and it is the same absolute position in every copy. Real duplicated sequences occur at arbitrary offsets inside training windows. `--probe_offset random` draws each copy's offset uniformly from 0–192, from a separate random stream, so the hosts and probes are identical to the fixed runs.

- Scoring: the scored span is widened to whole tokens. Extraction enforces the letters already revealed inside the first generated token.
- Regression: fixed mode reproduces traj1 digit for digit (commits `7b6ade7`, `f91fa2a`; tmux `off1`).
- Setup: AR × char/3mer/6mer × 2 seeds, 30 epochs.

**Result** (r=16, bits/nt / rank-1 / exact extraction, mean of 2 seeds; `figures/off1_offset_report.md`):

| tokenizer | fixed: training host | fixed: NEW host, same position 96 | random: training host (own offset) | random: new host, new offset |
|---|---|---|---|---|
| char | 0.41 / 1.00 / 0.95 | **0.52 / 1.00 / 0.50** | 1.93 / 0.45 / 0.00 | **2.06 / 0.00 / 0.00** |
| 3mer | 0.001 / 1.00 / 1.00 | **0.50 / 1.00 / 0.35** | 0.009 / 1.00 / 1.00 | **4.02 / 0.05 / 0.00** (chance for this overfit model ≈ 4.19) |
| 6mer | 0.001 / 1.00 / 1.00 | **0.15 / 1.00 / 1.00** | 0.012 / 1.00 / 1.00 | in-phase **2.18 / 0.33 / 0.00**; out-of-phase 2.49 / 0.00 / 0.00 (chance ≈ 2.51) |

**Reading.**

1. **Most of the "repetition" memorization we measured was anchored to absolute position.**
   - With fixed placement, a 16× probe moved into a brand-new context *at the same position* is still recognized (100%) and extracted (char 50%, 6mer 100%).
   - With random placement, the same probe in a new context at a new position is essentially not recognized by any tokenizer.
   - For char, repetition gives no benefit at all: r=16 at its own training host 1.93 ≈ r=1 1.93, versus 0.41 with fixed placement.
   - The backbone uses learned absolute position embeddings. With consistent placement, the 16 copies reinforce one (position, content) association; with random placement they do not consolidate into a position-free memory within 30 epochs.
2. **For k-mer models, what does transfer depends on tokenization phase.** 6mer r=16 in a new context: rank-1 33% when the new offset shares a k-mer phase with a training copy, 0% when it does not. The same nucleotides under a shifted tokenization are, to the model, a different sequence.
3. **Example-level (whole-window) memorization is unaffected, and the tokenizer ordering holds.**
   - At the training host every k-mer model still recognizes and extracts every probe at any offset (it memorizes whole training windows).
   - At matched held-out floor (train host, r=1): 6mer 0.63 / 3mer 1.63 at 2.20, versus 0.61 / 1.52 with fixed placement.
   - But tiers r=1/4/16 collapse onto one curve: repetition stops mattering.
4. **Consequences.**
   - (a) Our tier results with fixed placement overstate how repeated sequences are memorized independently of context. Adopt random placement as the default for the grid and report fixed placement as the special case.
   - (b) Alex's canaries are standalone 64-nt sequences, so every copy starts at position 0. That is the same anchoring: raise it in the 1:1 as a question, not in writing.
   - (c) Positional encoding becomes a design variable in the realistic setting. Real GLMs differ here: DNABERT uses learned absolute positions, DNABERT-2 uses ALiBi (relative), HyenaDNA is convolutional. This is the one place where "architecture" plausibly *does* matter, and we can test it on our backbone by swapping the absolute embedding for a relative one (RoPE/ALiBi).
   - (d) Open: does repetition start to matter with random placement under longer training (100 epochs), or with a relative-position backbone?

**Sanity.**
- Extraction at misaligned offsets works: k-mer train-host r=16 extraction is 100% at random offsets, so the constrained decoding is correct.
- char has no alignment issue at all (k=1), so its collapse cannot be a scorer artifact.
- Non-member false positives ≤ 1%.

### 4.10 off2 + rope1 (2 Oct) — longer training does not help; relative position encoding does

Two follow-ups to §4.9, both AR × char/3mer/6mer × 2 seeds.

- **off2:** random placement, 100 epochs (tmux `off2`).
- **rope1:** rotary relative positions (`--pos_enc rope`, commit `ba174a0`), 30 epochs, with random and with fixed placement (tmux `rope1`). RoPE has the same block shape and the same non-embedding parameters (12.611M) as the default body. Checks: attention scores depend only on relative offset, no causal leak, old checkpoints load unchanged.

**r=16 probe shown in a brand-new host: rank-1 recognition (exact extraction in brackets), mean of 2 seeds**

| position encoding | placement | char | 3mer | 6mer |
|---|---|---|---|---|
| absolute | fixed (same position) | 100% (50%) | 100% (35%) | 100% (100%) |
| absolute | random, 30 epochs | 0% (0%) | 5% (0%) | 32% (0%) |
| absolute | random, **100 epochs** | 0% (0%) | 5% (0%) | 37% (0%) |
| **RoPE** | fixed (same position) | 22% (0%) | 100% (0%) | 100% (100%) |
| **RoPE** | random, 30 epochs | 0% (0%) | **30%** (0%) | **80%** (3%) |

**Reading.**

1. **Training three times longer does not consolidate a position-free memory** under absolute positions: 0 / 5 / 37% at 100 epochs versus 0 / 5 / 32% at 30.
2. **Position encoding is a real switch for k-mer models.** With relative positions and random placement, recognition in a new context rises from 5% to 30% for 3mer and from 32% to 80% for 6mer. Verbatim extraction in a new context stays near zero.
3. **For char, absolute positions were the whole effect.**
   - With RoPE, even fixed placement gives only 22% recognition and 0% extraction in a new context.
   - At its own training host, the r=16 probe goes from 0.41 bits/nt (absolute, fixed) to 1.85 (RoPE, fixed).
   - So the char model's fast memorization of repeated probes in all earlier runs came from the absolute position table.
4. **The tokenizer ordering is unchanged and, if anything, sharper under RoPE.** At matched held-out floor 2.20 (r=1, training host): 6mer 0.57–0.58, 3mer 1.55–1.62, char not yet reached in 30 epochs (1.95–1.96 at 2.05).
5. **For the paper.**
   - Positional encoding is a third design axis that interacts with the tokenizer: coarse tokens plus relative positions give content memory that survives a change of position and context.
   - Real GLMs differ exactly here: DNABERT uses learned absolute positions, DNABERT-2 uses ALiBi, HyenaDNA is convolutional.
   - This is the part of "architecture" that our data say does matter.

**Caveats.**
- The 6mer random-placement numbers are for fresh offsets whose k-mer phase matches a training copy (39 of 40 probes at r=16). The single out-of-phase probe is at 0%.
- char under RoPE has only reached a held-out floor of ~2.07 in 30 epochs; a 100-epoch RoPE char run is needed before concluding it never forms the memory.

---

## 5. Findings of the week

1. **The tokenizer is the dominant factor** (59.5% of variance, 92.7% within masked models) on a fixed backbone. The published cross-model comparison therefore cannot attribute differences to architecture.
2. **Coarse tokenizers memorize both sooner and more.** At equal generalization cost they leak far more of the training set. Stopping training earlier does not remove the effect.
3. **Robust claim:** 6mer ≥ 3mer > char in every variant tried. The char → 3mer step is invariant to capacity and parametrization.
4. **Sensitivity claim:** the size of the large-vocabulary excess ranges from ≈ 0 (factorized embedding) to large (low embedding LR), for identical function classes. Memorization is a property of the training dynamics, not only of the model's function class. This strengthens the paper's thesis that an architecture label is not the variable. Reported as a range; mechanism not pursued yet.
5. **Objective:** MLM memorization is non-monotone in mask rate (peak 0.5); AR is off the MLM curve; MLM on char is "present but not extractable".
6. **Mechanism (new):** Kharitonov's sequence-length conjecture is refuted in the clean DNA test. Granularity of the prediction unit, not length, drives memorization (§4.7).
7. **Capacity (new, 2 seeds):** above model capacity, char/3mer memorize nothing (even 480 exposures). 6mer recognizes every member canary and extracts every 16× canary (§4.8).
8. **Instrument:** null battery passes for every tokenizer and scorer. The two MLM scorers (pll, prefix) diverge more on coarse tokens. Both are kept.

---

## 6. Problems hit and fixes

| Problem | Fix |
|---|---|
| `report.py` read `hamming`, pilot2 writes `hamming_nt` → KeyError; tok1/traj1 reports never written and the waiting null1 job blocked | field name fixed (`3422e92`), reports regenerated, null1 released automatically |
| Report rerun printed "no runs found" | must pass `--scores_name scores_final.json` |
| Trajectory panel unreadable (x-axis stretched to 4.1 bits) | zoom panel + one colour per tokenizer |
| char AR only reached floor 2.04 in 30 epochs → comparison band too narrow | traj2 at 100 epochs; analysis overlays several roots |
| Python `write_text` on Windows wrote CRLF, whole-file diffs | `sed -i 's/\r$//'`; later edits use `newline="\n"` |
| Assumed the factorized-rank control measured capacity | cap2/cap3 showed it is a reparametrization effect; interpretation corrected in the board |

---

## 7. Decisions taken

- Floor-matched comparison is the second budget axis (alongside fixed epochs / fixed supervised tokens).
- Every code change is committed and pushed to `glmex` immediately.
- Parametrization sensitivity is reported as a robustness range, not chased mechanistically for now.
- Both MLM scorers remain in every table.

## 8. Open items

1. MLM trajectories for 3mer / 6mer (so "more vs sooner" is shown for both objectives).
2. Real-data arm: smoke-test `real_data.py`, rerun a reduced grid on E. coli.
3. BPE in the scorer (requires whole-window ranking; BPE excluded from extraction).
4. Faster MLM scoring (PLL is ~25 min per run).
5. Formal dual-budget runs (fixed supervised tokens).
6. Mechanism of the parametrization effect (initialization scale? weight decay on the product?) — only if reviewers need it.
7. Alex 1:1 (email draft in `10_email_to_Alex_draft.md`); confirm deadlines; HPC request.
