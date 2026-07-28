# Claim 3 evaluation

Run the inherited fixed command:

`uv run python repro/src/verify.py`

The current verifier is `repro/src/verify_claims34.py`; its independent checker
is `repro/src/check_claims34.py`. Both must exit zero, the claim verdict must be
exactly `FALSIFIED`, and the primary-source mutation must be rejected.
