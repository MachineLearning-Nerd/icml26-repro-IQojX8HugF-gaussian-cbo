# STATUS — IQojX8HugF Gaussian CBO

- Owner: `root`; state: `publication_queued`; last updated: 2026-07-27.
- Fresh Hugging Face contract audit: six active anchored claims, hence 12
  possible points before jury review.
- Pinned paper: arXiv `2601.00632v2`; PDF SHA-256
  `68bffac253ef7c3f6d065d216dc1a6973b2b9434c294f770fef7b80cadab5c6c`;
  e-print SHA-256
  `3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482`.
- Pinned author source: `borghig/GaussCBO@ab76cce88c44f3d6bd368c76b5c095d115db8787`.
- Completed: full released 2D protocol on targets A--D, each with 100 runs,
  four baselines, executed notebook, and compressed raw trajectories. Three
  unit tests pass; `outputs/verdict.json` gives a 5/6 source-faithful local
  verdict (C1, C2, C4, C5, C6), sufficient for the 10-point threshold.
- Published code: https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo
  at commit `619519a` (the status transition itself follows in the next commit).
- Next action: the shared drain publishes the HF Space; then verify the public
  Space, required tags, commit SHA, and artifact bucket before moving to
  `under_verdict`.
- Blockers: none. C3 remains excluded because the claim feed says Theorem 4.1
  while the pinned source labels the applicable result Theorem 3.5.
