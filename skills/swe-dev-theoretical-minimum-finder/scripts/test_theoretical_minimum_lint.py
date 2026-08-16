from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


LINTER = Path(__file__).with_name("theoretical_minimum_lint.py")


def valid_dossier() -> str:
    return textwrap.dedent(
        """\
        ---
        generator: swe-dev-theoretical-minimum-finder
        artifact_version: 1
        topic: Example field
        target_capability: Diagnose representative system failures
        intended_learner: Practitioner with declared entry knowledge
        entry_assumptions: Basic algebra and domain vocabulary
        generated_at: 2026-08-12
        status: grounded
        scope: One representative problem family
        ---

        # Theoretical Minimum: Example field

        ## Target capability and scope
        ### Target performance
        Diagnose a representative failure and justify the diagnosis. [S01]
        ### Intended learner and entry assumptions
        The learner has the declared entry knowledge.
        ### Scope and exclusions
        One problem family is in scope.
        ### Completion test
        Solve and defend an unseen case.

        ## Minimum at a glance
        The minimum contains one unit. [S01]

        ## Dependency map
        ### Target performances
        Diagnosis depends on [M01].
        ### Load-bearing dependencies
        [M01] has no in-minimum prerequisite.
        ### Hidden prerequisites
        Basic algebra is an entry assumption.
        ### Boundaries
        Advanced optimization is out of scope.

        ## Theoretical minimum
        ### [M01] Governing invariant
        - Own without notes: Reconstruct the invariant and its assumptions.
        - Enables: Diagnose the target failure.
        - Depends on: Declared entry assumptions.
        - Removal failure: The learner cannot distinguish valid from invalid transitions.
        - Non-redundancy: No other retained unit constrains transitions.
        - Regeneration test: Derive the invariant from a blank page.
        - Defense obligation: Explain when the invariant stops applying.
        - Sources: [S01]

        ## Exclusions and deferrals
        Advanced optimization is excluded because the target does not require it. [SYNTHESIS]

        ## Deep structures, invariants, and limits
        The governing invariant constrains valid transitions. [S01]

        ## Minimum source spine
        The primary source grounds [M01]. [S01]

        ## Training sequence
        Regenerate [M01], then apply it to contrasting cases.

        ## Mastery examination
        ### Resource conditions
        Closed book; blank paper is allowed; hints are recorded.
        ### Blank-page regeneration
        Rebuild [M01] and state every assumption.
        ### Unseen and transfer problems
        Apply [M01] to three unfamiliar cases.
        ### Process rubric
        Assess framing and assumptions, representation choice, decomposition and derivation,
        decisive checks and counterexamples, recovery from a dead end, boundary conditions and
        uncertainty, and clarity under questioning.
        ### Oral defenses
        Defend the derivation and its limitations.
        ### Integrated challenge
        Diagnose and defend one unseen failure.
        ### Hint ladder
        Orienting question, relevant principle, then partial structure.

        ## Contradictions and disputed points
        No material dispute was found in the bounded search. [S01]

        ## Unknowns and search gaps
        Broader problem families were not searched.

        ## Claims and evidence ledger
        C01: The invariant constrains the target transition. [S01]

        ## Source Registry
        ### [S01] Example primary source
        - Author / institution: Example institution
        - Date / edition: 2025
        - Tier: 1
        - Type: official-doc
        - URL / identifier: https://example.com/source
        - Accessed: 2026-08-12
        - Verification: content
        - Supports: The governing invariant and target transition.
        - Limitations: Covers only the bounded problem family.

        ## Audit result
        - Provenance integrity: pass
        - Target capability clarity: pass
        - Prerequisite closure: pass
        - Deletion-test strength: pass
        - Core Tier 1-2 coverage: one Tier 1 source
        - Counterevidence search: bounded
        - Mastery-exam validity: pass
        - Link/content verification: content inspected
        - Known hallucination risks removed: none found
        - Remaining uncertainty: broader transfer
        - Structural lint: pass
        """
    ).replace(
        "scope: One representative problem family\n",
        "scope: One representative problem family\n"
        "source_counts:\n"
        "  tier_0: 0\n"
        "  tier_1: 1\n"
        "  tier_2: 0\n"
        "  tier_3: 0\n"
        "  tier_4: 0\n"
        "  tier_5: 0\n"
        "limitations:\n"
        "  - Broader transfer remains uncertain\n",
    )


def run_linter(content: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp_dir:
        artifact = Path(temp_dir) / "minimum.md"
        artifact.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(LINTER), str(artifact)],
            capture_output=True,
            check=False,
            text=True,
        )


class TheoreticalMinimumLintTests(unittest.TestCase):
    def test_accepts_valid_dossier(self) -> None:
        result = run_linter(valid_dossier())

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PASS: no structural errors", result.stdout)

    def test_rejects_previous_generator(self) -> None:
        previous_generator = "swe-dev-" + "cap" + "stone"
        content = valid_dossier().replace(
            "generator: swe-dev-theoretical-minimum-finder",
            f"generator: {previous_generator}",
        )

        result = run_linter(content)

        self.assertEqual(1, result.returncode)
        self.assertIn(
            "frontmatter must contain generator: swe-dev-theoretical-minimum-finder",
            result.stdout,
        )

    def test_requires_dossier_frontmatter_contract(self) -> None:
        required_lines = {
            "artifact_version": "artifact_version: 1\n",
            "topic": "topic: Example field\n",
            "target_capability": "target_capability: Diagnose representative system failures\n",
            "intended_learner": "intended_learner: Practitioner with declared entry knowledge\n",
            "entry_assumptions": "entry_assumptions: Basic algebra and domain vocabulary\n",
            "generated_at": "generated_at: 2026-08-12\n",
            "scope": "scope: One representative problem family\n",
        }

        for field, line in required_lines.items():
            with self.subTest(field=field):
                result = run_linter(valid_dossier().replace(line, ""))

                self.assertEqual(1, result.returncode)
                self.assertIn(f"frontmatter missing required field: {field}", result.stdout)

    def test_requires_source_summary_frontmatter(self) -> None:
        source_counts = (
            "source_counts:\n"
            "  tier_0: 0\n"
            "  tier_1: 1\n"
            "  tier_2: 0\n"
            "  tier_3: 0\n"
            "  tier_4: 0\n"
            "  tier_5: 0\n"
        )
        limitations = "limitations:\n  - Broader transfer remains uncertain\n"

        for field, block in {"source_counts": source_counts, "limitations": limitations}.items():
            with self.subTest(field=field):
                result = run_linter(valid_dossier().replace(block, ""))

                self.assertEqual(1, result.returncode)
                self.assertIn(f"frontmatter missing required field: {field}", result.stdout)

    def test_rejects_inaccurate_source_counts(self) -> None:
        content = valid_dossier().replace("  tier_1: 1\n", "  tier_1: 0\n")

        result = run_linter(content)

        self.assertEqual(1, result.returncode)
        self.assertIn("source_counts tier_1 declares 0 but Source Registry contains 1", result.stdout)

    def test_requires_removal_failure_for_each_unit(self) -> None:
        content = valid_dossier().replace(
            "- Removal failure: The learner cannot distinguish valid from invalid transitions.\n",
            "",
        )

        result = run_linter(content)

        self.assertEqual(1, result.returncode)
        self.assertIn("M01 missing minimum-unit field: Removal failure", result.stdout)

    def test_rejects_unknown_minimum_dependency(self) -> None:
        content = valid_dossier().replace(
            "- Depends on: Declared entry assumptions.",
            "- Depends on: [M99]",
        )

        result = run_linter(content)

        self.assertEqual(1, result.returncode)
        self.assertIn("M01 depends on unknown minimum unit M99", result.stdout)

    def test_requires_deletion_strength_in_self_audit(self) -> None:
        content = valid_dossier().replace("- Deletion-test strength: pass\n", "")

        result = run_linter(content)

        self.assertEqual(1, result.returncode)
        self.assertIn("Audit result missing required field: Deletion-test strength", result.stdout)

    def test_warns_when_blank_page_tasks_do_not_name_a_unit(self) -> None:
        content = valid_dossier().replace(
            "Rebuild [M01] and state every assumption.",
            "Rebuild the core idea and state every assumption.",
        )

        result = run_linter(content)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("M01 has no explicit blank-page regeneration task", result.stdout)

    def test_warns_when_process_rubric_omits_route_quality(self) -> None:
        content = valid_dossier().replace(
            "Assess framing and assumptions, representation choice, decomposition and derivation,\n"
            "decisive checks and counterexamples, recovery from a dead end, boundary conditions and\n"
            "uncertainty, and clarity under questioning.",
            "Assess whether the final answer is correct.",
        )

        result = run_linter(content)

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Process rubric does not mention recovery from dead ends", result.stdout)


if __name__ == "__main__":
    unittest.main()