# T03 — Prototype UI Model Schema (Base Model + Aggregation)

**Task ID**: T03
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

The UI Model (R-606, R-627, R-628, R-629, R-630) is the single most architecturally significant piece of new modeling work in this project, and `scope-analysis.md` flags it as the **top recommendation**: "treat as the first thing to prototype concretely... several other Core features depend on its shape being settled." `domain-concepts.md` rated this pattern's confidence as only medium, pending a real example.

This task produces a **worked example**, not yet the actual generation skill — the goal is de-risking the schema design before committing to it in T04's instructions.

## Objectives

- Produce at least one concrete `ui-model.md`/`.json` example against a real or toy domain
- Validate that "aggregation" is representable using only Markdown+JSON, with no new modeling notation required
- Sketch (not fully implement) the derived-model placeholder structure so the base-model schema doesn't need breaking changes later

## Detailed Requirements

### Functional Requirements
- **FR-03.1**: Example UI Model contains 2+ `UIModelEntry` items, each aggregating 2+ domain entities
- **FR-03.2**: Example demonstrates the full traceability chain: domain entities → Aggregation → UIModelEntry

### Technical Requirements
- **TR-03.1**: If a new notation genuinely is needed beyond Markdown+JSON, that gap must be explicitly documented as a finding of this task, not silently absorbed into T04

## Acceptance Criteria

- [ ] At least one concrete `ui-model.md` worked example published
- [ ] Schema confirmed workable using only Markdown+JSON, or gap explicitly documented
- [ ] Derived-model placeholder structure sketched

## Dependencies

### Prerequisites
- **T02** — conventions (ID formats, traceability tags) should be settled before schema is finalized

### Blocks
- T04 (screen inventory generation references UI Model entries)
