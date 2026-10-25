# T03 — Mode-Aware Gate Evaluation (Approval Checks)

**Task ID**: T03
**Phase**: Phase 2 - Orchestration
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22
**Completed**: 2026-10-22

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
- [x] `stakeholder_confirmation` check type documented in `gate-authoring-guide.md`
- [x] Orchestrator gate evaluator updated and the pseudocode in SKILL.md reflects the mode branch
- [x] At least one existing gate.json (candidate: `process-w5h`, `requirements-sanitize`) retrofitted as a worked example
- [x] Test: same project, same skill, run gate eval once in each mode — traditional blocks without confirmation record, solo passes with self-attestation logged

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

---

## Completion Notes

**Completed**: 2026-10-22

### Changes Made

- **`.github/skills/edps-workflow-orchestrator/SKILL.md`** (v1.0.0 → v1.1.0):
  - `evaluateSkillGate()` now accepts `projectMetadata`, reads `collaboration_mode` (defaulting to `traditional` if absent), and resolves it **before** applying archetype-based severity, per TR-03.1
  - New `resolveCheckSeverity()` helper: only `stakeholder_confirmation` checks are mode-aware (`solo` → `soft`, `traditional` → `hard`); every other check type keeps its declared severity unchanged
  - New `checkStakeholderConfirmation()` function: looks up an existing confirmation record; in `solo` mode with no record, auto-generates and appends a self-attestation record rather than failing, keeping the build-and-clarify loop frictionless; in `traditional` mode (or solo with an expected-but-missing record) with no record, fails with remediation
  - Documented the **confirmation record shape** (`role`, `confirmation_statement`, `confirmed_by`, `collaboration_mode`, `timestamp`) — identical structure in both modes so project history reads consistently across a mode switch
  - `Inputs` section now documents that the orchestrator reads `collaboration_mode` from `project-metadata.json` automatically before every gate evaluation

- **`gate-authoring-guide.md`** (Iteration 3 Documentation, still the canonical gate-authoring reference):
  - New **Check Type 4: Stakeholder Confirmation** — documents `role`, `confirmation_statement` fields, and the rule that this check type never declares a static `severity` (it is resolved from `collaboration_mode` at evaluation time)
  - Authoring Best Practices updated with a note not to add a `severity` field to this check type

- **`.github/skills/process-w5h/gate.json`** (v1.0.0 → v1.1.0) — retrofitted as the worked example (FR-03.2/TR-03.2):
  - New `stakeholder_roles_confirmed` check (`stakeholder_confirmation` type, role: "Primary Stakeholder") requiring confirmation that identified stakeholder roles/responsibilities are accurate before downstream domain modeling/planning treats them as settled
  - Chosen over `requirements-sanitize` because `requirements-sanitize` currently has no `gate.json` at all (would have required authoring one from scratch, a larger change than a focused retrofit)

### Key Decisions

- **Mode resolution happens inside `evaluateSkillGate()`, not as a separate pre-pass** — keeps the mode-vs-archetype ordering (TR-03.1) explicit and co-located with the rest of the severity logic, rather than splitting the branch across two functions
- **Only `stakeholder_confirmation` is mode-aware** — explicitly scoped this way so the change is additive; no existing gate.json's `artifact_existence`/`content_pattern`/`json_schema` checks change behavior
- **Solo-mode auto-pass generates its own audit record** rather than requiring the developer to pre-author one — this matches the source material's framing of solo mode as low-friction self-review, while still leaving a full audit trail (FR-03.3, TR-03.1's "preserve full audit trail" objective)
- **Did not retrofit all 32 gate.json files in this task** (TR-03.2 calls for an audit of all 32, but FR/DoD only required "at least one" as a worked example). Retrofitting the full set is better driven by T04/T05, which touch specific skills' instructions anyway — noted as follow-up below rather than scope-creeping T03

### Follow-up / Not Done Here

- Full audit of all 32 gate.json files for implicit stakeholder-review assumptions (TR-03.2) is **not** completed in this task — only `process-w5h` was retrofitted as the required worked example. Recommend folding the remaining audit into T04 (which already touches `process-w5h`, `requirements-sanitize`, `requirements-ingest` instructions) and T05 (`change-management`, `project-planning-tracking`)
- `requirements-sanitize` has no `gate.json` yet (pre-existing gap, unrelated to this feature) — if T04 adds one, it should include a `stakeholder_confirmation` check per its Definition-of-Done item about business-stakeholder validation

### Next Steps for Integration

- **T04**: Update `process-w5h`, `requirements-sanitize`, `requirements-ingest` skill *instructions* (not just gates) with mode-conditional guidance — the gate-level mechanism from this task now exists for them to reference
- **T05**: Apply the same mode-conditional pattern to `change-management` / `project-planning-tracking`, plus the "real external stakeholder" flag
