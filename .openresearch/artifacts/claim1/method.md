# Claim 1 method

`verify_geometry.py` samples 120 SPD reference/target configurations and
normalized positive weights. It checks the coordinate-average formula and the
log/extended-exp round trip. `check_accepted_claims.py` independently reads the
raw JSON; a `1e-6` error mutation must fail the `1e-10` tolerance.
