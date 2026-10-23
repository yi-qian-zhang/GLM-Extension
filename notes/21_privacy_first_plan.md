# Privacy-first restructure / 隐私主线重构

Erman settled the framing on 19 Oct: **the paper is a privacy paper**, and the tokenisation and
measurement work is the vehicle that makes the privacy claims believable, not the contribution.
This file is the plan for that turn. It supersedes the ordering in `18_paper_outline.md` §2, which
was written objective-first; the evidence rows there are still valid except where marked below.

Erman 在 10/19 定了主线：**这是一篇隐私论文**，切法与测量方面的工作是让隐私结论可信的载体，不是
主贡献。本文件是这次转向的方案，取代 `18_paper_outline.md` §2 的排序（那份是目标函数主线写的）；
那里的证据行仍然有效，除非下面标注为已撤回或已被取代。

---

## 1. Why the order changes / 为什么要换顺序

The old spine asked *what makes a genomic language model memorise* and answered with a factor
decomposition. Under that spine the strongest result in the paper — that a released model will
identify an individual while reproducing nothing — arrives in section 7 as a consequence.

The privacy spine asks *what happens to the people in the fine-tuning set*, and the answer is a
ladder: released models leak; they leak at a quality you would ship; they identify people even
where they leak nothing; the number you would use to catch this does not move; and the one
defence that works has a margin of three hundredths of a bit. Tokenisation enters as the
explanation for why some models look safe, and measurement enters as the reason the field has not
noticed.

旧的主线问"是什么让基因组语言模型记住"，用因子分解回答。在那条主线下，全文最强的结果——公开模型
一个字都不吐却能指认个体——要到第 7 节才作为推论出现。隐私主线问"微调集里的人会怎样"，答案是一个
阶梯：公开模型会漏；在你会接受的质量下漏；在一个字都不吐的地方仍能指认；你用来发现这件事的指标
不动；唯一有效的防御余量只有 0.03 bit。切法进来是为了解释为什么有些模型看起来安全，测量进来是为了
解释为什么领域此前没发现。

---

## 2. Page budget, 10 pages including every figure, table and caption

| § | Content | Pages | Figures / tables |
|---|---|---|---|
| 1 | Introduction: the threat, and the five findings as a list | 1.00 | — |
| 2 | Background: released GLMs, fine-tuning on cohorts, prior memorisation work | 0.75 | — |
| 3 | Threat model, data, and what we measure | 1.25 | F1 (probe + the three decoders) |
| 4 | **Released models leak at a quality you would ship** | 1.75 | F2 (cost vs leak), T1 (per checkpoint) |
| 5 | **Identification without reproduction** | 1.50 | F3 (identification vs verbatim, 3 seeds) |
| 6 | **What decides whether the leak is reachable**: slot count | 1.50 | F4 (slot-count curve at matched loss) |
| 7 | **What a practitioner can do**, and why the usual metric will not help | 1.25 | F5 (task score vs leakage) |
| 8 | Limitations and discussion | 0.75 | — |
| | *slack* | 0.25 | |

Five figures is already 1.25–1.5 pages of the ten. If the draft overruns, F1 is the one to cut
first — the probe geometry can be described in three sentences. F4 is load-bearing and cannot
move to the appendix: it is the only place the tokenisation claim is made.

五张图已经吃掉十页里的 1.25–1.5 页。超了的话先砍 F1（探针几何三句话能说清）。F4 是承重的，不能进
附录——切法那条结论只在那里成立。

---

## 3. Abstract, privacy-first / 摘要（隐私主线）

Draft, ~200 words. Every number is one we have measured on one basis; nothing here is pending.

> Genomic language models are released pretrained and fine-tuned locally, increasingly on cohort
> data. We ask what happens to the individuals in that cohort, and measure it on six released
> models rather than on a backbone of our own.
>
> Every released masked checkpoint we tested reproduces planted records verbatim at a held-out
> loss a practitioner would accept: the cheapest costs seven thousandths of a bit and returns 30 %
> of records. On real chromosome-22 haplotypes, each carried by at most five people in 2,548, a
> record present as a single copy comes back letter for letter about one time in ten.
>
> Reproduction is the wrong alarm. At checkpoints where verbatim extraction reads exactly zero in
> every seed, the same model ranks one individual's haplotype first against a hundred real rare
> segments seven to eight times out of ten, with none of 150 never-trained segments ever
> identified. Downstream task score moves one to two per cent across the same range.
>
> Whether a memorised record can be reached at all is set by how many token slots it occupies, not
> by how much the model knows: models that differ only in tokenisation answer any single hidden
> nucleotide identically and yet return 91 % or 0 % of whole records. No single extraction test is
> correct across tokenisers, which is why this has been missed.

**中文要点**（不进论文，供对讲稿用）：六个公开模型；最便宜的泄漏 +0.007 bit 换 30%；真实 chr22
单倍型单份记录约十分之一被逐字还原；在逐字提取恒为 0 的 checkpoint 上识别率 0.7–0.8，对照 0/150；
下游分数只动 1–2%；能不能取出来由槽数决定而非知识量，同知识下 91% 对 0%；没有单一测法跨切法成立。

---

## 4. Claim-to-evidence map, privacy-first / 结论与证据对照（隐私主线）

Log sections refer to `17_experiment_log_week3_EN.md`.

| # | Claim | Evidence | Log | Status |
|---|---|---|---|---|
| **P1** | Every released masked checkpoint tested reproduces planted records at a loss a practitioner would accept | DNABERT-2 +0.007 bits → 30 %; NT 250M +0.03 → 8/8/14 % over three seeds; NT 500M +0.46 → 78 % | 3.55, 3.58(e) | released, one basis |
| **P2** | On real human haplotypes a single copy is enough | NT 250M 8 %, NT 500M 12 % verbatim at single copy, chr22, ≤5 carriers of 2,548 | 3.51, 3.56 | released |
| **P3** | Identification runs far ahead of reproduction | DNABERT-2 chr22, 3 seeds: identification 0.70/0.80/0.80 at round 120 with verbatim 0.00 everywhere; control 0 of 150 | 3.55, 3.56 | released |
| **P4** | Slot count, not knowledge, decides reachability | matched-loss curve, slots 48/24/16/12/8 → 0/0/0/2/65 % at floor 2.20; both 6-mer and 3-mer answer a single hidden nucleotide 100 % | 3.58(f), 3.1 | controlled + released negative control |
| **P5** | The released DNABERT family shows no k trend, exactly as the slot account predicts | k = 3/4/5/6 overlapping, slot count ≈48 throughout → 10/0/10/0 %, per-letter knowledge 0.99–1.00 | 3.54 | released, prediction made before measuring |
| **P6** | Stopping at the held-out optimum works, with a 0.03-bit margin | at the optimum the leave-one-out probe sits at the never-trained control level; +0.03 → 8–14 % across three seeds | 3.53, 3.58(e) | released |
| **P7** | The metric practitioners select on is blind to all of this | NT chr22: MCC 0.802 → 0.780 while single-copy identification 0.04 → 0.35; DNABERT-2: MCC moves 1.1–1.5 % while identification 0 → 0.94 | 3.58(a,b) | released |
| **P8** | No single extraction test is correct across tokenisers | same checkpoint reads 0 % or 95 % by test; standard test under-reports ~2× on fixed-width, our decoder reads 0 on overlapping and BPE | 3.54 | released |

### Retired or demoted / 已撤回或降级

- **RETIRED.** "The maximum of the downstream score is a checkpoint that already leaks 20 %."
  It came from the `n_train=2000` smoke probe. The full probe has MCC declining monotonically with
  its maximum at a checkpoint whose single-copy identification is 0.00. See 3.58(b). The stronger
  claim survives on NT instead (P7). **Slide 50 of the 1016 and 1019 decks still carries the
  retired wording.**
- **CORRECTED.** Finding-1's near-optimum row: "standard 0 % vs ours 10–25 %" is, on one basis at
  n = 50, **standard 4–8 % vs ours 8–14 %**. See 3.58(e).
- **DEMOTED.** Old C1 (objective is the largest single factor, 57.7 % of variance). A variance
  decomposition cannot be run on a model somebody else trained, so it is toy-only. Keep it as a
  framing sentence in §2 or §8, not as a headline.
- **DEMOTED.** Old C15 (the character tokeniser removes leakage at no cost). HyenaDNA is a
  released single-nucleotide model at 14.24M — the same size as our 12.9M backbone — and extracts
  95 %. The claim is only true within one architecture and one objective, and must be stated that
  way.

### An apparent contradiction to resolve before writing §6

Old C4 says the mechanism is **token rarity, not slot count** (per-slot spread to 40×; canary-token
corpus counts 287,995 / 6,014 / 400 / 47). P4 says the mechanism is **slot count**. These answer
different questions and the paper must say so in one sentence, or a reviewer will read a
contradiction:

- rarity governs **how much is stored per slot** — the bits ruler, old C2/C4;
- slot count governs **whether what is stored can be pulled out whole** — the extraction ruler, P4.

A coarse tokeniser wins twice: its tokens are rarer, so more is stored per slot, and there are
fewer slots to get right at once. 3.58(f) shows both faces — extraction rises with coarseness
*and* the loss it costs to reach full extraction falls (2.47 / 3.01 / 4.15 bits for 6/4/3-mer).

旧 C4 说机制是**词元稀有度而非槽数**，P4 说是**槽数**。它们回答的是不同问题，论文必须用一句话讲明，
否则审稿人会读成自相矛盾：稀有度决定**每个槽存了多少**（比特尺子），槽数决定**存下来的东西能不能被
整条取出**（提取尺子）。粗切法两头占便宜：词元更稀有所以每槽存得更多，同时槽数更少所以更容易一次
全部猜对。

---

## 5. Required by the venue, not yet done / 投稿硬性要求，尚未完成

- **Public documented repository, link in the paper, by the submission deadline.** Our repo is
  private and `src/`, `experiments/`, `config/` are Alex's. Likely answer: publish `pilot2/` only,
  with a README and attribution to the BCB implementation. Needs a conversation with Alex and has
  lead time.
- **Ethics / responsible-use paragraph.** The paper demonstrates individual identification on
  1000 Genomes. The data is public and consented, but a privacy paper showing re-identification
  needs the paragraph; RECOMB's topic list does not require it and reviewers in this area will
  expect it anyway.
- **Training-set scale is a fixed variable.** Erman asked about it directly on 19 Oct. It is not
  tested and almost certainly cannot be before 4 Nov. It goes in §8 as a stated limitation, with
  the direction left open — the intuition that more data means more memorisation is a guess and
  may well be backwards.
- **Practitioner guidance subsection** (Erman's request, §7): stop at the held-out optimum; know
  the margin is 0.03 bits; know the downstream score will not warn you; prefer tokenisers with a
  higher slot count if the utility cost is acceptable, and re-measure that cost yourself.
