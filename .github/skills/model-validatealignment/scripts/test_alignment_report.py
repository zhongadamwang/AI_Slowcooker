"""Tests for report generation and round/revision staleness tracking (T04).

Complements test_alignment_contract.py (T01's fixture-proving tests, which
remain valid and unchanged) with the additional coverage T04's own
Validation Tests require: deterministic output, revision invalidation, and
report Markdown/JSON rendering.
"""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_validator import (
    BoundaryRef,
    DomainModelDoc,
    ScopedEntityRef,
    UIModelDoc,
    UseCaseModelDoc,
    validate_round,
)
from alignment_report import (
    RoundState,
    is_stale,
    report_to_json,
    report_to_markdown,
    reports_are_identical,
    resolve_round_for_resume,
    write_report,
)


class DeterministicOutputTests(unittest.TestCase):
    """T04 Validation Tests: 'deterministic output' -- same inputs must
    always produce the same report (finding order, finding_id assignment)."""

    def _run_three_level_valid_twice(self):
        boundaries = [
            BoundaryRef("BND-ROOT", "non-software", 0, "root-boundary/", None),
            BoundaryRef("BND-CHILD-SW", "software", 1, "root-boundary/child-software-boundary/", "BND-ROOT"),
        ]
        use_case_models = {
            "BND-CHILD-SW": UseCaseModelDoc(boundary_ref=boundaries[1]),
        }
        results = []
        for _ in range(2):
            report = validate_round(
                round_id="ROUND-DETERMINISM-TEST",
                boundaries=boundaries,
                domain_models={},
                use_case_models=use_case_models,
                ui_models={},
            )
            results.append(report_to_json(
                report, boundaries,
                {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
                generated_at="2026-11-08T00:00:00Z",
            ))
        return results

    def test_identical_inputs_produce_identical_reports(self):
        first, second = self._run_three_level_valid_twice()
        self.assertTrue(reports_are_identical(first, second))
        self.assertEqual(first["status"], second["status"])
        self.assertEqual(
            [f["finding_id"] for f in first["findings"]],
            [f["finding_id"] for f in second["findings"]],
        )

    def test_invalid_input_fixture_is_also_deterministic(self):
        boundaries = [BoundaryRef("BND-BILLING", "software", 0, "billing-boundary/", None)]
        domain_models = {"BND-BILLING": DomainModelDoc("BND-BILLING", {"E-010": "Invoice"})}
        false_claim = ScopedEntityRef(
            entity_id="E-011", entity_name="DiscountCode",
            scope="billing-boundary", defined_in="billing-boundary/domain-model.md",
        )
        use_case_models = {
            "BND-BILLING": UseCaseModelDoc(boundary_ref=boundaries[0], referenced_entities=[false_claim]),
        }
        reports = []
        for _ in range(3):
            report = validate_round(
                round_id="ROUND-DET-002",
                boundaries=boundaries,
                domain_models=domain_models,
                use_case_models=use_case_models,
                ui_models={},
            )
            reports.append(report_to_json(
                report, boundaries,
                {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
                generated_at="2026-11-08T00:00:00Z",
            ))
        self.assertTrue(all(reports_are_identical(reports[0], r) for r in reports[1:]))


class ReportRenderingTests(unittest.TestCase):
    """Proves report_to_json/report_to_markdown actually produce the
    contract Section 4.2 schema, and write_report persists both files."""

    def test_json_schema_has_required_fields(self):
        boundaries = [BoundaryRef("BND-X", "software", 0, "x/", None)]
        report = validate_round(
            round_id="ROUND-SCHEMA-TEST",
            boundaries=boundaries,
            domain_models={},
            use_case_models={"BND-X": UseCaseModelDoc(boundary_ref=boundaries[0])},
            ui_models={},
        )
        rendered = report_to_json(
            report, boundaries,
            {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
        )
        for key in ("round_id", "boundary_scope", "source_model_versions", "status",
                     "findings", "clarification_questions", "generated_at"):
            self.assertIn(key, rendered)
        self.assertEqual(rendered["status"], "PASS")

    def test_markdown_renders_without_error_and_contains_status(self):
        boundaries = [BoundaryRef("BND-UNCLASSIFIED", "unknown", 0, "x/", None)]
        report = validate_round(
            round_id="ROUND-MD-TEST",
            boundaries=boundaries,
            domain_models={},
            use_case_models={"BND-UNCLASSIFIED": UseCaseModelDoc(boundary_ref=boundaries[0])},
            ui_models={},
        )
        rendered = report_to_json(
            report, boundaries,
            {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
        )
        md = report_to_markdown(rendered)
        self.assertIn("NEEDS_CLARIFICATION", md)
        self.assertIn("## Clarification Questions", md)

    def test_write_report_persists_both_files_and_refuses_silent_overwrite(self):
        import tempfile
        boundaries = [BoundaryRef("BND-X", "software", 0, "x/", None)]
        report = validate_round(
            round_id="ROUND-WRITE-TEST",
            boundaries=boundaries,
            domain_models={},
            use_case_models={"BND-X": UseCaseModelDoc(boundary_ref=boundaries[0])},
            ui_models={},
        )
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            md_path, json_path = write_report(
                report, boundaries,
                {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
                out_dir,
            )
            self.assertTrue(md_path.exists())
            self.assertTrue(json_path.exists())

            # Idempotent re-write with identical content: must succeed.
            write_report(
                report, boundaries,
                {"domain_model": "v1", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
                out_dir,
            )

            # Re-write with DIFFERENT content under the SAME round_id: must refuse.
            boundaries_changed = [BoundaryRef("BND-X", "software", 0, "x/", None)]
            different_report = validate_round(
                round_id="ROUND-WRITE-TEST",  # same round_id
                boundaries=boundaries_changed,
                domain_models={},
                use_case_models={},  # now missing -> different status
                ui_models={},
            )
            with self.assertRaises(ValueError):
                write_report(
                    different_report, boundaries_changed,
                    {"domain_model": "v2", "process_model": "v1", "use_case_model": "v1", "ui_model": None},
                    out_dir,
                )


class RevisionInvalidationTests(unittest.TestCase):
    """T04 Validation Tests: 'revision invalidation' -- editing an affected
    model invalidates the previous round's result; resume must check
    versions rather than trust a stale PASS."""

    def test_unchanged_versions_are_not_stale(self):
        prior = RoundState(
            round_id="ROUND-001", status="PASS",
            boundary_scope_ids=["BND-X"],
            source_model_versions={"domain_model": "v1", "use_case_model": "v1"},
        )
        current = {"domain_model": "v1", "use_case_model": "v1"}
        self.assertFalse(is_stale(prior, current))
        self.assertEqual(resolve_round_for_resume(prior, current), "valid")

    def test_edited_model_makes_prior_round_stale(self):
        prior = RoundState(
            round_id="ROUND-001", status="PASS",
            boundary_scope_ids=["BND-X"],
            source_model_versions={"domain_model": "v1", "use_case_model": "v1"},
        )
        # domain_model was edited after the round's report was written.
        current = {"domain_model": "v2", "use_case_model": "v1"}
        self.assertTrue(is_stale(prior, current))
        self.assertEqual(resolve_round_for_resume(prior, current), "stale")

    def test_non_pass_prior_round_is_always_stale_regardless_of_versions(self):
        prior = RoundState(
            round_id="ROUND-002", status="NEEDS_CLARIFICATION",
            boundary_scope_ids=["BND-X"],
            source_model_versions={"domain_model": "v1"},
        )
        # Versions are unchanged, but a non-PASS round can never be
        # "resumed as aligned" -- it was never aligned to begin with.
        current = {"domain_model": "v1"}
        self.assertEqual(resolve_round_for_resume(prior, current), "stale")

    def test_no_prior_round_is_reported_distinctly_from_stale(self):
        current = {"domain_model": "v1"}
        self.assertEqual(resolve_round_for_resume(None, current), "no_prior_round")

    def test_a_skip_or_self_attestation_cannot_fabricate_a_valid_resume(self):
        """Directly proves contract Section 4.4's 'A skip, rapid archetype,
        or solo self-attestation cannot convert inconsistency into
        successful alignment' -- there is no code path in resolve_round_for_resume
        that takes a severity/mode parameter at all; staleness is purely a
        function of recorded vs. current model versions and the prior
        round's actual status."""
        import inspect
        sig = inspect.signature(resolve_round_for_resume)
        param_names = set(sig.parameters.keys())
        self.assertEqual(param_names, {"prior_round", "current_model_versions"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
