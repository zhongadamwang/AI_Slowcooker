# T04 - Build Shared Model-Alignment Validation

**Task ID**: T04  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 3.33 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Create proposed `model-validatealignment` with a small deterministic validator, source-backed reports, and focused clarification handling.

## Detailed Requirements

Sources: R-005, R-008, R-009, R-010, R-011.

- Validate entity identity/scope/membership and system-boundary identity/type/parent references across applicable models.
- Check actual source/version references; reject detached or contradictory manifest projections and stale report reuse.
- Explicitly distinguish consistency, unresolved clarification, malformed/missing applicable input, and justified UI non-applicability.
- Report item-level model/entity/boundary evidence and actionable questions. Preserve clarification history and require revalidation after answers.
- Delegate VR/HR checks to their existing owners; no duplicated boundary-routing or structural validators.

## Acceptance Criteria

- [ ] Consistent multi-level fixtures pass; scoped identical names do not produce false conflicts.
- [ ] Entity and boundary contradictions request clarification and never return an aligned result.
- [ ] Unknown UI boundary type, illegal UI placement, missing applicable models, malformed inputs, and source/manifest disagreement are explicit failures.
- [ ] Every report records round and source versions; editing an affected model invalidates the previous result.

## Validation Tests

Python standard-library tests cover each result class, deterministic output, entity collisions, missing links, UI applicability, and revision invalidation. Existing fixture source data is checked, not just file existence.

## Dependencies

Prerequisite: T01. Blocks T05. Implement against T01 fixtures independently of T02/T03.

## Implementation Notes and Deliverables

Skill instructions, hard/non-bypassable alignment gate, validator script, fixture suite, report Markdown/JSON, and clarification procedure.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [Shared-contract task](T01-define-modeling-contract.md)
