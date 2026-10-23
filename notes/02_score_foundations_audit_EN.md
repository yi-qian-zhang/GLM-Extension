# The Sequence Score: A Foundations Audit

**Scope.** This answers, in full: *where does the model-assigned score for a DNA sequence come from, which paper introduced it, why is it scientifically valid, and how do we confirm its truth and accuracy* — given that all three attack vectors in Nemecek et al. (BCB '26) are computed from it. Every citation below carries a verification status. Where a fact-check pass corrected an earlier claim, the corrected version is used and the correction is noted inline.

---

## BOTTOM LINE

1. **The score is mathematically impeccable *as a quantity*.** It is a log-probability under a distribution that the model constructs, not merely estimates. Its validity rests on a two-hypothesis theorem, an exact (not asymptotic) identity linking training to KL divergence, and a uniqueness theorem (Bernardo, via Gneiting & Raftery 2007) saying that log-probability is the *only* local proper scoring rule up to positive affine rescaling. There is no better choice available; there is provably no other choice.

2. **The score is not automatically a membership signal.** Every rigorous guarantee is about *expectations under a fixed distribution*. Converting it into a per-example membership decision requires either entropy-matched sets or per-example calibration. Neither is present in BCB '26.

3. **The 4.0 floor is a genuine impossibility proof — but only under conditions the DNABERT-2 path violates, and it does *not* transfer to BPE-token-level pseudo-log-likelihood.** This was the open question the verification pass was asked to resolve. It is resolved in §5.5 with a definite answer, and the answer changes what you can assert about 2.69.

4. **Three of the paper's constructs are misapplications, not implementation bugs:** its "extraction" metric is neither of Carlini's extraction definitions; its exposure formula mixes two incompatible index sets, giving a constant +118.034-bit inflation; and its "LiRA" is Yeom et al.'s Adversary 1 (the LOSS attack), the attack LiRA exists to replace.

---

# 1. THE SCORE ITSELF

Fix a discrete alphabet. Let $\mathcal{V}$ be the token vocabulary, $x = (x_1,\dots,x_T) \in \mathcal{V}^T$ a token sequence, $q_\theta$ the model. For nucleotide-level models $\mathcal{V} = \{A,C,G,T\}$ and tokens = nucleotides.

## 1.1 The definition

$$\log q_\theta(x) \;=\; \sum_{i=1}^{T} \log q_\theta(x_i \mid x_{<i}), \qquad q_\theta(\cdot\mid x_{<i}) = \mathrm{softmax}\big(f_\theta(x_{<i})\big)$$

Per-token cross-entropy and perplexity:

$$\mathcal{H}_{\text{nats}}(x) = -\frac{1}{T}\sum_{i=1}^{T} \ln q_\theta(x_i \mid x_{<i}), \qquad \mathrm{PPL}_{\text{tok}}(x) = \exp\!\big(\mathcal{H}_{\text{nats}}\big) = 2^{\mathcal{H}_{\text{bits}}} = q_\theta(x)^{-1/T}$$

The last form is the interpretation to hold onto: **perplexity is the reciprocal of the geometric mean of the probabilities the model assigned to the symbols that actually occurred** — an "effective branching factor," the size of the uniform alphabet that would have been equally hard to predict.

## 1.2 The chain rule: what is identity, and what is construction

This distinction is the single most important thing in the document, and it is where the DNABERT-2 bug lives.

**(a) The identity.** For *any* joint pmf $Q$ on $\mathcal{V}^T$:

$$Q(x_1,\dots,x_T) = \prod_{i=1}^{T} Q(x_i \mid x_{<i})$$

This is an identity of probability theory, not a modeling assumption. It is the definition of conditional probability, $Q(x_i\mid x_{<i}) := Q(x_{\le i})/Q(x_{<i})$, applied $T$ times and telescoped. It requires only $Q(x_{<i})>0$. It holds for **any** variable ordering. It assumes no Markov property, no independence, no finite context. Its information-theoretic image is the chain rule for entropy, Cover & Thomas Thm 2.5.1.

**An autoregressive LM does not use this identity. It runs it backwards.**

**(b) The construction.** An AR LM does not start from a joint and derive conditionals. It *emits* a family of conditionals and *defines* a joint as their product. That this product is a genuine probability distribution over $\mathcal{V}^T$ is a **theorem with exactly two hypotheses**:

- **(N) Normalization.** $\sum_{v\in\mathcal{V}} q_\theta(v\mid x_{<i}) = 1$ for each $i$. Softmax gives this by construction.
- **(C) Causality.** The $i$-th head is a function of $x_{<i}$ only — it must not depend on $x_i$ or $x_{>i}$.

*Proof (induction on $T$).*
$$\sum_{x\in\mathcal{V}^T}\prod_{i=1}^{T} q_\theta(x_i\mid x_{<i}) = \sum_{x_{<T}}\Big[\prod_{i<T} q_\theta(x_i\mid x_{<i})\Big]\sum_{x_T} q_\theta(x_T\mid x_{<T}) = \sum_{x_{<T}}\prod_{i<T}q_\theta(x_i\mid x_{<i}) = \dots = 1. \square$$

The inner sum collapses to 1 by **(N)**; the collapse is legal *only* because the bracketed factor does not depend on $x_T$, which is **(C)**.

**This proof is the entire load-bearing structure of the paper's scoring.** Drop (C) — let the $i$-th head see the whole sequence — and each factor $q_\theta(x_i \mid x_{1..T})$ is still normalized over $v$ for fixed context, but the inner sum no longer factors out. The product is not a distribution over sequences. For a leaky scorer placing geometric-mean probability $\varepsilon$ on the observed base, total mass is $\sum_x \prod_i q(x_i \mid x) = (4\varepsilon)^T$, which at the implied $\varepsilon = 1/2.69 = 0.372$ is $1.487^T$ — astronomically above 1. An object whose total mass exceeds 1 is subject to no information-theoretic lower bound at all.

## 1.3 Normalization units — the tokenizer correction

Let a sequence have $L$ nucleotides tokenized into $T$ tokens; define $k := L/T$. The number $\log q_\theta(x)$ is the same under either normalization; only the divisor changes:

$$\boxed{\;\mathrm{PPL}_{\text{nt}} = \mathrm{PPL}_{\text{tok}}^{\,1/k}, \qquad \mathrm{PPL}_{\text{tok}} = \mathrm{PPL}_{\text{nt}}^{\,k}, \qquad H_{\text{nt}} = H_{\text{tok}}/k \;\text{(bits)}\;}$$

*Verification:* uniform DNA with $k=5$ gives $\mathrm{PPL}_{\text{tok}} = 4^5 = 1024$, exactly the number of distinct 5-mers. Round-trip verified numerically to 12 decimals for $k \in \{1, 3, 4, 5, 5.6, 6\}$. This reduces to the Pile's $\mathrm{BPB} = (L_T/L_B)\,\ell/\ln 2$ (Gao et al. 2021, §3.1, verified verbatim).

**Aggregate first, normalize last.** For a corpus:
$$\mathrm{PPL}_{\text{nt}} = \exp\!\Big(-\tfrac{\sum_j \log q(x^{(j)})}{\sum_j L_j}\Big), \qquad \bar k = \frac{\sum_j L_j}{\sum_j T_j}$$
A mean of per-sequence $k$, or a mean of per-sequence perplexities, is a different and wrong number.

> **Correction applied.** An earlier report stated that "by Jensen, the mean of per-sequence perplexities is $\ge$ the corpus perplexity." **This holds only at equal lengths.** Counterexample: $(H_1,L_1)=(0,1)$, $(H_2,L_2)=(10,1000)$ gives corpus $\mathrm{PPL} = 2^{9.99} = 1017$ but mean-of-per-sequence $= 512.5$ — the inequality reverses. At fixed 256 nt it is safe; do not state it in general.

**Tokenization ambiguity.** A subword model defines a distribution over *token* sequences. The induced distribution over nucleotide strings is $P(s) = \sum_{t:\,\mathrm{detok}(t)=s} q(t) \ge q(t_{\text{canon}}(s))$. Standard practice scores only the canonical tokenization, so the reported log-likelihood is a **lower bound** on the true string log-likelihood and the derived $\mathrm{PPL}_{\text{nt}}$ is an **upper bound** on the true one. Cao & Rimell (2021) measure the gap: negligible in-domain, 0.9–1.9% out-of-domain *(figure not re-verified)*. Direction matters: marginalization can only *lower* perplexity, so it can never rescue a sub-floor reading — and sub-floor remains impossible for causal models because $P(s)$ is itself normalized over strings.

## 1.4 What a trained AR LM guarantees, and what it does not

**Guarantees (structural):**
- $q_\theta$ is a valid probability distribution over $\mathcal{V}^T$.
- $\log q_\theta(x)$ is a genuine log-probability, on an absolute scale, comparable across sequences of equal length under the same tokenizer.

**Guarantees nothing about:**
- $q_\theta$ being close to the data distribution.
- Calibration on any *particular* sequence.
- $q_\theta(x)$ being larger for training data than for held-out data — for any *individual* $x$.

Those last three are empirical, not structural, and the third is the one the entire privacy evaluation leans on.

## 1.5 The taxonomy, explicitly

| Claim | Status |
|---|---|
| $\log Q(x) = \sum_i \log Q(x_i\mid x_{<i})$ | **Identity** of probability theory. Assumes nothing. |
| $\prod_i q_\theta(x_i\mid x_{<i})$ is a distribution over $\mathcal{V}^T$ | **Theorem**, hypotheses (N) + (C). Two-line induction. |
| $\mathbb{E}_p[-\log q] = H(p) + D(p\Vert q) \ge H(p)$ | **Theorem** (Gibbs / Cover & Thomas 2.6.3). Exact, non-asymptotic. |
| Log score is strictly proper, and uniquely so among local rules | **Theorem** (G&R 2007 §4.1; Bernardo 1979 via G&R p. 366). |
| Minimizing empirical CE $\equiv$ minimizing $D(\hat P\Vert q_\theta)$ | **Exact identity**, sequence-level cross-entropy decomposition. |
| Left-to-right factorization is the right ordering for DNA | **Modeling assumption.** Nothing licenses comparing L→R and R→L joints. |
| Finite context window suffices | **Modeling assumption.** |
| Trained models assign higher likelihood to training data | **Empirical tendency**, not a theorem. See §4.1. |
| Report per-nucleotide, not per-token | **Empirical convention** — but a mandatory one for cross-model tables. |
| Score only the canonical tokenization | **Empirical convention** (a bound, with known direction). |
| Exclude padding from the loss | **Engineering convention.** No peer-reviewed source names it as a pathology; see §8. |

---

# 2. THE CITATIONAL LINEAGE

Verification method: arXiv API (`export.arxiv.org/api/query`) for all arXiv IDs; Crossref REST (`api.crossref.org/works`) for all DOIs; ACL Anthology / PMLR / USENIX / NeurIPS / ICLR proceedings pages for venue and pagination; direct grep against full-text extractions for every quoted passage.

## 2.1 The score and its information theory

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| Chain rule (identity) | $\log Q(x)=\sum_i \log Q(x_i\vert x_{<i})$; $H(X_1..X_n)=\sum_i H(X_i\vert X_{<i})$ | Cover & Thomas, *Elements of Information Theory* 2e, Thm 2.5.1 (p. 22). DOI [10.1002/047174882X](https://doi.org/10.1002/047174882X) | **VERIFIED verbatim** |
| AR construction validity | (N)+(C) $\Rightarrow$ $\sum_{x}\prod_i q(x_i\vert x_{<i})=1$ | No single primary source — elementary induction. Neural instantiation: Bengio, Ducharme, Vincent, **Jauvin**, *JMLR* 3:1137–1155 (2003) | Derivation sound; Bengio record **VERIFIED** (note: fourth author is **Jauvin**, not the widely propagated "Janvin") |
| Cross-entropy $=$ entropy $+$ KL | $\mathbb{E}_p[-\log q]=H(p)+D(p\Vert q)$; $D\ge0$ iff $p=q$ | Cover & Thomas Thm 2.6.3, eq. (2.82), p. 28 | **VERIFIED verbatim** ("with equality if and only if $p(x)=q(x)$ for all $x$") |
| Source coding bound | $\mathbb{E}[l]\ge H_D(X)$; wrong code: $H(p)+D(p\Vert q)\le\mathbb{E}_p l<H(p)+D(p\Vert q)+1$ | C&T Thm 5.3.1 eq. (5.21); Thm 5.4.3 eq. (5.42) | **VERIFIED verbatim** |
| MLE $\equiv$ min KL | $-\tfrac{1}{\vert D\vert}\sum_{x\in D}\log q_\theta(x)=H(\hat P)+D(\hat P\Vert q_\theta)$ | Elementary cross-entropy decomposition | **Sound.** See correction note below. |
| Conditional next-symbol LM; entropy | $n$-gram approximations to English; $H$ | Shannon, *BSTJ* 27(3):379–423 (1948), §3, §6, §7. DOI [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x) | **VERIFIED verbatim** (§3 heading "THE SERIES OF APPROXIMATIONS TO ENGLISH") |
| Noiseless-channel converse | Thm 9: *"It is not possible to transmit at an average rate greater than $C/H$."* | Shannon 1948 §9; supporting Thms 3 (AEP), 4 | **VERIFIED verbatim** |
| SMB / ergodic AEP | $-\tfrac1n\log p(X_0..X_{n-1})\to H$ a.s. | C&T Thm 16.8.1 | **VERIFIED** |
| Entropy of printed English | — | Shannon, *BSTJ* 30(1):50–64 (1951). DOI [10.1002/j.1538-7305.1951.tb01366.x](https://doi.org/10.1002/j.1538-7305.1951.tb01366.x) | **VERIFIED (metadata only)** |

> **Correction applied.** An earlier report justified the MLE↔KL identity by citing **Cover & Thomas Thm 11.1.2** (method of types, $Q^n(x)=2^{-n(H(P_x)+D(P_x\Vert Q))}$). That theorem **requires $Q$ to be memoryless**, which an AR LM emphatically is not. The conclusion is correct via the elementary *sequence-level* decomposition $\sum_x \hat P(x)(-\log q_\theta(x)) = H(\hat P)+D(\hat P\Vert q_\theta)$, which needs no theorem. Use that justification; drop the citation.

## 2.2 Proper scoring rules

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| Propriety | $S(Q,Q)\ge S(P,Q)$ for all $P,Q\in\mathcal{P}$; strict iff equality only at $P=Q$, *"thereby encouraging honest quotes by the forecaster"* | Gneiting & Raftery, *JASA* 102(477):359–378 (2007), eq. (1), p. 360. DOI [10.1198/016214506000001437](https://doi.org/10.1198/016214506000001437) | **VERIFIED verbatim** |
| Log score strictly proper | $\mathrm{LogS}(p,\omega)=\log p(\omega)$; *"strictly proper relative to the class $\mathcal{L}^1$…"*; divergence is KL | G&R eq. (19), §4.1, p. 366 | **VERIFIED verbatim** |
| Categorical case | $G(p)=\sum_j p_j\log p_j$; Bregman divergence $=\sum_j q_j\log(q_j/p_j)$ | G&R Example 3, p. 363 | **VERIFIED verbatim** |
| Propriety machinery | Proper iff $G(P)=S(P,P)$ convex and $S(P,\cdot)$ a subtangent; strictly proper iff $G$ strictly convex | G&R Theorem 1, p. 361 | **VERIFIED** |
| **Locality uniqueness** | *"every proper local scoring rule is equivalent to the logarithmic score"*, i.e. $c\log p(\omega)+h(\omega)$, $c>0$; and *"the linear score, LinS$(p,\omega)=p(\omega)$, is not a proper scoring rule, despite its intuitive appeal."* | Bernardo (1979), reported in G&R p. 366 | **VERIFIED verbatim in G&R** |
| Ancestry | *"This scoring rule dates back at least to Good (1952)"*; also Brier (1950) | Good, *JRSS-B* 14(1):107–114, DOI [10.1111/j.2517-6161.1952.tb00104.x](https://doi.org/10.1111/j.2517-6161.1952.tb00104.x); Brier, *Mon. Wea. Rev.* 78(1):1–3 | **VERIFIED** (both DOIs resolve) |

## 2.3 Perplexity

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| The **name** | Perplexity, whose log is entropy, is a better measure of "equivalent choice" than average branching factor | Jelinek, Mercer, Bahl, Baker, *JASA* **62(S1):S63** (1977). **DOI [10.1121/1.2016299](https://doi.org/10.1121/1.2016299)** | **VERIFIED — record, volume/issue/page, and DOI all resolve.** ⚠️ This is a **one-paragraph meeting abstract** (94th ASA Meeting, Miami Beach, Dec 1977), not a full paper. Typeset abstract body unread (AIP returns HTTP 403). |
| Formal definition in a full paper | — | Bahl, Jelinek, Mercer, *IEEE TPAMI* **5(2):179–190** (1983). DOI [10.1109/TPAMI.1983.4767370](https://doi.org/10.1109/TPAMI.1983.4767370) | **METADATA VERIFIED; equation in body NOT read.** |
| Operational definition | $\mathrm{PPL}(X)=\exp\{-\tfrac1t\sum_i \log p_\theta(x_i\vert x_{<i})\}$ | HuggingFace reference docs, https://huggingface.co/docs/transformers/perplexity; Carlini et al. 2021 | **VERIFIED verbatim in both** |
| Tokenizer-invariant unit | $\mathrm{BPB}=(L_T/L_B)\cdot\ell/\ln 2$, chosen for *"invariance to different tokenization schemes"* | Gao et al., *The Pile*, arXiv:2101.00027, §3.1 | **VERIFIED verbatim** |
| Cross-segmentation incomparability | Per-token PPL not comparable across segmentations | Cotterell, Mielke, Eisner, Roark, *NAACL-HLT 2018*, 536–541, DOI 10.18653/v1/N18-2085; Mielke et al., *ACL 2019*, arXiv:1906.04726 | **VERIFIED** |
| Marginal likelihood over tokenizations | $P(s)=\sum_{t:\mathrm{detok}(t)=s}q(t)$ | Cao & Rimell, *EMNLP 2021*, 2104–2114, DOI 10.18653/v1/2021.emnlp-main.161 | **VERIFIED (paper)**; the 0.9–1.9% figure not re-checked |
| Tightness of variable-length LMs | — | Du, Torroba Hennigen, Pimentel, Meister, Eisner, Cotterell, *ACL 2023*, **pp. 9744–9770**, arXiv:2212.10502 | **VERIFIED — previously flagged unverified; flag closed.** Moot at fixed length. |

> **Correction applied.** An earlier report instructed: *"Do not cite a DOI for [Jelinek 1977] unless you retrieve it yourself."* **That instruction is wrong.** DOI 10.1121/1.2016299 is real and resolves via Crossref to the exact volume/issue/page. The meeting-abstract caveat stands and should be stated whenever it is cited.

## 2.4 Memorization, canaries, extraction

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| Log-perplexity as a memorization primitive, with its own warning | $\mathrm{Px}_\theta(x_1..x_n)=-\log_2\Pr(x_1..x_n\vert f_\theta)$; *"the concrete log-perplexity value [is] ill suited as a direct measure of memorization"* | Carlini, Liu, Erlingsson, Kos, Song, *The Secret Sharer*, **USENIX Security '19, pp. 267–284**, arXiv:1802.08232 — Definition 1 | **VERIFIED verbatim** |
| Rank | $\mathbf{rank}_\theta(s[r])=\vert\{r'\in\mathcal{R}:\mathrm{Px}_\theta(s[r'])\le\mathrm{Px}_\theta(s[r])\}\vert$ — index set is **the full $\mathcal{R}$** | SS19 Definition 2 | **VERIFIED verbatim** |
| Guessing entropy | $E(s[r])=\tfrac12\vert\mathcal{R}\vert$ a priori; $=\mathbf{rank}$ with model access | SS19 Definition 3 | **VERIFIED verbatim** |
| **Exposure** | $\mathbf{exposure}_\theta(s[r])=\log_2\vert\mathcal{R}\vert-\log_2\mathbf{rank}_\theta(s[r])$; *"the median exposure is 1"* | SS19 Definition 4 | **VERIFIED verbatim** |
| Sampling estimator | $\approx\log_2\vert\mathcal{S}\vert-\log_2\mathbf{rank}_{\mathcal{S}}$ — **normalizer becomes $\log_2\vert\mathcal{S}\vert$** | SS19 §4.3, Theorem 1 | **VERIFIED verbatim** |
| Extrapolation estimator | $\approx-\log_2\int_0^{\mathrm{Px}(s[r])}\rho(x)dx$, skew-normal $\rho$; validated against all $10^9$ candidates, KS test $p>0.1$; *"this estimated exposure has no upper bound"* | SS19 §4.3 | **VERIFIED verbatim** |
| Exposure with $n$ **references**; random-guessing baseline | $\mathrm{Exposure}=\log_2(n)-\log_2\mathrm{Rank}$; no-memorization rank $=1+n/2$, exposure $\approx1$; mean $\approx1/\ln2\approx1.44$; median $=1$; 75th pct $=2$ | Jagielski, *A Note On Interpreting Canary Exposure*, arXiv:2306.00133 | **VERIFIED verbatim.** Strongest single citation for the exposure objection. |
| $\varepsilon$ lower bound | $\varepsilon\ge\ln(2)(\mathrm{Exposure}(c_{\text{median}})-1)$; divide by duplicate count via group privacy | Jagielski 2023 | **VERIFIED** |
| Enumerable-$\mathcal{R}$ practice | *"We limit ourselves to 6-digit secrets which allows us to efficiently enumerate over all possible secret values"* | Tramèr, Shokri, San Joaquin, Le, Jagielski, Hong, Carlini, *Truth Serum*, **CCS 2022**, arXiv:2204.00032, §6 | **VERIFIED verbatim** |
| Calibration raises exposure | 3.1 bits uncalibrated $\to$ 7.1 (2 shadow models, 16×) $\to$ 7.4; recovery in $<100$ guesses **0.1% $\to$ 10% (100×)** | Truth Serum §6.1 | **VERIFIED verbatim** |
| Extraction (argmax) | $s\leftarrow\arg\max_{s':\vert s'\vert=N} f_\theta(s'\vert c)$; $k$-eidetic memorization | Carlini, Tramèr, Wallace, et al., **USENIX Security '21, pp. 2633–2650**, arXiv:2012.07805, Defs 1–2 | **VERIFIED verbatim** |
| Raw perplexity is a **weak** extraction selector | 9% (top-$n$) and 3% (temperature) memorized vs **67%** for zlib-calibrated | C21 | **VERIFIED verbatim** |
| **$k$-extractability** | $s$ extractable with $k$ tokens of context if $\exists p$, $\vert p\vert=k$, with $[p\Vert s]$ in training data and $f$ emits $s$ from $p$ **under greedy decoding** | Carlini, Ippolito, Jagielski, Lee, Tramèr, Zhang, **ICLR 2023**, arXiv:2202.07646, Definition 3.1 | **VERIFIED verbatim** |
| Scaling laws | $M=a+b\log x$; model scale $R^2=99.8\%$, **+19 pp per decade of params**; context 33% @ 50 tokens $\to$ 65% @ 450; 2–5× more for larger models; GPT-J memorizes $\ge$1% of the Pile | C23 §1, §4 | **VERIFIED verbatim** |
| **Masked-model exception** | T5 requires a *different* definition (perfect masked-task solution); T5-XL 3B **3.5%** vs GPT-Neo 2.7B **53.6%**; duplication relationship is **non-monotonic** (159–196× memorized $<5.1\%$ vs 138–158× $\ge6.2\%$, both at 99.7% conf.) | C23 §5 | **VERIFIED verbatim** |

> **Correction applied.** C23 **does** reproduce the *model-scale* trend for T5 (*"while a scaling trend does hold here as well"*). It is specifically the **duplication** relationship that is non-monotonic for masked models. Do not paraphrase this as "scaling laws don't hold for masked LMs."

## 2.5 Membership inference

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| Membership experiment; $b=0$ means **member** | — | Yeom, Giacomelli, Fredrikson, Jha, **IEEE CSF 2018, pp. 268–282**, DOI [10.1109/CSF.2018.00027](https://doi.org/10.1109/CSF.2018.00027), arXiv:1709.01604 | **VERIFIED verbatim** |
| Membership advantage | $\mathrm{Adv}^M=2\Pr[\mathrm{Exp}=1]-1=\Pr[A{=}0\vert b{=}0]-\Pr[A{=}0\vert b{=}1]=\mathrm{TPR}-\mathrm{FPR}$ (Youden's $J$, balanced prior) | Yeom Definition 4 | **VERIFIED verbatim** |
| Generalization error | $R_{\text{gen}}=\mathbb{E}_{z\sim D}[\ell]-\mathbb{E}_{z\sim S}[\ell]$ | Yeom Definition 3 | **VERIFIED verbatim** |
| **The licence for loss-as-membership-score** | Adversary 1 (bounded loss $B$, output non-member w.p. $\ell/B$): $\mathrm{Adv}^M=R_{\text{gen}}/B$ — an **equality** | Yeom Theorem 2 | **VERIFIED verbatim** |
| DP upper bound | $\mathrm{Adv}^M\le e^\varepsilon-1$ | Yeom Theorem 1 | **VERIFIED** |
| Overfitting is **not necessary** | ARO-stable construction with advantage $\approx1$ and no generalization gap | Yeom Theorem 4 | **VERIFIED verbatim** |
| Shadow models | Train $k$ shadows with known membership labels; supervised attack classifier on output vectors | Shokri, Stronati, Song, Shmatikov, **IEEE S&P 2017, pp. 3–18**, DOI 10.1109/SP.2017.41 | **VERIFIED** |
| Bayes-optimal MI uses only the loss, with a **per-example** threshold $\tau(x,y)$ | — | **Sablayrolles, Douze, Schmid, Ollivier, Jégou**, *ICML 2019*, **PMLR 97:5558–5567** | **VERIFIED** (⚠️ published author order differs from arXiv's) |
| Difficulty calibration | $s_{\text{cal}}=s(h,(x,y))-\mathbb{E}_{g\leftarrow A(D_{\text{shadow}})}[s(g,(x,y))]$ | Watson, Guo, Cormode, Sablayrolles, *ICLR 2022*, arXiv:2111.08440 | **VERIFIED**; CIFAR-10 0.663→0.676 figure not re-checked |
| **LiRA** | $\Lambda=p(f\vert Q_{\text{in}}(x,y))/p(f\vert Q_{\text{out}}(x,y))$; logit rescale $\phi(p)=\log(p/(1-p))$; report **TPR@low FPR** + log–log ROC | Carlini, Chien, Nasr, Song, Terzis, Tramèr, **IEEE S&P 2022, pp. 1897–1914**, DOI 10.1109/SP46214.2022.9833649, arXiv:2112.03570 | **METADATA VERIFIED**; the 59.5%-vs-53.5% inversion and logit-rescaling details **NOT** re-read from the PDF |
| **Bounded-prior membership privacy** | $\Pr_P[t\in T\mid A(T)=S]\le e^\varepsilon\Pr_P[t\in T]$ for every prior $P$ in a family $\mathcal{D}$; bounded relaxation restricts to $a\le\Pr[t\in T]\le b$ | **Li, Qardaji, Su, Wu, Yang**, *Membership Privacy: A Unifying Framework*, **CCS 2013, pp. 889–900**, DOI 10.1145/2508859.2516686 — and **Tramèr, Huang, Hubaux, Ayday**, **CCS 2015, pp. 1286–1297**, DOI 10.1145/2810103.2813610 | **PAPERS VERIFIED; formal $\varepsilon/\delta$ statement NOT retrieved.** ⚠️ **This is NOT in Yeom et al.** — full-text search confirms the only "bounded" in Yeom is the bounded *loss* $B$. |

> **Two corrections applied.** (1) The Li et al. author list is **Ninghui Li, Wahbeh Qardaji, Dong Su, Yi Wu, Weining Yang**. "Jianneng Cao" is not an author of this paper. (2) Cite Yeom et al. as **CSF 2018**; the arXiv comments field says "IEEE Symposium on Security and Privacy, 2017," and that metadata is wrong.

## 2.6 The skeptical literature

| Claim | Source | Verified? |
|---|---|---|
| MIAs *"barely outperform random guessing"* across Pythia 160M–12B; apparent success attributed to *"a distribution shift, such as when members and non-members are drawn from the seemingly identical domain but with different temporal ranges"* | Duan, Suri, Mireshghallah, Min, Shi, Zettlemoyer, Tsvetkov, Choi, Evans, Hajishirzi, **COLM 2024**, arXiv:2402.07841 | **VERIFIED verbatim** |
| **Blind baselines beat published MIAs on all 8 evaluation datasets** | Das, Zhang, Tramèr, arXiv:2406.16201 (DATA-FM @ ICLR 2025; IEEE DLSP 2025) | **VERIFIED — every table number** |
| *"most MIA methods perform no better than random guessing when discriminating between members and non-members from the same distribution"*; dataset-level inference as the fix | Maini, Jia, Papernot, Dziedzic, **NeurIPS 2024**, arXiv:2406.06443 | **VERIFIED** |
| Post-hoc splits are the root cause; four fixes (randomized splits, injected randomized sequences, randomized fine-tuning, post-hoc controls) | Meeus, Shilov, Jain, Faysse, Rei, de Montjoye, **SaTML 2025**, arXiv:2406.17975 | **VERIFIED** |
| The null *"model was not trained on this data"* is **unsamplable**; the two sound escapes are **extraction attacks** and **membership inference on planted canaries** | Zhang, Das, Kamath, Tramèr, **SaTML 2025**, arXiv:2409.19798 | **VERIFIED** |
| Genuine LiRA at scale: ceiling **AUC < 0.7**; many individual decisions *"statistically indistinguishable from a coin flip"* | Hayes, Shumailov, Choquette-Choo, Jagielski, Kaissis, Nasr, et al., **NeurIPS 2025**, arXiv:2505.18773 | **VERIFIED** |
| Shift-free checkpoint-ordering testbed; blind BoW AUC 0.505; LOSS 0.506–0.513; Min-K% 0.489–0.502; zlib 0.499–0.500; MoPe 0.487–0.504; ReCaLL 0.487–0.493 | Wang, Wang, Li, Neel, *CheckMIABench*, arXiv:2606.17464 | **VERIFIED** ⚠️ significance claim is scoped **70m–2.8b**, not the full 70M–7B sweep; its WikiMIA blind figure is TPR 94.7% **@ 55% FPR** — do not conflate with Das et al.'s TPR@**5%**FPR = 94.7% |
| Under realistic conditions MIAs are weak privacy threats; using them as *the* privacy metric overestimates risk | Jebreel, Sánchez, Domingo-Ferrer, **ESORICS 2026**, arXiv:2603.22987 | **VERIFIED** |
| Min-K% Prob | Shi et al., **ICLR 2024**, arXiv:2310.16789 | **VERIFIED** |
| Neighbourhood comparison (no reference model needed) | Mattern, Mireshghallah, Jin, Schölkopf, Sachan, Berg-Kirkpatrick, *Findings of ACL 2023*, 11330–11343 | **VERIFIED** |
| Memorization without overfitting; larger models memorize more *and* generalize better | Tirumala, Markosyan, Zettlemoyer, Aghajanyan, **NeurIPS 2022**, arXiv:2205.10770 | **VERIFIED — flag closed** |
| Memorization can be *required* for optimal generalization on long tails | Feldman, **STOC 2020, pp. 954–959**, DOI 10.1145/3357713.3384290 | **VERIFIED** |
| Networks that generalize well nonetheless fit random labels | Zhang, Bengio, Hardt, Recht, Vinyals, **ICLR 2017**, arXiv:1611.03530 | **VERIFIED** |
| Lack of a well-defined randomness space; user-grounded reference sets | Kouam, Boyadzhiev, Rieck, arXiv:2608.02052 | **VERIFIED — venue is ACM CCS 2026; flag closed** |
| Probe choice changes canary verdicts; recommends decoy probes | Fan, Zhuang, Li, arXiv:2606.31168, ICML 2026 FoGen Workshop | **VERIFIED** ⚠️ backbone is **Qwen2.5-VL-7B** (a vision-language model), text-dominant LoRA-tuned — state this if cited |

## 2.7 Masked-model scoring

| Ingredient | Equation / claim | Primary source | Verified? |
|---|---|---|---|
| **PLL** | $\mathrm{PLL}(W)=\sum_t \log P_{\text{MLM}}(w_t\vert W_{\setminus t};\Theta)$; $\mathrm{PPPL}=\exp(-\tfrac1N\sum_W\mathrm{PLL}(W))$ | Salazar, Liang, Nguyen, Kirchhoff, **ACL 2020, pp. 2699–2712**, DOI 10.18653/v1/2020.acl-main.240 | **VERIFIED verbatim** |
| Cost | *"a sentence copy for each position, making the number of inference passes dependent on length"* — $O(\vert W\vert\cdot V)$ | Salazar et al. | **VERIFIED verbatim** |
| PLL is **unnormalized** | *"normalized $\log P_{LM}$, **unnormalized** PLL"*; $P_{\text{MLM}}(W)=\tfrac1Z\exp\mathrm{PLL}(W)$, $Z$ intractable and **length-dependent**; $\log P_{\text{GPT-2}}(\text{“San Francisco”})=-8.693$ vs $\mathrm{PLL}_{\text{RoBERTa}}=-1.006$ | Salazar et al. §2.1, Appendix B | **VERIFIED verbatim** |
| Rank-ordering licence | *"$\lambda\log Z$ does not affect rank-ordering when taking arg max"* — **valid only at fixed length** | Salazar et al. | **VERIFIED verbatim** |
| Vocabulary caveat | *"PPPLs are only comparable under the same subword vocabulary"* | Salazar et al. | **VERIFIED verbatim** |
| MLM is **not** an MRF | Original claim, then retraction, then peer-reviewed correction | Wang & Cho, *NeuralGen 2019*, ACL W19-2304, pp. 30–36, arXiv:1902.04094 — **claim still uncorrected in the published record**. Cho erratum (self-published, kyunghyuncho.me, 2019/2021). **Goyal, Dyer, Berg-Kirkpatrick, ICLR 2022**, arXiv:2106.02736: *"the masked conditionals on their own do not yield a Markov chain whose stationary distribution is that of our target distribution"* | **ALL VERIFIED verbatim.** Cite Goyal et al. as the peer-reviewed correction. |
| Mutual incompatibility of learned conditionals | Different masking patterns induce conditionals with no coherent joint | Young, Chen, You, arXiv:2301.00068; classical: Besag, *The Statistician* 24(3):179–195 (1975), DOI 10.2307/2987782 | **VERIFIED** |
| Within-word leakage in PLL; PLL-word-l2r | — | Kauf & Ivanova, **ACL 2023 Short, pp. 925–935**, DOI 10.18653/v1/2023.acl-short.80 | **VERIFIED** |
| Deriving proper LMs from MLMs | — | Torroba Hennigen & Kim, **ACL 2023 Short, pp. 1149–1159**, arXiv:2305.15501 | **VERIFIED — previously flagged "not vouched for"; flag closed** |
| **Erasure entropy** | *"the sum of entropies of the individual variables conditioned on all the rest"*; Theorem 1: $H^-(X)\le H(X)$, *"with equality if and only if [the variables] are independent"* | Verdú & Weissman, *IEEE Trans. Inf. Theory* **54(11):5030–5058** (2008), DOI 10.1109/TIT.2008.929968 | **VERIFIED verbatim, including the page range** |
| Erasure entropy $=$ population optimum of PLL | $\mathbb{E}_P[-\mathrm{PLL}(X)]\ge H^-(X)$ | **OUR DERIVATION** — no source states it | Mathematically sound (two lines from the verified Thm 1 + Gibbs); **present as a derivation, not received wisdom** |
| *"See itself"* | *"bidirectional conditioning would allow each word to indirectly 'see itself', and the model could trivially predict the target word in a multi-layered context"* | Devlin, Chang, Lee, Toutanova, **NAACL 2019**, §3.1, arXiv:1810.04805 | **VERIFIED verbatim.** The single best framing citation for the bug. |
| Target leakage (general ML) | *"the introduction of information about the data mining target that should not be legitimately available to mine from"* | Kaufman, Rosset, Perlich, Stitelman, *ACM TKDD* 6(4), Art. 15 (2012), DOI 10.1145/2382577.2382579 | **VERIFIED verbatim** |
| Any-order / masked-diffusion ELBO (a **valid** likelihood bound) | $-\log p_\theta(x)\le\mathbb{E}_{\sigma\sim U(S_n)}[-\sum_i\log p_\theta(x_{\sigma_i}\vert x_{\sigma_{<i}})]$ | Sahoo, Arriola, Schiff, Gokaslan, Marroquin, Chiu, Rush, Kuleshov, **NeurIPS 2024** | **VERIFIED (paper)** |

## 2.8 The genomic models and the DNA entropy scale

| Item | Value | Source | Verified? |
|---|---|---|---|
| HyenaDNA | *"uses single nucleotide tokens, and has full global context at each layer"*; **body confirms: "decoder-only… pretrained using next nucleotide (token) prediction"** $\Rightarrow$ causal, $k=1$ | Nguyen et al., **NeurIPS 2023 (Spotlight)**, arXiv:2306.15794 | **VERIFIED — previously-flagged causality question closed** |
| Evo | **single-nucleotide, byte-level tokenization, $k=1$** | Nguyen et al., *Science* 386(6723) (2024), DOI 10.1126/science.ado9336 | **VERIFIED — tokenizer flag closed** |
| DNABERT-2 | *"replace $k$-mer tokenization with Byte Pair Encoding (BPE)"* $\Rightarrow$ $k>1$ | Zhou, Ji, Li, Dutta, Davuluri, Liu, **ICLR 2024**, arXiv:2306.15006 | **VERIFIED verbatim.** ⚠️ **Average token length $k$: no published value exists.** Must be measured empirically. |
| Random DNA / conventional / frequency-only / best | 2.00 / 1.90 / **1.95** / 1.66 bits/base | Loewenstern & Yianilos, *J. Comput. Biol.* 6(1):125–142 (1999), DOI 10.1089/cmb.1999.6.125 | **VERIFIED** — note the **1.95** frequency-statistics-only figure, omitted from earlier reports; it is the more honest zero-order baseline |
| Reference-free compressors (bits/symbol) | HoSa **1.6265** / GeCo2 **1.6346** / XM **1.6383**; EsCo **1.8876** / **1.8949** / **1.9091**; ScPo **1.8925** / **1.8940** / **1.8951** | Pratas, Hosseini, Silva, Pinho, *Entropy* 21(11):1074 (2019), DOI 10.3390/e21111074, Table 1 | **VERIFIED — earlier digits were wrong by up to 0.008 bits; these are the typeset values.** Also **ScPo = *Schizosaccharomyces pombe*** (fission yeast), not *S. cerevisiae*. |
| GeCo3 | *E. coli* 1.09 MB; human **chr4 37.56 MB** | Silva, Pratas, Pinho, *GigaScience* 9(11):giaa119 (2020) | **VERIFIED — earlier report said 37.89 MB.** Corrected arithmetic: **1.580** bits/base (not 1.594); *E. coli* unchanged at ≈1.879 |
| HyenaDNA held-out PPL (Fig. 1.2) | 2-layer Transformer ≈**3.0–3.15**; 4-layer HyenaDNA 3.15→**2.95**; 8-layer 3.1→**2.92** | arXiv:2306.15794 Fig. 1.2 | **PARTIAL — read off a figure; no table exists.** ⚠️ Earlier reports said "2.9–3.3"; **nothing reaches 3.3.** Corrected range: ≈**2.9–3.15** |
| BCB '26 | Nemecek, Li, Jiang, Vaidya, Ayday, ACM BCB '26, DOI 10.1145/3807503.3819470, arXiv:2603.08913 | Crossref + arXiv | **VERIFIED** |

**The dynamic range this implies** — the most consequential single fact for interpreting any DNA perplexity number:

| Regime | bits/nt | $\mathrm{PPL}_{\text{nt}}$ |
|---|---|---|
| Information-theoretic ceiling (uniform iid) | 2.000 | **4.000** |
| 0-order baseline, human (GC ≈ 41%) | 1.9765 | **3.9353** |
| 0-order baseline, *E. coli* (GC ≈ 50.8%) | 1.99980 | **3.99889** |
| Best known compressors, *E. coli* / *S. pombe* | 1.888 / 1.893 | **3.70 / 3.71** |
| Best known compressors, human | 1.580–1.627 | **2.99–3.09** |
| Reported DNA LMs, human held-out | ≈1.55–1.66 | **≈2.9–3.15** |

*(0-order figures are our own arithmetic: $H = -2(0.205\log_2 0.205)-2(0.295\log_2 0.295)=1.9765$ for human.)*

**Read this carefully.** For human sequence the entire usable range of per-nucleotide perplexity lies between **≈3.94** (base composition only, zero learned structure) and **≈3.0** (matching the best DNA compressor ever built). For *E. coli* the band is **≈4.00 to ≈3.70** — an 8% window. Meanwhile a stride change alone moved GPT-2's WikiText-2 perplexity from **19.44 to 16.44** — a 15% swing with no model change (HuggingFace docs, verified). **A 15% evaluation artifact is larger than the entire distance from "learned nothing" to "state of the art" for bacterial genomes.** That is the strongest single argument that the scoring implementation must be audited before any attack result is trusted.

---

# 3. WHY IT IS SCIENTIFICALLY VALID — the strongest honest case

Five independent pillars. Each is a theorem; none is a heuristic.

## 3.1 The score is a log-probability by construction, not by assumption

Under (N) and (C), $q_\theta$ *is* a normalized distribution on $\mathcal{V}^T$ (§1.2). This is stronger than the usual framing: the model is not *approximating* a probability, it is *emitting* one. No calibration assumption is needed for $\log q_\theta(x)$ to be a genuine log-probability. This is the property that gives the score an absolute scale and makes every information-theoretic bound applicable.

## 3.2 Training targets exactly the right divergence — with an exact identity, not an approximation

$$-\tfrac{1}{|D|}\textstyle\sum_{x\in D}\log q_\theta(x) = H(\hat P) + D(\hat P\Vert q_\theta)$$

$H(\hat P)$ is $\theta$-independent. **Therefore minimizing empirical cross-entropy over $\theta$ is *exactly* minimizing $D(\hat P\Vert q_\theta)$** — no "up to a constant," no asymptotics.

Population version:
$$\mathbb{E}_{x\sim p}[-\log q_\theta(x)] = H(p) + D(p\Vert q_\theta) \ge H(p)$$
with equality iff $q_\theta = p$ (Cover & Thomas Thm 2.6.3, eq. 2.82).

## 3.3 The training objective's global optimum *is* memorization — which is why the score carries membership signal at all

The unconstrained minimizer of empirical cross-entropy over all distributions is $q^\star = \hat P$, the empirical distribution: mass $1/|D|$ on each training sequence, **exactly zero** on everything unseen. Gradient descent moves toward it. This is the honest, structural reason the score carries membership information — not an accident of overfitting, but the direction the objective points.

## 3.4 Log-probability is the *only* admissible per-sequence score

Gneiting & Raftery (2007), verified verbatim:
- $\mathrm{LogS}(p,\omega)=\log p(\omega)$ is **strictly proper** relative to $\mathcal{L}^1$; the associated information measure is negative Shannon entropy and the divergence is KL.
- **Bernardo's uniqueness result:** *"every proper local scoring rule is equivalent to the logarithmic score,"* i.e. equal to $c\log p(\omega)+h(\omega)$, $c>0$.
- The intuitively appealing linear score $\mathrm{LinS}(p,\omega)=p(\omega)$ is **not proper**.

A per-sequence LM score is by definition **local** — it looks only at the probability assigned to the outcome that actually occurred. So "why log-probability and not some other function of the model's output?" has a theorem for an answer: **if you want a score that is local and proper, log-probability is the only choice up to positive affine rescaling.**

Strict propriety also means overconfidence is punished without bound (the log score is unbounded below): a model cannot lower its measured cross-entropy by being confidently wrong. *(Condition to state: Bernardo's locality result requires $|\Omega|\ge3$ — for binary outcomes every proper rule is trivially local. Satisfied for $\mathcal{V}^T$.)*

## 3.5 The loss-threshold attack has an exact theorem behind it

Yeom et al. (CSF 2018) Theorem 2, verified verbatim: for Adversary 1 (query the model, output non-member with probability $\ell/B$),
$$\mathrm{Adv}^M(\text{Adversary 1}) = R_{\text{gen}}(A)/B$$
An **equality**, not a bound. A randomized loss-thresholding adversary achieves membership advantage exactly equal to the normalized generalization gap. This is the formal licence for "use the loss as a membership score," and it is the theorem the entire MIA vector rests on.

Complemented by Sablayrolles et al. (ICML 2019): under a posterior assumption on parameters, the **Bayes-optimal** membership rule depends on the model **only through the loss**. Black-box $\approx$ white-box; loss-based scoring leaves no information on the table.

## 3.6 What this adds up to

The quantity is not merely reasonable. It is:
- a genuine probability (theorem),
- the unique local proper scoring rule (theorem),
- exactly the thing training minimizes divergence on (identity),
- the Bayes-optimal membership statistic (theorem, under stated assumptions),
- lower-bounded by source entropy in a way that yields an executable correctness test (theorem).

**No competing quantity has this property set.** The student should be told, plainly, that the choice of score is the *strongest* part of the methodology, and that the vulnerabilities are entirely downstream of it.

---

# 4. WHERE IT IS NOT VALID — the honest limits

Every guarantee in §3 is a statement about **expectations under a fixed distribution**. None is a statement about a per-example decision. That gap is where every pathology below lives.

## 4.1 Intrinsic difficulty confounds the per-example score

$-\log q_\theta(x)$ is low both for memorized sequences **and** for sequences that are intrinsically easy: low-complexity, homopolymer runs, tandem repeats, Alu/LINE elements, CpG islands, GC extremes. A poly-A tract scores well whether or not it was trained on.

Decomposing: $\ell(f,z) \approx \mathrm{difficulty}(z) + \mathrm{membership\_effect}(z) + \mathrm{noise}$, and $\mathrm{Var}[\mathrm{difficulty}]$ across a corpus **dominates** $|\mathrm{membership\_effect}|$ for any single example. A global threshold $\ell<\tau$ therefore selects **easy examples**, only incidentally members.

**"The model assigns higher probability to training data" is not a theorem.** What is true is a statement about the *empirical mean* $\frac{1}{|D|}\sum_{x\in D}-\log q_\theta(x)$, which is what was minimized. Nothing constrains any individual $q_\theta(x)$, $x\in D$, relative to any individual $y\notin D$. Early stopping, regularization, limited capacity and smooth function classes all keep $q_\theta$ far from $\hat P$.

Primary sources, all verified:
- SS19 §4.1: *"whether the log-perplexity value is high or low depends heavily on the specific model, application, or dataset, which makes the concrete log-perplexity value ill suited as a direct measure of memorization."*
- C21: raw perplexity gave **9% / 3%** memorized samples vs **67%** for zlib-calibrated selection. This is primary-source evidence *against* using an uncalibrated likelihood as a memorization metric.
- Watson et al. (ICLR 2022): a **non-member can score high simply by being over-represented in the data distribution.**
- Sablayrolles et al.: the optimal threshold is $\tau(x,y)$, a **function of the example**. A constant $\tau$ is provably suboptimal.

**DNA-specific translation.** The zlib control does **not** port — zlib barely beats 2 bits/base on a 4-letter alphabet. The correct DNA analogue is division by a **genomics-grade compressor's** bits/nt for the same sequence (GeCo3 / JARVIS / XM), or by a $k$-th-order Markov model fit on held-out genome. In a genome where ~50% of sequence is repetitive, this is not a corner case; it is the dominant failure mode.

## 4.2 The set-level comparison is confounded too — and the confound is nameable

$$\mathbb{E}_{A}[-\log q] - \mathbb{E}_{B}[-\log q] = \underbrace{\big[H(A)-H(B)\big]}_{\text{intrinsic entropy gap}} + \underbrace{\big[D(A\Vert q)-D(B\Vert q)\big]}_{\text{what you want to measure}}$$

**Exact.** A raw NLL gap between member and non-member sets is evidence about model fit **only if the two sets have matched intrinsic entropy.** If they differ in GC content, repeat density, chromosome, assembly build, or provenance, the first term is nonzero and the attack measures composition. GC content alone moves the 0-order floor from 3.935 (41% GC) to 3.999 (50.8% GC) — a 1.6% shift with zero memorization, against an 8% total signal band for bacteria.

This is the best single audit tool in the whole document. Apply it to the member/non-member construction before trusting any gap.

## 4.3 Distribution shift masquerading as membership — and the blind baseline that detects it

**Das, Zhang & Tramèr (arXiv:2406.16201), verified in full.** Across **8 published MI evaluation datasets**, blind attacks — which distinguish member and non-member distributions **without looking at any trained model** — outperform state-of-the-art MI attacks:

| Benchmark | Metric | Best published attack | Blind baseline | Method |
|---|---|---|---|---|
| WikiMIA | AUC | 83.9% | **99.0%** | Bag-of-words |
| WikiMIA | TPR@5%FPR | 43.2% | **94.7%** | Bag-of-words |
| BookMIA | AUC | 88.0% | **91.4%** | Bag-of-words |
| Temporal Wiki | AUC | 79.6% | **79.9%** | Greedy rare-word |
| Temporal arXiv | AUC | 74.5% | **75.3%** | Bag-of-words |
| arXiv (all vs 1 mo) | TPR@1%FPR | 5.9% | **10.6%** | Date detection |
| arXiv (1 mo vs 1 mo) | TPR@1%FPR | 2.5% | **2.7%** | Greedy |
| LAION-MI | TPR@1%FPR | 2.5% | **8.9%** | Greedy |
| Project Gutenberg | TPR@1%FPR | 18.8% | **55.1%** | Greedy |

Blind wins on **all eight**. Their conclusion is total: existing evaluations tell us **nothing** about membership leakage.

**Why this is decisive.** An MIA claims to measure *what the model memorized*. A blind baseline measures *how the benchmark was built*. If the blind baseline wins, the published AUC is an upper bound on nothing about the model.

Corroborating, all verified: Duan et al. (COLM 2024) — success attributable to temporal distribution shift; Maini et al. (NeurIPS 2024) — *"most MIA methods perform no better than random guessing when discriminating between members and non-members from the same distribution"*; Meeus et al. (SaTML 2025) — post-hoc split construction is the root cause; Wang et al. (CheckMIABench 2026) — under a shift-free checkpoint-ordering design, **no attack is significantly above 0.500** across 70m–2.8b.

**Direct, cheap falsification test for BCB.** Train a bag-of-$k$-mers logistic regression ($k=3..6$) to separate the member split from the non-member split **using no model at all**. If it reaches AUC ≈ 0.70+, the reported membership signal is distribution shift. One afternoon.

**A quantitative hook.** Under the simple confound model where a fraction $\alpha$ of members is trivially separable and the rest is exchangeable with non-members,
$$\mathrm{AUC} = \alpha\cdot1 + (1-\alpha)\cdot\tfrac12 = \frac{1+\alpha}{2} \quad\Longrightarrow\quad 2(\mathrm{AUC}-0.5)=\alpha \text{ exactly.}$$
Worked: $\alpha = 900/1900$ gives $\mathrm{AUC} = 0.473684 + 0.526316\times0.5 = \mathbf{0.736842}$. **BCB's own risk score is $s_{\text{mia}}=\max(0,2(\mathrm{AUC}-0.5))$ — so BCB is already reporting $\alpha$ without knowing it.** Its AUC 0.70–0.79 implies $\alpha = 0.40$–$0.58$: *40–58% of member sequences are trivially identifiable from a confound.* That is a falsifiable prediction the blind baseline tests directly. Note also that if the confound is **symmetric** (members longer *and* non-members shorter, which is the usual genomic case), the same $\alpha$ gives $\mathrm{AUC}=0.8615$ — so 0.7368 is the *conservative* figure and the realistic confound ceiling is higher.

## 4.4 The null is unsamplable — the deepest problem

Zhang, Das, Kamath & Tramèr (SaTML 2025), verified: a scientifically convincing membership claim requires a low FPR under the null *"the model was not trained on this data,"* and that null is **unsamplable** — you don't know the training set and cannot afford to retrain. Their two recommended escapes: **(i) extraction attacks** and **(ii) membership inference on planted canaries**, where membership is controlled by construction.

**This is the strongest available justification for the canary component of BCB's framework, and simultaneously the strongest argument that the non-canary MIA component cannot carry a claim.**

## 4.5 Reference models are not optional

LiRA frames membership as a Neyman–Pearson test,
$$\Lambda(f;x,y)=\frac{p(f\mid Q_{\text{in}}(x,y))}{p(f\mid Q_{\text{out}}(x,y))}$$
where shadow models exist **solely to estimate the null (and alternative) distribution of the score for that specific example**. The logit rescaling $\phi(p)=\log(p/(1-p))$ makes confidences approximately Gaussian (raw confidence and raw cross-entropy are not). With $<64$ shadows, pool the **variances** globally but keep the **means per example** — pooling the means collapses LiRA back to a global threshold. Offline variant gives a per-example $p$-value under the null "not trained on."

Report **TPR at fixed low FPR (≤0.1%, and 1%)** and **log–log ROC**. Carlini et al.'s argument: privacy is not an average-case property; AUC is symmetric (charging the same for a false accusation as for a miss) and average-case. Their empirical kill shot — Yeom's global threshold at 59.5% balanced accuracy but essentially zero TPR at low FPR, versus Long et al. at 53.5% accuracy but strictly higher low-FPR TPR — **the aggregate ranking is inverted relative to the metric that matters**. *(Metadata verified; this specific comparison was not re-read from the PDF.)*

## 4.6 Tokenization dependence

HuggingFace reference, verified verbatim: *"the tokenization procedure has a direct impact on a model's perplexity"* and — decisively — *"the metric applies specifically to classical language models… and is not well defined for masked language models like BERT."*

For your model set: SimpleDNALM ($k=1$), HyenaDNA ($k=1$, verified), Evo ($k=1$, verified byte-level) coincide **accidentally**. DNABERT-2 (BPE, $k>1$, no published value) is on a **different scale**. Report every model in $\mathrm{PPL}_{\text{nt}}$ and never in native token units.

**An additional confound we have not seen stated anywhere, and which matters for BCB's table structure:** $k$ is not a property of the tokenizer alone — it is a property of the tokenizer *applied to a given corpus*. A BPE vocabulary trained on real multi-species genomes will produce **shorter** tokens on uniform random DNA (no exploitable motifs, so it falls back to short merges) than on real sequence. So DNABERT-2's $\bar k$ on the synthetic dataset $\ne$ its $\bar k$ on GUE or yeast, and a single conversion constant applied across BCB's four datasets would be wrong in a dataset-dependent direction. **Measure $\bar k = \sum_j L_j/\sum_j T_j$ separately per dataset.** *(This inference is ours; not from any source.)*

## 4.7 Length, stride, padding

**(a) Raw sum is not comparable across lengths.** $\log q(x)\approx -L\bar H$, so a ranking by raw summed log-probability is, to first order, a **ranking by length**. For canary extraction against 1,000 candidates this is not cosmetic: unequal lengths make the ranking measure nothing.

**(b) Normalization is not neutral either.** Early positions have little context and higher loss. An AR model without a BOS token cannot score $x_1$ at all: only $T-1$ of $T$ positions contribute, and whether the denominator is $T$ or $T-1$ changes the number. Variance of the per-token mean scales as $1/T$, so short sequences have heavier-tailed scores — any threshold applied across mixed lengths preferentially flags short sequences.

**(c) Dilution.** A 50 bp memorized span in a 1000 bp window contributes 5% of the average. C21's published fix is the sliding-window minimum over 50 tokens.

**(d) Stride.** Verified: GPT-2 on WikiText-2 gives **19.44** at stride 1024 and **16.44** at stride 512 — same model, same data, 15% apart. Train and test must be scored with byte-identical windowing, stride and batching.

**(e) Padding.** If pad tokens enter the loss and are predicted near-deterministically, observed CE $\approx(1-f_{\text{pad}})\cdot$ true CE. To fake 1.4276 bits from a true 2.0 bits requires $f_{\text{pad}}\approx\mathbf{0.286}$ — entirely plausible for fixed-length padded batches, and it would **silently survive a causal-mask fix**. The bias is multiplicative in bits, so it is invisible in a train/test *ratio* when both splits pad equally — and catastrophic when they don't (short canaries, full-length test sequences). Note explicitly: **no peer-reviewed source names this as a perplexity pathology.** It is convention-level, documented in HuggingFace's `-100` masking. Cite it as an implementation requirement, not a literature finding.

## 4.8 Masked/bidirectional models

Perplexity has **no definition** for a masked LM, because $q_\theta(x)$ is not a normalized distribution over sequences. The standard substitute is PLL (Salazar et al. 2020), and PLL is explicitly an **energy**, not a log-probability: their own worked example gives $\mathrm{PLL}_{\text{RoBERTa}}(\text{“San Francisco”})=-1.006$, i.e. $\exp(-1.006)=0.366$ — a single bigram carrying 37% of the mass. $\sum_x\exp\mathrm{PLL}(x)\ne1$; the normalizer $Z$ is intractable **and length-dependent**.

The historical claim that BERT is an MRF language model (Wang & Cho 2019) is **wrong and was retracted by Cho himself**. The error: the construction defines $\log\phi_t=\log P_\theta(x_t\mid x_{\setminus t})$ and assumes $x_t$ is unaffected by the other potentials — false, because $x_t$ is an input to $f_\theta(x_{\setminus t'})$ for every $t'\ne t$. The arXiv v2 and the ACL Anthology version **still carry the uncorrected claim**; anyone citing the published record inherits an error the author has disavowed. Cite **Goyal, Dyer & Berg-Kirkpatrick (ICLR 2022)** as the peer-reviewed correction.

**Consequence for cross-model tables:** even with a correct PLL, **a table placing DNABERT-2's pseudo-perplexity next to HyenaDNA's and Evo's perplexity is not a valid comparison.** PPPL is systematically lower on real data because each prediction uses bidirectional context. Defensible options: (i) report DNABERT-2 separately with an explicit caveat; (ii) compare each model only against *its own* control (its score on shuffled or random DNA), so only within-model ratios cross the table; (iii) equalize the conditioning set (§5.6); (iv) use an any-order/masked-diffusion ELBO, which *is* a valid variational upper bound on NLL and *does* respect the floor.

**A second-order bug to check independently:** Kauf & Ivanova (ACL 2023) show standard PLL **inflates scores** because masking only the target still leaks information from *within-word* neighboring subword tokens. For a BPE-tokenized DNA model this is not merely analogous — it is a live second bug, and it produces the same signature (scores too high, perplexity too low).

## 4.9 The train/test gap measures generalization, not memorization

**Verdict: the gap is a valid measure of generalization gap. It is not a valid measure of memorization.** It is neither necessary nor sufficient.

- **Not sufficient:** Yeom Theorem 4 — a model can generalize perfectly and still leak membership completely. High gap can also arise from distribution shift with no memorized content.
- **Not necessary:** Tirumala et al. (NeurIPS 2022) — larger models memorize *more and faster* while *generalizing better*. The gap and memorization move in **opposite directions** across scale. Feldman (STOC 2020) — on long-tailed distributions, memorizing rare instances is *necessary* for close-to-optimal generalization; a model can have zero gap and be memorizing by design. (Genomic relevance is high: rare variants are exactly a long tail.) Zhang et al. (ICLR 2017) — capacity to memorize is orthogonal to generalization. SS19 adds the temporal argument: canary exposure peaks around when training loss levels off, i.e. memorization is well underway while validation loss is still improving.

**Genomics-specific confounds, severe:**
1. **Near-duplication across splits.** Human sequence is ~50% repetitive; an Alu in "test" has hundreds of thousands of near-copies in "train." Plus paralogs, homologs, related individuals, shared haplotypes. **A random split of genomic windows does not produce independent test data.** Split by chromosome; if individuals are involved, split by individual with a kinship check; report the repeat fraction of each split.
2. **Chromosome-level shift.** Train chr1–20 / test chr21–22 partly measures GC content, gene density and repeat-class differences.
3. **Composition.** §4.2.
4. **Evaluation-time asymmetry.** §4.7.
5. **Deduplication status** differing between splits.

## 4.10 Per-decision instability

Hayes et al. (NeurIPS 2025), verified: scaling genuine LiRA to GPT-2-architecture models 10M–1B with references trained on 20B+ C4 tokens — strong MIAs **can** succeed on pretrained LLMs, but performance ceilings around **AUC < 0.7**, and even when aggregate performance beats chance, **many individual membership decisions are statistically indistinguishable from a coin flip** because they flip under training randomness. **A reported AUC with no seed variance is not interpretable.**

---

# 5. THE 4.0 FLOOR

## 5.1 The theorem, stated exactly

> Let $p, q$ be probability distributions on a common countable set $\mathcal{X}$. Then
> $$\mathbb{E}_{x\sim p}\big[-\log_2 q(x)\big] = H(p) + D(p\Vert q) \;\ge\; H(p),$$
> with equality iff $q = p$ $p$-a.e.

**Hypotheses — all four necessary, none asymptotic:**

- **(H1)** $q$ is normalized on $\mathcal{X}$. *(Sub-normalization $\sum q<1$ only raises the bound; it is **super**-normalization $\sum q>1$ that destroys it.)*
- **(H2)** $q$ is chosen independently of the evaluation sample.
- **(H3)** The expectation is under the true $p$ over the whole sample — not a selected subsequence.
- **(H4)** $H(p)$ is the entropy of the **actual** data, not the assumed data.

For $p$ = iid uniform on $\{A,C,G,T\}$: $H(p)=\log_2 4 = 2$ bits/nt **exactly**, so
$$\mathrm{PPL}_{\text{nt}} = 2^{\mathbb{E}[-\log_2 q]} \ge \mathbf{4.0}$$
with equality iff $q$ is exactly uniform at every position. Two-line proof; not a rule of thumb.

> **Important correction to the earlier reports.** An earlier statement of the conditions gave "$q$ is a genuine normalized distribution **over sequences**, $\sum_x q(x)=1$" as a necessary condition. **It is sufficient, not necessary.** A per-position family $\{q_i\}$ that is normalized *per position* and does not see its own target satisfies the floor with no joint ever being normalized. This over-strong condition is exactly what led one report to the wrong conclusion about PLL in §5.5.
>
> **The correct necessary condition is: per-position normalization over $\{A,C,G,T\}$, plus no self-conditioning.**

## 5.2 The only two legitimate routes below 4.0 on uniform DNA

**(a) Sampling noise.** Quantified in §5.3. Bounded by $O(1/n)$.

**(b) The data is not what you think it is (H4).** A biased RNG, GC skew, or accidental reuse of real sequence lowers $H(p)$ and lowers the floor honestly. To reach 1.4276 bits/nt legitimately requires true source entropy $\le1.4276$ bits/nt — a composition like $(0.62,0.18,0.10,0.10)$, grossly visible in a mononucleotide count. **One line of code falsifies it.**

**Everything else is a bug.** Full differential diagnosis:

1. **$q$ not normalized over sequences** — bidirectional context leaking $x_i$ into the prediction of $x_i$. *Diagnostic:* on $\mathcal{V}=4$, $L=8$ (65,536 sequences), brute-force $\sum_x\prod_i q(x_i\mid\cdot)$; it must equal 1.000. Cheap, decisive, worth adding as a unit test.
2. **Normalizer mismatch** — per-token summed log-prob divided by a nucleotide count (or vice versa) without the $k$ correction.
3. **Non-uniform "random" data** — route (b) above.
4. **Off-by-one** — scoring $T-1$ positions while dividing by $T$.
5. **Selection** — averaging over a subset chosen because the model scores it well. The floor bounds $\mathbb{E}_{x\sim p}$; selection has **no $\sqrt n$ protection**.
6. **Teacher forcing with the target visible** — the general case of (1).
7. **Padding contamination** — §4.7(e). $f_{\text{pad}}\approx0.286$ reproduces 1.4276 from a true 2.0.
8. **Subword tokenization of a PLL objective** — §5.5. Quantitatively the largest of these, and absent from all prior reports.

## 5.3 Finite-sample fluctuation — exact numbers

Setup from the brief: 200 sequences × 256 nt.

**(i) The closed form, verified.** Parametrize $q_a=\tfrac14(1+\varepsilon_a)$, $\sum\varepsilon_a=0$, $S=\sum\varepsilon_a^2$. To second order, $\mathrm{KL}\approx S/8$ nats and $\mathrm{sd}(\ell)\approx\sqrt S/2$ nats. Minimizing $S/8 - z\sqrt S/(2\sqrt n)$ over $S$ gives $\sqrt S = 2z/\sqrt n$ and

$$\boxed{\;\text{max legitimate dip below } H(p) \;=\; \frac{z^2}{2n}\ \text{nats} \;=\; \frac{z^2}{2n\ln 2}\ \text{bits}\;}$$

Verified against an exact non-perturbative scan over the 4-simplex (closed form is a 0.5–2% *under*estimate, i.e. mildly anti-conservative — immaterial here):

| tokenization | $n$ | $z$ | max dip (bits/nt) | implied $\mathrm{PPL}_{\text{nt}}$ floor |
|---|---|---|---|---|
| single-nt | 51,200 | 3 | $1.27\times10^{-4}$ | 3.99965 |
| single-nt | 51,200 | 4 | $2.25\times10^{-4}$ | 3.99938 |
| single-nt | 51,200 | 5 | $3.52\times10^{-4}$ | 3.99902 |
| BPE, $k\approx5.6$ | 9,143 | 4 | $1.26\times10^{-3}$ | 3.99650 |
| BPE, $k\approx5.6$ | 9,143 | 5 | $1.97\times10^{-3}$ | 3.99453 |

**The structural insight is the whole point:** a perfectly uniform model has *zero* per-token variance, so it cannot fluctuate below at all. Any downward fluctuation must be **bought** with miscalibration, which raises the mean by $\Theta(S)$ while the noise only falls as $\Theta(\sqrt S/\sqrt n)$. The trade-off is what makes the dip $O(1/n)$.

> **Correction applied.** An earlier report stated the deviation below the floor is $O(1/\sqrt N)$. **It is $O(1/N)$.** Taken literally, $O(1/\sqrt N)$ would admit a legitimate dip of ~0.2 bits/nt at $n=10^5$ — nearly half the observed deficit. Off by a factor of $\sqrt n \approx 226$.

**(ii) A rigorous, assumption-free replacement — use this, not the CLT.** Invoking a CLT at $z\sim10^2$ is not a valid use of a CLT. You do not need one. The no-hypercompression inequality is exact:

> For any normalized $q$ on $\mathcal{X}$ chosen independently of $x\sim p$: $\;\Pr\big[\log_2\tfrac{q(x)}{p(x)}\ge t\big]\le 2^{-t}$.
> *Proof:* Markov's inequality on $q/p$, using $\mathbb{E}_p[q/p]=\sum_x q(x)\le1$. $\square$

For uniform DNA ($-\log_2 p(x)=2n$), a measured deficit of $\delta$ bits/nt over $n$ scored nucleotides has probability at most $2^{-n\delta}$, **whatever the model**:

| $n$ | $\delta$ (bits/nt) | rigorous bound |
|---|---|---|
| 51,200 | $1\times10^{-4}$ | $\le 2.9\times10^{-2}$ |
| 51,200 | $2\times10^{-4}$ | $\le 8.3\times10^{-4}$ |
| 51,200 | $1\times10^{-3}$ | $\le 3.9\times10^{-16}$ |
| 51,200 | **0.5724 (observed)** | $\le 2^{-29307}\approx 10^{-8822}$ |
| 9,143 | **0.5724 (observed)** | $\le 2^{-5233}\approx 10^{-1575}$ |

Inverting: at $\alpha=10^{-6}$ the rigorous max dip is $3.9\times10^{-4}$ bits/nt, i.e. $\mathrm{PPL}_{\text{nt}}\ge3.99892$. Note the bound reproduces the Gaussian form analytically ($\log_2(1/\alpha)/n$ vs $z^2/(2n\ln2)$, since $\ln(1/\alpha)\approx z^2/2$ in a Gaussian tail) — independent confirmation that the closed form is right, while being valid in the far tail where a CLT is not.

**(iii) What a realistic slightly-miscalibrated scorer looks like** on $n=51{,}200$:

| model conditional $q$ | $\mathbb{E}[\mathrm{CE}]$ | per-token sd | SE of the mean | measured PPL |
|---|---|---|---|---|
| $(.28,.26,.24,.22)$ | 2.00581 b/nt | 0.130 b | $5.7\times10^{-4}$ b | $4.016\pm0.0016$ |
| $(.30,.25,.25,.20)$ | 2.01472 b/nt | 0.207 b | $9.2\times10^{-4}$ b | $4.041\pm0.0026$ |
| $(.35,.25,.22,.18)$ | 2.04323 b/nt | 0.349 b | $1.5\times10^{-3}$ b | $4.122\pm0.0044$ |

**Answer, stated plainly.** For a correctly implemented causal scorer on 200×256 uniform random DNA, the plausible range is
$$\mathrm{PPL}_{\text{nt}} \in [\,3.999,\ \approx4.06\,]$$
with a standard error on the order of $10^{-3}$ perplexity units and an absolute hard floor of **3.9990** at any sane confidence level. **A value of 3.98 is already impossible.**

## 5.4 Exactly how damning is 2.69

$2.69 \Rightarrow \log_2 2.69 = \mathbf{1.4276}$ bits/nt. Deficit from 2.0 bits: **0.5724 bits/nt**.

- **Rigorous (Barron):** probability $\le 10^{-8822}$ at $n=51{,}200$, $\le 10^{-1575}$ at $n=9{,}143$. Assumption-free.
- **Sigma equivalent** (worst-case-optimal $q$, the most generous possible): $z=\sqrt{2n\ln2\cdot\delta}$ gives **201.6σ** at $n=51{,}200$ and **85.2σ** at $n=9{,}143$.
- **In model terms:** under the leaky-scorer identity $\mathrm{PPPL}=1/\varepsilon$, we get $\varepsilon = 1/2.69 = 0.372$ — the model assigns (geometric mean) **37.2%** to the true base where the Bayes-optimal answer on informationless data is exactly **25%**. That is **1.49×** chance. Over a 1,000-token sequence, ~572 bits of the target leaked into its own conditioning.

> **Corrections applied.** (1) An earlier report said "in sigma units it is on the order of $10^2$–$10^3$." **The $10^3$ end is not attained**; the correct range is 85σ–202σ, all $10^2$. (2) The same report's "1,625×" and "~290×" figures are ratios of **dips**, and since dip $\propto z^2$, they correspond to $\sqrt{1625}\cdot5=202$ and $\sqrt{290}\cdot5=85$. (3) Note that the *smaller* $n$ (BPE) gives the *smaller* $z$, not the larger — the earlier phrasing invited the opposite reading. (4) **Replace the sigma framing entirely with Barron in anything written down.** $10^{-8822}$ is exact; "202σ" is uninterpretable.

## 5.5 Does the same floor apply to a PLL scorer? — RESOLVED

The three ground reports contradicted each other. Here is the resolved answer, in three parts.

### Part A — Single-nucleotide masking: **YES, the floor holds exactly at 4.0.**

> **Theorem (PLL floor).** Let $X=(X_1,\dots,X_n)\sim P$. Let $\{q_i(\cdot\mid x_{\setminus i})\}$ be **any** family of conditionals that are (i) normalized over the alphabet at position $i$ and (ii) functions of $x_{\setminus i}$ **only**. Then
> $$\mathbb{E}_P[-\mathrm{PLL}(X)] = \sum_i \mathbb{E}\big[-\log q_i(X_i\mid X_{\setminus i})\big] \;\ge\; \sum_i H(X_i\mid X_{\setminus i}) \;=:\; H^-(X)$$
> with equality iff $q_i$ equals the true conditional a.s.
>
> *Proof.* Fix $i$, condition on $X_{\setminus i}=c$. Then $\mathbb{E}_{X_i}[-\log q_i(X_i\mid c)] = H(X_i\mid X_{\setminus i}{=}c)+D_{KL}(P(\cdot\mid c)\Vert q_i(\cdot\mid c)) \ge H(X_i\mid X_{\setminus i}{=}c)$. Average over $c$, sum over $i$. $\square$

$H^-(X)$ is exactly **erasure entropy** (Verdú & Weissman 2008, definition verified verbatim). **The population optimum of PLL is the erasure entropy.** *(This identification is our derivation; no paper states it. It follows in two lines from verified results, and is arguably worth stating explicitly in the write-up.)*

**Corollary A.** If $X_i \stackrel{iid}{\sim}\mathrm{Unif}\{A,C,G,T\}$, then $H(X_i\mid X_{\setminus i})=H(X_i)=\log_2 4$ exactly — independence makes conditioning worthless. Hence $\mathrm{PPPL}\ge4.0$, with equality iff the model outputs uniform. **Confirmed by brute force over all $4^8$ strings with a single-nucleotide tokenizer: $H^- = 16.000000$ bits/seq $=2.000000$ bits/nt, floor exactly 4.000000.**

Numerically confirmed both directions: a *proper* context-only scorer on uniform DNA making aggressive, confident, wrong guesses from neighbours recorded $\mathrm{PPPL}=\mathbf{31.93}$ — well above 4.0, and it cannot be pushed below by any strategy. A *leaky* scorer placing mass $\epsilon$ on the observed token gave $\mathrm{PPPL}=1/\epsilon$: **1.111** at $\epsilon{=}0.9$, **1.010** at 0.99, **1.001** at 0.999. Monotone collapse toward 1.0.

**Verdict:** the earlier claim that "the 4.0 floor does not apply to PLL" is **WRONG** for single-nucleotide masking. The floor comes not from the product being a normalized joint (it is not) but from a **per-position Gibbs inequality** — which is precisely why the over-strong condition in §5.1 was the source of the error.

### Part B — On real DNA: **NO, and you must not port the check.**

Verdú & Weissman **Theorem 1** (verified verbatim): $H^-(X)\le H(X)$, *"with equality if and only if [the variables] are independent."* Real DNA is strongly dependent, so $H^- < H$ **strictly**. A **correct** PLL scorer on real DNA legitimately reports per-nucleotide pseudo-perplexity **below** the autoregressive entropy rate, because it conditions on both sides.

Uniform random DNA is the **unique** input distribution where the erasure-entropy floor and the entropy-rate floor coincide. That is precisely what makes it a clean leakage detector — and precisely why the check must never be applied to real sequence, and why PPPL and causal PPL must never be pooled in a table.

### Part C — BPE token-level masking: **NO. The floor is NOT 4.0, and this is the finding that changes the plan.**

DNABERT-2's PLL masks a **BPE token**, so the relevant floor is $H^-$ of the **token** process, not the nucleotide process. BPE tokens are strongly dependent even when the underlying nucleotides are iid uniform: merge canonicity constrains neighbours, and at fixed total length $L$ the masked token's nucleotide length is exactly determined by the others. Therefore $H^-(\text{tokens}) < H(\text{tokens}) = 2L$ **strictly**.

There is an exact computation, requiring **no model at all**. Under fixed-length uniform DNA every length-$L$ string is equiprobable and BPE encoding is injective, so for a masked position with context $c$,
$$P(\text{token}_i=v\mid c) = \frac{1}{\#\mathcal{V}_{\text{valid}}(c)}, \qquad H(\text{token}_i\mid c)=\log_2\#\mathcal{V}_{\text{valid}}(c)$$
where $\mathcal{V}_{\text{valid}}(c)$ is the set of vocabulary items that, inserted at $i$, yield a length-$L$ string whose canonical BPE encoding is $c$ with $v$ at $i$. **The floor is the geometric-mean number of tokens that legally fit the hole — computable from the tokenizer alone.**

Measured (BPE trained on random DNA, exact enumeration of $\mathcal{V}_{\text{valid}}$ per masked position):

| $\vert\mathcal V\vert$ | $k$ (nt/tok) | mean $\#\mathcal V_{\text{valid}}$ | **erasure floor** | **best possible $\mathrm{PPPL}_{\text{nt}}$** | claimed floor |
|---|---|---|---|---|---|
| 4 (no merges) | 1.00 | 4.00 | 2.0000 b/nt | **4.0000** | 4.0 ✅ |
| 68 | 2.54 | 9.92 | 1.3052 b/nt | **2.4711** | 4.0 ❌ |
| 132 | 2.90 | 17.02 | 1.4100 b/nt | **2.6573** | 4.0 ❌ |
| 260 | 3.28 | 23.89 | 1.3974 b/nt | **2.6342** | 4.0 ❌ |

Note also the per-token floor is $\approx$10–24, **far below** the $4^k$ of 34–94 that one report claimed.

### The three consequences — state these to the student explicitly

1. **The proposed CI assertion "$\mathrm{PPPL}_{\text{nt}}\ge4.0$ for DNABERT-2" is invalid as written.** It would fail on a *correct* token-level PLL implementation. The correct assertion for a subword model is $\mathrm{PPPL}_{\text{nt}}\ge 2^{H^-_{\text{tok}}/L}$ with $H^-_{\text{tok}}$ measured from DNABERT-2's real tokenizer by the recipe above.

2. **"2.69 < 4.0 therefore the scored object is not a likelihood" is not sound as a general argument.** It is sound iff the scorer's conditionals are normalized over $\{A,C,G,T\}$ and do not see their own target. Under token-level BPE PLL, a legitimate floor of ≈2.47–2.66 sits **right on top of** the observed 2.69. **If the extension paper asserts the 4.0 argument as a proof, a referee who knows subword information theory will break it.**

3. **The bug diagnosis nevertheless stands — on independent grounds.** The described implementation (bidirectional encoder, no causal mask, next-token-shifted head) violates condition (C) directly: self-attention without a causal mask gives position $i$'s representation access to $x_{i+1}$ at every layer, so the scored quantity is $q(y\mid x_{\setminus\{i+1\}}, \mathbf{y})$ and $H(X_{i+1}\mid X_1..X_n)=0$. The floor collapses from $\log_2 4$ to **0**, so the attainable perplexity is $\ge1.0$, not $\ge4.0$, and a fully-converged leaky model drives PPPL $\to1.0$. Nothing is wrong with the optimizer — it is solving a copy task, and the identity map is the optimum. **This is the exact pathology BERT's masking objective exists to prevent** (Devlin et al., verified verbatim: *"bidirectional conditioning would allow each word to indirectly 'see itself', and the model could trivially predict the target word in a multi-layered context"*). That framing is much stronger than the floor argument and does not depend on any number.

### The single most important thing to establish first

**Is BCB's 2.69 per-token or per-nucleotide?** Neither report resolves it, and both implicitly assume per-nucleotide in places.

- If **per-nucleotide**: 2.69 sits above the BPE-PLL erasure floor of ≈2.47–2.66 and the floor argument does **not** carry the bug diagnosis. Use the structural (C)-violation argument instead.
- If **per-token** with $k\approx2.5$: the implied per-nucleotide figure is $2.69^{1/2.5}=\mathbf{1.47}$ bits-equivalent, which is **below even the erasure floor**, and the bug conclusion is airtight.

This single fact determines which argument you can make. Resolve it before writing anything.

## 5.6 What to do instead — matched conditioning

There is **no formal treatment of equalizing conditioning information for cross-architecture memorization comparison** in the literature we could find. This is a genuine gap and plausibly the extension's contribution. Three options:

- **Option 1 — Don't compare.** Report causal PPL for causal models and PPPL for DNABERT-2, never pooled, never on a shared axis. Safe, weak.
- **Option 2 — Equalize the conditioning set (recommended primary fix).** Score every model with the *same* prefix-only conditioning: feed DNABERT-2 $x_{<i}$ with all of $x_{\ge i}$ masked, read position $i$. Cost is $n$ forward passes. Both models then estimate the same quantity $H(X_i\mid X_{<i})$, comparability is exact, **and the 4.0 floor is restored for both.** Methodological precedent: von Arx & Dieudonné's contrast of native FIM-format probes vs. prefix probes.
- **Option 3 — Use a genuinely valid likelihood (stronger theoretical claim).** The any-order / masked-diffusion ELBO:
$$-\log p_\theta(x) \le \mathbb{E}_{\sigma\sim U(S_n)}\Big[-\sum_{i=1}^{n}\log p_\theta(x_{\sigma_i}\mid x_{\sigma_{<i}})\Big]$$
Each factor conditions on a **strict prefix under a random order** — never on all other tokens — so this is a true variational upper bound on NLL, $\mathbb{E}[-\log p_\theta(X)]\ge H(X)$ by Gibbs, and **the 4.0 floor holds.** Contrast with PLL, which conditions on everything else and therefore targets erasure entropy. Sahoo et al. (NeurIPS 2024) give the Rao-Blackwellized continuous-time ELBO.

Report PLL/PPPL **only** as a ranking score for equal-length, equal-tokenization candidates — never as a perplexity.

---

# 6. VERDICT ON THE BCB PAPER'S USE OF EACH METRIC

All BCB claims below were verified against the arXiv full text (arXiv:2603.08913) and the Crossref record for DOI 10.1145/3807503.3819470.

## 6.1 Perplexity

**Is the metric sound?** Yes, for causal models. It is the unique local proper scoring rule, it has an exact floor, and it is the right quantity to average.

**Is BCB's implementation faithful?** Partly, with one misapplication and two implementation defects.

| Component | Verdict |
|---|---|
| Causal models (SimpleDNALM, HyenaDNA, Evo) | **Metric sound.** All three are $k=1$ (HyenaDNA and Evo verified), so per-token = per-nucleotide and the floor applies directly. |
| **DNABERT-2 row** | **METRIC MISAPPLIED.** Perplexity has no definition for a masked LM (HuggingFace, verbatim: *"not well defined for masked language models like BERT"*). Placing a bidirectional encoder's score in a perplexity table alongside causal models is a category error, independent of the bug. |
| DNABERT-2 scoring implementation | **IMPLEMENTATION BROKEN** on top of the misapplication: a next-token-shifted head with no causal mask violates condition (C), and the model's own target is in its conditioning set. |
| The **2.69** value | **CONFIRMED in the published paper**: Table 4, DNABERT-2 / Synthetic / **Test = 2.69 ± 0.04**. Whether it is per-token or per-nucleotide is **unresolved** and must be established (§5.5). |
| $\bar k$ normalization | **NOT DONE and NOT POSSIBLE from published information.** DNABERT-2's average token length has no published value. Its per-token perplexity is on a different scale from the other three models', and $\bar k$ additionally differs per dataset. |
| $s_{\text{ppl}} = 1 - \bar p_{\text{canary}}/\bar p_{\text{test}}$ | **IMPLEMENTATION DEFECT in aggregation.** A ratio of *arithmetic means of exponentials* has no information-theoretic meaning and is dominated by the high-perplexity tail of whichever set has more variance. Aggregate in the bits domain (total NLL / total nucleotides) or report the full per-sequence distribution. |

> **Correction applied, and it matters for fairness to the paper.** An earlier report claimed BCB's Table 4 shows *"synthetic-dataset perplexities of 3.82–4.00 … so even the 'clean' models sit slightly under the floor."* **This is not supported.** In Table 4, SimpleDNALM / Synthetic is Train 3.93 / **Test 4.00** / Canary 3.93. The **held-out synthetic value is exactly 4.00, not below it**; 3.93 and 3.91 are *train* and *canary* (trained-on) values, and 3.82–3.86 are GUE/Yeast rows — real genomic data, to which no 4.0 floor applies. **Only DNABERT-2's 2.69 is anomalous.** Delete this claim; as stated it manufactures a floor violation the table does not show.

## 6.2 Exposure

**Is the metric sound?** Yes. SS19 Definition 4, $\mathbf{exposure}=\log_2|\mathcal{R}|-\log_2\mathbf{rank}$, with the scientific justification being Definition 3: exposure is the $\log_2$ ratio of guessing entropies with and without model access — the number of bits of guesswork the model saves an adversary.

**Is BCB's implementation faithful?** **No — and this is an implementation defect with an exact, quantifiable magnitude, not a subtle judgment call.**

- **What the paper states.** §4.3.2 Eq. (1) writes $\text{Exposure}(s)=\log_2|R|-\log_2(\text{rank}(s))$ and glosses $\text{rank}(s)$ as the rank *"among all possible sequences in $R$"* — i.e. SS19 Definition 2, correctly.
- **What the paper does.** Same paragraph: condition on a canary prefix, generate with **beam search (width 10, max 1,000 candidate sequences)**, rank the true canary among *those*. Canaries are 100 sequences of 64 nt, uniform, 50% GC (all verified), so $|R|=4^{64}$ and $\log_2|R|=128$.
- **The paper is internally inconsistent on its own page:** Eq. (1)'s rank is defined over a set of $3.4\times10^{38}$ elements and computed over a set of at most $10^3$.

**The arithmetic.** With $n\le1000$ candidates, $\mathbf{rank}\in[1,n{+}1]$, so
$$\text{Exposure}_{\text{BCB}} \in [\,128-\log_2 1001,\ 128\,]=[\,118.03,\ 128.00\,]$$
whereas SS19's sampling estimator on the same experiment gives
$$\text{Exposure}_{\text{correct}} = \log_2(1000)-\log_2(\mathbf{rank}) \in [\,-0.0014,\ 9.97\,]$$
$$\Longrightarrow\quad \text{Exposure}_{\text{BCB}} = \text{Exposure}_{\text{correct}} + \underbrace{(\log_2 4^{64}-\log_2 1000)}_{\mathbf{118.034\ \text{bits}}}$$

**A constant additive offset of 118.034 bits on every canary, every model, every dataset.** Three consequences:

1. **Rank ordering is preserved; absolute values are meaningless.** Between-configuration comparisons survive; every absolute exposure number is inflated by 118 bits.
2. **The null baseline moves from 1 bit to 119.03 bits.** Under no memorization, median rank $=(n{+}1)/2=501$, so $\text{Exposure}_{\text{BCB}}=128-\log_2 501=119.03$. **Under BCB's formula, "119 bits" means "no memorization at all."** A reader applying SS19's stated null (median 1) or Jagielski's (mean ≈1.44) to a reported 120 would conclude near-total memorization when the chance-corrected signal is ≈1 bit.
3. **The claimed information content is unsupportable by the experiment.** Exposure $=128$ asserts a $3.4\times10^{38}$-fold reduction in adversary guesswork. An experiment against 1,000 alternatives can support at most $\approx10^3$-fold. The metric asserts $10^{35}$ times more evidence than the measurement contains.

**An independent, additional defect.** SS19 Theorem 1's estimator requires $t\sim\mathrm{Uniform}(\mathcal{R})$. Beam-search candidates come from the model's own high-likelihood tail. That set is **not exchangeable** with the canary, so even the *corrected* $\log_2(1000)$ estimator would be biased (downward on exposure), and the uniform null on rank does not hold.

**The fix is one line** — use $\log_2 n$ — or, better, SS19 §4.3's skew-normal extrapolation estimator, which is directly applicable to 64-nt canaries and costs the same 1,000 forward passes already being spent. Or, as Truth Serum §6 did, shrink $\mathcal{R}$ so it can be enumerated.

**One mitigating finding, which changes how this should be framed.** **No numeric exposure values appear in the arXiv HTML** — §4.3.2 says only that the paper *"report[s] extraction success rates and mean exposure scores disaggregated by repetition tier,"* and the extractable tables are perplexity/gap-ratio tables. If no exposure numbers were ever printed, the 118-bit offset is a **latent defect in the code and in the paper's Eq. (1)**, not a published wrong number. **Check the ACM DL version (DOI 10.1145/3807503.3819470) before asserting what was published.**

**The strongest single citation for this objection** is Jagielski, *A Note On Interpreting Canary Exposure* (arXiv:2306.00133) — a Google DeepMind primary source, by an author of C21/C23, stating in print that with $n$ references the normalizer is $\log_2(n)$, that the no-memorization rank is $1+n/2$ giving exposure ≈1, and that the mean under random guessing is $1/\ln 2\approx1.4427$. It is short enough that the student can read it in ten minutes.

## 6.3 Extraction

**Is the metric sound?** The metric BCB uses is **not** either of Carlini's extraction definitions. This is a **misapplication**, not a bug.

- **C21 Definition 1:** $s\leftarrow\arg\max_{s':|s'|=N} f_\theta(s'\mid c)$. C21 uses likelihood only as a *filter over generations*, and found it weak (9%/3% vs 67% zlib-calibrated). **C21 is primary-source evidence against using an uncalibrated likelihood as the memorization metric.**
- **C23 Definition 3.1:** $s$ is extractable with $k$ tokens of context if $[p\Vert s]$ is in the training data and $f$ **produces $s$ from $p$ under greedy decoding**. Exact string match. **No candidate set, therefore no chance floor** — a 32-nt suffix matched by chance has probability $4^{-32}\approx5\times10^{-20}$.
- **Neither paper uses exposure.** Exposure belongs to SS19 and its descendants.

**BCB's criterion.** Rank the true canary against candidates and count success at rank $\le100$. **This threshold does not appear anywhere in the paper text** — $s_{\text{ext}}$ is defined only as *"the fraction of canary sequences successfully recovered via beam search."* **The operative definition exists only in code.** That is itself a finding.

**The chance floor is exact, not approximate.** Under exchangeability of the canary with $n$ decoys and no ties, $\mathbf{rank}\sim\mathrm{Uniform}\{1,\dots,n{+}1\}$, so
$$\Pr[\mathbf{rank}\le k]=\frac{k}{n+1}, \qquad \Pr[\mathbf{rank}\le100]=\frac{100}{1001}=\mathbf{0.0999001}$$

> **Off-by-one to check in the code.** If the repo's `rank` counts $\#\{\text{decoys scoring}\le\text{canary}\}$ (range 0..1000) rather than SS19 Definition 2 (range 1..1001), then `rank <= 100` admits 101 outcomes and $p=101/1001=0.1009$. One percentage point on a quantity that is itself ~10%.

**The statistical power situation is far worse than "8–12% straddles chance."** With 25 canaries per tier and $p=100/1001$:
- successes: mean 2.4975, **SD = 1.4993 canaries**
- rate: **SD = 6.0 percentage points**

| observed | rate | $\Pr[X\ge k]$ under the null |
|---|---|---|
| 2 | 8% | 0.728 |
| 3 | 12% | 0.462 |
| 4 | 16% | 0.236 |
| 5 | 20% | 0.098 |
| **6** | **24%** | **0.033** |
| 8 | 32% | 0.0023 |

**Central ~95% range of the observed rate under pure chance: 0% to 24%.** The smallest one-sided-significant count at $\alpha=0.05$ is **6/25 = 24%**.

Therefore, of BCB's reported extraction numbers:
- SimpleDNALM single-insertion **8–12%**: indistinguishable from zero.
- DNABERT-2 flat **12–15%** (reported as "resistance"): indistinguishable from zero.
- HyenaDNA **18%**: indistinguishable from zero. Even 20% gives $p=0.098$.
- **Only the high-repetition tiers (88–100%, and Evo's 100% on real data) carry signal.**

Two conditions that void this null entirely and must be checked: **(a) independence across canaries** — if all 25 are ranked against one shared decoy set, successes are positively correlated and the true SD exceeds 6.0 pp; **(b) exchangeability** — if candidates come from beam search rather than uniform random DNA, $\mathrm{Uniform}\{1..1001\}$ does not hold at all and 100/1001 is not the floor. Additionally, a **leaky scorer breaks exchangeability**, so the DNABERT-2 scoring bug must be fixed before any null is trusted.

> **Unresolved discrepancy, flagged for the student.** BCB §4.3.2 describes **beam search** (width 10, ≤1,000 candidates). The repo, per the brief, ranks against **1,000 uniformly random candidates**. These are materially different estimators with different nulls. **Resolve against the code before writing anything about this.**

**BCB's scaling-law transfer claim fails on three counts.** §5.2 claims SimpleDNALM's monotonic rise *"directly confirm[s]"* that Carlini's duplication scaling laws extend to genomics:
1. **The anchor point is uninformative.** The single-insertion tier sits at chance; only the ceiling is measured. Chance-correcting would make the trend *steeper*, so the direction likely survives — but the origin is not measured.
2. **DNABERT-2 is the exact case C23 says the duplication law does not hold for.** C23 had to change the memorization definition outright for T5 (perfect masked-task solution instead of prefix→suffix), found absolute memorization an order of magnitude lower (T5-XL 3B 3.5% vs GPT-Neo 2.7B 53.6%), and reported a *statistically significant non-monotonic inversion* with duplication. **BCB's flat DNABERT-2 result is not evidence about DNABERT-2's memorization; it is evidence that a prefix-continuation metric was applied to a model with no prefix-continuation semantics** — same root cause as the scoring bug. *(Note: C23 **does** reproduce the model-**scale** trend for T5; only the duplication relationship breaks.)*
3. **The metric is not C23's metric**, so "Carlini's law transfers" is a claim about a different dependent variable.

**The clean fix.** Port C23 Definition 3.1: greedily decode from a $k$-nt prefix of the canary and check exact match of the remaining $64-k$ nt. That is Carlini's own definition, it is cheap, and **its chance floor is effectively zero.** The whole 10%-floor objection disappears rather than needing a correction term.

## 6.4 Membership inference

**Is the metric sound?** Loss/likelihood as a membership signal is licensed by Yeom Theorem 2 ($\mathrm{Adv}^M=R_{\text{gen}}/B$, an equality) and by Sablayrolles et al. (Bayes-optimal MI depends on the model only through the loss). **The quantity is fine.**

**Is BCB's implementation faithful?** **No — and the problem is a naming error on top of a methodological one.**

BCB §4.3.4, verified verbatim: *"We employ a likelihood-ratio attack that fits parametric distributions to the training and test loss populations and classifies membership based on the resulting likelihood ratio."*

**There are no reference models and no per-example null.** Fitting two parametric distributions to the *aggregate* train-loss and test-loss populations and thresholding the ratio is a **monotone reparameterization of a global loss threshold** — i.e. **Yeom et al.'s Adversary 1, the LOSS attack**, the exact attack Carlini et al. built LiRA to replace. Calling it LiRA is a citation error a reviewer will find.

Compounding this, BCB reports **AUC only (0.70–0.79**, highest Evo(LoRA)/*E. coli* 0.79±0.02, lowest Evo/GUE 0.70±0.01, all 16 configurations verified**)** — the exact metric Carlini et al. argue against, and via $s_{\text{mia}}=\max(0,2(\mathrm{AUC}-0.5))$ it is literally reporting the Yeom membership advantage under a balanced prior.

**Against the five conditions under which a likelihood-based membership signal is trustworthy, the non-canary MIA satisfies none of 1–4:**

| Condition | BCB non-canary MIA |
|---|---|
| 1. The null is samplable (reference models / canaries / checkpoint ordering) | ❌ Neither |
| 2. Members and non-members exchangeable (randomized before training, blind baseline at chance) | ❌ Not demonstrated |
| 3. Score calibrated per example ($\tau(x)$, not $\tau$) | ❌ Global threshold |
| 4. Reported at low FPR with log–log ROC | ❌ AUC only |
| 5. Stable under training randomness | ❌ No seed variance reported |

**In fairness — one point in BCB's favour that should be preserved.** Duan et al.'s "MIAs barely work" finding is specifically about **near-single-epoch pretraining on web-scale corpora**, where the generalization gap that Yeom Theorem 2 converts into advantage is near zero. BCB's setup includes **LoRA fine-tuning and repeated canaries**, which is the *opposite* regime — genuinely higher memorization pressure. Fine-tuning MIA is meaningfully easier than pretraining MIA. Duan et al. condemns the *uncontrolled* part of BCB's result, not automatically the result. Say so; it is a real distinction, and it is exactly where a credible canary-based finding could live.

**Separately: "bounded-prior membership privacy" is not in Yeom et al.** Full-text search confirms the only "bounded" in that paper is the bounded *loss* $B$. The notion is **Li, Qardaji, Su, Wu & Yang (CCS 2013)** and **Tramèr, Huang, Hubaux & Ayday (CCS 2015)** — the latter being the advisor's own paper. The distinction from AUC:

| | Bounded-prior membership privacy | AUC / Yeom advantage |
|---|---|---|
| Quantity | **Posterior/prior ratio** for a specific individual | Rank-ordering quality over a population |
| Direction | **Worst-case** over all $t$, all outputs, all priors in the family | **Average-case** over a paired sample |
| Prior | Explicitly modeled and bounded ($a\le p\le b$) | Silently fixed at $1/2$ |
| Object | A **guarantee on the mechanism**, holds for every adversary | A **measurement of one attack** |
| Answers | "How much can anyone's belief about *this person* move?" | "Can an attack rank members above non-members on average?" |

Two attacks with identical AUC can have wildly different worst-case posterior shifts. **AUC cannot be converted into a privacy guarantee; bounded-prior MP is one.** *(The formal $\varepsilon/\delta$ statement could not be retrieved — ACM DL 403, EPFL Infoscience 429, author-site PDF 404. Get the PDF from Ayday; he is an author.)*

## 6.5 Summary verdict

| Metric | Is the metric sound? | Is BCB's use faithful? | Classification |
|---|---|---|---|
| **Perplexity, causal models** | ✅ Yes | Mostly — needs $\bar k$ audit and bits-domain aggregation | *Implementation needs auditing* |
| **Perplexity, DNABERT-2** | ✅ Yes for causal LMs only | ❌ No | **Metric misapplied** *(a masked LM has no perplexity)* **+ implementation broken** *(self-conditioning)* |
| **Exposure** | ✅ Yes (SS19 Def. 4) | ❌ No | **Implementation broken** — mixes $\log_2\vert R\vert$ with a rank from ≤1,000; $+118.034$ bit constant offset; null moves 1 → 119.03. **One-line fix.** *Possibly latent — no exposure numbers found in the published text.* |
| **Extraction** | ✅ C21/C23 definitions are sound | ❌ No | **Metric misapplied** — neither C21 argmax nor C23 $k$-extractability; rank-based criterion with a 10% chance floor, defined only in code; applied to a masked model that C23 explicitly excludes |
| **MIA** | ✅ Yes (Yeom Thm 2) | ❌ No | **Metric misapplied + misnamed** — a global loss threshold (Yeom Adversary 1) presented as LiRA; no reference models, no per-example null, AUC-only reporting |

---

# 7. THE CHECKLIST

What the student's own evaluation must include to survive review at a 2027 ML or security venue.

## 7.1 Scoring correctness — CI assertions that fail the build

1. **Uniform-random floor test, causal models.** Held-out iid uniform DNA $\Rightarrow$ $\mathrm{PPL}_{\text{nt}}\ge3.999$ for every causal model, with the empirical CI reported. Any value below fails.
2. **Uniform-random floor test, PLL scorers — corrected.** For single-nucleotide masking, assert $\ge4.0$. **For BPE token-level masking, the assertion is $\mathrm{PPPL}_{\text{nt}}\ge 2^{H^-_{\text{tok}}/L}$**, with $H^-_{\text{tok}}$ measured from DNABERT-2's real tokenizer: sample uniform 256-nt strings, tokenize, and for each masked position count $\#\{v\in\mathcal{V}: \text{insertion re-tokenizes canonically to the same context at total length 256}\}$; average $\log_2$ of that count, divide by 256. **Do not assert 4.0 for token-level PLL — it will fail on a correct implementation.** *(Best alternative: mask at single-nucleotide resolution, which restores the 4.0 floor exactly.)*
3. **Normalization test.** At each scored position, the four conditional probabilities over $\{A,C,G,T\}$ sum to 1.000.
4. **Sequence-normalization brute force.** On $\mathcal{V}=4$, $L=8$ (65,536 sequences), $\sum_x\prod_i q(x_i\mid\cdot) = 1.000$. Cheap and decisive.
5. **Mask-leakage test.** Re-score with the target position masked/removed; perplexity must rise. No change $\Rightarrow$ leakage.
6. **Padding test.** Report the scored-position count alongside every perplexity; assert it equals the nucleotide count.
7. **Unit test.** Every reported perplexity is per-nucleotide ($2^{\mathrm{BPN}}$, $\mathrm{BPN}=$ total NLL in bits / total nucleotides), never per-token. Measure $\bar k = \sum_j L_j/\sum_j T_j$ **separately per dataset**.
8. **Aggregation test.** Corpus perplexity is $\exp(-\sum_j\log q(x^{(j)})/\sum_j L_j)$, never a mean of per-sequence perplexities.
9. **Stride/window test.** Identical windowing, stride and batching for train and test; report the stride.
10. **0-order baseline test.** Report each model against $2^{H_0}$ for the same sequence's base composition (3.935 human, 3.999 *E. coli*). "Learned something" means beating this, **not** beating 4.0.
11. **Shuffle test.** Shuffle each test sequence; perplexity must rise to $\approx2^{H_0}$. If it doesn't, the model isn't using order and the score is composition.

## 7.2 Mandatory — omission is a desk-level objection

- [ ] **Blind baseline.** Bag-of-$k$-mers ($k=3..6$), plus GC and repeat-content classifiers, trained on the member/non-member split with **no model access**. Report AUC and TPR@1%FPR beside every attack number. If it is not ≈0.5, the split is broken and no attack number is interpretable. (Prediction to test: BCB's AUC 0.70–0.79 implies $\alpha=0.40$–$0.58$ trivially-separable members.)
- [ ] **Log–log ROC + TPR@{1%, 0.1%}FPR** for every attack. AUC may appear but never alone.
- [ ] **A real per-example null.** One of: (a) $N\ge16$ reference models with a documented IN/OUT assignment per example; (b) planted canaries; (c) **the CheckMIABench checkpoint-ordering construction** — data seen just before and just after a checkpoint is same-distribution by construction, so for SimpleDNALM, where you control training, simply log the data order. Cheapest and cleanest available. State which and give $N$.
- [ ] **Randomized membership assignment made before training**, with split procedure and seed published.
- [ ] **Seed variance.** $\ge3$ training seeds; report the **per-example decision flip rate**, not just mean ± sd of AUC (Hayes et al.).
- [ ] **Rename the attack.** A two-distribution fit to aggregate train/test losses is the **LOSS attack (Yeom et al. Adversary 1)**, not LiRA.
- [ ] **Confidence intervals** on AUC and TPR@lowFPR, bootstrapped over examples *and* over seeds.
- [ ] **Fix exposure.** Use $\log_2 n$ with $n$ = the actual candidate count, or SS19's skew-normal extrapolation, or enumerate a shrunken $\mathcal{R}$ (Truth Serum §6). Never mix $\log_2|\mathcal{R}|$ with a sampled rank.
- [ ] **Fix extraction.** Replace rank $\le100$-of-1,001 with C23 $k$-extractability (greedy decode from a $k$-nt prefix, exact match of the remaining $64-k$ nt). Chance floor ≈0. If you keep a ranking criterion, report the chance floor beside every number and the exact binomial null.
- [ ] **Report the empirical null, not just the analytic one.** Run the identical pipeline on **held-out canaries that were never inserted** (Jagielski's reference set; "decoy probes" in Fan et al. 2026). The gap between inserted and held-out canaries *is* the memorization signal. This alone would have caught the extraction floor.
- [ ] **Never table PPPL beside causal PPL.** Use Option 2 (prefix-only conditioning for all models) as the primary fix.

## 7.3 Strongly expected

- [ ] **Difficulty calibration ablation:** raw loss vs $s - \mathbb{E}_{\text{ref}}[s]$ (Watson et al.), showing how much of the raw signal is difficulty. Expect the uncalibrated number to be an **under**estimate (Truth Serum: 3.1 → 7.1 bits; 0.1% → 10% recovery).
- [ ] **Genomics-grade compressor control.** Divide by GeCo3 / JARVIS / XM bits-per-nt for the same sequence — the correct DNA substitute for zlib, which does not port.
- [ ] **Entropy-matching audit.** Apply $\Delta\mathbb{E}[-\log q] = \Delta H + \Delta D$ explicitly. Match member/non-member sets on GC content, repeat fraction (RepeatMasker), sequence length, chromosome, assembly build and organism. Report matched as primary, unmatched as a shift demonstration.
- [ ] **Split integrity.** Split by chromosome; if individuals are involved, by individual with a kinship check. Report the repeat fraction of each split. Exclude or separately report runs of `N` and soft-masked regions.
- [ ] **Check Kauf–Ivanova within-token leakage** separately — BPE makes DNABERT-2 vulnerable to it even after the causal-mask fix.
- [ ] **Canary independence.** Confirm each canary is ranked against its own decoy set, or widen the reported SD.
- [ ] **Multiple-testing control** if screening many candidate sequences.
- [ ] **$\varepsilon$ lower bound** via $\varepsilon\ge\ln(2)(\mathrm{Exposure}(c_{\text{median}})-1)$, with sampling-error correction **and division by the duplication count via group privacy** — this directly affects the 1/5/10/20 repetition tiers.
- [ ] **Report the median**, not the mean, across canaries (Jagielski: less outlier-sensitive; median's random-guessing baseline is exactly 1).

## 7.4 Framing advice

The defensible core of the BCB framework is the **canary track**. Zhang et al. (SaTML 2025) explicitly name canary-based membership inference and extraction as the two methods that escape the unsamplable-null problem. **Lead with canaries; treat the natural-sequence MIA as a controlled negative rather than a headline.**

Given §4, *"under a shift-free design, membership inference on genomic LMs performs at chance except for repeated canaries"* is a **more publishable and more defensible** claim in 2027 than AUC 0.79 with no controls. CheckMIABench and Jebreel et al. are proof that the venues reward this.

## 7.5 The three things to do before anything else

1. **Establish whether BCB's 2.69 is per-token or per-nucleotide.** It decides whether the floor argument works at all. If per-token with $k\approx2.5$, the implied per-nt figure is 1.47, below even the erasure floor, and the bug conclusion is airtight.
2. **Compute DNABERT-2's real erasure-entropy floor from its tokenizer** — no model required, one afternoon. That number, not 4.0, is the correct CI assertion for token-level PLL.
3. **Replace the sigma argument with the no-hypercompression bound** in everything written down. $\Pr[\text{deficit}\ge\delta] \le 2^{-n\delta}$ is exact, assumption-free, and gives $10^{-8822}$ where a CLT gives an uninterpretable "202σ."

---

# 8. WHAT REMAINS UNVERIFIED

**No citation in this document was fabricated.** The two 2026 arXiv references flagged by an earlier automated pass as possibly hallucinated — **arXiv:2605.22981** (von Arx & Dieudonné, *Memorization Dynamics of Fill-in-the-Middle Pretraining*, MemFM @ ICML 2026) and **arXiv:2605.24173** (Wang & Asokan, *Extracting Training Data from Diffusion Language Models via Infilling*) — are **both genuine**, confirmed through the arXiv API with matching titles, authors, categories and submission dates.

## 8.1 Verified to exist, but contents not read

1. **Jelinek et al. 1977 abstract body.** DOI, volume/issue/page and indexed abstract content verified; the typeset abstract text is unread (AIP returns HTTP 403).
2. **Bahl, Jelinek & Mercer 1983.** Metadata verified; the perplexity equation in the body is unread. Do not cite it *for the equation* without checking.
3. **Carlini et al. LiRA (S&P 2022) body.** Metadata and pagination verified. **The 59.5%-vs-53.5% accuracy inversion, the logit-rescaling formula, and the global-vs-per-example variance discussion were not re-read from the PDF.**
4. **Watson et al. (ICLR 2022)** CIFAR-10 AUC figures 0.663 → 0.676 — not re-checked.
5. **Cao & Rimell (EMNLP 2021)** "0.9–1.9% perplexity improvement out-of-domain" — not re-checked.
6. **von Arx & Dieudonné** and **Wang & Asokan** body claims (linear growth with repetitions, prefix anchoring, "up to three times more verbatim sequences," email-recall comparison) — existence and metadata verified; findings not re-read.
7. **Shannon 1951** — metadata only.
8. **Evo (Science 2024)** — Crossref metadata verified; single-nucleotide byte-level tokenization confirmed from the Arc Institute / bioRxiv description, not the *Science* text itself.
9. **Goyal et al. (ICLR 2022)** critique of Wang & Cho — verified from the abstract and secondary sources; full text not read.

## 8.2 Could not be retrieved at all

10. **Li et al. (CCS 2013) formal $\varepsilon/\delta$ statement of positive membership privacy.** ACM DL not fetched. The author list is now corrected; the definition in §6.4 is a **structurally faithful paraphrase, not a verified quotation.**
11. **Tramèr, Huang, Hubaux & Ayday (CCS 2015) formal bounded-prior theorem.** ACM DL 403, EPFL Infoscience 429, author-site PDF 404. **Get the PDF from Ayday before writing the formal statement.**
12. **DNABERT-2's average token length $k$.** No published value exists that could be found. **Measure it empirically, per dataset.**
13. **BCB '26 exposure numeric values.** None found in the arXiv HTML. **Check the ACM DL version (DOI 10.1145/3807503.3819470)** before asserting what exposure values were published. This determines whether the 118-bit offset is a published wrong number or a latent code defect — which changes how you frame it.

## 8.3 No source exists

14. **Any pre-1977 primary use of "perplexity"** in this technical sense. Not found. The underlying quantity is Shannon (1948) restated; priority on the *name and its use as an LM evaluation metric* is Jelinek's.
15. **Any peer-reviewed paper naming "padding contamination" as a perplexity pathology.** Convention-level only. Cite the HuggingFace `-100` masking convention as an implementation requirement, not a literature finding.
16. **Any formal treatment of matched conditioning for cross-architecture memorization comparison.** Genuine gap; plausibly the extension's contribution.

## 8.4 Our own derivations, attributable to no source

17. **Erasure entropy $=$ the population optimum of PLL.** Follows in two lines from Verdú & Weissman's verified Definition 1 and Theorem 1 plus Gibbs, but no paper states it. **Present it as a derivation.** It is also the most novel result in this audit.
18. **The BPE erasure-entropy floor for token-level PLL** (≈1.31–1.41 bits/nt, $\mathrm{PPPL}_{\text{nt}}$ ≈2.47–2.66). Computed here on BPE vocabularies trained on random DNA. **The DNABERT-2-specific number must be measured from DNABERT-2's actual tokenizer** — the vocabularies used here are not DNABERT-2's.
19. **The no-hypercompression bound as applied here.** The inequality itself is elementary (Markov on $q/p$) and is commonly attributed to Barron in the MDL literature; **the specific Barron citation was not verified in this pass.** The two-line proof given in §5.3 is self-contained, so the result does not depend on the attribution — but do not cite Barron without checking.
20. **The $\mathrm{AUC}=(1+\alpha)/2$ / $2(\mathrm{AUC}-0.5)=\alpha$ identity and the symmetric-confound variant** (0.8615). Elementary; ours.
21. **The observation that $\bar k$ is corpus-dependent** (BPE produces shorter tokens on random DNA than on real DNA, so DNABERT-2's conversion constant differs per dataset). Ours; not from any source.
22. **The 0-order baselines** (human 1.9765 bits / PPL 3.9353; *E. coli* 1.99980 / 3.99889), the **GeCo3 bits-per-base conversions** (1.879 *E. coli*, 1.580 chr4), and **$f_{\text{pad}}\approx0.286$**. Our arithmetic.
23. **The blind bag-of-$k$-mers proposal for DNA.** Das et al.'s method transplanted; ours.

## 8.5 Corrections applied to the ground reports — consolidated

| # | Original claim | Corrected |
|---|---|---|
| 1 | Li et al. CCS 2013 authors include "Jianneng Cao" | **Ninghui Li, Wahbeh Qardaji, Dong Su, Yi Wu, Weining Yang**, pp. 889–900 |
| 2 | "Do not cite a DOI for Jelinek 1977" | **DOI 10.1121/1.2016299 is real and resolves.** Keep the meeting-abstract caveat |
| 3 | BCB Table 4 synthetic PPLs 3.82–4.00 put "clean" models under the floor | **Unsupported.** SimpleDNALM held-out synthetic is exactly **4.00**; 3.93/3.91 are train/canary; 3.82–3.86 are real-genome rows. Only 2.69 is anomalous |
| 4 | JARVIS/GeCo2/XM digits | **HoSa 1.6265 / 1.6346 / 1.6383; EsCo 1.8876 / 1.8949 / 1.9091; ScPo 1.8925 / 1.8940 / 1.8951.** Errors up to 0.008 bits. ScPo = *S. pombe*, not *S. cerevisiae* |
| 5 | GeCo3 human chr4 = 37.89 MB → 1.594 bits/base | **37.56 MB → 1.580 bits/base** |
| 6 | HyenaDNA PPL 2.9–3.3 | **≈2.9–3.15**; Transformer ≈3.0–3.15. Nothing reaches 3.3 |
| 7 | CheckMIABench: no attack significant across 70M–7B | **Scoped 70m–2.8b.** Its WikiMIA blind figure is TPR 94.7% **@ 55% FPR** — not Das et al.'s TPR@5%FPR |
| 8 | Sablayrolles author order (arXiv) | Published PMLR order: **Sablayrolles, Douze, Schmid, Ollivier, Jégou** |
| 9 | Yeom et al. cited as IEEE S&P 2017 (arXiv comments field) | **IEEE CSF 2018, pp. 268–282.** The arXiv metadata is wrong |
| 10 | "Carlini's scaling laws don't hold for masked LMs" | C23 **does** reproduce the *model-scale* trend for T5; only the **duplication** relationship is non-monotonic |
| 11 | Finite-sample dip below the floor is $O(1/\sqrt N)$ | **$O(1/N)$** — $z^2/(2n\ln2)$ bits. Off by $\sqrt n\approx226$ |
| 12 | "The 4.0 floor does not apply to PLL" | **Wrong for single-nucleotide masking** (per-position Gibbs gives it exactly). **Right for BPE token-level masking**, but for a reason no report gave |
| 13 | PLL per-token floor is $4^k$ | **Wrong** — measured 10–24, far below $4^k$ = 34–94 |
| 14 | Global normalization $\sum_x q(x)=1$ is a necessary condition for the floor | **Sufficient only.** Necessary condition is per-position normalization + no self-conditioning |
| 15 | "By Jensen, mean of per-sequence PPLs $\ge$ corpus PPL" | **True only at equal lengths.** Reverses at unequal lengths |
| 16 | MLE↔KL justified by Cover & Thomas Thm 11.1.2 | **Method of types requires memoryless $Q$.** Use the elementary sequence-level decomposition instead |
| 17 | Sigma equivalent of 2.69 is $10^2$–$10^3$ | **85σ–202σ**, all $10^2$; the smaller $n$ gives the *smaller* $z$ |
| 18 | 10% extraction floor: "the low end straddles chance" | **With 25 canaries, nothing below 24% is distinguishable from chance** at $\alpha$=0.05 |
| 19 | Salazar et al. say PPPL "is not directly comparable to autoregressive perplexity" | **They do not.** They say *"PPPLs are only comparable under the same subword vocabulary."* The incomparability argument is ours |
| 20 | Flags now **closed** | HyenaDNA is causal next-token (body-verified); Evo is single-nucleotide byte-level, $k=1$; Du et al. ACL 2023 is real (pp. 9744–9770); Torroba Hennigen & Kim arXiv:2305.15501 is real (ACL 2023, pp. 1149–1159); Tirumala et al. is NeurIPS 2022; Kouam et al. is CCS 2026; arXiv:2603.19375 is TMLR'26; arXiv:2503.19338 is an **unrefereed preprint**; Verdú & Weissman is 54(11):**5030–5058** |

---

## Scratch artifacts

Full extracted text of the primary sources, for re-checking any quotation:
- `C:\Users\ZYQ\AppData\Local\Temp\claude\E--OneDrive---Case-Western-Reserve-University-PhD-Research-GLM-Collaboration-Extensions\b73d3a18-27f9-4f6c-a0fd-0a12258228b1\scratchpad\gr2007.txt` — Gneiting & Raftery 2007
- `C:\Users\ZYQ\AppData\Local\Temp\claude\E--OneDrive---Case-Western-Reserve-University-PhD-Research-GLM-Collaboration-Extensions\b73d3a18-27f9-4f6c-a0fd-0a12258228b1\scratchpad\shannon1948.txt` — Shannon 1948
- `C:\Users\ZYQ\AppData\Local\Temp\claude\E--OneDrive---Case-Western-Reserve-University-PhD-Research-GLM-Collaboration-Extensions\b73d3a18-27f9-4f6c-a0fd-0a12258228b1\scratchpad\cover_thomas.txt` — Cover & Thomas 2nd ed.