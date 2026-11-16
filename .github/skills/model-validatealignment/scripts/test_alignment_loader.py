"""Tests for the file-based path: alignment_loader.py and validate_alignment.py.

test_alignment_contract.py and test_alignment_report.py exercise the decision
logic on in-memory documents. These tests prove the same logic runs against
real boundary folders on disk, including the checks only real files can
trigger (unresolved references, missing scripts, edits after a round).
"""

import filecmp
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from alignment_loader import discover_boundaries, load_round, parse_boundary
from run_fixtures import FIXTURES_DIR, run_fixture, summarize
from validate_alignment import check_stale, main, run_round

SKILLS_DIR = FIXTURES_DIR.parents[1]


def findings(report, needle):
    return [f for f in report["findings"] if needle in f["description"]]


class FixtureFilesTests(unittest.TestCase):
    """Every fixture's real files must reproduce its expected-report.json."""

    def test_every_fixture_matches_its_expected_report(self):
        fixtures = sorted(p for p in FIXTURES_DIR.iterdir() if (p / "expected-report.json").is_file())
        self.assertEqual(len(fixtures), 5)
        for fixture in fixtures:
            with self.subTest(fixture=fixture.name):
                expected = json.loads((fixture / "expected-report.json").read_text(encoding="utf-8"))
                self.assertEqual(summarize(run_fixture(fixture)), summarize(expected))

    def test_three_level_fixture_models_match_the_generator_examples(self):
        # The fixture reuses the use-case and UI models shipped as the two generator
        # skills' worked examples; a copy that drifts would silently test something else.
        root = FIXTURES_DIR / "three-level-valid" / "root-boundary"
        for skill in ("usecase-generatemodel", "ui-generatemodel"):
            example = SKILLS_DIR / skill / "examples" / "three-level-worked-example" / "root-boundary"
            for source in (p for p in example.rglob("*") if p.is_file()):
                with self.subTest(file=str(source.relative_to(example))):
                    self.assertTrue(filecmp.cmp(source, root / source.relative_to(example), shallow=False))

    def test_discovery_lists_parents_before_children(self):
        root = FIXTURES_DIR / "three-level-valid"
        loaded = load_round(discover_boundaries(root), root)
        self.assertEqual([b.boundary_id for b in loaded.boundaries], ["BND-ROOT", "BND-CHILD-SW", "BND-GRANDCHILD"])
        self.assertEqual(loaded.boundaries[1].parent_boundary_id, "BND-ROOT")
        self.assertEqual(loaded.boundaries[2].hierarchy_level, 2)

    def test_same_entity_id_in_two_scopes_is_not_a_conflict(self):
        root = FIXTURES_DIR / "three-level-valid"
        loaded = load_round(discover_boundaries(root), root)
        self.assertIn("E-002", loaded.domain_models["BND-ROOT"].entities)
        self.assertIn("E-002", loaded.domain_models["BND-CHILD-SW"].entities)
        self.assertEqual(run_fixture(root)["status"], "PASS")


class BoundaryParsingTests(unittest.TestCase):
    def parse(self, body):
        with tempfile.TemporaryDirectory() as tmp:
            main_md = Path(tmp) / "main.md"
            main_md.write_text(body, encoding="utf-8")
            return parse_boundary(main_md, "b")

    def test_hierarchy_management_stub_is_unknown(self):
        ref = self.parse("# X — Main\n\n## System Boundary\n\n- **Boundary ID**: `BND-01-X`\n"
                         "- **Boundary Type**: `unknown` — **[ACTION REQUIRED]** confirm whether this boundary is "
                         "`software` or `non-software`, then replace this line.\n")
        self.assertEqual((ref.boundary_id, ref.boundary_type), ("BND-01-X", "unknown"))

    def test_missing_section_is_unknown_not_defaulted(self):
        self.assertEqual(self.parse("# X — Main\n\nNo boundary section here.\n").boundary_type, "unknown")

    def test_prose_instead_of_a_type_is_unknown(self):
        ref = self.parse("# X\n\n## System Boundary\n\n- **Boundary Type**: *(not yet declared)*\n")
        self.assertEqual(ref.boundary_type, "unknown")

    def test_unrecognised_declared_type_is_kept_for_the_validator_to_reject(self):
        ref = self.parse("# X\n\n## System Boundary\n\n- **Boundary ID**: `BND-X`\n- **Boundary Type**: `hybrid`\n")
        self.assertEqual(ref.boundary_type, "hybrid")


class RealFileChecksTests(unittest.TestCase):
    """Each test copies a passing fixture, breaks one thing, and expects it to be reported."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copytree(FIXTURES_DIR / "three-level-valid" / "root-boundary", self.tmp / "root-boundary")
        self.root = self.tmp / "root-boundary"
        self.child = self.root / "child-software-boundary"

    def validate(self):
        return run_round("ROUND-TEST", discover_boundaries(self.tmp), self.tmp)

    def edit_json(self, path, change):
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def test_untouched_copy_passes(self):
        self.assertEqual(self.validate()["status"], "PASS")

    def test_ui_entries_in_a_non_software_boundary_are_an_error(self):
        shutil.copyfile(self.child / "ui-model.json", self.root / "ui-model.json")
        report = self.validate()
        self.assertEqual(report["status"], "INVALID_INPUT")
        self.assertTrue(findings(report, "BND-ROOT is non-software but has 2"))

    def test_ui_entry_citing_an_undefined_entity_is_an_error(self):
        self.edit_json(self.child / "ui-model.json", lambda d: d["entries"][0]["domain_entity_refs"].append("E-999"))
        report = self.validate()
        self.assertEqual(report["status"], "INVALID_INPUT")
        self.assertTrue(findings(report, "UME-001 references entity E-999"))

    def test_ui_entry_citing_an_undefined_use_case_is_an_error(self):
        self.edit_json(self.child / "ui-model.json", lambda d: d["entries"][0].update(source_use_case_refs=["UC-042"]))
        self.assertTrue(findings(self.validate(), "cites use case UC-042"))

    def test_script_citing_another_boundarys_entity_is_an_error(self):
        script = self.child / "use-case-scripts" / "UC-002-update-job-status.md"
        script.write_text(script.read_text(encoding="utf-8") + "\nAlso touches TimeEntry (E-004).\n", encoding="utf-8")
        report = self.validate()
        self.assertEqual(report["status"], "INVALID_INPUT")
        self.assertTrue(findings(report, "references entity E-004"))

    def test_missing_script_file_is_an_error(self):
        (self.child / "use-case-scripts" / "UC-001-schedule-technician.md").unlink()
        self.assertTrue(findings(self.validate(), "which does not exist"))

    def test_ui_references_section_in_a_non_software_script_is_an_error(self):
        script = self.root / "use-case-scripts" / "UC-001-request-field-service.md"
        script.write_text(script.read_text(encoding="utf-8") + "\n## UI References\n- Step 1 → Screen SCR-001\n", encoding="utf-8")
        self.assertTrue(findings(self.validate(), "has a UI References section"))

    def test_use_case_model_disagreeing_with_main_md_is_an_error(self):
        self.edit_json(self.root / "use-case-model.json", lambda d: d["boundary_ref"].update(boundary_type="software"))
        self.assertTrue(findings(self.validate(), "main.md is the authoritative source"))

    def test_unknown_actor_is_an_error(self):
        self.edit_json(self.child / "use-case-model.json", lambda d: d["use_cases"][0].update(primary_actor_ref="A-077"))
        self.assertTrue(findings(self.validate(), "names primary actor A-077"))

    def test_unresolved_marker_needs_clarification_not_pass(self):
        self.edit_json(self.child / "use-case-model.json",
                       lambda d: d["use_cases"][0].update(requirement_refs=["R-204 [UNRESOLVED — see changelog]"]))
        report = self.validate()
        self.assertEqual(report["status"], "NEEDS_CLARIFICATION")

    def test_unparseable_model_file_is_an_error_not_a_crash(self):
        (self.child / "use-case-model.json").write_text("{not json", encoding="utf-8")
        report = self.validate()
        self.assertEqual(report["status"], "INVALID_INPUT")
        self.assertTrue(findings(report, "could not be read"))

    def test_missing_domain_model_is_an_error(self):
        (self.child / "domain-model.md").unlink()
        self.assertTrue(findings(self.validate(), "domain-model.md is required for boundary BND-CHILD-SW"))


class RoundPersistenceTests(unittest.TestCase):
    """A written report records content versions, so a later edit is detected as stale."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copytree(FIXTURES_DIR / "three-level-valid" / "root-boundary", self.tmp / "root-boundary")
        self.out = self.tmp / "artifacts" / "Analysis"
        self.args = ["--round-id", "ROUND-001", "--root", str(self.tmp / "root-boundary"),
                     "--output-dir", str(self.out), "--base-dir", str(self.tmp)]

    def test_cli_writes_report_and_status_pointer(self):
        self.assertEqual(main(self.args), 0)
        status = json.loads((self.out / "alignment-status.json").read_text(encoding="utf-8"))
        self.assertEqual((status["status"], status["latest_round_id"]), ("PASS", "ROUND-001"))
        self.assertTrue((self.out / "alignment-report-ROUND-001.md").is_file())
        report = json.loads((self.out / "alignment-report-ROUND-001.json").read_text(encoding="utf-8"))
        self.assertEqual(set(report["source_model_versions"]), {"BND-ROOT", "BND-CHILD-SW", "BND-GRANDCHILD"})

    def test_report_is_valid_until_a_model_in_scope_is_edited(self):
        main(self.args)
        report = self.out / "alignment-report-ROUND-001.json"
        self.assertEqual(check_stale(report, self.tmp), "valid")
        model = self.tmp / "root-boundary" / "child-software-boundary" / "domain-model.md"
        model.write_text(model.read_text(encoding="utf-8") + "\n### Vehicle *(E-005)*\nA van.\n", encoding="utf-8")
        self.assertEqual(check_stale(report, self.tmp), "stale")
        self.assertEqual(main(["--check-stale", str(report), "--base-dir", str(self.tmp)]), 3)

    def test_editing_a_script_also_makes_the_round_stale(self):
        main(self.args)
        script = self.tmp / "root-boundary" / "use-case-scripts" / "UC-001-request-field-service.md"
        script.write_text(script.read_text(encoding="utf-8") + "\nExtra step.\n", encoding="utf-8")
        self.assertEqual(check_stale(self.out / "alignment-report-ROUND-001.json", self.tmp), "stale")

    def test_non_pass_round_exits_non_zero_and_is_never_valid_on_resume(self):
        (self.tmp / "root-boundary" / "use-case-model.json").unlink()
        self.assertEqual(main(self.args), 2)
        self.assertEqual(check_stale(self.out / "alignment-report-ROUND-001.json", self.tmp), "stale")

    def test_same_round_id_cannot_be_reused_for_a_different_result(self):
        main(self.args)
        (self.tmp / "root-boundary" / "use-case-model.json").unlink()
        self.assertEqual(main(self.args), 64)


if __name__ == "__main__":
    unittest.main(verbosity=2)
