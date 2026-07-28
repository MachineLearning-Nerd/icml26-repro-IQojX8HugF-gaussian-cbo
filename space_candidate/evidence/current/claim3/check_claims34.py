"""Independent fail-closed checker for Claim 3/4 source-verifier outputs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SOURCE_SHA256 = "6b35ec4859cc23bac62bec4a20c6a9d59e1c360a9cf44a1ba1b68b96042b09b1"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    source = ROOT / ".openresearch" / "artifacts" / "source" / "REVIEW_manuscript_GaussCBO.tex"
    observed_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    c3 = read_json(
        ROOT / ".openresearch" / "artifacts" / "claim3" / "generated" / "claim3_verdict.json"
    )
    c4 = read_json(
        ROOT / ".openresearch" / "artifacts" / "claim4" / "generated" / "claim4_verdict.json"
    )
    controls = read_json(
        ROOT
        / ".openresearch"
        / "artifacts"
        / "claim3"
        / "generated"
        / "source_mutation_controls.json"
    )
    checks = {
        "source_hash_matches": observed_sha == EXPECTED_SOURCE_SHA256,
        "c3_is_falsified": c3["verdict"] == "FALSIFIED",
        "c3_actual_number_is_3_5": c3["actual_number"] == "Theorem 3.5",
        "c3_finite_alpha_bound_detected": c3["checks"]["finite_alpha_conclusion_is_inequality"],
        "c3_exact_minimizer_statement_absent": c3["checks"]["does_not_state_exact_global_minimizer"],
        "c4_is_falsified": c4["verdict"] == "FALSIFIED",
        "c4_actual_number_is_3_1": c4["actual_number"] == "Lemma 3.1",
        "c4_impossible_moment_detected": c4["checks"][
            "therefore_no_initial_distribution_satisfies_printed_condition"
        ],
        "mutations_rejected": all(controls.values()),
    }
    output = {
        "verdict": "VERIFIED_CHECKER" if all(checks.values()) else "CHECKER_FAILED",
        "checks": checks,
        "source_sha256": observed_sha,
    }
    for claim_id in ("claim3", "claim4"):
        out = ROOT / ".openresearch" / "artifacts" / claim_id / "generated"
        (out / f"{claim_id}_independent_checker.json").write_text(
            json.dumps(output, indent=2) + "\n", encoding="utf-8"
        )
    print(json.dumps(output, indent=2))
    if output["verdict"] != "VERIFIED_CHECKER":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
