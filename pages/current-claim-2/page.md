# Current Claim 2 — VERIFIED

**Exact claim.** The Gaussian CBO particle recurrence combines normalized
weights `exp(-alpha E)`, deterministic drift toward the weighted LBW
barycenter, and difference-scaled stochastic exploration, driving particles
toward consensus over time.

**Faithful protocol.** In orthonormal `d=2` LBW coordinates, 40 Gaussian
particles execute 400 Euler–Maruyama steps (`dt=.01`, `alpha=20`, `lambda=1`,
`sigma=.7`) for seeds 260100–260123. The same Gaussian increments are evaluated
by vectorized and literal particle-by-particle updates.

| Quantity | Result |
| --- | ---: |
| median final/initial variance | `0.0009641721` |
| bootstrap 95% CI | `[0.0007690647, 0.0015070913]` |
| seeds below ratio 0.05 | `24/24` |
| median second-half log slope | `-1.7437756` |
| literal-loop max error | `0` |
| frozen-update control ratio | `1.0` |

The corrupted frozen-update control uses identical inputs and computes weights,
drift, and noise but omits the state update. It remains at variance ratio one
and fails the main consensus threshold, proving that the checker does not pass
from initialization alone. A preregistered high-noise control was rejected
after typical paths still contracted; it is not presented as supporting
evidence.

Run `uv run python repro/src/verify.py`. Inspect the
[generator](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/run_claim2_dynamics.py),
[independent checker](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/check_claim2.py),
[raw trajectory CSV](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/claim2_trajectory.csv),
[particle snapshots](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/claim2_particle_snapshots.csv),
[checker output](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/claim2_checker.json),
and [control output](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim2/claim2_negative_control.json).

**Limit.** This directly replaces the old one-step toy, but remains a finite
smooth-energy dynamics demonstration, not the universal mean-field theorem.
The old page is labeled [Historical rejected baseline](#/claim-2).
