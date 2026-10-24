# Experiment Log — Week 3 (5–11 October 2026)

**Project:** tokenizer × objective (× position encoding) in GLM memorization — paper 1, target RECOMB 2027 (abstract 28 Oct, full paper 4 Nov; checkpoint 21 Oct; fallback ISMB/ECCB, 7 Jan)
**Owner:** Spencer Zong · **Branch:** `glmex`, commits `ba174a0` → `7d16e5f`
**Compute:** TJU_6004, 4 × RTX 4090, conda `glm`
**Meetings this week:** Alex 1:1 on 4 Oct (`16_meeting_Alex_1004.md`); Erman's venue suggestion on 4 Oct (RECOMB / ISMB)

Running log; each step is appended when it happens. Numbers in this file are read from the server outputs named in each entry.

---

## 1. Decisions carried into the week

- Framing (Alex): "a more in-depth analysis of what prior work left open", not an "ablation"; drop "architecture was not the variable".
- Scope (Alex): toy model + HyenaDNA + DNABERT family; Evo out.
- Venue (Erman + Alex): bioinformatics conference first. Decision 7 Oct: aim RECOMB 2027, go/no-go on 21 Oct based on the DNABERT family result; fallback ISMB/ECCB 2027.
- Random canary placement is now the default for every new run (`--probe_offset random`).

---

## 2. Step log

### 2.1 (8 Oct, 01:53) core100 — core AR grid with 100 canaries per tier, 3 seeds, random placement

`tmux core100` → `outputs/core100/`. `pilot2/sweep.sh outputs/core100 ar "0 1 2" "--epochs 30 --tiers 1,4,16 --probes_per_tier 100 --n_nonmember 100 --save_epochs 1,2,3,5,8,12,20,30 --score_snapshots --probe_offset random" "char 3mer 6mer"`. 9 runs, ~15 min.

**Result (per cell 300 probe judgements, so about ±5 points on a rate):**

| | char | 3mer | 6mer |
|---|---|---|---|
| r=1 canary bits/nt at matched held-out floor 2.20 (train host) | — (char reaches only 2.03–2.05 in 30 epochs) | 1.63 | **0.76** |
| r=16 canary in a new host at a new offset: rank-1 | 0% | 2% | **39%** (in-phase, n=285) |
| non-member false positives (fresh host) | 0% | 1% | 0% |
| r = 1 / 4 / 16 at own training host, epoch 30 (bits/nt) | 1.95 / 1.95 / 1.95 | 0.02 / 0.01 / 0.02 | 0.03 / 0.03 / 0.03 |

Reading: with 100 canaries everything from week 2 holds: tokenizer order 6 > 3 > 1 at matched floor; under random placement the repetition tiers collapse onto one value at the training host (whole-example memorization), and recognition in a new context survives only for 6mer and only when the k-mer phase matches. Files: `outputs/core100/trajectory.md`, `offset_report.md`.

### 2.2 (8 Oct) Private repo check — `/data/wh/yqdata/PLM-Memorization` (read-only)

Core `src/` identical to the public repo. Resolved all 11 questions; details in `16_meeting_Alex_1004.md` §6. Key points for our methods section: his "extraction success" = rank ≤ 100 among 1,000 random sequences (chance 10%); Table 3 = max of three normalized scores (`compute_risk_scores.py`); canaries are standalone 64-nt sequences among 256-nt ones (his own comment, `canary_detectability.py:212`), padded to 512, MIA loss not pad-masked. No checkpoints exist.

### 2.3 (8 Oct) DNABERT family pipeline — `pilot2/dnabert.py` (commit `12cfc48`), `pilot2/analyze_dnabert.py` (`c1fbc06`)

- Data: the same pilot2 windows and canaries (288 nt, random offsets).
- Tokenization: DNABERT's overlapping k-mers from its own `vocab.txt`.
- Fine-tuning: **native MLM head**, DNABERT-style span masking (k consecutive tokens, ~15% of tokens), AdamW lr 2e-5, wd 0.01, 10% warm-up then constant, effective batch 16, grad clip 1.0 (the published config values), 30 epochs, snapshots at 1/3/8/15/30, plus the pretrained model scored before fine-tuning (epoch 0).
- Scoring: per-nucleotide span-masked PLL (mask the k tokens covering nt j; read the token starting at j, restricted to k-mers consistent with the visible neighbours, marginalized to the letter at j); probes scored every 3rd nucleotide (32 positions); rank vs a 100-sequence random pool; left-to-right extraction from a 48-nt prefix with consistent-k-mer decoding.
- Smoke test: pretrained 6-mer on uniform DNA = 2.05–2.11 bits/nt (chance), pipeline end-to-end in 43 s.
- Launched 02:09, `tmux dnabert1` → `outputs/dnabert/dnabert{3,4,5,6}_s{0,1}/`. Training ≈ 13–15 min per model; each snapshot score ≈ 5 min; ≈ 55 min per run; two runs per GPU.
- Pre-registered prediction: memorization at matched held-out floor increases 3 < 4 < 5 < 6.

### 2.4 (8 Oct) E. coli arm wired in — commit `7d16e5f`

`pilot2/real_data.py` gained `offset_mode`; `pilot2/run_pilot.py` gained `--data ecoli --fasta ...`. Smoke test passes in both modes. Note: on real DNA the held-out score can be below 2.0 (structure to learn), so the scorer's `floor_ok` flag is expected to read VIOLATION there; it is informational only.

### 2.5 (8 Oct, 02:54) Overnight queue — `pilot2/queue_1008.sh`, `tmux night`, log `outputs/night_1008.log`

Waits for `DNABERT1_DONE`, then:

| GPU | Runs | Output |
|---|---|---|
| 0 | E. coli, AR × {char, 3mer, 6mer} × seeds {0,1}, 50 probes/tier, random placement, snapshots; then E. coli MLM@0.15 / @0.5 × 3 tokenizers, seed 0 (40 probes/tier, pool 300) | `outputs/ecoli_ar/`, `outputs/ecoli_mlm/` |
| 1, 2 | Synthetic MLM@0.15 / @0.5 × 3 tokenizers × seeds 0 / 1, 40 probes/tier, pool 300, random placement | `outputs/core_mlm/` |
| 3 | DNABERT seed 2 for k = 3..6; then RoPE char × 2 seeds, 100 epochs, random placement | `outputs/dnabert/`, `outputs/rope_char100/` |

Ends with `NIGHT_DONE` in the log.

### 2.6 (8 Oct, 04:00) DNABERT family, first result: essentially no memorization at the published setting

`outputs/dnabert/dnabert_report.md` (seeds 0 and 1, native MLM head, 15% token masking, lr 2e-5, 30 epochs):

| k | held-out floor at epoch 30 | r=16 canary, training host (bits/nt / rank-1 / exact) | r=16, new host | false positives |
|---|---|---|---|---|
| 3 | 2.002 | 2.00 / 0.00 / 0.00 | 2.00 / 0.00 / 0.00 | 0.01 |
| 4 | 2.005 | 1.99 / 0.10 / 0.00 | 1.99 / 0.10 / 0.00 | 0.03 |
| 5 | 2.009 | 1.98 / 0.00 / 0.00 | 1.99 / 0.00 / 0.00 | 0.00 |
| 6 | 2.017 | 1.96 / 0.10 / 0.00 | 1.96 / 0.08 / 0.00 | 0.01 |

Reading. None of the four models memorizes the canaries in 30 epochs: canary bits stay at 1.96–2.00, rank-1 ≤ 10%, extraction 0, and the held-out floor never leaves 2.00–2.02 (no overfitting at all). The pretrained models (epoch 0) sit at 2.09–2.11 on uniform DNA, as expected. There is a faint 6 < 5 < 4 < 3 ordering at r=16 (1.96 < 1.98 < 1.99 < 2.00), in the predicted direction but within noise. So the pre-registered test is **not decided** by this run.

Why the pressure was too weak (diagnosis, not a result): with overlapping k-mers, hiding one nucleotide requires masking k consecutive tokens, so a 15% *token* mask rate hides only ~15%/k of the *nucleotides* (5% for k=3, 2.5% for k=6). Each sequence therefore supervises very few nucleotides per epoch, and lr 2e-5 is small. This also makes the standard setting unfair across k (smaller k hides more nucleotides per epoch). The published pipeline instead supervised every position with a next-token head.

Two corrected variants, implemented in `pilot2/dnabert.py` (commit after `c1fbc06`; `--objective causal`, `--mask_nt_rate`), both smoke-tested:

- **causal**: next-token prediction with a causal attention mask on the encoder and the native head (no new head, no bidirectional leak). With overlapping k-mers each next token adds exactly one nucleotide, so this is nucleotide-level AR over k-mer embeddings and per-nt scoring is exact (restrict to the 4 k-mers consistent with the k−1 known letters). lr 2e-5 as published. Pretrained model under a causal mask starts far off (4.8 bits/nt) and reaches ~2.04 after one smoke epoch.
- **nt0.05_lr1e-4**: MLM with the *hidden-nucleotide* rate fixed at 5% for every k (token rate = 5% × k), lr 1e-4.

Launched 04:08, `tmux dnabert2` (GPU 3: causal k=3..6 and nt-variant k=3,4; GPU 0: nt-variant k=5,6), seed 0, same snapshots; ends with `DNABERT2_DONE`. The seed-2 runs of the original setting were stopped (uninformative) and their partial outputs removed.

### 2.7 (8 Oct, 04:20) HyenaDNA downloaded and load-tested (no experiment yet)

`/data/wh/yqdata/models/HyenaDNA/{hyenadna-tiny-1k-seqlen-hf, hyenadna-small-32k-seqlen-hf}` via hf-mirror (curl). Both load under transformers 4.29 with `trust_remote_code`, as `HyenaDNAForCausalLM`: tiny 0.44M params, small 3.28M. Character vocabulary (A/C/G/T = ids 7–10, 16 logits), causal, the tokenizer appends `[SEP]` and no BOS. The 14.2M HyenaDNA in the BCB paper is a larger checkpoint (medium); to fetch if needed. Plan: a thin wrapper so the pilot2 AR scorer runs on it unchanged (1-mer, causal, pretrained unembedding kept).

### 2.8 (8 Oct, 07:30–08:30) Morning launches: DNABERT causal seeds 1–2 and 100 epochs; HyenaDNA pipeline

- **`tmux dnabert3`** (GPU 1, 2): `--objective causal`, k = 3..6, seeds 1 and 2, 30 epochs — robustness of §3.1. Ends `DNABERT3_DONE`.
- **`tmux dnabert4`** (GPU 0, 3): `--objective causal`, k = 3..6, seed 0, **100 epochs**, snapshots 15/30/50/75/100 → `outputs/dnabert_e100/`. Question: do k = 3, 4 catch up (sooner vs more at the real-model scale)? Ends `DNABERT4_DONE`.
- **`pilot2/hyena.py`** (commit after `f8fa2ba`): pretrained HyenaDNA (character model, causal) on the same data, native unembedding kept, [BOS] prepended; per-nt scoring from the four ACGT logits; pool 500; greedy extraction. Published config: lr 2e-5, wd 0.01, 10% warm-up, batch 8 × 2. Models downloaded via hf-mirror: tiny (0.45M), small (4.07M), **medium-160k (14.24M; the checkpoint named in the BCB config)**. [corrected 20 Oct: counted directly from the state_dict as 450,712 / 4,069,168 / 14,236,768. An earlier note here read 6.55M for medium and called the paper's 14.2M a discrepancy; the count was short, almost certainly by omitting the implicit Hyena filter MLPs, and the paper's figure is right.] Smoke: pretrained medium on uniform DNA = 2.10 bits/nt (chance); one epoch → 2.00.
- **`tmux hyena1`** (GPU 1, 2): medium × seeds 0/1/2 at lr 2e-5; medium at lr 1e-4; small at 2e-5; 30 epochs, snapshots, epoch-0 baseline → `outputs/hyena/`. Ends `HYENA1_DONE`.
- Combined random-placement decomposition built as `outputs/core_all/` (symlinks to core100 seeds 0–1 and core_mlm) and reported in §3.3.

### 2.9 (8 Oct, 11:00) Real models on the real genome: memorisation vs utility in one run

Erman asked for a utility metric next to memorisation. Design: fine-tune the pretrained models on **real E. coli windows** with planted canaries (the realistic threat: fine-tuning on a sensitive real cohort). The held-out loss on unseen E. coli windows is then the utility measure, and it is recorded at every snapshot together with the canary scores, so one run gives the memorisation-vs-utility trajectory. `--data ecoli` added to `pilot2/dnabert.py` and `pilot2/hyena.py` (commit after `3cfb6e9`), smoke-tested.

Launched `tmux real1` → `outputs/dnabert_ecoli/` (DNABERT causal, k = 3..6, seed 0, 50 epochs, snapshots 1/3/8/15/30/50, epoch-0 baseline; one k per GPU) and `outputs/hyena_ecoli/` (HyenaDNA medium, seeds 0 and 1, same schedule). Ends `REAL1_DONE`.

### 2.10 (8 Oct, 12:00) Figures for the proposal update and the paper — `pilot2/figures_proposal.py`

Five figures built from the saved reports (copies in `claude_notes/figures/proposal/`):

| file | what it shows | source |
|---|---|---|
| F1_variance.png | share of variance (tokenizer / objective / interaction / seed), fixed vs random placement | tok1, core_all |
| F2_matched_floor.png | r=1 canary memorised vs held-out loss, synthetic and E. coli, 3 tokenizers | core100, ecoli_ar |
| F3_dnabert_family.png | DNABERT 3/4/5/6-mer: r=16 recognised at epoch 30 (training host / new host, 3 seeds); 100-epoch trajectories | dnabert, dnabert_e100 |
| F4_position.png | r=16 canary in a new sequence: absolute+fixed / absolute+random / RoPE+random, from-scratch backbone | off1, core100, rope_rand |
| F5_real_models.png | r=16 memorised over fine-tuning: HyenaDNA medium vs DNABERT 3-mer / 6-mer (causal) | hyena, dnabert |

- F6_utility.png: memorisation vs utility on E. coli for the real models (added 8 Oct, 14:00; source dnabert_ecoli, hyena_ecoli).

Each figure carries a one-line explanation for Alex to drop into Aims 1.1 / 1.2 (to be written with the figure captions once the E. coli real-model runs finish).

### 2.11 (8 Oct, 18:20) Three additions after the user's review: E. coli seeds, DNABERT-2 (BPE), all of Alex's real datasets

Decision (user, 8 Oct evening): paper writing waits until the experiments are complete. Three items added.

**(1) DNABERT causal on E. coli, seeds 1 and 2** — same settings as seed 0 (3.9): `tmux ecoli_s12`, `pilot2/queue_ecoli_s12.sh`, one k per GPU, seeds in sequence, then `analyze_dnabert` over `outputs/dnabert_ecoli`. About 1 h per run.

**(2) DNABERT-2 = the BPE member of the real-model family** — `pilot2/dnabert2.py` (commit e29fb56). Model `zhihan1996/DNABERT-2-117M` (117M, BPE vocab 4096, ALiBi, non-overlapping tokens 1–32 nt, mostly 5–8), downloaded with curl via hf-mirror to `/data/wh/yqdata/models/DNABERT2` (the repo has no `special_tokens_map.json`; the first attempt saved a 404 page under that name, deleted). Load test: tokenizer round-trips, the MLM head is in the checkpoint (`cls.predictions.*`), masked-token prediction works (log p = −0.04 for an easy token). Triton flash attention fails on the server (`libcuda.so` stub), so the module's exact PyTorch attention path is forced.
  * Scoring is per TOKEN, converted to bits per nucleotide by dividing by the nucleotides the scored tokens cover (there is no exact per-nt probability with variable-length tokens). Probe score = tokens overlapping the 96-nt span; floor = whole window.
  * `--objective causal` folds a causal mask into the ALiBi bias (upper triangle −1e4); verified that changing the last 5 tokens leaves earlier logits unchanged (max diff 0.0). `--objective mlm` = native head, 15 % token masking, PLL scoring.
  * Extraction reveals the tokens ending at or before offset+48 (the recorded `k_revealed_nt` is ≤ 48, typically 44–48), then decodes greedily. For mlm the unknown region keeps the true token layout (number and length of masked slots), a mild advantage to the model; stated here and to be stated in the paper.
  * Output files have the same shape as `dnabert.py`; out dirs `dnabert2bpe[_causal][_<data>]_s<seed>`; `analyze_dnabert.py` lists them as k = "BPE" after the 6-mer.
  * Smoke tests pass (causal E. coli: floor 2.74 → 2.10 after one epoch; mlm synthetic 2.04 → 1.95).

**(3) All real datasets from Alex's configs** (`config/*.yaml`, `src/data/real_data_loader.py`): E. coli (have), **yeast S288C R64** (GCF_000146045.2, 12.1 Mb, 17 chromosomes → 42,212 windows; downloaded from NCBI), **GUE human promoters prom_300_all** (`leannmlindsey/GUE`, 47,357 train rows of 300 nt, centre-cropped to 288 → 47,356 windows; csv fetched from hf-mirror because `datasets` fails to import on the server (libsndfile)). GRCh38 is listed in his loader but his paper uses GUE for human; not downloaded (3 GB). `real_data.py` now has `DATA_PATHS` / `load_windows` (FASTA → windows, CSV → one window per row) and all three CLIs plus `run_pilot.py` take `--data ecoli|yeast|gue` (`--fasta` only overrides). Order-0 entropy of the windows: E. coli 1.9998, GUE 1.983, yeast 1.959 bits/nt.

Launched `tmux bpe_real` (`pilot2/queue_1008b.sh`) and `tmux bpe_ecoli` (the BPE E. coli line relaunched after a wrong `--stride` flag), alongside `ecoli_s12`:

| GPU | jobs (in order) | out |
|---|---|---|
| 0 | DNABERT-2 causal, E. coli, seeds 0/1/2, 50 ep | `outputs/dnabert_ecoli/dnabert2bpe_causal_ecoli_s*` |
| 1 | DNABERT 3/4/5/6 causal + DNABERT-2 causal on **yeast**, seed 0, 50 ep | `outputs/dnabert_yeast` |
| 2 | same on **GUE** | `outputs/dnabert_gue` |
| 3 | HyenaDNA medium yeast, GUE (50 ep); DNABERT-2 causal **synthetic** seeds 0/1/2 (30 ep, joins `outputs/dnabert`); DNABERT-2 **native MLM** E. coli seed 0 | `outputs/hyena_yeast`, `outputs/hyena_gue`, `outputs/dnabert`, `outputs/dnabert_ecoli` |
| 2+3 | toy backbone AR × char/3mer/6mer × 2 seeds on yeast and GUE (as `ecoli_ar`) | `outputs/yeast_ar`, `outputs/gue_ar` |

Ends with `ECOLI_S12_DONE` / `QUEUE_1008B_DONE` in `outputs/dnabert_ecoli/queue_s12.log` / `outputs/queue_1008b.log`. Expected finish: E. coli seeds ~4 h; yeast / GUE DNABERT lines ~6–8 h (shared GPUs); all by the morning of 9 Oct.

### 2.12 (8 Oct, 22:00) Downstream utility = GUE promoter detection, DNABERT's own benchmark — `pilot2/downstream.py` (e2a0d5f)

User's question "what is utility, which metric?" → answer: held-out bits/nt on unseen windows of the same genome, i.e. language-model utility, not a downstream task. User's decision: since GUE prom_300_all is the benchmark the DNABERT papers themselves use, add it.

Design (`--downstream` flag in `dnabert.py`, `dnabert2.py`, `hyena.py`; evaluated at epoch 0, every snapshot and the final model, stored under `downstream` in the score json):
  * **linear probe** — frozen mean-pooled last hidden state → logistic regression; cheap; representation quality.
  * **fine-tune** — DNABERT-2 recipe scaled down: deep copy of the model + linear head, AdamW 3e-5, batch 32, 2 epochs on 20k labelled train rows (paper: 3 epochs on all 47k); the copy is discarded, the memorisation run is untouched.
  * Metric: accuracy and **MCC** (the GUE metric) on the full 5,920-row test split, which is disjoint from the training file.
  * Smoke test (10k rows / 1 epoch / 1k test) before any fine-tuning: MCC 0.45–0.48 for all three families (DNABERT-3 causal-masked, DNABERT-2 causal, HyenaDNA). Per-snapshot cost ≈ 1–3 min.
  * `analyze_real.py` gains two columns (probe MCC, fine-tune MCC) and a third table: the epoch with the best downstream MCC and the canary status there — the utility optimum by DNABERT's own metric.

Launched `tmux gue_ds` (`pilot2/queue_gue_ds.sh`): GUE rerun of DNABERT 3/4/5/6 causal, DNABERT-2 BPE causal and HyenaDNA medium with the probe at every snapshot → `outputs/dnabert_gue_ds`, `outputs/hyena_gue_ds`; ends `GUE_DS_DONE` in `outputs/queue_gue_ds.log`. The earlier GUE runs (3.14) stay as they are.

### 2.13 (8 Oct, late) Downstream panel widened: human-wide GUE tasks + yeast histone marks (323d410)

User's question "why only prom_300_all, what about the other species?" → answer: the utility task must match the fine-tuning data (human promoters → human task); GUE has no bacterium; mouse / virus / fungi-species tasks measure transfer, not utility on the fine-tuned data. User's decision: add (A) a wider human panel and (B) yeast-matched tasks, queued on the server.

`pilot2/downstream.py` generalised to any list of GUE tasks (`--downstream_tasks`, default by `--data`: gue → prom_300_all; yeast → emp_H3, emp_H3K4me3). Multi-class MCC via sklearn (splice has 3 classes). Downloaded from hf-mirror: prom_core_all (70 nt, 53k train), human_tf_0 (100 nt, 32k), splice_reconstructed (400 nt, 36k, 3 classes), emp_H3 and emp_H3K4me3 (500 nt yeast histone-mark sets, 12–33k). `analyze_real.py` prints per-task MCC columns and uses the mean over tasks for the best-downstream table.

Queued `tmux ds2` (`pilot2/queue_ds2.sh`), which starts after `gue_ds` finishes and the smoke test passes (`outputs/DS2_GO`):
  (A) GUE memorisation runs with the human-wide panel prom_core_all + human_tf_0 + splice at every snapshot → `outputs/dnabert_gue_ds2`, `outputs/hyena_gue_ds2`;
  (B) yeast memorisation runs with emp_H3 + emp_H3K4me3 at every snapshot → `outputs/dnabert_yeast_ds`, `outputs/hyena_yeast_ds`.
Six models each (DNABERT 3/4/5/6 causal, DNABERT-2 BPE causal, HyenaDNA medium), seed 0, 50 epochs. Ends `DS2_DONE` in `outputs/queue_ds2.log`. E. coli keeps the language-model utility only (no bacterial task in GUE) — to be stated in the paper.

### 2.14 (9 Oct, 05:00-06:00) The four RECOMB hardening items, queued

After the "can this win RECOMB" discussion the user asked for the first four of the five items on
the list. Item 2 was already running; items 1, 3 and 4 were built tonight.

**(1) The from-scratch BPE cell** — `pilot2/bpe_arm.py` (aef2380). DNABERT-2 shows that the BPE model
memorises most, but it also has 117M instead of 86-89M parameters, ALiBi instead of learned absolute
positions and a different pretraining corpus, so it cannot isolate the tokenizer. This trains the SAME
12.9M backbone as `run_pilot.py` with a BPE vocabulary, so char / 3mer / 6mer / BPE differ in the
tokenizer and nothing else. Forced differences, stated with the results: AR only (variable-length tokens
are right-padded and a bidirectional objective would leak through the pads, so BPE+MLM stays with
`dnabert2.py`, which has a native attention mask); scores are token sums divided by the nucleotides those
tokens cover; the embedding table is larger (the capacity controls `--emb_rank` / `--d_ff` still apply).
Four BPE vocabularies trained with `pilot2/train_bpe.py` (now also `--synthetic` and CSV corpora):
synthetic k=4.83, E. coli k=5.01, yeast k=5.05, GUE k=4.9 nt/token. Output names (`bpe4096_ar_s0`,
`bpe4096_ecoli_ar_s0`, ...) are read by `analyze_traj.py`, so the BPE rows land in the matched-overfitting
table next to the k-mer cells.

**(3) Real human canaries** — `pilot2/human_canary.py`, `pilot2/analyze_human.py` (318060f, 2421ef8).
Downloaded hg38 chr22 (51 Mb) and the 1000 Genomes phase-3 phased VCF for chr22 (2,548 samples, 186 MB).
A canary is now a REAL haplotype segment: 96 nt of chr22 centred on a variant with AC/AN <= 0.001 and at
most 5 carriers, with the carrier's alternate allele substituted at every rare variant in the window.
400 canaries, 366 distinct carriers, 2.07 rare variants each, AF mean 3.5e-4, max 9.8e-4, GC 43 %.
Non-members come from the same pool, so the control is equally real and equally rare and differs only in
having been trained on. Every extraction now records the decoded bases, so `analyze_human.py` can score
the privacy-relevant question per variant: did the model return the individual's rare allele, the
reference base (the null), or neither. `--canary_npz` works in all four model CLIs.
Two notes for the write-up: the INFO AF field of that VCF is rounded to two decimals, so every variant
rarer than 1 % reads as 0.00 and the frequency must come from AC/AN (this silently produced zero canaries
at first); and a real segment is in-distribution, so part of it is predictable from biology, which makes
this test strictly more conservative than the random-canary one.

**(4) Mechanism, per-token accounting** — `pilot2/token_info.py`. A 96-nt canary is 192 bits for every
tokenizer; what changes is the number of token slots carrying them (char 96, 3-mer 32, 6-mer 16, BPE ~20)
and the information per slot. The script re-reads the saved scores and reports memorisation at matched
held-out loss both per nucleotide (the result) and per token slot (the explanation), plus the corpus
statistic behind it: how often the tokens making up a canary occur elsewhere in the training corpus, and
what fraction never occur at all. If a model stores a roughly fixed amount per slot, the per-nucleotide
curves that separate by tokenizer should move together per slot, and the residual is what the tokenizer
explains beyond slot counting. Figure with both panels via `--plot`.

**Infrastructure note.** Mutagen had stalled for hours staging a 238 MB chr22 VCF left in `data/1000g/`
by an earlier session, which blocked all code from reaching the server. Large corpora now live outside the
synced tree in `/data/wh/yqdata/glm_data` (1000g, human, gue) and the code takes the root from
`GLMEXT_DATA` (default `data`), so a download can never block the sync again. Tonight's code also went up
with `scp` to bypass the backlog.

**Queued.** `tmux night1009` (`pilot2/queue_night1009.sh`), after the prep smoke tests passed:
  * phase A, now, 4 GPUs: BPE cell on synthetic (2 seeds), E. coli (2 seeds), yeast, GUE, 30 epochs with
    snapshots; then `analyze_traj` against core100 / ecoli_ar and `token_info` for both;
  * phase B, after `tmux seeds12` finishes so the GPUs are not oversubscribed: real human canaries on
    chr22 for DNABERT 3/4/5/6 causal, DNABERT-2 BPE, HyenaDNA medium and the from-scratch BPE cell,
    50 epochs, snapshots 1/3/8/15/30/50 plus the pre-fine-tuning baseline;
  * phase C: `analyze_real`, `analyze_human`, `analyze_dnabert` over `outputs/human_real`.
Ends `NIGHT1009_DONE` in `outputs/queue_night1009.log`. Still running alongside: `tmux ds2` (human-wide
GUE panel + yeast histone tasks) and `tmux seeds12` (yeast / GUE seeds 1 and 2), both from 2.13.

---

## 3. Results (to be filled as runs finish)

- [x] 2.3 DNABERT family (seeds 0, 1): table from `pilot2.analyze_dnabert` → `outputs/dnabert/dnabert_report.md`
- [x] 2.5 E. coli AR
- [x] 2.5 synthetic MLM core
- [x] 2.5 RoPE char 100 epochs (DNABERT seed 2 of the original setting dropped; causal seeds 1–2 running)
- [x] 2.5 E. coli MLM

### 3.1 DNABERT family — causal variant: the pre-registered ordering holds (seed 0; seeds 1, 2 running in `tmux dnabert3`)

`outputs/dnabert/dnabert_report.md`, epoch 30, lr 2e-5, random placement; cells = bits/nt / rank-1 / exact:

| k | held-out floor | r=4 training host | r=16 training host | **r=16 in a new host, new offset** |
|---|---|---|---|---|
| 3 | 2.002 | 1.99 / 0.05 / 0 | 1.99 / 0.10 / 0 | 2.00 / **0.00** / 0 |
| 4 | 2.005 | 1.99 / 0.05 / 0 | 1.96 / 0.35 / 0 | 1.97 / **0.30** / 0 |
| 5 | 2.012 | 1.96 / 0.25 / 0 | 1.86 / 1.00 / 0 | 1.86 / **0.90** / 0 |
| 6 | 2.045 | 1.83 / 0.80 / 0 | 1.23 / 1.00 / 0 | 1.29 / **1.00** / 0.10 |

- **3 < 4 < 5 < 6 on every column**, at the same learning rate, epochs and (nearly identical, 2.00–2.05) held-out floors. False positives 0–3%. Epoch 0 (pretrained weights under a causal mask) is far from fitted (2.8–4.7 bits) and reaches ~2.0 after one epoch for every k, so all four start the comparison from a common point.
- Trajectory: k=6 reaches rank-1 100% at epoch 15, k=5 at 30, k=4 35% at 30, k=3 never within 30 epochs.
- **Unlike our from-scratch absolute-position models, the pretrained DNABERT models recognise the canary in a new host at a new offset as well as in its training host** (k=6: 100% / 100%; k=5: 90% / 100%). The memory is content-based. This is the privacy-relevant case.
- **MLM with equalised hidden-nucleotide rate (5%, lr 1e-4):** r=16 training host 2.00 / 1.89 / 1.96 / 1.73 bits (k = 3/4/5/6), rank-1 0 / 15 / 15 / 75%. Same direction, weaker, with a 4/5 swap inside noise (20 probes). k=6 snapshot scoring was still running at 07:00.
- Still open: seeds 1 and 2 (running). A matched-floor comparison is not possible here because nothing overfits in 30 epochs at lr 2e-5; the comparison is at matched epochs with the floors reported.

### 3.2 Real genome (E. coli, `outputs/ecoli_ar/`, AR × 3 tokenizers × 2 seeds, 50 probes/tier, random placement)

| | char | 3mer | 6mer |
|---|---|---|---|
| r=1 bits/nt at matched floor 2.10 / 2.20 | 1.84 / — | 1.58 / 1.36 | **1.05 / 0.68** |
| r=16 at own training host, epoch 30 (bits / rank-1 / exact) | 1.77 / 0.97 / 0 | 0.02 / 1.00 / 1.00 | 0.02 / 1.00 / 1.00 |
| r=16 in a new host, new offset (rank-1) | 1% | 8% | **48%** (in-phase, n=94) |
| non-member false positives | 0% | 0% | 1% |

The tokenizer order holds on real DNA and the gap is wider than on synthetic data (at 2.10: 1.84 / 1.58 / 1.05 vs 1.89 / 1.74 / 1.21). Held-out "floors" are above 2.0 for char (2.11–2.16) because a 12.9M model trained on 5,000 windows does not learn E. coli structure; the chance line is no longer exactly 2.000, so only within-corpus comparisons are made. `outputs/ecoli_mlm/` (MLM@0.15/0.5, seed 0, 40 probes): little memorisation in 30 epochs, 6mer most (r=16 rank-1 12–28%).

### 3.3 Masked objective under random placement (`outputs/core_mlm/`, 40 probes/tier, 2 seeds) and the combined decomposition

- r=16 training host, pll: char 1.999 / 3mer 1.98–1.99 / 6mer 1.92–1.93; rank-1 0 / 3–12 / 57–72%; extraction 0 everywhere. Masked models memorise far less than the fixed-placement week-2 numbers suggested (then: 3mer@0.5 0.16, 6mer@0.5 0.11).
- **Combined two-way decomposition, random placement, seeds 0+1 (`outputs/core_all/`, AR from core100 + MLM from core_mlm): objective 57.7%, tokenizer 15.4%, interaction 26.9%, seed 0.0%.** Within masked models the tokenizer explains 97.8%; within causal models 100%.
- **This changes the headline.** Under fixed placement (week 2, `tok1`) the split was tokenizer 59.5 / objective 25.7. Under random placement the objective dominates, because causal models memorise whole training examples (k-mer bits ≈ 0.01) while masked models barely memorise at 30 epochs, and char AR also stays near 1.95. The honest statement: *the objective decides whether whole examples are memorised; within an objective, the tokenizer decides almost everything else.* Both tables go in the paper, labelled by placement.

### 3.4 RoPE char at 100 epochs (`outputs/rope_char100/`)

Own training host: r=16 fully memorised by epoch 100 (0.01 bits, 93% extraction) at a held-out floor of 10.6–10.9 bits (extreme overfitting). In a new host: still 0%. The matched-floor r=1 curve coincides with absolute-position char (1.797 vs 1.773 at 2.20). For char, relative positions change nothing; position-free recognition of a repeated sequence appears only with k-mer tokenizers.

### 3.5 Pointers

Copies in `claude_notes/figures/`: `dnabert_dnabert_report.md`, `core_all_tok_analysis_r16_train.md`, `core_mlm_tok_analysis_r16_train.md`, `ecoli_ar_trajectory.md/.png`, `ecoli_ar_offset_report.md`, `core100_*`, `rope_char100_trajectory.md`.

### 3.6 DNABERT causal, three seeds (`tmux dnabert3` done 08:25): the ordering is stable

Epoch 30, mean of seeds 0/1/2 (`outputs/dnabert/dnabert_report.md`, rows `causal`):

| k | floor | r=16 training host (bits / rank-1 / exact) | r=16 new host | r=4 training host |
|---|---|---|---|---|
| 3 | 2.002 | 1.99 / 0.03 / 0 | 1.99 / 0.07 / 0 | 2.00 / 0.03 / 0 |
| 4 | 2.006 | 1.96 / 0.37 / 0 | 1.96 / 0.37 / 0 | 1.99 / 0.08 / 0 |
| 5 | 2.011 | 1.86 / 0.88 / 0 | 1.85 / 0.92 / 0 | 1.96 / 0.25 / 0 |
| 6 | 2.042 | 1.23 / 1.00 / 0.03 | 1.32 / 1.00 / 0.10 | 1.83 / 0.80 / 0 |

Monotone in k on every column with three seeds; false positives ≤ 1%. New-host recognition equals training-host recognition (content memory).

### 3.7 HyenaDNA (`tmux hyena1` done ~09:40): the pretrained character model memorises far MORE than the DNABERT family

`outputs/hyena/*.log` (summary lines), 30 epochs, lr 2e-5 unless noted, random placement, pool 500:

| model (params) | epoch | floor | r=1 training host | r=16 training host (bits / rank-1 / exact) | r=16 new host |
|---|---|---|---|---|---|
| medium-160k (14.24M), seed 0 | 0 | 2.094 | 2.09 / 0 / 0 | 2.07 / 0 / 0 | 2.07 / 0 / 0 |
| | 15 | 2.032 | 1.94 / 0.55 / 0 | **0.21 / 1.00 / 0.95** | 0.26 / 1.00 / 1.00 |
| | 30 | 2.445 | 1.59 / 1.00 / 0 | 0.14 / 1.00 / 0.70 | 0.31 / 1.00 / 0.65 |
| medium, seeds 1 / 2 at epoch 30 | 30 | 2.39 / 2.35 | 1.60 / 1.58 | 0.13 / 0.16 (rank-1 1.00, exact 0.95 / 0.65) | 0.33 / 0.48 |
| medium, lr 1e-4 | 30 | 2.349 | 1.43 / 1.00 / 0 | 0.12 / 1.00 / 0.65 | 0.76 / 0.95 / 0.20 |
| small-32k (3.28M) | 30 | 2.192 | 1.68 / 1.00 / 0 | 0.22 / 1.00 / 0.85 | 0.64 / 1.00 / 0.25 |

Reading.
- HyenaDNA, a **single-nucleotide** model, memorises the 16× canaries almost completely by epoch 15 (0.21 bits, 95% verbatim extraction, 100% recognition in a new host) at a held-out floor of only 2.03. DNABERT-6 (causal) reaches 1.23 bits and 3% extraction at epoch 30 with floor 2.04. So **across architectures the tokenizer ordering does not hold**: the character model memorises more than every k-mer BERT, at the same lr and epochs and at a matched floor.
- Why this is not a contradiction of §3.1 / §3.6: the within-DNABERT comparison varies only k; HyenaDNA vs DNABERT varies architecture (Hyena vs Transformer encoder), size (6.5M vs 89M), pretraining objective (causal vs masked) and, importantly, **objective match**: HyenaDNA is fine-tuned on the objective it was pretrained with, while DNABERT is pretrained masked and fine-tuned causal (its epoch-0 floor under a causal mask is 2.8–4.7 bits). This is exactly the confounded comparison the BCB paper made; our data say that in such a comparison the tokenizer is not the deciding variable.
- It also matches the BCB paper's own observation that HyenaDNA shows the strongest extraction.
- The HyenaDNA memory is content-based (new host ≈ training host), unlike our from-scratch absolute-position toy models.
- Model size note, resolved 20 Oct: the checkpoint named in the BCB config (`hyenadna-medium-160k-seqlen-hf`) has **14,236,768 parameters (14.24M)**, counted from its own state_dict, which agrees with the 14.2M in the paper's Table 1. The 6.55M recorded here earlier was our miscount; no question for Alex arises. Companion counts: tiny-1k 450,712, small-32k 4,069,168.

### 3.8 DNABERT causal at 100 epochs (`tmux dnabert4`, k = 3 and 5 finished; 4 and 6 running)

| k | epoch | floor | r=16 training host | r=16 new host |
|---|---|---|---|---|
| 3 | 50 / 75 / 100 | 2.016 / 2.089 / 2.195 | 1.93 / 1.72 / 1.36 (rank-1 0.4 / 0.8 / 1.0; exact 0) | 1.96 / 1.95 / 1.84 (rank-1 0.1 / 0.2 / 0.55) |
| 5 | 50 / 75 / 100 | 2.024 / 2.072 / 2.156 | 1.56 / 0.63 / 0.28 (rank-1 1.0; exact 0 / 0.5 / 1.0) | 1.60 / 0.85 / 0.54 (exact 0 / 0.5 / 0.9) |

At a matched floor (k=3 at epoch 100, 2.195, vs k=5 at epoch 75, 2.072) k=5 has memorised far more (0.63 vs 1.36 bits; 50% vs 0% verbatim). So at the real-model scale, too, coarser tokens memorise **more, not only sooner**. k = 4 and 6 to be added when the runs finish.

**3.8 completed (10:40, all four k):** `outputs/dnabert_e100/dnabert_report.md` (copy: `figures/dnabert_e100_report.md`).

| k | floor at epoch 30 / 50 / 75 / 100 | r=16 training host, bits at 30 / 50 / 75 / 100 | exact extraction at 100 | r=16 new host at 100 (rank-1 / exact) |
|---|---|---|---|---|
| 3 | 2.00 / 2.02 / 2.09 / 2.20 | 2.00 / 1.93 / 1.72 / 1.36 | 0% | 55% / 0% |
| 4 | 2.01 / 2.03 / 2.08 / 2.15 | 1.97 / 1.82 / 1.41 / 0.97 | 20% | 100% / 5% |
| 5 | 2.01 / 2.02 / 2.07 / 2.16 | 1.89 / 1.56 / 0.63 / 0.28 | 100% | 100% / 90% |
| 6 | 2.04 / 2.12 / 2.31 / 2.50 | 1.47 / 0.33 / 0.19 / 0.12 | 95% | 100% / 65% |

Interpolated at a matched held-out floor, r=16 canary bits/nt: @2.05: 1.84 / 1.62 / 1.06 / 1.28; @2.10: 1.68 / 1.27 / 0.52 / 0.61 (k = 3 / 4 / 5 / 6). So at the real-model scale coarser k-mers memorise more at equal generalisation cost, with k = 5 and 6 indistinguishable at matched floor (6 overfits faster, so at a fixed epoch it is ahead). For r=1 canaries the matched-floor values are flat across k (1.81–1.89 at 2.10): a single exposure is not memorised by any DNABERT within this budget. Both facts go in the paper as they are.

### 3.9 Real models fine-tuned on the real genome: memorisation vs utility (`tmux real1`, done 13:30)

Utility = held-out loss on unseen E. coli windows (bits/nt, lower = more useful; the pretrained HyenaDNA scores 2.07 on E. coli, the DNABERT models 2.9–4.8 under a causal mask). Canary numbers as before (20 per tier, random placement). Files: `outputs/dnabert_ecoli/dnabert_report.md` (copy `figures/dnabert_ecoli_report.md`), `outputs/hyena_ecoli/*.log`.

**DNABERT family (causal fine-tuning, lr 2e-5, seed 0)** — utility / r=16 canary bits (rank-1, exact):

| k | epoch 8 | epoch 15 | epoch 30 | epoch 50 |
|---|---|---|---|---|
| 3 | 1.939 / 2.05 | 1.908 / 2.02 | 1.890 / 1.94 (0.10, 0) | 1.919 / 1.60 (0.90, 0) |
| 4 | 1.935 / 2.05 | 1.925 / 2.00 | 1.919 / 1.77 (0.60, 0) | 1.932 / 0.90 (1.00, 0.40) |
| 5 | 1.931 / 2.03 | 1.917 / 1.98 | 1.910 / 1.69 (0.90, 0) | 1.934 / 0.58 (1.00, 0.50) |
| 6 | 1.928 / 1.98 | 1.919 / 1.85 (0.50) | 1.922 / 0.99 (1.00, 0.20) | 1.981 / 0.31 (1.00, 1.00) |

**HyenaDNA medium (2 seeds)** — utility / r=16 bits (rank-1, exact): epoch 8: 1.92 / 0.61–0.64 (1.00, 0.30–0.40); epoch 15: 1.96 / 0.27 (1.00, 0.70–0.80); epoch 30: 2.19–2.20 / 0.17–0.18 (1.00, 0.70–0.85); epoch 50: 2.82–2.88 / 0.11–0.12 (1.00, 0.70–0.85). r=1 canaries: 1.67–1.69 at epoch 30, 1.19–1.20 at epoch 50 (rank-1 1.00).

Reading.
1. **Order holds on the real genome with real models**: at epoch 50, r=16 bits 1.60 / 0.90 / 0.58 / 0.31 for k = 3/4/5/6, exact extraction 0 / 40 / 50 / 100%, new-host recognition 90–100% for all four.
2. **Utility peaks early (epoch 15–30 for DNABERT, epoch 8 for HyenaDNA) and memorisation is already under way at the peak.** DNABERT-6 at its best utility (1.92, epoch 30) has the 16× canary at 0.99 bits with 100% recognition and 20% verbatim extraction; HyenaDNA at its best utility (1.92, epoch 8) has it at 0.64 bits with 100% recognition and 30–40% extraction. So **stopping at the utility optimum does not prevent memorisation**, which answers Erman's question directly: the trade-off is not "a little less memorisation for a little less utility"; the canaries are captured before utility starts to degrade.
3. After the utility peak, more epochs only buy more memorisation at a utility cost (HyenaDNA: utility 1.92 → 2.88, worse than before fine-tuning, while the canary goes 0.64 → 0.12).
4. HyenaDNA again memorises more and sooner than any DNABERT at equal utility (0.64 vs 1.85–2.05 bits at utility ≈ 1.92).
5. Caveat: DNABERT seed 0 only; HyenaDNA 2 seeds agree.

### 3.10 E. coli, real models, 3 seeds + DNABERT-2 (BPE) (`ecoli_s12`, `bpe_ecoli`; 19:50)

`pilot2/analyze_real.py` (1f180b3) → `outputs/dnabert_ecoli/real_report_ecoli.md` (copy `figures/real_report_ecoli.md`). DNABERT k-mer rows are now 3-seed means; the seed-0 numbers of 3.9 move by ≤ 0.03 bits. DNABERT-2 BPE: 2 seeds done (third running).

**At each model's best-utility epoch** (lowest held-out E. coli loss) — r=16 canary bits / rank-1 / exact extraction, training host:

| model | params | best epoch | utility | r=16 at best | utility at ep 50 | r=16 at ep 50 |
|---|---|---|---|---|---|---|
| DNABERT 3-mer | 86M | 30 | 1.890 | 1.95 / 0.13 / 0 | 1.919 | 1.60 / 0.88 / 0 |
| DNABERT 4-mer | 86M | 30 | 1.915 | 1.77 / 0.60 / 0 | 1.930 | 0.88 / 1.00 / 0.33 |
| DNABERT 5-mer | 87M | 30 | 1.907 | 1.70 / 0.80 / 0 | 1.935 | 0.59 / 1.00 / 0.55 |
| DNABERT 6-mer | 89M | 15 | 1.921 | 1.85 / 0.23 / 0 | 1.988 | 0.30 / 1.00 / 0.98 |
| **DNABERT-2 BPE** | 117M | 8 | 1.955 | **1.31 / 1.00 / 0** | **2.630** | **0.05 / 1.00 / 1.00** |
| HyenaDNA medium (char) | 14.24M | 8 | 1.917 | 0.62 / 1.00 / 0.35 | 2.849 | 0.12 / 1.00 / 0.77 |

Reading.
1. **BPE extends the k-mer line**: within the DNABERT family the coarser the tokenizer, the more is memorised at matched epochs (ep 15: 3/4/5/6-mer 2.02/2.00/1.97/1.85 vs BPE 0.25 bits; ep 50: 1.60/0.88/0.59/0.30 vs 0.05). At its own best-utility epoch BPE already has 100 % recognition of the 16× canary; the k-mers 13–80 %.
2. **BPE also destroys utility fastest**: held-out loss 1.95 (ep 8) → 2.63 (ep 50), worse than the untuned model's 2.74 is approached; the k-mer models stay at 1.92–1.99. The BPE model trades utility for memorisation like HyenaDNA does, the k-mer models do not (yet) at 50 epochs.
3. Caveat for the paper: DNABERT-2 has 117M parameters vs 86–89M, a different position scheme (ALiBi vs learned absolute) and non-overlapping tokens, so "BPE" here is "the BPE model", not the tokenizer alone. The from-scratch BPE arm (same backbone) is what separates the two; it is on the list.
4. HyenaDNA remains the cross-architecture exception (char-level but memorises most per unit of utility), as in 3.7/3.9.
5. The matched-floor interpolation in `dnabert_report.md` is undefined on real data (floors < 2.0); use the best-utility table instead.

### 3.11 From-scratch backbone (AR, char / 3-mer / 6-mer) on all three real datasets (`bpe_real`, toy lines; 19:53)

Same protocol as `ecoli_ar` (3.3): 5,000 real windows + canaries, 50 per tier, 2 seeds, 30 epochs, snapshots scored. Files `outputs/{ecoli,yeast,gue}_ar/trajectory.md`.

**r=16 canary bits/nt at matched held-out loss** (mean of 2 seeds; char never overfits to 2.03 on yeast / GUE within 30 epochs):

| dataset | tok | @2.03 | @2.05 | @2.10 | @2.20 | @2.40 |
|---|---|---|---|---|---|---|
| E. coli | char | 1.88 | 1.86 | 1.80 | — | — |
| E. coli | 3-mer | 1.63 | 1.58 | 1.46 | 1.21 | 0.95 |
| E. coli | 6-mer | 1.15 | 1.05 | 0.81 | 0.48 | 0.09 |
| yeast | 3-mer | 1.67 | 1.62 | 1.50 | 1.26 | 1.03 |
| yeast | 6-mer | 1.19 | 1.08 | 0.85 | 0.49 | 0.06 |
| GUE (human promoters) | 3-mer | 1.72 | 1.67 | 1.55 | 1.32 | 1.07 |
| GUE (human promoters) | 6-mer | 1.19 | 1.08 | 0.82 | 0.46 | 0.05 |

Same-epoch view, epoch 12 r=16 bits: E. coli 1.09 / 0.57 (3-mer / 6-mer), yeast 1.26 / 0.59, GUE 1.34 / 0.59; char at epoch 30: 1.77 / 1.94 / ≈1.9.

Reading: **the tokenizer effect is the same on all three real genomes, to within a few hundredths of a bit** — 6-mer > 3-mer > char at every matched floor, with the 6-mer/3-mer gap ≈ 0.5–0.65 bits at @2.10 on each. The organism (bacterium, yeast, human promoters) does not change the ordering or its size; what the data contributes is only the level of the held-out floor (E. coli 1.91, yeast 1.93, GUE 1.92 at best). This is the dataset-generality claim for the paper: one table, three genomes, one ranking.

### 3.12 DNABERT-2 (BPE) on synthetic data, 3 seeds, next to the k-mer rows (`bpe_real` GPU3; 20:18)

`outputs/dnabert/dnabert_report.md` now has the BPE rows (30 epochs, causal, same schedule as the 3/4/5/6-mer runs). r=16 canary bits / rank-1 / exact extraction, training host:

| k | epoch 15 (floor) | epoch 30 (floor) | matched @2.03, r=16 |
|---|---|---|---|
| 3 | 2.00 / 0 / 0 (2.001) | 1.99 / 0.03 / 0 (2.002) | — |
| 4 | 2.00 / 0.07 / 0 (2.002) | 1.96 / 0.37 / 0 (2.006) | — |
| 5 | 1.97 / 0.30 / 0 (2.004) | 1.86 / 0.88 / 0 (2.011) | — |
| 6 | 1.89 / 1.00 / 0 (2.009) | 1.23 / 1.00 / 0.03 (2.042) | 1.47 |
| **BPE** | **0.28 / 1.00 / 1.00** (2.063) | 0.14 / 1.00 / 0.98 (2.281) | **1.11** |

Reading: on iid synthetic DNA, where nothing but the canaries can be learned, the BPE model memorises more than the 6-mer at the same epoch and also at the same held-out floor (1.11 vs 1.47 bits at 2.03), and it is the only DNABERT that reaches verbatim extraction (100 % at epoch 15). The ordering 3 < 4 < 5 < 6 < BPE is monotone in every column. Same caveat as 3.10 (117M params, ALiBi, non-overlapping tokens).

### 3.13 DNABERT-2 (BPE) under its NATIVE masked objective on E. coli (`bpe_real` GPU3; 20:50)

One seed, 15 % token masking (DNABERT-2's own pretraining objective), PLL scoring; utility here is PLL bits/nt, not comparable to the causal floors. r=16 canary bits / rank-1 / exact extraction:

| epoch | PLL utility | r=1 train | r=4 train | r=16 train | r=16 fresh |
|---|---|---|---|---|---|
| 0 | 1.872 | 2.01 / 0 / 0 | 1.98 / 0.10 / 0 | 2.02 / 0.10 / 0 | 2.02 / 0 / 0 |
| 8 | 1.572 | 1.96 / 0 / 0 | 1.87 / 0.10 / 0 | 1.68 / 0.80 / 0 | 1.71 / 0.80 / 0 |
| 15 | 1.568 (best) | 1.94 / 0.30 / 0 | 1.71 / 0.70 / 0 | **0.70 / 1.00 / 0** | 0.74 / 1.00 / 0 |
| 30 | 1.594 | 1.72 / 0.60 / 0 | 0.95 / 1.00 / 0 | 0.05 / 1.00 / 0.30 | 0.14 / 1.00 / 0.70 |
| 50 | 1.644 | 1.47 / 0.90 / 0 | 0.38 / 1.00 / 0 | 0.02 / 1.00 / 0.30 | 0.16 / 1.00 / 0.50 |

Reading. **With non-overlapping BPE tokens the native 15 % masked objective memorises strongly** (16× canary at 0.70 bits with 100 % recognition at the utility optimum, 0.05 bits by epoch 30, verbatim extraction 30–70 %). This is the opposite of the DNABERT k-mer result under the same nominal objective (3.1: no memorisation at 15 % token masking), and the difference is exactly the overlap: masking 15 % of overlapping k-mers hides only 15 %/k of nucleotides, masking 15 % of BPE tokens hides 15 % of nucleotides. So "masked models memorise less" in the real-model family is a property of overlapping k-mer masking, not of the masked objective as such; the from-scratch grid (non-overlapping k-mers) already showed MLM memorising at a 0.5 mask rate. Verbatim extraction under MLM is lower than under causal (30 % vs 100 % at epoch 30), matching the toy-grid pattern "masked models recognise but extract less".

### 3.14 Real models on yeast and GUE (human promoters): the three-genome picture (`bpe_real`; all done 21:17)

Seed 0 only on yeast / GUE (E. coli has 3 seeds, 3.10). Reports: `outputs/dnabert_{yeast,gue}/real_report_{yeast,gue}.md` (copies in `figures/`). Causal fine-tuning, 50 epochs.

**r=16 canary bits/nt at epoch 30 and 50, training host** (rank-1 is 1.00 for every cell at epoch 50; exact extraction in brackets at epoch 50):

| model | E. coli ep30 | ep50 | yeast ep30 | ep50 | GUE ep30 | ep50 |
|---|---|---|---|---|---|---|
| DNABERT 3-mer | 1.95 | 1.60 (0) | 1.48 | 0.75 (0.70) | 1.94 | 1.54 (0.05) |
| DNABERT 4-mer | 1.77 | 0.88 (0.33) | 1.37 | 0.53 (0.85) | 1.77 | 1.00 (0.25) |
| DNABERT 5-mer | 1.70 | 0.59 (0.55) | 0.93 | 0.37 (1.00) | 1.61 | 0.50 (0.75) |
| DNABERT 6-mer | 0.99 | 0.30 (0.98) | 0.43 | 0.20 (1.00) | 0.88 | 0.30 (0.85) |
| DNABERT-2 BPE | 0.12 | 0.05 (1.00) | 0.14 | 0.06 (1.00) | 0.14 | 0.04 (1.00) |
| HyenaDNA medium | 0.17 | 0.12 (0.77) | 0.17 | 0.13 (0.70) | 0.16 | 0.11 (0.70) |

**At each model's best-utility epoch** — utility / r=16 bits / rank-1 / exact:

| model | E. coli | yeast | GUE |
|---|---|---|---|
| DNABERT 3-mer | ep30 1.890 / 1.95 / 0.13 / 0 | ep15 1.926 / 1.96 / 0.20 / 0 | ep30 1.911 / 1.94 / 0.30 / 0 |
| DNABERT 4-mer | ep30 1.915 / 1.77 / 0.60 / 0 | ep15 1.927 / 1.97 / 0.10 / 0 | ep15 1.917 / 1.99 / 0.00 / 0 |
| DNABERT 5-mer | ep30 1.907 / 1.70 / 0.80 / 0 | ep15 1.937 / 1.89 / 0.50 / 0 | ep15 1.922 / 1.94 / 0.30 / 0 |
| DNABERT 6-mer | ep15 1.921 / 1.85 / 0.23 / 0 | ep8 1.939 / 1.94 / 0.20 / 0 | ep15 1.901 / 1.83 / 0.90 / 0 |
| DNABERT-2 BPE | ep8 1.955 / 1.30 / 1.00 / 0 | ep3 1.952 / 1.92 / 0.90 / 0 | ep3 1.933 / 1.92 / 0.80 / 0 |
| HyenaDNA medium | ep8 1.917 / 0.62 / 1.00 / 0.35 | ep8 1.929 / 0.41 / 1.00 / 0.60 | ep3 1.900 / 1.95 / 0.15 / 0 |

Reading.
1. **The ordering 3 < 4 < 5 < 6 < BPE holds on all three genomes at epoch 30 and at epoch 50**, every column monotone (one tie-level exception: GUE 4-mer vs 3-mer at ep30 is 1.77 vs 1.94, still ordered). The absolute levels are close across genomes (6-mer ep50 0.30 / 0.20 / 0.30; BPE 0.05 / 0.06 / 0.04). Together with 3.11 (from-scratch backbone) this is the dataset-generality result: organism changes the held-out floor, not the ranking.
2. **"Early stopping at best utility" is not a defence, but how much it leaks depends on the model**: at the utility optimum the k-mer DNABERTs have the 16× canary at 1.83–1.99 bits with 0–90 % recognition and no extraction; DNABERT-2 BPE already 80–100 % recognition on all three genomes (and 1.30 bits on E. coli); HyenaDNA 0.41–0.62 bits with 35–60 % verbatim extraction on E. coli and yeast. On GUE HyenaDNA's utility optimum is at epoch 3, before capture (by epoch 8 it is at 0.26 bits — not shown — while utility is only 0.005 worse). So the honest statement is: the utility optimum sits on the steep part of the memorisation curve, and the margin between "best utility" and "canary captured" is a few epochs at most.
3. **After the optimum every model trades utility for memorisation**: utility at epoch 50 is worse than at the optimum by 0.03–0.06 (k-mer), 0.6–0.7 (BPE) and 0.7–0.9 bits (HyenaDNA), while the canaries go to ≤ 0.3 bits.
4. Yeast makes the k-mer models memorise a little more than E. coli / GUE at equal epochs (ep50 3-mer 0.75 vs 1.60 / 1.54), plausibly because its windows are more predictable (entropy 1.96 vs 1.98–2.00), so the model has spare capacity sooner; a point for the discussion, not a result.
5. Caveats: single seed on yeast / GUE; DNABERT-2 has more parameters; HyenaDNA utility is measured with its native head, DNABERT with a causal mask on a bidirectional encoder (its ep0 utility is 2.7–4.8, so the fine-tuning first has to repair that).

### 3.15 Downstream utility (GUE promoter detection) vs memorisation on GUE, six real models (`gue_ds`; done 04:24, 9 Oct)

`outputs/dnabert_gue_ds/real_report_gue_ds.md` (copy `figures/real_report_gue_ds.md`). Seed 0. Columns: LM utility (held-out bits/nt), linear-probe MCC, fine-tune MCC (20k rows × 2 epochs, full 5,920-row test), r=16 canary bits / rank-1 / exact.

| model | ep | LM utility | probe MCC | **ft MCC** | r=16 train |
|---|---|---|---|---|---|
| DNABERT 3-mer | 0 / 15 / 50 | 2.92 / 1.91 / 1.94 | 0.775 / 0.816 / 0.799 | 0.836 / 0.851 / 0.856 | — / 2.03 / 1.54 (1.00, 0.05) |
| DNABERT 4-mer | 0 / 15 / 50 | 2.68 / 1.92 / 1.96 | 0.766 / 0.818 / 0.813 | 0.818 / 0.839 / 0.838 | — / 1.99 / 1.00 (1.00, 0.25) |
| DNABERT 5-mer | 0 / 15 / 50 | 3.29 / 1.92 / 1.96 | 0.782 / 0.809 / 0.802 | 0.843 / 0.857 / 0.858 | — / 1.94 / 0.50 (1.00, 0.75) |
| DNABERT 6-mer | 0 / 15 / 50 | 4.45 / 1.90 / 2.01 | 0.750 / 0.821 / 0.801 | 0.833 / 0.851 / 0.852 | — / 1.83 / 0.30 (1.00, 0.85) |
| DNABERT-2 BPE | 0 / 15 / 50 | 2.74 / 1.97 / **2.61** | 0.739 / 0.779 / 0.768 | 0.810 / 0.817 / 0.826 | — / 0.27 (1.00, 1.00) / 0.04 (1.00, 1.00) |
| HyenaDNA medium | 0 / 15 / 50 | 1.95 / 1.94 / **2.81** | 0.761 / 0.797 / 0.783 | 0.803 / 0.806 / 0.814 | — / 0.23 (1.00, 0.95) / 0.11 (1.00, 0.70) |

Reading.
1. **The downstream metric is blind to memorisation.** Fine-tune MCC moves by ≤ 0.03 over 50 epochs for every model (3-mer 0.836→0.856, BPE 0.810→0.826, HyenaDNA 0.803→0.814) while the 16× canary goes from unmemorised to fully extractable and, for BPE and HyenaDNA, the LM utility collapses (1.97→2.61, 1.94→2.81). The promoter classifier re-learns what it needs during its own fine-tuning; it does not care that the backbone has memorised the training windows.
2. **Selecting the checkpoint by downstream score picks the leakiest one** for 4 of 6 models: the best fine-tune MCC is at epoch 50 for 3-mer, 5-mer, BPE and HyenaDNA, where the 16× canary is at 1.54 / 0.50 / 0.04 / 0.11 bits with 5–100 % verbatim extraction. "Best downstream" is therefore not a defence either, and it is worse than "best LM utility" (3.14), which at least stops before verbatim extraction for the k-mer models.
3. The **linear probe** is the only downstream signal that tracks the LM utility: it peaks at epoch 8–15 (0.81–0.82) and declines slightly after, but by ≤ 0.02, far too little to detect what the canaries show.
4. Levels are sane: DNABERT-2 reports ≈ 0.87 MCC on prom_300_all with the full recipe; our scaled-down probe gives 0.81–0.86 for all models, so the probe is working, not saturated at chance.
5. Caveats: seed 0; the labelled training rows come from the same file as the (unlabelled) memorisation fine-tuning windows (as in any pretrain→fine-tune pipeline); human-wide panel and yeast histone tasks are running (`ds2`).

### 3.16 The from-scratch BPE cell and the mechanism: it is token rarity, not slot counting (`night1009` phase A; 06:33, 9 Oct)

Phase A ran the BPE cell of the tokenizer axis on our own 12.9M backbone (`pilot2/bpe_arm.py`), AR,
30 epochs with snapshots, 50 canaries per tier at random offsets: synthetic and E. coli with 2 seeds,
yeast and GUE with 1. Non-embedding parameters are 12.61M, identical to the k-mer cells, and the
non-member controls stay at the held-out floor throughout with 0 % rank-1 and 0 % extraction, so the
scoring convention (token sums divided by covered nucleotides) is calibrated.

**Matched held-out loss, 16x canary, memorised bits/nt is 2 - probe bits/nt; the table shows probe bits/nt
(lower = more memorised).** Reports `outputs/{core100,ecoli_ar}/trajectory.md` (copies
`figures/bpe_trajectory.md`).

| data | tokenizer (nt/token) | @2.05 | @2.10 | @2.20 | @2.40 |
|---|---|---|---|---|---|
| E. coli | char (1.0) | 1.858 | 1.804 | — | — |
| E. coli | 3-mer (3.0) | 1.583 | 1.458 | 1.207 | 0.947 |
| E. coli | **BPE (5.0)** | **1.344** | **1.115** | **0.608** | **0.294** |
| E. coli | 6-mer (6.0) | 1.050 | 0.811 | 0.475 | 0.085 |
| synthetic | 3-mer | 1.864 | 1.757 | 1.567 | 1.235 |
| synthetic | **BPE (4.7)** | 1.445 | 1.267 | 0.629 | 0.279 |
| synthetic | 6-mer | 1.598 | 1.124 | 0.578 | 0.160 |

**1. The headline claim has to be corrected.** On a matched backbone the BPE cell sits BETWEEN the 3-mer
and the 6-mer on E. coli, at the position its mean token length (5.0 nt) predicts, and it is never below
the 6-mer. So "BPE memorises most" (3.10, 3.12, 3.14) is a property of DNABERT-2, not of BPE: that model
also has 117M instead of 86-89M parameters, ALiBi instead of learned absolute positions, and a different
pretraining corpus. The tokenizer axis is monotone in **mean token length**, and BPE is simply a tokenizer
with a token length of about 5. This is the control the paper needed and it strengthens the claim, because
the axis now has a continuous parameter rather than a four-way categorical.

**2. One new interaction.** At r=1 the BPE cell memorises LESS than the 3-mer (E. coli @2.10: 1.787 vs
1.580) while at r=16 it memorises more (1.115 vs 1.458). BPE segmentation depends on context, and with
random placement the same canary is cut differently in each host, so a single occurrence contributes to a
different token sequence each time and the evidence does not accumulate; by 16 occurrences it does. The
k-mer cells have a fixed grid (up to phase) and do not show this. Worth one paragraph: it predicts that a
BPE model leaks rare, single-occurrence records less than its token length suggests.

**3. The mechanism is token rarity, not slot counting** (`pilot2/token_info.py`,
`figures/{synthetic,ecoli}_token_info.{md,png}`). A 96-nt canary is 192 bits for every tokenizer; what
changes is the number of slots (char 96, 3-mer 32, BPE 21, 6-mer 16) and how often those tokens occur in
the rest of the corpus (4,000 ordinary windows of E. coli):

| tokenizer | slots per canary | vocab | canary-token corpus count |
|---|---|---|---|
| char | 96.0 | 7 | 287,995 |
| 3-mer | 32.0 | 67 | 6,014 |
| BPE | 20.8 | 4,096 | 400 |
| 6-mer | 16.0 | 4,099 | 47 |

If a model stored a fixed amount per slot, the per-nucleotide curves would collapse when re-expressed per
slot. They do the opposite: at @2.10, r=16, memorised bits per slot are 0.17 (char), 1.63 (3-mer), 0.86
(BPE), 7.14 (6-mer) — a 40x spread, wider than the 7x spread per nucleotide. So fewer slots is not the
explanation; coarse tokenizers store more per slot as well. What does order the four cells, on both
datasets, is the corpus count above: the canary of a 6-mer model is written in tokens that appear 47 times
elsewhere, the canary of a char model in tokens that appear 288,000 times. Storing a rare token costs
almost no interference with ordinary data; storing a frequent one means storing it in context. That is the
sentence the mechanism section should make precise, and it also explains why the effect is monotone in
token length rather than in vocabulary size (the 6-mer and BPE vocabularies are both ~4,100 but their
canary-token counts differ by 8x).

**Limitation to state.** On synthetic data the BPE cell never reaches a held-out floor below 2.084, while
the k-mer cells reach 2.00-2.03, because a 4,096-way softmax over variable-length tokens does not calibrate
to the uniform distribution with 5,000 windows; the matched-floor comparison there is only valid at
@2.10-2.40. On real data (where the distribution is learnable) BPE reaches 2.03 and the comparison is clean
over the whole grid, so E. coli is the primary panel.

### 3.17 The wider human panel: three more GUE tasks, same verdict (`ds2`; k-mer family done 06:38, 9 Oct)

Asked of the GUE fine-tuning runs at every snapshot: core promoter detection (prom_core_all, 70 nt),
transcription-factor binding (human_tf_0, 101 nt) and splice-site reconstruction (splice_reconstructed,
400 nt, 3 classes). Report `outputs/dnabert_gue_ds2/real_report_gue_wide.md`. Fine-tune MCC (20k rows,
2 epochs) in task order TF / core-promoter / splice:

| model | ep 0 | ep 8 | ep 15 | ep 30 | ep 50 | r=16 canary at ep 50 |
|---|---|---|---|---|---|---|
| DNABERT 3-mer | .650 / .628 / .767 | .675 / .642 / .792 | .647 / .636 / .795 | .654 / .640 / .794 | .642 / .636 / .797 | 1.54 bits, 100 % rank-1, 5 % exact |
| DNABERT 6-mer | .664 / .643 / .766 | .653 / .654 / .782 | .660 / .661 / .795 | .655 / .662 / .803 | .646 / .658 / .801 | 0.30 bits, 100 % rank-1, 85 % exact |

Reading.
1. **Same verdict on all four tasks.** Over 50 epochs each task moves by at most 0.04 MCC, with no
downward trend, while the 16x canary goes from unmemorised to 85 % verbatim extraction. Adding tasks does
not rescue the downstream metric as a leakage signal; the promoter result of 3.15 was not a quirk of that
one dataset.
2. **The only downstream number that moves is the linear probe on splice** (0.26 at epoch 0 to 0.41-0.43
by epoch 8-15, then flat). It moves UP: fine-tuning on E. coli-style windows improves the representation
for a task about sequence structure. So the downstream signal that is sensitive to fine-tuning is
sensitive in the wrong direction for leakage detection.
3. One degenerate cell to mention if these numbers are shown: DNABERT-6 at epoch 1 scores MCC 0.000 on
splice, i.e. that 2-epoch 3-class fine-tune collapsed onto one class. It recovers at every later snapshot
(0.78-0.80). With 2 epochs of supervised fine-tuning an occasional collapse is expected; it is not a
property of the checkpoint.

### 3.18 Real human canaries: the carrier's rare allele comes back (`night1009` phase B; 10:00, 9 Oct)

Canaries are real 96-nt haplotype segments of chr22 carrying rare 1000 Genomes variants (AC/AN <= 0.001,
<= 5 carriers; 2.07 variants each). Non-members come from the same pool, so they are equally real and
equally rare and differ only in having been in the training data. Fine-tuning on 5,420 real chr22 windows,
50 epochs, 20 canaries per tier, random placement. Each variant inside the decoded region is one trial with
three outcomes: the carrier's ALT allele, the reference base (the null), or neither. Report
`outputs/human_real/human_report.md` (copy `figures/human_report.md`).

**Epoch 50, rare-allele recovery (trials in brackets) and verbatim extraction of the 48-nt continuation:**

| model | r=16 allele | r=1 allele | non-member allele | r=16 exact | r=1 exact | r=16 bits/nt |
|---|---|---|---|---|---|---|
| DNABERT 3-mer | 0.97 (29) | 0.37 (38) | 0.21 (67) | 0.80 | 0.00 | 0.38 |
| DNABERT 4-mer | 0.86 | 0.32 | 0.19 | 0.75 | 0.00 | 0.43 |
| DNABERT 5-mer | 0.79 | 0.42 | 0.18 | 0.65 | 0.00 | 0.49 |
| DNABERT 6-mer | 1.00 | 0.34 | 0.24 | 0.85 | 0.10 | 0.29 |
| **DNABERT-2 BPE** | **1.00** | **0.82** | 0.31 | **1.00** | **0.55** | 0.04 |
| **HyenaDNA medium** | **1.00** | **0.55** | 0.27 | 0.75 | 0.05 | 0.15 |

Reading.
1. **The privacy statement the paper needs.** Give a fine-tuned model the first 48 nt of a real human
haplotype segment it was trained on and let it continue: the carrier's rare allele comes back 79-100 % of
the time for a segment seen 16 times, against 18-31 % for matched segments the model never saw. Before
fine-tuning every gap is within noise of zero, so this is not sequence predictability; it is the training
data coming back. Whole-segment recovery is 65-100 %.
2. **One occurrence is enough for the two models that memorise most.** DNABERT-2 reproduces a segment seen
ONCE verbatim 55 % of the time and returns its carrier's rare allele 82 % of the time against a 31 %
baseline; HyenaDNA 55 % allele recovery against 27 %. The k-mer family at r=1 is near its baseline
(0.32-0.42 vs 0.18-0.24) with no verbatim extraction except 6-mer at 10 %. So the single-record threat is
real but model-dependent, and it lands on exactly the two models that the earlier arms flagged.
3. **The 16x tier is saturated**, so the tokenizer ordering is not resolvable there (0.79-1.00 across the
k-mer family, all four with ~29 trials). The r=1 tier is where the models separate. The second pass
(below) raises the trials per cell to ~75.
4. **The from-scratch toy backbone is an upper bound, not a threat model.** Trained 30 epochs from random
init on the same 5,420 windows, the 12.9M BPE cell recovers every allele and extracts every segment at
r=1 and r=16 alike (1.00/1.00, 0.009 bits) while scoring 2.78 bits/nt on unseen real sequence, i.e. worse
than chance: it has memorised the corpus instead of learning it. Useful as the ceiling, useless as a model.
5. **One column of this pass is invalid and is being redone.** The ranking pool was uniform random DNA,
which any real human sequence outranks, so non-member rank-1 is 0.45-0.55 and the rank column says nothing
about membership. Fixed (163db5b) by ranking each canary against other real rare-variant segments from the
same pool, which is the matched test: can the model pick this individual's segment out of other people's.
The allele, extraction and bits columns are unaffected. Second pass `tmux human2`
(`pilot2/queue_human2.sh`) re-runs all six models with the real pool and 50 canaries per tier, plus the
toy char / 6-mer cells for the same comparison on real canaries; then `tmux seeds12b` picks up the extra
yeast / GUE seeds that were deferred at 08:45.

### 3.19 Yeast histone marks: six downstream tasks, two organisms, same verdict (`ds2` done 10:53, 9 Oct)

The yeast arm was given the two GUE histone-mark tasks of S. cerevisiae (emp_H3, emp_H3K4me3) at every
snapshot, which is the organism-matched downstream metric for a model fine-tuned on yeast windows.
Report `outputs/dnabert_yeast_ds/real_report_yeast_ds.md`. Fine-tune MCC in task order H3 / H3K4me3:

| model | ep 0 | ep 15 | ep 50 | r=16 canary at ep 50 |
|---|---|---|---|---|
| DNABERT 3-mer | .723 / .253 | .724 / .255 | .722 / .305 | 0.76 bits, 100 % rank-1, 68 % exact |
| DNABERT 6-mer | .718 / .230 | .727 / .243 | .738 / .279 | 0.21 bits, 100 % rank-1, 100 % exact |
| DNABERT-2 BPE | .746 / .000 | .707 / .292 | .737 / .286 | 0.06 bits, 100 % rank-1, 100 % exact |
| HyenaDNA medium | .684 / .229 | .678 / .231 | .693 / .255 | 0.13 bits, 100 % rank-1, 70 % exact |

Reading.
1. **Six tasks, two organisms, one answer.** Across GUE promoter detection, core-promoter detection,
transcription-factor binding, splice-site reconstruction (3.15, 3.17) and now the two yeast histone marks,
no task moves by more than about 0.05 MCC over 50 epochs, and none moves down, while every model goes from
no memorisation to 70-100 % verbatim extraction of the 16x canary. The claim "downstream performance does
not reveal memorisation" is now supported on the task families a GLM paper would actually report.
2. **Calibration of the probe.** On emp_H3 our scaled-down fine-tune reaches 0.68-0.75 MCC against about
0.78 for the published full recipe, so the probe is sound. On emp_H3K4me3 it reaches only 0.23-0.31 against
about 0.70 published: 20k rows, 2 epochs and a mean-pooled linear head are not enough for that task. The
H3K4me3 column should therefore be read as a weak probe, not as a model comparison, and the paper should
say so.
3. Two degenerate fine-tunes to mention if the raw tables are shown: DNABERT-2 at epoch 0 on H3K4me3 and
DNABERT-6 at epoch 1 on splice both score MCC 0.000, i.e. the 2-epoch head collapsed onto one class. Both
recover at every later snapshot.

### 3.20 The tokenizer axis on real human canaries, matched backbone: the character model does not leak (`human_toy`; 11:13, 9 Oct)

Same 12.9M backbone, AR, 30 epochs with snapshots, on 5,420 real chr22 windows with 50 real rare-variant
haplotype canaries per tier at random offsets, ranked against other real rare segments. Two seeds for
char / 3-mer / 6-mer, one for BPE (plus the seed-0 BPE from phase B). Reports
`outputs/human_toy/{trajectory.md,human_report.md,human_token_info.md}`.

**Trajectory, 16x canary (seed means):**

| tokenizer | best held-out loss (epoch) | canary bits there | exact there | state at epoch 30 |
|---|---|---|---|---|
| char | **1.794 (30, still falling)** | 1.612 | **0.00** | floor 1.794, canary 1.612, **0 % exact, allele gap +0.03** |
| 3-mer | 1.775 (5) | 1.667 | 0.00 | floor 3.925, canary 0.006, 100 % exact, allele 1.00 |
| 6-mer | 1.862 (5) | 1.421 | 0.00 | floor 2.347, canary 0.009, 100 % exact, allele 1.00 |
| BPE | 1.878 (5) | 0.813 | **0.14** | floor 2.681, canary 0.008, 100 % exact, allele 1.00 |

Reading.
1. **The strongest form of the result, and it is on real human data.** After 30 epochs the character model
has not begun to memorise: zero verbatim extraction at every tier and every snapshot, and the rare-allele
recovery gap against matched non-members stays within noise of zero (+0.03 at epoch 30). Over the same 30
epochs the 3-mer, 6-mer and BPE cells all reach 100 % verbatim extraction of the canary and recover the
carrier's rare allele every time, at both r=16 and r=1.
2. **And the character model is the most useful one.** Its held-out loss is still falling at epoch 30
(1.794) and is the lowest of the four at that point, while the coarse cells turn up after epoch 5-8 and end
at 2.35-3.93. So on real human sequence the fine tokenizer costs nothing in utility and removes the
leakage; this is the concrete recommendation the paper can make, measured rather than argued.
3. **Onset order is monotone in token length.** First verbatim extraction appears at epoch 5 for BPE
(14 %), epoch 8 for 6-mer (5 %), epoch 8-12 for 3-mer (2-34 %), never for char. At each model's own utility
optimum, char and 3-mer leak nothing, 6-mer nothing yet, BPE already 14 %: the coarser the tokenizer, the
earlier leakage starts relative to the point where one would stop training.
4. **Caveat to state plainly.** 30 epochs is where the coarse cells have long passed their optimum but the
character cell has not reached its own; a longer run would eventually make it memorise too (the
100-epoch RoPE runs on synthetic data showed char memorising late). The claim is therefore about matched
epochs and about the utility optimum, not about an impossibility. The character cell is also the most
expensive per window (96 token slots against 16), so the comparison is at matched data and epochs, not
matched compute; that belongs in the limitations.
5. Corpus statistics behind it, on this human corpus: the canary's tokens occur 287,916 times elsewhere for
char, 6,026 for the 3-mer and 48 for the 6-mer, the same ordering as on E. coli and synthetic data (3.16).

### 3.21 Real human canaries, second pass: corrected ranking pool and 3x the trials (`human2`; 11:20, 9 Oct)

Supersedes the numbers of 3.18. Same six pretrained models, 50 epochs on chr22, but 50 canaries per tier
instead of 20 (97 allele trials at r=16, 81 at r=1, 105 for non-members) and each canary ranked against
other real rare-variant segments instead of uniform random DNA. Report
`outputs/human_real2/human_report.md` (copy `figures/human_report_pass2.md`).

**Epoch 50. Rare-allele recovery / verbatim 48-nt extraction / rank-1 against real segments:**

| model | r=16 allele | r=1 allele | non-member allele | r=16 exact | r=1 exact | r=16 rank-1 | r=1 rank-1 | non-member rank-1 |
|---|---|---|---|---|---|---|---|---|
| DNABERT 3-mer | 0.99 | 0.27 | 0.25 | 0.96 | 0.00 | 1.00 | 0.08 | 0.00 |
| DNABERT 4-mer | 0.98 | 0.26 | 0.27 | 0.86 | 0.00 | 0.86 | 0.04 | 0.00 |
| DNABERT 5-mer | 0.88 | 0.31 | 0.22 | 0.66 | 0.00 | 0.88 | 0.08 | 0.00 |
| DNABERT 6-mer | 0.95 | 0.36 | 0.26 | 0.84 | 0.06 | 0.96 | 0.26 | 0.00 |
| **DNABERT-2 BPE** | **1.00** | **0.84** | 0.29 | **1.00** | **0.56** | 1.00 | — | 0.00 |
| **HyenaDNA medium** | 0.93 | **0.43** | 0.14 | 0.86 | 0.00 | 1.00 | — | 0.00 |

Reading.
1. **The membership signal is now clean.** With a matched real pool the non-member rank-1 rate is 0.00 for
every model (it was 0.45-0.55 against a random-DNA pool, which measured only "is this sequence real"). At
r=16 rank-1 is 0.86-1.00, at r=1 it is 0.04-0.26: membership inference on a real rare segment works when
the record repeats and barely works from one copy, except through extraction.
2. **The single-occurrence result holds with 81 trials.** DNABERT-2 recovers the carrier's rare allele for
a segment seen ONCE 84 % of the time against a 29 % baseline and reproduces it verbatim 56 % of the time;
HyenaDNA 43 % against 14 %. The k-mer family sits on its baseline (0.26-0.36 against 0.22-0.27) with no
verbatim extraction except 6 % for the 6-mer. The split is between models that memorise heavily overall
and models that do not, and it is the same split every other arm found.
3. **Timing.** DNABERT-2's single-copy leak appears late: r=1 allele recovery is 0.19 at epoch 8, 0.33 at
epoch 30 and 0.84 at epoch 50, while its 16x tier is already saturated at epoch 15. A defence based on
early stopping would have to stop before epoch 8, where the 16x tier is already at 0.75.
4. The 16x tier is saturated for all six models (0.88-1.00), so it cannot order the tokenizers; the toy
matched-backbone runs of 3.20 are where the tokenizer effect on real canaries is visible.

### 3.22 (9 Oct, after the 1:1) Erman’s blocking question, and what it really is

Erman stopped at one column of slide 7: whole-segment extraction for the 16x tier on human chr22, which
reads 96 / 86 / 66 / 84 per cent for the 3-, 4-, 5- and 6-mer DNABERT models. He expected it to rise with
k and asked for either an explanation or more runs. Three separate things are going on, and only the last
one needs GPU time.

**1. That column is the worst statistic to order models by.** It is thresholded (all 48 letters correct or
nothing), it is at the 16x tier where every model is near saturation, and it comes from 50 canaries, so one
standard error is about 7 points. The smooth statistic on the same runs is the canary score: 0.33 / 0.40 /
0.43 / 0.28 bits per letter. Still not monotone, so this is not the whole answer.

**2. On real sequence the right statistic subtracts the matched control.** A real canary is ordinary human
DNA, so part of its score is biology the model legitimately learned. `pilot2/analyze_matched.py`
(eec0e70) reports `excess = non-member bits − member bits` at the same checkpoint. On human chr22 at
epoch 50 that gives 1.46 / 1.37 / 1.39 / 1.55 bits for k = 3/4/5/6: flat, with the 6-mer highest, and the
spread (0.18 bits) is the size of the seed-to-seed noise I have not yet measured on this arm. Matched
*utility* turns out not to be available for this family: within 50 epochs these pretrained models barely
overfit on real data, so their held-out-loss ranges are 0.03 to 0.08 bits wide and do not overlap, which
also means the fixed-epoch comparison was already nearly utility-matched.

**3. The real point: the DNABERT family is not the clean tokenizer axis.** DNABERT tokenizes with
OVERLAPPING k-mers (stride 1), so a 288-nt window is 283-286 tokens whatever k is. Changing k there does
not change how many slots carry the canary; it changes the vocabulary and how much neighbouring tokens
overlap. My controlled arm uses NON-overlapping k-mers, where k really does change the slots per canary
(96 / 32 / 16) and the rarity of those slots, and there the ordering is monotone on synthetic DNA, E. coli,
yeast, GUE and human chr22 (3.16, 3.20). So the causal claim rests on the controlled arm, and the DNABERT
family answers a different, model-level question: do the published k-mer releases differ from each other.
On E. coli they come out ordered; on human chr22 they do not, and with overlapping k-mers there is no
strong reason they must. Writing it this way removes the apparent contradiction instead of explaining it
away, and it is a point I should have made two weeks ago.

**A methodological bug found while checking this.** Non-member canaries were being scored inside a
uniform-random host window while members were scored inside their real chromosome window, so the control
differed from the member in host type as well as in membership. For the 3-mer model this is large enough
to make the single-copy excess negative (−0.3 bits). Fixed in eec0e70: when canaries are real, the fresh
host is drawn from unused real windows of the same genome. This invalidates the control column of 3.18 and
3.21 and the single-copy numbers of 3.21, so the human arm is being re-run.

**Queued.** `tmux human3` (`pilot2/queue_human3.sh`), after `seeds12b`: six published models, real fresh
hosts, 50 canaries per tier, three seeds for the k-mer family and for DNABERT-2 and HyenaDNA, then
`analyze_real`, `analyze_human` and `analyze_matched`. That is the table for the paper and the answer to
Erman’s question with error bars.

### 3.23 Three seeds settle it: the published k-mer family IS ordered, and chr22 seed 0 was the outlier (`seeds12b`; 16:59, 9 Oct)

The extra seeds finished. With three seeds per cell the DNABERT family is monotone in k on every real
dataset, in both the smooth statistic and the thresholded one. Round 50, canary planted 16 times, training
host; reports `outputs/dnabert_{gue,yeast}_ds/real_report_*.md`.

| model | E. coli bits / exact (3 seeds) | yeast bits / exact (3 seeds) | GUE human promoters bits / exact (3 seeds) |
|---|---|---|---|
| DNABERT 3-mer | 1.60 / 0 % | 0.76 / 68 % | 1.53 / 5 % |
| DNABERT 4-mer | 0.88 / 33 % | 0.56 / 78 % | 1.00 / 23 % |
| DNABERT 5-mer | 0.59 / 55 % | 0.36 / 100 % | 0.51 / 68 % |
| DNABERT 6-mer | 0.30 / 98 % | 0.21 / 100 % | 0.29 / 90 % |
| DNABERT-2 BPE | 0.05 / 100 % | 0.05 / 100 % | 0.04 / 100 % |
| HyenaDNA medium | 0.12 / 77 % | 0.12 / 82 % | 0.11 / 83 % |

Reading.
1. **Monotone in k on all three datasets, in bits and in extraction.** The column Erman stopped at
(96 / 86 / 66 / 84 per cent) came from the human chr22 arm with one seed and with the host confound of
3.22; on the three datasets that now have three seeds there is no zigzag at all. So the honest answer to
his question is first that it was a single-seed artefact, and only second that the chr22 arm is the one
place where the published family might genuinely behave differently, which the re-run will show.
2. **The ordering is the same on a bacterium, a yeast and human promoter sequence**, and the absolute
levels line up within about 0.1 bits for the coarse models, which is the dataset-generality claim in its
strongest form.
3. **Two models break the k ordering from outside**, as before: DNABERT-2 memorises most of all and
HyenaDNA, which is letter-level, memorises more than the 5-mer. Both are explained by the controlled arm:
BPE has an average piece length of about five letters, and HyenaDNA differs in architecture and
pretraining, not in tokenizer.
4. Downstream scores over these same three seeds stay flat, which closes 3.15, 3.17 and 3.19: GUE promoter
0.856 / 0.838 / 0.858 / 0.852 for k = 3/4/5/6 and yeast H3 0.714 / 0.738 / 0.716 / 0.728, against canary
extraction of 5 to 100 per cent.

### 3.24 (9 Oct, 20:15) Correction: the character tokeniser delays memorisation, it does not prevent it

3.20 reported that the character cell shows no memorisation on real human canaries after 30 rounds and
concluded that fine tokenisation removes the leakage. Running the same cell to 150 rounds shows that
conclusion was wrong (`outputs/human_long`, two seeds):

| round | held-out loss | canary excess (bits/nt) | verbatim extraction |
|---|---|---|---|
| 20 | 1.774 | 0.16 | 0 % |
| 30 | 1.757 | 0.76 | 6 % |
| 50 | 3.389 | 3.69 | 68 % |
| 80 | 7.008 | 7.83 | 92 % |
| 150 | 10.209 | 11.48 | 100 % |

The character cell memorises completely; 30 rounds simply did not reach it. The claim in the
mitigation section has to change from "removes the leakage" to "delays it", with the delay quantified
against the 6-mer on the same schedule (running).

**A second, methodological point that this exposed.** The learning rate is cosine-annealed over the
*total* number of rounds, so the 150-round run is still hot at round 30 while the 30-round run has
already annealed: at round 30 the two differ (excess 0.76 against 0.19). Epoch number is therefore not
a comparable axis between runs with different schedules, which is exactly why every comparison in this
project is made at matched held-out loss. Any table that puts two differently scheduled runs in the
same epoch column is wrong, and 3.20 did that implicitly by comparing a 30-round character run with
30-round coarse runs -- that part is fine, because all four had the same schedule, but the conclusion
drawn from it over-reached.

**What survives from 3.20.** At matched held-out loss and at each cell's own utility optimum the
ordering is unchanged: at its best floor (1.757-1.794) the character cell is at 0.16-0.76 excess with
0-6 % extraction, while the 3-mer, 6-mer and BPE cells are at full extraction well before their floors
degrade that far. The useful statement is about the budget at which leakage begins, not about
immunity.

### 3.25 (10 Oct, 01:00) The objective axis on real human data, and a measurement bias that had to be removed first

Three arms finished. The second one changes the order of the mitigation recommendations and the third
forces a correction to 3.22-3.24.

**(a) Objective axis, from-scratch backbone, real human canaries, identical 30-round schedule.**
Epoch-1 excess is 0.00-0.04 for every cell, so a same-epoch comparison is sound here (a randomly
initialised model has no preference between the two canary groups; see (c) for why that matters).

| tokeniser | objective | round-30 held-out loss | round-30 excess | verbatim extraction |
|---|---|---|---|---|
| char | next-token | 1.794 | 0.28 | 0 % |
| char | masked 15 % | 1.854 | **0.02** | 0 % |
| char | masked 50 % | 1.832 | 0.04 | 0 % |
| 3-mer | next-token | 3.925 | 4.27 | **100 %** |
| 3-mer | masked 15 % | 1.717 | **0.12** | 0 % |
| 3-mer | masked 50 % | 1.667 | 0.15 | 0 % |
| 6-mer | next-token | 2.347 | 2.45 | **100 %** |
| 6-mer | masked 15 % | 1.840 | **0.16** | 0 % |
| 6-mer | masked 50 % | 1.807 | 0.29 | 0 % |
| BPE | next-token | 2.681 | 2.82 | **100 %** |

The masked cells memorise 15 to 35 times less than the same tokeniser trained next-token, reproduce
nothing verbatim at any snapshot, and reach a BETTER held-out loss (1.67-1.85 against 2.35-3.93),
because they are still improving at round 30 while the next-token cells have long passed their
optimum. Within the masked cells the dose-response of 3.2 reappears on real human data: 50 % masking
memorises more than 15 % (0.29 against 0.16 for the 6-mer).

**This reorders the mitigation section.** The objective is both the larger lever and the cheaper one:
it removes verbatim extraction outright, whereas fine tokenisation only delays it (3.24). The cost is
that a masked model cannot be sampled from, which rules it out for generative uses but not for the
embedding and classification uses that most genomic pipelines actually need. The ordering also matches
the variance decomposition, where the objective accounts for 58 % and the tokeniser for 15 %.

**(b) The released DNABERT checkpoints under their own masked objective**, at equal hidden-nucleotide
rate (5 % of nucleotides, so the comparison across k is fair), human chromosome 22, baseline-corrected
excess at round 50: \NUM{0.58} (k=6), \NUM{0.87} (k=5), \NUM{1.05} (k=4), and verbatim extraction 0 %
for k=3,4,5 and 10 % for k=6. Against the same checkpoints fine-tuned next-token (1.43-1.54 excess,
67-97 % extraction) the objective effect holds for published models on real human sequence, not only
for our backbone. One run to flag rather than interpret: DNABERT-3 destabilised between round 30 and
50 (held-out loss 1.391 to 1.933, excess turned negative), so its round-50 cell is excluded.

**(c) A measurement bias in the real-canary arm, found while checking (b).** At round 0 the pretrained
models already read the member canaries as 0.30-0.45 bits/nt easier than the non-members, before any
fine-tuning. Decomposing it: the host contributes 0.00-0.04 (the real-fresh-host fix of 3.22 works),
and the remainder is a difference between the two canary GROUPS. The cause is structural: which
canaries are members and which are controls is fixed by `--data_seed`, identical for every model and
every model seed, so an accidental difference between two sets of 50 real haplotype segments - they
differ in GC, repeat content and number of variants - does not average out. With random canaries the
offset is negligible (-0.36 to +0.11, mostly within 0.15, measured on the E. coli, yeast and GUE arms),
which is why this only surfaced on real canaries, and it is zero for from-scratch models at round 1
because an untrained model has no preference.

`pilot2/analyze_matched.py` now subtracts each cell's own round-0 excess (`--raw` keeps the old
behaviour) and prints the offsets it removed. Consequence for the chromosome-22 result: after
correction the four released k-mer checkpoints are **1.54 / 1.46 / 1.43 / 1.52** at r=16, i.e. flat,
and the single-copy column (0.03 / 0.47 / 0.38 / 0.02) is noise. The earlier reading that the 6-mer
was highest on chr22 (3.22, 3.24) was largely its own +0.21 offset, so **no ordering is resolvable on
chromosome 22 for the released family**. The three random-canary datasets of 3.23 are unaffected and
their monotone ordering stands. The proper fix for future runs is to vary `--data_seed` across runs so
the split is re-drawn; the round-0 subtraction is the correction available for the runs we have.

### 3.26 (10 Oct, 01:15) Re-drawing the canary split, and the two paper sections that had to change

**(a) The split re-draw is running** (tmux `dseed`, `pilot2/queue_dseed.sh`, GPUs 0/2/3, about 3.5 h).
3.25(c) left the member/non-member group offset handled by subtracting each cell's round-0 value,
which is a correction rather than a measurement. This arm re-draws the split instead: the six released
models on chromosome 22, the `queue_human3.sh` configuration unchanged apart from `--data_seed`
(2345 / 3456 / 4567, one model seed each, one root per split because run directory names do not
encode the data seed). With `human_real3` (data_seed 1234) that gives four independent draws, so the
chromosome-22 reading can be stated with an across-split spread. `analyze_matched` accepts several
roots and treats same-named cells as repeats, which is the averaging wanted here.

**(b) The chromosome-22 reading, stated carefully.** Two readings exist and they disagree, so the
paper now says so explicitly rather than picking one:

| | k=3 | k=4 | k=5 | k=6 | comment |
|---|---|---|---|---|---|
| excess at equal exposure (round 50) | 1.54 | 1.46 | 1.43 | 1.52 | flat, within seed noise |
| excess at matched held-out loss | 1.54 | 1.16 | 1.15 | 1.26 | inverted: k=3 highest |
| held-out loss at round 50 | 1.664 | 1.704 | 1.726 | 1.728 | k=3 overfits slowest |
| verbatim extraction at round 50 | 97 % | 86 % | 67 % | 85 % | not monotone |

The two disagree because the 3-mer is the slowest to overfit, so its round-50 checkpoint sits at a
better held-out loss than the others'. Worse, on chromosome 22 the six models' overfitting branches
overlap in a window only 0.01 bits/nt wide (1.655-1.664), and restricting the analysis to the four
k-mer models does not widen it, because the bound comes from the 3-mer never reaching the others'
loss within 50 rounds. So any matched comparison on this dataset is fragile. **Conclusion unchanged
from 3.25: no tokeniser ordering is resolvable on chromosome 22**, and the paper rests the ordering
claim on the three datasets where the comparison is well conditioned.

**(c) Sections updated.** `08_mitigation.tex` now leads with the objective and demotes the tokeniser
to second, with the numbers filled in from 3.24-3.25 and the mitigation table's first two rows
written out: objective = extraction 100 % to 0 %, excess 15-35x lower, no utility cost but no
sampling; tokeniser = about 10x delay in rounds, 100 % to 30 % extraction at matched held-out loss,
6x the token slots. The 150-round delay is now quantified rather than left as a TODO: at matched
held-out loss of 2.4 bits/nt the 6-mer extracts 100 % and the character cell 30 %, and the character
cell only reaches 100 % at round 150 where its held-out loss has degraded to 10.2 bits/nt (seeds 0
and 1: excess 11.48 and 11.79, extraction 1.00 and 1.00). `05_published.tex` has the chromosome-22
paragraph rewritten to (b) plus a new paragraph stating the group-offset correction and pointing at
the re-draw; `07_human.tex` has the excess column corrected (1.54 / 1.46 / 1.43 / 1.52 / 2.27 / 2.33)
and a caption note that recovery and extraction are read against the control column and need no such
correction.

**(d) Objective-axis table, current seed counts.** 3-mer and 6-mer cells have both seeds; the BPE
next-token cell and the two character masked cells still have one, because the character masked runs
take about 2 h 20 each on the shared GPU and seed 1 is still going. The numbers in 3.25(a) are seed
means over what has finished and move by at most a few hundredths when the second seed lands.

**(e) The email draft** (`19_email_overleaf_1009.md`) now carries the objective result and the
chromosome-22 correction, because Erman asked about exactly that column this morning and the honest
answer has three parts: wrong statistic, wrong axis, and a measurement bias.

### 3.27 (10 Oct, 02:10) Second queue: finishing the objective x tokeniser grid, and a reusable analyser

**(a) `pilot2/analyze_objaxis.py` (new, committed).** The table in 3.25(a) was produced by a throwaway
script. It is now a module: one row per (tokeniser, objective) cell at the end of a shared schedule,
with the across-seed range, the seed count and the epoch-1 excess, which must be ~0 for a from-scratch
backbone and is the group offset of 3.25(c) otherwise. It identifies the dataset from each run's
`args.json` rather than from the directory the run sits in, which is the mistake `token_info` made in
3.21. Re-running it reproduces 3.25(a) exactly and shows the seed ranges are tight: the excess range
across seeds is 0.01-0.02 for every cell that has two seeds, and the held-out loss range 0.002-0.03.

**(b) `pilot2/queue_1010a.sh` (launched, tmux `q1010a`).** Three holes in that grid, all cheap to fill
because these cells take 1-17 minutes each (79 s for the 6-mer, 155 s for the 3-mer, 1013 s for the
character cell, which pays for its 96 token slots):

1. **no 4-mer or 5-mer on human.** The tokeniser axis has five points on synthetic data and three on
   real human canaries, so the ordering claim on human data rests on three points. Adding both under
   all three objectives: 18 runs.
2. **two seeds where every other table has three.** Seed 2 for every existing cell: 6 runs.
3. **the BPE next-token cell has one seed**, because its seed-0 run was never launched. Seeds 0 and 2:
   2 runs. Masked BPE stays out by design -- with right-padding a bidirectional objective can attend
   through the pads (`pilot2/bpe_arm.py`), so that cell would not measure what it appears to, and this
   is stated as a scope limit rather than silently left blank.

Plus one symmetry fix: the 150-round delay claim of 3.24 has two seeds for the character cell and one
for the 6-mer reference, so the 6-mer seed 1 is queued (1 run). Every cell uses the `queue_human_toy`
/ `queue_1009b` argument string unchanged, so new cells are comparable with the old ones, and the
queue blocks on `Q1009B_DONE` (GPU 1) and `DSEED_DONE` (GPUs 0/2/3) so it never contends with the
running arms.

**(c) Monitoring.** Two watchers are armed: one for `DSEED_DONE` and one for `Q1010A_DONE`, both of
which also break out early on `Traceback`, `CUDA out of memory` or `Killed` in any of the arm's run
logs. The split re-draw is on pace -- all three splits finished $k{=}3$ at 01:44, so six models at
about 30 min each puts `DSEED_DONE` near 04:15 and `Q1010A_DONE` an hour or so after.

### 3.28 (10 Oct, 05:00) The split re-draw: the epoch-0 correction of 3.25(c) is wrong, and chromosome 22 stays unordered

`DSEED_DONE` at 04:17, 18 runs, no failures. Four independent draws of the member/non-member canary
split on chromosome 22: data_seed 1234 (three model seeds, the `human_real3` arm) and 2345 / 3456 /
4567 (one model seed each).

**(a) The epoch-0 subtraction does not survive its own test.** 3.25(c) found a 0.30-0.45 bits/nt
offset between the two canary groups at round 0 and prescribed subtracting it. With four draws the
prescription is refutable, and it is refuted three ways:

| | raw across-draw sd | baseline-corrected sd | r(offset, raw) | regression slope |
|---|---|---|---|---|
| DNABERT 3-mer | 0.07 | 0.24 | -0.60 | |
| DNABERT 4-mer | 0.07 | 0.15 | -0.15 | |
| DNABERT 5-mer | 0.06 | 0.17 | +0.80 | |
| DNABERT 6-mer | 0.04 | 0.39 | +0.39 | 0.055 |
| DNABERT-2 BPE | 0.06 | 0.08 | +0.62 | |
| HyenaDNA | 0.11 | 0.10 | +0.43 | |

(epoch-50 excess at r=16; the slope is cov/var of round-50 excess on round-0 offset.)

1. **The offset is gone after one epoch.** Excess at round 1 is 0.00 +- 0.05 for every model on every
   draw, although the round-0 offsets on those same runs range from -0.48 to +0.88. A real difference
   in group difficulty would persist; this does not.
2. **It barely propagates.** Regressing each draw's round-50 excess on its own round-0 offset gives a
   slope of 0.055 at r=16 and 0.19 at r=1, so subtracting the offset in full over-corrects by 5-20x.
3. **And that shows up as variance.** The raw statistic is 2-10x more stable across draws than the
   corrected one for the five models whose offsets are large; for HyenaDNA, whose offsets are ~0, the
   two agree, which is the control this argument needs.

What the round-0 reading actually measures is the instability of a pretrained model's prior over two
sets of real haplotypes. Note which models have it: +-0.9 for the four masked-pretrained DNABERTs,
+-0.09 for HyenaDNA, the only causal-pretrained model in the panel, and these are scored causally. So
`pilot2/analyze_matched.py` now reports the **raw** excess by default, keeps `--baseline` to reproduce
the subtraction, still prints the offsets as a diagnostic, and adds the across-run spread to the
trajectory table (across splits when several roots are given). Committed with the measurement in the
docstring, so the next reader does not have to rediscover it.

**(b) Chromosome 22 stays unordered, now with four draws behind it.** Raw excess at r=16:

| reading | k=3 | k=4 | k=5 | k=6 | DNABERT-2 | HyenaDNA |
|---|---|---|---|---|---|---|
| equal exposure, round 50 | 1.45 +-0.07 | 1.51 +-0.07 | 1.50 +-0.06 | 1.68 +-0.04 | 2.35 +-0.06 | 2.39 +-0.11 |
| matched held-out loss | 1.48 | 1.06 | 1.01 | 1.37 | 1.47 | 1.50 |
| verbatim extraction (r=50) | 94 % | 87 % | 78 % | 88 % | 100 % | 82 % |
| single copy, round 50 | 0.38 +-0.12 | 0.44 +-0.15 | 0.48 +-0.14 | 0.75 +-0.10 | 2.18 +-0.09 | 1.62 +-0.14 |

Equal exposure rises weakly with $k$ and separates $k=6$ from $k=3$; matched held-out loss reverses
the direction and puts $k=3$ highest. They disagree because the 3-mer overfits chromosome 22 most
slowly, so matching the loss hands it the most exposure to the planted records: its round-50 loss is
1.612 where the 6-mer is at 1.689, and the six rising branches overlap in a window 0.005 bits/nt wide
(1.624-1.629), which leaves no room to prefer one normalisation. **So no tokeniser ordering is
claimed on chromosome 22** -- unchanged from 3.25/3.26, but now with an error bar instead of a single
draw. What is robust there: DNABERT-2 and HyenaDNA sit above the whole k-mer family under both
readings and on every draw, as on the other three datasets, and the single-copy tier is the sharpest
separation of the three (0.38-0.48 for k=3,4,5 against 0.75 for k=6 and 2.18 for BPE).

Also worth recording: the recovery numbers reproduce across draws within 0.05 (3-mer at r=16: alt
1.00 on draw 1234 against 0.83-0.93 on the new draws; DNABERT-2 single copy: 0.86 against 0.84), so
Table 4 of the paper needed only its excess column and its extraction column updated to four-draw
means, which is done.

**(c) `05_published.tex` and `07_human.tex` rewritten** to this: the chromosome-22 paragraph now
states both normalisations and the refusal to order, a second paragraph states the four-draw
refutation of the epoch-0 correction, and the human table carries four-draw means with the
across-draw spread as the error bar.

### 3.29 (10 Oct, 04:35) The 5-mer does not exist on our backbone, and what GPU 2 is doing instead

Six cells of `queue_1010a` failed within a minute of starting:
`AssertionError: (288, 5)` from `pilot2/tokenizers.py`. Not a bug: non-overlapping k-mers need
`window % k == 0`, and the window is 288 nt, so our backbone admits k in {1,2,3,4,6,8,9,12} and never
5. DNABERT's 5-mer is unaffected because its k-mers overlap at stride 1, which is the same distinction
that explains Erman's non-monotone column (3.19, 3.26). **The tokeniser axis on our backbone is
therefore char / 3-mer / 4-mer / 6-mer plus BPE**, four k-mer points on human rather than the five I
wrote in 3.27, and the 150-round and seed-2 cells of that queue are unaffected. `queue_1010a.sh` is
still running, so its 5-mer lines will be replaced when it finishes rather than edited underneath a
running shell.

That freed GPU 2, which is now on `queue_1010b.sh` (tmux `q1010b`, about 3 h): the two gaps in the
E. coli arm, which is the second real genome behind the objective claim. The masked cells there have
one model seed where the next-token cells have two, so all six get a second seed (char ~60 min, 3-mer
~8, 6-mer ~3), and the 4-mer is missing on both objectives, so it is added at two seeds. Each root's
existing arguments are copied verbatim -- they differ between the two roots (the next-token arm scores
snapshots with 50 canaries per tier and a 500-sequence ranking pool, the masked arm does neither and
uses 40 and 300) -- because the point is to put an error bar on numbers already in the log, which a
re-run under different settings would not do.

### 3.30 (10 Oct, 06:20) E. coli confirms the objective axis on a second genome; yeast and GUE queued to finish the set

`Q1010B_DONE` at 06:16, 12 runs, no failures: the E. coli masked cells now have two model seeds and
the 4-mer exists on both objectives. With the analyser fixed (below), the E. coli grid at round 30,
canary planted 16x, two seeds each:

| tokeniser | next-token | | masked 15 % | | masked 50 % | |
|---|---|---|---|---|---|---|
| | excess | extraction | excess | extraction | excess | extraction |
| char | 0.49 | 0 % | **-0.01** | 0 % | **-0.01** | 0 % |
| 3-mer | 4.41 | 100 % | **-0.01** | 0 % | **0.00** | 0 % |
| 4-mer | 3.35 | 100 % | **0.02** | 0 % | **0.00** | 0 % |
| 6-mer | 2.62 | 100 % | **0.06** | 0 % | **0.12** | 0 % |

Held-out loss for the masked cells is 1.86-1.97 against 2.13-4.14 for next-token, so again the masked
model is both the less memorising and the better model at the same budget. On E. coli the masked
excess is at the noise floor -- the across-seed ranges are 0.01-0.03 wide and three of the eight cells
sit at or below zero -- which is a stronger statement than on human (0.02-0.29) and makes the claim
dataset-general rather than human-specific. The dose-response survives only for the 6-mer
(0.06 to 0.12), consistent with the mask rate being the second-order dial.

**Analyser fix that this table depended on.** `analyze_objaxis` read only `scores_ep*.json`, and the
masked arms are run without `--score_snapshots`, so they write `scores_final.json` only: every masked
row was silently missing from the first E. coli table. Each run now contributes at most one value per
epoch, so a run that has both `scores_ep30` and `scores_final` is not counted twice. The preamble now
also says how to read the table: **down a tokeniser's rows, never across tokenisers**, because at a
fixed round the tokenisers sit at held-out losses more than a bit/nt apart (E. coli next-token: 2.13
for char against 4.14 for the 3-mer), which confounds the excess. The tokeniser axis is read at
matched held-out loss, and nothing in this table should be used for it -- the apparent ordering
char < 6-mer < 4-mer < 3-mer in the next-token column is an overfitting ordering, not a tokeniser one.

**`queue_1010c.sh` launched (tmux `q1010c`, GPUs 0 and 3, about 2.5 h).** The objective claim should
hold on every dataset in the paper, and it was measured on three of five: synthetic, E. coli and human
have both objectives, yeast and GUE have next-token only. This queue adds their masked cells (two mask
rates, two seeds) and the 4-mer on both objectives, so all four real datasets share the
char / 3-mer / 4-mer / 6-mer axis. Cheap tokenisers run first, so if it has to be cut short the
unfinished cell is the character one.

Still on GPU 1: the two character masked cells at seed 2 for the human grid, then the human 4-mer.
Character cells are slow for a structural reason worth recording -- PLL scoring is one forward pass
per masked position, so it costs 288 passes per probe for the character tokeniser against 96 for the
3-mer and 48 for the 6-mer, and the snapshot schedule multiplies that by eight.

### 3.31 (10 Oct, 09:40) Five datasets agree on the objective, and the masked column gives the tokeniser axis for free

`Q1010C_DONE` at 09:33, 28 runs, no failures. Yeast and GUE now have masked cells and the 4-mer, so
every dataset in the paper carries both objectives on the same four-point tokeniser axis. Round 30,
canary planted 16x, two seeds, masked at 50 %:

| dataset | objective | char | 3-mer | 4-mer | 6-mer |
|---|---|---|---|---|---|
| E. coli | next-token | 0.49 (0 %) | 4.41 (100 %) | 3.35 (100 %) | 2.62 (100 %) |
| | masked 50 % | -0.01 (0 %) | 0.00 (0 %) | 0.00 (0 %) | 0.12 (0 %) |
| yeast | next-token | 0.15 (0 %) | 4.08 (100 %) | 3.36 (100 %) | 2.60 (100 %) |
| | masked 50 % | 0.00 (0 %) | 0.02 (0 %) | 0.03 (0 %) | 0.20 (0 %) |
| GUE promoters | next-token | 0.13 (0 %) | 4.05 (100 %) | 3.25 (100 %) | 2.53 (100 %) |
| | masked 50 % | 0.00 (0 %) | -0.00 (0 %) | 0.02 (0 %) | 0.23 (0 %) |
| human chr22 | next-token | 0.31 (0 %) | 4.24 (100 %) | — | 2.45 (100 %) |
| | masked 50 % | 0.03 (0 %) | 0.15 (0 %) | 0.23 (0 %) | 0.29 (0 %) |

**The objective result is now the most dataset-general claim in the paper**: across five datasets,
every masked cell reproduces 0 % of the planted records at every checkpoint and sits at excess <= 0.3,
while every coarse-tokeniser next-token cell reproduces 100 % at excess 2.5-4.4 -- and the masked
cells reach the better held-out loss (1.90-1.97 against 2.0-4.4) on the same budget.

**A second result that fell out of it.** Under next-token training at a fixed round the four
tokenisers sit at held-out losses 2.0-4.4, so their excess values are not comparable without the
matched-utility interpolation, which is the trap flagged in 3.30. Under masked training they all
converge to 1.90-1.97 on the same budget -- a spread of 0.05-0.09 within a dataset -- so **the masked
column is already matched**, and in it memorisation is monotone in token length on all four real
datasets: the 6-mer is the leakiest masked cell everywhere (0.12-0.29), the character cell the
tightest (-0.01 to 0.03). The mask-rate dose-response appears only where there is something to dose
(6-mer 0.12 to 0.23 between 15 % and 50 %; nothing resolvable for char). So the two levers compose
the way the variance decomposition says: the objective decides whether records are reproduced at all,
the tokeniser decides how much is memorised either way.

Paper: `04_controlled.tex` gains Table~\ref{tab:objaxis} (the table above) and a paragraph on the
masked column as a matched comparison; `08_mitigation.tex` states the five-dataset claim; `main.tex`
loads `multirow` for the table. Three cells of that table are still TODO -- the human 4-mer
next-token cell is on GPU 1 and the synthetic row is `queue_1010d` (tmux `q1010d`, six runs, the
cheapest cells in the project: the synthetic arm was the only one still missing the 4-mer, and the
mechanism section leans on it most).

Grid status after this: 5 datasets x {next-token, masked 15 %, masked 50 %} x {char, 3-mer, 4-mer,
6-mer} x 2-3 seeds, plus BPE under next-token on human and synthetic, plus the released-model panel
on four datasets with four canary splits on chr22. The grid is complete; what remains is writing.

### 3.32 (10 Oct, 10:50) Grid complete: both remaining queues done, two scripts corrected, Table 2 filled

`Q1010D_DONE` 09:48 (6 runs), `Q1010A_DONE` 10:45 (the GPU-1 branch: the two slow character masked
cells at seed 2, then the human 4-mer at three seeds). No failures beyond the 5-mer cells of 3.29.

**The grid as it now stands.** 5 datasets x {next-token, masked 15 %, masked 50 %} x
{char, 3-mer, 4-mer, 6-mer} x 2-3 seeds, plus BPE under next-token on human and synthetic, plus the
released-model panel (4 k-mer checkpoints + DNABERT-2 + HyenaDNA) on 4 datasets with 4 canary splits
on chromosome 22, plus the 150-round character and 6-mer runs for the delay claim, plus the GUE and
yeast-histone downstream panels. Nothing in the claim-to-evidence map (18) is now unsupported.

Human cells completed overnight: 4-mer next-token 3.23 (100 % extraction) at held-out loss 3.051,
4-mer masked 0.16 / 0.23 at 1.729 / 1.688, and seed 2 for all three character cells, which moved
nothing (char next-token 0.31 across three seeds, range 0.27-0.36). Synthetic 4-mer: next-token 3.34
(100 %), masked 0.03 / 0.11. Both rows of Table~\ref{tab:objaxis} are filled, and with them the
statement that the ordering by token length holds in the masked column on **all five** datasets.

**Two corrections to the scripts, made only after the queues exited** -- editing a file that a running
`bash` is still reading is how a run gets corrupted, which is why these waited:

1. `queue_1010a.sh` asked for 5-mer cells that cannot exist (3.29). The dead lines are replaced by the
   explanation, so the script is a correct record of what was run.
2. `queue_1010d.sh` sent the synthetic masked cells to `outputs/core_mlm`, and `core_mlm` turns out to
   be a duplicate of `core_all`'s masked cells -- identical files, identical md5s -- so passing both
   roots to `analyze_objaxis` counted every synthetic masked cell twice (the first synthetic table
   printed "4 seeds" for cells that have two). The new cells were copied into `core_all`, the script
   and the analysis now use that root alone, and the table was regenerated. Worth remembering as a
   pattern: `analyze_matched` and `analyze_objaxis` treat same-named cells in different roots as
   repeats, which is what the chromosome-22 split re-draw needs and exactly wrong for a duplicated
   root.

**Our backbone at matched held-out loss on human** (`human_obj_matched.md`, the AR cells; the masked
cells and the character cell do not overfit into the common range, which is itself the point): at
held-out loss 2.19, verbatim extraction is 39 % (3-mer), 37 % (4-mer), 75 % (BPE) and 88 % (6-mer),
so the thresholded statistic orders by token length on real human sequence. The smooth statistic at
the same point is 1.91 / 2.03 / 2.14 / 2.17, monotone but tight. This is the human counterpart of
Table~\ref{tab:controlled-matched} and should go in the appendix if the page budget bites.

### 3.33 (10 Oct, afternoon) The body is drafted end to end, and it is twice the page budget

With the grid complete the paper is the work, so every section now has prose instead of a plan. What
changed, what it cost, and what has to happen next.

**Sections written from measured numbers.**

| section | state | notes |
|---|---|---|
| 00 abstract | written, 229 words | the claim ladder: objective, tokeniser, utility blindness, real haplotypes |
| 01 introduction | written, 939 words | contributions renumbered to six; the stale "character tokeniser removes the leakage" claim is gone |
| 02 related | written | one TODO left, the two unverified 2026 infilling references |
| 03 setup | unchanged | one TODO, the schematic figure |
| 04 controlled | two paragraphs added | variance decomposition, placement flip, parametrisation sensitivity, above-capacity regime |
| 05 published | done earlier today | four-split chr22 reading |
| 06 utility | rewritten | the early-stopping claim is now correct (below) |
| 07 human | rewritten | four-split pooled recovery numbers |
| 08 mitigation | completed | the mitigation table has no empty cells left |
| 09 discussion | written | limitations now include the parametrisation sensitivity and the chr22 non-ordering |

**A claim that had to be corrected while writing 06.** The draft said "stopping at the best held-out
loss does not help". The data say something more precise and more useful: at its own loss optimum
every released model except the 3-mer extracts **0%** of the planted records, so stopping exactly
there does work --- and the optimum is a knife edge. Moving one snapshot costs HyenaDNA 0.004 bits of
held-out loss and takes it from 0% to 69% extraction; the corresponding gaps are 0.032 to 100% for
DNABERT-2, 0.039 to 51% for the 4-mer, 0.046 to 84% for the 5-mer and 0.111 to 95% for the 6-mer. A
validation loss five hundredths of a bit from optimal is what anyone would call converged. And the
optimum is not clean on the other rulers: recognition there is already 4% (4-mer), 28% (5-mer), 52%
(3-mer), 80% (DNABERT-2) and 88% (6-mer). **Stopping at the optimum suppresses what the model writes,
not what it knows.**

**The downstream claim also needed fixing.** "No task moves by more than 0.05 MCC and none moves
down" is false. Four of six tasks move by at most 0.037 in either direction; splice sites move up by
0.02-0.15 and H3K4me3 by 0.03-0.11 --- upward as leakage grows, so they actively mislead --- and TF
binding drifts down for three models by up to 0.036. Best-downstream selection picks 44-100%
extraction for five of six models, not four. Four of the 252 (model, round, task) fine-tuning runs
collapsed to a degenerate head and are excluded and listed; that is the only exclusion in the paper.

**New analyser:** `pilot2/analyze_downstream.py` (committed) pulls every score file's downstream
block into one table per model --- each task's fine-tuned and frozen-probe MCC beside the canary of
the same checkpoint --- plus the summary of what each stopping rule would select. The variance
decomposition was also recomputed on the finished grid: with the 4-mer added it is objective 67.1%,
tokeniser 12.0%, interaction 21.0%, seed 0.0% (24 runs); restricted to the three tokenisers the
fixed-placement arm also has, it reproduces the recorded 57.7 / 15.4 / 26.9 / 0.0 exactly, against
59.5 / 25.7 / 14.0 / 0.8 for fixed placement. Within the masked cells alone the tokeniser explains
97.8% of what is left, and within the next-token cells 100%.

**The problem: length.** The body is 8103 words excluding comments, which is about 12.5 pages of
10 pt text before any float, and there are seven tables and four planned figures on top of that. The
limit is 10 pages including everything. So the draft is roughly twice the budget.

The lever is the call's own rule: the appendix is a **separate PDF with no page limit**, and
reviewers may skip it. Nothing has to be deleted, only moved. Planned cut, section by section:
introduction 939 -> 600, related 510 -> 320, setup 531 -> 420, controlled 1505 -> 850 (the
parametrisation and capacity paragraphs go to the appendix as three sentences plus a pointer),
published 738 -> 480 (the group-offset argument moves), utility 1045 -> 600 (the per-model downstream
panels move; keep the stopping table), human 978 -> 700 (the headline novelty, cut least), mitigation
983 -> 700, discussion 645 -> 400. That lands near 5300 words, about 8 pages with floats, which
leaves room for two figures rather than four.

**Open question for the collaborators, not for the data:** the Overleaf project is now shared with
Erman and Alex, so the editing surface is there while these files are local. Either the files get
uploaded to Overleaf as a batch, or Overleaf's Git/GitHub sync is pointed at a repository, before
anyone else starts editing; otherwise the two copies diverge within a day.

### 3.34 (11 Oct) Verifying two references turned into a new control, four figures, and the cut to length

**(a) The references were wrong, two of three.** Checked against the local PDFs rather than from
memory:

| as filed | actually |
|---|---|
| "Memorization in Diffusion Language Models", Luo and others | **Characterizing Memorization in Diffusion Language Models: Generalized Extraction and Sampling Effects**, Luo, Yu, Li, Bjerva (Aalborg), arXiv:2603.02333 |
| "...by Infilling", Wang and Asokan | **...via Infilling**, Yihan Wang, N. Asokan (Waterloo/KTH), arXiv:2605.24173 |
| "Memorization Dynamics and the Fisher Information Metric", **Simon** von Arx | **Memorization Dynamics of Fill-in-the-Middle Pretraining**, **Tobias** von Arx and Tanguy Dieudonne (ETH), ICML 2026 workshop, arXiv:2605.22981 |

Morris (full eight-author list, arXiv:2505.24832) and Jagielski (an arXiv note, not a conference
paper) were corrected the same way. VERIFY flags: 5 -> 2 (the BCB proceedings version of Nemecek,
and the Nucleotide Transformer volume/pages).

von Arx and Dieudonne is the text analogue of our objective axis -- matched Llama 3.2 models,
fill-in-the-middle against left-to-right, with infilling recovering short or partial spans and
left-to-right the long exact ones -- so it is independent support, now cited in Sec. 2.

**(b) Wang and Asokan found a hole in our strongest claim, and the control closes it.** Their
result: prefix-only probing understates extraction from models that denoise arbitrary positions, by
up to 3x on LLaDA-8B and Dream-7B. Our extraction ruler is prefix-conditioned -- for a masked cell
`extract_prefix` masks everything after the revealed prefix -- so "masked training reproduces
nothing" had been shown only in the geometry that suits an autoregressive model. That is the first
question a reviewer who knows this literature would ask.

So `score.py` gained `extract_infill` (the host after the record stays visible; the 48 masked
nucleotides are decoded in confidence order, which is the stronger attack) and `infill_audit.py`
re-runs both protocols from the saved `final.pt`, writing to new files so nothing is overwritten.
**Result: the claim holds.** 120 cells -- five datasets, four tokenisers, two mask rates, two to
three seeds, three tiers, 20 canaries each -- give 0 % under both protocols, with 34.9 wrong
nucleotides out of 48 under the prefix protocol and 35.2 under infilling, against 35.0-35.6 for
non-members. The leakiest masked cell in the paper (human 6-mer at 50 % masking, excess 0.29) is at
the non-member level under the protocol designed to break it.

**(c) Four figures, built from the score files** (`pilot2/figures_paper.py`, PDF + PNG):
F1 the objective x tokeniser grid on all five datasets, with a second row replotting the masked
cells on their own scale so the surviving tokeniser ordering is visible -- **this replaced the wide
five-dataset table**; F2 the mechanism in three panels (per nucleotide, per slot, and memorisation
against canary-token corpus count, which orders every cell including BPE); F3 the variance
decomposition with the placement flip; F4 the 150-round delay and what it costs in held-out loss.

**(d) The cut.** Main text went from 8701 words to 6805 (5565 prose + 1240 inside floats), which is
about 10.6 pages against the 10-page limit including everything -- close enough that the Overleaf
compile decides it. Two passes: whole blocks moved into the appendix (parametrisation and capacity,
the placement decomposition, the per-model downstream panels, the infilling audit detail, the
four-draw argument), then a concision rewrite of every section. The appendix now has nine sections
built from the moved text rather than placeholders, and every `Appendix~A*` reference in the main
text resolves. Zero TODOs left in the main sections.

One judgement to record: the rule I used for what may move is the call's own -- reviewers may skip
the appendix, so it holds how things were done and the per-seed numbers, never the only evidence
for a claim. What stayed: the five-dataset objective result (now Fig. 1), the chromosome-22 four-draw
reading, the early-stopping margins, the human recovery table.

### 3.35 (11 Oct, 02:30) The 150-round arm closes the audit gap: the tokeniser ordering is now matched-utility on all five datasets

`Q1010E_DONE` at 02:27, 30 runs, no failures. The gap 3.32 found was that the tokeniser claim could
only be made at matched held-out loss on E. coli and human, because on synthetic, yeast and GUE the
30-round cells had no common overfitting band. At 150 rounds they do, and the band is 0.13-0.15
bits/nt wide instead of 0.005. Verbatim extraction of the 16x canary at the most-overfit shared
point:

| tokeniser | nt/token | synthetic | E. coli | yeast | GUE | human chr22 |
|---|---|---|---|---|---|---|
| character | 1.0 | 8 % | 0 % | 6 % | 5 % | — |
| 3-mer | 3.0 | 27 % | 0 % | 40 % | 33 % | 47 % |
| 4-mer | 4.0 | 88 % | 1 % | 93 % | 86 % | 53 % |
| BPE-4096 | 5.0 | 99 % | 28 % | 100 % | 99 % | 86 % |
| 6-mer | 6.0 | 100 % | 53 % | 100 % | 100 % | 100 % |

Monotone in nucleotides per token in every column, and BPE lands with the 6-mer rather than above
it, which is the control that separates the tokeniser from the model (DNABERT-2 memorises more than
any released k-mer checkpoint, and that is the model, not the tokeniser). The character cell never
reaches the common range on chromosome 22, which is itself the delay result of 3.24 seen from
another angle. This replaces the E. coli-only matched table in the paper.

**Two repairs to the draft, both found by auditing rather than by reading.** The concision pass of
3.34 extracted floats by searching for a label, and the fig:objaxis caption happens to contain the
string `tab:controlled-matched`; the extractor therefore returned the figure for the table, so
Sec. 4 ended up with the figure twice and no table at all, while four references to it still
pointed nowhere. Fixed, and the replacement table is the five-dataset one above. A reference audit
then showed `tab:human` and `tab:mitigation` had lost their in-text references in the same pass;
both are back. Every float now has exactly one label and at least one reference, and the main text
has no TODO left.

Final state of the main text: 6946 words, of which 5599 are prose and the rest inside the three
figures and five tables; estimated 10.6 pages against a 10-page limit, which is close enough that
the Overleaf compile decides it rather than my estimate.

### 3.36 (11 Oct, 02:50) The four robustness arms a reviewer will ask for, all launched

A asks whether a planted record is needed at all, B adds a second chromosome, C answers the
matched-compute objection, D tests whether the ordering is a small-model artefact. Three queues,
chained so nothing contends: `q1011a` (C and D) runs now, `q1011b` (B) has already fetched its data
and waits for the GPUs, `q1011c` (A) waits for B.

**C -- matched compute (`outputs/ecoli_mc`).** Every comparison so far is at matched data and
matched rounds, and a character model processes 288 token slots per window where the 6-mer processes
48. Here the round count is set so each cell processes the same number of token slots as the 6-mer at
30 rounds (30 x 5000 x 48 = 7.2M): char 5 rounds, 3-mer 15, 4-mer 20, 6-mer 30. Each cell's wall
clock is in its `train_summary`, so the same runs also answer the harsher version of the question --
attention is quadratic in the slot count, so equal slots is not equal seconds.

**D -- scale (`outputs/ecoli_big`).** The grid repeated at $d{=}768$, 8 layers, 12 heads: 59.9M
parameters, 56.7M non-embedding, 4.5x the backbone the paper uses and within a factor of two of
DNABERT. `run_pilot` gained `--d_model/--n_layers/--n_heads` for it (defaults unchanged). Next-token
at two seeds, masked at one, because PLL scoring is one forward pass per masked position.

**B -- a second chromosome (`outputs/human_chr21`).** hg38 chr21 (46 MB) and the 1000 Genomes
phase-3 GRCh38 phased VCF for chr21 (180 MB) are downloaded, from the same release as the chr22
files. Canaries are built by the same filter, then the released-model panel runs with two seeds for
the four $k$-mer checkpoints and one for DNABERT-2 and HyenaDNA.

**A -- natural duplicates, and what the smoke test changed about it.** The plan was to hash the
training corpus for 96-nt blocks it repeats by itself, score them with the paper's rulers and
compare against single-occurrence blocks: memorisation without anything planted. Two measurements
reshaped the design before any GPU time was spent.

1. **E. coli has no exact 96-nt repeats at all.** 85,000 distinct blocks across 5,000 windows,
   every one of them unique. The bacterium is simply not repetitive at this length, so the
   experiment cannot be run there.
2. **At 5,000 windows the control is already fully memorised.** Single-occurrence blocks come back
   at 100 % verbatim extraction and 0.002-0.03 bits/nt for the $k$-mer cells. With 5,000 windows and
   30 rounds the model has stored its training set wholesale, so "duplicated against not duplicated"
   has no contrast to measure. This is worth recording on its own: the planted-canary design is not
   a convenience, it is what makes the question answerable at a corpus size where everything fits.

Both are fixed by the corpus. Chromosome 22 at 60,000 windows (17 Mb) holds 2,235 blocks that occur
twice, 1,245 three or four times, 717 five to eight and 68 nine or more, and at that size the model
is far enough above capacity that it cannot store everything. So `q1011c` trains the four tokenisers
on 60,000 chr22 windows and then scores the natural duplicates. The planted canaries stay in the
training set, so the two populations can be read against each other directly: a block the corpus
repeats nine times against a record we inserted sixteen times.

New code, committed: `pilot2/natural_dups.py` (duplicate census + scoring from `final.pt`),
`--d_model/--n_layers/--n_heads` in `run_pilot`, and the three queue scripts.

### 3.37 (11 Oct, 07:30) All four robustness arms landed, and A needed a second control before it meant anything

275 minutes for the three queues, no failures.

**A -- memorisation with nothing planted.** On 60,000 chromosome-22 windows, scoring the 96-nt
blocks the corpus repeats by itself. The first pass looked like a clean win and was not yet an
argument: natural duplicates came back at 85-98 % verbatim against 15-38 % for single-occurrence
blocks, but a block chr22 repeats nine times is usually a transposable element, so a model may
complete it because the family is predictable rather than because it saw those copies. The control
is the same logic the planted canaries use: hash 60,000 windows of the same genome the run never
trained on, keep the blocks that repeat there and occur zero times in training, score them
identically.

| tokeniser | x1 trained / held out | x2 trained / held out | x3-4 trained / held out | x5-8 trained / held out |
|---|---|---|---|---|
| char | 3 % / 0 % | 63 % / 23 % | 83 % / 50 % | 97 % / 73 % |
| 3-mer | 23 % / 0 % | 87 % / 10 % | 97 % / 27 % | 100 % / 60 % |
| 4-mer | 23 % / 3 % | 87 % / 10 % | 100 % / 27 % | 97 % / 57 % |
| 6-mer | 30 % / 0 % | 93 % / 23 % | 100 % / 23 % | 100 % / 43 % |

(verbatim extraction, 30 blocks per cell.) Three readings. **Repetition in training is what the
rulers capture**: a block present twice is reproduced 63-93 % when trained on and 10-23 % when an
equally repetitive block of the same families was not. **Two copies of real sequence are enough** --
the planted 16x tier is not where this starts. And the **held-out column inverts the ordering**: on
repeats it has never seen, the character model completes more than the coarse ones (73 % against
43 % at multiplicity 5-8), so coarse tokenisers memorise more without generalising better. Worth
keeping: the predictability confound is real and large (held-out x5-8 reaches 43-73 %), so the first
pass would have overstated the effect by that much.

**D -- scale.** The E. coli grid on a 59.9M backbone (56.7M non-embedding, 4.5x ours, within a
factor of two of DNABERT) reproduces both findings. Matched held-out loss, r=16: excess 1.06
(char, 0 % extraction), 2.01 (3-mer, 5 %), 2.04 (4-mer, 51 %), 2.51 (6-mer, 100 %). Objective axis:
next-token excess 2.36-5.17 with 100 % extraction (char 0 %), masked -0.01 to 0.04 with **0 %
extraction in every cell**. The ordering is not a small-model artefact.

**C -- matched compute.** Round counts set so every cell consumes the same 8.71M supervised tokens
(char 5 rounds, 3-mer 15, 4-mer 20, 6-mer 30 -- the budget matched to three decimal places). At
matched held-out loss the order is unchanged: 1.32 (3-mer, 0 %), 1.45 (4-mer, 5 %), 1.96 (6-mer,
76 %), with the character cell never overfitting into the shared range. The wall clock is the
surprise: under that budget char is the **cheapest** (14 s against 35 s) because it takes six times
fewer optimiser steps. At this scale the GPU is step-bound, not FLOP-bound, so this would reverse at
longer windows where attention dominates -- stated that way in the paper rather than claimed as a
free lunch.

**B -- chromosome 21.** 400 canaries, 365 carriers, 2.23 variants each, two seeds for the k-mer
family. Rare-allele recovery at r=16 is 0.84-1.00 against a 0.23-0.29 control; DNABERT-2 again leaks
a record seen **once** (77 % of its rare alleles against 27 % control, 44 % of segments verbatim)
while no k-mer checkpoint extracts a single-copy record. And the anomaly reproduces: extraction at
r=16 is 79, 68, 48, 91 % for k=3,4,5,6 -- the same non-monotone shape with the same 5-mer dip as
chromosome 22. An artefact of one chromosome would not survive the change of chromosome.

**Into the paper.** Section 4 gains the natural-duplicate paragraph with Table 3 (two multiplicities
in the main text, the full table in Appendix A10) and a compact scale-and-compute paragraph; Section
5 gains the chromosome-21 paragraph; the limitations list loses three bullets that are now answered
rather than conceded. The variance figure moved to Appendix A4 and the mechanism figure stayed, which
is the right split: the mechanism panel is evidence, the variance bars are four numbers already in
the text.

**One repair.** The float-moving script matched `\begin{figure}...fig:variance...\end{figure}`
non-greedily from the FIRST figure in the file, so it swallowed the objective figure, the variance
decomposition paragraph and the placement paragraph along with the figure it was supposed to move.
Caught by the label/reference audit (fig:objaxis had a reference and no label), repaired, and the
audit is now part of the routine after any structural edit: every float must have exactly one label
and at least one reference.

Main text after all of it: 7505 words, 6068 of them prose, three figures and six tables, which
estimates to 10.6-11.5 pages depending on the words-per-page assumption. That has to be settled by a
compile rather than by arithmetic.

### 3.38 (11 Oct, 20:40) Reading the predecessor properly: it has four models, not nine, and its Evo result is a question we can answer

Adding the Nucleotide Transformer meant reading Nemecek et al. closely, which turned up two things.

**(a) A factual error in our draft.** We wrote "nine published genomic models". The paper evaluates
**four**: SimpleDNALM (12.9M, full fine-tune, character-level), DNABERT-2 (117M, full, BPE),
HyenaDNA (14.2M, full, single-nucleotide) and **Evo (7B, StripedHyena, LoRA, byte-level)**, on four
datasets. Corrected in the introduction and in related work. Worth recording separately: **our
controlled backbone is their SimpleDNALM**, which is why the two sets of numbers are comparable at
all, and we now say so.

**(b) Their headline result looks like a contradiction of ours.** Evo is the leakiest model in that
panel by a distance -- 100 % canary extraction on all three real genomes even at a *single*
insertion, where DNABERT-2 resists extraction entirely. Evo is byte-level, which is the finest
tokenisation there is, and our grid says fine tokenisation memorises least. Their own reading is
that the pretrained parameters already hold the distribution so a low-rank update has nothing to
learn except the examples. But Evo differs from the rest of their panel in scale, architecture,
tokenisation, objective AND fine-tuning strategy at once, so that reading is a hypothesis.

**The experiment that separates one of those five (`queue_1011d`).** Same backbone throughout:
pretrain on 60,000 chromosome-21 windows (giving our backbone what every released model has and ours
never had), then fine-tune on chromosome 22 with the planted canaries, once with all parameters and
once with a LoRA adapter of rank 8 on qkv/proj/ff1/ff2 -- the analogue of the
["Wqkv", "dense", "gated_layers", "wo"] set used for Evo -- everything else identical. RoPE
throughout, because the default blocks' fused in-projection is a Parameter and cannot be adapted.

First cell (character tokeniser, seed 0), both trajectories, canary planted 16x:

| | full ft | | LoRA r=8 | |
|---|---|---|---|---|
| round | held-out loss | excess (exact) | held-out loss | excess (exact) |
| 1 | 1.608 | 0.41 (0 %) | 1.605 | 0.11 (0 %) |
| 3 | 1.624 | 1.38 (82 %) | 1.601 | 0.24 (0 %) |
| 8 | 1.994 | 2.19 (98 %) | 1.608 | 0.55 (10 %) |
| 12 | 3.141 | 3.65 (92 %) | 1.617 | 0.82 (16 %) |
| 30 | 7.843 | 8.76 (100 %) | 1.652 | 1.22 (48 %) |

The two ranges overlap at 1.60-1.65, so the matched comparison is available. **At matched held-out
loss the full fine-tune memorises MORE, not less**: at 1.617 it is at about 1.16 excess and ~52 %
extraction against LoRA's 0.82 and 16 %; at 1.638, about 1.45 and ~87 % against 1.13 and 36 %. LoRA
also never extracts a single-copy canary at any round (r=1 exact 0 % throughout) where the full
fine-tune reaches 96 % by round 30 -- at a held-out loss of 7.84, which is useless.

So on a matched backbone **LoRA reduces memorisation at matched utility but does not prevent it**
(48 % of 16x canaries by round 30, at a perfectly good held-out loss of 1.65). Two consequences. The
predecessor's conclusion survives in its weaker form -- parameter-efficient fine-tuning is not a
defence -- and we can say why with a measurement rather than a hypothesis. But LoRA cannot be the
explanation for Evo being the leakiest model in that panel, because here it is the *protective*
direction. That leaves scale, architecture and pretraining corpus, and our own above-capacity result
(3.x) points at scale: a 7B model fine-tuned on a small corpus has capacity to spare.

A second thing this arm gives us for free: our backbone now has a pretrain-then-fine-tune setup, so
its numbers sit on the same footing as the released checkpoints rather than being from-scratch runs.

### 3.39 (12 Oct, 02:30) NT and Evo both land, and NT finds the hole in our headline claim

**(a) NT 250M runs, and it is the released model that sits on our axis.** Its vocabulary is the 4096
NON-overlapping 6-mers -- our 6-mer cell with 250M pretrained parameters behind it, 48 tokens per
288-nt window for both. Masked objective only: the released code multiplies its embeddings by the
attention mask, so the causal mask we give DNABERT is rejected, and that is the checkpoint's limit
rather than our choice.

**(b) And it breaks "a masked objective reproduces nothing".** The trajectory, canary planted 16x:

| | E. coli | | human chr22 | |
|---|---|---|---|---|
| round | held-out loss | excess (extraction) | held-out loss | excess (extraction) |
| 3 (optimum) | 1.823 | 0.01 (0 %) | 1.376 | 0.29 (0 %) |
| 8 | 1.826 | 0.31 (0 %) | 1.382 | 0.51 (**8 %**) |
| 15 | 1.851 | 1.62 (4 %) | 1.411 | 0.80 (6 %) |
| 30 | 2.004 | 2.11 (20 %) | 1.501 | 1.39 (12 %) |
| 50 | 2.263 | 2.37 (**28 %**) | 1.632 | 1.77 (**18 %**) |

At its utility optimum NT extracts 0 %, which is our claim and survives. Past it the claim does not:
a masked 250M model reaches 18-28 % verbatim extraction, and on human the knife edge is as thin as
it is for next-token training -- **0.006 bits/nt past the optimum is already 8 % extraction**.

Our own masked cells report 0 % at every checkpoint, but they were stopped at 30 rounds with their
held-out loss still improving: **they never entered the overfitting regime at all**, so "0 % at
every snapshot" was a statement about the budget, not about the objective. `queue_1011h` pushes the
3-mer and 6-mer masked cells to 150 rounds on human to settle which it is.

This is the kill shot a reviewer would have had, and it is better found now. It also makes the
paper's two recommendations the same shape, which is a better story than the one we had: **both
levers delay rather than prevent**, the objective by far the more, and neither is immunity. The
early-stopping finding of Sec. 6 now covers masked models too, which previously it did not.

**(c) Evo 1 (7B) runs under our rulers, and memorises nothing in 10 rounds.** E. coli, LoRA r=8 in
the predecessor's configuration, 4.4 h on one 4090:

| round | held-out loss | r=16 canary bits/nt | rank-1 | extraction |
|---|---|---|---|---|
| 0 | 1.704 | 2.13 | 5 % | 0 % |
| 1 | 1.517 | 2.10 | 5 % | 0 % |
| 10 | 1.425 | 2.10 | 5 % | 0 % |

The model learns the corpus -- held-out loss falls 1.70 to 1.43, and 1.70 before any fine-tuning is
already far better than our 12.9M backbone ever reaches -- while the planted canaries sit at chance
(2.0 for random DNA) at every tier and every round, with rank-1 at the 1 % chance level of a
100-candidate pool.

That is the opposite of the predecessor, which reports 100 % extraction on E. coli at a single
insertion. The difference is protocol, and the candidates are testable: 10 rounds against their 25;
our strict all-48-nucleotides greedy criterion against their beam search over 1000 candidates; and
our canaries sitting at an independently drawn offset inside a longer host window against theirs
being the training example. `queue_1011g` runs two cells at their corpus size and round count
(1000 windows, 25 rounds) differing only in canary placement -- the variable our own grid already
shows is worth 59.5 % against 15.4 % of the attributed variance.

Also recorded: Evo's held-out loss on human chromosome 22 before fine-tuning is **2.096, worse than
chance**. Evo 1 was trained on prokaryotic genomes, so human sequence is out of domain for it, and
any human-chromosome number from it has to be read that way.

**(d) Three walls cleared to get Evo running**, all without touching the shared environment:
transformers 4.29 is too old for the remote code (4.44 side-loaded with `--no-deps`, leaving the
env's torch 2.1.1 and numpy 1.24 alone); flash-attn is required and the wheel pinned in
`requirements_evo.txt` is cu11, which will not load against cu121 torch (2.5.8+cu122torch2.1 does,
and its kernel runs on a 4090); and StripedHyena compiles Triton kernels, which want `libcuda.so`
beside the `libcuda.so.1` that ldconfig reports -- Ubuntu 18.04 ships only the latter, so `evo.py`
points Triton at CUDA's own stub rather than adding a symlink to a system directory other people
share. Two more for the rulers: peft's `CAUSAL_LM` task type calls forward with `inputs_embeds`,
which StripedHyena does not accept, and `rank_probe` scores a whole candidate pool in one forward --
2.8 GiB of FFT workspace at 4096 channels -- so the wrapper chunks the batch.

**(e) Docker, checked rather than assumed.** `docker` 24.0.2 is installed, we are in the docker
group, nvidia-container-toolkit is present, `--gpus all` shows both cards, and glibc inside a
container is 2.35 against the host's 2.27. So the glibc wall that blocks Evo 2's
`transformer_engine >= 2.0` does come down in a container. The driver does not: 530.30.02 caps CUDA
at 12.1, and an RTX 4090 is a GeForce card, which CUDA forward compatibility does not cover. Evo 2
therefore needs a driver upgrade as well as a container, and that is a decision for whoever owns a
shared machine, not for us.

**(f) One near-miss worth recording.** The two new Evo cells were about to write into the finished
run's directory, because the run name carried only model, dataset and seed. Caught by reading the
directory listing before the first snapshot landed; the finished scores were preserved, the name now
carries epochs, corpus size and offset mode, and the adapter is saved at the end so a finished run
can be re-examined.

### 3.40 (12 Oct, 18:40) The budget explanation is dead, the three rulers come apart, and 3.39(b) was half wrong

**This entry corrects 3.39(b).** Last night I wrote that both levers "delay rather than prevent" and
that our masked cells' 0 % was "a statement about the budget, not about the objective". The first
half of that is now refuted for our own backbone, by the very run I queued to test it.

**(a) `queue_1011h`: five times the budget, total recognition, still nothing emitted.** The 3-mer and
6-mer masked cells on human chromosome 22, pushed from 30 rounds to 150:

| | 3-mer | | | | 6-mer | | | |
|---|---|---|---|---|---|---|---|---|
| round | floor | r=16 bits | r=16 rank-1 | exact | floor | r=16 bits | r=16 rank-1 | exact |
| 30 | 1.675 | 1.641 | 0.04 | 0 % | 1.828 | 1.655 | 0.10 | 0 % |
| 50 | 1.645 | 1.233 | 0.22 | 0 % | 1.845 | 1.301 | 0.28 | 0 % |
| 80 | 1.718 | 0.509 | 0.70 | 0 % | 1.947 | 0.688 | 0.90 | 0 % |
| 110 | 1.897 | 0.216 | 0.90 | 0 % | 2.074 | 0.313 | **1.00** | 0 % |
| 150 | 2.074 | 0.116 | 0.98 | 0 % | 2.176 | 0.140 | **1.00** | 0 % |

Both cells end well past their utility optimum and past the 2.000 chance level, so they are deep in
the overfitting regime the 30-round runs never reached. By the surprise ruler they have the canaries
almost exactly (0.12-0.14 bits/nt against a 2.000 chance level). By the recognition ruler the 6-mer
cell is at **rank-1 = 1.00 at every tier from round 110, including r=1** -- it picks a record it saw
**once** out of a hundred candidates, every time. **Verbatim extraction is 0.00 in all 30 cells**,
and the greedy reconstruction stays 30-34 of 48 nucleotides wrong, which is barely better than the
chance level of 36 and barely better than the same decode on a window the model never trained on.

So the budget explanation is dead, and what replaces it is better: **the three rulers dissociate**. A
masked model can store a record well enough to recognise a single copy of it with certainty and
still never emit it. That is not "memorises less"; it is memorisation of a different kind, and it is
exactly the distinction the paper's three rulers were built to make. This is the strongest result we
have for the objective axis.

**(b) But NT still extracts, and that is the real open question.** The Nucleotide Transformer at 250M
runs the same masked objective through **our own extraction code** and reaches 28 % on E. coli and
18 % on human. Two things follow. First, **the scorer is not broken** -- the same code path does
produce exact matches, which is the internal control the 0 % above needs, and the objection a
reviewer would have raised. Second, a masked model *can* be made to emit records, so the dissociation
in (a) is not a property of the objective alone.

It is also not a threshold in surprise: NT extracts 12 % at 0.285 bits/nt on human where our 3-mer
extracts 0 % at 0.116, i.e. **our cell is the more memorised of the two by the surprise ruler and
still emits nothing**. NT differs from our backbone in exactly two ways -- 250M parameters against
12.6M, and a pretrained prior -- and it cannot separate them.

**(c) `queue_1012a` separates them**, and it is the run that decides how the paper's headline is
phrased: 150 rounds at 59.9M and 201M from scratch, a causal cell beside every masked one (without
it a reviewer answers "everything extracts at 201M" and we could not contradict them), then masked
chromosome-21 pretraining feeding the same chromosome-22 fine-tune. Launched 18:41, all four cards,
about 6 s/round at 201M.

**(d) `queue_1011g`: Evo at the predecessor's configuration, both canary placements, still nothing.**
1000 windows and 25 rounds, the two cells differing only in where the canary sits in its host window:

| | floor ep1 -> ep25 | r=16 bits ep1 -> ep25 | r=16 rank-1 | exact |
|---|---|---|---|---|
| random offset | 1.590 -> 1.468 | 2.102 -> 2.075 | 0.00 | 0 % |
| fixed offset | 1.590 -> 1.473 | 2.112 -> **2.015** | 0.00 -> 0.15 | 0 % |

Placement moves the signal in the expected direction and nowhere near far enough. What matters more
is that **Evo's canary surprise never leaves the 2.0 chance level and its held-out loss plateaus by
round 10**, which rules out the explanation I thought most likely: if there is no signal at all, then
no extraction criterion, however lax, can recover anything, so "their beam search over 1000
candidates against our strict all-48 greedy" cannot be the difference. That leaves one untested
protocol difference -- in the predecessor the canary **is** the training example, where ours is
embedded inside a longer host window and is a fraction of that example's supervised tokens.

**(e) A caveat Evo's human numbers need.** On chromosome 22 its held-out loss starts at 2.096, worse
than chance, and reaches 1.855 by round 10, and at r=16 the canary surprise does fall to 1.780 with
rank-1 0.20. But its greedy decode **degenerates**: the mean longest single-nucleotide run in the
48-nt reconstruction is 35-43 of 48 at rounds 5-10, i.e. it emits homopolymer. Evo 1 is prokaryotic
and human is out of domain for it, and any human extraction number from it has to carry that.

**(f) Two cells that said "done" and had not run.** `queue_1011e`'s GUE cell died after round 1 (I
killed it to free a card for Evo) and both its 500M cells died immediately: the guard tested for
`config.json`, which the interrupted download had already written, while the weights had not arrived.
Both queues logged "done" regardless of exit status. `queue_1012b` re-runs the GUE cell, resumes the
500M download from the partial file still in the hub cache, and guards on the weights; both new
scripts record the exit status, which is how the two false lines got in.

### 3.41 (12 Oct, 19:40) The masked 0 % was partly our decoder, the mechanism is now measured, and scale alone does not turn extraction on

**This entry corrects 3.40 twice and is the most consequential thing found today.** An adversarial
audit of the draft asked whether the 0 % could be an artefact of how we decode, and named one
decode that had never been run. It was right to ask.

**(a) The conditional each ruler uses, which we had never separated.** `rank_probe` normalises
bits/nt over all 96 nucleotides of a canary and `extract_prefix` hands the attacker the first 48 of
them, so a low canary surprise can sit beside a hopeless reconstruction purely because half the
scored span was given away. `pilot2/recon_audit.py` measures the quantity extraction has to invert
instead: the teacher-forced surprise of the 48 TARGET nucleotides given the revealed 48, and the
fraction of decoding steps whose argmax is the true token.

**(b) And a decode neither shipped protocol performs.** Both mask the whole 8-16-token target block
at once, which is far outside the 15 % iid masking of training, while surprise and recognition read
a conditional with ONE token masked. Iterated conditional modes re-masks one target token at a time
and sweeps to a fixed point: in distribution, and the strongest attack available to someone holding
only the flanking sequence. On the 150-round chromosome-22 cells, 25 probes per tier:

| cell | tier | target bits/nt | per-step top-1 | prefix | edge-infill | **ICM** |
|---|---|---|---|---|---|---|
| 6-mer masked, 150 r | r=16 | 0.851 | 0.41 | 0 % | 0 % | **12 %** |
| 6-mer masked, 150 r | r=1 | 1.219 | 0.23 | 0 % | 0 % | 0 % |
| 6-mer masked, 150 r | r=0 control | 2.454 | 0.02 | 0 % | 0 % | 0 % |
| 3-mer masked, 150 r | r=16 | 1.296 | 0.31 | 0 % | 0 % | 0 % |
| next-token, 150 r, same data | r=16 | **0.000** | **1.00** | **100 %** | n/a | n/a |
| next-token, 150 r | r=0 control | 3.55 | 0.03 | 0 % | n/a | n/a |

**So "a masked objective reproduces nothing" is false, and it is our own backbone that falsifies it,
not only NT.** Three of 25 canaries come back verbatim from a cell that the two published protocols
call clean, with the non-member control at 0 % under the same decoder and its Hamming distance
moving the wrong way (34.8 against 33.9), so the gain is not decoder luck.

**(c) The mechanism, which is the part that makes this a better paper.** A next-token model at 150
rounds has the target half at **0.000 bits/nt with the true token top-1 at every single step** --- no
decoder cleverness is needed, which is why every causal cell reads 100 %. A masked model holds the
record too (0.85 against 2.45 for the matched control) but its per-step accuracy is 0.41, and
all-48-exact needs every step at once. That is where the tokeniser enters: **the 6-mer target is 8
decoding steps and the 3-mer target is 16**, at 0.41 against 0.31 per step, which is an exponential
difference in the joint and explains why the finer tokeniser never emits even when it stores as
much. The tokeniser axis and the extraction ruler are now connected by a measured quantity rather
than by the token-rarity hypothesis alone (3.16).

**(d) Scale alone does not turn masked extraction on.** `queue_1012a` stage 1, 150 rounds on
chromosome 22, from scratch:

| backbone | 3-mer r=16 target / top-1 / ICM | 6-mer r=16 target / top-1 / ICM |
|---|---|---|
| 12.6M | 1.296 / 0.31 / 0 % | 0.851 / 0.41 / **12 %** |
| 59.9M | 1.044 / 0.44 / 0 % | 1.237 / 0.19 / 0 % |
| 201M | 1.365 / 0.32 / 0 % | 1.862 / 0.03 / 0 % |

Sixteen times the parameters changes nothing, and the 201M cell holds the target half *less* than
the 12.6M one. So the Nucleotide Transformer's 18-28 % is unlikely to be a parameter count, which
leaves the pretrained prior --- stage 2 of the same queue, masked chromosome-21 pretraining feeding
the same fine-tune, now the decisive half. Caveat to settle with the floors: a 201M model at 150
rounds may simply sit at a different point on its own trajectory, so this is read at matched rounds
and not yet at matched overfitting.

**(e) Two corrections to 3.40, both mine.** (1) I wrote "0.12 bits/nt against a 2.000-bit chance
level" for the chromosome-22 cells. **Wrong**: those canaries are real haplotype segments from
`canaries_chr22.npz`, so 2.000 is the loss of a uniform predictor and not chance, and part of a real
canary's score is biology the model legitimately learned. The paper's own rule is excess against a
matched non-member control, and on that footing (`pilot2/prefix_vs_pll.py`) our 150-round cells
carry excess 1.57 (3-mer) and 1.89 (6-mer) at r=16 against NT's 1.19 --- the direction of the claim
survives, the arithmetic behind it did not. Raw bits are also not comparable between models whose
held-out floors differ (NT 1.632, ours 2.176). (2) I wrote that our Evo canary "is a fraction of
that example's supervised tokens" where the predecessor's is the whole example. **Also wrong, and
backwards**: their 64-nt canary is 12.5 % of a 512-token left-padded row and ours is 96 of 288 nt,
i.e. 33 %. The real differences are that the rest of their row is zero-entropy padding rather than
real genome competing for capacity, that every repetition is byte-identical and position-locked to
the window end, and that their loss ignores the padding (`ignore_index=pad_token_id`) so all of the
gradient is on the canary. The experiment must be written about identical position-locked
repetitions, not about token fractions, and it must ignore PAD in the loss or a drop in memorisation
would have a second explanation.

**(f) Three latent faults found before they cost anything.** `pilot2/infill_audit.py` rebuilt the
backbone with the default 512/4/8 geometry and its run-name pattern could not match the `_ft` names
`--init_from` produces, so the audit of `queue_1012a` --- both its 59.9M/201M arm and its
pretrained-prior arm, the arm that decides the paper's wording --- would have died or silently
skipped every cell. Its r=0 control also used a hardcoded offset 96 rather than `score_run`'s own
fresh draw, so it was not phase-matched. All three are fixed in `recon_audit.py`; `infill_audit.py`
itself is left alone until `queue_1012a` finishes, because that queue is mid-flight and every one of
its cells has to be scored by the same code.

**(g) Running now.** `queue_1012c` re-asks the whole masked grid (92 cells, five datasets, four
tokenisers, two mask rates, saved checkpoints, no training) with all three decoders, on card 0.
`queue_1012a` is in its causal wave, then the prior arm. `queue_1012b` holds for cards. Deferred
until nothing is in flight, because they touch files those queues import: the `--canary_alone`
flag for the Evo replication, and ICM on NT itself, which needs an NT fine-tune that saves its
weights since the released-checkpoint runs did not.

### 3.42 (12 Oct, 23:00) The masked 0 % is an attack-strength artefact: the record is there, and extraction rises monotonically with search budget

**(a) First, the grid survives.** `queue_1012c` re-asked every masked cell with a saved checkpoint
under all three decoders: **544 cells, 408 member rows, and exactly ONE extracts anything** --- the
150-round 6-mer cell at r=16. Five datasets, four tokenisers, two mask rates, two or three seeds,
and the 59.9M and 201M scale cells are all 0 % under prefix, edge-conditioned infilling and ICM
alike. So the paper's table is not wrong; it is incomplete in one place.

**(b) But my mechanism was wrong, and the right one changes the claim.** I reported the
prefix-conditional per-step top-1 rate as a ceiling. ICM beat it by two orders of magnitude (0.010
against 0.12), because ICM conditions on the suffix and on the other target tokens while a
prefix bound assumes left-to-right. The predictor that matches the decoder is **leave-one-out**:
every other target token held at its true value, one masked --- exactly the conditional the PLL
scorer reads and the one ICM converges to. At 150 rounds on chromosome 22:

| cell | tier | LOO bits/nt | LOO per-token top-1 | ceiling | prefix | ICM (1 restart) |
|---|---|---|---|---|---|---|
| 6-mer | r=16 | 0.134 | **0.97** | 0.84 | 0 % | 12 % |
| 6-mer | r=1 | 0.271 | 0.89 | 0.50 | 0 % | 0 % |
| 3-mer | r=16 | 0.116 | **0.96** | 0.72 | 0 % | 0 % |
| 6-mer | r=0 control | 2.490 | 0.02 | 0.000 | 0 % | 0 % |

**Given seven of its eight target tokens, the model names the eighth correctly 97 times in a
hundred.** The record is not partially retained, it is essentially present. So the 0 % was never an
information limit --- it is a **search** limit: one descent from one initialisation lands on the
wrong fixed point.

**(c) And the search gap closes as you spend on it.** `extract_icm --restarts` adds random
admissible starts beside the published joint-argmax one, sweeps each to a fixed point, and outputs
the one with the best **pseudo-log-likelihood** --- a quantity an attacker computes without the
answer, so this stays an attack and not an oracle. 6-mer, 150 rounds, 25 probes per tier:

| restarts | r=16 exact | r=1 exact | mean wrong nt (r=16) | oracle = attack? |
|---|---|---|---|---|
| 1 | 12 % | 0 % | 26.4 | yes |
| 2 | 16 % | 0 % | 24.0 | yes |
| 4 | 20 % | 0 % | 20.8 | yes |
| 8 | 20 % | **4 %** | 21.0 | yes |
| 16 | 24 % | 4 % | 18.8 | yes |
| 32 | **40 %** | 4 % | **12.9** | yes |

Monotone, steepening rather than flattening, and at 32 restarts it is halfway to the 0.84 ceiling
with the mean reconstruction down to 12.9 wrong nucleotides of 48 from the prefix protocol's 30.0. The non-member control stays at 0 % at
every budget, so this is not decoder noise. The truth-free selection picks the correct fixed point
whenever one exists, so the attacker needs no oracle. And at eight restarts **a canary inserted
exactly ONCE comes back verbatim from a masked model** that both published protocols call clean.

**The consequence for the paper is unavoidable: our 0 % measured the strength of our attack, and any
extraction number we publish for a masked model is a lower bound set by the compute we spent on it.**
The claim has to become quantitative --- how much work recovery takes --- rather than categorical.

**(d) The tokeniser now enters as search difficulty rather than as storage.** The 3-mer cell holds
just as much (LOO 0.96 per token, 0.116 bits/nt, ceiling 0.72) and yet eight restarts recover
nothing, and so does the oracle over those eight. Its target is **16 joint slots against the
6-mer's 8**. Under a masked objective the two tokenisers store the same record and differ only in
how hard it is to assemble --- which is a sharper statement than "finer tokenisation memorises
less", and a different one.

**(e) The objective contrast at 59.9M and 201M, for the record.** `queue_1012a` stage 1, 150 rounds,
same data and canaries:

| | 3-mer causal | 6-mer causal | 3-mer masked | 6-mer masked |
|---|---|---|---|---|
| floor at round 30 | 3.771 | 2.514 | 1.724 | 1.862 |
| r=1 extraction at round 30 | 68 % | **96 %** | 0 % | 0 % |
| r=1 extraction at round 150 | 100 % | 100 % | 0 % | 0 % |
| r=16 canary bits at 150 | 0.003 | 0.005 | 0.058 | 0.693 |

(59.9M shown; 201M is the same picture.) A causal model reproduces a single-insertion canary
**96 % of the time by round 30**, at a held-out loss it can still be argued for. Also worth
recording: **larger masked models memorise less at a fixed round count** --- r=16 canary surprise at
150 rounds is 0.140 / 0.693 / 1.691 bits/nt at 12.6M / 59.9M / 201M, because the bigger models are
simply less overfit after the same number of passes.

**(f) The prior arm, corrected.** I first read these cells off the aggregate scorer, which
normalises over all 96 nucleotides of a canary and mixed the two sizes together under one run name.
The reconstruction audit separates them, and it says something different:

| prior cell | tier | LOO bits/nt | LOO top-1 | ceiling | prefix | ICM (1 restart) |
|---|---|---|---|---|---|---|
| 12.6M, 6-mer | r=16 | 0.012 | **1.00** | 1.000 | **5 %** | **25 %** |
| 12.6M, 6-mer | r=1 | 0.043 | 0.99 | 0.967 | 0 % | 0 % |
| 12.6M, 3-mer | r=16 | 0.032 | 0.99 | 0.920 | 0 % | 0 % |
| 201M, 3-mer | r=16 | 0.084 | 0.97 | 0.790 | 0 % | 0 % |
| 201M, 6-mer | r=16 | 1.831 | 0.03 | 0.000 | 0 % | 0 % |

So a chromosome-21 prior does change whether the record comes out: the 12.6M 6-mer cell extracts
**5 % under the published prefix protocol** at a held-out loss that is not degraded, which no
from-scratch cell at any scale did. My earlier sentence that the prior "changes how much is stored,
not whether it comes out" was wrong and is withdrawn. What survives is that the prior does not do it
for the 3-mer at either size, and that the 201M 6-mer cell with a prior barely memorises at all
because it is nowhere near overfitting after 150 rounds. Honest limitation: ten rounds on 60,000
chromosome-21 windows is not a foundation-model prior, so this bounds "a little pretraining" and not
NT's actual pretraining.

**(h) The one discriminator that holds across everything measured tonight.** Storage is close to
universal once a masked cell passes its utility optimum: leave-one-out top-1 reaches 0.96 to 1.00 in
every such cell, at every multiplicity, single insertions included. What differs is reachability,
and the variable that tracks it is the number of joint slots the target occupies --- 8 for the
6-mer, 16 for the 3-mer. Eight slots yielded 5 % to 48 % depending on search budget, prior, and
round count. Sixteen slots yielded 0 % in every cell, at every budget up to 128 restarts, including
cells whose per-token knowledge is perfect. Whether that is a barrier or only a delay is what
`queue_1012g` is running now.

**(g) Running.** `queue_1012d`: seeds 1 and 2 at 150 rounds (the 12 % rested on one seed) and seed 0
pushed to 300 rounds. `queue_1012e`: the eight-restart attack on the scale cells, the prior arm and
the 30-round contrast. `queue_1012a` is on its last fine-tune; `queue_1012b`'s 500M cells follow it.

### 3.43 (13 Oct, 01:00) At 300 rounds the published protocol extracts from a masked model, and the slot count turns out to be a delay

**(a) Both tokenisers end up storing the record perfectly.** 300 rounds on chromosome 22, seed 0,
20 probes per tier, leave-one-out conditioning:

| cell | tier | LOO bits/nt | LOO top-1 | prefix protocol | ICM (1 restart) |
|---|---|---|---|---|---|
| 6-mer | r=16 | 0.001 | **1.00** | **10 %** | 40 % |
| 6-mer | r=4 | 0.001 | **1.00** | 0 % | 20 % |
| 6-mer | r=1 | 0.001 | **1.00** | 0 % | **20 %** |
| 3-mer | r=16 | 0.001 | **1.00** | 0 % | 0 % |
| 3-mer | r=1 | 0.008 | **1.00** | 0 % | 0 % |
| control | r=0 | 3.37 | 0.02 | 0 % | 0 % |

A leave-one-out top-1 of 1.00 at 0.001 bits/nt means that given the other target tokens the model
names the remaining one correctly **every time**, at every multiplicity, for a canary inserted
**once**. Storage is not partial and it is not a function of the tokeniser.

**Two firsts here.** The protocol the paper reports --- reveal 48 nucleotides, greedy-decode 48 ---
**extracts 10 % from a masked model with no help from us**, so the published 0 % was a statement
about the training budget as well as about the attack. And ICM recovers 20 % of canaries that were
inserted exactly once, which is the number that matters for a privacy claim.

**(b) The 16-slot barrier is a delay, not a wall.** The 3-mer target occupies 16 joint slots against
the 6-mer's 8, and through every cell so far that difference looked absolute: 0 % at 1, 8, 32 and
128 restarts even where per-token knowledge was perfect. At 300 rounds with 32 restarts it breaks
--- 5 % at r=4 --- so the slot count buys search time rather than immunity. That is the same shape
as every other lever in this paper (3.20, 3.24): **delay, not prevention**, and it is now measured
for the one lever we had been tempted to call a barrier.

**(c) The 150-round restart curve, complete.** 6-mer, 25 probes per tier:

| restarts | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
|---|---|---|---|---|---|---|---|---|
| r=16 exact | 12 % | 16 % | 20 % | 20 % | 24 % | 40 % | 44 % | **48 %** |
| r=1 exact | 0 % | 0 % | 0 % | 4 % | 4 % | 4 % | 4 % | 4 % |
| wrong nt (r=16) | 26.4 | 24.0 | 20.8 | 21.0 | 18.8 | 12.9 | 11.3 | 11.8 |

It flattens near 48 % against a ceiling of 0.84, so our attack is leaving something on the table but
is no longer cheap to improve. The non-member control is 0 % at every budget and the truth-free
pseudo-log-likelihood selection equals the oracle at every budget, so the attacker needs no answer
key.

**(d) Seeds replicate.** At one restart the 150-round 6-mer cell gives 12 %, 15 % and 5 % at seeds 0,
1 and 2, with leave-one-out top-1 0.97, 0.98 and 0.97 --- so the storage is identical across seeds
and only the search outcome varies, which is what a search-limited quantity should look like. The
3-mer cells are 0 % at all three seeds with leave-one-out top-1 0.96 to 0.98.

**(e) The last Evo variable, implemented without touching anything shared.** `--canary_alone` in
`pilot2/evo.py` fills the host row with PAD and writes the canary at `PROBE_OFFSET`, and masks PAD
out of the loss to match the predecessor's `ignore_index=pad_token_id`. It reproduces the four things
their planting has and ours does not: byte-identical repetitions, a locked position, zero-entropy
context, and all of the gradient on the canary. Confined to `evo.py` --- no shared builder, scorer or
tokeniser is touched, so nothing else in the paper can move under it --- and because the canary stays
at `PROBE_OFFSET` the geometry is exactly what `score_run` probes under `--probe_offset fixed`, with
the non-member control padded to match so it measures membership rather than padding. Smoke test
rewrote 34 rows correctly; the real cell is training. The baseline it is read against already exists:
`queue_1011g`'s fixed-offset cell is the same configuration with real hosts.

**Correction to my own earlier summary**, which the audit caught: their canary is 64 of 512 tokens
(12.5 % of its row) and ours is 96 of 288 (33 %), so the canary is a *smaller* fraction of its
example there. The variable is identical position-locked repetitions against varied hosts, not token
share.

**(f) Where the paper stands after tonight.** Storage is close to universal once a masked cell passes
its utility optimum, at every multiplicity, for both tokenisers. What varies is the work needed to
read it back, and three things set that work: the objective (a causal model needs none --- 0.000
bits/nt on the target half, the true token top-1 at every step, 100 % extraction), the number of
joint slots (8 against 16, worth everything at 150 rounds and a delay by 300), and the attacker's
search budget (12 % to 48 % on one cell). None of them is a defence, and the paper has to be written
in those terms.

### 3.44 (13 Oct, 05:00) A record inserted once comes back 95 % of the time, and the protocol this field uses calls it 0 %

**(a) The number.** 6-mer masked, human chromosome 22, 300 rounds, 128 restarts of the
iterated-conditional-modes decoder, 20 probes per tier:

| tier | prefix protocol | **ICM** | mean wrong nt of 48 |
|---|---|---|---|
| r=16 | 10 % | **95 %** | 0.2 |
| r=4 | 0 % | **80 %** | 5.9 |
| r=1 (**one** insertion) | 0 % | **95 %** | 1.6 |
| r=0 non-member | 0 % | **0 %** | 35.6 |

The reconstruction is not approximate: at r=16 it is wrong by two tenths of a nucleotide out of 48 on
average. The non-member control is 0 % under the same decoder with 35.6 wrong, and the attack chooses
its own output by pseudo-log-likelihood, so none of this needs an answer key. The 3-mer cell at the
same budget gives 10 % at r=4 and 0 % elsewhere: **16 joint slots against 8 is a cost, not a
barrier.**

**(b) What this does to the paper.** Our headline claim --- the objective decides whether whole
records come back --- is dead, and we killed it with our own stronger attack rather than having a
reviewer do it. What replaces it is worth more than what it replaces, and it is methodological:

- **Measured memorisation is attack-relative.** The same checkpoint reads 0 % or 95 % depending only
  on the decoder, and the decoder that works is the one matching the conditional the model was
  trained on.
- **The prefix protocol under-reports a masked model by up to 95 percentage points.** That protocol
  --- reveal a prefix, greedy-decode the rest --- is what this field uses, including the predecessor
  and including every table we have published so far. For a bidirectional model it is the wrong
  question, and the gap is not a correction factor, it is the whole measurement.
- **The objective and the tokeniser change the cost of extraction, not its possibility.** A causal
  model needs no search at all (0.000 bits/nt on the target half, the true token top-1 at every
  step, 100 %). A masked model needs a search whose difficulty scales with the number of joint slots
  --- 8 for the 6-mer, 16 for the 3-mer --- and with how far past its utility optimum it was trained.
  Every lever we have is a cost multiplier. None is a defence.

**(c) Where the number comes from, in one line each.** Storage: leave-one-out top-1 is 1.00 at
0.001 bits/nt, so given the other target tokens the model names the remaining one correctly every
time, at every multiplicity. Search: one descent gets 20 %, 128 restarts get 95 %, and the selection
rule needs no truth. Budget: 150 rounds gave 48 % at r=16 and 0 % at r=1; 300 rounds gives 95 % at
both.

**(d) NT v2 at 500M, for the scale point on a released checkpoint.** Under the prefix protocol
alone, r=16 extraction reaches **38 % on E. coli** (round 50, floor 2.210) and **32 % on chromosome
22** (round 50, floor 1.662), against 250M's 28 % and 18 %. At a single insertion it is 0 % at every
round on both. So scale raises extraction on the released family too, and the single-insertion tier
is where the search decoder would have to be pointed next.

**(e) Three things this immediately demands, now running as `queue_1013b`.**
1. **Early stopping.** Sec. 6 recommends stopping at the held-out optimum and the whole grid reports
   0 % at 30 rounds --- but that was one restart. 128 restarts on the 30-round cells decides whether
   the paper's one surviving recommendation survives.
2. **Generalisation.** 300 rounds is measured only on human. The same cells on E. coli, yeast, GUE
   and synthetic say whether 95 % is a chromosome-22 fact.
3. **Seeds.** 95 % rests on seed 0, exactly as 12 % did before seeds 1 and 2 gave 15 % and 5 %.

**(f) Still running.** The Evo `--canary_alone` cell (card 3, about five hours for 25 rounds) and the
last of the prior-arm audits.

### 3.45 (13 Oct, 17:30) All four questions answered: the protocol is wrong, early stopping is real, the tokeniser sets the price, and the Evo disagreement is resolved

**(a) The under-reporting is universal, not a chromosome-22 fact.** 6-mer masked, 300 rounds, 128
restarts, 20 probes per tier, five datasets:

| dataset | r=16 standard -> ours | r=1 (**one** insertion) standard -> ours | wrong nt of 48, ours |
|---|---|---|---|
| E. coli | 15 % -> **100 %** | 15 % -> **100 %** | 0.0 |
| yeast | 15 % -> **95 %** | 5 % -> **100 %** | 0.0-0.8 |
| GUE | 10 % -> **100 %** | 0 % -> **95 %** | 0.0-1.4 |
| synthetic | 0 % -> **100 %** | 5 % -> **100 %** | 0.0 |
| human chr22 | 10 % -> **95 %** | 0 % -> **95 %** | 0.2-1.6 |

Non-member controls stay at 0 % under the same decoder with 33-36 of 48 wrong. Seeds 1 and 2 on
human give 95 %/100 % and 90 %/95 % at r=16/r=1, so the number is not a seed artefact. **A masked
model trained past its optimum returns essentially every planted record, including records inserted
exactly once, and the protocol this field uses reports 0 to 15 %.**

**(b) Early stopping survives the strongest attack we have, and that is the paper's one real
recommendation.** At 30 rounds -- at or near the held-out optimum -- 128 restarts recover **0 % at
every tier, both tokenisers, both seeds**. And the reason is visible in the right statistic:
leave-one-out top-1 is **0.03 to 0.21**, against 1.00 at 300 rounds. The record is not hidden at the
optimum, it is **not yet stored**. So early stopping is not a decoding accident; it is the one lever
we have tested that removes the thing an attacker would search for.

**(c) The tokeniser sets the price, and the price is the whole outcome.** At 300 rounds the 3-mer
cells store the record just as completely on human (leave-one-out top-1 1.00 at 0.001 bits/nt, all
three seeds) and return **0 %**, where the 6-mer returns 90-100 %. The target is 16 joint slots
against 8. On E. coli, yeast, GUE and synthetic the 3-mer is 0 % as well. The only exceptions found
anywhere are 5-10 % on synthetic and at r=4, so it is a cost rather than a barrier -- but at every
budget we can afford, a 16-slot target is the difference between recovering everything and
recovering nothing.

**(d) The Evo disagreement is resolved, with one variable.** Same model, same LoRA configuration,
same corpus size, same 25 rounds, same held-out loss (1.473 against 1.478). The only difference is
whether a canary is its own training example or embedded in a varied host window:

| ruler at round 25 | real hosts | **canary alone** |
|---|---|---|
| r=16 canary surprise | 2.015 (chance) | **0.098** |
| r=16 rank-1 | 0.15 | **1.00** |
| r=16 verbatim extraction | **0 %** | **70 %** |
| r=16 wrong nt of 48 | 35 | **6** |
| r=4 rank-1 | 0.00 | **1.00** |
| r=1 rank-1 | 0.00 | **0.75** |

So the predecessor's 100 % is real and reproducible, and it is a property of **planting whole,
byte-identical, position-locked examples** rather than of Evo, of scale, or of byte-level
tokenisation. Our 0 % is equally correct for canaries embedded in varied hosts. Both numbers belong
in the paper with the mechanism between them, and this is the kind of disagreement that is worth
more resolved than either number alone. Note the single-insertion tier: recognised at 0.75 and
reproduced at 0 %, so even whole-example planting does not give verbatim recovery of a once-seen
record at 25 rounds.

**(e) The paper, as it now stands.**

*Thesis.* Whether a genomic language model gives a training record back is not a property of the
model. It is a property of the model together with how well the question is asked, and the standard
way of asking is wrong for half of all models.

*Method.* Three rulers on planted records -- surprise, recognition, reproduction -- plus the one
statistic that predicts reproduction, which is the model's accuracy on one target position given the
others, and a decoder matched to the conditional the model was actually trained on.

*Results.* (1) The standard prefix protocol under-reports masked models by up to 100 percentage
points, on five datasets, at single insertion. (2) Stopping at the held-out optimum removes the
stored record, and is the only lever tested that does. (3) Tokenisation and training budget set the
price of recovery, over three orders of magnitude of search, and neither makes recovery impossible.
(4) A 7B released model reproduces nothing when records sit in varied hosts and 70 % when each
record is its own example, which reconciles our result with the predecessor's.

*Contribution.* A corrected measurement protocol for bidirectional genomic models; a price list
across five datasets, four tokenisations, two objectives, three scales and two released
checkpoints; and the demonstration that every published claim of the form "our encoder-style
genomic model does not leak", ours included, rests on the wrong test.

### 3.46 (13 Oct, 19:00) The released-model evidence we already had, and the two bugs that would have thrown away the run meant to get more

The user's objection is that conclusions measured only on our own 12.9M backbone cannot be written
as claims about models in the world. It is correct, and acting on it turned up three things.

**(a) We already had the result, from 8 October, and never put it in the paper.** DNABERT-2, the
released 117M checkpoint, under ITS OWN native masked objective, on E. coli, re-read today from the
raw scores rather than from the old note:

| round | PLL held-out floor | r=16 bits / rank-1 / **verbatim** | r=1 rank-1 / verbatim |
|---|---|---|---|
| 15 (its best utility) | **1.568** | 0.698 / 1.00 / 0 % | 0.30 / 0 % |
| 30 | **1.594** (+0.026) | 0.048 / 1.00 / **30 %** | 0.60 / 0 % |
| 50 | 1.644 (+0.076) | 0.021 / 1.00 / 30 % | 0.90 / 0 % |

**At 0.026 bits past its own optimum — a model anyone would ship — a released masked checkpoint
reproduces 30 % of 16x-planted records verbatim, with recognition at 1.00, under the STANDARD
protocol and with no new decoder.** The mean reconstruction is 17.2 of 48 nucleotides wrong against
38-43 before memorisation sets in. This is a materially better privacy data point than our own
300-round cell, because that cell's held-out loss is 2.866 against a 1.675 optimum, i.e. worse than
uniform, while this one costs 0.026 bits.

It also means the paper's current claim that a masked objective prevents reproduction was already
contradicted by our own released-model data from five days ago, which the draft does not report.
That contradiction is in our files and a reviewer can find it.

**(b) So the released-model account is now three-quarters built, not empty.**

| claim | released-model evidence | status |
|---|---|---|
| masked released models store records completely | DNABERT-2 r=16 at 0.048 bits with rank-1 1.00; NT 250M and 500M | validated |
| and reproduce them verbatim at usable utility | DNABERT-2 30 % at +0.026 bits from its optimum | validated |
| including records present as a single copy | recognition 0.60-0.90, verbatim 0 % under the standard protocol | NOT yet |
| the standard protocol under-reports masked models | needs the search decoder on a released checkpoint | running |

The single-copy row is exactly where the new decoder has to be pointed, and it is the row that
matters for a privacy claim, because a rare haplotype is unique to one person.

**(c) Two bugs that would have silently wasted the runs meant to settle (c).** Both found by audit,
both verified. `recon_audit.rebuild` called our backbone's objective parser before deciding whether
the cell is a released one; that parser demands `mlm@<rate>` and raises on the bare `mlm` that
`nt.py` writes and the `causal` that `dnabert.py` writes, so every released cell died before the
decoder ran. Worse, it read `n_val` and `n_test` unguarded, and `dnabert.py`, `dnabert2.py` and
`hyena.py` all pass 200 without recording it — and probe HOSTS are drawn from the windows after
`n_train + n_val + n_test`, so a wrong value silently relocates every canary into a window the model
never trained on and the decoder returns a confident number for the wrong sequence. Fixed, and
verified by running the decoder on the ep15 checkpoint of the NT fine-tune still in flight:
leave-one-out per-position accuracy 0.77 for members against 0.00 for the matched control.

**(d) Keeping checkpoints is now the default, at the user's instruction, and it was never a real
saving.** `/data` has 5.3 TiB free against the 59 GiB all our outputs occupy; a snapshot of our
backbone is 56 MiB and of NT 250M about 0.9 GiB. The cost of deleting them was not disk, it was that
the decoder could only ever be pointed at a run's last round — which is why the
extraction-against-held-out-loss curve had to be faked by retraining at 150 and 300 rounds, and why
every released masked checkpoint had to be retrained from scratch today rather than merely
re-scored.

**(e) The decoder for overlapping k-mers, which can only live in nucleotide space.** One token at a
time is undefined on DNABERT: with stride 1 a valid token string satisfies
`token_t[1:] == token_{t+1}[:k-1]`, so changing one token contradicts the 2(k-1) overlapping it and
decodes to no DNA string; and five of a 6-mer's six letters are visible in its neighbours anyway, so
the conditional is answerable from context with no memorisation. `pilot2/recon_overlap.py` re-masks
one NUCLEOTIDE at a time by masking the k tokens covering it and marginalising onto that letter,
which is the conditional DNABERT was pretrained on. This also makes the mechanism falsifiable on
released models: hiding 48 nucleotides takes 48+(k-1) tokens, i.e. about 48 slots for EVERY k, so the
joint-slot claim predicts a FLAT profile across DNABERT k=3,4,5,6 beside the 0-to-95 split on the
non-overlapping axis. A large spread would refute it.

**(f) And the caveat the headline is still missing.** The 300-round cells sit at a held-out loss of
2.866 (chromosome 22) and 3.164 (E. coli), both worse than the 2.000 of a uniform predictor.
`queue_1013e` retrains one cell per tokeniser with twelve snapshots kept and runs the decoder at
every one, so the paper can publish the curve of recovery against utility instead of an endpoint at
a utility nobody would accept. The interesting region is between round 30 (floor 1.675, 0 %) and
round 150 (floor 2.176, 48 %), and it has never been measured with this decoder.

### 3.47 (13 Oct, 19:30) "150 rounds" and "300 rounds" are not two points on one trajectory

Noticed while the curve run was scoring its snapshots, and it corrects something I have written
several times. The 3-mer cell of `queue_1013e` reports a held-out floor of **2.353 at epoch 150**,
where the 3-mer cell of `queue_1011h` reported **2.074 at epoch 150**. Same tokeniser, same seed,
same data, same probe block. The difference is the learning-rate schedule: `pilot2/train.py:143`
computes the decay as `(step - warmup) / (total - warmup)`, and `total` is the whole run's step
count. So epoch 150 of a 300-epoch run is **mid-decay at a much higher learning rate** than epoch
150 of a 150-epoch run, and it is a different model.

Three consequences.

**(a) A sentence I have repeated is wrong as stated.** "150 rounds gives 48 % and 300 rounds gives
95 %" reads as two points on one trajectory. They are two separate runs with different schedules,
and the only honest way to put them side by side is by their own held-out losses: 48 % at a floor of
2.176, and 95 % at a floor of 2.866.

**(b) The curve must be plotted against held-out loss, not against round number.** That is already
what `queue_1013e` does -- twelve snapshots of ONE run, each carrying its own floor -- which turns
out to be necessary rather than merely tidy. Round number is not comparable across budgets and the
paper should not use it as an axis anywhere that two budgets are compared.

**(c) It also explains why the early-stopping result is cleaner than it looked.** The 30-round cells
that recover 0 % under 128 restarts were trained with a 30-epoch schedule, so they are fully decayed
and genuinely converged at their optimum, not merely stopped early in a longer schedule. Those are
two different claims and we have the stronger one: a model trained to convergence at its optimum
holds nothing the decoder can find. What we do NOT yet have is the other one -- stopping a long run
early -- and the twelve-snapshot curve supplies exactly that, because every snapshot comes from a
single 300-epoch schedule.

### 3.48 (13 Oct, 20:30) A released DNABERT stores the record perfectly at no utility cost, and the standard protocol says zero

**(a) The cleanest setting we have for the under-reporting claim, and it is on released weights.**
DNABERT k=3 and k=4, 150 rounds on E. coli, `--mask_nt_rate 0.05`, the configuration the family was
already measured with:

| | ep15 | ep50 | ep150 |
|---|---|---|---|
| held-out floor, k=3 | 1.774 | **1.724** (best) | 1.739, i.e. **+0.015** |
| r=16 canary bits | 1.846 | 0.070 | **0.003** |
| r=16 recognition | 0.40 | 1.00 | **1.00** |
| r=16 verbatim, STANDARD protocol | 0 % | 0 % | **0 %** |
| r=4 recognition | 0.00 | 0.50 | **1.00** |
| r=1 recognition | 0.00 | 0.00 | **0.58** |

k=4 is the same picture (0.004 bits/nt and recognition 1.00 at ep150, floor 1.739 against a best of
1.725). **A released checkpoint, at fifteen thousandths of a bit above its own best held-out loss,
holds a 16x-planted record at 0.003 bits/nt and names it first out of a hundred candidates every
time, and the protocol this field uses reproduces none of it.** The record is demonstrably present
and the model is demonstrably useful, so whether it comes out is a question about the decoder and
nothing else. That is a far better setting for the argument than our own 300-round cell, whose
held-out loss is 2.866 against a 1.675 optimum.

Note also that these models do NOT degrade the way our from-scratch cells do: the floor is flat from
ep50 to ep150. A pretrained 86M checkpoint fine-tuned on 5,000 windows memorises the planted records
without paying for it in held-out loss at all, which is the regime an actual practitioner is in.

`queue_overlap` is now running the nucleotide-level decoder on those weights, at their final round
and at their own optimum (ep50). Every snapshot was kept, so the DNABERT utility curve is available
too.

**(b) The utility curve, first two points, and they are the reassuring end.** One 300-round run of
the 6-mer cell, twelve snapshots, each read with 128 restarts:

| snapshot | floor | from best | LOO per-token top-1 (r=16) | verbatim, both protocols |
|---|---|---|---|---|
| ep15 | 1.866 | +0.040 (still improving) | 0.03 | 0 % |
| ep30 | **1.825** | **the optimum** | 0.07 | 0 % |
| non-member control | | | 0.02 | 0 % |

At and before the optimum the record is **not stored**: the leave-one-out accuracy is 0.03-0.07
against 0.02 for a sequence the model never saw. So the 0 % there is not a decoder failing to find
something, it is nothing being there. The decisive points are ep45 (+0.003), ep60 (+0.054), ep80
(+0.171) and ep100 (+0.351), all running.

**(c) NT 250M at round 50, for the record.** Floor 2.263 on E. coli (its optimum is 1.823) and 1.632
on chromosome 22 (optimum 1.376). Leave-one-out top-1 is **0.98** at r=16 on both, against 0.01 and
0.07 for the matched controls, with ceilings of 0.87 and 0.90 -- so a released 250M checkpoint also
stores the record almost completely. The standard prefix protocol already gets **35 %** (E. coli)
and **25 %** (chromosome 22), and 5 % at a single insertion on chromosome 22.

One thing to be careful about: at ONE restart the search decoder is WORSE than the prefix protocol
here (5 % against 35 %), the opposite of our backbone. NT is pretrained and 250M, so its
prefix-conditional is already strong (target top-1 0.78), and a single descent lands on the wrong
fixed point. The 128-restart pass is what the claim rests on and it is still running.

### 3.49 (13 Oct, 21:00) DNABERT holds the record perfectly and nothing can get it out, which is the mechanism confirming itself and the scope narrowing

**(a) The result.** DNABERT k=3, released weights, E. coli, round 150 at a held-out loss of 1.739
against its own best of 1.724, read with the nucleotide-level re-masking decoder at 32 restarts,
20 probes per tier:

| tier | LOO per-nucleotide top-1 | LOO bits/nt | implied ceiling | ICM-nt | oracle over 32 restarts | wrong nt of 48 |
|---|---|---|---|---|---|---|
| r=16 | **1.00** | 0.004 | **0.968** | **0 %** | **0 %** | 35.7 |
| r=4 | 0.91 | 0.361 | 0.233 | 0 % | 0 % | 36.4 |
| r=1 | 0.35 | 2.050 | 0.000 | 0 % | 0 % | 36.0 |
| r=0 control | 0.28 | 2.277 | — | 0 % | 0 % | 36.5 |

Given the other target nucleotides the model names the remaining one correctly **every single time**,
at 0.004 bits/nt, and the ceiling says 97 % of records should be reconstructible. The search recovers
**nothing** -- not once in 32 restarts across 20 probes -- and its reconstruction sits at the chance
Hamming distance, indistinguishable from the non-member control.

**(b) This is the mechanism confirming itself, on released weights.** Overlapping k-mers pin the
joint-slot count to the nucleotide count: hiding 48 nucleotides needs 48+(k-1) tokens, so the target
is **48 joint slots for every k**. Our own non-overlapping cells already showed 8 slots giving
90-100 % and 16 slots giving 0 %. Forty-eight slots giving 0 % is the same law continued, and it is
now measured on a released checkpoint rather than on a backbone we trained. The claim that the
joint-slot count sets the price of recovery has survived the test that could have refuted it.

**(c) And it narrows the scope of the headline, usefully.** "The standard protocol under-reports
masked models" is NOT true of DNABERT. There the standard protocol's 0 % is operationally correct:
the record is in the weights, but no decoder we can build gets it out, so the number a practitioner
cares about really is zero. The honest claim is narrower and sharper:

> The standard protocol under-reports masked models **whose target occupies few joint slots** --
> coarse non-overlapping tokenisation. It is accurate for fine or overlapping tokenisation, where the
> record is stored but unreachable.

That makes tokenisation the lever, not the objective, and it makes the recommendation concrete:
a fine or overlapping vocabulary keeps a fully memorised record out of reach, and that is a much
stronger thing to be able to say than "masked objectives are safer".

**(d) What this does to the released-model account.** The under-reporting claim now rests entirely on
the two released checkpoints with few-slot targets: NT v2 250M, whose 4096 non-overlapping 6-mers are
literally our own axis and whose 128-restart pass is still running, and DNABERT-2, whose BPE is also
non-overlapping and which is queued. DNABERT's four k variants become the negative control they were
predicted to be, and HyenaDNA and Evo stay on the causal side where the prefix protocol is already
the matched idiom. If NT and DNABERT-2 both come back at or near their ceilings, the claim is
established on released models with a mechanism and a control. If they come back at 0 % like
DNABERT, then the 95 % on our own 6-mer backbone is bounded to from-scratch models and the abstract
must say so.

**(e) The utility curve, third and fourth points.** The 6-mer cell, one 300-round run:

| snapshot | floor | from best | LOO top-1 (r=16) | verbatim |
|---|---|---|---|---|
| ep30 | 1.825 | the optimum | 0.07 | 0 % |
| ep45 | 1.829 | +0.003 | 0.17 | 0 % |
| ep60 | 1.879 | +0.054 | 0.37 | 0 % |

Storage is climbing steadily (0.07, 0.17, 0.37) while recovery stays at zero, so the turn has not
happened yet and the remaining points -- +0.171, +0.351 and beyond -- are where it must be.

### 3.50 (13 Oct, 21:40) Early stopping does not protect a released checkpoint, and the pretrained model leaks at a utility you would ship

**This reverses the recommendation in 3.45(b).** The early-stopping result was measured on our own
from-scratch backbone, where at the optimum there is nothing stored to find. On a released,
pretrained checkpoint that is false.

**(a) NT v2 250M, round 15, held-out loss 1.851 against its own optimum of 1.823 — plus 0.028 bits,
which is a model anyone would ship:**

| tier | standard protocol | **128 restarts** | oracle | LOO per-token top-1 |
|---|---|---|---|---|
| r=16 | **0 %** | **10 %** | 15 % | 0.70 |
| r=4 | 0 % | 0 % | 0 % | 0.04 |
| r=1 | 0 % | 0 % | 0 % | 0.01 |
| r=0 control | 0 % | 0 % | 0 % | 0.01 |

Two things at once. The search decoder recovers records from a released masked checkpoint **at
0.028 bits past its optimum**, where the protocol this field uses reports zero — so the
under-reporting claim now has released-model evidence. And early stopping is **not** a defence
there: a pretrained 250M model has already stored the 16x record by round 15 (leave-one-out 0.70),
whereas our 12.9M from-scratch backbone had stored nothing at all at its optimum (0.07 against a
control of 0.02).

The honest reading of the difference is that a pretrained model does not have to spend its capacity
learning the distribution, so it memorises planted records within a handful of rounds, long before
its held-out loss degrades. Our from-scratch cells had to be ruined first. **The from-scratch
backbone was giving us a falsely reassuring picture, and only a released checkpoint could show it.**

Caveat to close: NT's optimum is round 3 and our earliest kept snapshot is round 15, so this is
measured 0.028 bits past the optimum rather than at it. `queue_ntopt` is running rounds 1, 3 and 5
with the decoder at each, which is where a practitioner would actually stop.

**(b) The utility curve on our backbone, and where it turns.** One 300-round run of the 6-mer cell,
twelve snapshots, 128 restarts at each:

| snapshot | floor | from best | LOO top-1 (r=16) | verbatim | oracle |
|---|---|---|---|---|---|
| ep30 | 1.825 | the optimum | 0.07 | 0 % | 0 % |
| ep45 | 1.829 | +0.003 | 0.17 | 0 % | 0 % |
| ep60 | 1.879 | +0.054 | 0.37 | 0 % | 0 % |
| ep80 | 1.997 | +0.171 | 0.68 | 0 % | 0 % |
| ep100 | 2.176 | +0.351 | 0.88 | **20 %** | 25 % |

So for a from-scratch model recovery begins between +0.171 and +0.351 bits, which is past the point
where the model is worse than a uniform predictor (2.000). On its own that reads as reassuring. Put
beside NT's 10 % at +0.028, it is the opposite: **pretraining moves the leak from a broken model to a
usable one**, and that is the number that matters in practice.

**(c) DNABERT at its own optimum, for completeness.** k=3, round 50, held-out loss 1.724, its best:
leave-one-out per-nucleotide top-1 **0.96** at r=16 with a ceiling of 0.360, and the nucleotide-level
decoder recovers **0 %**, oracle 0 %. So DNABERT stores the record almost perfectly even at its
optimum and still nothing comes out, because the target is 48 joint slots.

**(d) The picture, now with released-model evidence in three of four rows.**

| model | tokenisation | joint slots | utility cost where it leaks | leak |
|---|---|---|---|---|
| our 6-mer, from scratch | non-overlapping 6-mer | 8 | +0.351 (broken model) | 20 % |
| **NT 250M, released** | non-overlapping 6-mer | 8 | **+0.028 (usable model)** | **10 %** |
| our 3-mer, from scratch | non-overlapping 3-mer | 16 | never, to 128 restarts | 0 % |
| **DNABERT k=3/4, released** | overlapping | 48 | never, stores at 1.00 | 0 % |

Three claims follow, and the recommendations change.

1. **The joint-slot count decides whether recovery is possible at all.** 8 slots leak, 16 and 48 do
   not, at every budget we can afford. This is the lever, and it is a tokenisation choice.
2. **Pretraining decides whether the leak happens at a utility anyone would accept.** This is why a
   controlled from-scratch backbone cannot be the only evidence, and the user was right to insist.
3. **Early stopping is not a defence for a pretrained model**, and Sec. 6 and Sec. 8 have to be
   rewritten. What survives is the narrower statement that a from-scratch model at its optimum has
   not yet stored the record.

### 3.51 (13 Oct, 23:10) The under-reporting claim now has released-model evidence: 35 % becomes 70 % on a published checkpoint

**(a) The pillar.** Nucleotide Transformer v2 250M, the released checkpoint, E. coli, round 50
(held-out loss 2.263 against its optimum of 1.823), 128 restarts, 20 probes per tier:

| tier | standard protocol | **search decoder** | oracle | ceiling | wrong nt of 48 |
|---|---|---|---|---|---|
| r=16 | **35 %** | **70 %** | 80 % | 0.869 | 12.2 -> **7.4** |
| r=4 | 0 % | 0 % | 0 % | 0.245 | 35.4 -> 35.0 |
| r=1 | 0 % | 0 % | 0 % | 0.010 | 34.5 -> 36.1 |
| r=0 control | 0 % | **0 %** | 0 % | 0.000 | 36.7 -> 36.2 |

On a published checkpoint the protocol this field uses reports **half** of what is actually
recoverable, and the decoder gets within 0.17 of the information-theoretic ceiling its own
leave-one-out accuracy implies. The non-member control stays at 0 % and its reconstruction stays at
the chance Hamming distance, so this is recall and not decoding luck.

**(b) Together with 3.50(a) the claim is now two-sided on released weights.**

| NT 250M, E. coli | held-out loss | from its optimum | standard | ours |
|---|---|---|---|---|
| round 15 | 1.851 | **+0.028 (a model you would ship)** | **0 %** | **10 %** |
| round 50 | 2.263 | +0.440 | 35 % | **70 %** |

At a utility anyone would accept the protocol reports **zero** where records do come back. Past the
optimum it reports **half**. Both measured on weights we did not train.

**(c) An honest limit that has to be stated.** On NT the single-copy and 4-copy tiers stay at 0 %
under every decoder, and the reason is visible in the right column: their ceilings are 0.010 and
0.245, so the record is not stored well enough for any search to find it. Our own backbone reached
95 % at a single copy, but only at a held-out loss of 2.866, i.e. on a model worse than a uniform
predictor. **So "a record present once comes back" is NOT established on released weights** and must
stay a controlled-backbone statement, scoped to a ruined model. What released weights establish is
the 16-copy case, which is still the right case for duplicated reference material and for anything
that appears in a corpus more than once.

**(d) The released-model account, as it stands tonight.**

| model | tokenisation | joint slots | utility | standard | ours |
|---|---|---|---|---|---|
| NT 250M | non-overlapping 6-mer | 8 | +0.028 | 0 % | **10 %** |
| NT 250M | non-overlapping 6-mer | 8 | +0.440 | 35 % | **70 %** |
| DNABERT k=3 | overlapping | 48 | +0.015 | 0 % | **0 %** (stores at 1.00) |
| DNABERT k=4 | overlapping | 48 | +0.014 | 0 % | **0 %** (stores at 1.00) |
| DNABERT-2 | non-overlapping BPE | few | +0.026 | 30 % | queued |

k=4 reproduces k=3 exactly (leave-one-out 1.00 at 0.006 bits/nt, ceiling 0.968, recovery 0 %,
oracle 0 %), and both store the record almost perfectly **at their own optimum** too (0.94-0.96).
So the flatness the joint-slot mechanism predicted holds for the two variants measured, and k=5 and
k=6 are running.

**(e) What the paper can now say, with the evidence attached to each clause.**

1. *Measured memorisation is attack-relative.* Released checkpoint, two utility points, 0 % -> 10 %
   and 35 % -> 70 %. **Released-model evidence.**
2. *The joint-slot count decides whether recovery is possible at all.* 8 slots recover, 16 and 48 do
   not, at every budget tried; two of the four rows are released weights. **Released-model evidence
   for the negative half, controlled for the positive half.**
3. *Pretraining decides the utility at which the leak appears.* NT leaks at +0.028, our from-scratch
   cells need +0.351. **Released against controlled, which is the comparison that makes the point.**
4. *Early stopping is not a defence for a pretrained model.* NT at +0.028. **Released-model
   evidence**, and it reverses what 3.45 recommended.
5. *A single-copy record coming back* stays controlled-backbone and ruined-utility only.

### 3.52 (13 Oct, 23:40) Two complete figures: the released DNABERT family is flat, and the utility curve has a knee

**(a) Figure A, the mechanism's negative control, on four released checkpoints.** DNABERT k=3, 4, 5
and 6, E. coli, round 150, nucleotide-level re-masking at 32 restarts, r=16:

| k | LOO per-nucleotide top-1 | LOO bits/nt | ceiling | recovery | oracle over 32 restarts |
|---|---|---|---|---|---|
| 3 | 1.00 | 0.004 | 0.968 | **0 %** | 0 % |
| 4 | 1.00 | 0.006 | 0.968 | **0 %** | 0 % |
| 5 | 1.00 | 0.003 | 1.000 | **0 %** | 0 % |
| 6 | 0.99 | 0.018 | 0.841 | **0 %** | 0 % |

**Perfectly flat across the entire released family.** Every variant stores the 16x record essentially
exactly and none of them gives any of it back. That is what the joint-slot account predicts and
nothing else does: overlapping k-mers pin the target at 48 slots whatever k is, so changing k from 3
to 6 cannot change recovery. Had the spread been large the mechanism would have been refuted. It is
a stronger test than a positive result because the prediction was made first and the four
checkpoints are not ours.

One clarification the paper has to make. Our earlier DNABERT result (3.10, 3.14) found the ordering
3 < 4 < 5 < 6 monotone, and that is not contradicted: it was an ordering of **how much is stored**,
measured with the surprise ruler on causal fine-tunes in the transient. Here at round 150 all four
have saturated at 0.003-0.018 bits/nt, so the ordering has washed out, and what is being compared is
**whether what is stored can be read back**. Two different rulers, and the paper must not let them
be read as one.

**(b) Figure B, the utility curve, all twelve snapshots of one 300-round run.** 6-mer masked, human
chromosome 22, r=16, 128 restarts, each point carrying its own held-out loss:

| round | held-out loss | vs best | LOO top-1 | recovery | oracle |
|---|---|---|---|---|---|
| 15 | 1.866 | +0.040 | 0.03 | 0 % | 0 % |
| 30 | **1.825** | **optimum** | 0.07 | 0 % | 0 % |
| 45 | 1.829 | +0.003 | 0.17 | 0 % | 0 % |
| 60 | 1.879 | +0.054 | 0.37 | 0 % | 0 % |
| 80 | 1.997 | +0.171 | 0.68 | **0 %** | 0 % |
| 100 | 2.176 | +0.351 | 0.88 | **20 %** | 25 % |
| 120 | 2.368 | +0.542 | 0.95 | 50 % | 50 % |
| 150 | 2.590 | +0.765 | 0.98 | 30 % | 30 % |
| 190 | 2.750 | +0.925 | 0.99 | 75 % | 75 % |
| 230 | 2.823 | +0.998 | 1.00 | 85 % | 85 % |
| 265 | 2.847 | +1.022 | 1.00 | 95 % | 95 % |
| 300 | 2.866 | +1.041 | 1.00 | 95 % | 95 % |

Three things to read off it. **Storage saturates long before recovery starts**: leave-one-out is
already 0.68 at +0.171 where recovery is still exactly zero, which is the storage-reachability
dissociation measured along a single trajectory rather than inferred across runs. **The knee is at
about +0.35 bits**, and the model is already worse than a uniform predictor there (2.176 against
2.000). And recovery saturates at 95 %, not 100 %, with the attack matching the oracle at every
point past the knee, so the truth-free selection costs nothing.

The dip at round 150 (30 % against 50 % before and 75 % after) is sampling noise: 20 probes give a
standard error near 11 points. If this curve goes in the paper it needs 50 probes per point, which
is a cheap re-run now that the checkpoints are kept.

**(c) The comparison that matters, and it needs both figures.** For a from-scratch model the leak
begins only after the model is ruined (+0.35 bits, past uniform). For the released pretrained NT the
leak begins at **+0.028 bits**, on a model anyone would ship. Reporting either alone misleads: the
first reads as reassuring, the second as alarming. **The honest statement is that pretraining moves
the knee from a broken model to a usable one**, and that is only visible because we have both.

### 3.53 (14 Oct, 17:00) Overnight: early stopping does work on a released model, a single-copy record does come back, and the slot law is airtight

All seven queues finished. Two of last night's conclusions change, both in the direction of being
more precise rather than less useful.

**(a) CORRECTION to 3.50. Early stopping IS a defence on a released checkpoint, with a 0.028-bit
margin.** I tested NT at round 15 and found 10 % recovery, and concluded early stopping fails. But
NT's optimum is round 3, and round 15 is twelve rounds past it. Measured AT the optimum:

| NT 250M, E. coli | held-out loss | vs optimum | LOO top-1 (r=16) | recovery |
|---|---|---|---|---|
| round 1 | 1.834 | +0.011 | 0.02 | 0 % |
| round 3 | **1.823** | **the optimum** | 0.01 | 0 % |
| round 5 | 1.826 | +0.003 | 0.03 | 0 % |
| round 15 | 1.851 | +0.028 | **0.70** | **10 %** |
| round 50 | 2.263 | +0.440 | 0.98 | 70 % |

At the optimum the record is **not stored at all** -- leave-one-out 0.01 against a non-member control
of 0.01 -- and nothing is recoverable under any decoder. So the recommendation survives on released
weights. What it costs is the margin: between round 5 and round 15 the model goes from storing
nothing to storing 0.70 and leaking 10 %, and the whole transition is worth **0.028 bits** of
held-out loss. That is inside the noise with which anyone picks a checkpoint, which is the
knife-edge Sec. 6 already describes, now measured on a released model and on the extraction ruler
rather than the surprise ruler.

So the honest claim is neither 3.45's "early stopping removes the stored record" nor 3.50's "early
stopping is not a defence". It is: **stopping at the optimum works, and the margin is three
hundredths of a bit.**

**(b) CORRECTION to 3.51(c). A single-copy record does come back from released weights, on human.**
NT 250M, chromosome 22, round 50, where the canaries are real rare haplotype segments:

| tier | standard protocol | **ours** | oracle | LOO top-1 |
|---|---|---|---|---|
| r=16 | 25 % | **65 %** | 75 % | 0.98 |
| r=4 | 0 % | **10 %** | 15 % | 0.70 |
| **r=1 (one copy)** | 5 % | **10 %** | 15 % | 0.62 |
| r=0 control | 0 % | **0 %** | 0 % | 0.07 |

I wrote last night that single-copy recovery was not established on released weights, on the basis of
the E. coli cell where r=1 is 0 %. On chromosome 22 it is 10 %, with the control at 0 %. The
difference is that E. coli's canaries are synthetic and chromosome 22's are real haplotypes, which
the pretrained model finds easier to hold. **So the strongest privacy statement now has
released-model evidence: a real rare-variant haplotype present once in the fine-tuning corpus is
reproduced verbatim from a published checkpoint.** It is 10 %, not 95 %, and the model is 0.44 bits
past its optimum, and both of those belong in the sentence.

**(c) The slot law, now with twelve points per tokeniser and 50 probes at the knee.** The 20-probe
dip at round 150 was sampling noise and is gone; the curve is monotone.

| vs optimum | 6-mer (8 slots) r=16 | 6-mer r=1 | 3-mer (16 slots) r=16 | DNABERT (48 slots) r=16 |
|---|---|---|---|---|
| +0.17 | 0 % | 0 % | 0 % | -- |
| +0.35 | **16 %** | 0 % | 0 % | -- |
| +0.54 | 46 % | 6 % | 0 % | -- |
| +0.77 | 48 % | **40 %** | 0 % | -- |
| +0.93 | 74 % | 58 % | 0 % | -- |
| +1.00 | 88 % | 74 % | 0 % | -- |
| +1.76 | -- | -- | **0 %** | -- |
| +0.015 (released) | -- | -- | -- | **0 %** at LOO 1.00 |

The 3-mer cell reaches leave-one-out 1.00 by round 190 and stays at **0 %** through a held-out loss
of 3.400, which is 1.76 bits past its optimum and far worse than a uniform predictor. One point
reads 5 % and the rest read 0, so that is noise. **Sixteen slots is a wall even when the record is
stored perfectly and the model is destroyed.** Forty-eight slots likewise, on four released
checkpoints. Eight slots leak from +0.35 and saturate near 90 %.

**(d) What is left.** DNABERT-2 trained but has not been decoded: its BPE is non-overlapping so the
token-level decoder is the right one, but BPE tokens are variable length and `recon_audit`'s
boundary-constraint helper assumes a fixed k, so it needs a span-aware version first. That is the
one remaining piece of the released-model account, and it matters because DNABERT-2 is the second
tokeniser family and already reads 30 % under the standard protocol. The DNABERT chromosome-22 pair
is decoding now, to check the flatness result where the records are real rather than synthetic.

### 3.54 (14 Oct, 17:30) No decoder is right for every vocabulary, and that reframes the paper for the last time

The BPE decoder is written and run, the overlapping decoder has been run on real haplotypes, and
together they refute the framing I have been using all day. **Our search decoder is not universally
stronger than the published one.** It wins on fixed-width non-overlapping k-mers and loses on BPE
and on overlapping k-mers.

**(a) The decoder comparison, every released cell we have.**

| released model | vocabulary | utility cost | standard protocol | our decoder | which wins |
|---|---|---|---|---|---|
| NT 250M, E. coli, ep15 | non-overlapping 6-mer | +0.028 | 0 % | **10 %** | **ours** |
| NT 250M, E. coli, ep50 | non-overlapping 6-mer | +0.440 | 35 % | **70 %** | **ours** |
| NT 250M, chr22, ep50 | non-overlapping 6-mer | +0.256 | 25 % | **65 %** | **ours** |
| DNABERT-2, E. coli, ep30 | BPE | **+0.008** | **30 %** | 0 % | standard |
| DNABERT-2, E. coli, ep150 | BPE | +0.482 | **74 %** | 0 % | standard |
| DNABERT k=6, chr22, ep150 | overlapping 6-mer | +0.180 | **56 %** | 0 % | standard |
| DNABERT k=3, chr22, ep150 | overlapping 3-mer | +0.110 | 2 % | **10 %** | ours |

Why ours loses where it loses is mechanical, not mysterious. Our decoder starts from a random
nucleotide assignment and climbs. On BPE a random string **re-segments** into different tokens, so
the conditional it climbs is evaluated on a window whose segmentation is itself garbage, and there is
no local structure to follow. On overlapping k-mers the same thing happens through a different route:
a random target makes every one of the 48 covering positions mutually inconsistent. The published
prefix decode, by contrast, builds left to right from real context and never leaves the manifold of
plausible strings. **It is the better attack precisely where the vocabulary couples neighbouring
positions.**

**(b) So the methodological claim narrows, and becomes more useful.** Not "the standard protocol
under-reports masked models". Rather:

> No single decoder measures memorisation correctly across vocabularies. The published prefix decode
> is the right question for BPE and for overlapping k-mers. For fixed-width non-overlapping k-mers it
> under-reports by up to 35 points, and a re-masking decode matched to the training conditional is
> required. A paper that reports one decoder for all models has measured the decoder, not the models.

That is a claim about measurement practice with four released checkpoints behind it, and it survives
the fact that our decoder is sometimes the weaker one -- indeed that fact is the evidence for it.

**(c) And the privacy result is now much stronger than the methodological one.** Reading each model
with whichever decoder is better for it:

| released checkpoint | utility cost | verbatim recovery |
|---|---|---|
| DNABERT-2, E. coli | **+0.008** | **30 %** |
| NT 250M, E. coli | +0.028 | 10 % |
| DNABERT k=3, chr22 | +0.110 | 10 % |
| DNABERT k=6, chr22 | +0.180 | **56 %** |
| NT 250M, chr22 | +0.256 | 65 %, and **10 % at a single copy** |
| NT 250M, E. coli | +0.440 | 70 % |
| DNABERT-2, E. coli | +0.482 | **74 %** |

**Every released masked checkpoint we tested reproduces planted records verbatim at a utility cost a
practitioner would accept**, the cheapest at eight thousandths of a bit. Four checkpoints, three
vocabulary families, synthetic and real records. The claim that a masked objective prevents
reproduction is dead on released weights, comprehensively, and that is the paper's result.

**(d) Two details that belong in the write-up.** Single-copy *recognition* is universal: DNABERT-2
reaches rank-1 1.00 at r=1 by round 80 while verbatim stays 0 %, so membership inference would flag
these records everywhere that reproduction does not. And on chromosome 22 the overlapping k=3 cell
gives **10 %** where E. coli gave 0 %, so the 48-slot barrier is a near-wall rather than a wall: real
sequence is predictable enough to give the search something to climb. The slot law is about
difficulty, not impossibility, and real records are easier than synthetic ones everywhere we look.

**(e) Queued on the four free cards** (`queue_1014a`): the single-copy chromosome-22 number at 60
probes instead of 20, because 10 % currently means two hits and it is the number that carries the
privacy claim; NT 500M with weights kept, for a scale point on released weights; NT seeds 1 and 2,
because every NT number is seed 0; and DNABERT-2 trained on chromosome 22, where its records are
real haplotypes rather than synthetic DNA.

### 3.55 (14 Oct, 19:00) DNABERT-2 on real haplotypes: 20 % verbatim at +0.033 bits, and 94 % membership on single copies

The second released tokeniser family, now on chromosome 22 where the planted records are real
rare-variant haplotype segments rather than synthetic DNA. Standard protocol, 150 rounds:

| round | held-out loss | from best | r=16 recognition / verbatim | r=1 recognition / verbatim |
|---|---|---|---|---|
| 15 | **1.266** | best | 0.60 / 0 % | 0.00 / 0 % |
| 30 | 1.299 | **+0.033** | **1.00 / 20 %** | 0.00 / 0 % |
| 50 | 1.357 | +0.090 | 1.00 / 10 % | 0.00 / 0 % |
| 80 | 1.454 | +0.187 | 1.00 / 20 % | **0.20** / 0 % |
| 120 | 1.599 | +0.333 | 1.00 / 50 % | **0.80** / 0 % |
| 150 | 1.726 | +0.459 | 1.00 / 40 % | **0.94** / 0 % |

**(a) The verbatim line.** At 0.033 bits past its own best held-out loss -- a model anyone would ship
-- a released 117M checkpoint reproduces **20 % of real rare-variant haplotypes** that were planted
16 times, and 50 % by +0.333. This is the second vocabulary family to do it and the first on real
human records, so the privacy result is no longer an NT property.

**(b) The membership line, which is the stronger one.** Single-copy *recognition* climbs 0.00 -> 0.20
-> 0.80 -> **0.94** while verbatim reproduction stays at exactly 0 % throughout. So a released
checkpoint will tell an attacker, correctly 94 times in a hundred, **whether one specific rare
haplotype was in its fine-tuning set**, while never reproducing it. Reproduction and membership come
apart completely here, and the direction matters: the ruler the field reports (verbatim) says zero
where the ruler that matters for a person's privacy (was my sequence in there) says almost
certainly yes.

That is the cleanest statement of the paper's Sec. 7 argument we have, and it is now on released
weights with real haplotypes rather than on our backbone with synthetic canaries.

**(c) What it costs to avoid.** Its optimum is round 15 at 1.266, where recognition is 0.60 at r=16
and 0.00 at a single copy and verbatim is 0 %. So stopping at the optimum again removes the thing
an attacker would use -- and again the margin is small, 0.033 bits to reach 20 % verbatim and 1.00
recognition.

The search decoder is running on these weights now. On E. coli it recovered nothing from this family
(3.54), so the expectation is that the standard protocol stays the better attack here and these
numbers are the ones that go in the paper.

### 3.56 (15 Oct, 03:10) Overnight: the privacy numbers get their intervals, the seeds replicate, and 500M leaks LESS

**(a) The headline privacy number, at 50 probes instead of 20.** NT 250M, chromosome 22, round 50,
128 restarts, real rare-variant haplotypes:

| tier | n | standard protocol | **search decoder** | oracle | LOO top-1 |
|---|---|---|---|---|---|
| r=16 | 50 | 18 % | **52 %** | 66 % | 0.96 |
| **r=1 (one copy)** | 50 | 2 % | **8 %** | 10 % | 0.57 |
| r=0 control | 50 | 0 % | **0 %** | 0 % | 0.08 |

The 20-probe estimates (25 % -> 65 % and 5 % -> 10 %) were in the right place but optimistic. At 50
probes the single-copy number is **4 of 50**, i.e. 8 % with a Wilson interval of roughly 3-19 %, and
the 16-copy number is 52 % against the standard protocol's 18 %. **So the under-reporting factor on
a released checkpoint is about three, and a real rare-variant haplotype present once is recovered
verbatim in roughly one case in twelve.** Both numbers go in with their intervals.

**(b) Three seeds, and the result replicates with spread.** NT 250M, E. coli, at round 15, which is
0.028-0.031 bits past each run's own optimum:

| seed | its optimum | round-15 floor | standard | **ours** | oracle | LOO |
|---|---|---|---|---|---|---|
| 0 | 1.823 | 1.851 | 0 % | **10 %** | 15 % | 0.70 |
| 1 | 1.824 | 1.855 | 5 % | **15 %** | 20 % | 0.71 |
| 2 | -- | -- | 0 % | **25 %** | 30 % | 0.77 |

Mean 17 % against the standard protocol's 2 %. The leave-one-out column is nearly constant across
seeds (0.70, 0.71, 0.77) while the recovered fraction varies 10-25 %, which is the signature of a
search-limited quantity and matches what the controlled backbone showed. At round 50 the two
measured seeds give 35 % -> 70 % and 25 % -> 80 %.

**(c) The 500M checkpoint leaks LESS under the matched decoder, not more.** NT 500M, E. coli:

| | held-out loss | from its optimum | standard | ours | LOO |
|---|---|---|---|---|---|
| round 3 (its optimum) | 1.798 | -- | 0 % | **0 %** | 0.01 |
| round 15 | 1.828 | +0.030 | 0 % | **0 %** | 0.48 |
| round 50 (standard protocol only so far) | 2.253 | +0.455 | **36 %** | running | -- |

At the same round and a comparable utility cost the 500M model has stored less (leave-one-out 0.48
against the 250M's 0.70) and the search decoder recovers nothing where it recovered 10-25 % at 250M.
That is the same direction our own backbone showed -- a larger masked model is less overfit after the
same number of passes -- and it cuts against the simple reading that scale makes leakage worse. Under
the STANDARD protocol at round 50 the 500M is the leakier of the two (36 % against 28 %), so the two
protocols disagree about the scale trend and the paper has to report both.

**(d) The membership result replicates in all three seeds, and its control is clean.** DNABERT-2 on
chromosome 22, single-copy real haplotypes, standard protocol at round 120:

| seed | held-out loss | single-copy recognition | single-copy verbatim | 16-copy verbatim |
|---|---|---|---|---|
| 0 | 1.599 | **0.80** | **0.00** | 0.50 |
| 1 | 1.593 | **0.70** | **0.00** | 0.40 |
| 2 | 1.607 | **0.80** | **0.00** | 0.30 |
| non-member control, all seeds | | **0.000** | 0.00 | -- |

Single-copy verbatim is 0.00 at **every** checkpoint in **every** seed, while recognition of the same
single-copy records reaches 0.70-0.80 and the never-trained control sits at 0.000 against a chance
level of 0.01. **A released checkpoint identifies which specific rare haplotype was in its
fine-tuning corpus, seven or eight times in ten, without ever reproducing it.** The dissociation is
not a one-seed artefact.

One caveat to close before this is written up: the non-member tier carries only 10 scored probes per
seed, so 0/10 is a clean separation from 0.70 but a weak bound on the false-positive rate itself.
More non-members is cheap and should be run.

**(e) Still running** (`queue_1014a`, `queue_finish`): NT 500M at round 50 under the search decoder,
NT seed 2 at round 50, DNABERT k=4 and k=5 on chromosome 22 to complete the flatness table on real
records, and the 3-mer utility curve at 50 probes, which was only ever done for the 6-mer.

### 3.57 (16 Oct, 09:00) The 16 Oct deck, rebuilt through the ppt-agent pipeline

Built the group-meeting section (slides 42-52 of the cumulative deck) with the `ppt-agent` skill
rather than by hand with python-pptx. The pipeline is HTML design drafts -> dom-to-svg -> native
PowerPoint shapes, so the slides stay editable in PowerPoint rather than arriving as pictures.

**Section**: a divider page plus ten content pages -- what changed since 9 Oct, the released-model
rule and its audit table, the test surface, the five findings, the mechanism with its negative
control, and where the paper stands. Eleven pages, each with the usual Chinese one-line summary and
the English speaking script in the notes.

**Three pipeline faults worth recording, because they will recur on the next deck.**

*(a) No mixed styling inside a line.* dom-to-svg emits one tspan per style run within a line, and
`svg2pptx` turns each tspan into its own non-wrapping textbox at a recomputed x. A bold phrase in
the middle of a sentence therefore lands the rest of the sentence on top of the phrase. Every
emphasis is now a whole line -- a bold lead-in above its paragraph -- which also reads better.

*(b) `<polyline>` is silently dropped.* `svg2pptx` has handlers for rect, text, circle, ellipse,
line, path and image, and none for polyline; the chart's two series vanished while the stats still
reported 0 skipped and 0 errors. Drawn as consecutive `<line>` segments they render correctly.

*(c) PowerPoint renders ~10.3 % wider than headless Chrome measures.* Measured, not estimated: a
line Chrome gives `textLength="538.109375"` comes out 593.6 px in the exported slide. Headless
Chrome does not get the real Calibri and falls back to narrower metrics, while PowerPoint
substitutes the deck's declared fonts (Source Serif 4, IBM Plex Sans -- neither installed on this
machine) with genuine Calibri. Since the line breaks are baked in by Chrome and each line is a
non-wrapping textbox, a line that merely fits in Chrome spills out of its card in PowerPoint. Text
is now laid out at 90 % of the available width, which absorbs it; verified by measuring glyph
extents in the exported PNG (text ends at 675-677 px against a card inner edge of 680).

**One content change made for honesty rather than for layout.** The Finding 5 chart first plotted
the downstream task score on an expanded 0.665-0.695 band, which made a series that moves by fifteen
thousandths look like a mountain -- the opposite of what the slide claims, and the exact chart crime
the section argues against. Both series now share one 0-1 axis: the task score is visibly flat while
single-copy identification climbs from 0 to 0.94.

Artefacts under `ppt-output/`: `style.json` (a `mocha_editorial` derivative retuned to this deck's
own measured tokens), `planning.json` (11 pages, passes `planning_validator.py` with 0 errors and 0
warnings), `slides/*.html`, `svg/*.svg`, `preview.html`. The deck itself is
`GLM Memorization - Spinoff Proposal (Group Meeting 1016).pptx`, 52 slides, built on the 41-slide
9 Oct deck. Automated `visual_qa.py` leaves two blank-space flags: the section divider, where the
whitespace is the design, and slide 45, which the 90 % text column pushes just over a 40 % heuristic.

Nothing here touches an experiment. `queue_util` and `queue_tighten` are still running and can only
tighten intervals.

### 3.58 (19-20 Oct) The decoder gets 41x faster, one claim is retired, and the tokenizer curve becomes a curve

Nothing between 16 and 20 Oct was written down, so this entry covers all of it. Four things
happened: a bug that had silenced every Nucleotide Transformer utility cell was fixed, a claim
already printed on slide 50 of two decks turned out to rest on a smoke-test probe and does not
survive the full one, the ICM decoder was rewritten and verified bit for bit, and the tokenizer
axis was finally measured at five cut sizes instead of three.

**(a) The NT branch of the downstream probe (`01d9ce5`).** `utility_at_leak` dispatches
Nucleotide Transformer runs as kind `"nt"`, but `_Backbone.forward` only knew `kmer` / `bpe` /
`hyena` and ended in `raise ValueError(self.kind)`. Every NT utility cell had been dying there
before producing a number, which is why the chr22 utility curve had three DNABERT-2 seeds and no
NT at all. The branch feeds `<cls>` followed by non-overlapping 6-mers, matching how `nt.py`
builds its training batches and how the scorers call the model, and trims the row to a whole
number of 6-mers because the vocabulary has no partial-k-mer token.

NT 250M on chr22, linear probe on frozen features, `n_train=20000`, GUE `prom_300_all`:

| checkpoint | held-out bits | r=16 verbatim | r=16 recognition | r=1 recognition | MCC |
|---|---|---|---|---|---|
| ckpt_ep15 (best saved) | 1.411 | 0.06 | 0.33 | 0.04 | **0.802** |
| ckpt_ep30 | 1.501 | 0.12 | 0.56 | 0.17 | 0.798 |
| ckpt_ep50 | 1.632 | 0.18 | 0.73 | 0.35 | 0.780 |
| final | 1.632 | 0.18 | 0.73 | 0.35 | 0.780 |

**(b) A claim retired.** The slide-50 statement -- "the task score's maximum is a checkpoint that
already leaks 20 %" -- came from `smoke_util.json`, the `n_train=2000` smoke probe, which put MCC
at 0.678-0.692 with its maximum at round 80. The full probe (`n_train=20000`, three seeds) puts
MCC at 0.787-0.802 and it **declines monotonically**; its maximum is round 15 for seeds 0 and 1
and round 50 for seed 2, and single-copy identification is 0.00 at all three of those points. So
on DNABERT-2 the metric does **not** point at a leaking checkpoint over a clean one.

What survives, and is still worth a slide: across the whole range the task score moves 1.1-1.5 %
while single-copy identification goes from 0 to 0.92-0.96. The metric carries essentially no
signal. The stronger form of the claim is available on NT instead, from table (a): there the
metric's own maximum, round 15, already reproduces 6 % of records and identifies 4 % of single
copies, because on real haplotypes NT has no clean checkpoint for the metric to point at.

**Slides 1016 and 1019 still carry the retired wording on slide 50 and have not been rebuilt.**

**(c) The ICM decoder, 141 s -> 3.4 s per probe (`d1a47b5`).** A cell was taking four hours at 31 %
GPU utilisation and 90 W of 450 W, which is what a 235M model looks like when it is called about
600,000 times at batch 1: 128 restarts x up to 6 sweeps x 8 target tokens per probe, each its own
forward, with roughly four host syncs per position-step -- argmax to int, two `.item()`
comparisons, and a 4096-wide `nonzero` to find the current token's row in the content table --
which is about two million syncs per cell. The restarts are independent and follow the same
schedule, so they now run as one batch; `changed` accumulates as a tensor and syncs once per
sweep; an index table replaces the `nonzero`; and a sweep that changes nothing leaves the state
its logits were computed from, so the pseudo-likelihood reuses them instead of recomputing eight
forwards per restart. Factor of 41.

Verified rather than asserted. Against the pre-batching code run on the same machine the same
day, `--chunk 1` reproduces every cell bit for bit -- the 128-restart Hamming vector, the chosen
prediction, the sweep counts, the leave-one-out numbers and the pseudo-likelihood score, 8 of 8
whole cells. That last column needed a fix: the old code summed the per-position terms as Python
floats and the new one summed them in float32, which moved the total by 1e-7 relative, enough to
reorder two restarts whose pseudo-likelihoods are nearly tied. The accumulator is float64 now.

`--chunk > 1` is a different arithmetic, not a different algorithm. bf16 picks kernels by batch
shape and ICM amplifies a last-bit logit difference into a different trajectory: across 16 cells
not one restart vector survived batching, yet 15 of 16 agreed on whether the attack succeeded and
the reported extraction rate was identical (8.0 % either way). The any-restart oracle moved from
18 % to 22 %. `--chunk 1` is kept as the setting that reproduces the old arithmetic exactly.

**(d) The machine's arithmetic changed across the reboot, and this is a methodological finding.**
`target_surprise` is code we did not touch and it runs at batch 1 in every case. It is bitwise
identical between two runs made today and 0 of 16 identical with the run made on 16 Oct. So the
16 Oct numbers are not reproducible on this machine regardless of any change of ours, and a
reported extraction percentage carries a run-to-run uncertainty of a few points that comes from
numerical sensitivity rather than from the probe count. **The binomial interval on the number of
probes understates the real uncertainty**, and the any-restart oracle -- a maximum over 128
stochastic restarts -- is the quantity most exposed to it. Either report that caveat or demote
the oracle to the appendix.

**(e) Seven cells re-run on one basis.** Because of (d), every n=50 cell was re-run with one code
path and one setting (`--tiers 16,1 --max_probes 50 --restarts 128 --chunk 64`). The 16 Oct
versions are archived unmodified in `outputs/pre_reboot_basis_1016/` (5 cells, 10 files). All
seven finished between 13:02 and 13:19 -- seventeen minutes for what the old decoder would have
spent about 28 GPU-hours on.

E. coli, 16 planted copies, 50 probes, `prefix` = the field's standard test, `icm` = ours:

| cell | target b/nt | standard | ours | oracle | LOO top-1 |
|---|---|---|---|---|---|
| 250M s0, ep15 (+0.03) | 0.971 | 4.0 % | **8.0 %** | 14 % | 0.72 |
| 250M s1, ep15 | 0.892 | 8.0 % | **8.0 %** | 22 % | 0.73 |
| 250M s2, ep15 | 0.888 | 4.0 % | **14.0 %** | 26 % | 0.75 |
| 250M s0, ep50 | 0.298 | 26.0 % | **66.0 %** | 84 % | 0.98 |
| 250M s1, ep50 | 0.275 | 26.0 % | **68.0 %** | 82 % | 0.97 |
| 250M s2, ep50 | 0.280 | 30.0 % | **76.0 %** | 88 % | 0.99 |
| 500M s0, ep50 | 0.307 | 36.0 % | **78.0 %** | 90 % | 0.99 |

Non-member controls read 0.0 % in every cell; the single-copy tier on E. coli reads 0 % throughout.

**This corrects the Finding-1 table in the 16 Oct deck.** The near-optimum row was written as
"standard 0 % vs ours 10-25 %". On one basis at n=50 it is **standard 4-8 % vs ours 8-14 %** --
the standard test under-reports by about a factor of two there, not infinitely. The far-past-optimum
row holds and is stronger than before: 26-30 % against 66-76 % across three seeds, and 36 % against
78 % on the 500M.

**(f) The tokenizer curve, read at matched held-out loss.** `core100` was re-run with five cut
sizes (`char 2mer 3mer 4mer 6mer`, AR, three seeds, uniform DNA) as `outputs/kcurve`, and
reproduces the original char/3mer/6mer cells exactly. Read at the final epoch it says nothing:
every k >= 3 saturates at 100 % extraction, including records planted once, so the table reads
0/0/1/1/1 and separates nothing. Read at matched held-out loss, which is what 3.11 did, it is a
curve. `pilot2/kcurve_report.py` produces it.

| tokenizer | slots for 48 nt | @2.05 | @2.10 | @2.20 | @2.40 | loss at 100 % |
|---|---|---|---|---|---|---|
| char | 48 | - | - | - | - | never |
| 2-mer | 24 | 0 % | 0 % | 0 % | 0 % | never |
| 3-mer | 16 | 0 % | 0 % | 0 % | 3 % | 4.15 |
| 4-mer | 12 | 0 % | 0 % | 2 % | 11 % | 3.01 |
| 6-mer | 8 | 1 % | **18 %** | **65 %** | **91 %** | **2.47** |

Controls 0.00 for every tokenizer at every snapshot. `char` has no entries because its held-out
loss never leaves 2.00-2.04 in thirty epochs -- it does not overfit far enough to reach the
comparison points, and extracts 0 % throughout.

Two readings. The ordering is monotone in the number of token slots the hidden 48 nucleotides
occupy, with no exception, and the right x axis is therefore the slot count rather than k -- which
is also why the released DNABERT family, whose tokens overlap so the slot count barely moves with
k, shows no trend. And the second column of the claim is cost: reaching full extraction costs 2.47
bits at 6-mer, 3.01 at 4-mer, 4.15 at 3-mer, and never happens at 2-mer or char. **Coarser
tokenisation does not only leak more, it leaks more cheaply**, which puts this result in the same
currency as the released-model numbers.

**(g) The window is configurable now (`83c7bee`).** `KmerTokenizer` asserts `window_nt % k == 0`
and 288 is not divisible by 5, so a 5-mer run could not be built at all. `WINDOW` now comes from
`PILOT2_WINDOW`, default 288 so every existing result and every unchanged command behaves as
before; 300 divides every k from 1 to 6. It is an environment variable rather than a flag because
several modules do `from .data import WINDOW`, which binds at import time -- setting it afterwards
would leave each module with a different window, which produces wrong numbers rather than errors.

The same commit fixes three analysis entry points -- `recon_audit`, `infill_audit`,
`natural_dups` -- that rebuilt a run's tokenizer with a literal 288. Left alone they would have
analysed a 300-nt run as if it were 288: wrong slot count, every probe offset resolving somewhere
else, and no error raised. They read the run's own `data_meta.json` through `data.window_of()` now,
falling back to 288, which is the window older runs were in fact built at.

**(h) Running, state unknown.** `kcurve300` was launched at 18:03 on 20 Oct: six tokenizers
(k = 1..6) x three seeds at window 300, with the matched-floor analysis chained after it so the
result lands in `outputs/kcurve300/MATCHED_FLOOR.txt` without supervision. `STATUS.txt` had
reached `START` when contact was lost. The server has been refusing connections on port 6004 since
some time on 21 Oct -- the second outage in four days, host pingable, so sshd or the port forward
rather than the machine. Whether the sweep finished before the outage is not known. It adds k=2
and k=5 to the curve above; it does not change any conclusion.

**(i) Also resolved.** The HyenaDNA parameter count: the checkpoint `config/hyenadna_config.yaml`
names has **14,236,768 parameters**, counted from its own state_dict, which agrees with the BCB
paper's Table 1. The 6.55M recorded earlier in 3.6 was our miscount, and 3.6 now says so. Worth
keeping in mind for the paper: HyenaDNA at 14.24M and our controlled backbone at 12.9M are the
same size, so the 1-mer counterexample cannot be waved away as a scale effect.

### 3.59 (21-23 Oct) Every chromosome-22 cell re-measured on one basis, the tokenizer sweep completed, and the paper written

**(a) `kcurve300` did finish, which closes 3.58(h).** All eighteen runs (k = 1..6, three seeds,
window 300) completed before the outage and the matched-floor analysis ran with them. The curve now
has every cut size:

| tokenizer | slots for 48 nt | @2.05 | @2.10 | @2.20 | @2.40 | loss at 100 % |
|---|---|---|---|---|---|---|
| char | 48 | - | - | - | - | never |
| 2-mer | 24 | 0 % | 0 % | 0 % | 0 % | never |
| 3-mer | 16 | 0 % | 0 % | 0 % | 2 % | 4.07 |
| 4-mer | 12 | 0 % | 0 % | 2 % | 12 % | 2.99 |
| 5-mer | 9.6 | 0 % | 2 % | 24 % | 61 % | 2.63 |
| 6-mer | 8 | 1 % | 17 % | 67 % | **92 %** | **2.47** |

Monotone in the slot count with no exception across six cut sizes, and monotone in what full
extraction costs. The window-288 sweep of 3.58(f) agrees where the two share a tokenizer: 2 % against
3 %, 12 % against 11 %, 92 % against 91 % at matched loss 2.40, and 4.07/2.99/2.47 against
4.15/3.01/2.47 for the cost of saturation. Two sets of runs at different geometries, one curve.

**(b) The nineteen chromosome-22 cells were re-run on one numerical basis (23 Oct, 20:51-23:34).**
`outputs/chr22_rerun/STATUS.txt` records `rc=0` on all nineteen and `ALL_FINISHED`. Every cell is 50
probes per tier, every cell on the same host after the reboot, so nothing in the table below is
comparing a pre-reboot number with a post-reboot one. The reports are now published as
`results/*/*/rb_*.{md,json}`, which they were not before: the newest reports in `results/` dated from
14-15 Oct, had 20 probes and 32 restarts, and disagree with these (the overlapping family read
10/0/10/0 % there against 2/0/4/0 % here). The 14-15 Oct cells are superseded, not averaged in.

| checkpoint | held-out bits/nt | 16 copies, standard | 16 copies, ours | 1 copy, standard | 1 copy, ours |
|---|---|---|---|---|---|
| NT 250M round 15 | 1.145 | 6 % | 6 % | 0 % | 0 % |
| NT 250M round 30 | 0.739 | 10 % | 28 % | 0 % | 0 % |
| NT 250M round 50 | 0.465 | 18 % | **52 %** | 2 % | **8 %** |
| NT 500M round 15 | 1.045 | 16 % | 14 % | 0 % | 0 % |
| NT 500M round 50 | 0.396 | 24 % | **58 %** | 0 % | **12 %** |
| never-trained control | - | 0 % | 0 % | 0 % | 0 % |

The first launch of this batch died instantly in nineteen cells on `data/human/chr22.fa`:
`GLMEXT_DATA` lives in `.bashrc`, which a non-interactive SSH does not read. That is the third time
the same `.bashrc` guard has cost a batch (conda, the proxy, now the data root), and the fix is the
same each time -- export it inside the script. Before relaunching I also checked that all four runs
name `canary_npz=/data/wh/yqdata/glm_data/human/canaries_chr22.npz`; without it they would have
fallen back to iid canaries silently and the whole human arm would have measured nothing.

**(c) Where our decoder reads zero, the leave-one-out probe says the record is there.** Asked for one
nucleotide of a planted record with the other 47 supplied, DNABERT-2 answers correctly 0.94/0.93/0.95
across three seeds for records planted **once**, which bounds whole-record recovery at 0.27/0.21/0.39.
Our BPE search returns 0 % from all three. The standard prefix-conditioned protocol, which is matched
to that vocabulary, returns 30 %. The released overlapping family behaves the same way and more
strongly: per-position accuracy 0.99-1.00 at 16 copies, implied ceiling 0.70-0.87, and our
nucleotide-level decoder recovers 2 %, 0 %, 4 %, 0 % for k = 3,4,5,6. Both zeros are limits of the
attack, not properties of the model, and the paper has to say so in both places -- it is the same
inference the field currently makes in the opposite direction.

**(d) `pilot2/rescore.py` (`29d6d12`) separates the measurement from the machine.** Scoring a saved
checkpoint again from its own `args.json` was not possible before, so every recognition number dated
from the day its run finished -- a problem once the host's floating-point behaviour changed across the
18 Oct reboot. Re-scoring a checkpoint whose old scores still exist answers the question the paper
has to answer anyway: identification reproduces **to the digit** (rank-1 0.800 before and after,
held-out loss identical to four decimals), while extraction on the same checkpoint moves by **six
points**, which is the same order as the binomial standard error on 50 probes. So: identification
quoted without an interval, extraction quoted with one.

**(e) Code, measurements and logs are public.** `pilot2/export_figure_data.py` flattens 3,844 score
files (725 MB) into `results/figure_data.csv` -- 27,106 rows, 2.3 MB, keyed on (group, run) because
`3mer_ar_s0` exists in both `kcurve` and `kcurve300`. That file, 201 MB of score output and these
notes are on `origin/glmex`. It was checked rather than assumed: the matched-loss cells recomputed
from the CSV reproduce the table in (a) cell for cell, including the window-288 column.

**(f) The paper is written end to end.** Eight sections, about 5,800 words, privacy first, in
`paper/sections/p0*.tex`, with Overleaf connected over its git bridge (`git.overleaf.com`, branch
`main`) rather than GitHub Sync, because the LaTeX is a subdirectory of a large repository. Three
things worth recording from the writing:

- The citations never compiled. `main.tex` loaded no `natbib`, so every `\citep` was an undefined
  control sequence, the key was printed into the running text and the bibliography came out empty:
  28 errors, all of them this. With `natbib` and `plainnat` the log is clean -- 0 errors, 0 warnings.
- Drawing the figures caught two wrong numbers and one broken cross-reference. The round-120 MCC
  range was quoted as 0.788-0.792 when seed 1 reads 0.7845; the downstream decline was called
  monotone when seed 2 rises at round 50 before falling again; and the paragraph on DNABERT's flat
  row cited `\S\ref{sec:slots}`, which is its own section, so the printed paper pointed the reader
  at the page they were on. Plotting a claim is a cheaper audit than re-reading it.
- Three figures are drawn, not five: `F5_slots`, `F6_ident`, `F7_blind`, by
  `pilot2/figures_privacy.py` from `figure_data.csv`. The planned probe-geometry figure was dropped
  because the text carries it, and the released-cost figure because Table 1 already does.

The compiled PDF is 12 pages: the extra title page the call allows, ten content pages, and the
references, which the call excludes. It fits, with three figures and five tables in it.

### 3.60 (23 Oct) The title was wrong for the venue, and the related work was missing this field's own literature

**(a) Three years of RECOMB titles, read rather than assumed.** The accepted lists for 2024 (57
papers), 2025 (55) and 2026 (65) contain **no paper with a manifesto subtitle**, so
``Reproduction Is the Wrong Alarm, and Tokenisation Explains Why'' had to go. The venue's own
privacy papers are named for the artefact that leaks: *Private Information Leakage from Polygenic
Risk Scores* (RECOMB 2026, Nikitin and Gursoy, Genome Research special issue), *TX-Phase: Secure
Phasing of Private Genomes in a Trusted Execution Environment* (2025), *Privacy Preserving
Epigenetic PaceMaker* and *Secure Discovery of Genetic Relatives* (2024). Declarative findings are
accepted too (*Synthetic control removes spurious discoveries from double dipping...*, 2025), so the
register is sober, not dull. New title, chosen by the user from four candidates:

> **Identification without Reproduction: Privacy Leakage from Fine-Tuned Genomic Language Models**

It states the paper's own claim, it reads in the venue's syntax, and it separates us from the
predecessor, which quantifies how much is memorised where we argue the usual ruler points the wrong
way. The slot mechanism is deliberately not in the title: it is the explanation, and putting it
there moves the reader's attention off the people being identified.

**(b) Attack papers do belong here.** Worth recording because it was an open worry: RECOMB has
published attacks on released genomic artefacts before. *Reconstructing Genotypes in Private Genomic
Databases from Genetic Risk Scores* (RECOMB 2020, extended abstract pp. 266-268; full version in
J. Comput. Biol. 28(5):435-451) and the 2026 polygenic-score paper above are both leakage results,
not protective methods. Our threat model is in scope.

**(c) Nine references added, all checked on 23 Oct.** The related-work section cited two CCS papers
on privacy definitions and nothing a RECOMB reader would recognise as genomic privacy. Added: Homer
et al. 2008 (allele-frequency membership), Shringarpure and Bustamante 2015 and von Thenen et al.
2019 (beacons), Paige et al. 2021 and Nikitin and Gursoy 2026 (polygenic scores), Erlich and
Narayanan 2014 (the survey for ``identification is the harm''), Oprisanu et al. 2022 (NDSS) and
Belfiore et al. 2025 (membership inference against generative models of genomes --- the nearest
neighbours by subject, though both audit model *output* rather than released weights), and Che et
al. 2026, **the one that matters most**: it proves the general form of our section 5 result, that
counterfactual memorisation and adaptive extraction do not bound one another in either direction,
with a construction that is fully extractable while loss-based audits certify it clean. Our result
is the measured instance of their theorem on released genomic weights, with a mechanism attached;
the paper now says so rather than letting a reviewer discover it.

The predecessor's entry is also fixed: accepted at ACM BCB 2026, DOI 10.1145/3807503.3819470, which
its own VERIFY note had been waiting for.

**(d) The audit notes are no longer printed (done 24 Oct).** `plainnat` renders `note`, so the
references carried lines like ``checked 10 Oct 2026 against the PDF'' and ``VERIFY volume/pages''.
`paper/strip_notes.py` now writes `refs_submit.bib` --- `refs.bib` with the `note` fields removed and
every other field copied byte for byte, so the submitted bibliography cannot drift from the audited
one --- and `main.tex` cites that. It cost a page: 13 pages became 12, references now 10-11.

The script also prints which entries still say VERIFY, because stripping them should not hide an
unfinished check from us. It listed five; three were resolved the same day against Europe PMC,
Crossref and arXiv:

- `vonthenen2019reidentification` is Bioinformatics **35(3):365--371**, 2019, and the DOI we had
  guessed is right (Europe PMC, PMID 30052749). Volume, number and pages were simply missing.
- `dalla2024nucleotide` is Nature Methods **22(2):287--297**, 2025 (PMID 39609566); only the issue
  number was missing.
- The predecessor is published, not merely accepted: **BCB '26, Rende, Italy, pp. 1--10**, ACM
  (Crossref record for 10.1145/3807503.3819470).
- `nikitin2026prs` is advance online publication, 17 Aug 2026, with **no volume or issue assigned**,
  so it cites as Genome Research 2026 with its DOI and no pages field --- the article id
  `gr.282202.126` would otherwise print as a page number.
- `belfiore2025bihmia`: the arXiv listing claims **no venue and no journal reference**. The AAAI
  2026 attribution came from a third-party lecture page whose date is inconsistent, so we cite the
  preprint. dblp sits behind a bot check and was not worked around.

Two VERIFY notes remain, both waiting on a publisher rather than on us.

## 4. Open items

- HyenaDNA (pretrained 1-mer, causal) as the second real-model anchor — not started; needs its HF code to load under transformers 4.29.
- Utility metric next to memorization (Erman) — needs real data; plan: held-out loss on E. coli + a small downstream probe.
- Explanation for "smaller tokens overfit less at equal memorization" (Erman) — hypothesis: context collision; test pending.
- Figures + one-paragraph explanations for Alex's proposal update (mid-October).
