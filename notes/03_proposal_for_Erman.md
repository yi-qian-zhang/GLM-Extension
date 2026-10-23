# Proposed Spinoff: Isolating Tokenization and Pretraining Objective in Genomic Language Model Memorization

**To:** Dr. Erman Ayday
**From:** Spencer Zong
**Date:** 2026-09-18
**Status:** Proposal for discussion

---

## 1. Summary

I propose a controlled ablation study that isolates **tokenization granularity** and **pretraining objective** as drivers of memorization in genomic language models, on a fixed backbone with fixed data.

The headline deliverable is a **variance decomposition**: of the spread in measured memorization across models, how much is attributable to the tokenizer, how much to the training objective, how much to random seed — and how that spread compares in magnitude to the cross-architecture spread reported in our BCB '26 paper.

This is a standalone conference paper aimed at an AI/ML venue, coordinated with Alex, and it directly executes an experiment the published paper asks for in its own Discussion section.

---

## 2. What I have done so far

- Read the BCB '26 paper in full.
- Read the NIH proposal through the end of Aim 1 (both sub-aims).
- Read Alex's Extension Ideas note.
- Read the Engravings paper.
- Cloned and read the `GLM-Memorization` repository end to end, including the attack implementations, the data pipeline, the model wrappers and the trainer.
- Completed a foundations audit of the scoring methodology used by all three attack vectors, tracing each metric to its primary source and verifying every citation against arXiv / Crossref / ACL Anthology.

---

## 3. Where the published work sits relative to Aim 1

| Aim 1.1 component | Status after BCB '26 |
|---|---|
| Perplexity-based detection | Published |
| Canary extraction | Published |
| Membership inference (threshold + likelihood ratio) | Published |
| ML-based MIA | Not started |
| Attribute inference | Explicitly out of scope in the paper |
| Vulnerable attributes / vulnerable prompts | Not started |
| **Aim 1.2 (all defenses)** | **Preliminary figures in the proposal only; Alex confirms unassigned** |

Alex's Extension Ideas note names three reviewer-driven extensions, none of which appear in the proposal:

1. Corpus size scaling study
2. **"Fix the model architecture and then train autoregressively and masked pretraining objectives to silo this"**
3. Alternative membership privacy metrics (bounded-prior membership privacy)

My proposal executes **#2** as its spine, absorbs **#3** as the reporting standard, and carries **#1** as a robustness control.

---

## 4. The scientific motivation

### 4.1 The published comparison varies four things at once

The BCB '26 paper attributes differences in memorization profile to **architecture**. But the four evaluated models differ simultaneously in:

- architecture (transformer encoder / Hyena convolution / StripedHyena SSM)
- **tokenization** (single-nucleotide / BPE / byte-level)
- parameter count (12.9M to 7B)
- **pretraining objective** (causal next-token / masked)

The paper identifies this itself, in print (Section 6, Limitations and future work):

> "the methodology does not isolate this factor from other confounding variables, **including parameter count and tokenization strategy**, and a controlled ablation comparing pretraining objectives on a fixed architecture would be needed to establish a causal relationship."

So the causal claim is not yet identified, and the paper says so. This proposal supplies the missing experiment.

### 4.2 Tokenization is the second, unexamined variable

The proposal's Aim 1 Rationale asserts that genomic data's **"fixed 4-letter alphabet"** may alter memorization dynamics in ways domain-agnostic evaluations miss. That assertion has never been tested.

It is testable here in a way that is **not possible in natural language**. The same nucleotide string, carrying identical information, can be tokenized at character / 3-mer / 6-mer / BPE granularity with no change to its semantic content. In text, changing the tokenizer changes what a token means and lets the vocabulary co-adapt to the corpus; character-level English is not a lossless objective-agnostic representation the way `{A,C,G,T}` is.

This is the experiment that gives the paper a claim an ML audience cannot get from text.

### 4.3 The comparison is currently made in mismatched units

A related and independent issue: perplexity is computed **per token**. For a single-nucleotide tokenizer, per-token equals per-nucleotide. For a BPE tokenizer whose average token spans *k* nucleotides, per-token perplexity is on a scale of roughly the *k*-th power of the per-nucleotide value.

Table 4 places both on the same axis. The conversion factor for DNABERT-2 cannot be recovered from published information — its average token length is not reported anywhere in the DNABERT-2 paper, and it varies by corpus.

This is not a side issue. It means that part of the published cross-model spread may be a units artifact, and quantifying that is a direct contribution of the proposed tokenization axis.

---

## 5. The proposed paper

**Working title.** *Architecture Was Not the Variable: Tokenization Granularity and Pretraining Objective Account for Memorization Differences in Genomic Language Models*

**Claim.** On a fixed backbone with fixed data, fixed non-embedding parameter budget and a fixed probe set, varying only tokenization granularity and pretraining objective produces a spread in measured memorization comparable to the spread the literature attributes to architecture. Once memorization is measured per nucleotide rather than per token, and masked models are scored under matched conditioning, the masked-versus-causal distinction is a continuous dose-response in mask rate rather than a qualitative architectural property.

**Core design.** A 4 × 4 grid on a fixed 12.9M-parameter backbone:

- Tokenizer: character / non-overlapping 3-mer / non-overlapping 6-mer / BPE-4096
- Objective: causal autoregressive / masked at 15%, 30%, 50%
- Repetition tiers r ∈ {1, 4, 8, 16} carried *within* each run at no extra cost
- 3 seeds (5 at headline cells)

Approximately 90 training runs, all from scratch, all under our control.

**Why the result is guaranteed.** A variance decomposition yields a number regardless of outcome:

| Outcome | Headline |
|---|---|
| Tokenizer + objective reproduce ≥ 60% of the published cross-model spread | Architecture was not identified; tokenizer and objective are first-order privacy design choices |
| 30–60% | First quantification of the decomposition; architecture carries a measurable residual |
| < 30% | **Architecture is genuinely dominant under control — this validates the published result** |

There is no branch that produces nothing. For a first paper on a six-month clock, I weight this above a higher-ceiling but binary-outcome design.

---

## 6. Methodological prerequisites

While reproducing the pipeline I identified several measurement details in the evaluation code that need to be settled before any extension is built on top of it — principally around how canary sequences are tracked through the data pipeline, how loss is aggregated over padded positions, how bidirectional encoders are scored, and the chance baseline of the rank-based extraction criterion.

**I am working through these directly with Alex.** They do not affect the feasibility of the proposed design, because it builds its own model family from scratch with its own instrumentation rather than extending the published numbers. I raise them here only to note that the calibration work is accounted for in the timeline (weeks 1–6).

The foundations audit also produced two items worth flagging as positives:

- **Bounded-prior membership privacy** — Alex's extension #3 — traces to Li, Qardaji, Su, Wu & Yang (CCS 2013, *Membership Privacy: A Unifying Framework for Privacy Definitions*) and to **Tramèr, Huang, Hubaux & Ayday (CCS 2015)**, i.e. your own paper. I have read the CCS 2015 paper and taken the formal statement from it, so I no longer need a copy. The relevant definitions are set out in §6.1 below.

  It is the right reporting standard for this work: unlike AUC, it is a worst-case guarantee on the mechanism rather than an average-case measurement of one attack. Two attacks with identical AUC can produce very different worst-case posterior shifts, and AUC cannot be converted into a privacy guarantee at all.
- Uniform synthetic DNA has an exact information-theoretic perplexity floor of 4.0 per nucleotide. This gives us something natural language does not have: an analytically known "no memorization" value against which any scoring implementation can be validated before it is trusted. I intend to make this a standing correctness check in the codebase, and it is worth a short methods subsection in the paper.

### 6.1 The reporting standard, stated precisely

Verified against the CCS 2013 primary source (definition numbering is Li et al.'s; the CCS 2015 restatement renumbers them).

**Positive membership-privacy (CCS 2013 Def. 3.1).** A mechanism *A* provides (*D*, γ)-PMP under a family *D* of distributions over 2^U, with γ ≥ 1, iff for every S ⊆ range(*A*), every D ∈ *D*, and every entity t ∈ U:

```
(1)   Pr[t ∈ T | A(T) ∈ S]  ≤  γ · Pr[t ∈ T]
(2)   Pr[t ∉ T | A(T) ∈ S]  ≥  (1/γ) · Pr[t ∉ T]
```

**Why (2) is needed, in the paper's own example.** Take γ = 1.2 and a prior Pr[t] = 0.85. Equation (1) alone bounds the posterior at 0.85 × 1.2 = 1.02 — vacuous, so an adversary could reach complete certainty while nominally satisfying a "strong" γ. Equation (2) lower-bounds Pr[¬t | S] at 0.15 / 1.2 = 0.125, capping the posterior at 0.875. Both are needed; the two together give

```
(3)   Pr[t | S]  ≤  min{ γ · Pr[t],  (γ − 1 + Pr[t]) / γ }
```

**Sufficient condition (Lemma 3.2).** If Pr[S | t] ≤ γ · Pr[S | ¬t] for every t with 0 < Pr[t] < 1 and every output event S, then *A* provides ({D}, γ)-PMP. This is the form a mechanism designer actually controls, and it is the hook a loss-based attack would attach to.

**The bridge to DP (Thm. 4.8).** *A* satisfies ε-bounded DP **iff** it provides (D_B, e^ε)-PMP, where D_B is the family of bounded mutually-independent distributions — those assigning each entity an independent inclusion probability p_t, restricted to datasets of one fixed size.

**The bounded-prior relaxation (CCS 2015 Def. 8).** For 0 < a ≤ b < 1, the subfamily D_B[a,b] ⊆ D_B restricts the adversary's prior to Pr[t] ∈ [a, b] ∪ {0, 1}. Under this weaker and more realistic adversary, the same γ-PMP is attainable with a *weaker* DP budget than (ln γ)-DP; Lemma 3 there gives a per-entity tight parameter γ(t) < γ. This is the part that is directly useful to us: it converts "how much background knowledge do we credit the adversary with" from a hidden assumption into a stated interval.

**What this buys the paper.** I would report γ alongside TPR at low FPR, and state [a, b] explicitly, which forces the threat model to be concrete: before querying the model, how confident could an adversary be that a given individual is in the fine-tuning cohort? In the genomic setting that is arguable from cohort size and recruitment scope — exactly the assumption AUC leaves silent. Two attacks with identical AUC can produce very different worst-case posterior shifts, and AUC cannot be converted into a guarantee at all.

**One open question I would like your view on** (§11.2): the CCS 2015 formulation applies PMP to a released GWAS statistic. Moving it to a per-sequence loss under a queried model changes what the mechanism output *S* is, and the adversary gets to choose the query. Were there subtleties there you considered at the time?

---

## 7. Venue

**Primary target: NeurIPS 2027** (deadline ~May 2027 — to be confirmed).
**Backstop: SaTML 2028** (~Sept–Oct 2027).

Rationale:

- The claim shape is a mechanism paper with a variance decomposition and a dose-response curve, which is what ML main tracks reward. It is not an audit paper, which is what security venues reward — hence NeurIPS before SaTML.
- Per your note that we are not restricted to the genomics domain, this is where my own background is strongest and where I can contribute fastest.
- The calendar works without a cliff: a 24-week plan starting 2026-09-22 completes ~2027-03-08, leaving roughly nine weeks for internal review and the ablations internal review will demand.

If you would prefer a bioinformatics venue, the same experiment set supports an ISMB/RECOMB framing with the emphasis shifted from variance decomposition to practical guidance for GLM practitioners on tokenizer and objective selection under privacy constraints. I would want your view on this.

---

## 8. Resources

| | |
|---|---|
| Compute | **4 × RTX 4090, which I own.** No HPC dependency for the core experiments. |
| GPU time (core) | Estimated 10–260 GPU-hours depending on pipeline efficiency; to be measured in week 2 |
| Disk | **< 8 GB total** |
| Shadow / reference models | None required for the core |
| Human subject data | **None** — no IRB, no dbGaP |
| Models needed | None beyond our own from-scratch backbone for the core; DNABERT-2 and HyenaDNA only in an optional external-validity arm |

The disk figure is worth noting given the storage constraint Alex raised. For comparison, a reference-model LiRA evaluation would need ~768 training runs, and a corpus-scaling grid including Evo could reach the terabyte range. This design needs neither.

**Evo is excluded** from the core, deliberately. Beyond the compute and storage cost, the published evaluation trains a full-rank output head alongside the low-rank adapter, which confounds adapter capacity with readout capacity. Disentangling that is its own project.

I would still like HPC access as a backstop and for the optional external-validity arm, and would appreciate a pointer on the fastest route to an allocation.

---

## 9. Timeline

| Phase | Weeks | Output | Gate |
|---|---|---|---|
| Foundation | 1–6 | Calibrated instrumentation; pilot on one cell | **Gate 1 (wk 3):** is there measurable dynamic range and a usable scorer? |
| Main grid | 7–12 | 90 runs; variance decomposition | **Gate 3 (wk 12):** which of the three outcome branches are we in? |
| Protocol contribution | 13–17 | Matched-conditioning recovery experiment | **Gate 4 (wk 16):** does recovery agree with ranking? |
| Stretch + writing | 18–24 | Full draft | **Gate 5 (wk 20):** cut stretch arms, or slip to SaTML |

Each gate has a defined fallback. Full detail in the accompanying experiment plan.

---

## 10. Relationship to the rest of Aim 1

This paper deliberately does **not** consume the largest unexecuted items in the proposal. It leaves available:

- **Aim 1.2 (defenses)** — confirmed unassigned. I would like to claim it as paper two. One note: at the 12.9M-parameter from-scratch scale, the downstream utility axis may not move measurably, which would make a privacy–utility tradeoff plot uninformative. Establishing a usable utility protocol is a prerequisite I would want to scope before committing.
- **Attribute inference and kinship leakage.** The proposal motivates GLM privacy partly on heritability — that a memorized sequence exposes relatives who never consented. Nothing in the published work measures this. The 1000 Genomes high-coverage release provides 602 complete trios under fully open access with no data application required, which makes it directly testable. I believe this is the highest-ceiling direction available and the one least likely to be scooped by an NLP group, but it is data-engineering-first in the area where my background is thinnest, so I propose it as paper three rather than first. **I would like to stake it out now if that is acceptable to you**, and can write a one-page sketch.

---

## 11. Questions for you

1. Do you agree with the AI/ML venue target, or would you prefer this framed for ISMB / RECOMB / AMIA? The experiment set supports either.
2. On bounded-prior membership privacy: your CCS 2015 formulation applies PMP to GWAS summary statistics, where the mechanism output is a released statistic. In our setting the output is a per-sequence loss under a queried model. Are there subtleties in that translation you considered at the time? And is there a defensible way to argue the prior interval [a, b] for a fine-tuning cohort, or is that necessarily a stated assumption?
3. Is it acceptable for me to stake out the kinship / attribute-inference direction as a follow-on, and should Aim 1.2 be sequenced before or after it?
4. What is the fastest route to an HPC allocation, and is there a group compute policy I should know about?
5. Alex is a coauthor on this by default in my view, since it extends his framework. Please tell me if you would structure authorship differently.
