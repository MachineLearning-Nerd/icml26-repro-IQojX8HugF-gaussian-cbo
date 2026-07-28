# Current Claim 6 — VERIFIED

**Exact claim.** Extending the covariance map to every symmetric tangent,
`(I+T) Sigma0 (I+T)`, automatically preserves positive semidefiniteness and
permits singular covariances without a projection.

For any vector `x`,

```text
x' (I+T) Sigma0 (I+T) x
= ((I+T)x)' Sigma0 ((I+T)x) >= 0,
```

because `Sigma0` is positive semidefinite and `T` is symmetric. If `I+T` is
singular, the covariance can be singular; no clipping or eigenspace projection
is added. The operation is the same pair of matrix multiplications used by the
extended map.

The cumulative numerical regression sampled 120 SPD references and arbitrary
symmetric tangents. Its minimum observed covariance eigenvalue was
`0.0012894107712282973`; all PSD assertions passed.

Run `uv run python repro/src/verify.py`. Inspect
[verify_geometry.py](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim6/verify_geometry.py)
and [raw output](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim6/independent_geometry.json).
The [independent checker](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim6/claim6_independent_checker.json)
also constructs `T=diag(-1,0)`, obtaining an exact zero eigenvalue, and its
[control](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim6/claim6_negative_control.json)
rejects a negative-eigenvalue mutation.
The previously accepted page remains [reachable](#/claim-6).

**Limit.** “No added cost” is checked structurally—no projection and the same
two matrix products—not as a universal wall-clock equality across libraries.
