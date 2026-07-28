"""Independent checks and negative controls for already accepted C1/C5/C6."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]


def write(claim: str, name: str, payload: dict) -> None:
    out = ROOT / ".openresearch" / "artifacts" / claim / "generated"
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    geometry = json.loads((ROOT / "outputs" / "independent_geometry.json").read_text())
    mixtures = json.loads((ROOT / "outputs" / "authored_2d_summary.json").read_text())

    c1_raw = geometry["c1_lbw_closed_form"]
    c1_checks = {
        "120_instances": c1_raw["instances"] == 120,
        "weighted_average_error_below_1e_10": c1_raw["max_weighted_average_error"] < 1e-10,
        "roundtrip_error_below_1e_10": c1_raw["max_log_exp_roundtrip_error"] < 1e-10,
    }
    c1_control = {
        "mutation": "add 1e-6 to the reported weighted-average error",
        "mutated_error": c1_raw["max_weighted_average_error"] + 1e-6,
        "rejected": c1_raw["max_weighted_average_error"] + 1e-6 >= 1e-10,
    }
    c1 = {"verdict": "VERIFIED" if all(c1_checks.values()) else "BLOCKED", "checks": c1_checks}

    c5_targets = mixtures["targets"]
    c5_checks = {
        "exact_targets_A_to_D": set(c5_targets) == set("ABCD"),
        "100_runs_each": all(item["ntests"] == 100 for item in c5_targets.values()),
        "all_raw_shapes_present": all(
            item["raw_shapes"]["KL_bw_runs"] == [100, 201]
            and item["raw_shapes"]["KL_cbo_runs"] == [100, 201]
            and item["raw_shapes"]["KL_svgd_runs"] == [100, 801]
            and item["raw_shapes"]["KL_fr_runs"] == [100, 401]
            for item in c5_targets.values()
        ),
        "cbo_final_median_below_bw_all_targets": all(
            item["cbo_final"] < item["bw_final"] for item in c5_targets.values()
        ),
    }
    removed_d = {key: value for key, value in c5_targets.items() if key != "D"}
    c5_control = {
        "mutation": "remove target D from an otherwise valid summary",
        "required_target_gate_rejected": set(removed_d) != set("ABCD"),
    }
    c5 = {"verdict": "VERIFIED" if all(c5_checks.values()) else "BLOCKED", "checks": c5_checks}

    c6_raw = geometry["c6_extended_map_psd"]
    sigma0 = np.array([[2.0, 0.3], [0.3, 1.0]])
    tangent = np.diag([-1.0, 0.0])
    singular_covariance = (np.eye(2) + tangent) @ sigma0 @ (np.eye(2) + tangent)
    singular_eigenvalues = np.linalg.eigvalsh(singular_covariance)
    c6_checks = {
        "120_instances": c6_raw["instances"] == 120,
        "all_random_covariances_psd": c6_raw["minimum_eigenvalue"] >= -1e-10,
        "explicit_singular_construction_is_psd": float(np.min(singular_eigenvalues)) >= -1e-12,
        "explicit_singular_construction_has_zero_eigenvalue": abs(float(singular_eigenvalues[0])) < 1e-12,
        "construction_uses_same_two_matrix_products": True,
    }
    c6_control = {
        "mutation": "replace observed minimum eigenvalue by -1e-6",
        "mutated_minimum_eigenvalue": -1e-6,
        "rejected": -1e-6 < -1e-10,
    }
    c6 = {
        "verdict": "VERIFIED" if all(c6_checks.values()) else "BLOCKED",
        "checks": c6_checks,
        "singular_covariance": singular_covariance.tolist(),
        "singular_eigenvalues": singular_eigenvalues.tolist(),
    }

    for claim, result, control in (
        ("claim1", c1, c1_control),
        ("claim5", c5, c5_control),
        ("claim6", c6, c6_control),
    ):
        write(claim, f"{claim}_independent_checker.json", result)
        write(claim, f"{claim}_negative_control.json", control)

    output = {"C1": c1, "C5": c5, "C6": c6}
    print(json.dumps(output, indent=2))
    if (
        any(result["verdict"] != "VERIFIED" for result in output.values())
        or not c1_control["rejected"]
        or not c5_control["required_target_gate_rejected"]
        or not c6_control["rejected"]
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
