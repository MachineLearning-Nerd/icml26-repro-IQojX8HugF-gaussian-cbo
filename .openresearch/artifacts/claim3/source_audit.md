# Claim 3 source audit

The official arXiv v2 PDF was retrieved on 2026-07-28 with the explicit
`OpenResearch-Reproduction/1.0 (paper audit)` User-Agent. Its SHA-256 is
`68bffac253ef7c3f6d065d216dc1a6973b2b9434c294f770fef7b80cadab5c6c`.
The v2 e-print archive SHA-256 is
`3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482`;
the retained main TeX has SHA-256
`6b35ec4859cc23bac62bec4a20c6a9d59e1c360a9cf44a1ba1b68b96042b09b1`.

The official PDF calls `t:convergence` **Theorem 3.5**, not Theorem 4.1.
The theorem assumes a bounded-below twice differentiable finite-dimensional
energy with bounded second derivatives, support covering the minimizers, and
explicit `C1>0`, `C2<=3/4` parameter/initial-law conditions. Its exponential
conclusions concern variance and convergence to a consensus point. At finite
`alpha`, it concludes only
`E#(z_tilde) <= inf E# + r(alpha) + log(2)/alpha`; the residual tends to zero
as `alpha -> infinity`.

The ar5iv v2 HTML rendering numbers the same anchor as Theorem 4.1, in conflict
with the official PDF and archived TeX structure. Numbering alone is therefore
not the main scientific basis: the stronger exact-global exponential
conclusion is absent in either rendering.
