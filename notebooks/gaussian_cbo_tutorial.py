import marimo

__generated_with = "0.23.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import textwrap

    return mo, np, plt, textwrap


@app.cell
def _(mo, textwrap):
    mo.md(
        textwrap.dedent(
            r"""
        # Gaussian CBO: from interacting Gaussians to consensus

        ![Observed consensus trajectories](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/main/reports/gaussian-cbo/images/headline_consensus.png)

        The formal reproduction used **40 Gaussian particles, 400 steps, and
        24 deterministic seeds**. Median final-to-initial particle variance was
        `0.000964` (bootstrap 95% CI `[0.000769, 0.001507]`), while an
        update-omitted control stayed exactly at `1`.

        This notebook explains the mechanism using embedded results. It does
        not rerun the expensive source-scale mixture experiment.
        """
        )
    )
    return


@app.cell
def _(mo):
    alpha = mo.ui.slider(0.0, 30.0, value=10.0, step=0.5, label="inverse temperature α")
    alpha
    return (alpha,)


@app.cell
def _(alpha, mo, np, plt):
    energies = np.array([0.05, 0.25, 0.75, 1.5])
    locations = np.array([-1.8, -0.4, 0.9, 2.0])
    raw = np.exp(-alpha.value * (energies - energies.min()))
    weights = raw / raw.sum()
    consensus = float(weights @ locations)

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.scatter(locations, np.zeros_like(locations), s=700 * weights + 35, c=energies, cmap="viridis_r")
    ax.axvline(consensus, color="#c92a2a", lw=2, label=f"weighted consensus = {consensus:.3f}")
    ax.set(xlabel="one LBW coordinate", yticks=[], title="Lower energy receives exponentially more influence")
    ax.legend(frameon=False)
    ax.grid(axis="x", alpha=0.2)
    mo.vstack(
        [
            mo.md(
                f"`weights = {np.round(weights, 4).tolist()}`  \n"
                f"As α grows, the consensus moves toward the lowest-energy particle."
            ),
            fig,
        ]
    )
    return


@app.cell
def _(mo, textwrap):
    mo.md(
        textwrap.dedent(
            r"""
        ## The update in LBW coordinates

        For particle \(i\), the reproduced Euler–Maruyama step is

        \[
        z_{k+1}^{i}=z_k^i+\lambda\Delta t(\bar z_k-z_k^i)
        +\sigma\sqrt{\Delta t}(\bar z_k-z_k^i)\odot \xi_k^i.
        \]

        The first increment is deterministic exploitation. The second is
        stochastic exploration, scaled by distance from consensus. Both vanish
        when particles agree. A literal nested loop and the vectorized
        implementation matched with maximum error **zero**.

        ![Drift and noise diagnostics](https://raw.githubusercontent.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/main/reports/gaussian-cbo/images/drift_noise_mechanism.png)
        """
        )
    )
    return


@app.cell
def _(mo):
    claim_rows = [
        {"Claim": "C1", "Verdict": "VERIFIED", "Evidence": "120 SPD algebra cases"},
        {"Claim": "C2", "Verdict": "VERIFIED", "Evidence": "24 multi-step trajectories + control"},
        {"Claim": "C3", "Verdict": "FALSIFIED", "Evidence": "finite-α theorem conclusion is weaker"},
        {"Claim": "C4", "Verdict": "FALSIFIED", "Evidence": "printed squared moments are < 0"},
        {"Claim": "C5", "Verdict": "VERIFIED", "Evidence": "100 runs on targets A–D"},
        {"Claim": "C6", "Verdict": "VERIFIED", "Evidence": "PSD identity + 120 cases"},
    ]
    mo.md("## Cumulative assessment")
    mo.ui.table(claim_rows)
    return


@app.cell
def _(mo, textwrap):
    mo.md(
        textwrap.dedent(
            r"""
        ## What the theorem audit changes

        The official Theorem 3.5 proves exponential **consensus** and bounds the
        limit energy at finite α:

        \[
        E^\#(\tilde z)\leq \inf E^\#+r(\alpha)+\log(2)/\alpha.
        \]

        It does not state exact-global exponential convergence at finite α.
        Official Lemma 3.1 also prints an impossible premise: expectations of
        squared norms are strictly negative. The reproduction therefore marks
        those exact attributions FALSIFIED while making no claim against the
        plausibly corrected results.

        Continue with the
        [illustrated report](https://github.com/MachineLearning-Nerd/icml26-repro-IQojX8HugF-gaussian-cbo/blob/main/reports/gaussian-cbo/report.md)
        or inspect the
        [current evaluator logbook](https://huggingface.co/spaces/DineshAI/IQojX8HugF).
        """
        )
    )
    return


if __name__ == "__main__":
    app.run()
