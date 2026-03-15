```skill
---
name: edps-compliance
description: Validate EDPS (Evolutionary Development Process System) methodology compliance across process hierarchies. Checks evolutionary decomposition patterns, boundary validation rules (VR-1 through VR-4), requirements traceability at each hierarchy level, change history metadata, and incremental model refinement adherence. Generates item-level pass/fail compliance reports in both JSON and Markdown formats. Use when a user wants to validate EDPS compliance, check hierarchy conformance, generate a compliance report, or get remediation suggestions for violations.
---

# EDPS Compliance Checking

Validate that process hierarchy artifacts conform to EDPS methodology principles and generate a scored compliance report with remediation guidance.

## Inputs

- **Target scope**: one of:
  - Single diagram: `[process-folder]/collaboration.md`
  - Full hierarchy: `[process-folder]/` (recursively includes all sub-process folders)
  - Entire org model: `orgModel/` root
- **Optional**: `[process-folder]/hierarchy-metadata.json` — hierarchy metadata produced by `hierarchy-management`
- **Optional**: `[process-folder]/hierarchy-index.md` — cross-reference index produced by `hierarchy-management`
- **Optional**: `--mode strict | relaxed` (default: `relaxed`)

## Outputs

- `[target-folder]/artifacts/Testing/edps-compliance-report.json` — machine-readable per-rule results
- `[target-folder]/artifacts/Testing/edps-compliance-report.md` — human-readable scored report with remediation suggestions
- Console summary: overall score, violation count by severity, and next recommended action

---

## Compliance Rule Catalogue

### Group A — Boundary Diagram Rules (inherited from `diagram-generatecollaboration`)

| ID | Name | Severity | Description |
|----|------|----------|-------------|
| VR-1 | Single External Interface | ERROR | Each `box` boundary must have exactly one external `actor` communicating directly into it. Multiple actors must route through a shared gateway. |
| VR-2 | Boundary-First Reception | ERROR | The first message from an external actor inside any `box` must target a `boundary`-type participant. Actors must not bypass the entry point. |
| VR-3 | Control-Only Decomposition | ERROR | Only `control`-type participants are eligible for sub-process decomposition. Decomposing `actor`, `boundary`, or `entity` types is prohibited. |
| VR-4 | Cohesive Responsibility | WARNING | All participants within the same `box` boundary must share a cohesive functional domain. Mixed concerns trigger a warning. |

### Group B — Hierarchy Structural Rules

| ID | Name | Severity | Description |
|----|------|----------|-------------|
| HR-1 | Parent-Child Link Integrity | ERROR | Every sub-process folder must have a valid `**Parent Process**` link in its `main.md` that resolves to an existing parent `main.md`. |
| HR-2 | Decomposed Participant Exists | ERROR | Every sub-process folder must correspond to a `control`-type participant that exists in the parent `collaboration.md`. |
| HR-3 | Breadcrumb Consistency | WARNING | The breadcrumb trail in each `main.md` must correctly enumerate all ancestor levels with working relative links. |
| HR-4 | Sub-Processes Section Populated | WARNING | The parent `main.md` **Sub-Processes** section must list all child sub-process folders with valid links. |
| HR-5 | Folder Naming Convention | ERROR | Sub-process folder names must match the pattern `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`. |
| HR-6 | Metadata Currency | WARNING | `hierarchy-metadata.json` must exist at the root scope level and its `last_updated` timestamp must be more recent than any `collaboration.md` modification time within the hierarchy. |

### Group C — EDPS Evolutionary Principles

| ID | Name | Severity | Description |
|----|------|----------|-------------|
| EP-1 | Traceability Presence | ERROR | Each hierarchy level (each `collaboration.md`) must contain at least one requirements traceability reference — either a `[R-NNN]` inline citation or a `**Source Requirements**` frontmatter block. |
| EP-2 | Abstraction Level Separation | ERROR | A `collaboration.md` must not mix concerns from different hierarchy levels. Participants from child boundary folders must not appear directly in a parent diagram. |
| EP-3 | Evolution Metadata | WARNING | Each `main.md` should include a `**Status**` field (`Active`, `Draft`, `Deprecated`) and a `**Last Updated**` or equivalent timestamp comment (`<!-- Last Updated: ... -->`). |
| EP-4 | Incremental Refinement Traceability | WARNING | When a sub-process folder exists, the parent `collaboration.md` should contain a `%% decomposed: [ParticipantName] → [NN]-[ParticipantName]Boundary/collaboration.md` comment annotating the decomposition. |

---

## Workflow

### Step 1 — Discover Scope

1. Determine whether it is a single-file, folder, or full `orgModel/` scan.
2. Collect all `collaboration.md` files within scope.
3. For each file, determine its hierarchy level by counting the depth from the `orgModel/` root (Level 0 = root, Level 1 = direct children, etc.).
4. Locate `hierarchy-metadata.json` at the nearest ancestor level (if present).

### Step 2 — Apply Group A Rules (per `collaboration.md`)

For each `collaboration.md`:

#### VR-1 Check
- Parse `box … end` blocks from the Mermaid `sequenceDiagram`.
- For each box, identify participants declared outside all box blocks (external actor candidates).
- Identify which external participants send messages to participants inside this box.
- **FAIL** if more than one distinct external participant sends directly to inside-box participants without a shared gateway.

#### VR-2 Check
- For each box, find the first message received by any participant inside the box from an external actor.
- Inspect the receiving participant's `@{ "type": "..." }` annotation.
- **FAIL** if the receiving type is not `boundary`.

#### VR-3 Check
- Scan for sub-process sub-folders corresponding to participants in this diagram.
- For each decomposed participant, verify its `@{ "type": "..." }` is `control`.
- **FAIL** if a non-`control` participant has a corresponding sub-folder.

#### VR-4 Check
- Extract participant labels within each box.
- Apply simple cohesion heuristic: if participant labels span clearly unrelated functional domains (e.g., "UserAuthService" and "InventoryCache" in the same boundary), emit a WARNING.
- Use keyword clustering: group by common domain nouns in the label. If the top cluster covers < 60 % of participants, flag as low-cohesion.

### Step 3 — Apply Group B Rules (per folder/hierarchy)

#### HR-1 Check
- Read `**Parent Process**` link from each sub-process `main.md`.
- Resolve the relative path and verify the target `main.md` exists.

#### HR-2 Check
- Read the parent `collaboration.md` and extract all `control`-type participants.
- Compare against sub-process folder names (strip ordinal prefix and `Boundary` suffix, compare case-insensitively with PascalCase normalization).
- **FAIL** if a sub-folder exists that cannot be matched to any `control`-type participant.

#### HR-3 Check
- Parse the breadcrumb line from each `main.md`.
- Resolve each linked path; verify each target `main.md` exists.
- **WARNING** on any broken relative link.

#### HR-4 Check
- Read the parent `main.md` **Sub-Processes** section.
- Compare the listed child links against actual sub-folders.
- **WARNING** if any sub-folder is missing from the section.

#### HR-5 Check
- For each sub-process folder name, apply the regex `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`.
- **FAIL** on any non-conforming name.

#### HR-6 Check
- Locate `hierarchy-metadata.json`.
- **WARNING** if absent.
- If present, compare `last_updated` against the modification time heuristic (use the latest `<!-- Last Updated: -->` comment found across all `collaboration.md` files within scope, or the most recent file mtime reported by file listing).

### Step 4 — Apply Group C Rules (per level)

#### EP-1 Check
- Scan each `collaboration.md` for `[R-` citation patterns or a `**Source Requirements**:` line.
- **FAIL** if none found.

#### EP-2 Check
- Build a participant name set for each hierarchy level.
- **FAIL** if any participant name in a parent `collaboration.md` matches the name of a boundary sub-folder at a child level (indicating direct leakage of child-level participants into the parent).

#### EP-3 Check
- Scan each `main.md` for `**Status**:` and either `**Last Updated**:` or `<!-- Last Updated:`.
- **WARNING** if either is absent.

#### EP-4 Check
- For each decomposed participant in a `collaboration.md`, check that a `%% decomposed:` annotation exists on or near the participant declaration line.
- **WARNING** if absent.

### Step 5 — Score and Aggregate

```
compliance_score = (passed_checks / total_checks) × 100

severity_counts:
  errors   = count of FAIL results on ERROR-severity rules
  warnings = count of FAIL results on WARNING-severity rules

overall_status:
  COMPLIANT     → errors = 0 and compliance_score ≥ 90
  MOSTLY_COMPLIANT → errors = 0 and compliance_score ≥ 70
  NEEDS_ATTENTION  → errors > 0 and errors ≤ 3
  NON_COMPLIANT    → errors > 3
```

### Step 6 — Generate Reports

#### JSON Report (`edps-compliance-report.json`)

```json
{
  "report_metadata": {
    "generated": "ISO8601 timestamp",
    "scope": "path to target folder or file",
    "mode": "strict | relaxed",
    "schema_version": "1.0"
  },
  "summary": {
    "overall_status": "COMPLIANT | MOSTLY_COMPLIANT | NEEDS_ATTENTION | NON_COMPLIANT",
    "compliance_score": 0.0,
    "total_checks": 0,
    "passed": 0,
    "failed_errors": 0,
    "failed_warnings": 0,
    "levels_scanned": 0,
    "diagrams_scanned": 0
  },
  "rule_results": [
    {
      "rule_id": "VR-1",
      "rule_name": "Single External Interface",
      "group": "A",
      "severity": "ERROR",
      "status": "PASS | FAIL | SKIPPED",
      "checked_files": ["path/to/collaboration.md"],
      "violations": [
        {
          "file": "path/to/collaboration.md",
          "location": "box OrderService boundary, line ~42",
          "detail": "Two external actors (UserPortal, AdminConsole) send directly to OrderService boundary without a shared gateway",
          "remediation": "Introduce a gateway control-type participant outside the box to route messages from both actors, then have only the gateway enter the boundary."
        }
      ]
    }
  ],
  "trend": {
    "previous_score": null,
    "delta": null,
    "note": "No previous report found for trend comparison."
  }
}
```

#### Markdown Report (`edps-compliance-report.md`)

```markdown
# EDPS Compliance Report

**Generated**: [timestamp]  
**Scope**: [target path]  
**Mode**: [strict | relaxed]  
**Overall Status**: [status badge]

## Summary

| Metric | Value |
|--------|-------|
| Compliance Score | [score]% |
| Total Checks | [n] |
| Passed | [n] |
| Errors (blocking) | [n] |
| Warnings | [n] |
| Levels Scanned | [n] |
| Diagrams Scanned | [n] |

## Rule Results

### Group A — Boundary Diagram Rules

| Rule | Status | Violations |
|------|--------|------------|
| VR-1 Single External Interface | ✅ PASS / ❌ FAIL / ⚠️ WARN | [n] |
...

## Violations Detail

### ❌ [Rule ID]: [Rule Name]

**File**: `path/to/collaboration.md`  
**Location**: [description of location in file]  
**Issue**: [specific description of the violation]  
**Remediation**: [concrete fix instruction]

---

## Remediation Priority

1. **Critical (Errors)**: Fix all ERROR violations before proceeding — these indicate structural violations of EDPS principles.
2. **Advisory (Warnings)**: Address WARNING violations to improve methodology alignment and documentation quality.

## Trend

[Score delta vs. previous report, or "No previous report found."]
```

---

## Strict vs. Relaxed Mode

| Behaviour | Strict | Relaxed (default) |
|-----------|--------|-------------------|
| WARNING violations block `COMPLIANT` status | Yes | No |
| EP-3 and EP-4 missing metadata treated as | ERROR | WARNING |
| VR-4 cohesion heuristic threshold | 70 % | 60 % |
| HR-6 missing metadata treated as | ERROR | WARNING |
| Report generated even when errors exist | No — exits with error summary first | Yes |

---

## Remediation Suggestions Reference

| Rule | Common Fix |
|------|-----------|
| VR-1 | Introduce a gateway `control`-type participant outside the `box` to funnel multiple actors into a single entry point |
| VR-2 | Reorder the first message inside the `box` so an external actor's first target is always a `boundary`-type participant |
| VR-3 | Remove the sub-folder for the non-`control` participant, or reclassify the participant type to `control` in the parent diagram |
| VR-4 | Split participants with unrelated domains into separate `box` boundaries |
| HR-1 | Re-add the `**Parent Process**` link in `main.md` and correct the relative path |
| HR-2 | Rename or remove the orphaned sub-folder, or add the missing `control`-type participant to the parent diagram |
| HR-3 | Regenerate breadcrumb using `hierarchy-management` (cross-reference rebuild command) |
| HR-4 | Run `hierarchy-management` Sub-Processes table update for the parent `main.md` |
| HR-5 | Rename the folder to conform to `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$` and update all references |
| HR-6 | Run any `hierarchy-management` decomposition or statistics command to regenerate `hierarchy-metadata.json` |
| EP-1 | Add `**Source Requirements**: [R-NNN]` to the diagram header or inline `[R-NNN]` citations in the diagram description |
| EP-2 | Remove child-level participant declarations from the parent diagram; reference the boundary as a single black-box participant |
| EP-3 | Add `**Status**: Active` and `<!-- Last Updated: YYYY-MM-DD -->` to the `main.md` header |
| EP-4 | Add `%% decomposed: [ParticipantName] → [NN]-[ParticipantName]Boundary/collaboration.md` after the participant declaration in the parent `collaboration.md` |

---

## Integration with Other Skills

- Run **after** `hierarchy-management` has generated or updated a hierarchy to validate its output.
- Run **before** `integration-testing` to ensure EDPS structure is sound before full test execution.
- Violations reported by `edps-compliance` inform `change-management` entries when structural changes are required to remediate.
- The compliance score trends feed into `project-status-reporting` health metrics.
```
