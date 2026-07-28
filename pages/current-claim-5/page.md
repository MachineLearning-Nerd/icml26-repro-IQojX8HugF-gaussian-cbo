# Current Claim 5 — VERIFIED

**Exact claim.** On the released 2D mixture targets A–D, Gaussian CBO achieves a
lower final median KL than Bures–Wasserstein gradient flow, including the
non-convex bimodal cases.

The cumulative verifier re-reads all four committed raw bundles. Each contains
100 CBO and BW trajectories of length 201, plus SVGD (801) and FR (401).

| Target | CBO final median KL | BW final median KL | CBO lower? |
| --- | ---: | ---: | --- |
| A | `0.303598` | `0.664196` | yes |
| B | `0.0194335` | `0.0346156` | yes |
| C | `-0.0204902` | `0.0360361` | yes |
| D | `0.235077` | `0.429286` | yes |

Run `uv run python repro/src/verify.py`. The current
[summary code](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim5/summarize_authored_2d.py)
and [raw summary JSON](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim5/authored_2d_summary.json)
are mirrored here. Download the underlying source-scale arrays from GitHub:
[A](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/raw/main/outputs/authored_2d_A.raw.npz),
[B](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/raw/main/outputs/authored_2d_B.raw.npz),
[C](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/raw/main/outputs/authored_2d_C.raw.npz),
[D](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/raw/main/outputs/authored_2d_D.raw.npz).

The [independent checker](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim5/claim5_independent_checker.json)
rejects missing targets, incorrect shapes, non-finite values, absent baselines,
or any target where CBO is not lower. Its explicit
[negative control](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim5/claim5_negative_control.json)
removes target D and confirms that the required-target gate fails.

The previously judge-accepted full executed output remains unchanged at
[Historical accepted baseline — Claim 5](#/claim-5).

**Limit.** The verdict is scoped to these released A–D targets, this 100-run
protocol, and the paper’s final median KL estimator.
