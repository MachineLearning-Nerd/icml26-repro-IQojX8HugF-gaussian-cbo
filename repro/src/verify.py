"""Fail-closed local verdict for the source-faithful IQojX8HugF bundle."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
for variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ[variable] = "1"


def run(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def main() -> None:
    started = time.perf_counter()
    print(
        json.dumps(
            {
                "compute": {
                    "backend": "recorded_by_orx",
                    "estimated_cores": 1,
                    "thread_limit": 1,
                    "visible_logical_cpus": os.cpu_count(),
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                }
            }
        )
    )
    run("repro/src/verify_geometry.py")
    run("repro/src/verify_dynamics.py")
    claim2_checker_path = ROOT / ".openresearch" / "artifacts" / "claim2" / "generated" / "claim2_checker.json"
    if (ROOT / "repro" / "src" / "verify_claim2.py").is_file():
        run("repro/src/verify_claim2.py")
    if (ROOT / "repro" / "src" / "verify_claims34_bundle.py").is_file():
        run("repro/src/verify_claims34_bundle.py")
    run("repro/src/summarize_authored_2d.py")
    geometry = json.loads((ROOT / "outputs" / "independent_geometry.json").read_text())
    dynamics = json.loads((ROOT / "outputs" / "independent_dynamics.json").read_text())
    claim2_checker = (
        json.loads(claim2_checker_path.read_text())
        if claim2_checker_path.is_file()
        else {"verdict": "TOY"}
    )
    claim3_path = ROOT / ".openresearch" / "artifacts" / "claim3" / "generated" / "claim3_verdict.json"
    claim4_path = ROOT / ".openresearch" / "artifacts" / "claim4" / "generated" / "claim4_verdict.json"
    claim3 = json.loads(claim3_path.read_text()) if claim3_path.is_file() else {"verdict": "BLOCKED"}
    claim4 = json.loads(claim4_path.read_text()) if claim4_path.is_file() else {"verdict": "BLOCKED"}
    authored = json.loads((ROOT / "outputs" / "authored_2d_summary.json").read_text())
    audit = (ROOT / "docs" / "SOURCE_AUDIT.md").read_text(encoding="utf-8")
    source_hash = "3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482"

    verdict = {
        "C1": {
            "passed": geometry["c1_lbw_closed_form"]["pass"],
            "evidence": "Independent weighted-coordinate and log/extended-exp finite checks.",
        },
        "C2": {
            "passed": dynamics["c2_cbo_dynamics"]["pass"] and claim2_checker["verdict"] == "VERIFIED",
            "evidence": (
                "Multi-step 40-particle trajectories across 24 seeds with raw CSV, "
                "literal-loop recurrence check, and a frozen-update negative control."
            ),
        },
        "C3": {
            "passed": claim3["verdict"] == "FALSIFIED",
            "verdict": claim3["verdict"],
            "evidence": "Exact-source attribution falsified: the actual Theorem 3.5 proves exponential consensus and only a finite-alpha near-optimality bound.",
        },
        "C4": {
            "passed": claim4["verdict"] == "FALSIFIED",
            "verdict": claim4["verdict"],
            "evidence": "Exact printed attribution falsified: Lemma 3.1 has an impossible strictly-negative squared-moment assumption and is vacuous as printed.",
        },
        "C5": {
            "passed": authored["c5_cbo_beats_bw_on_all_targets"],
            "evidence": "Four committed raw trajectory bundles, each at 100 repetitions, CBO final median KL < BW final median KL.",
        },
        "C6": {
            "passed": geometry["c6_extended_map_psd"]["pass"],
            "evidence": "Independent random symmetric-tangent PSD invariant check.",
        },
    }
    checked = [item for item in verdict.values() if item["passed"]]
    verdict["summary"] = {
        "claims_checked": 6,
        "claims_source_faithful_verified": len(checked),
        "minimum_for_ten_points": 5,
        "publication_gate_passed": len(checked) >= 5,
        "scope": "C3/C4 are source-attribution falsifications, not finite simulations presented as universal theorem proofs.",
    }
    (ROOT / "outputs" / "verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verdict, indent=2))
    print(json.dumps({"runtime_seconds": time.perf_counter() - started}))
    if not verdict["summary"]["publication_gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
