# T04 — Author screen-generateinventory Skill

**Task ID**: T04
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Implements R-601 (Screen Inventory Generation, standalone artifact). This is the first real generation skill, producing the entry-point artifact every other generation task depends on.

## Objectives

- Author `.github/skills/screen-generateinventory/SKILL.md` (confirm final skill name during authoring)
- Generate `screen-inventory.md`/`.json` in `artifacts/UI Prototype/` from requirements + UI Model input

## Detailed Requirements

### Functional Requirements
- **FR-04.1**: Given requirements.json + ui-model.json, produce a screen inventory listing each screen's purpose, UI Model reference, and requirement traceability
- **FR-04.2**: Output is always a standalone artifact, never embedded in a larger document (per D-6)

### Technical Requirements
- **TR-04.1**: Follow T02's established ID/traceability conventions exactly

## Acceptance Criteria

- [x] SKILL.md authored and follows existing EDPS skill conventions (Intent, Inputs, Outputs, Usage sections)
- [x] Given a test requirements.json + ui-model.json, produces a valid screen inventory
- [x] Output location and naming match T02's conventions

## Dependencies

### Prerequisites
- **T01** — artifact category must exist
- **T03** — UI Model schema must be settled

### Blocks
- T05 (layout spec generation needs a screen inventory to iterate over)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/screen-generateinventory/SKILL.md`** (new, v1.0.0, skill_id S33): authored following the standard EDPS skill template (Intent, Inputs, Outputs, Core Function, Usage, processing steps, Quality Checks, Integration, Example Prompt). Key design points:
  - Explicit pre-condition: a UI Model must already exist before this skill can run (nothing to generate a screen inventory from otherwise)
  - `ui_model_ref` documented as singular (never an array) in both the JSON schema and prose, enforcing R-606/R-628's one-to-one Screen→UIModelEntry cardinality
  - `import_origin` field included now (value always `"generated"` in MVP) specifically so T04's schema doesn't need a breaking change when the Phase 2 import capability (R-615) adds `"imported"` as a second value
  - Step 1 (Screen Identification) explicitly warns against defaulting to one-screen-per-UIModelEntry when a list-style entry might need both a list and detail screen — but only when requirements actually call for it, not automatically
  - Step 2 explicitly treats a screen with no supporting requirement as a signal to reconsider, not a silent pass-through, consistent with solo-mode's build-and-clarify principle
  - Explicitly scoped which of T02's hard-constraints checklist items apply to this skill (text-only output, no direct domain reference) vs. which don't (mockup portability, design-tool/framework constraints, changelog) — since this skill produces no HTML/CSS/JS and its own output is a derived index, not an authored document requiring its own changelog
  - Derived-model screen generation explicitly deferred to Phase 3; MVP operates against the base UI Model only

- **`.github/skills/screen-generateinventory/gate.json`** (new, skill_id S33, confirmed unique against all 32 existing skill_ids): 5 checks — 3 hard (`screen_inventory_exists`, `screens_traced_to_ui_model`, `screens_traced_to_requirements`), 1 hard structural check (`standalone_artifact`, guarding against T08 ever inlining the inventory into the design document), 1 soft (`id_format_valid`)

- **`.github/skills/README.md`**: new **S11 — UI Prototyping** section added to the skills table (first entry in a new category, distinct from S1–S10)
- **`.github/skills/INDEX.md`**: skill count bumped 32→33, version 2.1.0→2.2.0, new changelog entry announcing the skill

### Key Decisions

- **Did not yet register this skill in `edps-workflow-orchestrator`'s DAG catalogue** — that is explicitly T10's scope (Gate & Orchestrator Registration, batched across all of T04–T09 at once), not repeated per-skill here. Adding it to README.md/INDEX.md now is purely documentation indexing, not orchestrator wiring.
- **Reused `change-management`'s `generate_change_id()` scan-and-increment pattern** for `SCR-[###]` generation rather than inventing a new ID algorithm, per T02's own convention
- **No in-document changelog required for screen-inventory.md/.json** — explicitly called out as a deliberate exception to T02's general changelog convention, since this artifact is a derived index regenerated fresh each run, not an authored document accumulating its own edit history (contrast with `LayoutSpec`/`DesignDocument`/`UIModel`, which do carry changelogs)

### Next Steps for Integration

- **T05** (`screen-generatelayout`): consumes `screen-inventory.json`'s `screens` array directly; should reuse this skill's `screen_id`/`ui_model_ref`/`requirement_refs` field names exactly, not redefine them
- **T10**: must register `screen-generateinventory` (S33) in the orchestrator's DAG with prerequisites on UI Model availability and `requirements-ingest`
