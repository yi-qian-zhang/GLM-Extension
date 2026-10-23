# Tokenizer × Objective Ablation for GLM Memorization — Progress Summary

**Spencer · 29 September 2026** 

## Idea

**The problem.** The BCB'26 paper shows that four GLMs memorize to different degrees. But those four models differ in architecture, tokenizer, pretraining objective and size all at once, so the difference cannot be attributed to any one of them. The paper's Discussion says a controlled ablation is needed, and that is extension #2 in the extension notes.

**What I do.** I train one small Transformer from scratch, keep everything else fixed, and change only one thing at a time:

- the **tokenizer**: single nucleotide (char), 3-mer, or 6-mer (BPE planned);
- the **pretraining objective**: causal (next-token) or masked, at several mask rates.

Then I plant canaries and measure how much each model memorizes.

**The question.** Which design choice actually drives memorization in a GLM, and by how much?

**Why it matters.** If the tokenizer and the objective explain most of the difference, then a gap between two GLMs should not be read as "architecture A is safer than B". The privacy risk would instead depend on choices a model builder can control directly.

## Setup

- **Backbone:** one fixed Transformer (12.9M parameters; d=512, 4 layers).
- **Data:** synthetic iid DNA, so the chance floor is exactly 2.000 bits/nt. Canaries are planted at 0 / 1 / 4 / 16 repetitions.
- **Metrics:** all per nucleotide. Canary bits/nt, rank-1 against a 500-sequence random pool, and exact 48-nt prefix extraction.
- **Deliverable:** a variance decomposition of memorization into tokenizer, objective, interaction and seed.

## Results so far (pilot scale, 2 seeds each)

1. **The tokenizer dominates.**

   | source of variance in r=16 canary memorization | share |
   |---|---|
   | tokenizer | **59.5%** |
   | objective | 25.7% |
   | interaction | 14.0% |
   | seed | 0.8% |

   Within masked models, the tokenizer explains 92.7%.

2. **Coarser tokens memorize sooner *and* more.**
   - At matched held-out loss, i.e. equal generalization cost, 6-mer ≫ 3-mer > char.
   - Example: r=1 canary bits/nt at a held-out floor of 2.20 are 0.61 / 1.52 / 1.77.
   - So early stopping does not remove the effect.

3. **It is not a parameter-count effect.**
   - Shrinking the body to equalize total parameters changes nothing.
   - A factorized embedding changes the 6-mer magnitude a lot, even at full rank, where the function class is identical. So the magnitude is implementation-sensitive; the ordering is not.

4. **Sequence length is not the mechanism.**
   - Kharitonov et al. (2021) showed larger BPE vocabularies memorize more and conjectured that shorter sequences are the cause.
   - I stretched k-mer sequences to char length with unscored filler tokens. Memorization stayed at the k-mer level.
   - The joint-prediction unit (k nucleotides per softmax), not length, drives the effect.

5. **Above model capacity the effect becomes qualitative.**
   - With 20× data (more than ~3.6 bits/param), char and 3-mer memorize nothing, even canaries seen 480 times.
   - 6-mer still recognizes every member canary and extracts every 16× canary verbatim.

6. **Canary placement matters (new).**
   - With every copy at a fixed position, a 16× canary moved into a new context *at the same position* is still recognized (char 100%, 6-mer 100%).
   - With copies at random positions (realistic for duplicated genomic sequence), recognition in a new context at a new position largely disappears for all tokenizers. For char, 16 repetitions then equal 1.
   - For k-mer models, what transfers depends on whether the tokenization phase matches.
   - Whole-example memorization and the tokenizer ordering are unaffected.
   - Implication: positional encoding (absolute vs relative) becomes a genuine design variable.

7. **Instrument checks pass.** Untrained models give uniform ranks, a blind baseline is at chance, non-member false positives are ≤ 5%, and the seed variance is < 1%.

## Positioning

"Larger vocabulary → more memorization" is known from NLP (Kharitonov et al. 2021), so I treat it as a replicated premise rather than the headline. What I think is new:

- (i) the joint tokenizer × objective decomposition;
- (ii) separating "more" from "sooner" at matched held-out loss;
- (iii) the standard parameter-count control changes memorization by itself;
- (iv) a direct test that refutes the sequence-length explanation;
- (v) the placement / positional-encoding dependence;
- (vi) a calibrated per-nucleotide instrument in the genomic setting.

## Next

1. **External validity on real models:** the DNABERT 3/4/5/6-mer family. It is the same architecture, data and objective, and differs only in k; all four are already downloaded and load-tested. I will fine-tune each with planted canaries and score them through the native MLM head, predicting 3 < 4 < 5 < 6.
2. **Relative vs absolute position encoding** on my backbone.
3. **Real genome** (E. coli).
4. **Masked-model trajectories.**
5. **More canaries per tier** (100).
