# T21: Resolve C-4 — Impact Analysis Risk Scale Normalization

**Task ID**: T21  
**Phase**: Phase 3.5 - Conflict Resolution  
**Priority**: Medium  
**Estimated Effort**: 1 day  
**Status**: Not Started  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

During architectural review, `change-impact-analysis` and `change-management` were found to use incompatible risk classification scales:

| Skill | Risk Levels |
|-------|-------------|
| `change-management` | `Low` / `Medium` / `High` (3-level) |
| `change-impact-analysis` | `NONE` / `LOW` / `MEDIUM` / `HIGH` / `CRITICAL` (5-level, uppercase) |

The `change-impact-analysis` SKILL.md states its JSON output is "directly compatible with `change-management` skill's `affected_documents` format" — but `CRITICAL` and `NONE` values have no mapping in `change-management`. A downstream consumer reading severity from a `change-impact-analysis` report and attempting to feed it into a `change-management` workflow will silently lose or misclassify `CRITICAL` impacts.

This task resolves the incompatibility by adding a normalized `risk_level` output field to `change-impact-analysis` that maps to `change-management`'s 3-level scale.

## Objectives

- Define an explicit mapping table from `change-impact-analysis`'s 5-level severity to `change-management`'s 3-level `risk_level`
- Add a `normalized_risk_level` field to `change-impact-analysis` JSON output
- Update the "compatibility" claim in `change-impact-analysis/SKILL.md` to accurately describe the mapping
- No changes required to `change-management` (lower risk for existing workflows)

## Detailed Requirements

### Functional Requirements

- **FR-T21.1**: Add a **Risk Level Mapping** section to `change-impact-analysis/SKILL.md` defining the normalization table:

  | Internal Severity | `normalized_risk_level` (change-management compatible) | Rationale |
  |---|---|---|
  | `NONE` | `Low` | No impact — maps to minimum risk |
  | `LOW` | `Low` | Minor impact — within Low threshold |
  | `MEDIUM` | `Medium` | Moderate impact — maps directly |
  | `HIGH` | `High` | Significant impact — maps directly |
  | `CRITICAL` | `High` | Exceeds change-management's scale — capped at High with `critical_flag: true` |

- **FR-T21.2**: Add `normalized_risk_level` and `critical_flag` fields to each artifact entry in `change-impact-report.json`. Schema update:

  ```json
  {
    "artifact_path": "string",
    "severity": "NONE|LOW|MEDIUM|HIGH|CRITICAL",
    "normalized_risk_level": "Low|Medium|High",
    "critical_flag": false
  }
  ```

  `critical_flag` is `true` only when `severity` is `CRITICAL`; `false` in all other cases.

- **FR-T21.3**: Add a `summary.critical_count` field to `change-impact-report.json` root-level summary block, counting the number of artifacts with `critical_flag: true`.
- **FR-T21.4**: Update the compatibility claim in `change-impact-analysis/SKILL.md` Outputs section to read: _"The `affected_documents` entries in `change-impact-report.json` are compatible with `change-management` skill's `affected_documents` format using the `normalized_risk_level` field. Use `critical_flag: true` to identify CRITICAL impacts that exceed `change-management`'s native scale."_
- **FR-T21.5**: Update `change-impact-report.md` (the human-readable report template) to surface `critical_flag: true` artifacts in a dedicated **Critical Impacts** section at the top of the report, separate from the main artifact list.

### Technical Requirements

- **TR-T21.1**: The `normalized_risk_level` field must use the exact casing accepted by `change-management` (`Low`, `Medium`, `High`) to ensure zero-friction JSON consumption.
- **TR-T21.2**: Existing `change-impact-report.json` consumers that read only the `severity` field must not be broken — `severity` values are unchanged.

### Business Requirements

- **BR-T21.1**: A practitioner using `change-impact-analysis` output as input to `change-management` must be able to use `normalized_risk_level` directly without manual translation.
- **BR-T21.2**: CRITICAL impacts must not be silently downgraded — the `critical_flag` ensures they remain visibly flagged even when normalized to `High`.

## Acceptance Criteria

### Must Have
- [ ] Risk Level Mapping table added to `change-impact-analysis/SKILL.md`
- [ ] `normalized_risk_level` and `critical_flag` fields added to `change-impact-report.json` schema in SKILL.md
- [ ] `summary.critical_count` added to JSON summary schema
- [ ] Compatibility claim in Outputs section updated (FR-T21.4)
- [ ] Human-readable report template updated with Critical Impacts section (FR-T21.5)

### Should Have
- [ ] Example JSON snippet in SKILL.md showing a CRITICAL entry with `critical_flag: true` and `normalized_risk_level: "High"`

### Could Have
- [ ] Note in `change-management/SKILL.md` Inputs section suggesting `change-impact-analysis` as a compatible upstream source

## Implementation Approach

### Phase 1: Analysis
1. Read `change-impact-analysis/SKILL.md` Outputs section and JSON schema definition
2. Read `change-management/SKILL.md` to confirm `affected_documents` schema (field names and risk_level values)
3. Identify all locations in `change-impact-analysis/SKILL.md` that reference the compatibility claim

### Phase 2: Implementation
1. Edit `change-impact-analysis/SKILL.md` — add Risk Level Mapping section
2. Edit `change-impact-analysis/SKILL.md` — update JSON schema with new fields
3. Edit `change-impact-analysis/SKILL.md` — update Outputs compatibility claim
4. Edit `change-impact-analysis/SKILL.md` — update Markdown report template

### Phase 3: Validation
1. Verify all 5 severity levels map correctly to normalized output
2. Verify `severity` values in schema are unchanged (no breaking change)
3. Create 2 test cases: (a) CRITICAL artifact → `critical_flag: true`, `normalized_risk_level: "High"`; (b) NONE artifact → `critical_flag: false`, `normalized_risk_level: "Low"`

## Dependencies

### Prerequisites
- **Task Dependencies**: T11 (`change-impact-analysis` skill created)
- **Artifact Dependencies**: `change-impact-analysis/SKILL.md`, `change-management/SKILL.md`

### Blocking/Blocked By
- **Blocks**: T14 (Integrate with Existing Skills Framework) — unified pipeline depends on compatible risk scales
- **Blocked By**: None (independent of T18, T19, T20)

## Deliverables

- Updated `change-impact-analysis/SKILL.md` (mapping table, new JSON fields, updated compatibility claim)
- Test cases in `artifacts/Testing/T21-test-cases.md`

## Notes

- This task intentionally does not upgrade `change-management` to a 5-level scale to minimise disruption to existing Project 1 and Project 2 workflows that consume `change-management` output.
- If a future iteration decides to promote `change-management` to a 5-level scale, the `critical_flag` field provides a clean migration path.
