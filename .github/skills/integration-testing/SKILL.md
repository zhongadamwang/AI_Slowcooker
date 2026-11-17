---
name: integration-testing
description: Verify the EDPS skill suite end to end by running its executable checks - skill frontmatter and links, catalogue and gate ID consistency, gate definition lint, every unit test suite, the alignment validator fixtures - and optionally every completion gate of an archetype against a real project, written as integration-test-report.md/.json. Use after changing any skill, gate, script, or the orchestrator's catalogue; before merging or releasing skill changes; or when the user asks whether the skills still work together or where a project stands across all its gates.
license: MIT
metadata:
  version: 2.0.0
  last-updated: "2026-11-17"
---

# Integration Testing

Run the suite's real checks with one script and report what passed and failed. Do not judge the suite by reading skill files; a check that was not run is not a pass.

## Running it

From the repository root:

```bash
# the suite only
python3 .github/skills/integration-testing/scripts/run_suite.py

# the suite, plus every gate of an archetype against a project, with a written report
python3 .github/skills/integration-testing/scripts/run_suite.py \
    --project "OrgDocument/projects/[NN] - [Project Name]" --archetype standard \
    --report-dir "OrgDocument/projects/[NN] - [Project Name]/artifacts/Testing"
```

Exit code 0 means every suite check passed. Only the Python standard library is needed.

## What it checks

| # | Check | Fails when |
|---|---|---|
| 1 | Skill structure | A `SKILL.md` has no frontmatter, unexpected frontmatter keys, a `name` that differs from its folder, an empty or over-long description, no license, or a broken link to its own `references/`, `scripts/`, `assets/`, or `examples/`; or a skill has no `gate.json` |
| 2 | Catalogue | A skill is missing from the orchestrator's Skill Catalogue, or its gate's `skill_id` differs from the catalogue |
| 3 | Gate definitions | `run_gate.py --lint` reports a problem in any `gate.json` |
| 4 | Test suites | Any `test_*.py` under `.github/skills/` fails |
| 5 | Fixtures | `model-validatealignment`'s fixtures stop matching their expected reports |
| 6 | Project gates (with `--project`) | Reported per skill, in catalogue order. Not counted as suite failures: a project partway through its workflow legitimately fails the gates of skills it has not run yet. Gates that need an orgModel process or boundary folder are listed as not run; run `run_gate.py` for those with `--process` or `--boundary` |

## Reporting

With `--report-dir`, the script writes `integration-test-report.md` and `integration-test-results.json`. Report to the user:

- the suite status and the count of checks passed;
- each failed check with its detail, and which skill or file it points at;
- for a project run, which gates fail and whether that is expected (the skill has not run yet) or a defect (the skill ran and its output does not meet its gate).

When a check fails after a change, fix the cause; do not loosen a gate or skip a test to make the suite pass. If a gate is wrong (it expects something its skill does not document), fix the gate and say so.

## Adding checks

- A new unit test anywhere under `.github/skills/` named `test_*.py` is picked up automatically.
- A new skill is checked automatically once its folder has a `SKILL.md`; add it to the orchestrator's Skill Catalogue with a new ID, and give its `gate.json` the same `skill_id`.

## Integration

**Checks**: every skill, `edps-workflow-orchestrator/scripts/run_gate.py`, `model-validatealignment`'s validator

**Used by**: whoever changes the suite, and `edps-workflow-orchestrator` as the final validation step of the `standard` and `compliance` archetypes
