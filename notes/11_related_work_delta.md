# Related work — verified, with our delta

> 英文在上，中文在下。PDF 都在 `related papers/`（文件名 = 第一作者 + 年份 + 标题关键词）。全部在 arXiv 上核实过标题、作者和日期（2026-09-28）。

---

## 1. The one that matters most: Kharitonov, Baroni & Hupkes (2021)

**"How BPE Affects Memorization in Transformers"** — arXiv:2110.02782 (Facebook AI). File: `Kharitonov2021_How_BPE_Affects_Memorization.pdf`

**What they did.**
- NLP Transformers of three kinds: causal LM, MLM (mask 0.2) and an encoder classifier. The LM/MLM are 4 layers, d=512, very close to our backbone.
- Varied: BPE vocabulary size, from 611 to about 20K.
- Memorization measured three ways: fitting random labels, loss-threshold membership inference (AUC), and QA answer recovery.
- **Parameter-count control:** they replace the embedding with an embedding followed by a fully-connected layer. This is exactly our `--emb_rank` factorization.
- They also use **random strings** (incompressible data), which rules out "BPE removes redundancy".
- A "duplicated vocabulary" (synonym-token) experiment rules out vocabulary size on its own. By exclusion, they **conjecture that shorter sequences** cause the effect.

**Finding.** Larger vocabulary → more memorization, for LM, MLM and encoder, and still true under the parameter control.

> **他们做了什么：** NLP 里的三种 Transformer（接龙 LM、完形填空 MLM 掩码 0.2、编码器分类器），LM/MLM 是 4 层、d=512，和我们的骨架非常接近。只改 BPE 词表大小（611 到约 2 万）。用三种方式测记忆：拟合随机标签、按损失阈值做成员推断（AUC）、问答答案复现。**参数量对照**：把嵌入层换成"嵌入 + 全连接层"——和我们的 `--emb_rank` 完全是同一个做法。还用了**随机字符串**（不可压缩的数据），排除了"BPE 去掉冗余"这个解释；用"重复词表"（同义 token）实验排除了"词表变大本身"。靠排除法，他们**猜测**原因是序列变短。
>
> **结论：** 词表越大记得越多，LM、MLM、编码器都成立，控制参数量后仍成立。

**Consequence for us.** "Coarser tokens memorize more" is **not new**. The tokenizer headline alone would be rejected as known. We must cite this paper prominently and build on it.

> **对我们意味着什么：** "切得越粗记得越多"**不是新发现**。如果只拿这一条当主结论，审稿人会直接说"已知"。必须显著引用这篇，并在它的基础上往前走。

**What we have that they don't** (the delta paragraph):

1. **Their parameter control is itself a confound.**
   - Our cap3 shows that a factorized embedding at full rank (512) is the *same function class* as the plain tied embedding, with more parameters.
   - Yet it cuts the 6-mer excess over 3-mer from 0.61 to 1.44 bits/nt at matched overfitting, roughly to the 3-mer level.
   - Their "controlled" and "vanilla" curves therefore differ by parametrization, not only by parameter count.
   - We can show exactly this, on their own style of control. This is a genuinely new methodological point.
2. **"More" vs "sooner".**
   - They measure at a fixed training budget (500 or 100 or 70 epochs).
   - We separate speed from amount by aligning on held-out loss (equal generalization cost). The alignment is schedule-invariant.
   - Result: coarse tokenizers memorize both sooner *and* more.
3. **The objective axis as a factor, not as three separate architectures.**
   - They show that LM, MLM and encoder all follow the vocabulary trend.
   - We vary the objective on one backbone, including a mask-rate dose-response (non-monotone, peak at 0.5), and **decompose variance**: tokenizer 59.5%, objective 25.7%, interaction 14.0%, seed 0.8%.
   - The interaction term and the "present but not extractable" regime of char-level MLM are new.
4. **A calibrated instrument.**
   - Genomic iid data has an *exact* chance floor (2.000 bits/nt). Every metric is per nucleotide, so tokenizers with different sequence lengths are commensurable.
   - Canary repetition tiers, a rank against a random pool, exact prefix extraction, and a null battery.
   - Their metrics are per example (accuracy, AUC), with no floor.
5. **Their mechanism can be tested directly in DNA.**
   - Their conjecture is sequence length. k-mer tokenizers change sequence length *deterministically* (288 / 96 / 48 tokens per window) with no change in the data.
   - Our char → 3mer step is capacity-clean and parametrization-invariant, which is the cleanest test of their length hypothesis anyone has.
6. **Domain and stakes.**
   - Real GLMs use exactly these tokenizers: DNABERT uses 6-mer, DNABERT-2 uses BPE-4096, Nucleotide Transformer uses 6-mer, HyenaDNA and Evo are char-level.
   - The published GLM privacy comparison (Alex's BCB paper) attributes to architecture what our grid attributes mostly to the tokenizer.

> **我们有、他们没有的**（这就是"区别段落"）：
>
> 1. **他们的参数量对照本身就是混淆。**
>    - 我们的 cap3 证明：拆成两块、但维度不压缩（512 维）的嵌入，和原版能表达的函数完全相同，参数还更多。
>    - 可是同等过拟合下，6 字母比 3 字母多记的部分从 0.61 变成 1.44 bit，差不多掉到 3 字母的水平。
>    - 所以他们"控制参数"和"不控制"两条曲线的差别，混进了写法的影响，不只是参数量。
>    - 这一点我们能用他们同款的对照方法直接演示出来，是真正新的方法学贡献。
> 2. **"记得更多"和"记得更快"。**
>    - 他们在固定训练量（500 / 100 / 70 轮）下测。
>    - 我们按留出集损失对齐（同样的泛化代价）把速度和数量分开，而且这种对齐不受训练日程影响。
>    - 结论：粗切法记得更快，**也**记得更多。
> 3. **训练目标作为一个"因素"，而不是三种不同架构。**
>    - 他们只说明 LM、MLM、编码器都服从"词表越大记得越多"的趋势。
>    - 我们在同一个骨架上改训练目标，包括掩码比例的剂量反应（先升后降，峰值 0.5），并且**分解方差**：切法 59.5%、目标 25.7%、交互 14.0%、种子 0.8%。
>    - 交互项，以及单字母完形填空"记住了但抽不出"的现象，都是新的。
> 4. **校准过的尺子。**
>    - 均匀随机 DNA 的瞎猜基准线**精确已知**（2.000 bit/字母）。所有指标按字母计，序列长度不同的切法也能直接比较。
>    - 另有探针重复档位、随机池排名、前缀逐字抽取、空白对照。
>    - 他们的指标是按样本算的（准确率、AUC），没有基准线。
> 5. **他们的机制猜想在 DNA 上可以直接检验。**
>    - 他们猜的是"序列长度"。k 字母切法**确定性地**改变序列长度（每个窗口 288 / 96 / 48 个 token），数据本身一点不变。
>    - 我们的"单字母 → 3 字母"这一段与容量、写法都无关，是目前对"序列长度假说"最干净的检验。
> 6. **领域和现实意义。**
>    - 真实 GLM 正好用这几种切法：DNABERT 用 6-mer，DNABERT-2 用 BPE-4096，Nucleotide Transformer 用 6-mer，HyenaDNA 和 Evo 是单字母。
>    - 已发表的 GLM 隐私比较（Alex 的 BCB 论文）把差异归因于架构，我们的网格显示大部分来自切法。

**Action items.**
- (a) Reframe the paper's contribution around points 1–5, with "tokenizer matters" as the *replicated* premise, not the headline.
- (b) Add a direct test of the length hypothesis. Candidates: vary k at fixed vocabulary cost, or a 6-mer model with its window cut so the token count matches 3mer.
- (c) Report our factorized-embedding result as a caution about their control.

> **要做的事：** (a) 把论文贡献重新围绕第 1–5 点来写，"切法有影响"作为**复现的前提**，而不是主结论；(b) 加一个直接检验"序列长度假说"的实验（比如在相同词表代价下改 k，或者把 6 字母的窗口截短，让 token 数和 3 字母一样）；(c) 把我们"拆嵌入"的结果写成对他们那种对照方法的提醒。

---

## 2. Capacity on random data: Morris et al. (2025)

**"How much do language models memorize?"** — Morris, Sitawarin, Guo, Kokhlikyan, Suh, Rush, Chaudhuri, Mahloujifar. arXiv:2505.24832. File: `Morris2025_How_Much_Do_LMs_Memorize.pdf`

- **What they did:** trained hundreds of GPT-style models on **uniformly random bitstrings**, the same logic as our iid DNA.
- **Findings:** capacity is about **3.6 bits per parameter**. Models memorize until capacity fills, after which generalization ("grokking") takes over.

**Relevance.**
- Our backbone has about 12.6M parameters, so a capacity of roughly 45M bits.
- Our training set is 5,000 × 288 nt × 2 bits ≈ 2.9M bits, which is **about 15× below capacity**. That explains why AR can memorize everything.
- Our results are therefore in the "capacity exceeds data" regime.
- A reviewer will ask whether the tokenizer effect survives once the data exceeds capacity. This makes Alex's extension #1 (corpus scaling) more important than we planned: we should add at least one point above capacity, for example ~20× more data or a smaller model.
- Also cite them for the random-data methodology.

> - **做了什么：** 在**均匀随机比特串**上训了几百个 GPT 式模型，思路和我们的随机 DNA 一样。
> - **结论：** 容量约 **每个参数 3.6 bit**；模型会一直记，直到容量填满，之后转向泛化。
>
> **和我们的关系：**
> - 我们的骨架约 12.6M 参数，按这个估计容量约 4500 万 bit。
> - 我们的训练集是 5000 × 288 字母 × 2 bit ≈ 290 万 bit，**比容量小约 15 倍**，这就解释了为什么接龙模型能全部背下来。
> - 所以我们现在的结果都处在"容量大于数据"的区间。
> - 审稿人一定会问：数据超过容量以后，切法效应还在吗？这让 Alex 的扩展第 1 条（语料规模）比原计划更重要——至少要加一个"数据超过容量"的点（比如数据量扩大约 20 倍，或者换更小的模型）。
> - 另外，随机数据的方法论可以引用这篇。

---

## 3. The objective axis in NLP (2026)

These three are the direct competitors on the **objective** half of our idea: AR vs masked / infilling / diffusion.

> 这三篇是我们 idea 里**训练目标**那一半的直接竞争者（接龙 vs 掩码 / 填空 / 扩散）。

| Paper | What | Finding | Our delta |
|---|---|---|---|
| **von Arx & Dieudonné**, "Memorization Dynamics of Fill-in-the-Middle Pretraining", arXiv:2605.22981 (21 May 2026) | Matched Llama-3.2 models, FIM vs left-to-right, repeated Gutenberg excerpts | FIM recovers short or partial spans more often; L2R is more confident on long exact continuations; extraction scales ~linearly with repetition; prefix context stays crucial | Objective only, no tokenizer axis, no decomposition; natural text, no exact floor |
| **Wang & Asokan**, "Extracting Training Data from Diffusion Language Models via Infilling", arXiv:2605.24173 (22 May 2026) | LLaDA-8B, Dream-7B; new infilling extraction protocol | Mask geometry governs extractability (edge-conditioned masks extract up to 3× more than prefix-conditioned); redacted PII can be recovered better than from AR | Attack paper on pretrained models; supports our point that the **scorer / conditioning choice changes the measured answer** (our pll vs prefix divergence) |
| **Luo, Yu, Li & Bjerva**, "Characterizing Memorization in Diffusion Language Models: Generalized Extraction and Sampling Effects", arXiv:2603.02333 (2 Mar 2026) | Theory + experiments, DLM vs AR under equivalent conditions | Higher sampling resolution → more exact extraction; AR decoding is the maximum-resolution case; DLMs leak substantially less PII | Consistent with our "masked models: present but not extractable". They vary decoding; we vary training objective and tokenizer jointly |

> | 论文 | 做了什么 | 结论 | 和我们的区别 |
> |---|---|---|---|
> | **von Arx & Dieudonné** | 配对的 Llama-3.2，FIM 填空 vs 从左到右，重复的古腾堡文本片段 | FIM 更常复现短片段或部分片段；从左到右对长的逐字续写更有把握；抽取量和重复次数大致成线性；前缀上下文仍然关键 | 只有训练目标，没有切法轴、没有方差分解；自然文本，没有精确基准线 |
> | **Wang & Asokan** | LLaDA-8B、Dream-7B；新的"填空式抽取"协议 | 遮挡的形状决定能抽出多少（两边给条件比只给前缀最多多抽 3 倍）；被抹掉的个人信息比从接龙模型更容易恢复 | 针对预训练模型的攻击论文；支持我们的观点：**打分 / 条件方式的选择会改变测出来的答案**（我们 PLL 和前缀两把尺子的分歧） |
> | **Luo 等** | 理论 + 实验，同等条件下比较扩散模型和接龙模型 | 采样分辨率越高，逐字抽取越多；接龙解码是分辨率最高的情况；扩散模型泄露的个人信息少得多 | 与我们"完形填空模型记住了但抽不出"一致。他们改的是解码方式，我们同时改训练目标和切法 |

---

## 4. Training dynamics: Tirumala et al. (2022)

**"Memorization Without Overfitting: Analyzing the Training Dynamics of Large Language Models"** — Tirumala, Markosyan, Zettlemoyer, Aghajanyan. arXiv:2205.10770 (NeurIPS 2022). File: `Tirumala2022_Memorization_Without_Overfitting.pdf`

- **Findings:** larger models memorize **faster** and can memorize more before overfitting.
- **Relevance:** this is the precedent for our "sooner vs more" framing, and they also measure memorization over training.
- **Our delta:**
  - They vary model size; we hold size fixed and vary tokenizer and objective.
  - We make the comparison at matched held-out loss.

> - **结论：** 模型越大记得**越快**，而且在过拟合之前能记住更多。
> - **和我们的关系：** 这是我们"更快 vs 更多"这个框架的先例，他们也是沿着训练过程测记忆。
> - **区别：** 他们改模型大小，我们固定大小、改切法和训练目标；我们的对比是在同等留出集损失下做的。

---

## 5. Methods we use (cite, not competitors)

| Paper | Use |
|---|---|
| Salazar, Liang, Nguyen & Kirchhoff, "Masked Language Model Scoring", ACL 2020, arXiv:1910.14659 | Our PLL scorer |
| Mireshghallah, Goyal, Uniyal, Berg-Kirkpatrick & Shokri, "Quantifying Privacy Risks of Masked Language Models Using Membership Inference Attacks", arXiv:2203.03929 (EMNLP 2022) | Likelihood-ratio membership inference on MLMs (AUC 0.90 vs prior 0.66); baseline for MLM privacy |
| Carlini, Ippolito, Jagielski, Lee, Tramèr & Zhang, "Quantifying Memorization Across Neural Language Models", arXiv:2202.07646 (ICLR 2023) | Our exact-extraction definition (k-token prefix → exact suffix) |
| Jagielski, "A Note On Interpreting Canary Exposure", arXiv:2306.00133 (2023) | Links canary exposure to membership inference and DP; supports our rank-based canary reporting |

> | 论文 | 我们用它做什么 |
> |---|---|
> | Salazar 等 2020 | 我们的 PLL 打分器 |
> | Mireshghallah 等 2022 | 完形填空模型上的似然比成员推断（AUC 0.90，之前的方法 0.66），MLM 隐私的对照 |
> | Carlini 等 2023 | 我们"逐字抽取"的定义（给前缀 → 精确复现后缀） |
> | Jagielski 2023 | 把探针暴露度和成员推断、差分隐私联系起来，支持我们基于排名的探针报告方式 |

---

## 6. Bottom line on novelty

**Honest assessment:**

- **Not novel alone:**
  - "larger vocabulary → more memorization" (Kharitonov 2021);
  - "masked or diffusion objectives → less extractable" (Luo 2026, von Arx 2026).
- **Novel:**
  - (i) the **joint** tokenizer × objective decomposition with an interaction term, on one backbone;
  - (ii) matched-overfitting separation of "more" from "sooner";
  - (iii) showing that the standard parameter control (factorized embedding) changes memorization by itself, so the tokenizer effect's magnitude is parametrization-dependent while its ordering is not;
  - (iv) a calibrated per-nucleotide instrument with an exact floor;
  - (v) the genomic setting, where these tokenizers are the actual design choices of deployed GLMs, and a published comparison exists whose attribution this corrects.
- **Biggest risk:**
  - Reviewers who know Kharitonov will call the paper incremental if we lead with the tokenizer effect. Lead with (i)–(iii).
  - The data-below-capacity regime (Morris 2025) needs one above-capacity point.

> **实话评估：**
>
> - **单独拿出来不新的：**
>   - "词表越大记得越多"（Kharitonov 2021）；
>   - "掩码 / 扩散目标更难被抽取"（Luo 2026、von Arx 2026）。
> - **新的：**
>   - (i) 在同一骨架上**联合**分解切法 × 训练目标，包括交互项；
>   - (ii) 按同等过拟合把"更多"和"更快"分开；
>   - (iii) 证明标准的参数量对照（拆嵌入）本身就会改变记忆量——切法效应的**大小**依赖写法，**排序**不依赖；
>   - (iv) 校准过、按字母计、有精确基准线的尺子；
>   - (v) 基因组场景：这些切法正是已部署 GLM 的真实设计选择，而且有一篇已发表的比较，我们能纠正它的归因。
> - **最大风险：**
>   - 懂 Kharitonov 的审稿人会觉得是增量工作——如果我们拿"切法效应"开头的话。所以要拿 (i)–(iii) 开头。
>   - 我们处在"数据小于容量"的区间（Morris 2025），需要补一个"数据超过容量"的点。
