# Evaluator visibility matrix

Traversal starts at `pages/index.md` and uses only pages and links visible
there. “Complete” means the canonical page exposes the exact contract,
assumptions, code, command/environment, inline result, raw link, checker,
control, limitations, and evidence verdict.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | current-claim-1 | yes | yes | yes | yes | deterministic tolerance rejection | yes | VERIFIED |
| C2 | current-claim-2 | yes | yes | yes | yes | frozen update fails | yes | VERIFIED |
| C3 | current-claim-3 | yes | yes | yes | yes | exact-global source mutation rejected | yes | FALSIFIED |
| C4 | current-claim-4 | yes | yes | yes | yes | finite-moment repair rejected | yes | FALSIFIED |
| C5 | current-claim-5 | yes | yes | yes | yes | malformed/missing arrays fail | yes | VERIFIED |
| C6 | current-claim-6 | yes | yes | yes | yes | negative eigenvalue fails | yes | VERIFIED |

Shared command: `uv run python repro/src/verify.py`. Shared environment:
[Python pin, pyproject and uv.lock](https://huggingface.co/spaces/DineshAI/IQojX8HugF/tree/main/evidence/current/environment).
Evidence-generating Git SHA:
`c3dc10d3dc90397af7404da268bc64ca52f65910`.
