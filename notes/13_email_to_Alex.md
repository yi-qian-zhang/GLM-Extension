# Email to Alex — final version

> 用法：
> 1. **只复制"英文邮件"那一部分**（从 Subject 到署名）发给 Alex，附件带上 `12_progress_summary_EN.md`（可以直接附 md，或者复制进 Word/Google Doc）。
> 2. 下面的"中文对照"只给你看，逐段对应，不要发出去。
> 3. 语气已经处理成"请教"：每个关于原代码的问题都给了他台阶（"我可能读错了"、"你可能早就知道"），也说明了我们没有改他的代码。

---

## 英文邮件（复制这部分）

**Subject:** A controlled tokenizer × objective ablation building on the BCB paper — progress, and some questions

Hi Alex,

I've been working through the BCB paper, your extension notes and the GLM-Memorization repo, and I'd like to tell you what I've started on and get your view.

**The idea**

The BCB paper shows that four GLMs memorize to different degrees. But those four models differ in architecture, tokenizer, pretraining objective and size all at once, so we can't tell which of these causes the difference. Your Discussion says a controlled ablation is needed, and that is your extension #2.

My project is that ablation. I train one small Transformer from scratch, keep everything fixed, and change only one thing at a time:

- the **tokenizer**: single nucleotide, 3-mer, or 6-mer (BPE next);
- the **pretraining objective**: causal (next-token) or masked, at several mask rates.

Then I plant canaries and measure, per nucleotide, how much each model memorizes. The question I want to answer is: **which design choice actually drives memorization in a GLM, and by how much?** If the tokenizer and objective explain most of it, then a difference between two GLMs should not be read as "architecture A is safer than B".

I'd really like you on this as a coauthor. It's your framework and your idea.

**What I've found so far** (pilot scale; a one-page summary is attached)

- The tokenizer is the biggest factor. On the fixed backbone it explains ~60% of the variance in canary memorization, the objective ~26%, and the random seed < 1%.
- Coarser tokens memorize sooner *and* more: at equal held-out loss, 6-mer memorizes far more than 3-mer, which memorizes more than single nucleotide.
- It is not a parameter-count effect, and it is not the sequence-length effect conjectured by Kharitonov et al. (2021). When the data exceed the model's capacity, the single-nucleotide model memorizes nothing while the 6-mer model still extracts every repeated canary.
- Canary placement matters a lot. With every copy at the same position, a repeated canary is recognized even in a new context. With copies at random positions, that largely disappears, which makes positional encoding a real design variable.

**On direction and novelty**

1. Is a small from-scratch model family on synthetic DNA a convincing way to make this point, or would you rather see it tied to the four models from the paper early on? My plan for external validity is the DNABERT 3/4/5/6-mer family (same architecture, data and objective, differing only in k), fine-tuned with planted canaries.
2. The closest prior work I've found is Kharitonov, Baroni & Hupkes (2021), who showed in NLP that larger BPE vocabularies memorize more, so I treat that as a replicated premise. What I think is new is listed in the attachment: the joint decomposition, "more vs. sooner", the parameter-control and sequence-length results, and the placement effect. Does that positioning seem strong enough to you? Is there genomics or privacy work I'm missing?
3. Are you comfortable with a framing along the lines of "architecture was not the variable"? I want it to read clearly as an extension of your paper, which raises this question itself, not as a critique of it.

**On the original pipeline**

I'd like my measurements to be consistent with yours, so I have a few questions about the implementation. You may well know the answers already, and I may simply be misreading the code.

4. **Checkpoint.** `run_experiment.py` passes the test loader to the trainer for early stopping and then evaluates `best_model.pt`. The paper notes that a separate validation split would likely give higher vulnerability scores. In my pilots, choosing the checkpoint by held-out loss picked the least-memorized epoch (rank-1 rose from ~5% to 100% just by scoring the final checkpoint). Was best-by-test-loss the intended choice for the reported numbers?
5. **Extraction.** The Methods describe prefix-conditioned beam search (width 10, up to 1,000 candidates). In the code, `run_experiment.py` calls `attack_all_canaries`, and I couldn't find where `prefix_attack` is called. Which version produced the reported extraction numbers?
6. **DNABERT-2 head.** The wrapper adds a new linear head trained with a next-token (shifted) loss on top of the bidirectional encoder, with no causal mask. Since each position can then attend to the token it is asked to predict, I wondered whether that head could learn to copy rather than memorize. Was this setup deliberate? For the DNABERT arm I was planning to use the native MLM head with pseudo-log-likelihood instead. Does that seem right to you?
7. **Table 3.** `metrics.py` combines the three vectors with 0.3 / 0.3 / 0.4 weights, while the paper describes a maximum. Do you still have the script that produced Table 3?
8. **Membership inference and length.** If I read the data code correctly, the canaries are inserted as standalone 64-nt sequences while the other sequences are 256 nt. `compute_losses` averages the loss over all positions, and I think that includes padding, since the labels are a copy of `input_ids`. If so, a classifier using only sequence length would reach about 900/1900 + ½·1000/1900 ≈ 0.74 AUC, which is close to the band in Table 5. Could you check whether I'm reasoning about this correctly?
9. **Canary position.** Related to the placement result above: because the canaries are standalone sequences, every copy starts at position 0. In my runs, fixed placement makes repeated canaries far easier to recognize than random placement. Do you think this could contribute to the repetition trends in the paper?
10. **Settings.** Which hyperparameters were actually used for each model (epochs reached, learning rate, LoRA or full fine-tuning)? Are any of the fine-tuned checkpoints still available? Not for exact reproduction, just so I know whether I'm in a comparable regime.
11. If any of these turn out to need a change, how would you like it handled: as an update to the GLM-Memorization repo, or as a note in my methods section? That's entirely your call.

**Next step**

Erman suggested that the three of us set up a joint meeting to go over the current progress and where to take this next. I'd really welcome that. I'm honestly not sure yet whether what I have is novel enough, and I'd like to hear what you think. Would you have time this week or next? I'm happy to send the slides beforehand.

Thanks a lot,
Spencer

---

## 中文对照（只给你看，不要发）

**主题：** 在 BCB 论文基础上做的"切法 × 训练目标"受控消融——进展和几个问题

你好 Alex，

我一直在读 BCB 论文、你的扩展建议和 GLM-Memorization 代码仓库。想跟你说一下我开始做的事情，听听你的看法。

**想法**

BCB 论文表明，4 个基因大模型的记忆程度不一样。但这 4 个模型的架构、切法、预训练目标、大小全都同时不同，所以没法判断差别到底是哪一个造成的。你在讨论部分说过需要一个受控消融实验，这也是你扩展建议的第 2 条。

我的课题就是做这个消融实验。我从零训练一个小 Transformer，其他全部固定，每次只改一样东西：

- **切法**：单字母、3 字母、6 字母（之后加 BPE）；
- **预训练目标**：接龙（预测下一个 token）或完形填空（几种不同的遮盖比例）。

然后往训练数据里塞卧底，按每个字母来衡量每个模型记住了多少。我想回答的问题是：**到底是哪个设计选择在决定基因大模型的记忆，各占多大比重？** 如果切法和训练目标能解释大部分差别，那么两个 GLM 之间的差别就不应该被解读成"A 架构比 B 架构安全"。

非常希望你作为共同作者参与。框架是你的，想法也是你的。

**目前的发现**（试点规模；附件是一页的总结）

- 切法是最大的因素。在固定骨架上，它解释了约 60% 的卧底记忆差异，训练目标约 26%，随机种子不到 1%。
- 切得越粗，记得越快，**也**记得越多：在同样的留出集损失下，6 字母远多于 3 字母，3 字母多于单字母。
- 这不是参数量造成的，也不是 Kharitonov 等人（2021）猜测的"序列变短"造成的。数据超过模型容量后，单字母模型什么都记不住，6 字母模型仍能抽出每一个重复过的卧底。
- 卧底放在哪里影响很大。每份拷贝都在同一位置时，重复过的卧底换到新上下文里仍能被认出来；拷贝随机放在不同位置时，这种能力大部分消失。所以位置编码成了一个真正的设计变量。

**关于方向和新颖性**

1. 用从零训练的小模型家族加合成 DNA 来说明这件事，有说服力吗？还是你更希望尽早和论文里的 4 个模型挂钩？我计划用 DNABERT 3/4/5/6 字母系列（架构、数据、训练方式都相同，只有 k 不同）塞卧底微调，来验证在真实模型上是否成立。
2. 我找到的最接近的前人工作是 Kharitonov、Baroni 和 Hupkes（2021），他们在 NLP 里证明了 BPE 词表越大记得越多，所以我把这一点当作复现的前提。我认为新的地方列在附件里：联合分解、"更多 vs 更快"、参数量对照和序列长度的结果、位置效应。你觉得这个定位够强吗？基因组或隐私方向有没有我漏掉的工作？
3. "架构不是那个变量"这类说法你能接受吗？我希望它读起来明确是对你论文的延伸（你的论文自己就提出了这个问题），而不是批评。

**关于原始代码**

我希望我的测量和你的保持一致，所以有几个实现上的问题。你可能早就知道答案，也可能只是我读错了代码。

4. **检查点：** `run_experiment.py` 把测试集的 loader 交给训练器做早停，然后用 `best_model.pt` 评估。论文里也提到，单独的验证集很可能会得到更高的风险分数。我的试点里，按留出集损失挑检查点，挑到的是记忆最少的那一轮（只要改用最终检查点打分，认出率就从约 5% 升到 100%）。论文里的数字是有意用"测试损失最低"的检查点吗？
5. **抽取攻击：** 方法部分写的是以前缀为条件的 beam search（宽度 10，最多 1000 个候选）。代码里 `run_experiment.py` 调用的是 `attack_all_canaries`，我没找到 `prefix_attack` 在哪里被调用。论文里的抽取数字是哪个版本跑出来的？
6. **DNABERT-2 的输出头：** 包装代码在双向编码器上加了一个新的线性头，用"预测下一个 token"的损失训练，没有因果遮罩。这样每个位置都能看到它要预测的那个 token，我在想这个头会不会学成"照抄"而不是"记忆"。这是有意这样设置的吗？在 DNABERT 那一组实验里，我打算改用原生的完形填空头，用伪对数似然打分，你觉得可以吗？
7. **表 3：** `metrics.py` 用 0.3 / 0.3 / 0.4 的权重合并三个指标，论文里描述的是取最大值。生成表 3 的脚本还在吗？
8. **成员推断和长度：** 如果我没读错数据代码，卧底是作为单独的 64 字母序列插入的，而其他序列是 256 字母。`compute_losses` 对所有位置的损失取平均，而且因为 labels 直接复制自 `input_ids`，我认为填充位也算在里面。如果是这样，只看序列长度的分类器就能达到约 900/1900 + ½·1000/1900 ≈ 0.74 的 AUC，和表 5 的范围很接近。你能帮我看看我的推理对不对吗？
9. **卧底位置：** 和上面的位置结果有关：因为卧底是单独成段的序列，每份拷贝都从第 0 个位置开始。我的实验里，位置固定会让重复过的卧底比随机位置时容易认出得多。你觉得这会不会影响了论文里"重复次数"的趋势？
10. **实际设置：** 每个模型实际用了哪些超参数（实际训练到第几轮、学习率、LoRA 还是全量微调）？微调好的检查点还在吗？不是为了精确复现，只是想知道我的实验和你的是否在可比的范围里。
11. 如果上面哪一点确实需要修改，你希望怎么处理：更新 GLM-Memorization 仓库，还是在我的论文方法部分说明？完全由你决定。

**下一步**

Erman 建议我们三个人约一个 joint 会议，一起讨论目前的进度和未来的方向。我很希望能开这个会。说实话，我还不确定现在做的这些新颖性够不够，很想听听你的看法。你这周或下周有时间吗？我可以提前把 slides 发给你。

非常感谢，
Spencer
