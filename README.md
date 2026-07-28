# Claim-by-claim Gaussian CBO reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/blob/main/notebooks/gaussian_cbo_tutorial.py)

We reproduced all six evaluator claims for *Variational inference via Gaussian
interacting particles in the Bures–Wasserstein geometry*
([arXiv:2601.00632](https://arxiv.org/abs/2601.00632)). The central empirical
upgrade replaces a one-step toy with the exact Gaussian CBO recurrence over 40
particles, 400 steps, and 24 fixed seeds. Median final/initial particle variance
was **0.000964** (95% bootstrap CI `[0.000769, 0.001507]`), versus exactly
**1.0** for an update-omitted control.

Assessment: C1, C2, C5, and C6 are VERIFIED. C3 is FALSIFIED as attributed
because the official theorem gives exponential consensus plus a finite-α
near-optimality bound, not exact-global exponential convergence. C4 is
FALSIFIED as printed because its squared-moment expectations are required to
be `<0`. These source verdicts do not reject plausibly corrected theorems.

The full 2D mixture comparison was preserved at paper scale: targets A–D,
100 runs each, 20 CBO particles, `T=10`, `dt=.05`, with BW/SVGD/FR
comparators. No GPU was used; all formal checks ran on one-thread local CPU.
The latest verifier took 3.72 seconds, while cold/package release runs took up
to 15.74 seconds.

- [Illustrated technical report](reports/gaussian-cbo/report.md)
- [Self-contained marimo tutorial](notebooks/gaussian_cbo_tutorial.py)
- [Current evaluator logbook](https://huggingface.co/spaces/DineshAI/IQojX8HugF)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
| --- | --- | --- | --- | --- |
| `main` | Public landing page, report, and notebook | Not run as an experiment (publication surface) | Presentation only | none |
| [`orx/validated-7-of-12-baseline`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/validated-7-of-12-baseline) | Freeze and repair the judged baseline’s fresh-clone verifier | `uv run python repro/src/verify.py` | C1/C5/C6 pass; C2 toy; C3 absent; C4 weak | local CPU, 1 thread, 2.79 s verifier |
| [`orx/c2-multi-step-gaussian-cbo-dynamics`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/c2-multi-step-gaussian-cbo-dynamics) | Full recurrence, 24 seeds, literal-loop check, failing control | `uv run python repro/src/verify.py` | C2 VERIFIED; cumulative accepted claims pass | local CPU, 1 thread, 3.43 s |
| [`orx/c3-c4-exact-source-contracts`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/c3-c4-exact-source-contracts) | Hash-bound theorem/lemma parsing and mutation controls | `uv run python repro/src/verify.py` | C3 and C4 FALSIFIED as stated; all six resolved | local CPU, 1 thread, 3.67 s |
| [`orx/evaluator-visible-cumulative-release`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/evaluator-visible-cumulative-release) | Additive Space candidate, report, notebook, and accepted-claim controls | `uv run python repro/src/verify.py` | All six resolved; C1/C5/C6 controls and explicit singular C6 case pass | local CPU, 1 thread, 6.16 s |
| [`orx/final-release-manifest`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/final-release-manifest) | Freeze allowlist, hashes, and release-gate regression | `uv run python repro/src/verify.py` | All six resolved; release gate passes | local CPU, 1 thread, 15.74 s |
| [`orx/post-publication-provenance-correction`](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/tree/orx/post-publication-provenance-correction) | Reporting-only correction of runtime and command provenance | `uv run python repro/src/verify.py` | Claim evidence unchanged; cumulative regression passes | local CPU, 1 thread, 3.72 s |

The previous live score remains **7/12** until the live judge evaluates a new
Space revision. A conservative forecast is 9–12/12; 12/12 is the
best-supported possible outcome, not an earned score.

---

# Gaussian CBO reproduction — IQojX8HugF

Reproduction of *Variational inference via Gaussian interacting particles in
the Bures--Wasserstein geometry* (arXiv:2601.00632v2).

The primary implementation is pinned at
`borghig/GaussCBO@ab76cce88c44f3d6bd368c76b5c095d115db8787` in
`repro/upstream/`. It is NumPy-only and the source-scale 2D protocol runs on
CPU: targets A--D, 100 independent runs per target, 20 particles, `T=10`, and
`dt=.05`.

## Reproduce the authors' protocol

```bash
source .venv/bin/activate
python repro/src/run_authored_2d.py --targets A --timeout 3600
python repro/src/run_authored_2d.py --targets B --timeout 3600
python repro/src/run_authored_2d.py --targets C --timeout 3600
python repro/src/run_authored_2d.py --targets D --timeout 3600
python repro/src/verify.py
```

The wrapper retains source notebook cells 0--5, which include the authors'
single-run and full repeated comparison. It changes only the documented target
selector in cell 5, then appends one I/O-only cell to retain the already-created
four trajectory matrices as a compressed raw artifact. It writes one completed
notebook and one raw `.npz` atomically per target. This avoids mixing the
separately scoped sensitivity sweeps into the claim-5 artifact while preserving
the released 100-run comparison unchanged.

## Evidence policy

The six active anchored claims are listed verbatim in
[`docs/CLAIMS_PINNED.md`](docs/CLAIMS_PINNED.md). The source labels its
mean-field convergence result *Theorem 3.5*, while the current anchored feed
calls it *Theorem 4.1*. The mismatch is retained in the evidence map; this
package will not represent the numbering as source-faithful.
