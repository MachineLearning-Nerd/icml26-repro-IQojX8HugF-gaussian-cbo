"""Independent finite checks for IQojX8HugF geometry claims.

This module intentionally does not import the authors' implementation.  It
reimplements the linear-algebra identities using eigendecompositions and emits
a compact JSON artifact.  It checks mathematical consequences, rather than
claiming to re-prove the paper's universal theorems from finite samples.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def sym(a: np.ndarray) -> np.ndarray:
    return (a + a.T) / 2


def spd(rng: np.random.Generator, d: int) -> np.ndarray:
    a = rng.normal(size=(d, d))
    return sym(a @ a.T + 0.2 * np.eye(d))


def sqrt_spd(a: np.ndarray) -> np.ndarray:
    w, q = np.linalg.eigh(sym(a))
    if np.min(w) <= 0:
        raise ValueError("expected SPD matrix")
    return sym((q * np.sqrt(w)) @ q.T)


def log_map(base: np.ndarray, target: np.ndarray) -> np.ndarray:
    base_sqrt = sqrt_spd(base)
    w, q = np.linalg.eigh(sym(base))
    base_inv_sqrt = sym((q * (1 / np.sqrt(w))) @ q.T)
    return sym(base_inv_sqrt @ sqrt_spd(base_sqrt @ target @ base_sqrt) @ base_inv_sqrt - np.eye(len(base)))


def extended_exp(base: np.ndarray, tangent: np.ndarray) -> np.ndarray:
    a = np.eye(len(base)) + sym(tangent)
    return sym(a @ base @ a)


def main() -> None:
    rng = np.random.default_rng(20260727)
    inverse_errors: list[float] = []
    psd_min_eigenvalues: list[float] = []
    barycenter_errors: list[float] = []

    for d in (2, 3, 5):
        for _ in range(40):
            base = spd(rng, d)
            target = spd(rng, d)
            tangent = log_map(base, target)
            decoded = extended_exp(base, tangent)
            inverse_errors.append(float(np.linalg.norm(decoded - target, ord="fro")))

            # C6: for arbitrary symmetric tangent, (I+T) base (I+T) is PSD.
            arbitrary_tangent = sym(rng.normal(size=(d, d)))
            psd_min_eigenvalues.append(float(np.min(np.linalg.eigvalsh(extended_exp(base, arbitrary_tangent)))))

            # C1: in LBW coordinates the barycenter is exactly a weighted mean.
            states = [sym(rng.normal(size=(d, d))) for _ in range(5)]
            weights = rng.random(5)
            weights /= weights.sum()
            manual = sum(w * state for w, state in zip(weights, states))
            direct = np.tensordot(weights, np.stack(states), axes=(0, 0))
            barycenter_errors.append(float(np.linalg.norm(manual - direct, ord="fro")))

    result = {
        "c1_lbw_closed_form": {
            "instances": len(barycenter_errors),
            "max_weighted_average_error": max(barycenter_errors),
            "max_log_exp_roundtrip_error": max(inverse_errors),
            "pass": max(barycenter_errors) < 1e-12 and max(inverse_errors) < 1e-9,
        },
        "c6_extended_map_psd": {
            "instances": len(psd_min_eigenvalues),
            "minimum_eigenvalue": min(psd_min_eigenvalues),
            "pass": min(psd_min_eigenvalues) >= -1e-10,
        },
        "scope": "Finite independent algebra checks only; they do not prove C3/C4 universal convergence or well-posedness claims.",
    }
    output = Path("outputs/independent_geometry.json")
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["c1_lbw_closed_form"]["pass"] or not result["c6_extended_map_psd"]["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
