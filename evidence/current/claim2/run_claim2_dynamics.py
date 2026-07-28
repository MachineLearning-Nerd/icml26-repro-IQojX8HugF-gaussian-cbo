"""Generate multi-step evidence for the Gaussian CBO particle dynamics.

The simulation is written directly in orthonormal LBW coordinates for d=2.
It implements Eq. (4.2)/(4.3) of arXiv:2601.00632v2 with fixed Gaussian
increments and records every trajectory metric needed by an independent
checker.  It does not import the historical one-step verifier.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".openresearch" / "artifacts" / "claim2" / "generated"
SEEDS = tuple(range(260100, 260124))
SNAPSHOT_STEPS = {0, 50, 100, 200, 400}
SQRT2 = np.sqrt(2.0)


@dataclass(frozen=True)
class Config:
    name: str
    particles: int = 40
    steps: int = 400
    dt: float = 0.01
    alpha: float = 20.0
    lmbda: float = 1.0
    sigma: float = 0.7
    initial_mean_scale: float = 1.2
    initial_tangent_scale: float = 0.18
    apply_update: bool = True


def energy(states: np.ndarray) -> np.ndarray:
    """Smooth quadratic energy in unique LBW coordinates near the identity."""
    target = np.array([1.0, -0.75, 0.12, -0.08, 0.06])
    return 0.5 * np.sum((states - target) ** 2, axis=1)


def stable_weights(values: np.ndarray, alpha: float) -> np.ndarray:
    shifted = values - np.min(values)
    raw = np.exp(-alpha * shifted)
    return raw / np.sum(raw)


def tangent_min_eigenvalue(states: np.ndarray) -> float:
    t11 = states[:, 2]
    t22 = states[:, 3]
    t12 = states[:, 4] / SQRT2
    trace_half = 1.0 + 0.5 * (t11 + t22)
    radius = np.sqrt((0.5 * (t11 - t22)) ** 2 + t12**2)
    return float(np.min(trace_half - radius))


def metrics(
    states: np.ndarray,
    consensus: np.ndarray,
    weights: np.ndarray,
    drift: np.ndarray,
    noise: np.ndarray,
) -> dict[str, float]:
    values = energy(states)
    arithmetic_mean = np.mean(states, axis=0)
    return {
        "variance": float(np.mean(np.sum((states - arithmetic_mean) ** 2, axis=1))),
        "best_energy": float(np.min(values)),
        "weighted_energy": float(np.dot(weights, values)),
        "consensus_energy": float(0.5 * np.sum((consensus - np.array([1.0, -0.75, 0.12, -0.08, 0.06])) ** 2)),
        "max_weight": float(np.max(weights)),
        "drift_rms": float(np.sqrt(np.mean(drift**2))),
        "noise_rms": float(np.sqrt(np.mean(noise**2))),
        "min_transport_eigenvalue": tangent_min_eigenvalue(states),
    }


def literal_step(
    states: np.ndarray,
    consensus: np.ndarray,
    gaussian: np.ndarray,
    config: Config,
) -> np.ndarray:
    result = np.empty_like(states)
    for particle in range(config.particles):
        for coordinate in range(states.shape[1]):
            difference = consensus[coordinate] - states[particle, coordinate]
            result[particle, coordinate] = (
                states[particle, coordinate]
                + config.dt * config.lmbda * difference
                + np.sqrt(config.dt) * config.sigma * difference * gaussian[particle, coordinate]
            )
    return result


def run_variant(
    config: Config,
    metrics_writer: csv.DictWriter,
    snapshots_writer: csv.DictWriter,
) -> tuple[list[float], float]:
    final_ratios: list[float] = []
    max_literal_error = 0.0
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        states = np.empty((config.particles, 5), dtype=np.float64)
        states[:, :2] = rng.normal(scale=config.initial_mean_scale, size=(config.particles, 2))
        states[:, 2:] = rng.normal(scale=config.initial_tangent_scale, size=(config.particles, 3))
        initial_variance = None

        for step in range(config.steps + 1):
            values = energy(states)
            weights = stable_weights(values, config.alpha)
            consensus = weights @ states
            difference = consensus[None, :] - states
            drift = config.dt * config.lmbda * difference
            gaussian = rng.normal(size=states.shape) if step < config.steps else np.zeros_like(states)
            noise = np.sqrt(config.dt) * config.sigma * difference * gaussian
            row_metrics = metrics(states, consensus, weights, drift, noise)
            if initial_variance is None:
                initial_variance = row_metrics["variance"]
            metrics_writer.writerow(
                {
                    "variant": config.name,
                    "seed": seed,
                    "step": step,
                    "time": step * config.dt,
                    **row_metrics,
                }
            )
            if step in SNAPSHOT_STEPS:
                particle_energies = energy(states)
                for particle, state in enumerate(states):
                    snapshots_writer.writerow(
                        {
                            "variant": config.name,
                            "seed": seed,
                            "step": step,
                            "particle": particle,
                            "m1": state[0],
                            "m2": state[1],
                            "t11": state[2],
                            "t22": state[3],
                            "sqrt2_t12": state[4],
                            "energy": particle_energies[particle],
                        }
                    )
            if step == config.steps:
                final_ratios.append(row_metrics["variance"] / initial_variance)
                break
            vectorized = states + drift + noise if config.apply_update else states.copy()
            if config.apply_update and seed == SEEDS[0] and step == 0:
                literal = literal_step(states, consensus, gaussian, config)
                max_literal_error = float(np.max(np.abs(vectorized - literal)))
            states = vectorized
    return final_ratios, max_literal_error


def bootstrap_ci(values: list[float], seed: int = 260100632) -> list[float]:
    array = np.asarray(values)
    rng = np.random.default_rng(seed)
    samples = rng.choice(array, size=(10_000, len(array)), replace=True)
    medians = np.median(samples, axis=1)
    return [float(x) for x in np.quantile(medians, [0.025, 0.975])]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    main_config = Config(name="paper_dynamics")
    control_config = Config(name="frozen_update_control", apply_update=False)
    metrics_path = OUT / "claim2_trajectory.csv"
    snapshots_path = OUT / "claim2_particle_snapshots.csv"
    fields = [
        "variant",
        "seed",
        "step",
        "time",
        "variance",
        "best_energy",
        "weighted_energy",
        "consensus_energy",
        "max_weight",
        "drift_rms",
        "noise_rms",
        "min_transport_eigenvalue",
    ]
    snapshot_fields = [
        "variant",
        "seed",
        "step",
        "particle",
        "m1",
        "m2",
        "t11",
        "t22",
        "sqrt2_t12",
        "energy",
    ]
    with metrics_path.open("w", newline="", encoding="utf-8") as metrics_handle, snapshots_path.open(
        "w", newline="", encoding="utf-8"
    ) as snapshots_handle:
        metrics_writer = csv.DictWriter(metrics_handle, fieldnames=fields)
        snapshots_writer = csv.DictWriter(snapshots_handle, fieldnames=snapshot_fields)
        metrics_writer.writeheader()
        snapshots_writer.writeheader()
        main_ratios, literal_error = run_variant(main_config, metrics_writer, snapshots_writer)
        control_ratios, control_literal_error = run_variant(control_config, metrics_writer, snapshots_writer)

    runtime = time.perf_counter() - started
    summary = {
        "claim": "C2",
        "paper_config": asdict(main_config),
        "negative_control_config": asdict(control_config),
        "seeds": list(SEEDS),
        "literal_loop_max_error": max(literal_error, control_literal_error),
        "paper_dynamics": {
            "median_final_to_initial_variance": float(np.median(main_ratios)),
            "bootstrap_95_ci": bootstrap_ci(main_ratios),
            "fraction_below_0_05": float(np.mean(np.asarray(main_ratios) < 0.05)),
        },
        "frozen_update_control": {
            "median_final_to_initial_variance": float(np.median(control_ratios)),
            "bootstrap_95_ci": bootstrap_ci(control_ratios, seed=260100633),
            "fraction_below_0_05": float(np.mean(np.asarray(control_ratios) < 0.05)),
        },
        "compute": {
            "backend": "recorded_by_orx",
            "estimated_cores": 1,
            "thread_limit": int(os.environ.get("OMP_NUM_THREADS", "1")),
            "visible_logical_cpus": os.cpu_count(),
            "python": platform.python_version(),
            "runtime_seconds": runtime,
        },
        "raw_files": {
            str(metrics_path.relative_to(ROOT)): sha256(metrics_path),
            str(snapshots_path.relative_to(ROOT)): sha256(snapshots_path),
        },
    }
    summary_path = OUT / "claim2_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
