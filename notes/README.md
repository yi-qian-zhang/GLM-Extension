# Working notes

The research log for the genomic-language-model memorisation study in `pilot2/`. These are
working notes, not a paper: they are written as the experiments run, they record what was
measured before anyone knew which way it would come out, and several entries exist only to
correct an earlier one. That is deliberate. Where a claim in the paper differs from a claim
here, the paper is the considered version and these files are the audit trail that shows how
it got there.

Everything in `pilot2/` is on the `glmex` branch, which is where this work lives. `main`
mirrors the upstream BCB implementation (`src/`, `experiments/`, `config/`) and is kept
unchanged for comparison.

## Reading order

| File | What it is |
|---|---|
| `21_privacy_first_plan.md` | Current plan: the privacy-first restructure, the ten-page budget, and the claim-to-evidence map. **Start here.** |
| `18_paper_outline.md` | Section skeleton and the venue requirements that constrain it |
| `20_research_chain_EN.md`, `20b_` | How the idea changed, stage by stage, with the belief revisions that drove each turn |
| `17_experiment_log_week3_EN.md`, `17b_` | The main experiment log. Longest file here; §3.x entries are chronological |
| `09_`, `08_` (+ `b` variants) | Earlier weeks |
| `04_experiment_plan.md`, `04b_` | The running plan and status board |
| `figures/` | Generated reports and plots referenced from the logs |

Files ending in `b` are the Chinese counterpart of the preceding English file, kept in step.

## What is not here

- Meeting records in which collaborators are quoted. Those stay private; the technical content
  they produced appears in the logs on its own terms.
- Model checkpoints and the raw score files. The logs quote the numbers; the artefacts
  themselves are too large for git.

## A caution about numbers

Two things in these logs make a quoted percentage less exact than it looks, and both are
recorded in `17_experiment_log_week3_EN.md` §3.58:

1. The extraction decoder is chaotic in the model's last-bit arithmetic. Restart trajectories
   do not reproduce across batch shapes, so a reported rate carries a few points of run-to-run
   uncertainty that the binomial interval on the probe count does not capture.
2. The machine's own floating-point behaviour changed across a reboot on 18 October. Numbers
   measured before and after are not bitwise comparable, which is why every cell that backs a
   paper claim was re-run on a single basis on 19 October.

Where a log entry predates that re-run and the re-run disagrees, the re-run wins.
