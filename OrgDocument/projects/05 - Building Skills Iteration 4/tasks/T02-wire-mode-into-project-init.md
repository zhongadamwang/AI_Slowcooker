# T02 — Add Collaboration Mode to Project Initialization

**Task ID**: T02
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 1 day
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22

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
- [ ] New projects initialized via `project-document-management` have `collaboration_mode` set in metadata
- [ ] Mode changes are logged in `evolution_history`
- [ ] Gate schema for `project-document-management` (`gate.json`) updated to check the field exists (soft check, since field didn't exist before)

## Dependencies

### Prerequisites
- **T01** — Collaboration mode schema definition

### Blocks
- T03 (orchestrator/gate behavior reads this field)
