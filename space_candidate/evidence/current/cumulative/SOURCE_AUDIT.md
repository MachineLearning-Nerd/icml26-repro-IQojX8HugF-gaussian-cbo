# Primary-source audit

The archival source is arXiv `2601.00632v2`, whose downloaded e-print has
SHA-256 `3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482`.
The code artifact is independently pinned in `repro/upstream/` at
`borghig/GaussCBO@ab76cce88c44f3d6bd368c76b5c095d115db8787`.

| Claim | Source-faithful audit | Scope retained in this reproduction |
|---|---|---|
| C1 | Eq. (20)--(21) and Appendix B.2 give the explicit LBW weighted barycenter in linearized coordinates. | The independent test checks the coordinate average and log/extended-exp round trip on finite SPD instances. |
| C2 | Eq. (7), the consensus display, and the evolution display define Boltzmann weights `exp(-alpha E)`, consensus drift, and difference-scaled Brownian noise. The pinned `cbo.py` implements these at lines 81--96 and 153--170. | A 400-step, 40-particle test over 24 seeds checks the full recurrence, with a literal-loop comparison and frozen-update negative control. It remains finite evidence, not a universal proof. |
| C3 | The official PDF and archived TeX label the relevant result **Theorem 3.5**, not Theorem 4.1. More importantly, it proves exponential variance/consensus convergence and only a finite-`alpha` near-optimality inequality. | **FALSIFIED as attributed.** The source-bound verifier distinguishes exponential consensus from exact global optimality and rejects a mutated exact-equality source. |
| C4 | The official PDF and archived TeX label the result **Lemma 3.1**. Its printed initial-moment premise is `<0`, which no expectation of a squared norm can satisfy. | **FALSIFIED as printed.** A machine-checked order certificate establishes vacuity; a plausible `<infinity` repair is explicitly treated as a different contract. |
| C5 | Section 4/Figure 2 and `experiment_2D.ipynb` define 2D Gaussian-mixture targets, 100 repetitions, 20 particles, `T=10`, `dt=.05`, and the CBO/BW/SVGD/FR comparison. | Four unmodified-in-substance executed notebooks preserve the raw source outputs, one per target; only the notebook's `test` selector changes in memory. |
| C6 | Appendix B.2 explicitly extends `(I+T) Sigma0 (I+T)` to every symmetric `T` and states the result is PSD; its computation is matrix multiplication. | Independent random-matrix invariant test checks PSD numerically. |

The ar5iv v2 HTML rendering numbers these anchors as Theorem/Lemma 4.1, in
conflict with the official PDF and archived TeX structure. The audit records
that discrepancy. Neither verdict depends on numbering alone: C3 turns on the
finite-`alpha` conclusion, and C4 on the impossible printed premise.
