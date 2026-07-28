# Claim 2 method

The verifier works in the five-dimensional orthonormal LBW coordinate vector
`(m1,m2,T11,T22,sqrt(2)T12)` for `d=2`, with identity reference covariance.
This makes the paper's component-wise product and Brownian increments literal
Euclidean operations without replacing the named algorithm.

For 24 fixed seeds and 40 particles, the verifier executes 400
Euler--Maruyama steps on a smooth quadratic energy. It records particle
variance, energy, exponential-weight concentration, drift magnitude, noise
magnitude, and the smallest eigenvalue of `I+T` at every step. Five full
particle snapshots per seed are retained separately. A particle-by-particle
loop is compared with the vectorized update using the same Gaussian
increments.

The negative control changes only the diffusion scale from `0.7` to `2.0`.
This crosses the standard consensus boundary `sigma^2 < 2 lambda`; it should
increase rather than contract ensemble variance. The independent checker reads
only raw CSV/JSON files and exits nonzero unless both the positive criteria and
the intended control failure hold.
