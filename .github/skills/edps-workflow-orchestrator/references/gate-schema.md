# Gate Schema and Evaluation

Every skill has a `gate.json` describing what must be true of its output before the skill counts as complete. `scripts/run_gate.py` is the implementation of everything on this page; if the two disagree, the script is right and this page needs fixing.

## Running a gate

```bash
# from the repository root
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py <skill-name> \
    --project "OrgDocument/projects/[NN] - [Project Name]" \
    [--process "OrgDocument/orgModel/[NN] - [Process Name]"] \
    [--boundary <boundary folder>] [--target <folder>] \
    [--archetype standard|rapid|compliance] [--mode solo|traditional] [--json]

# validate the gate definitions themselves
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py --lint [skill-name ...]
```

Exit code `0` means progression is allowed, `1` means the gate failed, `2` means it could not be fully evaluated. The runner only reads files; it never writes project state.

`--mode` defaults to `collaboration_mode` in the project's `project-metadata.json`, and to `traditional` when that is absent. `--archetype` defaults to `standard`.

## Path scopes

A path in a gate is resolved against one of five folders. A path with no prefix is relative to the project root.

| Prefix | Resolved against | Supplied by |
|---|---|---|
| *(none)* or `{project}/` | Project root (`OrgDocument/projects/[NN] - [Project Name]/`) | `--project` |
| `{process}/` | An orgModel process folder | `--process` |
| `{boundary}/` | One boundary folder (holds `main.md`) | `--boundary` |
| `{target}/` | A folder the skill was asked to produce, e.g. a new skill | `--target` |
| `{repo}/` | Repository root | automatic |

Paths may be globs (`tasks/T*-*.md`). A content check on a glob must hold for every matching file, and at least one file must match.

If a check needs a scope folder that was not supplied, the check is **skipped**, not passed. A skipped hard check makes the whole gate `incomplete`.

## Top-level fields

| Field | Meaning |
|---|---|
| `skill_id` | Must equal the skill's ID in the orchestrator's Skill Catalogue |
| `skill_name` | Must equal the skill's folder name |
| `checks` | The list of checks (below) |
| `workflow_archetypes` | Per archetype: `hard`, `soft`, or `bypass` (see Outcomes) |
| `severity`, `gate_type`, `version`, `description`, `quality_score_weight`, `bypass_allowed` | Descriptive; not used by the runner |

## Check fields common to every type

| Field | Meaning |
|---|---|
| `id` | Unique within the gate |
| `type` | One of the types below |
| `severity` | `hard` or `soft` (not used by `stakeholder_confirmation`) |
| `description`, `remediation` | Shown in the report |
| `applies_when` | Optional condition; when false the check is `not_applicable` |

`applies_when` is an object, never prose:

```json
{ "file": "{boundary}/use-case-model.json", "json_path": "$.boundary_ref.boundary_type", "not_equals": "software" }
{ "file": "{boundary}/ui-model.json", "json_path": "$.entries.length", "equals": 0 }
{ "file": "artifacts/UI Prototype/design-document.md", "exists": true }
```

With a `json_path`, the first selected value is compared using `equals` or `not_equals`; if the file is missing the check is skipped. Without a `json_path`, the condition is whether the file exists.

## Check types

| Type | Required | Optional | Passes when |
|---|---|---|---|
| `artifact_existence` | `artifacts` (list of paths) | | Every path (or glob) matches something |
| `content_pattern` | `file` | `must_contain`, `must_not_contain` (literal strings), `must_contain_pattern`, `must_not_contain_pattern` (regular expressions), `min_matches`, `json_path` | All literal strings are present, no forbidden string or pattern is, and `must_contain_pattern` matches at least `min_matches` times (**default 1**). With `json_path`, the rules are applied to each selected value instead of the whole file |
| `file_content` | `file` | `min_lines`, `must_contain` | The file has at least `min_lines` lines and every literal string |
| `file_count` | `pattern` (glob) | `min_count`, `max_count` | The number of matching files is within bounds |
| `folder_structure` | `base_path` | `required_folders`; `folder_pattern` + `min_folders`; `min_files` + `file_extensions` | Each stated rule holds under `base_path` |
| `json_schema` | `file`, `required_fields` | `json_path`, `non_empty_fields` | Every selected object (the document root by default) has each required field, and each `non_empty_fields` entry is not an empty string, list, or object |
| `json_query` / `threshold` | `file`, `json_path` | `expected_value`, `min_value`, `max_value` | Every selected value satisfies the stated comparisons; selecting nothing fails |
| `field_completeness` | `file`, `json_path` ending in `[*].field`, `min_percent_complete` | | At least that percentage of items have a non-empty `field` |
| `stakeholder_confirmation` | `role`, `confirmation_statement` | | A confirmation for `role` is recorded in `project-state.json` (see below) |

A missing file fails the check. A `json_path` that selects an empty array under `[*]` passes `json_schema`, `content_pattern`, and `field_completeness` vacuously: there is nothing to be wrong.

### Supported `json_path` syntax

`$`, `.key`, `.*`, `[*]`, `[n]`, and a trailing `.length` on an array, object, or string. Nothing else (no filters, no recursive descent).

### Stakeholder confirmation

Confirmations are records in the `confirmations` array of the project's `project-state.json`:

```json
{
  "role": "Business Owner",
  "confirmation_statement": "Success criteria reflect actual business priority",
  "confirmed_by": "self-attestation | <real stakeholder name/identifier>",
  "collaboration_mode": "solo | traditional",
  "timestamp": "2026-10-22T09:00:00Z"
}
```

This is the only mode-aware check type. In `traditional` mode it is hard and fails without a record for the role. In `solo` mode it is soft and passes without a record, reporting that the developer self-attests; the orchestrator should then append the record so the audit trail is complete. No other check type changes with collaboration mode.

## Outcomes

Each check ends as `passed`, `failed`, `skipped`, or `not_applicable`. The gate's status is then:

| Status | When | Progression |
|---|---|---|
| `bypassed` | The gate's `workflow_archetypes` entry for this archetype is `bypass` | Allowed |
| `failed` | A hard check failed and the archetype entry is `hard`; or the archetype is `compliance` and the quality score is below 0.80 | Blocked |
| `incomplete` | A hard check was skipped | Blocked until re-run with the missing scope |
| `passed_with_warnings` | Any check failed without blocking, or the quality score is below the archetype's threshold | Allowed |
| `passed` | Everything evaluated passed | Allowed |

Where a gate's archetype entry is `soft`, hard-check failures are reported as warnings instead of blocking. A gate that must never be softened (for example `model-validatealignment`) sets every archetype to `hard`.

The quality score is passed checks divided by evaluated checks (skipped and not-applicable checks are excluded). The warning threshold is 0.95 for `compliance` and 0.80 otherwise.

## Writing a gate

- Check for what the skill's `SKILL.md` says it produces: the same file names, folders, headings, and JSON keys. A gate that expects something the skill never writes fails on correct output.
- Prefer `json_schema`/`json_query` on the JSON output over regular expressions on its text.
- Run `run_gate.py --lint` after editing; `test_run_gate.py` fails if any gate in the repository does not lint clean.
