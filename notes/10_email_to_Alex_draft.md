# Email to Alex — draft (not sent)

> 用法：Part A 是邮件正文，英文在上、中文翻译在下（中文只给你看，不要发出去）。Part B 是**只在 1:1 当面问**的问题，不写进邮件。Part C 是为什么这么分。
> 发送前请你自己再读一遍，改成你自己的语气；尤其是称呼和结尾。

---

## Part A — Email

**Subject:** Controlled tokenizer × objective ablation building on the BCB paper — early results, would love your read

> 主题：在 BCB 论文基础上做的"分词 × 训练目标"受控消融——初步结果，想听听你的看法

---

Hi Alex,

> 你好 Alex，

I've been working through the BCB paper and your extension notes. Your Discussion says a controlled ablation on a fixed architecture would be needed to attribute memorization differences causally, and that tokenization wasn't isolated. I've started building exactly that as my first project, and I'd really like you on it as a coauthor. It's your framework, and the idea is your extension #2.

> 我一直在读 BCB 论文和你的扩展建议。你在讨论部分写到，要把记忆差异因果地归因，需要在固定架构上做受控消融，而且分词方式没有被隔离出来。我已经开始把这个作为我的第一个课题来做，非常希望你作为共同作者参与——框架是你的，这个 idea 也是你的扩展第 2 条。

**The design.**
- One fixed 12.9M-parameter Transformer.
- Varied: only the tokenizer (char / 3-mer / 6-mer, with BPE next) and the pretraining objective (causal vs masked at several mask rates).
- Training data: synthetic uniform DNA, so the chance floor is exactly 2 bits/nt. Canaries are planted at 0/1/4/16 repetitions.
- Measurement: everything per nucleotide — canary bits/nt, rank against a random pool, and exact prefix extraction.
- Deliverable: a variance decomposition of memorization into tokenizer / objective / seed.
- Your extension #3 (bounded-prior membership privacy) would be the reporting standard, and #1 (corpus scaling) a control.

> **设计：** 固定一个 12.9M 参数的 Transformer，只改分词（单字母 / 3 字母 / 6 字母，下一步加 BPE）和训练目标（接龙 vs 不同掩码比例的完形填空）。训练数据是均匀随机合成 DNA，瞎猜的基准线正好是 2 bit/字母；探针分 0/1/4/16 次重复塞进去。所有指标都按每个字母计：探针 bits/nt、在随机池里的排名、给前缀后的逐字抽取。产出是把记忆量拆成分词 / 目标 / 种子各占多少。你的扩展第 3 条（有界先验成员隐私）作为报告标准，第 1 条（语料规模）作为对照。

**Where it stands after two weeks of pilots** (4 × 4090, each run takes minutes):

1. On the fixed backbone, the **tokenizer explains ~60% of the variance** in canary memorization, the objective ~26%, their interaction ~14%, and the seed <1%.
2. Coarser tokens memorize **both sooner and more**. At an equal held-out loss, i.e. the same generalization cost, 6-mer models leak far more canaries than char models, so early stopping doesn't remove the effect.
3. Masked-model memorization is non-monotone in mask rate, peaking at 0.5. Causal models sit far off that curve.
4. A capacity control (shrinking the body to match parameter counts) doesn't change the 6-mer result. But an equivalent reparametrization of the embedding does change it a lot. So part of the large-vocabulary effect depends on training details, not only on the model class.
5. The null checks pass: untrained models give uniform ranks, and a blind baseline is at chance.

> **两周试点后的进展**（4 张 4090，每次训练几分钟）：
> 1. 固定骨架下，**分词解释了探针记忆约 60% 的方差**，训练目标约 26%，交互约 14%，随机种子不到 1%。
> 2. 切得越粗，**记得更快也更多**：在同样的留出集损失下（同样的泛化代价），6 字母模型泄露的探针远多于单字母模型，所以提前停止抵消不了。
> 3. 完形填空模型的记忆量随掩码比例先升后降，峰值在 0.5；接龙模型远离这条曲线。
> 4. 容量对照（缩小主体让参数量对齐）不改变 6 字母的结果；但对嵌入层做一个等价的换写法，影响却很大——大词表效应有一部分取决于训练细节，而不只是模型本身。
> 5. 空白对照都通过（未训练模型排名均匀，盲基线在随机水平）。

**What I'd most like your read on:**

1. **Direction.** Is a small, from-scratch model family on synthetic DNA the right way to make this point? Or would you want it anchored to the four models from the paper earlier rather than later? I'm planning a real-genome arm on E. coli next.
2. **Novelty.** The closest prior work I've found is Kharitonov, Baroni & Hupkes (2021, "How BPE Affects Memorization in Transformers"). They showed in NLP that larger BPE vocabularies memorize more, even with a parameter-count control. So "the tokenizer matters" on its own isn't new.

   What I think is new:
   - (a) the joint tokenizer × objective decomposition, including the interaction;
   - (b) separating "memorizes more" from "memorizes sooner" at matched held-out loss;
   - (c) their parameter control, a factorized embedding, turns out to change memorization by itself in our runs, even at full rank where the function class is identical;
   - (d) the calibrated genomic setting, where these tokenizers are the real design choices.

   On the objective side there are recent NLP papers: von Arx & Dieudonné 2026, Wang & Asokan 2026, Luo et al. 2026. Does this positioning seem strong enough to you, and is there anything in the genomics or privacy literature I'm missing?
3. **Framing.** Is the "the architecture label isn't the variable" framing something you're comfortable with, given it builds directly on your paper's own Discussion? I want to be sure it reads as an extension of your work, not a critique of it.

> **最想听你看法的三点：**
> 1. **方向：** 用从零训练的小模型家族 + 合成 DNA 来说明这件事，路子对吗？还是你希望尽早和论文里那 4 个模型挂钩？我下一步打算在大肠杆菌上做真实基因组的版本。
> 2. **新颖性：** 我找到的最接近的前人工作是 Kharitonov、Baroni 和 Hupkes 2021 年的 "How BPE Affects Memorization in Transformers"。他们在 NLP 里证明了词表越大记得越多，而且控制了参数量也成立。所以单说"切法有影响"并不新。
>
>    我认为新的地方是：
>    - (a) 切法 × 训练目标的联合分解，包括交互项；
>    - (b) 在同等留出集损失下，把"记得更多"和"记得更快"分开；
>    - (c) 他们用来控制参数量的方法（拆分嵌入），在我们的实验里本身就会改变记忆量，即使维度不压缩、能表达的函数完全相同；
>    - (d) 校准过的基因组场景，这些切法正是真实模型的设计选择。
>
>    训练目标那一侧，最近有几篇 NLP 论文：von Arx & Dieudonné 2026、Wang & Asokan 2026、Luo 等 2026。你觉得这样定位够不够强？基因组或隐私方向的文献里还有我漏掉的吗？
> 3. **定位：** "架构标签不是那个变量"这个说法，因为是直接接着你论文讨论部分往下做的，你觉得这样讲可以吗？我想确保它读起来是你工作的延伸，而不是在批评它。

Could we find 30–45 minutes this week or next? I'd like to walk you through the setup and the plots, and I also have some implementation questions about the original pipeline that I'd rather ask than guess at. I'm happy to send the slides beforehand if that's useful.

> 这周或下周能找 30–45 分钟聊一下吗？我想给你过一遍实验设置和图，另外还有一些关于原始代码实现的问题，想当面问而不是自己猜。如果有帮助，我可以提前把 slides 发给你。

Thanks!
Spencer

> 谢谢！
> Spencer

---

## Part B — Questions for the 1:1 only (do not put in writing)

> 这些是当面问的。前面 10 分钟先讲 idea 和结果，然后再按顺序问。**全部当成"请教"来问，不是挑错**——他很可能已经知道答案。

**B1. Coauthorship and division of work** (ask first)
"Would you want to be on this as a coauthor? How involved would you like to be: weekly check-ins, or reviewing drafts?"
> 共同作者和分工：你愿意做共同作者吗？想参与到什么程度——每周碰一次，还是只看稿子？

**B2. Which checkpoint produced the memorization numbers?**
"In my pilots, selecting the checkpoint by validation loss picks the least-memorized epoch on random data. The rank-1 rate went from 5% to 100% just by scoring the final checkpoint instead. Which checkpoint did the paper's numbers come from?"
> 论文的数字来自哪个 checkpoint？我的试点里按验证损失挑 checkpoint 会挑到记得最少的那一轮，换成最终 checkpoint，rank-1 从 5% 变成 100%。

**B3. Extraction attack wiring**
"The Methods describe prefix-conditioned beam search, but `run_experiment.py` calls `attack_all_canaries`, and `prefix_attack` doesn't seem to be called. Which one produced the reported numbers?"
> 抽取攻击：方法部分写的是前缀条件 beam search，但代码里调用的是 `attack_all_canaries`，`prefix_attack` 好像没被调用。论文数字是哪个跑出来的？

**B4. DNABERT-2 scoring head**
"Was the causal-shift head on DNABERT-2 a deliberate choice? For our bridge to real models I was planning to use its native MLM head with pseudo-log-likelihood."
> DNABERT-2 的打分头：在双向编码器上接因果移位头是有意的吗？我们接真实模型时打算用它原生的 MLM 头做 PLL。

**B5. How were the four models fine-tuned?** Epochs, learning rate, and whether a new output head was added.
"Not for exact reproduction. I just want to know whether our regime is comparable, and whether a new head was trained from scratch, since that would itself change memorization."
> 那 4 个模型是怎么微调的（轮数、学习率、有没有新加输出头）？不是为了精确复现，是想知道我们是否在可比的范围里；新训的输出头本身就会影响记忆。

**B6. Table 3 script**
"`metrics.py` implements the 0.3/0.3/0.4 weighted aggregation from the proposal rather than the max in the paper. Do you still have the script that produced Table 3?"
> Table 3 的脚本：`metrics.py` 里是 proposal 的 0.3/0.3/0.4 加权，而论文写的是取最大值。生成 Table 3 的脚本还在吗？

**B7. How should corrections be handled?**
"If any of these turn out to need changes, would you prefer a repo update, or should it go into my methods section? It's your call, it's your framework."
> 如果上面哪一条需要修正，你希望更新原仓库，还是写进我论文的方法部分？你来定。

**B8. The canary length / padding question** — only after he is engaged, possibly in a second meeting, and phrased as arithmetic to check.
See `01_spinoff_plan_full_EN.md` §4 Step 4 for the exact wording.
> 探针长度 / 填充的问题：等他投入进来之后再问，可以放到第二次见面，而且要当成"帮我核对一下算术"来问。原话见 `01_spinoff_plan_full_EN.md` §4 第 4 步。

**B9. Practical constraints**
"Storage on Pioneer, access to the original fine-tuned checkpoints, and the timeline you have in mind for your own next paper, so we don't collide."
> 实际约束：Pioneer 的存储；能不能拿到原来微调好的 checkpoint；他自己下一篇的时间线，避免撞车。

---

## Part C — Why the split

- **The email only contains our own results and open questions about direction.** That is safe to put in writing and gives him something concrete to react to.
  > 邮件里只放我们自己的结果和方向性问题——这些写下来没问题，也让他有具体东西可以回应。
- **Anything that could read as "your paper has a bug" stays verbal:** checkpoint selection, extraction wiring, the Table 3 script, the length confound. He may already know, and there may be context we're missing. Raising it privately and in person, once, lets him decide what to do. It's his and Erman's call, not ours.
  > 任何可能被读成"你的论文有 bug"的东西都只当面说（checkpoint 选择、抽取攻击接线、Table 3 脚本、长度混淆）。他可能早就知道，也可能有我们不了解的背景。私下、当面、只提一次，由他决定怎么处理——这是他和 Erman 的事，不是我们的。
- **No numbered list of problems in any document or email, ever** (rule from `01_spinoff_plan_full_EN.md` §4).
  > 任何文档或邮件里都不出现"问题清单"（`01_spinoff_plan_full_EN.md` §4 的规则）。
