# Research chain: how the idea changed, and what forced each change

Written 14 Oct 2026. Built by extracting every belief revision from the three week logs
(69 entries, `08`, `09`, `17`) plus the original plan and the outline, then checking each one
against the log text: 118 revisions found, 107 confirmed verbatim, 11 plausible, none refuted, and
32 further revisions that the first pass had missed.

This document is the spine only: the ten points at which the paper itself changed shape. The
hundred smaller corrections stay in the week logs.

---

## 0. The original idea (18 Sep 2026)

> "tokenization granularity and pretraining objective account for memorization differences"

One small Transformer trained from scratch, everything else held fixed, and the deliverable was a
variance decomposition of memorisation across a tokeniser x objective grid. The tokeniser axis was
the novelty claim: the experiment that "exists nowhere else" and that "an NLP lab cannot get from
text". Released pretrained models were deliberately **excluded** from the core, and that exclusion
was named as the thing being given up: "this is the feature that made the BCB paper the BCB paper,
and I am dropping it."

Four of those five decisions have since been reversed. The grid survives, as a control.

---

## 1. The instrument is not free (25 Sep, week-1 pilot)

Three measurement faults surfaced before a single headline number existed.

**Checkpoint selection was inverted.** The same weight trajectory scored at `best.pt` gave median
rank 39, rank-1 0.05, and 0 of 20 verbatim; scored at `final.pt`, median rank 1, rank-1 1.00, bits
1.992 -> 0.586, verbatim 0.65. On iid data validation loss bottoms out in two or three epochs, so
"lowest validation loss" selects the **least** memorised epoch. Named as an instrument hazard in
Methods, not fixed as a bug. The reference pipeline selects the same way, which is a plausible cause
of its near-chance low-repetition tiers.

**The two masked scorers disagree.** At 50 epochs the prefix-conditioned scorer put 16x canaries at
2.10-2.25 bits, i.e. *worse than chance*, while the pseudo-likelihood scorer was calibrated at
2.0006. Scorer agreement fell from Spearman 0.96-0.99 to 0.40-0.69. Decision: keep both everywhere,
each with its own per-cell held-out floor check, and flag a failing scorer rather than drop it.

**That decision is the seed of the paper's final claim**, three weeks early and unrecognised at the
time.

---

## 2. "Tokeniser matters" was already known (28 Sep)

Kharitonov, Baroni & Hupkes (arXiv:2110.02782) already show that a larger BPE vocabulary gives more
memorisation, for causal, masked and encoder models, surviving their own parameter control. The
headline was demoted from a finding to a replicated premise.

Two days later the opposite correction landed on the model panel: DNABERT ships **four** pretrained
checkpoints differing only in k, and the Morris capacity arithmetic showed our from-scratch cells sit
about 15x below capacity while deployed models do not. Released models were promoted from stretch to
core.

---

## 3. We had been measuring position, not content (29 Sep)

Every planted copy sat at nucleotide 96 of its host. With offsets drawn at random instead, the same
r=16 canary in a fresh host fell from 0.52 bits / 100% rank-1 / 50% verbatim to far less. Most of
the "repetition" memorisation measured so far was anchored to absolute position through the learned
position table.

Random placement became the default, and the variance decomposition **inverted**: from tokeniser
59.5% / objective 25.7% to objective 57.7% / tokeniser 15.4%, and on the finished grid objective
67.1% / tokeniser 12.0%. The progress summary's headline was upside down.

---

## 4. The venue and the frame changed, not the data (2-4 Oct)

The advisor's judgement, not a measurement: two tracks, the genomic findings to a bioinformatics
venue first, and a utility metric required beside memorisation. The collaborator's direction: not an
"ablation", do not say "architecture was not the variable", say prior work lacks X, Y, Z and we go
deeper. Also, checked line by line, the predecessor's `prefix_attack` is defined and never called,
so its published "extraction" is a ranking result.

---

## 5. Fine tokenisation delays, it does not prevent (9-10 Oct)

At 30 rounds the character cell showed 0% verbatim at every tier on real chromosome-22 haplotypes,
at no utility cost, and that was written up as the paper's concrete recommendation.

**Nine hours later** the same cell run to 150 rounds: round 30 1.757 held-out / 6% verbatim; round 50
3.389 / 68%; round 150 10.209 / 100%. Thirty rounds simply had not reached it. The recommendation
changed from "removes" to "delays", and the stale sentence had to be cut from the introduction.

The objective then took its place as the lead lever, because masked cells removed verbatim
extraction outright where tokenisation only delayed it.

---

## 6. A released model breaks the objective claim (12 Oct)

Nucleotide Transformer v2 250M, masked only, same extraction code: 0% at its own optimum, 20% at
round 30, 28% at round 50 on E. coli; 8% at **0.006 bits** past the optimum on chromosome 22.

First reading: both levers delay rather than prevent, and our own 0% was a statement about the
30-round budget, since those cells stopped with held-out loss still improving.

---

## 7. The rulers had never been separated (12 Oct)

Two faults, both ours. `rank_probe` normalises over all 96 nucleotides of a canary while
`extract_prefix` gives away the first 48, so a low canary surprise could sit beside a hopeless
reconstruction for arithmetic reasons. And **neither shipped protocol performs the decode the model
was trained for**: both mask the entire 8-16-token target at once, against 15% iid masking in
training.

Measuring the conditional the model actually learned -- every other target token at its true value,
one masked -- gave leave-one-out top-1 of 0.96-1.00. The record was essentially present. A
re-masking decoder then recovered 12% where both published protocols read 0%.

And extraction stopped being a property of a checkpoint: 1/2/4/8/16/32 restarts gave 12/16/20/20/24/40%,
monotone, with the non-member control at 0% throughout and a truth-free selection rule matching the
oracle at every budget. **Any extraction number is a lower bound set by the attacker's compute.**

---

## 8. The headline dies, killed by our own attack (13 Oct)

300 rounds, 128 restarts, chromosome 22: r=16 goes 10% -> **95%**, r=4 0% -> 80%, and a canary
inserted **once** 0% -> 95%, with 1.6 wrong nucleotides of 48 and the control at 0%.

"The objective decides whether whole records come back" is dead. What replaced it: measured
memorisation is attack-relative, and the objective and tokeniser change the **cost** of extraction
rather than its possibility.

The mechanism changed with it. Token rarity (corpus counts 287,995 / 6,014 / 400 / 47) explains how
much is **stored**, on the surprise ruler. The number of **joint slots** the target occupies explains
whether what is stored can be **read back**: 8 slots leak, 16 give 0% through a held-out loss of
3.400, 48 give 0% on four released checkpoints. Two mechanisms on two rulers, and the paper must not
let them be read as one.

---

## 9. The controlled backbone was systematically reassuring (13 Oct)

Forced by the user's objection that conclusions measured only on our own 12.9M model are not claims
about models in the world.

Our from-scratch 6-mer cell begins to leak at **+0.351 bits**, past the point where the model is
worse than a uniform predictor. The released NT 250M leaks at **+0.028 bits**, on a model anyone
would ship. A released DNABERT holds a record at leave-one-out 1.00 at +0.015 bits.

**Pretraining decides the utility at which the leak appears.** Reporting either alone misleads: the
from-scratch curve reads as reassuring, the released one as alarming. The controlled grid is the
control; the released checkpoints are the finding. This was the single highest-value intervention in
the project and it came from outside the measurements.

---

## 10. No decoder is right for every vocabulary (14 Oct)

Both decoders on every released cell. Ours wins on fixed-width non-overlapping 6-mers: NT 250M
0% -> 10% at +0.028, 35% -> 70% at +0.440, 25% -> 65% on chromosome 22. Ours **loses** on BPE and on
overlapping k-mers: DNABERT-2 reads 30% standard against 0% ours at +0.008, and 74% against 0% at
+0.482; DNABERT k=6 on chromosome 22 reads 56% standard against 0% ours.

The reason is mechanical. Our decoder climbs from a random nucleotide assignment. On BPE a random
string **re-segments**, so the conditional it climbs is evaluated on a window whose segmentation is
itself garbage; on overlapping k-mers the 48 covering positions are mutually inconsistent. The
published prefix decode builds left to right from real context and never leaves the manifold of
plausible strings, which is why it is stronger exactly where the vocabulary couples neighbouring
positions.

So: **no single decoder measures memorisation correctly across vocabularies.** A paper reporting one
decoder for all models has measured the decoder.

And with each model read by whichever decoder suits it, the privacy result overtook the
methodological one: **every released masked checkpoint tested reproduces planted records verbatim at
a utility cost a practitioner would accept**, the cheapest at +0.008 bits.

---

## Where it stands, 14 Oct 2026

**Released-model evidence (statable as claims about models in the world).**

| checkpoint | vocabulary | utility cost | verbatim recovery |
|---|---|---|---|
| DNABERT-2 117M | BPE | **+0.008** | 30% |
| NT v2 250M | non-overlapping 6-mer | +0.028 | 10% |
| DNABERT k=3 86M, chr22 | overlapping | +0.110 | 10% |
| DNABERT k=6 86M, chr22 | overlapping | +0.180 | 56% |
| NT v2 250M, chr22 | non-overlapping 6-mer | +0.256 | 65%, and 10% at a single copy |
| NT v2 250M | non-overlapping 6-mer | +0.440 | 70% |
| DNABERT-2 117M | BPE | +0.482 | 74% |

**Controlled-backbone only (must be framed, not generalised).** The variance decomposition, the
matched-held-out-loss tokeniser ordering, the token-rarity mechanism, the spaced-k-mer control, the
equal-supervised-tokens control, the twelve-point utility curve, and the single-copy 95%, which
occurs only at a held-out loss of 2.866 against a 1.675 optimum -- a model worse than a uniform
predictor.

**Still true and still useful.** Early stopping at the held-out optimum removes the stored record,
on released weights, with a margin of **0.028 bits**. Single-copy *recognition* is universal where
reproduction is not, so membership inference flags records that no decoder reproduces.

---

## What the current outline still says that is dead

Sections 00 (abstract), 01 (introduction, contribution 2), 04 (Figure 1 caption), 08 (mitigation,
both paragraphs and the mitigation table) and appendix A8 all assert that every masked cell
reproduces 0% of planted records, "including under the edge-conditioned infilling protocol that is
designed to break it". That is false three ways over: by our own backbone at 128 restarts, by NT
under the standard protocol, and by DNABERT-2 under its own masked objective -- the last of which has
been in our logs since 8 Oct and was never written up.

Unaffected and writable as they stand: the whole of the early-stopping section, the whole of the
rare-allele / membership-inference section, the DNABERT k-ordering on three genomes, the chr21
replication, the four-draw canary-split methodology, and the Evo planting-artefact reconciliation.

---

## The pattern, which is worth more than any single result

**Every reversal came from extending a budget or changing an instrument. Not one came from a new
model.** 150 rounds instead of 30; 128 restarts instead of 1; a decoder matched to the training
conditional instead of the inherited one; random placement instead of fixed; `final.pt` instead of
`best.pt`.

**Three claims were reversed within 24 hours of being made** (sections 3.20 -> 3.24, 3.39 -> 3.41,
3.50 -> 3.53). In each case the first version was the one that would have gone into a draft.

**The from-scratch backbone was reassuring in a way that was not true of released weights**, in the
same direction every time. A controlled model is the right instrument for isolating a variable and
the wrong one for estimating a risk.

**The instrument became the result.** The week-1 decision to keep two disagreeing scorers rather than
pick one is, three weeks later, the paper's contribution.
