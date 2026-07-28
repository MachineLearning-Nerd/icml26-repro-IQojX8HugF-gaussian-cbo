# Claim 3 method

The verifier parses the complete retained primary TeX, reconstructs the shared
theorem counter, extracts the `t:convergence` block, and checks each conclusion
separately. It treats exponential consensus and finite-alpha near-optimality as
different statements.

The independent checker reads only the emitted verdict and the primary source
hash. A mutation control replaces the finite-alpha inequality by exact equality
and must be rejected by the source hash. No finite run is used as proof of a
universal theorem.
