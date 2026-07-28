# Claim 2 source audit

The source archive was retrieved from
`https://export.arxiv.org/e-print/2601.00632v2` on
`2026-07-28T04:49:03Z` with an explicit
`OpenResearch-Reproduction/1.0` User-Agent. Its SHA-256 is
`3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482`.
The independent ar5iv rendering
`https://ar5iv.labs.arxiv.org/html/2601.00632v2` had SHA-256
`89b6200a35a9474359e9f55f1b4724baee8e2b13bb6d1685e740994d4ebe3f45`.

The exact source anchors are:

- `eq:consensus`: normalized weights proportional to
  `exp(-alpha E#(m,T))` and the weighted mean in LBW coordinates;
- `eq:cboLBW`: for each of `N` particles, deterministic drift
  `lambda(zbar-z) dt` plus coordinate-wise multiplicative Brownian noise
  `sigma(zbar-z) odot dB`;
- `eq:cbonum`: the Euler--Maruyama recurrence with `sqrt(dt)` Gaussian
  increments;
- `alg:gcbo`: evaluate energy, compute weights and consensus, sample normal
  vectors, and update every particle until convergence.

The source assumes `lambda,sigma > 0`, independent Brownian processes, and
i.i.d. initial particles. Claim 2 is an algorithm/mechanism claim, not the
universal mean-field convergence theorem audited separately as Claim 3.
