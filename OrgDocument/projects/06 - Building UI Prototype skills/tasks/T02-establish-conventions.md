# T02 — Establish Traceability & Format Conventions

**Task ID**: T02
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 0.5 day
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Several requirements (R-605, R-606, R-623–R-626) are cross-cutting constraints that every generation task (T04–T09) must respect, rather than a single standalone feature. Documenting them once now avoids re-deriving them ad-hoc in each later task's own instructions.

## Objectives

- Finalize ID formats for screens and UI Model entries
- Document the traceability tag convention used across generated Markdown/JSON
- Publish a pre-ship checklist covering the hard constraints (text-based, no design tool, no tech stack, `file://` portability)

## Detailed Requirements

### Functional Requirements
- **FR-02.1**: ID format finalized — proposed `SCR-[###]` for screens, `UME-[###]` for UI Model entries (per `vocabulary.md`'s proposal), confirmed rather than left as "recommended, not yet enforced"
- **FR-02.2**: Traceability tag format documented — how `requirement_refs`/`ui_model_ref` are embedded in generated output

### Technical Requirements
- **TR-02.1**: Constraints checklist must be literal and checkable (a real checklist, not prose) so T04–T09 can verify against it directly

## Acceptance Criteria

- [ ] Conventions document published at `artifacts/Documentation/ui-prototyping-conventions.md`
- [ ] ID formats finalized and cross-referenced from this document
- [ ] Hard-constraints checklist present and literal/checkable

## Dependencies

### Prerequisites
- None

### Blocks
- T03, T04, T05, T06, T07, T08, T09 (all reference these conventions)
