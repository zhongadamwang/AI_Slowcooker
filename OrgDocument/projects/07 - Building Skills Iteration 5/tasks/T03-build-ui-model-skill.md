# T03 - Build Software-Boundary UI Models

**Task ID**: T03  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 2.00 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Create proposed `ui-generatemodel` to close the existing manual UI Model generation gap while preserving the current aggregation and screen traceability contracts.

## Detailed Requirements

Sources: R-002, R-005, R-008, R-011.

- Consume boundary-scoped domain/process/use-case models using T01's contract. Development can use contract fixtures before T02 implementation is complete.
- Extend existing UIModel/UIModelEntry data with boundary and applicable use-case/process references; retain entity aggregation and stable `UME` identities.
- Generate model Markdown/JSON only for software boundaries with UI requirements; record non-applicability explicitly otherwise.
- Unknown boundary type requires clarification before screen production. Do not treat domain-concepts completion as UI readiness.

## Acceptance Criteria

- [ ] Existing UI model structure and aggregation semantics remain usable by the screen pipeline.
- [ ] Every UI entry resolves to a software boundary and valid scoped entity references.
- [ ] Non-software boundaries and software boundaries without UI requirements produce no screens or forced UI model.
- [ ] Missing source references and unknown boundary classification are reported explicitly.

## Validation Tests

Software/non-software/unclassified fixtures, software-without-UI fixture, stable-ID revision, and compatibility with the existing singular screen reference.

## Dependencies

Prerequisite: T01. Blocks T05. T02 is a runtime input responsibility, not a prerequisite for parallel implementation using shared fixtures.

## Implementation Notes and Deliverables

Skill instructions, gate, extended UI-model contract/example, focused tests, and migration notes for current model consumers.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [UI inventory contract](../../../../.github/skills/screen-generateinventory/SKILL.md)
