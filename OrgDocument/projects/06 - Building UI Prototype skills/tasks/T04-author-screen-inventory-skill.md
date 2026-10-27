# T04 — Author screen-generateinventory Skill

**Task ID**: T04
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

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

- [ ] SKILL.md authored and follows existing EDPS skill conventions (Intent, Inputs, Outputs, Usage sections)
- [ ] Given a test requirements.json + ui-model.json, produces a valid screen inventory
- [ ] Output location and naming match T02's conventions

## Dependencies

### Prerequisites
- **T01** — artifact category must exist
- **T03** — UI Model schema must be settled

### Blocks
- T05 (layout spec generation needs a screen inventory to iterate over)
