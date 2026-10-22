# T03 — Mode-Aware Gate Evaluation (Approval Checks)

**Task ID**: T03
**Phase**: Phase 2 - Orchestration
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22

## Description

The current gate system (`skill-completion-gates`, T08 from Iteration 3) only has three check types: `artifact_existence`, `content_pattern`, `json_schema`. None of them represent "a human stakeholder confirmed this output." This task introduces a new check type, `stakeholder_confirmation`, and makes its severity mode-dependent: hard-blocking in `traditional` mode, auto-pass-with-self-attestation-log in `solo` mode.

## Objectives

- Add `stakeholder_confirmation` as a fourth gate check type
- Make `edps-workflow-orchestrator`'s gate evaluator read `project-metadata.json`'s `collaboration_mode` and apply mode-specific severity
- Preserve full audit trail in both modes (who/what confirmed, even if "who" is the same developer wearing a different hat)

## Detailed Requirements

### Functional Requirements
- **FR-03.1**: New gate check type `stakeholder_confirmation` — fields: `role` (e.g., "Business Owner"), `confirmation_statement` (what's being confirmed), `severity`
- **FR-03.2**: In `traditional` mode: `stakeholder_confirmation` checks behave as `hard` — block workflow until an explicit confirmation record (with the role and a free-text confirmation note) is present in project state
- **FR-03.3**: In `solo` mode: `stakeholder_confirmation` checks auto-convert to `soft` — the developer's self-attestation (a one-line note: "Confirmed as [role]: ...") satisfies the check without blocking, logged identically for traceability
- **FR-03.4**: Gate failure/pass reporting must show which mode was active and why severity differs, so a mode switch is never silently surprising

### Technical Requirements
- **TR-03.1**: Update `evaluateSkillGate()` pseudocode in `edps-workflow-orchestrator/SKILL.md` to branch on `collaboration_mode` before applying `archetype`-based severity (mode check happens first, then archetype)
- **TR-03.2**: Retrofit existing gate.json files that implicitly assume stakeholder review (e.g., content checks referencing "stakeholder" in remediation text) to use the new check type where appropriate — audit all 32 gate.json files

## Acceptance Criteria

### Definition of Done
- [ ] `stakeholder_confirmation` check type documented in `gate-authoring-guide.md`
- [ ] Orchestrator gate evaluator updated and the pseudocode in SKILL.md reflects the mode branch
- [ ] At least one existing gate.json (candidate: `process-w5h`, `requirements-sanitize`) retrofitted as a worked example
- [ ] Test: same project, same skill, run gate eval once in each mode — traditional blocks without confirmation record, solo passes with self-attestation logged

### Validation Tests
- **Test-03.1**: `solo` mode — skill completion with no confirmation record → auto-pass, self-attestation entry appended to project state
- **Test-03.2**: `traditional` mode — same scenario → hard block, remediation message asks for stakeholder confirmation record
- **Test-03.3**: Mode switched mid-project (via T02's `set-mode`) — previously-passed solo confirmations are *not* retroactively invalidated, but newly-evaluated gates follow the new mode

## Dependencies

### Prerequisites
- **T01** — mode schema
- **T02** — mode field available in project state

### Blocks
- T04, T05 (skill-specific updates depend on this check type existing)
