"""Create the report's evidence figures from committed raw artifacts."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
IMAGES = Path(__file__).resolve().parent / "images"
TRAJECTORY = ROOT / ".openresearch" / "artifacts" / "claim2" / "generated" / "claim2_trajectory.csv"
COLORS = {"CBO": "#0b7285", "BW": "#e8590c", "control": "#868e96"}


def load_c2() -> dict[str, dict[int, dict[str, np.ndarray]]]:
    buckets: dict[str, dict[int, dict[str, list[float]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    with TRAJECTORY.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            variant = row["variant"]
            step = int(row["step"])
            for key in ("variance", "drift_rms", "noise_rms"):
                buckets[variant][step][key].append(float(row[key]))
    return {
        variant: {
            step: {key: np.asarray(values) for key, values in metrics.items()}
            for step, metrics in steps.items()
        }
        for variant, steps in buckets.items()
    }


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(IMAGES / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def c2_consensus(data: dict[str, dict[int, dict[str, np.ndarray]]]) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    for variant, label, color in (
        ("paper_dynamics", "Gaussian CBO", COLORS["CBO"]),
        ("frozen_update_control", "frozen-update control", COLORS["control"]),
    ):
        steps = sorted(data[variant])
        raw = np.stack([data[variant][step]["variance"] for step in steps])
        normalized = raw / raw[0]
        median = np.median(normalized, axis=1)
        q1, q3 = np.quantile(normalized, [0.25, 0.75], axis=1)
        time = np.asarray(steps) * 0.01
        ax.plot(time, median, color=color, lw=2.3, label=label)
        ax.fill_between(time, q1, q3, color=color, alpha=0.18)
    ax.axhline(0.05, color="#c92a2a", ls="--", lw=1.2, label="acceptance threshold")
    ax.set_yscale("log")
    ax.set(xlabel="time", ylabel="particle variance / initial variance")
    ax.set_title("Consensus emerges across 24 full trajectories")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    save(fig, "headline_consensus.png")


def c2_seed_ratios(data: dict[str, dict[int, dict[str, np.ndarray]]]) -> None:
    main = data["paper_dynamics"]
    control = data["frozen_update_control"]
    ratios = main[400]["variance"] / main[0]["variance"]
    control_ratios = control[400]["variance"] / control[0]["variance"]
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    x = np.arange(len(ratios))
    ax.scatter(x, ratios, color=COLORS["CBO"], s=34, label="Gaussian CBO")
    ax.scatter(x, control_ratios, color=COLORS["control"], marker="x", s=35, label="control")
    ax.axhline(0.05, color="#c92a2a", ls="--", lw=1.2)
    ax.set_yscale("log")
    ax.set(xlabel="seed index", ylabel="final / initial variance")
    ax.set_title("Every preregistered seed passes; the control fails")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    save(fig, "seed_robustness.png")


def c2_mechanism(data: dict[str, dict[int, dict[str, np.ndarray]]]) -> None:
    main = data["paper_dynamics"]
    steps = sorted(main)[:-1]
    time = np.asarray(steps) * 0.01
    drift = np.asarray([np.median(main[step]["drift_rms"]) for step in steps])
    noise = np.asarray([np.median(main[step]["noise_rms"]) for step in steps])
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    ax.plot(time, drift, lw=2.2, color="#5f3dc4", label="deterministic drift RMS")
    ax.plot(time, noise, lw=2.2, color="#f08c00", label="stochastic increment RMS")
    ax.set_yscale("log")
    ax.set(xlabel="time", ylabel="median coordinate RMS")
    ax.set_title("Both named mechanisms are active, then decay with consensus")
    ax.grid(alpha=0.22)
    ax.legend(frameon=False)
    save(fig, "drift_noise_mechanism.png")


def c5_medians() -> None:
    targets = list("ABCD")
    cbo, bw = [], []
    for target in targets:
        with np.load(ROOT / "outputs" / f"authored_2d_{target}.raw.npz") as data:
            cbo.append(float(np.median(data["KL_cbo_runs"][:, -1])))
            bw.append(float(np.median(data["KL_bw_runs"][:, -1])))
    x = np.arange(len(targets))
    width = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 4.5))
    ax.bar(x - width / 2, cbo, width, color=COLORS["CBO"], label="CBO")
    ax.bar(x + width / 2, bw, width, color=COLORS["BW"], label="BW gradient flow")
    ax.axhline(0, color="black", lw=0.7)
    ax.set_xticks(x, targets)
    ax.set(xlabel="2D mixture target", ylabel="final median KL estimate")
    ax.set_title("Released 100-run protocol: CBO is lower on A–D")
    ax.grid(axis="y", alpha=0.22)
    ax.legend(frameon=False)
    save(fig, "mixture_final_medians.png")


def c5_distributions() -> None:
    targets = list("ABCD")
    positions, values, colors = [], [], []
    for index, target in enumerate(targets):
        with np.load(ROOT / "outputs" / f"authored_2d_{target}.raw.npz") as data:
            values.extend([data["KL_cbo_runs"][:, -1], data["KL_bw_runs"][:, -1]])
        positions.extend([index * 3.0, index * 3.0 + 1.0])
        colors.extend([COLORS["CBO"], COLORS["BW"]])
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    artists = ax.boxplot(values, positions=positions, widths=0.72, patch_artist=True, showfliers=False)
    for box, color in zip(artists["boxes"], colors, strict=True):
        box.set_facecolor(color)
        box.set_alpha(0.72)
    ax.set_xticks([index * 3.0 + 0.5 for index in range(4)], targets)
    ax.set(xlabel="target (CBO left, BW right)", ylabel="final KL estimate")
    ax.set_title("Endpoint distributions across all 100 repetitions")
    ax.grid(axis="y", alpha=0.22)
    save(fig, "mixture_endpoint_distributions.png")


def main() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10.5, "axes.spines.top": False, "axes.spines.right": False})
    data = load_c2()
    c2_consensus(data)
    c2_seed_ratios(data)
    c2_mechanism(data)
    c5_medians()
    c5_distributions()
    for path in sorted(IMAGES.glob("*.png")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
