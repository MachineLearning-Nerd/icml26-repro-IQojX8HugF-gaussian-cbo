# Results

The final local gate verifies five source-faithful anchored claims: C1, C2,
C4, C5, and C6. C3 is deliberately not counted: the current feed says
“Theorem 4.1,” whereas the pinned source calls the relevant result Theorem 3.5.

For C5, the released repeated-run protocol was executed for every defined 2D
target: 100 repetitions, 20 CBO particles, `T=10`, `dt=.05`, and BW/SVGD/FR
comparators. Each result has an executed notebook plus full trajectory arrays.

| Target | CBO median final KL | BW median final KL | CBO < BW |
|---|---:|---:|---|
| A | 0.303598 | 0.664196 | yes |
| B | 0.0194335 | 0.0346156 | yes |
| C | -0.0204902 | 0.0360361 | yes |
| D | 0.235077 | 0.429286 | yes |

This is an in-scope comparison, not a universal superiority claim: CBO is not
claimed here to dominate every baseline, every metric, or every target.
