# Current Claim 3 — FALSIFIED as attributed

**Exact claim tested.** “Theorem 4.1 proves convergence of the Gaussian CBO
dynamics to global minimizers at an exponential rate.”

The official arXiv v2 PDF and TeX number the source anchor `t:convergence` as
**Theorem 3.5**. More importantly, its exponential conclusions are:

- `Var(rho_t) -> 0` exponentially;
- the consensus point and ordinary mean converge exponentially to `z_tilde`.

At finite `alpha`, global optimality is only bounded:

```text
E#(z_tilde) <= inf E# + r(alpha) + log(2)/alpha,
with r(alpha) -> 0 as alpha -> infinity.
```

The theorem does not state `E#(z_tilde)=inf E#` or
`z_tilde in argmin E#` at finite `alpha`. Therefore the exact attribution
conflates exponential consensus with exact-global convergence and is
**FALSIFIED**. This does not falsify the corrected theorem.

The source-bound parser reconstructs the shared theorem counter and rejects a
mutation replacing the inequality by exact equality. Its independent checker
passes every gate:

```json
{"source_hash_matches":true,"c3_is_falsified":true,
"c3_actual_number_is_3_5":true,"c3_finite_alpha_bound_detected":true,
"c3_exact_minimizer_statement_absent":true,"mutations_rejected":true}
```

Run `uv run python repro/src/verify.py`. See the
[claim contract](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/claim_contract.json),
[verifier](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/verify_claims34.py),
[checker](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/check_claims34.py),
[raw verdict](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/claim3_verdict.json),
and [mutation control](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/claim3/source_mutation_controls.json).

The ar5iv v2 HTML renders the anchor as Theorem 4.1, conflicting with the
official PDF. The semantic finite-α gap survives either numbering.
