# T01 — Extend project-document-management with UI Prototype Artifact Category

**Task ID**: T01
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 0.5-1 day
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Every UI prototyping generation output (screen inventory, layout specs, mockups) needs a standard place to live. Per requirements R-601/R-601a and the D-6 decision (standalone screen inventory artifact), this project depends on `project-document-management` accepting a new `UI Prototype` artifact category alongside its existing ones (`Analysis`, `Changes`, `Documentation`, `Sample Data`, `Source Materials`, `Testing`).

This is a small, explicit cross-skill change — not something this project can assume into existence silently.

## Objectives

- Add `UI Prototype` as a recognized artifact category in `project-document-management`'s folder-scaffolding templates
- Ensure the change is additive and backward-compatible with existing projects

## Detailed Requirements

### Functional Requirements
- **FR-01.1**: New projects initialized with UI prototyping in scope get an `artifacts/UI Prototype/main.md` folder
- **FR-01.2**: Existing projects without this category remain unaffected

### Technical Requirements
- **TR-01.1**: Follows the existing `main.md` directory documentation rules already established in `project-document-management/SKILL.md`
- **TR-01.2**: Optionally extend `project-document-management`'s `gate.json` with a soft check for the new category's presence, consistent with how Iteration 4 added `collaboration_mode_present` as a soft check

## Acceptance Criteria

- [ ] `.github/skills/project-document-management/SKILL.md` updated with the new artifact category
- [ ] New projects initialized via `project-document-management` get an `artifacts/UI Prototype/main.md` folder when the UI Prototyping skill set is in use
- [ ] Existing projects without this category are unaffected (additive change only)

## Dependencies

### Prerequisites
- None — this is a foundational cross-skill change

### Blocks
- T04 (screen inventory needs somewhere to be written)
