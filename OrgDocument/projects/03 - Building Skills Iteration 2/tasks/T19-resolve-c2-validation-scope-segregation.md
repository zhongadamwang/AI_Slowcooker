# T19: Resolve C-2 — Structural Validation Scope Segregation

**Task ID**: T19  
**Phase**: Phase 3.5 - Conflict Resolution  
**Priority**: High  
**Estimated Effort**: 1-2 days  
**Status**: Completed  
**Assigned**: GitHub Copilot  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

During architectural review, four Group B rules in `edps-compliance/SKILL.md` were found to substantially duplicate rules already covered by `hierarchy-validation/SKILL.md`:

| `edps-compliance` | `hierarchy-validation` counterpart |
|---|---|
| HR-1 — Parent-Child Link Integrity | HX-1 (Parent Link Resolves) + HX-2 (Child Link Resolves) |
| HR-3 — Breadcrumb Consistency | HX-3 — Breadcrumb Path Integrity |
| HR-4 — Sub-Processes Section Populated | HX-5 — Hierarchy Index Currency (partial) |
| HR-5 — Folder Naming Convention | HN-1 — Folder Name Convention (identical regex) |

Running both skills produces two separate, potentially contradictory reports covering the same artifacts. `hierarchy-validation` also provides `--fix` capability for these issues while `edps-compliance` does not. This task segregates responsibility so each skill owns a non-overlapping mandate.

## Objectives

- Designate `hierarchy-validation` as the sole authority for file/link integrity and structural naming
- Strip the redundant HR-1, HR-3, HR-4, HR-5 rules from `edps-compliance` Group B
- Add a `hierarchy-validation PASS` pre-condition gate to `edps-compliance`
- Retain `edps-compliance`'s unique Group B rules (HR-2, HR-6) and all Group C evolutionary-principles rules

## Detailed Requirements

### Functional Requirements

- **FR-T19.1**: Remove HR-1, HR-3, HR-4, and HR-5 rule definitions and their check algorithm blocks from `edps-compliance/SKILL.md` Group B.
- **FR-T19.2**: Add a **Pre-Conditions** section to `edps-compliance/SKILL.md` stating: before executing any compliance checks, `hierarchy-validation` must have been run on the same target scope and must have exited with overall status `PASS` or `PASS-WITH-WARNINGS`. If not, `edps-compliance` must halt and return a `pre-condition-not-met` error with remediation guidance.
- **FR-T19.3**: `edps-compliance` may optionally accept `hierarchy-validation-report.json` as an input to satisfy the pre-condition gate automatically (rather than requiring a separate manual run).
- **FR-T19.4**: Retained Group B rules in `edps-compliance` after this change: **HR-2** (Decomposed Participant Exists — checks that a sub-folder matches a `control`-type participant in the parent diagram, a semantic rule not covered by `hierarchy-validation`) and **HR-6** (Metadata Currency — checks `hierarchy-metadata.json` timestamp currency, not covered by `hierarchy-validation`).
- **FR-T19.5**: Update the `edps-compliance` compliance score formula: `total_checks` must reflect the reduced rule set (HR-1/3/4/5 removed). The pre-condition gate failure must produce a `BLOCKED` overall status distinct from `FAIL`.
- **FR-T19.6**: Update `hierarchy-validation/SKILL.md` description to explicitly state it is the authoritative structural integrity checker for the EDPS skill suite. No logic changes required.

### Technical Requirements

- **TR-T19.1**: The `pre-condition-not-met` error response must include: `missing_pre_condition`, `suggested_command` (invoke `hierarchy-validation` with same target), and `blocking_issues` list.
- **TR-T19.2**: When `hierarchy-validation-report.json` is provided as input, `edps-compliance` must validate the report's `target_scope` matches its own target before accepting it. Mismatched scope must produce a `scope-mismatch` warning and fall back to requiring a manual pre-condition confirm.

### Business Requirements

- **BR-T19.1**: A practitioner must be able to run `hierarchy-validation` once and pass its report to `edps-compliance` — a single-pass workflow with no redundant checks.
- **BR-T19.2**: Any new structural/link-integrity rule added in a future iteration must be added only to `hierarchy-validation`. `edps-compliance` picks it up via the pre-condition gate automatically.

## Acceptance Criteria

### Must Have
- [x] HR-1, HR-3, HR-4, HR-5 rule definitions and algorithms removed from `edps-compliance/SKILL.md`
- [x] `edps-compliance/SKILL.md` contains a Pre-Conditions section referencing `hierarchy-validation`
- [x] `edps-compliance/SKILL.md` Inputs section lists `hierarchy-validation-report.json` as optional input
- [x] HR-2 and HR-6 retained in `edps-compliance/SKILL.md` with unchanged logic  
- [x] Compliance score formula updated to reflect reduced `total_checks`
- [x] `BLOCKED` overall status defined for pre-condition-not-met scenarios
- [x] `hierarchy-validation/SKILL.md` description updated to assert authoritative scope

### Should Have
- [x] `pre-condition-not-met` error response schema documented
- [x] Scope-mismatch guard for `hierarchy-validation-report.json` input documented

### Could Have
- [ ] Workflow diagram showing `hierarchy-validation → edps-compliance` pipeline sequence

## Implementation Approach

### Phase 1: Analysis
1. Read `edps-compliance/SKILL.md` Group B section and identify exact text blocks for HR-1, HR-3, HR-4, HR-5
2. Confirm HR-2 and HR-6 have no counterpart in `hierarchy-validation` (verify non-overlap)
3. Read `hierarchy-validation/SKILL.md` to confirm it covers all four removed checks

### Phase 2: Implementation
1. Edit `edps-compliance/SKILL.md` — remove HR-1, HR-3, HR-4, HR-5 rule blocks
2. Edit `edps-compliance/SKILL.md` — add Pre-Conditions section before workflow
3. Edit `edps-compliance/SKILL.md` — add `hierarchy-validation-report.json` to Inputs
4. Edit `edps-compliance/SKILL.md` — update scoring section with `BLOCKED` status
5. Edit `hierarchy-validation/SKILL.md` — update description to claim authoritative scope

### Phase 3: Validation
1. Verify retained HR-2 and HR-6 algorithms are intact and unchanged
2. Verify compliance score formula is arithmetically correct with reduced rule count
3. Create 3 test cases: (a) pre-condition satisfied via report input, (b) pre-condition not met — BLOCKED, (c) scope-mismatch guard triggered

## Dependencies

### Prerequisites
- **Task Dependencies**: T10 (hierarchy-validation created), T9 (edps-compliance created), T18 (C-1 resolved — edps-compliance already updated)
- **Artifact Dependencies**: `edps-compliance/SKILL.md`, `hierarchy-validation/SKILL.md`

### Blocking/Blocked By
- **Blocks**: T14 (Integrate with Existing Skills Framework) — pipeline sequencing requires clear skill mandates
- **Blocked By**: T18 (must apply after C-1 edits to `edps-compliance` are complete, to avoid merge conflicts on the same file)

## Deliverables

- Updated `edps-compliance/SKILL.md` (4 rules removed, pre-condition gate added)
- Updated `hierarchy-validation/SKILL.md` (authoritative scope declared)
- Test cases in `artifacts/Testing/T19-test-cases.md`

## Notes

- HR-2 (Decomposed Participant Exists) is a semantic/content check — it verifies *which participant* was decomposed, not just that links resolve. It remains squarely in `edps-compliance`'s mandate.
- HR-6 (Metadata Currency) checks timestamp freshness of `hierarchy-metadata.json`, which is a process hygiene rule rather than a structural integrity rule, and belongs with the compliance checker.
