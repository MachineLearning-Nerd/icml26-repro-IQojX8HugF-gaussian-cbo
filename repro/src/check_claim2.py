"""Independent fail-closed checker for Claim 2 raw CSV evidence."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim2" / "generated"


def load_endpoints() -> dict[str, dict[int, dict[int, dict[str, float]]]]:
    data: dict[str, dict[int, dict[int, dict[str, float]]]] = defaultdict(lambda: defaultdict(dict))
    with (OUT / "claim2_trajectory.csv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            variant = row.pop("variant")
            seed = int(row.pop("seed"))
            step = int(row.pop("step"))
            row.pop("time")
            data[variant][seed][step] = {key: float(value) for key, value in row.items()}
    return data


def log_slopes(seed_rows: dict[int, dict[int, dict[str, float]]]) -> list[float]:
    slopes: list[float] = []
    for rows in seed_rows.values():
        steps = sorted(rows)
        start = len(steps) // 2
        x = np.asarray(steps[start:], dtype=float) * 0.01
        y = np.log(np.maximum([rows[step]["variance"] for step in steps[start:]], 1e-300))
        slopes.append(float(np.polyfit(x, y, 1)[0]))
    return slopes


def main() -> None:
    data = load_endpoints()
    required_variants = {"paper_dynamics", "noise_dominated_control"}
    if set(data) != required_variants:
        raise SystemExit(f"expected variants {required_variants}, found {set(data)}")
    expected_seeds = set(range(260100, 260124))
    if any(set(rows) != expected_seeds for rows in data.values()):
        raise SystemExit("seed set does not match the preregistered 24 seeds")
    if any(set(steps) != set(range(401)) for rows in data.values() for steps in rows.values()):
        raise SystemExit("a raw trajectory is missing one or more of 401 time points")

    main_ratios = np.asarray(
        [steps[400]["variance"] / steps[0]["variance"] for steps in data["paper_dynamics"].values()]
    )
    control_ratios = np.asarray(
        [
            steps[400]["variance"] / steps[0]["variance"]
            for steps in data["noise_dominated_control"].values()
        ]
    )
    main_slopes = np.asarray(log_slopes(data["paper_dynamics"]))
    control_slopes = np.asarray(log_slopes(data["noise_dominated_control"]))
    main_noise = [
        row["noise_rms"]
        for steps in data["paper_dynamics"].values()
        for step, row in steps.items()
        if step < 400
    ]
    main_drift = [
        row["drift_rms"]
        for steps in data["paper_dynamics"].values()
        for step, row in steps.items()
        if step < 400
    ]
    all_values = [
        value
        for variants in data.values()
        for steps in variants.values()
        for row in steps.values()
        for value in row.values()
    ]
    criteria = {
        "complete_and_finite": bool(np.isfinite(all_values).all()),
        "median_variance_ratio_below_0_05": bool(np.median(main_ratios) < 0.05),
        "at_least_90pct_seeds_below_0_05": bool(np.mean(main_ratios < 0.05) >= 0.9),
        "median_log_variance_slope_below_minus_0_5": bool(np.median(main_slopes) < -0.5),
        "deterministic_drift_active": bool(np.max(main_drift) > 0),
        "stochastic_exploration_active": bool(np.max(main_noise) > 0),
    }
    control = {
        "median_variance_ratio_above_1": bool(np.median(control_ratios) > 1.0),
        "median_log_variance_slope_positive": bool(np.median(control_slopes) > 0),
        "would_fail_main_consensus_threshold": bool(not (np.median(control_ratios) < 0.05)),
    }
    summary = json.loads((OUT / "claim2_summary.json").read_text(encoding="utf-8"))
    literal_loop = bool(summary["literal_loop_max_error"] < 1e-12)
    verdict = {
        "verdict": "VERIFIED" if all(criteria.values()) and all(control.values()) and literal_loop else "BLOCKED",
        "criteria": criteria,
        "negative_control": control,
        "literal_loop_matches_vectorized": literal_loop,
        "observed": {
            "median_variance_ratio": float(np.median(main_ratios)),
            "variance_ratio_seed_range": [float(np.min(main_ratios)), float(np.max(main_ratios))],
            "median_log_variance_slope": float(np.median(main_slopes)),
            "log_variance_slope_seed_range": [float(np.min(main_slopes)), float(np.max(main_slopes))],
            "control_median_variance_ratio": float(np.median(control_ratios)),
            "control_median_log_variance_slope": float(np.median(control_slopes)),
        },
        "scope": "Finite d=2 smooth-energy demonstration of the exact multi-step particle recurrence; not a universal convergence proof.",
    }
    (OUT / "claim2_checker.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    (OUT / "claim2_negative_control.json").write_text(
        json.dumps({"config": summary["negative_control_config"], **control}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(verdict, indent=2))
    if verdict["verdict"] != "VERIFIED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
