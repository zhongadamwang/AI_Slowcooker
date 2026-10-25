# T02 — Add Collaboration Mode to Project Initialization

**Task ID**: T02
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 1 day
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22
**Completed**: 2026-10-22

## Description

Wire the `collaboration_mode` field (defined in T01) into `project-document-management` so every new project explicitly chooses a mode at init time, and into `project-metadata.json`'s evolution history so mode changes are auditable.

## Objectives

- Add `collaboration_mode` as an input prompt to `project-document-management`, alongside existing `archetype` input
- Record mode changes as evolution_history entries (mode is not meant to change often, but must be traceable if it does)

## Detailed Requirements

### Functional Requirements
- **FR-02.1**: `project-document-management` SKILL.md updated to accept `collaboration_mode` (`solo` | `traditional`, default `solo` for new projects per T01)
- **FR-02.2**: `project-metadata.json` template updated with `"collaboration_mode": "solo | traditional"` field
- **FR-02.3**: A `change-mode` operation exists (e.g., `orchestrate set-mode solo`) that updates the field and appends an evolution_history entry with timestamp + reason

### Technical Requirements
- **TR-02.1**: Existing `project-metadata.json` files without the field are treated as `traditional` on read (safe default, see T01 TR-01.1)
- **TR-02.2**: `main.md`/`README.md` templates generated at init should state the active mode plainly so it's visible without opening JSON

## Acceptance Criteria

### Definition of Done
- [x] New projects initialized via `project-document-management` have `collaboration_mode` set in metadata
- [x] Mode changes are logged in `evolution_history`
- [x] Gate schema for `project-document-management` (`gate.json`) updated to check the field exists (soft check, since field didn't exist before)

## Dependencies

### Prerequisites
- **T01** — Collaboration mode schema definition

### Blocks
- T03 (orchestrator/gate behavior reads this field)

---

## Completion Notes

**Completed**: 2026-10-22

### Changes Made

- **`.github/skills/project-document-management/SKILL.md`** (v2.0.0 → v2.1.0):
  - Added `collaboration_mode` as an optional input (default `solo`), cross-referencing `collaboration-mode-reference.md`
  - `project-metadata.json` template (Step 3) now includes `collaboration_mode` at both the top level and inside each `evolution_history` entry
  - New **Reading Legacy Metadata** subsection: absence of the field is read as `traditional`, never inferred as `solo`
  - New **Change Collaboration Mode** quick command: validates target mode, records `from_mode`/`to_mode`/`reason`/timestamp as a patch-version evolution_history entry, explicitly states the change is non-retroactive, and updates `main.md`/`README.md` mode text if present
  - Project `main.md` template now states **Collaboration Mode** plainly alongside Archetype
  - **Initialize New Project** quick command updated to accept and apply `collaboration_mode`
  - Added Best Practice #8: never infer `collaboration_mode` as a side effect of another operation

- **`.github/skills/project-document-management/gate.json`** (new `collaboration_mode_present` check):
  - Soft `json_schema` check requiring the `collaboration_mode` field
  - Explicitly non-blocking (absence = `traditional`, not a failure) — nudges new projects to set it explicitly without breaking any existing project's gate evaluation
  - Remediation points to the new Change Collaboration Mode operation

### Key Decisions

- Kept the field change **metadata-only** (patch version bump), consistent with how other non-structural metadata edits are versioned in this skill
- Did not invent a separate `set-mode` CLI-style command name; instead documented it as a named operation ("Change Collaboration Mode") consistent with this skill's existing "Quick Commands" pattern (Initialize New Project, Upgrade Archetype, Structure Validation, etc.)
- Declined to hardcode a cross-reference link from the generic `main.md` template to Iteration 4's `collaboration-mode-reference.md`, since that template is reused by every project in every iteration, not just this one — the mode value itself is stated plainly instead

### Next Steps for Integration

- **T03**: Orchestrator's `evaluateSkillGate()` needs to read `collaboration_mode` from `project-metadata.json` (defaulting to `traditional` when absent, per this task) before applying archetype-based severity for the new `stakeholder_confirmation` check type
- **T04/T05**: Mode-conditional skill instructions can now rely on `collaboration_mode` being a documented, readable field
