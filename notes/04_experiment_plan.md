# Experiment Plan

**Project:** Isolating tokenization and pretraining objective in GLM memorization
**Owner:** Spencer Zong
**Date:** 2026-09-25 (rev. 2; original 2026-09-18)
**Compute:** 4 × RTX 4090 (local), HPC as backstop
**Venue stance:** build to the NeurIPS standard, expect SaTML. The final target is decided at Gate 3 (week 12), not now.

---

## 0. Design decisions fixed before any run

Do not defer these. Each one bites in week 12 if left open.

| Decision | Value | Rationale |
|---|---|---|
| Host window length | **288 nt** | Divisible by 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 96 — character, 3-mer and 6-mer all tile exactly, no boundary fudge |
| Probe (canary) length | **96 nt** | Same divisibility: 96/3 = 32 tokens, 96/6 = 16 tokens |
| Probe placement | **Offset 96 inside the host window** (a multiple of 6) | Keeps k-mer token frames identical across tokenizers |
| Probe insertion | **Embedded inside host windows, tagged at construction** | Length-matched by construction; no position bookkeeping; no membership signal from sequence length |
| Corpus size | **N = 15,000 windows** | Fits E. coli (16,116 windows at stride 288) so N is constant across synthetic and real arms |
| Repetition tiers | **r ∈ {1, 4, 8, 16}, 30 probes per tier** | 30/tier meets the proposal's own power requirement (≥ 30 canaries per configuration). Insertions = 870 → 5.8% of windows, 1.9% of tokens |
| Parameter matching | Non-embedding params fixed (4 layers, d = 512, 8 heads). **Tied input/output embeddings.** Embedding params reported as a covariate. One capacity-matched control cell with reduced d_model for large-vocab arms | Vocab 8 → 4k embedding params; vocab 4096 → 2.1M. Without this, tokenizer is confounded with capacity |
| Padding | **Dynamic padding; loss masked on PAD** | Padding fraction varies with tokenizer (44% at char, 91% at 6-mer in a 512 buffer). Unmasked, this alone would produce the headline result |
| Optimization budget | **Dual currency: fixed epochs as primary, fixed supervised-token count as control** | An MLM at 15% masking sees ~6.7× fewer supervised positions per pass. Either currency alone is uninterpretable |
| Seeds | 3 for the grid, 5 at headline cells; bootstrap CIs with 1,000 resamples | Proposal promised k = 5 and bootstrapped CIs |
| **All metrics** | **Per nucleotide, never per token** | A 96-nt probe is 96 tokens under char, 32 under 3-mer, 16 under 6-mer. Conversion: PPL_nt = PPL_tok^(1/k) |

### Reporting standard

- Calibrated rank p-value, not raw success rate
- **Rank-1 verbatim recovery rate** (threshold-free, floor-immune)
- **TPR at FPR 1e-3 and 1e-4** on log-scale ROC, not AUC alone
- Bounded-prior posterior advantage γ, with the prior interval [a, b] stated explicitly (Li, Qardaji, Su, Wu & Yang, CCS 2013 Def. 5; Tramèr, Huang, Hubaux & Ayday, CCS 2015 Def. 8 — PDF in `papers/`)
- Exposure normalized by log2(n_candidates), **not** log2(4^L)

---

## E0 — Calibrated instrument and null battery `[CORE]`

**Question.** Does each metric return its analytically known value on a corpus whose answer is known in closed form — and is the masked-model scorer exchangeable with the autoregressive one as a ranking function?

### E0a — The entropy floor as a build-breaking assertion

Uniform synthetic DNA has entropy exactly 2.000 bits/nt, so held-out per-nucleotide perplexity has an exact floor of **4.000**.

Verified bounds for a correct causal scorer on 200 × 256 nt:

| Confidence | Max legitimate dip below 4.0 |
|---|---|
| 3σ-equivalent | 1.27 × 10⁻⁴ bits/nt → PPL ≥ 3.99965 |
| α = 10⁻⁶ (rigorous, assumption-free) | 3.9 × 10⁻⁴ bits/nt → PPL ≥ 3.99892 |

**A held-out value of 3.98 on uniform DNA is already impossible.** Assert `PPL_nt ≥ 3.999` in CI.

Scope conditions — the floor holds when and only when:

| Scorer | Floor at 4.0? |
|---|---|
| Causal, single-nucleotide tokenizer | ✅ exactly |
| Pseudo-log-likelihood, **single-nucleotide** masking | ✅ exactly (per-position Gibbs) |
| Pseudo-log-likelihood, **subword/BPE** masking | ❌ floor is 2^(H⁻_tok / L), must be measured from the tokenizer |
| Any scorer, **real** DNA | ❌ does not apply |

For the BPE arm, compute the erasure-entropy floor from the tokenizer alone (no model needed): for each masked position, enumerate the vocabulary items that legally fit the hole under canonical BPE re-encoding; the floor is the geometric mean of that count.

### E0b — Scorer equivalence control

**This is the one point of genuine research risk and it must be answered before the grid runs.**

Rank is invariant under a monotone transform applied uniformly, but **not** under swapping in a scorer that induces a different ordering with different noise. If the masked scorer is noisier, a probe's rank degrades at equal memorization and we would report "MLM memorizes less" having measured "the scorer is noisier."

Three checks:

1. Score **one AR-trained model** under both the AR likelihood and the PLL scorer. Do the probe rank distributions agree (Spearman ρ, rank-1 agreement)?
2. Does the PLL scorer's implied per-nucleotide entropy on held-out uniform DNA equal **2.000 bits**?
3. Reverse direction: score an MLM-trained model under PLL and under a causal-masked forward pass. Is the bias symmetric?

**Pilot result (2026-09-25).** On an MLM trained at 15% masking, `pll` sits at 2.0006 bits/nt while `prefix` drifts to 2.04–2.05 and ranks r=16 probes below chance; the two disagree (Spearman 0.4–0.7 at 50 epochs). **Both scorers are kept and reported everywhere.** Each carries its own held-out floor check per cell; a scorer that fails its floor is flagged in the table, not dropped. The mask rate at which the two scorers come back into agreement is itself an E2 result, and `prefix` remains the matched-conditioning instrument for E3.

**Decision at Gate 2:** measurable and correctable bias → correct it and document. Unpredictable → restrict cross-objective comparison to E3's matched-conditioning protocol and narrow the headline to tokenization.

### E0c — Null battery

Four null conditions per metric:

- (a) randomly initialized model
- (b) model trained on a disjoint corpus that never saw the probes
- (c) analytic chance floor: `P(rank ≤ k) = k/(n+1)`
- (d) **blind baseline** — a classifier using only surface statistics of the probe (length, GC content, k-mer composition) with no model access

(d) is not optional. Published work shows blind baselines beat many reported membership attacks. If the blind baseline matches the model-based attack, the attack measures distribution shift, not memorization.

**Models:** backbone at d = 512, char tokenizer. **Data:** uniform synthetic (H = 2.000 exactly) plus E. coli as a non-null control.
**Cost:** ~20 GPU-h, < 1 GB.
**Output:** Table 1 (every metric × every null condition) + a Methods subsection on scorer calibration.

---

## E1 — The commensurable grid `[CORE — HEADLINE]`

**Question.** With architecture, non-embedding parameter count, data, probe set and optimization budget held fixed, how much of the spread in measured memorization is attributable to tokenizer granularity, to objective, and to seed — and how does that spread compare to the published cross-architecture spread?

### Axes

| Axis | Levels |
|---|---|
| Tokenizer | char (vocab 8) / 3-mer (~68) / 6-mer (~4100) / BPE-4096 trained on public DNA |
| Objective | causal AR / MLM@0.15 / MLM@0.30 / MLM@0.50 |
| Repetition | r ∈ {1, 4, 8, 16} — **within run, zero extra cost** |
| Seed | 3 (5 at four headline cells) |

### Run budget

| Arm | Runs |
|---|---|
| Full 4 × 4 grid on synthetic | 48 |
| Reduced 4 × 2 (AR, MLM@0.30) on E. coli | 24 |
| Extra objectives (span corruption, prefix-LM), char only | 6 |
| Capacity-matched control (large-vocab arms) | 12 |
| **Total** | **≈ 90** |

### Controls

- Zero-probe run per (tokenizer, objective) cell → baseline train/test gap
- Identical probe set reused across every cell
- Both optimization budget currencies
- Explicit trainable-parameter ledger per arm

### Metrics

Calibrated extraction rate, rank-1 verbatim recovery, exposure against a shared 10⁵ candidate pool, canary-vs-test perplexity gap — **all per nucleotide**. Variance decomposition by nested ANOVA / mixed model with bootstrap CIs.

### Cost on 4 × 4090

Compute-bound arithmetic (6 × params × tokens, 12.9M params, 50 epochs):

| Tokenizer | Tokens/epoch | Per run @ 10% MFU | @ 20% MFU |
|---|---|---|---|
| char | 4.32M | 17 min | 8 min |
| 3-mer | 1.44M | 5.6 min | 2.8 min |
| 6-mer | 0.72M | 2.8 min | 1.4 min |
| BPE-4096 | 0.90M | 3.5 min | 1.8 min |

**Grid total: 5–11 GPU-hours → 1.5–3 hours wall-clock on 4 cards.**

Caveat: this assumes pre-tokenization, AMP and proper batching. The current reference pipeline tokenizes inside `__getitem__` with `num_workers=0`, which starves the GPU and could be 10× slower. **Measure actual MFU in week 2 and replace these numbers.**

Scoring (batched): ~8–15 s per model against a 10⁵ pool → under 30 min for all 90.
Disk: ~5 GB at fp32, 2.4 GB at bf16. Persist per-probe score arrays (~1 MB each), not intermediate checkpoints.

### Output

- **Figure 1** — the variance decomposition. The paper's central figure.
- **Figure 2** — per-nucleotide vs per-token metrics side by side, quantifying how much of the published cross-model spread is a units artifact.
- **Table 2** — per-repetition-tier disaggregation (announced in the published Methods, never shown).

---

## E2 — Mask-rate dose-response `[CORE]`

**Question.** Is the masked/causal distinction qualitative or quantitative? Does measured memorization vary continuously with mask rate, with causal AR sitting at the m = 1.0 endpoint of a single curve?

A dose-response survives regardless of whether any particular functional form holds; an A/B comparison does not. This is also the direct test of the published paper's mechanistic hypothesis that masked pretraining produces distributed, unextractable memorization.

**Axes.** m ∈ {0.05, 0.15, 0.30, 0.50, 0.80} at char tokenizer, plus causal AR plotted at m = 1.0. 6-mer at three mask rates as replication. r ∈ {1, 4, 8, 16} within run. 3 seeds.
**Runs.** (5 + 3) × 3 = 24, plus reuse of E1's AR cells.
**Controls.** Both budget currencies: fixed optimizer steps AND fixed supervised-token count.
**Cost.** ~40 GPU-h, ~1.5 GB.

**Output — Figure 3.** Exposure and rank-1 recovery vs mask rate, with AR at m = 1.0 and a fitted curve.

- Curve smooth and AR sits on it → "masked models are safer" is a rescaling, not a property.
- AR sits off the curve → the residual localizes exactly where a genuine qualitative difference lives, and that is the more interesting paper.

---

## E3 — Matched-conditioning recovery `[CORE]`

**Question.** Is memorized content in masked models present but not emittable, or simply absent? Under an adversary supplying the same number of known nucleotides, in the same positions, at the same search budget, does a masked model recover the probe at the same rate as a causal one?

This is the half of Alex's extension #2 that makes the comparison measurable at all. **No formal treatment of matched conditioning for cross-architecture memorization comparison exists in the literature** — this is a genuine gap and plausibly the paper's methodological contribution.

### Protocol

- Adversary supplies K known nucleotides at the sequence start; K/96 ∈ {0.25, 0.50, 0.75}.
- On uniform DNA, K revealed nucleotides is **exactly 2K bits** of conditioning — closed form. Competing work matches on *token counts*, which breaks the moment tokenizers differ. Ours is exact. This is where the tokenization axis and the objective axis reinforce each other.
- AR completes by beam search (width 10, **KV-cached** — the reference implementation does a full padded forward per beam per step and must be rewritten).
- MLM completes by **strictly left-to-right iterative unmasking** — *not* confidence-ordered, which would give the MLM an easy-positions-first advantage the AR model structurally cannot have.
- Same beam width, same budget. Report exact-match recovery on the suffix plus edit distance.

### Extraction definition

Use the Carlini 2023 definition: greedily decode from a k-nt prefix and check **exact match** of the remaining 96 − k nt. Chance probability of a 32-nt match is ~5 × 10⁻²⁰, so the chance-floor problem disappears entirely rather than needing a correction term.

### Scope limit — state it up front

Infilling runs on **char, 3-mer and 6-mer only**, where token boundaries are deterministic. **BPE is excluded from E3**, because a nucleotide string has exponentially many valid BPE tokenizations and "did the model emit the correct suffix" is ill-posed without constrained decoding over the token lattice. This is honest, it is a real open problem, and it does **not** touch E1 or E2, whose primary probe is rank-based scoring of a fixed string requiring no generation.

**Models.** E1's checkpoints; attack-only.
**Cost.** ~50 GPU-h (beam search dominates), negligible disk.

**Output — Figure 4.** Recovery rate vs conditioning fraction, AR vs MLM at matched bits, per tokenizer. This is the figure that says "discoverable but not extractable" or "not there at all."

---

## E4 — External validity on real pretrained GLMs `[CORE — promoted 2026-09-28; arm (c) is the headline validation]`

> **Why this arm decides the venue.** Every core result is on a 12.9M from-scratch backbone. A NeurIPS/ICML reviewer will ask whether it holds on a real pretrained GLM; without E4 the honest answer is "unknown," and that alone routes the paper to SaTML. So: if Gate 3 lands Strong or Moderate, E4 is promoted to CORE and E5 is cut first. If Gate 3 lands Weak, E4 stays stretch and SaTML is the target regardless.

**Question.** Does the law fit on a 12.9M from-scratch backbone predict memorization in real pretrained genomic foundation models?

**Arm (a) DNABERT-2** (117M, BPE, masked). Score through its **native masked head by pseudo-log-likelihood**, not through a bolted-on causal head. This avoids the hardest engineering path and is also the principled choice, since PLL on the native head matches what the model was pretrained for. Note this is the *same scorer E0 already built*.

**Arm (b) HyenaDNA** (14.2M, single-nucleotide, causal — both confirmed from the primary source). Restore its pretrained unembedding rather than replacing it with a fresh linear layer. If restoring the head does not bring held-out perplexity below 4.0 on uniform data, **drop the arm and say so in Limitations** — do not spend a week on it.

**Arm (c) — the DNABERT k-mer family: a natural experiment** `[CORE, added 2026-09-28]`

DNABERT (Ji et al., Bioinformatics 2021) released four pretrained models that differ **only in k**. Same team, same BERT-base architecture, same human-genome pretraining corpus, same masked objective. This is the tokenizer axis of our grid, realized at scale by someone else. It is the most direct external test we could ask for.

*Verified 2026-09-28:*

| model | params (fp32 weights) | vocab | license |
|---|---|---|---|
| `zhihan1996/DNA_bert_3` | ~87M (347 MB) | 69 | Apache-2.0 |
| `zhihan1996/DNA_bert_4` | ~87M (347 MB) | 261 | Apache-2.0 |
| `zhihan1996/DNA_bert_5` | ~87M (350 MB) | 1029 | Apache-2.0 |
| `zhihan1996/DNA_bert_6` | ~90M (359 MB) | 4101 | Apache-2.0 |

- All four are BertForMaskedLM with 12 layers, d=768, 12 heads and 512 positions, and ship custom code (`dnabert_layer.py`, `trust_remote_code`).
- The server cannot reach huggingface.co but **can reach `hf-mirror.com`**, so download via `HF_ENDPOINT=https://hf-mirror.com`.
- Total download ≈ 1.4 GB. `/data` has 5.4 TB free.

*Protocol:*

1. Fine-tune each of the four on the same canary-planted corpus, following **Alex's pipeline** (fine-tuning on a sensitive cohort is the realistic threat model and his paper's setting).
   - Canaries at r ∈ {0, 1, 4, 16}.
   - Same number of optimizer steps and the same learning rate for all four.
   - Two seeds.
2. Score with our instrument: per-nucleotide PLL through the native MLM head, rank against a random pool, and final-checkpoint scoring. Report the held-out floor per model, and compare at matched held-out loss as well as at a fixed step count.
3. Also report the extraction rate (left-to-right unmasking).

*Prediction (pre-registered here):* memorization increases with k, 3 < 4 < 5 < 6, at matched held-out loss. The size of the step from 5 to 6 is not predicted, because our cap1–cap4 results show the large-vocabulary magnitude is implementation-sensitive; only the ordering is.

*Two DNABERT-specific differences we must handle:*

- **Overlapping k-mers.** DNABERT tokenizes with stride 1, so an L-nt sequence gives about L−k+1 tokens for every k. Sequence length is therefore nearly **constant across the family**. This is convenient, because it removes Kharitonov's length confound by design. It is consistent with our spaced-k-mer result that length is not the driver.
- **Masking leaks through neighbors.** Each nucleotide appears in k consecutive tokens, so masking one token leaks it from its neighbors. PLL must mask a contiguous span of k tokens around each nucleotide, as DNABERT pretraining does. This needs a dedicated scorer (`pilot2/score_dnabert.py`) and its own floor check on uniform DNA.

*Checks before the main run:*

- The pretrained model loads under our env (transformers 4.29.2; custom code may need pinning).
- The held-out floor on uniform DNA is ≥ 2.0 bits/nt through the span-masked PLL.
- The null battery passes on the un-fine-tuned model.

*Cost:* 4 models × 2 seeds × one fine-tune of about 10–30 min on a 4090, plus span-PLL scoring. Roughly 10–20 GPU-h and ~3 GB kept (finals only).

*Why it decides the paper:*

- If the ordering holds, the from-scratch mechanism predicts a real, widely used GLM family (6.4k / 6.0k downloads for the 3- / 6-mer models). That is Figure 5.
- If it fails, the difference between from-scratch training and fine-tuning is itself the finding, and it is reported as such.

**Evo is excluded permanently.** Reason for Limitations: the published evaluation trains a full-rank output head alongside the low-rank adapter, so "LoRA-only" does not describe the optimization; disentangling adapter capacity from readout capacity is its own project.

**Cost.** ~40 GPU-h, ~3 GB (DNABERT-2 checkpoints ~470 MB; save finals only).
**Output — Figure 5.** Predicted vs observed, two anchor models.

---

## E5 — Corpus scale as a control `[STRETCH — cut first]`

**Question.** Does the decomposition hold at 4× corpus size? (Alex's extension #1, in reduced form.)

**Axes.** N ∈ {15,000, 60,000} × tokenizer ∈ {char, 6-mer} × objective ∈ {AR, MLM@0.30} × 3 seeds = 24 runs, of which 12 are already in E1. Both budget currencies. Probe mass reported per cell as a covariate.

**Cost.** ~70 GPU-h, ~1 GB.
**Output.** Figure 6 or a robustness panel. If cut: one sentence in Limitations.

---

## Totals

| | |
|---|---|
| Experiments | 6 (4 CORE, 2 STRETCH) |
| Display items | 6 figures + 3 tables → trim to 5 + 2 in a 9-page body |
| GPU (core) | 5–260 GPU-h depending on pipeline efficiency — **measure in week 2** |
| Disk (everything) | **< 8 GB** |
| Shadow / reference models | 0 |
| Human subject data | 0 |
| Genomics on the critical path | Minimal — k-mer tokenizers, GC content, a FASTA reader |

---

## Engineering prerequisites

Fix in this order. Each is a precondition for measuring the next.

| # | Item | Days | Why |
|---|---|---|---|
| 1 | Mask loss on padding | 1 | **Blocking.** Padding fraction varies with tokenizer (44% char → 91% 6-mer). Unmasked, this alone reproduces the headline result in the wrong direction |
| 2 | Checkpoint selection / early stopping on **masked** validation loss, on a **validation** split disjoint from test | 2 | Blocking. Currently selects on padding-diluted loss, evaluated on the test split |
| 3 | Probe tracking — replaced, not patched; tag at construction | 3 | Blocking |
| 4 | Extraction: hoist and batch the candidate pool; adopt exact-match criterion | 1 | Cheapest high-leverage day. The reference implementation re-seeds the RNG inside the per-probe loop and runs 100 × 1,001 unbatched forwards. Batching buys a 10⁵ pool for less than the current cost of 10³ |
| 5 | Efficiency: AMP, batch size, pre-tokenization, dynamic padding | 3 | Enabling. Determines whether the grid is 3 hours or 30 |
| 6 | PLL scorer for bidirectional models | 3 | Needed for E0/E3. **This is the method, not a repair** |
| 7 | Golden tests + sweep driver | 4 | Infrastructure |
| | **Total** | **~17 engineer-days ≈ 4 weeks** | |

### Golden tests that must fail the build

- Padding fraction of the loss is exactly zero
- Probe-flag precision = 1.0 and recall = 1.0
- Train / validation / test splits are disjoint
- Chance floor calibration: `P(rank ≤ k) = k/(n+1)` on an untrained model
- Held-out `PPL_nt ≥ 3.999` on uniform synthetic data, per scorer
- Brute-force normalization check: on vocab 4, L = 8 (65,536 sequences), `Σ_x Π_i q(x_i | ·)` must equal 1.000 for any scorer claimed to be a likelihood

### Environment

Build a clean minimal environment: recent torch + numpy + `tokenizers` + `biopython`. **Do not use the reference `requirements.txt`** — it is a `pip freeze` pinning `torch==2.1.1+cu118` and `transformers==4.29.2`, contains an unresolvable local path dependency, and pins a PyPI package named `evo` that is an unrelated SLAM trajectory-evaluation library. The core backbone is pure PyTorch `nn.TransformerEncoder` and needs none of it. Only E4 needs the HuggingFace stack.

---

## Timeline and gates

### Phase 1 — Foundation (weeks 1–6) — week 1 starts Monday 2026-09-29

**W1.** Confirm 2027 venue deadlines. Request HPC access (long lead time). Build clean environment. Read the positioning literature and write a one-paragraph delta against each: von Arx & Dieudonné (arXiv:2605.22981), Wang & Asokan (arXiv:2605.24173), Mireshghallah et al. EMNLP 2022, Salazar et al. ACL 2020, Jagielski arXiv:2306.00133. Email Alex for a 1:1.

**W2–3.** Standalone throwaway pilot harness, deliberately bypassing most of the reference code. Backbone d = 512, char tokenizer, causal AR and MLM@0.15, N = 5,000 synthetic, 20 probes at r ∈ {1, 16}, batched scorer with 10⁴ pool. Fix items 1 and 2 in the pilot only.

> ### GATE 1 — end of W3. ~5 GPU-hours. The most important date in the project.
>
> - **Q1 (scorer):** do the AR and PLL scorers rank the probe set consistently on the same AR-trained model? Does PLL's implied entropy on held-out uniform DNA land at 2.000 bits?
> - **Q2 (dynamic range):** does extraction at r = 16 exceed r = 1 by more than seed noise, under the calibrated null?
> - **Q3 (objective signal):** does MLM@0.15 differ measurably from AR under matched scoring?
>
> **Branches.** Q2 fails → raise N and r before the grid; the instrument lacks resolution, not the science. Q3 flat → pivot the headline to tokenization-only and drop the objective axis to a two-level control; the paper survives, narrower. Q1 fails unrecoverably → restrict cross-objective comparison to E3; if E3 also cannot be matched, switch to the runner-up direction at week 4 with 20 weeks intact.

**W3–6.** Full foundation in parallel: engineering items 3–7, golden tests, sweep driver.

> ### GATE 2 — end of W6. Scorer equivalence at full rigor, both directions, on the real harness.
> Green → run E1. Amber (measurable correctable bias) → correct, document, run E1. Red → E1 runs as a tokenization study only.

### Phase 2 — The grid (weeks 7–12)

**W7–11.** E1, ~90 runs. Batch submission; monitor, do not babysit.
**W10–12.** E2, overlapping E1's queue.

> ### GATE 3 — end of W12. The variance decomposition.
>
> | Result | Action |
> |---|---|
> | **Strong** (≥ 60% of published spread) | Headline: "architecture was not identified." Aim NeurIPS |
> | **Moderate** (30–60%) | Headline: the quantification itself. NeurIPS-viable, SaTML certain |
> | **Weak** (< 30%) | Architecture genuinely dominates under control — validates the published paper. Pivot headline to E2 dose-response + the per-nucleotide commensurability correction. Target SaTML 2028. **Do not force the NeurIPS framing** |

### Phase 3 — Protocol contribution (weeks 13–17)

**W13–16.** E3: KV-cached beam search, left-to-right unmasking decoder, three conditioning fractions × three tokenizers.

> ### GATE 4 — end of W16. Does infilling agree with ranking?
> Agreement → memorization present and emittable; clean story. Disagreement → **this is the better paper**: "discoverable but not extractable" under masked objectives, which directly answers the published mechanistic hypothesis. Either way, write it up.

**W17.** Buffer. Something will need re-running.

### Phase 4 — Stretch and writing (weeks 18–24)

**W18–20.** E4 if Gate 3 was Strong or Moderate; otherwise E5, or start writing early.
**W20–22.** Full draft. Figures built from persisted score arrays, not from re-running anything.
**W23.** Internal review — Alex first, then Erman. Expect demands for ablations.
**W24.** Revision. Draft complete ~2027-03-08.

> ### GATE 5 — week 20. If fewer than three CORE experiments have landed: cut both STRETCH arms, cut E3 to char-only, target SaTML 2028. A four-month slip with a revision path, costing nothing but ambition.

---

## Week 1 actions (2026-09-29 → 10-03)

0. **Status of prerequisites:** both PMP source papers are in `papers/` and the formal definitions are verified (§0 reporting standard is now grounded). The Erman proposal (03) and the group-meeting deck are ready to send/present.
1. **Build the clean environment and train the backbone for 100 steps on the 4090s.** Measure actual MFU. This replaces the single largest uncertainty in the plan.
2. **Request HPC access** — ask for concurrent job limit, max walltime, scratch quota and purge policy, and GPU generation. Has a queue; start it Monday.
3. **Email Alex to request a 1:1.** Lead with the idea and the 8 GB figure, propose him as coauthor, then ask implementation questions as questions.
4. **Read Jagielski, *A Note On Interpreting Canary Exposure*** (arXiv:2306.00133). Ten minutes; it is the primary source for the exposure normalization standard.
5. **Confirm NeurIPS 2027 and SaTML 2028 deadlines.** If NeurIPS 2027 is earlier than ~April, make SaTML 2028 primary and keep the plan unchanged.

---

## Open items requiring external input

| Item | From whom |
|---|---|
| Does the ACM DL version of the published paper print numeric exposure values? (The arXiv version does not) | Check directly |
| Does the extraction experiment use beam search (per the paper's Methods) or uniform random candidates (per the code)? | Alex |
| DNABERT-2's average token length k — no published value exists | Measure empirically, per corpus |
| Subtleties in moving PMP from a released GWAS statistic to a per-sequence loss; how to argue the prior interval [a, b] | Erman — the CCS 2015 definitions themselves are now retrieved, PDF in `papers/` |
| Li et al. CCS 2013 full text (closed access, no open PDF exists) | CWRU ACM DL subscription, or Erman |
| Venue preference: AI/ML vs bioinformatics | Erman |
