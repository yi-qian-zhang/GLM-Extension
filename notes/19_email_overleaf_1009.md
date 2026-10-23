# Email: Overleaf access for the RECOMB paper (9 Oct 2026)

To: Erman Ayday, Alexander Nemecek
Subject: **Overleaf project for the memorization paper — you both have edit access**

---

Hi Erman, hi Alex,

I have set up the Overleaf project for the memorization paper, and you both have edit access through
this link:

https://www.overleaf.com/6579122586wjpbgsdftnzd#f3378e

Erman, could you invite the other collaborators you mentioned? The link above carries edit rights,
so forwarding it to them is enough, or send me their addresses and I will add them.

What is in the project now: the section skeleton laid out for the RECOMB format (10 pages Letter
including all figures and captions, 10pt, 1-inch margins, with the optional appendix as a separate
PDF), the bibliography, and a table that maps every planned claim to the specific run that supports
it. The experiments are essentially finished — all four datasets, the extra seeds and the human
chromosome 22 arm are done; one confirmation arm is running tonight (below) — so from here it is
figures and writing.

Two results came in after the meeting that change what the paper leads with.

**The training objective is a bigger lever than the tokenizer, and it is the cheap one.** With the
backbone, the data and the schedule held fixed, and with real human haplotype segments as the
planted records, masked training memorizes 15 to 35 times less than the same tokenizer trained
next-token, reproduces no planted segment exactly at any checkpoint (against 100 per cent for
next-token), and reaches a *better* held-out loss on the same budget. It holds for the released
models too: the DNABERT checkpoints fine-tuned under their own masked objective, at matched
hidden-nucleotide rate, extract 0 per cent on chromosome 22 where the same checkpoints fine-tuned
next-token extract 67 to 97 per cent. So the mitigation section now leads with the objective, and the
fine tokenizer is the second recommendation, with the delay caveat above.

**Erman, this is also the answer to the non-monotonic column you asked about this morning.** Three
things were wrong with that column. It is verbatim extraction, which is thresholded and saturated, so
it is the wrong statistic to order models by. The DNABERT family tokenizes with overlapping k-mers,
so it is not the clean tokenizer axis to begin with (more below). And there was a measurement bias:
which canaries are members and which are matched controls was fixed by a single data seed, identical
for every model, so an accidental difference between the two groups of 50 real haplotype segments did
not average out — before any fine-tuning the pretrained checkpoints already read the member group
0.3 to 0.45 bits per nucleotide more easily. With that subtracted, the four k-mer checkpoints on
chromosome 22 are flat rather than ordered, and I am re-running the arm tonight with the split
re-drawn three more times so the paper can state it with an across-split spread instead of a
correction. The ordering by tokenizer granularity is clean on the other three datasets and that is
where the claim will rest; chromosome 22 is reported as the dataset where it is not resolvable.

Two things I would like to settle on Monday, because the abstract registration on 28 October has to
match the final paper closely: the title, and the author list and order. For the title I would
suggest

> *Tokenization and Training Objective Determine Memorization in Genomic Language Models*

I looked at the 221 papers RECOMB accepted between 2023 and 2026: the median title is 10 words, none
of them is a question, and the analysis papers follow this declarative pattern, so I would drop the
question form I used in the slides.

One correction to a result I showed this morning. The character-level tokenizer does not prevent
memorization, it delays it. I had only run it for 30 epochs; at 150 epochs it reaches complete
verbatim extraction of the planted human haplotypes. At matched held-out loss it still memorizes
clearly less than the 6-mer, so the recommendation for the mitigation section stands, but as a delay
with a compute cost rather than as a fix. On the same 150-epoch schedule and at the same held-out
loss, the 6-mer reproduces every planted segment exactly while the character model reproduces 28 per
cent of them.

Alex, one related point that may matter for how we describe your results: DNABERT tokenizes with
overlapping k-mers, so changing k changes the vocabulary but not the number of token slots per
window. Our controlled models use non-overlapping k-mers, where k does change the slots. They are
two different axes, and separating them removed an apparent contradiction between the two sets of
numbers, so I will state it explicitly in the setup section.

Finally, one requirement from the call that affects both of you: a paper that develops new software
or analysis methods must link a public, documented repository in the paper itself. Our code is on a
private branch at the moment, so we should agree what becomes public before 4 November. This does
not block the 28 October abstract.

Thanks,
Spencer

---

## 中文对照（自己留档，不发送）

邮件要点：
1. Overleaf 已建好，Erman 和 Alex 都有编辑权限，链接在正文里。
2. 请 Erman 邀请其余合作者（转发链接即可，或把邮箱给我）。
3. 项目里现有：按 RECOMB 格式（10 页含图、10pt、1 英寸边距、附录单独 PDF）排好的分节骨架、参考文献、以及"每条结论对应哪个实验"的对照表。实验基本跑完，今晚还有一组确认实验（见第 8 条）。
4. 周一要定两件事：标题、作者名单与顺序（因为 10/28 注册摘要后必须与终稿一致）。标题建议 *Tokenization and Training Objective Determine Memorization in Genomic Language Models*，依据是 2023–2026 年 221 篇 RECOMB 录用标题的统计：中位数 10 词、零问句、分析类论文都是陈述句。
5. **主动更正今早汇报的一个结论**：单字母切法不是防止记忆，是推迟记忆；只跑 30 轮看不出来，150 轮会完全被逐字复原。同等留出集损失下它仍然明显少记，所以建议保留，但措辞改成"推迟 + 算力代价"。
6. 给 Alex 的一点：DNABERT 用重叠 k-mer，改 k 不改变槽数；我们的受控模型用不重叠 k-mer。两者是不同的轴，分开说就消掉了两组数字之间的表面矛盾。
7. 征稿要求：开发新方法的论文必须在正文里给公开代码仓库链接，11/4 之前要定哪些公开。不影响 10/28 的摘要注册。
8. **会后两个新结果，改变了论文的主线顺序**：
   - 目标比切法是更大的杠杆，而且更便宜：同骨架同数据同日程、真实人类单倍型卧底，填空比接龙少记 15–35 倍、逐字复原 0%（接龙 100%）、留出集损失还更好；公开 DNABERT 用自己的填空目标在 chr22 上逐字复原 0%，而同 checkpoint 接龙是 67–97%。所以缓解措施第一条改成"目标"，细切法降为第二条并带"只是推迟"的限定。
   - **这同时是对 Erman 今早那个"非单调列"问题的回答**：那一列是逐字复原（阈值化、已饱和），本来就不该拿来排序；DNABERT 用重叠 k-mer，不是干净的切法轴；而且存在测量偏差——成员/对照的划分由单一 data_seed 固定、对所有模型都一样，两组各 50 条真实片段的偶然差异不会被平均掉，微调前预训练模型就已经把成员组读得容易 0.3–0.45 bit。减掉这个偏移后，chr22 上四个 k 字母 checkpoint 是持平而非有序；今晚正在重抽划分再跑三遍，让论文能给出跨划分的离散度而不是一个校正值。切法排序在另外三个数据集上是干净的，论文的结论建立在那三个上，chr22 作为"排不出顺序"的数据集如实报告。
