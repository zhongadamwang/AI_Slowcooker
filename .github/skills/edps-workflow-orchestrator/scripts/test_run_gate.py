"""Tests for run_gate.py: check types, path scopes, severity resolution, and gate outcomes."""

import json
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_gate
from run_gate import evaluate_gate, json_select, lint_gate, run_check


class GateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.project = self.tmp / "project"
        (self.project / "artifacts" / "Analysis").mkdir(parents=True)
        self.ctx = {"repo": self.tmp, "project": self.project, "mode": "traditional"}

    def write(self, rel, content, base=None):
        path = (base or self.project) / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")
        return path

    def status(self, check, **ctx):
        check = {"id": "c", "severity": "hard", **check}
        return run_check(check, {**self.ctx, **ctx})["status"]


class JsonSelectTests(unittest.TestCase):
    DOC = {"a": {"b": 3}, "items": [{"x": 1}, {"x": 2}, {}], "who": {"details": "d"}, "what": {}}

    def test_paths(self):
        self.assertEqual(json_select(self.DOC, "$.a.b"), [3])
        self.assertEqual(json_select(self.DOC, "$.items[*].x"), [1, 2])
        self.assertEqual(json_select(self.DOC, "$.items.length"), [3])
        self.assertEqual(json_select(self.DOC, "$.items[1].x"), [2])
        self.assertEqual(json_select(self.DOC, "$.*.details"), ["d"])
        self.assertEqual(json_select(self.DOC, "$.missing.key"), [])

    def test_unsupported_syntax_is_rejected(self):
        with self.assertRaises(ValueError):
            json_select(self.DOC, "$.items[?(@.x>1)]")


class CheckTypeTests(GateTestCase):
    def test_artifact_existence_supports_globs(self):
        check = {"type": "artifact_existence", "artifacts": ["artifacts/Analysis/report-*.json"]}
        self.assertEqual(self.status(check), "failed")
        self.write("artifacts/Analysis/report-1.json", {})
        self.assertEqual(self.status(check), "passed")

    def test_pattern_must_match_at_least_once_by_default(self):
        self.write("artifacts/Analysis/a.md", "no ids here")
        check = {"type": "content_pattern", "file": "artifacts/Analysis/a.md", "must_contain_pattern": r"R-\d{3}"}
        self.assertEqual(self.status(check), "failed")
        self.write("artifacts/Analysis/a.md", "see R-001")
        self.assertEqual(self.status(check), "passed")
        self.assertEqual(self.status({**check, "min_matches": 2}), "failed")

    def test_content_rules_apply_to_every_file_a_glob_matches(self):
        self.write("tasks/T01-a.md", "## Acceptance Criteria")
        self.write("tasks/T02-b.md", "nothing")
        check = {"type": "content_pattern", "file": "tasks/T*-*.md", "must_contain": ["## Acceptance Criteria"]}
        self.assertEqual(self.status(check), "failed")

    def test_forbidden_text_and_pattern(self):
        self.write("artifacts/Analysis/a.md", "ok\n## UI References\n")
        self.assertEqual(self.status({"type": "content_pattern", "file": "artifacts/Analysis/a.md",
                                      "must_not_contain_pattern": "(?m)^## UI References"}), "failed")
        self.assertEqual(self.status({"type": "content_pattern", "file": "artifacts/Analysis/a.md",
                                      "must_not_contain": ["TODO"]}), "passed")

    def test_content_pattern_with_json_path_checks_each_selected_value(self):
        self.write("m.json", {"use_cases": [{"id": "UC-001"}, {"id": "UC-2"}]})
        check = {"type": "content_pattern", "file": "m.json", "json_path": "$.use_cases[*].id",
                 "must_contain_pattern": r"^UC-\d{3}$"}
        self.assertEqual(self.status(check), "failed")

    def test_missing_file_fails_instead_of_passing(self):
        self.assertEqual(self.status({"type": "content_pattern", "file": "nope.md", "must_contain": ["x"]}), "failed")

    def test_json_schema_required_and_non_empty_fields(self):
        self.write("m.json", {"entries": [{"id": "A", "refs": []}]})
        base = {"type": "json_schema", "file": "m.json", "json_path": "$.entries[*]"}
        self.assertEqual(self.status({**base, "required_fields": ["id", "refs"]}), "passed")
        self.assertEqual(self.status({**base, "required_fields": ["id"], "non_empty_fields": ["refs"]}), "failed")
        self.assertEqual(self.status({**base, "required_fields": ["absent"]}), "failed")

    def test_json_schema_over_an_empty_array_passes_vacuously(self):
        self.write("m.json", {"entries": []})
        self.assertEqual(self.status({"type": "json_schema", "file": "m.json", "json_path": "$.entries[*]",
                                      "required_fields": ["id"]}), "passed")

    def test_json_query_bounds_and_expected_value(self):
        self.write("s.json", {"status": "PASS", "summary": {"critical": 2}})
        self.assertEqual(self.status({"type": "json_query", "file": "s.json", "json_path": "$.status",
                                      "expected_value": "PASS"}), "passed")
        self.assertEqual(self.status({"type": "json_query", "file": "s.json", "json_path": "$.summary.critical",
                                      "max_value": 0}), "failed")
        self.assertEqual(self.status({"type": "threshold", "file": "s.json", "json_path": "$.summary.critical",
                                      "min_value": 1, "max_value": 5}), "passed")
        self.assertEqual(self.status({"type": "json_query", "file": "s.json", "json_path": "$.absent",
                                      "max_value": 0}), "failed")

    def test_field_completeness(self):
        self.write("g.json", {"criteria": [{"metric": "m"}, {"metric": ""}, {}, {"metric": "n"}]})
        check = {"type": "field_completeness", "file": "g.json", "json_path": "$.criteria[*].metric"}
        self.assertEqual(self.status({**check, "min_percent_complete": 50}), "passed")
        self.assertEqual(self.status({**check, "min_percent_complete": 80}), "failed")

    def test_file_content_and_file_count(self):
        self.write("artifacts/Analysis/r.md", "# Requirements\nline\n")
        self.assertEqual(self.status({"type": "file_content", "file": "artifacts/Analysis/r.md", "min_lines": 10,
                                      "must_contain": ["# Requirements"]}), "failed")
        self.write("tasks/T01-a.md", "x")
        self.assertEqual(self.status({"type": "file_count", "pattern": "tasks/T*-*.md", "min_count": 3}), "failed")
        self.assertEqual(self.status({"type": "file_count", "pattern": "tasks/T*-*.md", "min_count": 1,
                                      "max_count": 5}), "passed")

    def test_folder_structure(self):
        (self.project / "tasks").mkdir()
        check = {"type": "folder_structure", "base_path": "{project}", "required_folders": ["artifacts", "tasks"]}
        self.assertEqual(self.status(check), "passed")
        self.assertEqual(self.status({**check, "required_folders": ["artifacts/Source Materials"]}), "failed")
        process = self.tmp / "process"
        (process / "01-OrderBoundary").mkdir(parents=True)
        self.assertEqual(self.status({"type": "folder_structure", "base_path": "{process}",
                                      "folder_pattern": "*-*Boundary/", "min_folders": 1}, process=process), "passed")

    def test_unknown_check_type_fails(self):
        self.assertEqual(self.status({"type": "telepathy"}), "failed")


class ScopeAndConditionTests(GateTestCase):
    def test_scoped_path_without_its_folder_is_skipped_not_passed(self):
        check = {"type": "artifact_existence", "artifacts": ["{boundary}/use-case-model.json"]}
        self.assertEqual(self.status(check), "skipped")
        boundary = self.tmp / "b"
        self.write("use-case-model.json", {}, base=boundary)
        self.assertEqual(self.status(check, boundary=boundary), "passed")

    def test_applies_when_on_a_json_value(self):
        boundary = self.tmp / "b"
        self.write("use-case-model.json", {"boundary_ref": {"boundary_type": "software"}}, base=boundary)
        self.write("ui-model.json", {"entries": [{"entry_id": "UME-001"}]}, base=boundary)
        check = {"type": "json_query", "file": "{boundary}/ui-model.json", "json_path": "$.entries.length",
                 "expected_value": 0,
                 "applies_when": {"file": "{boundary}/use-case-model.json",
                                  "json_path": "$.boundary_ref.boundary_type", "not_equals": "software"}}
        self.assertEqual(self.status(check, boundary=boundary), "not_applicable")
        self.write("use-case-model.json", {"boundary_ref": {"boundary_type": "non-software"}}, base=boundary)
        self.assertEqual(self.status(check, boundary=boundary), "failed")

    def test_applies_when_file_exists(self):
        check = {"type": "content_pattern", "file": "later.md", "must_not_contain": ["bad"],
                 "applies_when": {"file": "later.md", "exists": True}}
        self.assertEqual(self.status(check), "not_applicable")
        self.write("later.md", "bad")
        self.assertEqual(self.status(check), "failed")


class StakeholderConfirmationTests(GateTestCase):
    CHECK = {"id": "c", "type": "stakeholder_confirmation", "role": "Business Owner", "confirmation_statement": "ok"}

    def test_traditional_mode_needs_a_record_and_is_hard(self):
        result = run_check(self.CHECK, self.ctx)
        self.assertEqual((result["status"], result["severity"]), ("failed", "hard"))
        self.write("project-state.json", {"confirmations": [{"role": "business owner", "confirmed_by": "Dana"}]})
        self.assertEqual(run_check(self.CHECK, self.ctx)["status"], "passed")

    def test_solo_mode_self_attests_and_is_soft(self):
        result = run_check(self.CHECK, {**self.ctx, "mode": "solo"})
        self.assertEqual((result["status"], result["severity"]), ("passed", "soft"))


class GateOutcomeTests(GateTestCase):
    """evaluate_gate against a throwaway skills directory."""

    def setUp(self):
        super().setUp()
        self.skills = self.tmp / "skills"
        patcher = unittest.mock.patch.object(run_gate, "SKILLS_DIR", self.skills)
        patcher.start()
        self.addCleanup(patcher.stop)

    def gate(self, checks, archetypes=None):
        gate = {"skill_id": "S99", "skill_name": "demo", "checks": checks,
                "workflow_archetypes": archetypes or {"standard": "hard", "rapid": "soft", "compliance": "hard"}}
        self.write("demo/gate.json", gate, base=self.skills)
        self.write("demo/SKILL.md", "x", base=self.skills)

    HARD = {"id": "h", "type": "artifact_existence", "severity": "hard", "artifacts": ["must-exist.md"]}
    SOFT = {"id": "s", "type": "artifact_existence", "severity": "soft", "artifacts": ["nice-to-have.md"]}

    def test_hard_failure_blocks_in_standard_but_only_warns_where_the_archetype_is_soft(self):
        self.gate([self.HARD])
        self.assertEqual(evaluate_gate("demo", self.ctx, "standard")["status"], "failed")
        rapid = evaluate_gate("demo", self.ctx, "rapid")
        self.assertEqual((rapid["status"], rapid["allowed"]), ("passed_with_warnings", True))

    def test_archetype_marked_hard_cannot_be_softened(self):
        self.gate([self.HARD], {"standard": "hard", "rapid": "hard", "compliance": "hard"})
        for archetype in ("standard", "rapid", "compliance"):
            self.assertFalse(evaluate_gate("demo", self.ctx, archetype)["allowed"])
        self.assertFalse(evaluate_gate("demo", {**self.ctx, "mode": "solo"}, "rapid")["allowed"])

    def test_soft_failure_warns(self):
        self.write("must-exist.md", "x")
        self.gate([self.HARD, self.SOFT])
        result = evaluate_gate("demo", self.ctx)
        self.assertEqual((result["status"], result["quality_score"]), ("passed_with_warnings", 0.5))

    def test_all_passing(self):
        self.write("must-exist.md", "x")
        self.gate([self.HARD])
        self.assertEqual(evaluate_gate("demo", self.ctx)["status"], "passed")

    def test_bypass_archetype(self):
        self.gate([self.HARD], {"standard": "soft", "rapid": "bypass", "compliance": "soft"})
        self.assertEqual(evaluate_gate("demo", self.ctx, "rapid")["status"], "bypassed")

    def test_unevaluated_hard_check_makes_the_gate_incomplete(self):
        self.gate([{**self.HARD, "artifacts": ["{boundary}/x.json"]}])
        result = evaluate_gate("demo", self.ctx)
        self.assertEqual((result["status"], result["allowed"]), ("incomplete", False))

    def test_skill_without_a_gate(self):
        self.assertEqual(evaluate_gate("absent", self.ctx)["status"], "no_gate")

    def test_lint_catches_schema_problems(self):
        self.gate([{"id": "a", "type": "content_pattern", "severity": "hard", "file": "orgModel/*/main.md"},
                   {"id": "a", "type": "json_schema", "severity": "maybe", "file": "x.json"},
                   {"id": "b", "type": "content_pattern", "severity": "hard", "file": "x.md",
                    "must_contain_pattern": "(", "applies_when": "boundary_type != 'software'"}])
        problems = "\n".join(lint_gate("demo"))
        for expected in ("no rule to check", "looks repo-relative", "duplicate check id", "missing ['required_fields']",
                         "severity must be", "does not compile", "applies_when must be an object"):
            self.assertIn(expected, problems)


class RepositoryGatesTests(unittest.TestCase):
    def test_every_skill_has_a_gate_that_lints_clean(self):
        skills = sorted(p.name for p in run_gate.SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())
        self.assertGreater(len(skills), 40)
        for skill in skills:
            with self.subTest(skill=skill):
                self.assertEqual(lint_gate(skill), [])

    def test_gate_skill_ids_are_unique(self):
        ids = [json.loads(p.read_text(encoding="utf-8"))["skill_id"] for p in run_gate.SKILLS_DIR.glob("*/gate.json")]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
