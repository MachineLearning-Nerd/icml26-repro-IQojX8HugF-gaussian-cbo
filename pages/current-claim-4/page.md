# Current Claim 4 — FALSIFIED as printed

**Exact claim tested.** “Lemma 4.1 establishes well-posedness of the particle
dynamics under local Lipschitz continuity of the energy.”

The official arXiv v2 PDF and TeX number `l:well` as **Lemma 3.1** and print:

```text
E|m_0^i|^2, E||T_0^i||^2_{Sigma0} < 0.
```

Squared Euclidean and weighted matrix norms are pointwise nonnegative.
Monotonicity of expectation gives both expectations at least zero. Hence no
initial distribution satisfies the printed strict-negative premise, making the
lemma vacuous as published. It cannot establish the unqualified claim without
an erratum; the likely `< infinity` repair is a different contract.

The source verifier also confirms that the energy premise is the displayed
growth-weighted LOT-Lipschitz inequality for every pair of `P2` measures. A
mutation changing `<0` to `<infinity>` must and does fail the primary-source
hash.

```json
{"c4_is_falsified":true,"c4_actual_number_is_3_1":true,
"c4_impossible_moment_detected":true,"mutations_rejected":true}
```

Run `uv run python repro/src/verify.py`. See the
[claim contract](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim4/claim_contract.json),
[source audit](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim4/source_audit.md),
[verifier](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/verify_claims34.py),
[raw verdict](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim4/claim4_verdict.json),
and [independent checker](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim4/claim4_independent_checker.json).

This verdict does not claim the plausibly repaired theorem is false. The old
source-match-only page is [Historical rejected baseline](#/claim-4).
