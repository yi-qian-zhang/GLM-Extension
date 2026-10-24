# Paper: "What Makes a Genomic Language Model Memorise?"

Target: **RECOMB 2027**. Fallback: **ISMB/ECCB 2027** (deadline 7 Jan 2027, has a privacy track).

## Hard requirements from the 2027 call (read 9 Oct 2026)

| Item | Requirement |
|---|---|
| Abstract | **28 Oct 2026**, 23:59 AoE. Title, authors and abstract must closely match the final paper. |
| Full paper | **4 Nov 2026**, 23:59 AoE |
| Notification | 22 Dec 2026; conference 17-20 May 2027, satellites 15-16 May |
| Length | **10 pages max, Letter, including all figures, tables and captions.** Bibliography excluded. One extra title page allowed. |
| Format | min 10pt font, 1-inch margins, PDF. No required template (LNCS optional). |
| Review | **Single-blind** - do not anonymise. |
| Appendix | Optional, **separate PDF**, no page limit. Reviewers may skip it. |
| Code | A paper with new software/analysis **must link a public documented repository in the paper**. |
| Submission | EasyChair: https://easychair.org/conferences/?conf=recomb2027 |
| Preprints | Allowed without restriction. Accepted papers must go to bioRxiv/arXiv by the final-version deadline. |
| Author cap | At most 4 submissions per author, else desk reject. |
| Journal | Accepted papers not published elsewhere are offered a Journal of Computational Biology special issue. 2027 partners still being finalised. |

## Blocking actions (not writing)

1. **Public code repository.** Required *in the paper*. Our work lives on the private branch
   `glmex` of the collaboration repo; `pilot2/` is ours and `src/`, `experiments/`, `config/` are
   Alex's. Decide with Alex and Erman what becomes public, then publish a repository with a README
   that reproduces every table. This gates the 4 Nov deadline, not the 28 Oct abstract.
2. **Author list and order**, needed for the 28 Oct abstract registration, which must then match.
3. **Overleaf project** with Erman as owner plus the four collaborators he will name.

## Build

```
pdflatex main && bibtex main && pdflatex main && pdflatex main
pdflatex appendix
```

## Layout

- `main.tex` - preamble, title page, section includes. The page budget is in its header comment.
- `sections/` - one file per section; all prose lives here so the venue can be switched by
  replacing the preamble only.
- `appendix.tex` - the separate appendix PDF.
- `refs.bib` - entries marked `VERIFY` need their venue checked before submission.
- `figures/` - PDF/PNG figures. Sources: `GLM-Extension/pilot2/figures_proposal.py`,
  `token_info.py --plot`, `analyze_*.py` reports in `claude_notes/figures/`.

## Where each number comes from

Every claim maps to a section of the experiment log `claude_notes/17_experiment_log_week3_EN.md`
(Chinese: `17b`). See `claude_notes/18_paper_outline.md` for the claim-to-evidence table.
