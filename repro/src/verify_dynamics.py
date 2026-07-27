"""Independent algebra checks for the finite-particle CBO update (Claim 2).

This module intentionally does not import the author's package.  It checks the
three structural ingredients stated in the anchored claim: Boltzmann weights,
deterministic consensus drift, and multiplicative stochastic exploration.
It is a finite algebraic check, not a proof of the paper's mean-field results.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def softmin(energies: np.ndarray, alpha: float) -> np.ndarray:
    shifted = energies - np.min(energies)
    raw = np.exp(-alpha * shifted)
    return raw / raw.sum()


def main() -> None:
    # Deliberately non-tied energies make the exponential preference testable.
    energies = np.array([0.1, 0.4, 0.8, 1.3])
    states = np.array([-2.0, -0.5, 1.0, 3.0])
    alpha, lam, sigma, dt = 3.0, 1.25, 0.7, 0.04
    weights = softmin(energies, alpha)
    consensus = float(weights @ states)
    current = float(states[-1])
    deterministic = current + dt * lam * (consensus - current)

    # Holding the Gaussian increment fixed isolates the stated noise scaling.
    gaussian_increment = -0.6
    noisy = deterministic + np.sqrt(dt) * (consensus - current) * sigma * gaussian_increment
    noiseless = deterministic
    weights_shifted = softmin(energies + 17.0, alpha)

    result = {
        "c2_cbo_dynamics": {
            "normalized_weights": weights.tolist(),
            "weights_sum": float(weights.sum()),
            "lowest_energy_has_largest_weight": bool(weights[0] == weights.max()),
            "energy_shift_invariant_max_error": float(np.max(np.abs(weights - weights_shifted))),
            "consensus": consensus,
            "deterministic_drift_moves_toward_consensus": bool(abs(deterministic - consensus) < abs(current - consensus)),
            "multiplicative_noise_changes_update": bool(abs(noisy - noiseless) > 1e-12),
            "pass": bool(
                np.isclose(weights.sum(), 1.0)
                and weights[0] == weights.max()
                and np.allclose(weights, weights_shifted)
                and abs(deterministic - consensus) < abs(current - consensus)
                and abs(noisy - noiseless) > 1e-12
            ),
        },
        "scope": "Independent finite algebra check; source audit maps these ingredients to Eq. (7)/Algorithm 1.",
    }
    output = Path("outputs/independent_dynamics.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["c2_cbo_dynamics"]["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
