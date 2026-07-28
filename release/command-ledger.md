# Command ledger

All formal scientific checks used one inherited command:

```bash
uv run python repro/src/verify.py
```

The orchestration and audit commands executed during this campaign were:

```bash
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx skill orx-lit
orx projects --json
orx project view 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3
orx runs 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3
git branch -a
git status --short
git rev-parse HEAD
df -h .
env | sed 's/=.*//' | sort
git submodule update --init --recursive
orx paper 2601.00632 --full
curl -L -A 'OpenResearch-Reproduction/1.0' https://export.arxiv.org/e-print/2601.00632v2
curl -L -A 'OpenResearch-Reproduction/1.0' https://ar5iv.labs.arxiv.org/html/2601.00632v2
curl -L -A 'OpenResearch-Reproduction/1.0 (paper audit)' https://arxiv.org/pdf/2601.00632v2
pdftotext -layout 2601.00632v2.pdf 2601.00632v2.txt
curl -L https://huggingface.co/datasets/ICML-2026-agent-repro/verdicts/resolve/main/verdicts.json
git clone https://huggingface.co/spaces/DineshAI/IQojX8HugF
git clone https://huggingface.co/spaces/MarxistLeninist/IQojX8HugF
uv lock
uv sync
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'Validated 7-of-12 baseline' --run-command 'uv run python repro/src/verify.py'
orx exp run 828df604-7190-4001-829b-e8ac8b84ed99 --backend local
orx exp wait 828df604-7190-4001-829b-e8ac8b84ed99 --timeout 480
orx logs 36eb906f-e372-4066-b10e-3b3b0e3bc953
orx exp run 828df604-7190-4001-829b-e8ac8b84ed99 --backend local
orx exp wait 828df604-7190-4001-829b-e8ac8b84ed99 --timeout 480
orx logs 83698a54-9946-4165-a4ad-4890f2ce3fb5
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'C2 multi-step Gaussian CBO dynamics' --parent 828df604-7190-4001-829b-e8ac8b84ed99
orx exp run c50c49d4-3090-4e76-83e6-6ae886f618ba --backend local
orx exp wait c50c49d4-3090-4e76-83e6-6ae886f618ba --timeout 480
orx logs 46b1838e-7099-4ec9-8cee-658c00b24de2
orx exp run c50c49d4-3090-4e76-83e6-6ae886f618ba --backend local
orx exp wait c50c49d4-3090-4e76-83e6-6ae886f618ba --timeout 480
orx logs 1d0dae31-9bd9-489c-9ac7-f798bd7ef220
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'C3-C4 exact source contracts' --parent c50c49d4-3090-4e76-83e6-6ae886f618ba
orx exp run 7723542d-c569-446e-bcd6-2b7b321de3df --backend local
orx exp wait 7723542d-c569-446e-bcd6-2b7b321de3df --timeout 480
orx logs bd7873e8-1303-4425-84a7-c63542671cf2
orx exp run 7723542d-c569-446e-bcd6-2b7b321de3df --backend local
orx exp wait 7723542d-c569-446e-bcd6-2b7b321de3df --timeout 480
orx logs 14a515f2-ac1e-47a2-b12d-d6bd1b8b39ff
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'Evaluator-visible cumulative release' --parent 7723542d-c569-446e-bcd6-2b7b321de3df
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 uv run python reports/gaussian-cbo/make_figures.py
uv run marimo check notebooks/gaussian_cbo_tutorial.py
uv run python repro/src/audit_space_candidate.py
orx exp run 3623cc7b-be13-4ea7-8d36-fd2563f6f44f --backend local
orx exp wait 3623cc7b-be13-4ea7-8d36-fd2563f6f44f --timeout 480
orx logs 2f287973-817b-47c9-b9d2-98eb22ff77eb
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'Final release manifest' --parent 3623cc7b-be13-4ea7-8d36-fd2563f6f44f
orx exp run d0d96a1f-ace3-4379-83d8-adcfd2eb87ab --backend local
orx exp wait d0d96a1f-ace3-4379-83d8-adcfd2eb87ab --timeout 480
orx logs 1f344847-63ab-4d36-8afd-23d1bc2acc91
python3 repro/src/audit_space_candidate.py
git clone --branch orx/final-release-manifest --single-branch git@github.com:MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo.git
git ls-remote origin refs/heads/orx/final-release-manifest
HfApi.create_commit(repo_id="DineshAI/IQojX8HugF", repo_type="space", operations=<89 allowlisted text files>, parent_commit="25fc9ebcb7055ac69fc2cad7a31a45c834678099")
git push origin main
git ls-remote origin refs/heads/main
snapshot_download(repo_id="DineshAI/IQojX8HugF", repo_type="space", revision="057941dfbe085e4bcf52e76179023eb2b2fa8e65")
orx create-experiment 88269cec-b3b8-4872-ab6e-8fcc0f2ec9b3 --title 'Post-publication provenance correction' --parent d0d96a1f-ace3-4379-83d8-adcfd2eb87ab
```

All Git edits were committed and pushed before the corresponding formal run.
No direct training command, GPU command, raw SSH command, or alternate run
command was used. The final reporting-only node's formal run is discoverable
from its inherited command and `orx exp status`; it necessarily occurs after
this ledger is frozen into that node's commit.
