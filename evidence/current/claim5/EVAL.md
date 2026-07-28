# Claim 5 evaluation

Run `uv run python repro/src/verify.py`. It re-reads all four 100-run raw
bundles, prints every endpoint result, and exits nonzero for an incomplete
target set, malformed shape, non-finite value, missing baseline, or failed
CBO-versus-BW comparison.
