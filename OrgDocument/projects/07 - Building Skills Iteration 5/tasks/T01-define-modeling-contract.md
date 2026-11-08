# T01 - Define Entity, Boundary, and Modeling-Round Contracts

**Task ID**: T01  
**Phase**: 1 - Foundation  
**Priority**: P0-Critical  
**Estimated Effort**: 2.00 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Define one minimal cross-model contract before implementing producers and validation. Reuse existing entity IDs, hierarchy metadata, UIModelEntry aggregation, and artifact ownership.

## Detailed Requirements

Sources: R-002, R-005, R-007, R-008, R-009, R-010, R-011.

- Define scoped entity and system-boundary references, explicit software typing, actor roles relative to a boundary, cross-level mappings, source/version references, and model applicability.
- Specify use-case model/script and UI-model extensions, artifact locations resolved from metadata, and source-backed alignment manifest/report formats.
- Define round scope, revision invalidation, clarification/revalidation, and non-bypassable alignment completion. Do not conflate boundary type with participant stereotype.
- Preserve existing screen IDs, singular `ui_model_ref`, and VR/HR authority; do not require identical entities at every hierarchy level.

## Acceptance Criteria

- [ ] Shared contract documents all fields, ownership, applicability, and compatibility rules with valid positive/negative fixtures.
- [ ] Three-level fixture includes a non-software parent, software child, and scoped entity-name collision.
- [ ] Unknown boundary type, missing applicable model, and source/manifest disagreement have explicit failure/clarification outcomes.
- [ ] New responsibility-based names and unused skill IDs are selected without renumbering S11 or S33-S38.

## Validation Tests

Validate fixture schemas/references and demonstrate that boundary stereotype alone cannot authorize UI. Document how references are checked against actual model artifacts.

## Dependencies

Prerequisites: none. Blocks T02, T03, T04.

## Implementation Notes and Deliverables

Shared modeling contract reference under the responsible skill, schema/examples, applicability table, and compatibility notes. No new generic modeling repository or gate service.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [Requirements](../artifacts/Analysis/requirements.md)
