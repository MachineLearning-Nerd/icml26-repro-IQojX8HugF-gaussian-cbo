# Current verification summary

Previous live judge: **7/12** at immutable Space revision
`25fc9ebcb7055ac69fc2cad7a31a45c834678099`.

The current cumulative suite ran from Git SHA
`c3dc10d3dc90397af7404da268bc64ca52f65910` with the single command:

```bash
uv run python repro/src/verify.py
```

It used CPython 3.12.11, the committed `uv.lock`, a one-thread limit, and local
CPU. The complete run took 3.667 seconds. No GPU was used.

| Claim | Verdict | Central evidence | Honest scope |
| --- | --- | --- | --- |
| C1 | VERIFIED | 120 SPD cases; max barycenter error `3.61e-16`, round-trip `2.22e-13` | finite algebraic regression |
| C2 | VERIFIED | 40 particles × 400 steps × 24 seeds; median variance ratio `0.000964` | faithful finite dynamics demonstration |
| C3 | FALSIFIED | official result is Theorem 3.5 and gives finite-α near-optimality, not exact global optimality | exact attribution only |
| C4 | FALSIFIED | official Lemma 3.1 prints squared-moment expectations `<0` | exact printed lemma only |
| C5 | VERIFIED | full 100-run A–D arrays; CBO final median below BW on every target | released 2D protocol |
| C6 | VERIFIED | 120 arbitrary symmetric tangents; minimum covariance eigenvalue `0.001289` | finite check plus algebraic identity |

The exact primary sources are pinned by SHA-256: arXiv v2 e-print
`3481d169…2482`, official PDF `68bffac2…5c6c`, and retained main TeX
`6b35ec48…09b1`. ar5iv’s numbering conflict is disclosed on C3/C4 and is not
the sole basis of either verdict.

Download the [cumulative verdict JSON](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/evidence/current/cumulative/verdict.json)
and [pinned environment](https://huggingface.co/spaces/DineshAI/IQojX8HugF/tree/main/evidence/current/environment).
