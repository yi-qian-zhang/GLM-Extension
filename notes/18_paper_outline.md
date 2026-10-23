# Paper outline and claim-to-evidence map / 论文提纲与证据对照

Skeleton lives in `paper/` (LaTeX, section files under `paper/sections/`). Build notes and the full
list of RECOMB 2027 requirements are in `paper/README.md`.

骨架在 `paper/`（LaTeX，分节文件在 `paper/sections/`）。编译说明和 RECOMB 2027 的完整要求在 `paper/README.md`。

---

## 1. Venue facts that shape the writing / 决定写法的投稿事实

| | |
|---|---|
| Abstract / 摘要注册 | 28 Oct 2026, must closely match the final title, authors and abstract |
| Full paper / 全文 | 4 Nov 2026 |
| Length / 篇幅 | **10 pages, Letter, including every figure, table and caption**; references excluded; one extra title page allowed |
| Format / 格式 | min 10pt, 1-inch margins, PDF; no required template; violating either is a desk reject |
| Review / 评审 | single-blind, do **not** anonymise |
| Appendix / 附录 | separate PDF, unlimited, reviewers may skip it |
| Code / 代码 | a public documented repository link **must appear in the paper** |
| Author cap / 作者上限 | at most 4 submissions per author |
| After acceptance | bioRxiv/arXiv posting required; JCB special issue offered |

Ten pages including figures is the binding constraint. The page budget in `paper/main.tex` allocates
1.25 pages to the introduction, 0.75 to related work, 1.25 to setup, 1.75 to the controlled grid,
1.5 to utility, 1.75 to the human arm, 1.0 to mitigation and 0.75 to the discussion. Anything that
does not fit goes to the appendix, which reviewers may ignore, so nothing load-bearing may live
there.

十页含图是硬约束。`paper/main.tex` 头部的页数预算：引言 1.25、相关工作 0.75、方法 1.25、受控实验 1.75、实用性 1.5、人类卧底 1.75、缓解措施 1.0、讨论 0.75。放不进去的进附录，而审稿人可以不看附录，所以关键内容不能放那里。

---

## 2. Claim-to-evidence map / 结论与证据对照

Every number in the paper must be traceable to a row here. Log sections refer to
`claude_notes/17_experiment_log_week3_EN.md` (Chinese: `17b`).

论文里每个数字都要能追到这张表的一行。日志小节号指 `17_experiment_log_week3_EN.md`（中文 `17b`）。

| # | Claim / 结论 | Evidence / 证据 | Log | Output |
|---|---|---|---|---|
| C1 | The objective decides whether whole records are memorised; it is the largest single factor | variance decomposition, random placement: objective 57.7%, tokeniser 15.4%, interaction 26.9%, seed 0.0% | 3.2, 3.4 | `outputs/core_all`, `tok1` |
| C2 | Within an objective, memorisation is monotone in average token length | controlled grid at matched held-out loss, E. coli: char 1.804 / 3-mer 1.458 / BPE 1.115 / 6-mer 0.811 @2.10 | 3.16 | `outputs/{core100,ecoli_ar,bpe_arm}` |
| C3 | The BPE model is not special; "BPE memorises most" was a property of DNABERT-2 | matched backbone puts BPE (5.0 nt/token) between 3-mer and 6-mer | 3.16 | `bpe_arm` |
| C4 | The mechanism is token rarity, not slot count | per-slot spread grows to 40x; canary-token corpus counts 287,995 / 6,014 / 400 / 47 | 3.16 | `token_info.py` |
| C5 | The length conjecture of Kharitonov et al. fails on DNA | spaced k-mers hold sequence length fixed and reproduce the effect | earlier week | `len_sp` |
| C6 | Fixed canary placement manufactures apparent memorisation | fixed vs random offset, absolute vs RoPE | 3.5, 3.6 | `off1`, `rope_rand` |
| C7 | The released k-mer family is ordered on three real genomes | 3 seeds, round 50: E. coli 1.60/0.88/0.59/0.30, yeast 0.76/0.56/0.36/0.21, GUE 1.53/1.00/0.51/0.29 | 3.23 | `dnabert_{ecoli,yeast,gue}*` |
| C8 | Two released models break the order from outside the tokeniser axis | DNABERT-2 (117M, ALiBi) and HyenaDNA (char, different architecture) | 3.7, 3.10, 3.23 | `hyena*`, `dnabert2*` |
| C9 | Stopping at the best held-out loss does not prevent capture | at the optimum: 6-mer 1.85 bits/23% recognised, DNABERT-2 100% recognised, HyenaDNA 35% extracted | 3.9, 3.14 | `real_report_*.md` |
| C10 | Six downstream tasks across two organisms are blind to memorisation | MCC change <= 0.05 over 50 rounds, no downward trend, while extraction goes to 70-100% | 3.15, 3.17, 3.19 | `*_ds`, `gue_ds2` |
| C11 | Selecting a checkpoint by downstream score picks the leakiest | best MCC at round 50 for 4 of 6 models | 3.15 | `real_report_gue_ds.md` |
| C12 | Repeated real human records leak from every released model | r=16 allele recovery 0.90-1.00 vs control 0.22-0.26, extraction 67-100% | 3.21, 3.24 | `human_real3` |
| C13 | One copy is enough for the two heaviest memorisers | DNABERT-2 0.86 vs 0.26 control and 57% verbatim; HyenaDNA 0.47 vs 0.26 | 3.24 | `human_real3` |
| C14 | Membership inference alone understates single-copy risk | rank-1 only 4-26% at r=1 against a real pool, while extraction succeeds | 3.21 | `human_real3` |
| C15 | The character tokeniser removes the leakage at no cost in held-out loss | 0% extraction at every tier and snapshot, allele gap +0.03, best held-out loss 1.794 still falling | 3.20 | `human_toy` |

### Claims deliberately NOT made / 刻意不下的结论

- No impossibility claim for the character tokeniser: 30 rounds is not past its own optimum.
- No matched-compute comparison: a character model processes six times the token slots.
- No ordering based on the chromosome-22 extraction column, which is non-monotone (97/86/67/85%) by
  more than its standard error and has no mechanism.
- No claim about models larger than 117M parameters or about a second chromosome.

---

## 3. Figures / 图

| Fig | Content | Source |
|---|---|---|
| 1 | design schematic: fixed backbone, three knobs, canary tiers, three rulers | to draw |
| 2a | variance decomposition, fixed vs random placement | `figures_proposal.py` F1 |
| 2b | memorisation per nucleotide vs per token slot | `token_info.py --plot` |
| 3 | the four tokeniser trajectories on real human canaries | `human_toy/trajectory.png` |

Tables: controlled matched-floor (Sec. 4), released family on three genomes (Sec. 5), downstream
(Sec. 6), human chr22 (Sec. 7), mitigation summary (Sec. 8). That is four figures-worth plus five
tables for ten pages, which is already at the limit; the mitigation table and the human table are
the two that must survive any cut.

表：受控同等过拟合（第 4 节）、公开家族三个基因组（第 5 节）、下游（第 6 节）、人类 22 号染色体（第 7 节）、缓解措施汇总（第 8 节）。十页里四张图加五张表已经到顶；真要砍，必须保住缓解措施表和人类表。

---

## 4. Blocking items that are not writing / 不属于写作的阻塞项

1. **Public code repository**, required in the paper by the call. Our work is on the private branch
   `glmex`; `pilot2/` is ours, `src/`, `experiments/`, `config/` are Alex's. Needs a decision with
   Alex and Erman on what becomes public, then a repository with a README that reproduces every
   table. Gates 4 Nov, not 28 Oct.
2. **Author list and order**, needed for the 28 Oct abstract, which must then match the final paper.
3. **Overleaf project** with Erman as owner plus the four collaborators he will name.
4. Three transcription errors in the 9 Oct meeting notes to correct on Monday: the single-copy
   trajectory is 0.19 -> 0.33 -> 0.84 and not saturated at 19%; the questioned column is verbatim
   extraction and not usefulness; "4K model" means the k-mer family.
