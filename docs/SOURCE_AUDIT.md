# Primary-source audit

The archival source is arXiv `2601.00632v2`, whose downloaded e-print has
SHA-256 `3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482`.
The code artifact is independently pinned in `repro/upstream/` at
`borghig/GaussCBO@ab76cce88c44f3d6bd368c76b5c095d115db8787`.

| Claim | Source-faithful audit | Scope retained in this reproduction |
|---|---|---|
| C1 | Eq. (20)--(21) and Appendix B.2 give the explicit LBW weighted barycenter in linearized coordinates. | The independent test checks the coordinate average and log/extended-exp round trip on finite SPD instances. |
| C2 | Eq. (7), the consensus display, and the evolution display define Boltzmann weights `exp(-alpha E)`, consensus drift, and difference-scaled Brownian noise. The pinned `cbo.py` implements these at lines 81--96 and 153--170. | `verify_dynamics.py` independently checks exactly those finite algebraic ingredients; it does not identify numerical code with a proof. |
| C3 | The source labels the relevant mean-field convergence theorem **Theorem 3.5**, not Theorem 4.1. It is conditional on its stated assumptions and its large-alpha energy qualification. | **Not counted as source-faithful for this contract** because the current feed's theorem number is wrong. No finite run is presented as a proof of convergence. |
| C4 | Source Lemma 3.1 states a unique strong particle solution under the displayed moment and local-Lipschitz condition. The text immediately clarifies that local Lipschitzness of the component energies is a sufficient route to that condition. | Counted only with these conditions, not as an unconditional simulation claim. The executed source protocol supplies a finite no-exception sanity check, not a theorem proof. |
| C5 | Section 4/Figure 2 and `experiment_2D.ipynb` define 2D Gaussian-mixture targets, 100 repetitions, 20 particles, `T=10`, `dt=.05`, and the CBO/BW/SVGD/FR comparison. | Four unmodified-in-substance executed notebooks preserve the raw source outputs, one per target; only the notebook's `test` selector changes in memory. |
| C6 | Appendix B.2 explicitly extends `(I+T) Sigma0 (I+T)` to every symmetric `T` and states the result is PSD; its computation is matrix multiplication. | Independent random-matrix invariant test checks PSD numerically. |

The audit intentionally separates what a source theorem says from what a finite
reproduction can establish. In particular, C3 is disclosed as a contract/source
discrepancy rather than silently re-numbered.
