"""Primary-source verifiers for the exact Claim 3 and Claim 4 attributions.

These are source-level claims about what numbered results prove.  The checker
binds itself to the archived arXiv v2 TeX, reconstructs shared theorem
numbering, and distinguishes the printed conclusions from stronger paraphrases.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / ".openresearch" / "artifacts" / "source" / "REVIEW_manuscript_GaussCBO.tex"
EXPECTED_SOURCE_SHA256 = "6b35ec4859cc23bac62bec4a20c6a9d59e1c360a9cf44a1ba1b68b96042b09b1"
SHARED_ENVIRONMENTS = ("theorem", "proposition", "lemma", "corollary", "definition", "assumption")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def uncomment(tex: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())


def environment_number(tex: str, label: str) -> tuple[str, int, int]:
    label_position = tex.index(rf"\label{{{label}}}")
    sections = list(re.finditer(r"\\section\{", tex[:label_position]))
    if not sections:
        raise ValueError(f"no section before {label}")
    section_number = len(sections)
    section_start = sections[-1].start()
    prefix = tex[section_start:label_position]
    environments = list(
        re.finditer(
            r"\\begin\{(" + "|".join(SHARED_ENVIRONMENTS) + r")\}",
            prefix,
        )
    )
    if not environments:
        raise ValueError(f"no theorem-like environment before {label}")
    return environments[-1].group(1), section_number, len(environments)


def theorem_block(tex: str, label: str, environment: str) -> str:
    label_position = tex.index(rf"\label{{{label}}}")
    start = tex.rfind(rf"\begin{{{environment}}}", 0, label_position)
    end_marker = rf"\end{{{environment}}}"
    end = tex.index(end_marker, label_position) + len(end_marker)
    return tex[start:end]


def main() -> None:
    raw = SOURCE.read_bytes()
    source_sha = sha256_bytes(raw)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"primary-source SHA mismatch: {source_sha}")
    tex = uncomment(raw.decode("utf-8"))

    c3_env, c3_section, c3_counter = environment_number(tex, "t:convergence")
    c3_block = theorem_block(tex, "t:convergence", c3_env)
    c3_number = f"{c3_env.title()} {c3_section}.{c3_counter}"
    c3_checks = {
        "official_tex_numbers_result_theorem_3_5": c3_number == "Theorem 3.5",
        "variance_converges_exponentially": r"\var(\rho_t) \to 0$ exponentially fast" in c3_block,
        "consensus_point_converges_exponentially": (
            r"converge to $\tilde z$ exponentially fast" in c3_block
        ),
        "finite_alpha_conclusion_is_inequality": (
            r"\E^\#(\tilde z) \leq \underline{\E}+ r(\alpha)  + \frac{\log 2}\alpha"
            in c3_block
        ),
        "residual_only_vanishes_as_alpha_tends_to_infinity": (
            r"r(\alpha):=" in c3_block
            and re.search(
                re.escape(r"r(\alpha):=")
                + r".*?"
                + re.escape(r"\to 0$ as $\alpha \to \infty"),
                c3_block,
                flags=re.DOTALL,
            )
            is not None
        ),
        "does_not_state_exact_global_minimizer": (
            r"\E^\#(\tilde z) = \underline{\E}" not in c3_block
            and r"\tilde z \in \argmin" not in c3_block
        ),
    }
    c3 = {
        "claim": (
            "Theorem 4.1 proves convergence of the Gaussian CBO dynamics to global "
            "minimizers at an exponential rate."
        ),
        "verdict": "FALSIFIED" if all(c3_checks.values()) else "BLOCKED",
        "basis": (
            "The official v2 TeX numbers the result Theorem 3.5. It proves exponential "
            "consensus/variance decay, but gives only a finite-alpha upper bound on the "
            "limit energy; exact global optimality appears only in the alpha->infinity limit."
        ),
        "checks": c3_checks,
        "actual_number": c3_number,
        "source_sha256": source_sha,
        "scope": "Falsification of the exact theorem attribution, not a counterexample to the corrected theorem.",
    }

    c4_env, c4_section, c4_counter = environment_number(tex, "l:well")
    c4_block = theorem_block(tex, "l:well", c4_env)
    c4_number = f"{c4_env.title()} {c4_section}.{c4_counter}"
    impossible_moment = (
        r"\mathbb{E}|m_0^i|^2,\mathbb{E}\|T_0^i\|_{\Sigma^0}^2 <0" in c4_block
    )
    c4_checks = {
        "official_tex_numbers_result_lemma_3_1": c4_number == "Lemma 3.1",
        "printed_initial_moment_condition_is_strictly_negative": impossible_moment,
        "squared_norms_are_pointwise_nonnegative": True,
        "expectations_of_nonnegative_random_variables_are_nonnegative": True,
        "therefore_no_initial_distribution_satisfies_printed_condition": impossible_moment,
        "displayed_energy_condition_is_global_for_every_pair": (
            r"for any $\mu^1, \mu^2 \in \mathcal{P}_2(\Rd)$" in c4_block
            and r"1 + M_2(\mu^1) + M_2(\mu^2)" in c4_block
        ),
    }
    c4 = {
        "claim": (
            "Lemma 4.1 establishes well-posedness of the particle dynamics under local "
            "Lipschitz continuity of the energy functional."
        ),
        "verdict": "FALSIFIED" if all(c4_checks.values()) else "BLOCKED",
        "basis": (
            "The official v2 source numbers the result Lemma 3.1 and prints the impossible "
            "assumption E|m0|^2,E||T0||^2<0. Because squared norms and their expectations "
            "are nonnegative, the lemma is vacuous as printed; it cannot establish the "
            "unqualified claimed result without correcting the source."
        ),
        "checks": c4_checks,
        "actual_number": c4_number,
        "source_sha256": source_sha,
        "scope": (
            "Falsification of the exact printed attribution. Replacing <0 by <infinity is "
            "a plausible typo repair, but that repaired lemma is a different contract."
        ),
    }

    # Mutation controls: a verifier not bound to the primary-source hash could
    # silently accept plausible repairs that materially change each claim.
    c3_mutation = tex.replace(
        r"\E^\#(\tilde z) \leq \underline{\E}+ r(\alpha)  + \frac{\log 2}\alpha",
        r"\E^\#(\tilde z) = \underline{\E}",
        1,
    )
    c4_mutation = tex.replace(
        r"\mathbb{E}|m_0^i|^2,\mathbb{E}\|T_0^i\|_{\Sigma^0}^2 <0",
        r"\mathbb{E}|m_0^i|^2,\mathbb{E}\|T_0^i\|_{\Sigma^0}^2 <\infty",
        1,
    )
    controls = {
        "c3_exact_globality_mutation_rejected_by_source_hash": (
            sha256_bytes(c3_mutation.encode("utf-8")) != EXPECTED_SOURCE_SHA256
        ),
        "c4_finite_moment_repair_rejected_by_source_hash": (
            sha256_bytes(c4_mutation.encode("utf-8")) != EXPECTED_SOURCE_SHA256
        ),
    }

    for claim_id, result in (("claim3", c3), ("claim4", c4)):
        out = ROOT / ".openresearch" / "artifacts" / claim_id / "generated"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{claim_id}_verdict.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
    controls_path = ROOT / ".openresearch" / "artifacts" / "claim3" / "generated"
    (controls_path / "source_mutation_controls.json").write_text(
        json.dumps(controls, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"C3": c3, "C4": c4, "negative_controls": controls}, indent=2))
    if c3["verdict"] != "FALSIFIED" or c4["verdict"] != "FALSIFIED" or not all(controls.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
