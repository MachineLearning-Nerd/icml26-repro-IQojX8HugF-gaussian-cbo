# Evaluator-blind red-team review

## Pass 1 — candidate only

Starting only from `pages/index.md`, the reviewer opened:
`current-summary`, `current-claim-1` through `current-claim-6`, then
`visibility-matrix`. It did not use OpenResearch logs or unpublished paths.

Initial misses:

- C3/C4 source numbering was ambiguous because ar5iv and the official PDF
  disagree.
- C2’s old one-step page remained easier to find than the current dynamics.
- C5’s raw arrays were not linked from the current page.

Fixes: current pages were moved to the top of navigation; the old weak pages
were labeled exactly “Historical rejected baseline”; C3/C4 now cite official
PDF, e-print and TeX hashes and disclose the ar5iv conflict; direct raw links
were added for C2 and C5.

## Pass 2 — after fixes

The same entrypoint traversal found, for every claim, its contract, assumptions,
inline output, code, fixed command, environment, raw data, independent checker,
negative control, verdict, and limitation. No conclusion required hidden
repository or OpenResearch knowledge. The visibility matrix has no missing
cells.
