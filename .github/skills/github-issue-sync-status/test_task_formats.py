"""Both GitHub scripts must read the project task template ('**Status**: In Progress')
and the older GitHub-issue format ('**State:** in-progress'), and write status back
in the file's own format. Runs offline: the requests module is stubbed.

Run: python3 test_task_formats.py
"""

import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path

sys.modules.setdefault("requests", types.ModuleType("requests"))
SKILLS = Path(__file__).resolve().parents[1]


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, SKILLS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


create = load("github-issue-create-update/create_update_issues.py", "create_update_issues")
sync = load("github-issue-sync-status/sync_status.py", "sync_status")

TEMPLATE_TASK = """# T09 - Build thing

**Task ID**: T09
**Priority**: P1-High
**Estimated Effort**: 2 person-days
**Status**: In Progress
**Assigned**: Unassigned

## Acceptance Criteria
- [ ] Works
"""

GITHUB_TASK = """# Issue: T10 - Other thing
**State:** in-progress
**Labels:** feature, mvp
**Assignees:** octocat
**Priority:** Medium
"""


class FieldParsingTests(unittest.TestCase):
    def test_both_field_styles_are_read(self):
        for module in (create, sync):
            self.assertEqual(module.read_field(TEMPLATE_TASK, "Status"), "In Progress")
            self.assertEqual(module.read_field(GITHUB_TASK, "State"), "in-progress")
            self.assertIsNone(module.read_field(TEMPLATE_TASK, "State"))

    def test_status_values_normalize(self):
        cases = {"Not Started": "ready", "In Progress": "in-progress", "⛔ Blocked": "blocked",
                 "Completed ✅": "completed", "✅ Completed": "completed", "done": "completed", "": "ready"}
        for value, expected in cases.items():
            self.assertEqual(create.normalize_state(value, "ready"), expected, value)


class CreateParsingTests(unittest.TestCase):
    def setUp(self):
        cls = next(v for v in vars(create).values() if isinstance(v, type) and hasattr(v, "parse_task_file"))
        self.creator = cls.__new__(cls)
        self.creator.config = types.SimpleNamespace(
            state_mapping={"ready": "open", "blocked": "open", "in-progress": "open", "completed": "closed", "cancelled": "closed"},
            priority_labels={p: {"name": f"priority:{p.lower()}"} for p in ("High", "Medium", "Low")},
            additional_labels=[], default_assignee=None)

    def parse(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "T.md"
            path.write_text(text, encoding="utf-8")
            return self.creator.parse_task_file(str(path))

    def test_template_task(self):
        data = self.parse(TEMPLATE_TASK)
        self.assertEqual(data["state"], "open")
        self.assertEqual(data["labels"], ["priority:high"])
        self.assertEqual(data["assignees"], [])

    def test_github_task(self):
        data = self.parse(GITHUB_TASK)
        self.assertEqual(sorted(data["labels"]), ["feature", "mvp", "priority:medium"])
        self.assertEqual(data["assignees"], ["octocat"])


class SyncWriteBackTests(unittest.TestCase):
    def setUp(self):
        cls = next(v for v in vars(sync).values() if isinstance(v, type) and hasattr(v, "update_task_file_status"))
        self.syncer = cls.__new__(cls)
        self.syncer.config = types.SimpleNamespace(dry_run=False, add_completion_date=True)

    def complete(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "T.md"
            path.write_text(text, encoding="utf-8")
            data = self.syncer.parse_task_file(path)
            self.syncer.update_task_file_status(data, "completed", {"state": "closed"})
            return data, path.read_text(encoding="utf-8")

    def test_template_format_is_preserved(self):
        data, text = self.complete(TEMPLATE_TASK)
        self.assertEqual(data["current_state"], "in-progress")
        self.assertIn("**Status**: Completed\n**Completed**: ", text)
        self.assertNotIn("**State:**", text)

    def test_github_format_is_preserved(self):
        _, text = self.complete(GITHUB_TASK)
        self.assertIn("**State:** completed\n**Completed Date:** ", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
