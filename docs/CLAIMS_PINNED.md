# Pinned current anchored contract

Refreshed 2026-07-27 from the official challenge Space
`ICML-2026-agent-repro/challenge`, `claims_anchored.json` SHA-256
`7c0373fbbfb98b5acdc2c0ac122d9d81431bd6b42dda76fa36a91b49ec4b7825`.

1. The LBW parametrization identifies a non-degenerate Gaussian with its OT
   map from a reference measure and has a closed-form weighted barycenter.
2. Gaussian CBO uses stochastic exploration plus deterministic drift to
   exponentially weighted consensus barycenters.
3. The feed attributes exponential convergence to global minimizers to
   “Theorem 4.1”. The pinned source instead presents the applicable result as
   **Theorem 3.5**: the mean-field consensus converges exponentially to
   `z_tilde`, with energy approaching the infimum as alpha increases, under
   explicit smoothness, support, and parameter assumptions. This package
   preserves that limitation exactly.
4. Local-Lipschitz energy conditions give a unique strong particle solution
   (source Lemma 3.1).
5. On low-dimensional non-log-concave Gaussian mixtures, the released CBO
   protocol is compared against BW gradient flow and other baselines.
6. The extended map `(I+T) Sigma0 (I+T)` remains PSD for every symmetric `T`
   and costs no more than the base matrix operations.

Every claim requires both source-aligned evidence and an independent check;
finite experiments are not presented as proofs of universal statements.

