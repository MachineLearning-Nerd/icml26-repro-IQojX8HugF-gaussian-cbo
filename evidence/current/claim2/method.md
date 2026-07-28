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

The negative control is a deliberately corrupted implementation with the
particle update omitted while all inputs, seeds, weights, drift, and noise are
still computed. Its particle variance must remain exactly unchanged, and it
must fail the main consensus threshold. This tests that the independent
checker cannot pass merely because the input ensemble or energy is convenient.
The checker reads only raw CSV/JSON files and exits nonzero unless both the
positive criteria and the intended control failure hold.

An earlier `sigma=2` control was rejected after its typical paths still
contracted. That is expected for multiplicative geometric noise even when a
second moment can grow; it was not a valid median-trajectory control.
