# T01 — Extend project-document-management with UI Prototype Artifact Category

**Task ID**: T01
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 0.5-1 day
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

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

- [x] `.github/skills/project-document-management/SKILL.md` updated with the new artifact category
- [x] New projects initialized via `project-document-management` get an `artifacts/UI Prototype/main.md` folder when the UI Prototyping skill set is in use
- [x] Existing projects without this category are unaffected (additive change only)

## Dependencies

### Prerequisites
- None — this is a foundational cross-skill change

### Blocks
- T04 (screen inventory needs somewhere to be written)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/project-document-management/SKILL.md`** (v2.2.0 → v2.3.0):
  - `standard` archetype folder tree now shows `UI Prototype/` as an opt-in category, explicitly commented as conditional ("Only when the project uses UI prototyping skills")
  - Step 2 (Create Project Folder Tree) updated with the same conditional annotation, consistent with how `Documentation/` is already annotated as archetype-conditional
  - New **Integration Points** subsection: "UI Prototyping skill set (`screen-generateinventory` and related skills, planned — Project 06)" documenting the folder dependency, ordering rule (this skill creates the folder → UI Prototyping skills fill it), and an explicit note that this category is opt-in by actual skill usage, not tied to archetype the way `Documentation/` is

- **`.github/skills/project-document-management/gate.json`**:
  - New soft check `ui_prototype_category_consistent` — does not require the folder for every project (only flags if UI Prototyping outputs exist without the folder); kept soft and non-blocking since this is an opt-in category, not a universal requirement

### Key Decisions

- **Made `UI Prototype/` opt-in, not archetype-tied**: unlike `Documentation/` (present for standard/hierarchical, absent for flat), `UI Prototype/` depends on whether a project actually uses the UI Prototyping skill set — a standard-archetype project with no UI work shouldn't get an empty `UI Prototype/` folder by default. This matches `domain-alignment.md`'s general pattern of keeping new concepts additive and narrowly scoped.
- **Did not force this into the `flat` archetype's tree** — `flat` is explicitly for lightweight projects; UI prototyping is a `standard`/`hierarchical`-tier concern consistent with where `Documentation/` already lives
- **Gate check kept soft and permissive** — since this category's presence is conditional on actual skill usage (not detectable purely from project-metadata.json yet), a hard check would produce false positives for the vast majority of projects that don't use UI prototyping at all

### Next Steps for Integration

- **T04** (`screen-generateinventory` skill): should reference this task's new Integration Points section when documenting its own output location
- Future: once UI Prototyping skills are built (T04+), the gate check's `required_folders` can be tightened if a reliable signal exists (e.g., a `ui_prototyping_enabled` flag in `project-metadata.json`) rather than inferring usage indirectly
