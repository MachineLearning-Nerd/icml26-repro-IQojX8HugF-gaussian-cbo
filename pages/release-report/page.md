# Release report and score forecast

- Previous live judged score: `7/12`
- Conservative projected score range after the proposed change: **9–12/12**
- Best-supported possible new score: **12/12 forecast, not a judge result**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| C1 | 2 | 2 | HIGH | VERIFIED | accepted 120-case algebra check reruns; finite numerical scope |
| C2 | 1 | 2 | HIGH | VERIFIED | full recurrence over 24 multi-step runs plus literal loop and failing frozen control |
| C3 | 0 | 2 | MEDIUM | FALSIFIED | exact attribution exceeds official theorem; risk is evaluator interpretation of source-version numbering |
| C4 | 0 | 2 | MEDIUM | FALSIFIED | impossible printed premise is decisive; risk is evaluator silently treating `<0` as an obvious typo |
| C5 | 2 | 2 | HIGH | VERIFIED | accepted full 100-run A–D raw arrays rerun unchanged |
| C6 | 2 | 2 | HIGH | VERIFIED | accepted PSD regression plus direct quadratic-form identity |

Current total remains **7/12** until the live judge evaluates a new revision.
The conservative projected total is **9–12/12**; the best-supported possible
total is **12/12**, solely as a forecast.

Changed since the previous judge: C2 replaces a one-step toy with multi-step
dynamics; C3 and C4 gain exact, executable source falsifications. No claim is
BLOCKED in the candidate. Historical accepted evidence for C1/C5/C6 remains
reachable and unchanged.

Exact publication action: upload only the manifest-listed text files to the
existing `DineshAI/IQojX8HugF` Space using the Hugging Face API, then download
the returned revision and repeat the hash/traversal audit. The initial
evidence upload produced `057941df…`; this additive child corrects its runtime
provenance without changing any claim result. No second Space is created.

Baseline HF Head and Judge Head are both
`25fc9ebcb7055ac69fc2cad7a31a45c834678099`. The winning scientific branch is
`orx/c3-c4-exact-source-contracts` at `c3dc10d3…`; the frozen formal release
branch is `orx/final-release-manifest` at `9835abf6…`. The stacked tree is
baseline → C2 dynamics → C3/C4 source contracts → evaluator-visible package →
final manifest → reporting-only provenance correction.

All work used local CPU because every task was estimated at one core and under
five minutes. The final frozen manifest verifier took 15.737 seconds (the
preceding evaluator package took 6.165 seconds); local cost was `$0`, Hugging
Face CPU runtime/cost was `0 s / $0`, and GPU runtime was zero.
The judged tree has 21 paths; all 21 remain in the candidate, all immutable
ones are byte-identical, and exact historical copies preserve the two changed
navigation files.

The exact 89-path text upload list and its SHA-256 manifest are
[allowlist](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/release/upload-allowlist.txt)
and [manifest](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/release/upload-manifest.sha256).
The full [command ledger](https://huggingface.co/spaces/DineshAI/IQojX8HugF/blob/main/release/command-ledger.md)
is evaluator-visible.
