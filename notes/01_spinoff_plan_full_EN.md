# FINAL RECOMMENDATION

**Prepared 2026-09-18. One paper. One claim. Start Monday.**

---

## 1. RECOMMENDED PACKAGE

### Working title

**"Architecture Was Not the Variable: Tokenization Granularity and Pretraining Objective Account for Memorization Differences in Genomic Language Models"**

(Alternate, if the result lands hard: *"Masked Is Not Safer, It Is Sparser: A Dose-Response Account of Memorization Under Pretraining Objectives"*)

### One-sentence claim

> On a fixed backbone with fixed data, fixed parameter budget, and a fixed probe set, varying only **tokenization granularity** and **pretraining objective** produces a spread in measured memorization comparable to the spread the published literature attributes to *architecture* — and once memorization is measured per nucleotide rather than per token, and masked models are scored with an objective-native probe, the masked-versus-causal distinction is a **continuous dose-response in mask rate**, not a qualitative architectural property.

### Target venue

**Primary: NeurIPS 2027 (deadline ~May 2027 — confirm exact date).**
**Backstop: SaTML 2028 (~Sept–Oct 2027).**
**Explicitly ruled out: ICML 2027 (~Jan 2027) — too soon; ICLR 2027 and SaTML 2027 — already past or within weeks.**

Why NeurIPS primary. Three reasons, in order.

1. **It matches the claim shape.** This is a mechanism paper with a variance decomposition and a dose-response curve. The `ml-venue-bar` report lists five shapes that get accepted at ML main tracks; this is shape 1 (quantitative law with functional form) crossed with shape 4 (measured causal effect with a practical recommendation). It is not shape 2 (an audit), which is why it does not belong at SaTML first.
2. **It matches Spencer's stated preference** for AI/ML venues, which the advisor has explicitly permitted.
3. **The calendar works without a cliff.** A 24-week plan starting 2026-09-22 completes ~2027-03-08. That leaves ~9 weeks of slack before a May deadline — enough for internal review, the ablations internal review will demand, and a rewrite. Every other venue on the list either lands 12 weeks from now (impossible) or 12 months from now (wastes the year). If week 12's gate comes back weak, SaTML 2028 is a four-month-later fallback with a revision culture, and nothing is lost.

I am moderately uncertain about exact 2027 deadlines (knowledge cutoff May 2026) — **verify them in week 1**; if NeurIPS 2027 turns out to be earlier than ~April, fall back to SaTML 2028 as primary and keep the same plan.

### The anchor — honoring the user's constraint explicitly

This package is anchored in **both** permitted buckets simultaneously, for both of its halves. That is the strongest standing available.

**Anchor 1 — Alex's extension #2, verbatim.** `ext_ideas.txt`:

> "Fix the model architecture and then train autoregressively and masked pretraining objectives to silo this"

This is the paper's objective axis, executed exactly as named.

**Anchor 2 — the published paper demands it, in print.** `bcb_paper.txt` L567–570:

> "the methodology does not isolate this factor from other confounding variables, **including parameter count and tokenization strategy**, and a controlled ablation comparing pretraining objectives on a fixed architecture would be needed to establish a causal relationship."

Note what that sentence gives me for free: it names **tokenization strategy** as an unisolated confound, by the authors, in the published text. So the tokenization axis is not something I invented to make the paper interesting — it is the second variable the paper itself says was never controlled. This is the single most important sentence in the entire source corpus for this recommendation.

**Anchor 3 — proposal Aim 1.1, promised and not delivered.** `nih_proposal.txt` L277–279:

> "we will apply this analysis across architectures, **repetition regimes**, and mitigation strategies to assess how training dynamics influence memorization risk"

The repetition-regime disaggregation is announced in the paper (§4.3.3, L334–336: *"We additionally disaggregate canary perplexity by repetition tier, enabling analysis of how insertion frequency modulates the model's confidence"*) and **never shown** — Table 4 has one canary column, not four. My grid delivers it as a byproduct at every cell.

**Anchor 4 — proposal Aim 1 Rationale, the stated domain premise.** L226–229:

> "GLMs operate on data with unique properties (e.g., **fixed 4-letter alphabet**, strong biological structure...) that may amplify or alter memorization dynamics in ways that domain-agnostic privacy evaluations fail to capture."

The proposal asserts the fixed alphabet matters and never tests it. The tokenization-over-fixed-alphabet experiment is that assertion, made falsifiable.

**Anchor 5 — Alex's extension #3, absorbed as the reporting standard.** "Alternative membership privacy metrics (bounded-prior membership privacy)." Per the `alex-extensions` report, this is a subsection, not a paper — and its honest home is *how you report* corrected numbers: TPR at low FPR on log-scale ROC, plus bounded-prior posterior advantage, instead of AUC alone. That is where it goes: E0's reporting layer.

**Alex's extension #1 (corpus scaling)** appears as a reduced two-level control in a STRETCH experiment, not as an axis. Justification in §2.

---

## 2. WHY THIS ONE — adjudicating the critiques

### The state of the panel

Every one of the five framings came back **VIABLE-WITH-CHANGES** from both reviewers, and every one had at least one reviewer-identified defect sitting directly on its headline. That is the finding. There is no clean winner among the five as proposed, so the recommendation must be a merge — and the merge is not arbitrary, because **four independent reviewer voices converged on the same construction.**

- The `vulnerable-prompts` novelty reviewer's single change: *"Promote E6 from droppable stretch goal to the spine of the paper: build your own commensurable model family and make the headline a variance decomposition over it, not a ranking reversal among Alex's four wrappers."*
- The `scaling-and-objective` novelty reviewer's single change: *"Delete Exp. 3 (the entropy dial) and replace it with a tokenization-granularity experiment over the fixed alphabet... the only axis in your entire inventory that genuinely does not exist in text."*
- The `alex-extensions` ground report's verdict on extension #2: *"FULL PAPER. The strongest standalone spinoff for an AI/ML venue."*
- The `ml-venue-bar` ground report's affordance ranking: *"Underrated, and it is the one that rescues framing (b): tokenization varied over a fixed alphabet."*

Two reviewers reviewing *different* proposals, plus two ground reports written *before* any proposal existed, independently arrived at the same experiment. That is the strongest signal in the entire dossier, and it is what I am acting on.

### Rulings on specific disagreements

**RULING 1 — "Memorization audits are probe-dependent" is a section, not a paper. I side with both critics against the `vulnerable-prompts` proposer.**

The proposer graded his own hook MEDIUM-STRONG against two ground reports that independently said "section." The novelty reviewer then showed the headline statistic is arithmetically unbuildable: the Kendall-tau ordering runs over models the proposal's own exclusion rules disqualify (HyenaDNA excluded by its perplexity rule; DNABERT-2 valid in 1 of 9 probe conditions; Evo confounded by finding F), leaving **n ≈ 2 commensurable models**. Tau on two items takes two values. The claim is unbuildable, not merely risky.

**But I am salvaging two pieces of it**, because they survive the critique intact: (a) **pseudo-log-likelihood as the objective-native scorer for bidirectional models**, which is not a "probe taxonomy" but the necessary instrument for any masked/causal comparison; and (b) **matched-conditioning infilling**, which becomes my E3. The nine-probe taxonomy, the "closed and enumerable probe space" claim (correctly demolished — only strand and direction are closed; prefix fraction and mask geometry are as open as text), and reverse-complement as an intellectual centerpiece are all dropped.

**RULING 2 — Aim 1.2 / defenses cannot be paper one, and the reason is not political.**

Two feasibility reviewers, working on different framings, independently discovered the same disqualifying fact: a 12.9M-parameter model pretrained from scratch on ~256 kb–2.5 Mb cannot produce a moving downstream utility axis. GUE `prom_300_all` has ~53k labeled examples; essentially all the signal comes from supervised fine-tuning, so `utility(defended) − utility(undefended) ≈ 0 ± seed noise` for every defense in the plan. A privacy-**utility** paper whose y-axis cannot move is not a paper, and the failure is silent — a flat plot looks like a null result for four months before anyone questions the instrument.

Four of five ground reports independently sequenced Aim 1.2 second. I am making that a firm ruling, and adding the mechanical reason: **the utility axis does not exist at this model scale, and building one is a separate project.** Aim 1.2 remains claimed and available; it is paper two or three, after either a larger pretraining run or a linear-probe utility protocol exists.

**RULING 3 — The MIA length confound (finding C) is real, is the highest-confidence item in the dossier, and must NOT be this paper's headline.**

The arithmetic is decisive: `AUC = 900/1900 + (1000/1900)×0.5 = 0.7368`, against a published band of 0.70–0.79 across all sixteen configurations. That match is too tight to be coincidence, and the mechanism is visible in the source (`mia_attack.compute_losses` uses `reduction='mean'` with no `ignore_index` while `dnabert_wrapper.compute_perplexity` *does* mask — two code paths in one repo disagreeing).

I am nonetheless overriding every proposal that wanted to publish it, for two independent reasons. First, the `ml-venue-bar` report is correct that an audit paper needs 4–6 systems to fail the null, and Spencer has one. Second, and decisively: **a first-year's debut paper should not be a correction of his senior labmate's published numbers.** The `defenses` novelty reviewer put it exactly right — it becomes "an erratum with a compute bill."

**The structural advantage of my recommendation is that finding C never has to appear in print.** My paper does not use membership inference as a primary vector, and it dissolves the confound by construction (all windows are length-matched because probes are embedded, not appended). C becomes a private conversation with Alex — §4 below.

**RULING 4 — Kinship is the best idea and the wrong first project. I am overriding two ground reports that ranked it first.**

`novelty-scan` ranked it #1 of 8 ("the strongest OPEN cell in the set"); `ml-venue-bar` ranked it #1 of 7 ("the only one with a credible ICML/NeurIPS path"). Both reviewers of the `attribute-inference` framing independently said "fold the trios in as the attribute." I believe all four are right about the science.

I am overriding them on execution risk, on four grounds: (i) `repo-audit` costs the pipeline at 15–20 engineer-days before the first result and calls it *"a separate project, not an extension of this codebase"*; (ii) it is data-engineering-first in exactly the domain Spencer has flagged as thinnest; (iii) `README.md:289` states the pipeline contains no real human genomic data, so reversing it needs Ayday's explicit sign-off before work starts; (iv) the variant-density problem is a genuine coin flip — at 288 nt two humans are usually byte-identical, and if that kills it, there is no fallback inside the framing.

**What I am giving up is real and I want it named:** the only cell with no occupant, the only direction with no text analogue that an NLP lab can scoop, and the one that closes the gap between the BCB paper's own motivation (heritability, "exposing biological relatives who never consented") and what it measured. **Mitigation, and it is not optional:** Spencer writes a one-page project sketch for the kinship paper and gives it to Ayday in month 1, so the direction is staked out inside the lab, and does not touch it again until paper one is submitted. §8 has the ask.

**RULING 5 — The corpus-scaling grid (Alex's #1) is a control, not an axis.**

Alex himself framed it as "lowest hanging" and journal-bound. Independently, wherever a version of it appeared in a proposal, a novelty reviewer found the design underpowered: six triangular cells fitting four parameters, iso-*r* rows carrying one cell at the top level, and a two-point plot standing in for "the exponent as a function of X." The `alex-extensions` report's own verdict: *"STRONG SECTION as listed. FULL PAPER only in the capacity/phase-boundary framing."* I take it as two corpus-size levels in a STRETCH experiment — enough to say "the effect holds at 4× corpus size," not enough to claim a law.

**RULING 6 — The `wildcard` framing's headline is refuted and I am not rescuing it.**

The novelty reviewer showed that Lee et al. 2022 ships `ExactSubstr`, a suffix-array method removing any ≥50-token substring occurring more than once **irrespective of containing document** — i.e. fragment-level deduplication, deployed, four years old. The proposal's adversary was assembled by deleting the second half of its own most-cited reference. The feasibility reviewer separately simulated the Jaccard claim and found it false (k=5 independent-pair Jaccard = 0.122, not saturated near 1.0). Two independent refutations of the same headline. Dead.

**RULING 7 — The `attribute-inference` mechanism has a sign error and the headline experiment measures the wrong thing.**

The novelty reviewer's catch is correct: on the accuracy scale, always-predict-major-allele achieves `1 − MAF`, so headroom `1 − b(v) → 0` as MAF → 0. Both terms move the same direction; there is no product of opposing functions and no interior maximum. The feasibility reviewer independently found that E2 evaluates held-out individuals, which makes it an imputation benchmark against Beagle, not a leakage measurement. Two independent, load-bearing defects. Also dead as a first paper.

### What I am giving up, stated plainly

1. **The kinship story** — highest ceiling, no text analogue, unscoopable. Deferred, not abandoned. Staked with Ayday in month 1.
2. **The Duan-shaped MIA correction** — the near-certain result. Not published; handled privately.
3. **Attribute inference** — the largest unexecuted Aim 1.1 item. Dropped on merits (Jayaraman & Evans CCS 2022; LD imputation eats the headroom) plus the wiring defect above.
4. **All of Aim 1.2** — confirmed unassigned, preliminary figures already drawn, and the single most theoretically novel unclaimed item in either document (frequency-stratified DP noise). Deferred on the utility-axis ruling.
5. **Cross-architecture breadth** — no Evo, no full DNABERT-2, no HyenaDNA in the core. This is the feature that made the BCB paper the BCB paper, and I am dropping it. A reviewer can legitimately ask whether these are properties of small causal transformers. That is the trade I am making for immunity to findings D, E and F, a sub-8 GB disk footprint, and a schedule that finishes.
6. **The demonstrated-harm motivation.** There is no individual, no re-identification, no breach. This is worse at USENIX/CCS and better at NeurIPS/SaTML — which matches Spencer's stated preference, but it forecloses the venue where Ayday's group has standing.

### Why the ICML/NeurIPS "why not text?" question survives here and did not survive elsewhere

Three answers, ranked by how load-bearing each is. The first one is the paper's spine and it must be in the first page, not a footnote.

**1. Tokenization granularity over a fixed, closed, complete alphabet, on identical data (fully non-portable).** The *same* 288-nucleotide string, carrying *identical* information, tokenized at character / non-overlapping 3-mer / non-overlapping 6-mer / BPE-4096 granularity. You cannot run this in text: an English tokenizer change changes what a token means semantically, the vocabulary distribution co-adapts to the corpus, and character-level English is not a lossless objective-agnostic representation the way `{A,C,G,T}` is. This is the experiment that exists nowhere else, and it is the one both novelty reviewers independently asked for.

**2. The computable entropy floor (partially portable — concede it, then state the residual).** Uniform synthetic DNA is exactly 2 bits/nt, so held-out per-nucleotide perplexity is exactly 4.000, and any value below is an *impossibility proof* that the scoring protocol leaks. This is how finding D was caught (DNABERT-2 at 2.69). Concede up front that a uniform-token null corpus is constructible in any modality. The residual is real: in DNA the null corpus is not a toy — synthetic uniform DNA is one of the four datasets the field actually trains and evaluates on, so the calibration test runs on the production pipeline rather than a special case; and real genomic sequence sits near a measurable bound (~1.9 bits/base by compression), extending the argument past the synthetic case.

**3. The conditioning budget in exact bits (non-portable, and it directly beats the two 2026 competitors).** For matched-conditioning infilling, K revealed nucleotides on uniform DNA is exactly 2K bits, in closed form. Both von Arx & Dieudonné (arXiv:2605.22981) and Wang & Asokan (arXiv:2605.24173) match on **token counts**, which is a proxy that breaks the moment tokenizers differ. Mine is exact. This is the one place where the tokenization axis and the objective axis reinforce each other rather than merely coexisting.

### Positioning against the two May-2026 papers — write this paragraph in week 1

Both bracket the objective question and neither covers it.

- **von Arx & Dieudonné, "Memorization Dynamics of Fill-in-the-Middle Pretraining."** FIM is still autoregressive with a permuted factorization; the model never conditions bidirectionally on unobserved positions. My MLM arm does. They match conditioning in tokens; I match in bits. They use one tokenizer; tokenization is my second axis.
- **Wang & Asokan, "Extracting Training Data from Diffusion Language Models via Infilling."** Masked-diffusion LMs are trained with a *time-varying* mask schedule and a different denoising objective; BERT-style MLM at a fixed rate is a different training distribution. Their contribution (mask geometry governs extractability, 3× effect) is something I *use* as prior art in E3's design, not something I re-derive.
- **Mireshghallah et al., EMNLP 2022** supplies reference-MLM likelihood-ratio scoring and **Salazar et al. 2020** supplies PLL. **Claim neither as novel.** What is new is the controlled backbone, the tokenization cross, the mask-rate dose-response, and the variance decomposition.

**Also engage `PMC13340166`** ("Tokenization strategy, rather than domain specialization, emerged as the primary determinant of the privacy-utility balance"). It is adjacent and a reviewer will know it. The delta: they study **embedding-reconstruction** privacy across 13 heterogeneous models with different architectures, sizes and corpora; I study **memorization and extraction** on a single controlled backbone where tokenization is the only thing that changes. Their result makes my hypothesis live; it does not answer it.

### The one thing that makes this paper safe: the result is guaranteed

This is the decisive structural advantage and it is the reason I am recommending this over anything else on the panel.

Every other framing's headline is a coin flip. Does the ranking reverse? Does the interior maximum exist? Is the circularity effect large? Does β move with entropy? If no, the paper dissolves and is discovered at month four.

**A variance decomposition is a number you get regardless.** "Tokenizer accounts for X% of the variance in measured memorization, objective for Y%, mask rate for Z%, seed for W%" is a result whether the percentages are large or small. If tokenizer+objective reproduce the full published cross-model spread, the headline is "architecture was not identified." If they account for 40%, the headline is "architecture carries a residual of 60%, and here is the first quantification of it." If they account for 5%, the headline is "architecture is robustly the dominant factor, confirmed under control" — which validates the published paper and is a genuinely useful, publishable, and *politically ideal* outcome.

There is no branch of this experiment that produces nothing. That is worth more to a first-year with six months than any amount of ceiling.

---

## 3. THE EXPERIMENT PLAN

### Design decisions fixed in week 1 (do not defer these — they bite in week 12)

| Decision | Value | Why |
|---|---|---|
| Host window length | **288 nt** | Divisible by 1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 96 — char, 3-mer and 6-mer all tile exactly, no boundary fudge |
| Probe length | **96 nt** | Same divisibility; 96/3 = 32 tokens, 96/6 = 16 tokens |
| Probe placement | **offset 96** within the host window (a multiple of 6) | Keeps k-mer token frames identical across tokenizers |
| Probe insertion | **embedded inside host windows**, tagged at construction | Kills finding B at source; kills finding C structurally; keeps corpus size honest |
| Corpus size | **N = 15,000 windows** | Fits E. coli (16,116 windows at stride 288) so N is held constant across the synthetic and real arms |
| Repetition tiers | **r ∈ {1, 4, 8, 16}**, 30 probes per tier | 30/tier honors the proposal's own power requirement (L300: *"N ≥ 30 canaries per configuration"*), which the paper missed at 25/tier. Insertions = 30 × 29 = 870 → **5.8% of windows, 1.9% of tokens** carry a probe. The published config sits at 47% of examples; state this contrast as a one-line finding, not a footnote |
| Parameter matching | **Non-embedding params fixed** (4 layers, d=512, 8 heads). Embedding params reported as a covariate; **tied input/output embeddings**; plus one capacity-matched control cell with reduced `d_model` for large-vocab arms | Vocab 8 → 4k embedding params; vocab 4096 → 2.1M. Without this, tokenizer is confounded with capacity and a reviewer kills the headline |
| Padding | **Dynamic padding with attention masks; loss masked on PAD** | See §4, finding G — this is not hygiene, it is the confound that would otherwise *be* the tokenizer effect |
| Seeds | **3 for the grid, 5 for headline cells**, plus bootstrap CIs at N=1000 resamples over candidate pools | The proposal promised k=5 and bootstrapped CIs (L299–303); the paper delivered 3 seeds and no CIs. Cheap to honor |
| Reporting | Calibrated rank p-value; **rank-1 verbatim recovery rate**; TPR@FPR 1e-3 and 1e-4 on log-scale ROC; bounded-prior posterior advantage. **All metrics per nucleotide, never per token** | Rank-1 is threshold-free and floor-immune; it exists in the proposal (L261) and was dropped from the paper. Per-nucleotide is Alex #3 and the commensurability fix |

---

### E0 — Calibrated instrument and null battery **[CORE]**

**Question.** Does each metric return its analytically known value on a corpus whose answer is known in closed form — and is pseudo-log-likelihood exchangeable with autoregressive likelihood as a ranking function?

**The second half of that question is the paper's single point of research risk and it must be answered before the grid runs.** The `scaling-and-objective` feasibility reviewer identified the hole correctly: rank is invariant under a monotone transform applied uniformly to all candidates, but **not** to swapping in a scorer that induces a different ordering with different noise. If `f_PLL` is the noisier estimator, a canary's rank degrades at equal memorization and you would report "MLM memorizes less" having measured "PLL is a noisier ranker." That is finding C's structure reappearing one level up.

**The scorer-equivalence control (run this first).** Score **one AR-trained model** under both `f_AR` and `f_PLL`. Three checks:
1. Do the rank distributions of the probe set agree (Spearman ρ, and agreement in rank-1 recovery)?
2. Does `f_PLL`'s implied per-nucleotide entropy on held-out uniform DNA equal **2.000 bits**? (This is the entropy-floor test applied to the *scorer* rather than the model — a genuinely novel methodological move that only DNA permits, and worth a half-page in Methods.)
3. Reverse direction: score an MLM-trained model under `f_PLL` and under a causal-masked forward pass. Is the bias symmetric?

If the scorers disagree with a *measurable, correctable* bias, correct it and report the correction. If they disagree unpredictably, E1's cross-objective comparison is restricted to within-objective contrasts plus E3's infilling, and the headline narrows to tokenization. **Decide this at Gate 2, week 6.**

**Null battery.** Four null conditions per metric: (a) randomly-initialized model; (b) model trained on a disjoint corpus that never saw the probes; (c) analytic chance floor per scorer (`P(rank ≤ k) = k/(|pool|+1)`; the shipped protocol's is exactly 100/1001 = 9.99%); (d) a blind baseline using only surface statistics of the probe (length, GC, k-mer composition) with no model access, per Das/Zhang/Tramèr.

**Models.** SimpleDNALM d=512, char tokenizer. **Datasets.** Synthetic uniform (H = 2.000 bits/nt exactly), E. coli K-12 as non-null control.
**GPU.** ~20 A100-h. **Disk.** <1 GB.
**Becomes.** Table 1 (null battery: every metric × every null condition × as-published vs corrected protocol) and a Methods subsection on scorer calibration.

---

### E1 — The commensurable grid: tokenizer × objective variance decomposition **[CORE — HEADLINE]**

**Question.** With architecture, non-embedding parameter count, data, probe set and optimization budget held fixed, how much of the spread in measured memorization is attributable to tokenizer granularity, to pretraining objective, and to seed — and how does that spread compare in magnitude to the cross-model spread the published work attributes to architecture?

**Axes and levels.**
- Tokenizer ∈ {char (vocab 8), non-overlapping 3-mer (vocab ~68), non-overlapping 6-mer (vocab ~4100), BPE-4096 trained on public DNA}
- Objective ∈ {causal AR, MLM@0.15, MLM@0.30, MLM@0.50}
- Repetition tier r ∈ {1, 4, 8, 16} — **lives within each run**, costs no extra runs, and delivers the proposal's promised per-tier disaggregation for free
- Seeds: 3 (5 at the four headline cells)

Full 4×4 grid on synthetic (48 runs) + reduced 4×2 (AR, MLM@0.30) on E. coli (24 runs) + 2 extra objectives (T5-style span corruption, prefix-LM) at char only × 3 seeds (6 runs) + capacity-matched control (2 large-vocab arms × 2 objectives × 3 seeds = 12 runs). **≈ 90 runs.**

**Controls.** Zero-probe run per (tokenizer, objective) cell for the baseline train/test gap; identical probe set reused across every cell; **dual optimization budget** — fixed epochs as primary, fixed *supervised-token* count as control (an MLM at m=0.15 sees ~6.7× fewer supervised positions per pass, so either currency alone is uninterpretable and a reviewer will say so); explicit trainable-parameter ledger per arm.

**Metrics.** Calibrated extraction rate, rank-1 verbatim recovery, exposure against a 10⁵ shared pool, canary-vs-test perplexity gap — **all per nucleotide.** Variance decomposition by nested ANOVA / mixed model with bootstrap CIs.

**GPU.** ~150 A100-h training + ~80 A100-h probing. **Disk.** ~5 GB (90 × 52 MB fp32, or 2.4 GB bf16). Persist per-probe score arrays (~1 MB each), not intermediate checkpoints.

**Becomes.** **Figure 1** — the variance decomposition, the paper's central figure. **Figure 2** — per-nucleotide vs per-token metrics side by side, showing how much of the *published* cross-model spread is a units artifact (a 96-nt probe is 96 tokens under char, 32 under 3-mer, 16 under 6-mer, ~24–30 under BPE; the published tables compare these directly). **Table 2** — per-tier disaggregation, the thing §4.3.3 announced and never showed.

---

### E2 — Mask-rate dose-response **[CORE]**

**Question.** Is the masked/causal distinction qualitative or quantitative? Concretely: does measured memorization vary *continuously* with mask rate, with causal AR sitting at the m = 1.0 endpoint of a single curve?

This experiment is the answer to the `scaling-and-objective` novelty reviewer's best point: a dose-response survives regardless of whether any particular functional form (their `E_eff` scalar) holds, whereas an A/B does not. It is also the direct test of the BCB paper's own mechanistic hypothesis (L460–470) that masked pretraining produces "distributed, unextractable" memorization — which, per finding D, has never actually been measured, because the only published masked GLM was scored open-book.

**Axes.** Mask rate m ∈ {0.05, 0.15, 0.30, 0.50, 0.80} at char tokenizer, plus causal AR plotted at m = 1.0. Second tokenizer (6-mer) at three mask rates as a replication. r ∈ {1, 4, 8, 16} within run. 3 seeds.
**Runs.** (5 + 3) × 3 = 24, plus reuse of E1's AR cells.
**Controls.** Both budget currencies again; fixed total optimizer steps AND fixed supervised-token count.
**GPU.** ~40 A100-h. **Disk.** ~1.5 GB.
**Becomes.** **Figure 3** — exposure and rank-1 recovery vs mask rate, with causal AR at m=1.0 and a fitted curve. If the curve is smooth and AR sits on it, "masked models are safer" is a rescaling, not a property. If AR sits off the curve, the residual localizes exactly where a genuine qualitative difference lives — and *that* is the more interesting paper.

---

### E3 — Matched-conditioning infilling: discoverable vs extractable memorization **[CORE]**

**Question.** Is memorized content in masked models *present but not emittable*, or simply absent? Under an adversary supplying the same number of known nucleotides, in the same positions, at the same search budget, does an MLM recover the probe at the same rate as a causal model?

This is the second half of what Alex's extension #2 requires to be measurable at all, and it is where the "exact bits of conditioning" advantage does real work.

**Protocol.** Adversary supplies K known nucleotides at the sequence start, K/96 ∈ {0.25, 0.50, 0.75}. AR completes by beam search (width 10, KV-cached — the existing `beam_search_generate` does a full padded forward per beam per step and must be rewritten). MLM completes by **strictly left-to-right iterative unmasking** — *not* confidence-ordered, which would give the MLM an easy-positions-first advantage the AR model structurally cannot have and would break the matching. Same beam width, same budget. Report exact-match recovery on the suffix, plus edit distance.

**Scope note on BPE.** Infilling is run on **char, 3-mer and 6-mer only**, where token boundaries are deterministic. BPE is excluded from E3 with a one-paragraph explanation: a nucleotide string has exponentially many valid BPE tokenizations, so "did the model emit the correct suffix" is ill-posed without constrained decoding over the token lattice. This is honest, it is a real open problem, and **it does not touch E1 or E2**, because the primary probe there is rank-based scoring of a fixed string, which needs no generation and no decode. Flagging this scope limit up front is what keeps the BPE problem from becoming the 15-day time sink it was in the `vulnerable-prompts` plan.

**Models.** E1's trained checkpoints. Attack-only for most of it.
**GPU.** ~50 A100-h (beam search is the expensive part). **Disk.** negligible.
**Becomes.** **Figure 4** — recovery rate vs conditioning fraction, AR vs MLM at matched bits, per tokenizer. This is the figure that says "discoverable but not extractable" or "not there at all."

---

### E4 — External validity on real pretrained GLMs **[STRETCH — cut second]**

**Question.** Does the law fit on a 12.9M from-scratch backbone predict memorization in real pretrained genomic foundation models?

**Two arms.** (a) **DNABERT-2** (117M, BPE, MLM) scored through its **native MLM head by PLL** — not through the repo's bolted-on causal head. This deliberately avoids the hardest engineering path (injecting a causal mask into MosaicBERT's custom `trust_remote_code` attention) and is also the principled choice, because PLL on the native head is what the model was pretrained for. **In my design this is not a bug fix — it is the same scorer E0 already built.** (b) **HyenaDNA** (14.2M, single-nucleotide, causal) with its pretrained unembedding restored rather than replaced by a fresh `nn.Linear`. If restoring the head does not bring its held-out perplexity below the 4.0 uniform-chance value, **drop the arm and say so in Limitations** — do not spend a week on it.

**Evo is excluded permanently**, and the reason goes in Limitations: `get_peft_model` is applied to `self.model.encoder` only while the fresh `lm_head` is never frozen and `trainer.py:162-166` optimizes all parameters, so "LoRA-only" does not describe what the code does; disentangling adapter capacity from a fully-trained readout is its own project.

**GPU.** ~40 A100-h. **Disk.** ~3 GB (DNABERT-2 checkpoints ~470 MB each; save finals only).
**Becomes.** **Figure 5** — predicted vs observed, two anchor models.

---

### E5 — Corpus scale and repetition regime as controls **[STRETCH — cut first]**

**Question.** Does the tokenizer × objective decomposition hold at 4× corpus size, and does the repetition-tier structure change shape? (Alex's extension #1, in reduced form.)

**Axes.** N ∈ {15,000, 60,000} × tokenizer ∈ {char, 6-mer} × objective ∈ {AR, MLM@0.30} × 3 seeds = 24 runs, of which 12 are already in E1. Both budget currencies. Probe mass reported per cell as a covariate.
**GPU.** ~70 A100-h (dominated by the N=60k cells). **Disk.** ~1 GB.
**Becomes.** **Figure 6** or a Table 3 robustness panel. If cut, one sentence in Limitations: "we hold corpus size fixed; the scaling behaviour of this decomposition is left to future work" — which is honest and costs nothing.

---

### Totals

| | |
|---|---|
| Experiments | 6 (4 CORE, 2 STRETCH) |
| Display items | 6 figures + 3 tables → trim to **5 figures + 2 tables** in a 9-page body, with Table 2 and Figure 6 to appendix |
| GPU (CORE only) | ~260 A100-hours |
| GPU (with STRETCH) | ~370 A100-hours |
| Disk (everything) | **< 8 GB** |
| Shadow/reference models | **zero** |
| Human subject data | **zero** — no IRB, no dbGaP, no README:289 reversal |
| Genomics on the critical path | **essentially zero** — k-mer tokenizers, GC content, a FASTA reader |

**The disk number is the pitch to Alex.** His only stated constraint is *"we just have to be mindful of storing the models."* A correct reference-model LiRA costs 768 runs and ~23 GB with adapter-only checkpointing (~10 TB without). A corpus-scaling grid with Evo costs up to 2 TB. This paper costs **8 GB** and needs no Evo, no full DNABERT-2 training, and no shadow models. Lead with that number in the first meeting.

---

## 4. THE BUG-FIX QUESTION

### Which findings block *this* paper, in what order

**Order matters: fix in this sequence, because each one is a precondition for measuring the next.**

| # | Fix | Days | Status |
|---|---|---|---|
| **1** | **G — SimpleDNALM trains on padding** | 1 | **BLOCKING — CRITICAL** |
| **2** | **H — checkpoint selection & early stopping on unmasked loss, on the TEST split** | 2 | **BLOCKING** |
| **3** | **B — probe tracking; replaced, not patched** | 3 | **BLOCKING** |
| **4** | **A — extraction chance floor** | 1 | **BLOCKING (and it is the cheapest day in the project)** |
| **5** | Efficiency: AMP, batch size, pre-tokenization, dynamic padding | 3 | Enabling |
| **6** | C — padding mask in the MIA loss path | 0.5 | Hygiene, one line |
| **7** | D — PLL scorer for bidirectional models | 3 | Needed for E0/E3; **it is the method, not a repair** |
| **8** | Golden tests + sweep driver + SLURM templates | 4 | Infrastructure |
| | **Total** | **~17 engineer-days ≈ 4 weeks at realistic first-year throughput** | |

**Why G is first and why it is the most important finding in this dossier for this specific paper — and nobody flagged this.**

`dnabert_wrapper.py:278` uses `CrossEntropyLoss(ignore_index=-100)` but `dataset.py:342` sets `labels = input_ids.clone()` and `dataset.py:193` sets `pad_token_id = 0`. Padding is **never** ignored. That is bad in general. Here it is **specifically fatal**, because the padding fraction *varies systematically with tokenizer*:

- A 288-nt window in a 512-token buffer: **char** → 288 real tokens, 43.8% padding. **3-mer** → 96 tokens, 81.3% padding. **6-mer** → 48 tokens, **90.6% padding.**

So a 6-mer model would spend 90% of its gradient learning to predict `[PAD]`, and "the 6-mer model memorizes less" would be entirely explained by that. **G is not overhead for this paper — without it, the headline experiment is uninterpretable, and the confound points in the direction that would make the result look most exciting.** Fix it with masked loss *and* dynamic padding sized per tokenizer, then assert in a golden test that the padding fraction of the loss is exactly zero.

H compounds G directly: `trainer.py:356` accumulates the unmasked loss, `:433` selects `best_model.pt` on it, `:439` early-stops on it, and the correctly-masked perplexity at `:359-363` is computed, logged and discarded — so "best model by validation loss" partly means "best at predicting padding," and early stopping at `patience: 5, min_delta: 0.001` on a padding-diluted signal can halt runs **differentially across tokenizer arms**. Memorization is a late-training phenomenon; a run that stops early under-reports it. Also, `run_experiment.py:151-153` passes `eval_loader=test_loader`, so selection happens on the evaluation split. Build a real three-way train/validation/test split and select on masked validation perplexity.

A is the cheapest and highest-leverage day in the whole project: `extraction_attack.py:204` re-seeds `np.random.default_rng(42)` *inside* `rank_canary`, so all probes are scored against an identical fixed 1,000-candidate pool at 100 × 1,001 unbatched forward passes per model per config. Hoisting the pool out and batching it is ~91× then another 10–30×, which **buys a 10⁵-candidate pool for less than the current cost of 10³**. That simultaneously fixes the 9.99% chance floor, gives exposure real range (currently confined to [118.03, 128] against a nominal 128), and makes 90 models × 2 scorers affordable.

**Environment — and this is a large, under-appreciated win.** The core of this paper needs **none** of the pinned stack. `requirements.txt` is a `pip freeze` pinning `transformers==4.29.2`, `torch==2.1.1+cu118`, `opacus==1.4.0`, an unresolvable `evo-model @ file:///your/evo/model/path`, and `evo==1.34.3` (which is the SLAM trajectory-evaluation package on PyPI, not a genomic model). Every competing framing budgets 1–3 weeks fighting this. **SimpleDNALM is pure PyTorch `nn.TransformerEncoder`** — Spencer builds a clean minimal environment (recent torch + numpy + `tokenizers` + `biopython` for FASTA) in one day and never touches the legacy pins for any CORE experiment. Only E4 (STRETCH) needs the HF stack, and by then he can afford the time.

### How to frame each finding — the three-bucket rule

| Finding | Bucket | What goes in the paper |
|---|---|---|
| **A** (chance floor) | **Silent methodology, one sentence + citation** | "We calibrate the null rank distribution for each scoring function and report rank-based results as calibrated p-values together with the threshold-free rank-1 verbatim recovery rate [cite Jagielski arXiv:2306.00133]." No comparison to a published number. |
| **B** (probe tracking) | **Silent — the code is replaced, not patched** | "Probes are embedded within host windows and tagged at construction time." That is a design statement, not a correction. |
| **C** (MIA length) | **PRIVATE CONVERSATION WITH ALEX. Not in the paper at all.** | The paper's design makes it moot (all windows length-matched). One methods sentence: "all sequences are length-matched by construction, so membership statistics cannot separate on length." A reader who knows will notice; a reader who does not is not being misled. |
| **D** (open-book scoring) | **The method, presented positively** | "Bidirectional encoders are scored by pseudo-log-likelihood [Salazar 2020; Mireshghallah 2022], which is the objective-native scoring function; scoring a bidirectional encoder with a causal-shift head does not yield a valid sequence probability, a pitfall recently identified in the fill-in-the-middle and diffusion-LM settings [von Arx 2026; Wang & Asokan 2026]." **Zero mention of the BCB paper in that sentence.** It is a known, named, cited failure class. |
| **E/F** (fresh heads, LoRA claim) | **Limitations, one sentence, for the models I excluded** | "We exclude Evo because the published evaluation trains a full-rank output head alongside the low-rank adapter, which confounds adapter capacity with readout capacity." Neutral, factual, about scope. |
| **G, H** (padding, selection) | **Silent methodology** | "Loss is computed only over non-padding positions; model selection and early stopping use masked validation perplexity on a held-out validation split disjoint from the test set." |

**The single most important word choice in this entire project is "unidentified," not "wrong."** The paper's claim is that the published architectural comparison is *not identified* — it varies four things at once — and that a controlled ablation is needed. **The paper itself says this, in print, at L567–570.** Spencer is not contradicting Alex; he is executing the experiment Alex's own Discussion section asks for. If Spencer never departs from that framing, there is no political problem to manage.

### The interpersonal plan — concrete, in order

This matters as much as the science, and the sequencing is not negotiable.

**Step 1 — Book a 1:1 with Alex. Video or in person. Not email, not Slack, not a shared document.**

Email to request it, and the email contains **only** this:

> Subject: Following up on the BCB paper — a controlled ablation I'd like to build with you
>
> Hi Alex — I've been reading through the BCB paper and the repo carefully. Your Discussion section says a controlled ablation comparing pretraining objectives on a fixed architecture would be needed to establish a causal relationship, and that the method doesn't isolate tokenization strategy. I'd like to build exactly that as my spinoff, and I'd like you on it. Do you have 45 minutes this week or next? I have a bunch of implementation questions I'd rather ask than guess at.

That is the whole email. No findings. No line numbers. No attachments.

**Step 2 — In the meeting, lead with the idea for the first ten minutes.** Present the grid, the variance decomposition, and — critically — **the 8 GB disk number**, because storage is the constraint he named. Propose him as a coauthor before he has to wonder. Say it out loud: *"I'd want you on this as a coauthor, obviously — it's your framework."*

**Step 3 — Then ask the implementation questions, as questions.** These are genuine open questions, not accusations, and he may well already know the answers:

- "I want to reimplement the extraction vector the way you intended. The Methods describe prefix-conditioned beam search, but `run_experiment.py:210` calls `attack_all_canaries`, and `prefix_attack` doesn't seem to get called. Was the rank-based version the intended one, or is that a wiring gap?"
- "For DNABERT-2 — was the causal shift over the bidirectional encoder deliberate? For my version I was going to use its native MLM head with pseudo-log-likelihood, since that's what it was pretrained for. Does that seem right to you?"
- "Do you still have the script that produced Table 3? `metrics.py` implements the weighted 0.3/0.3/0.4 aggregation from the proposal rather than the max from the paper, so I can't regenerate it from the repo."

That last one matters practically and it is not remotely confrontational.

**Step 4 — Raise C only after he is engaged, and only as arithmetic, in the same 1:1 or the second one.** Never in writing first.

> "One thing I wanted to sanity-check with you. The train set has 900 standalone 64-nt canary copies and the test set is all 256-nt, and `compute_losses` averages over all 512 positions including padding. I worked out what a length-only classifier would get — 900/1900 plus half of 1000/1900, which is 0.737 — and that's basically the band in Table 5. I might be misreading the code. Can you check my reasoning?"

Then **stop talking and let him respond.** This is his call to escalate or not. Spencer's job is to have raised it privately, once, with the arithmetic, and then follow Alex's lead. If Alex wants to handle it as a repo update, a corrigendum, or nothing at all, that is his and Ayday's decision, not Spencer's.

**Step 5 — Separately, later, meet Ayday.** After Alex is on board. Ayday gets: the project pitch, the venue target and timeline, the resource argument (8 GB, ~300 A100-h, no human data so no IRB), the fact that Alex is a coauthor, and the one-page kinship sketch as project two. **Ayday does not get a findings list.** If Alex has escalated something, Ayday already knows; if he has not, it is not Spencer's to escalate in his first month.

### What NOT to do — explicitly

- **Do not send a numbered list of findings to anyone, ever.** Not to Alex, not to Ayday, not in a group channel, not in a shared doc.
- **Do not use the words** "bug," "error," "wrong," "invalid," "broken," "does not support the claim," or "the published numbers are." Use "unidentified," "confounded," "I want to make sure I reimplement this correctly," "known pitfall in this class of models."
- **Do not CC Ayday on anything about the code** in the first three months.
- **Do not put the padding / open-book / chance-floor analysis in a shared document, a lab wiki, or a slide deck** before Alex has heard all of it verbally and had a chance to respond.
- **Do not present at lab meeting** with a slide comparing "published" to "corrected" numbers. If a lab-meeting talk is needed, present the *forward-looking* design: the grid, the ablation, the variance decomposition.
- **Do not claim PLL or the length-confound observation as your discovery.** Both are cited, named failure modes in the 2026 literature (von Arx & Dieudonné; Wang & Asokan; Duan et al. 2024; Das/Zhang/Tramèr 2024; Fan et al. 2606.31168). Attributing them to the literature rather than to your own audit is both more accurate and vastly less abrasive.

### The contingency, and it is strong

**If Alex reacts badly, this paper still runs.** Not one CORE experiment compares against a published number. The models are built from scratch by Spencer, on a backbone he controls, with a probe set he designs. Worst case, he builds his own family, cites the BCB paper as motivation, and writes a Related Work paragraph. That is a genuinely robust fallback, and it is a primary reason I am recommending this framing over any that requires repairing the published instruments before it can begin.

---

## 5. TIMELINE — weeks 1–24 (starting 2026-09-22)

### Phase 1 — Foundation and Gate 1 (weeks 1–6)

**W1.** HPC access request submitted (long lead time — do it first). Clean minimal environment built locally. Read von Arx & Dieudonné 2605.22981, Wang & Asokan 2605.24173, Mireshghallah EMNLP 2022, Salazar 2020, PMC13340166. Write the one-paragraph positioning delta against each. Confirm 2027 venue deadlines. Email Alex for the 1:1.

**W2–3.** Build a **standalone throwaway pilot harness** — deliberately bypassing most of the repo. SimpleDNALM d=512, char tokenizer, causal AR and MLM@0.15, N=5,000 synthetic uniform, 20 probes at r ∈ {1, 16}, batched scorer with a 10⁴ pool. Fix G and H in the pilot harness only (these are two small changes and the pilot is meaningless without them).

> ### **GATE 1 — end of W3. ~5 GPU-hours. This is the most important date in the project.**
>
> Three questions:
> - **Q1 (scorer):** Do `f_AR` and `f_PLL` rank the probe set consistently on the same AR-trained model? Does PLL's implied per-nucleotide entropy on held-out uniform DNA land at 2.000 bits?
> - **Q2 (dynamic range):** Does extraction at r=16 exceed r=1 by more than seed noise, under the calibrated null?
> - **Q3 (objective signal):** Does MLM@0.15 differ measurably from AR under matched scoring?
>
> **Branches.** Q2 fails → raise N and r before the main grid; the instrument lacks resolution, not the science. Q3 flat → **pivot the headline to tokenization-only** and drop the objective axis to a two-level control; the paper survives, narrower. Q1 fails unrecoverably → restrict all cross-objective comparison to E3's infilling protocol and state it in Methods; if E3 also cannot be matched, **switch to the runner-up (§7) at week 4, with 20 weeks intact.**

**W3–6.** Full foundation in parallel with the pilot: B (probe builder), A (pool hoist + batching + 10⁵ pool), efficiency work (AMP, batch size, pre-tokenization, dynamic padding), golden tests (padding-fraction = 0; probe-flag precision = 1.0; split disjointness; chance-floor calibration; held-out perplexity ≥ 4.000 on uniform), sweep driver + SLURM templates.

> ### **GATE 2 — end of W6.** The scorer-equivalence control at full rigor, both directions, on the real harness. Green → run E1. Amber (measurable correctable bias) → apply the correction, document it, run E1. Red → E1 runs as a tokenization study only.

### Phase 2 — The grid (weeks 7–12)

**W7–11.** E1 main grid, ~90 runs. Batch submission; monitor, do not babysit. **W10–12.** E2 dose-response, overlapping E1's GPU queue.

> ### **GATE 3 — end of W12.** The variance decomposition.
>
> - **Strong** (tokenizer + objective reproduce ≥60% of the published cross-model spread): headline is "architecture was not identified." Aim NeurIPS. Write the introduction in that register.
> - **Moderate** (30–60%): headline is the quantification itself — "the first decomposition of memorization variance in genomic LMs, with architecture carrying a residual of X%." Still NeurIPS-viable; SaTML certain.
> - **Weak** (<30%): **architecture genuinely dominates under control.** This validates the published paper, which is a good outcome scientifically and an excellent one politically. Pivot the headline to the **dose-response (E2) plus the per-nucleotide commensurability correction**, both of which are results regardless. Target SaTML 2028. Do not force the NeurIPS framing.

### Phase 3 — The protocol contribution (weeks 13–17)

**W13–16.** E3 infilling: build the KV-cached beam search and the left-to-right unmasking decoder, run at three conditioning fractions across three tokenizers.

> ### **GATE 4 — end of W16.** Does the infilling result agree with the ranking result? Agreement → memorization is present and emittable; the story is clean. Disagreement → **this is the better paper**: "discoverable but not extractable" under masked objectives, which is the Carlini/Nasr framing and directly answers the BCB paper's mechanistic hypothesis. Either way, write it up.

**W17.** Buffer. Re-run anything that failed. This week exists because something will.

### Phase 4 — Stretch and writing (weeks 18–24)

**W18–20.** E4 (external validity) if Gate 3 was Strong or Moderate; otherwise E5 (scale controls) or skip both and start writing early.
**W20–22.** Full draft. Figures built from persisted score arrays, not from re-running anything.
**W23.** Internal review — Alex first, then Ayday. Expect demands for ablations; W24 absorbs them.
**W24.** Revision. Draft complete ~2027-03-08.

**W25–32 (outside the plan, before the May deadline).** Ablations from internal review, related-work deepening, polish, submission.

> ### **GATE 5 — week 20.** If fewer than three CORE experiments have landed, cut both STRETCH arms, cut E3 to char-tokenizer-only, and target **SaTML 2028** instead of NeurIPS 2027. That is a four-month schedule slip with a revision path and it costs nothing but ambition.

---

## 6. WHAT SPENCER DOES THIS WEEK

In this order. All five are doable in a week and none require HPC.

**1. Request HPC access and, specifically, ask for the numbers nobody else asked for.** Not just "do I have an allocation" but: *how many concurrent GPU jobs can I run, what is the max walltime per job, what is my scratch quota, what is the scratch purge policy, and are the GPUs A100-80GB or something older?* Every proposal on the panel implicitly assumed infinite parallelism. 300 A100-hours on 1 concurrent GPU with a 12-hour walltime cap and day-long queues is a 6-week wall-clock item, not a 2-week one. **This has a queue; start it Monday morning.**

**2. Build a clean minimal environment and get SimpleDNALM to train for 100 steps.** A fresh venv with recent `torch`, `numpy`, `tokenizers`, `biopython` — deliberately *not* `requirements.txt`, which pins `torch==2.1.1+cu118`, `transformers==4.29.2`, and an unresolvable `evo-model` path. Import `SimpleDNALM` from `src/models/dnabert_wrapper.py` directly, generate 500 synthetic sequences, train 100 steps on CPU or a local GPU. **Goal: confirm the model class runs at all, decoupled from the rest of the repo.** This is the single highest-information hour of the week.

**3. Write a 30-line script that confirms G and H with printed numbers.** 
- For G: tokenize one 256-nt sequence at `max_length=512`, build labels the way `dataset.py:342` does, and print the fraction of loss terms where the label equals `pad_token_id`. Expect ~0.49. Then print it for a hypothetical 6-mer tokenization. Expect ~0.91.
- For H: print which `DataLoader` object `run_experiment.py:151-153` passes as `eval_loader`, and print which loss tensor `trainer.py:433` selects on.

These take twenty minutes and they are the two facts that determine whether the headline experiment is interpretable. **Save the output — it is what Spencer will need when he explains his design choices, and it is evidence he read the code rather than a report about the code.**

**4. Read the four positioning papers and write the delta paragraph.** von Arx & Dieudonné (2605.22981), Wang & Asokan (2605.24173), Mireshghallah et al. (EMNLP 2022), Salazar et al. (2020), plus PMC13340166. Write one paragraph, ~150 words, stating exactly what each does and what this paper does that they do not. **If that paragraph cannot be written convincingly, the project needs rethinking now, not in month four.** Show it to Alex in the first meeting — it will read as seriousness, not as territory-marking.

**5. Send the meeting request to Alex.** The exact email text is in §4, Step 1. Nothing more in it than that. Then draft (but do not send) the one-page kinship project sketch for Ayday.

---

## 7. RUNNER-UP

**Kinship-conditioned membership inference on real pedigrees — the paper where the imputation and blind-baseline critiques invert into the experimental design.** Train a genomic LM on a cohort of related individuals from 1000G 30x (3,202 individuals, 602 trios, fully open) or the Platinum Pedigree; then, holding the genome of a *relative* of a candidate, measure whether the relative's membership is detectable above the rate their own non-membership should permit, with the kinship coefficient φ (0.5 parent/sibling → 0.25 → 0.125 → 0 unrelated) as a continuous, ground-truthed difficulty dial. It is the only cell `novelty-scan` found unoccupied, the only direction with no text analogue an NLP lab can scoop, it closes the gap between the BCB paper's own motivation (*"familial propagation of privacy risk has no direct analog in text-based memorization"*) and what it measured, and its theory anchors are Humphries et al. CSF 2023 plus Almadhoun/Ayday/Ulusoy *Bioinformatics* 2020 — which means Ayday's own prior work is the genomics anchor. It requires a correct reference-model LiRA, the pedigree-aware split, and above all the **blind baseline that separates model leakage from shared-sequence correlation**, which must be built first, not last.

**Switch trigger — one specific, dated condition.** If **Gate 1 (week 3) comes back Red** — the two scoring functions cannot be made exchangeable and the infilling protocol also cannot be matched in bits — the objective axis is unmeasurable and the recommended paper collapses to a tokenization-only study, which is thinner than I want to defend. In that case, at week 4, switch: spend weeks 4–6 on a variant-density feasibility probe (20 individuals, MHC/HLA chr6:28.5–33.4 Mb plus a high-density non-MHC stratum, does a membership statistic separate a parent-present cohort from a parent-absent one at all), and make a hard go/no-go at week 6 with 18 weeks remaining. **Secondary trigger:** if Ayday, in the month-1 meeting, says he wants the kinship direction started immediately and will sign off on human data — take it, and reverse the paper order. That would be his call to make and it is a good one; it just is not the call to make on Spencer's behalf.

---

## 8. OPEN QUESTIONS FOR ALEX AND AYDAY

### For Alex — in a 1:1, in this order, after ten minutes of leading with the idea

1. *"Your Discussion says a controlled ablation on a fixed architecture is what's needed to establish causality, and that tokenization strategy wasn't isolated. That's exactly what I want to build. Would you want to be on it as a coauthor?"* — ask this first, and mean it.

2. *"I want to reimplement the extraction vector the way you intended. The Methods describe prefix-conditioned beam search with a beam width of 10, but `run_experiment.py:210` calls `attack_all_canaries`, and `prefix_attack` doesn't seem to be called anywhere. Was the rank-based version the one that produced the numbers, or is that a wiring gap I should fix in my version?"*

3. *"For DNABERT-2 — was the causal-shift head on the bidirectional encoder a deliberate choice? For my ablation I was planning to score it through its native MLM head with pseudo-log-likelihood, since that's what it was pretrained for. Does that match what you'd do?"*

4. *"Do you still have the script that generated Table 3? `metrics.py` implements the weighted 0.3/0.3/0.4 aggregation from the proposal rather than the max from the paper, and Eq. 3 isn't in the repo, so I can't regenerate it."*

5. *"How would you want the corrected protocol handled — as a code update to the GLM-Memorization repo, or folded into my spinoff's methods section? Your call, it's your framework."* — **this is the question that determines whether the corrections are a repo commit or a Methods paragraph, and it is genuinely his to answer.**

6. *(Second meeting, or later in the first, after he is engaged)* — the finding-C arithmetic, phrased as in §4 Step 4.

7. Practical: *"What hyperparameters did you actually run? Not for exact reproduction — I know that's not required — but so I know whether I'm in the same regime."* And: *"Was `use_causal_mask` ever toggled off outside the DP path?"*

### For Ayday — separately, after Alex is on board

1. *"My plan is a controlled tokenizer × objective ablation on a fixed backbone — the ablation the BCB paper's Discussion asks for and Alex named as an extension. Alex would be a coauthor. Target is NeurIPS 2027 with SaTML 2028 as fallback. Does the venue choice work for you?"*

2. *"Resource-wise this needs about 300 A100-hours and under 8 GB of disk — no Evo, no shadow models, no human data, so no IRB. Is that within what you'd want me spending?"* — this answers the question he will ask before he asks it.

3. **The kinship claim, with the one-pager in hand:** *"The strongest unexecuted idea I've found is measuring whether membership leaks about relatives who were never in the training set — using the trios in 1000G, with the kinship coefficient as a difficulty dial. It connects to your Bioinformatics 2020 work on dependent tuples. I don't think I should start it until this paper is submitted, because it needs a VCF pipeline that doesn't exist and I'd rather build it properly. Can I claim it as project two?"*

4. *"That direction would need real human genomic data, and the repo's README currently states there is none in the pipeline. If I go there later, what's the process — is 1000G open-access enough, or does it need something formal?"* — ask now so the lead time is absorbed while paper one runs.

5. *"Aim 1.2 — I've concluded it can't be the first paper, because the whole aim is a privacy-utility tradeoff and there's currently no utility metric anywhere in the framework. A 12.9M model pretrained on a megabyte of data can't produce a moving downstream accuracy number. Building that utility axis is its own piece of work. Is it worth me scoping it as project three?"*

6. Housekeeping: *"Alex mentioned storage is the binding constraint on Pioneer. How much scratch do I have, and is there a purge policy I should plan around?"*

---

### Closing note on confidence

I am confident about the ruling that Aim 1.2 cannot be paper one (two independent reviewers found the same disqualifying mechanism), about the ruling that finding C must not be published by Spencer (four independent sources agree on the substance and the politics are unambiguous), and about the feasibility profile of this recommendation (verified line numbers, zero shadow models, zero human data, 8 GB of disk, no genomics on the critical path).

I am **less** confident about one thing and I will name it rather than bury it: **whether the tokenizer × objective spread will be large enough to support the "architecture was not identified" headline.** That is what Gate 3 exists to answer at week 12. But unlike every other framing on this panel, a weak answer there does not leave Spencer with nothing — it leaves him with a variance decomposition, a dose-response curve, and a commensurability correction, all of which are publishable results, and all of which validate rather than contradict his senior labmate's work. That asymmetry is the entire argument, and it is why this is the recommendation.