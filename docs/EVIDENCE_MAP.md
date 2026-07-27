# Claim evidence map

| Claim | Primary-source anchor | Required evidence | Current assessment |
|---|---|---|---|
| C1 LBW closed-form barycenter | Eq. (5), Eq. (20)--(21), Appendix B.2 | Pinned implementation plus independent weighted-coordinate and log/exp round-trip checks | Independent finite checks pass; source-scale code path is pinned. |
| C2 CBO dynamics | Eq. (7), Algorithm 1 | Author run and an independent inspection of exponential weights/drift/noise terms | Pass: `outputs/independent_dynamics.json` checks the three finite algebraic ingredients; the full source notebooks exercise the pinned implementation. |
| C3 convergence | Source **Theorem 3.5** | Assumption-by-assumption source audit and a finite illustrative control | Contract calls this “Theorem 4.1”; wording/number mismatch must remain disclosed. Do not claim a finite experiment proves the universal result. |
| C4 well-posedness | Source Lemma 3.1 | Exact source assumptions plus a solution-path sanity check | Pass, conditional exactly as stated in the source; see `SOURCE_AUDIT.md`. The finite runs are sanity evidence only, not a proof. |
| C5 non-convex GMM comparison | Section 4, Figure 2, released `experiment_2D.ipynb` | Full author protocol: 100 repetitions with all four baselines; independent raw-output readback | Pass: A--D notebooks have no errors and raw 100-run trajectories. CBO/BW final median KL: A `0.303598/0.664196`; B `0.0194335/0.0346156`; C `-0.0204902/0.0360361`; D `0.235077/0.429286`. |
| C6 extended exponential map | Eq. (4), Figure 3, Appendix B.2 | Independent PSD invariant over arbitrary symmetric tangents | Pass: 120 random SPD instances, minimum eigenvalue `0.0012894`. |

The local gate passes **5/6** source-faithful claims (C1, C2, C4, C5, C6) and
rejects the contract/source mismatch in C3. Each asserted empirical C5 result
has both its executed source notebook and a complete compressed raw trajectory
artifact.
