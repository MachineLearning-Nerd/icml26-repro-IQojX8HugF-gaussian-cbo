# Current Claim 1 — VERIFIED

**Exact claim.** The LBW parametrization maps each non-degenerate Gaussian to
its optimal transport map from a reference Gaussian and makes the weighted
barycenter a closed-form coordinate average.

**Contract and assumptions.** The checker samples 120 independent SPD
reference/target matrices and normalized positive weight vectors. It compares
the weighted LBW coordinate average with the implementation and checks
log/extended-exp round trips.

**Observed raw result.**

```json
{"instances":120,"max_weighted_average_error":3.606973610583171e-16,
"max_log_exp_roundtrip_error":2.2216942829692866e-13,"pass":true}
```

The fail-closed cumulative command is
`uv run python repro/src/verify.py`; seed handling and assertions are visible in
[verify_geometry.py](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim1/verify_geometry.py),
with [raw JSON](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim1/independent_geometry.json).
An [independent checker output](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim1/claim1_independent_checker.json)
re-reads the raw JSON. Its [negative control](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim1/claim1_negative_control.json)
adds `1e-6` to the weighted-average error and confirms that the `1e-10` gate
rejects it.

**Limit.** This is a high-precision finite regression, not a replacement for
the algebraic derivation. The previously judge-accepted page remains reachable
as [historical evidence](#/claim-1).
