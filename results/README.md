# Results

The measured output behind the paper and the logs in `notes/`. Directory names match the
`outputs/<sweep>/<run>/` paths quoted throughout the logs, so a claim in `notes/` can be
traced to the file it came from.

## What is here

| | |
|---|---|
| `figure_data.csv` | **Every figure in the paper can be redrawn from this one file.** 27,106 rows, one per (run, snapshot, tier, host) |
| `<sweep>/<run>/recon_*.json` | Extraction results per cell: the 128-restart Hamming vector, the chosen prediction, leave-one-out numbers |
| `<sweep>/<run>/args.json` | The exact configuration each run was launched with |
| `<sweep>/<run>/utility_at_leak.json` | Downstream task score beside the memorisation numbers, per checkpoint |
| `*.md` | The generated reports the logs quote |

Regenerate the table with `python -m pilot2.export_figure_data --root outputs --out results/figure_data.csv`.

### figure_data.csv columns

`group` is the sweep directory and `run` the run inside it; both are needed, because the same
run name exists under more than one sweep (`3mer_ar_s0` is in both `kcurve` and `kcurve300`,
at windows 288 and 300). `heldout_bits_per_nt` is the held-out loss at that snapshot, which is
the axis every tokenizer comparison is read on — never the epoch number, because the
tokenizers converge at very different rates. `tier` is how many times the record was planted;
`tier=0` with `host=fresh` is the never-trained control and reads zero throughout.
`exact_rate` is the fraction of planted records returned letter for letter.

## What is not here, and why

Three kinds of file were left out. They are reproducible from the code and the checkpoints,
and together they are about 750 MB, which does not belong in a git repository:

- `scores_ep*.json` and `scores_final.json` (725 MB) — per-probe detail at every snapshot.
  Everything the figures read out of them is in `figure_data.csv`.
- `data_meta.json` (28 MB) — the planted probe sequences and their offsets. For the human
  arms these are rare-variant haplotypes from 1000 Genomes phase 3, which is public consented
  data; they are omitted for size, not for sensitivity.
- Model checkpoints (60 GB) — see the paper for where these are published.

Ask if you need any of them; they exist.

## A caution about the numbers

Two facts recorded in `notes/17_experiment_log_week3_EN.md` §3.58 make a quoted percentage
less exact than it looks, and they apply to this directory too:

1. The extraction decoder is chaotic in the model's last-bit arithmetic. Restart trajectories
   do not reproduce across batch shapes, so a rate carries a few points of run-to-run
   uncertainty beyond the binomial interval on the probe count. The any-restart oracle, a
   maximum over 128 stochastic restarts, is the most exposed.
2. The machine's floating-point behaviour changed across a reboot on 18 October 2026. Cells
   measured before and after are not bitwise comparable. Every cell backing a paper claim was
   re-run on a single basis on 19 October; `pre_reboot_basis_1016/` keeps the superseded
   versions unmodified so the two can be compared.

Where an older file and the 19 October re-run disagree, the re-run is the one the paper uses.
