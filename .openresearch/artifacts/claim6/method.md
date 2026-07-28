# Claim 6 method

The direct identity writes the quadratic form as
`((I+T)x)' Sigma0 ((I+T)x) >= 0`. `verify_geometry.py` adds 120 random
instances. `check_accepted_claims.py` constructs `T=diag(-1,0)`, yielding an
exact zero eigenvalue, and rejects a negative-eigenvalue mutation.
