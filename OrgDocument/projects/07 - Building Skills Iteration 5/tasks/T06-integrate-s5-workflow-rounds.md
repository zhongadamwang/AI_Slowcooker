# T06 - Integrate S5 Membership and Modeling-Round Lifecycle

**Task ID**: T06  
**Phase**: 3 - Integration  
**Priority**: P0-Critical  
**Estimated Effort**: 3.33 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Replace the S11 category with S5 membership and make validated modeling rounds part of orchestration, routing, gates, and resume behavior.

## Detailed Requirements

Sources: R-001, R-002, R-006, R-009, R-010, R-011.

- Register new responsibilities and a real UI-model prerequisite; remove the S06-only proxy for UI readiness.
- Update catalog, navigator/routing/templates, applicable archetypes, completion events, and persistent round/report references.
- Keep UI execution conditional; preserve the S11 `documentation-automation` ID, S33-S38 IDs, and existing project state/history.
- Do not create cyclic DAG prerequisites. Represent refinement as new rounds, invalidating affected completions/report references on edits and checking them on resume.
- Alignment inconsistency is non-bypassable across solo/traditional and standard/rapid/compliance; it is not a softened stakeholder-confirmation check.

## Acceptance Criteria

- [ ] Active categories contain S5 membership for all six UI skills and no separate S11 category.
- [ ] Old skill IDs and resumed states remain identifiable; unknown legacy boundary typing is surfaced for clarification.
- [ ] A non-software workflow does not require UI; a software UI workflow verifies an actual UI model before inventory.
- [ ] Fresh, revised, and resumed rounds require a current report; skip/rapid/solo cannot falsely close inconsistency.

## Validation Tests

Catalog/ID checks, dependency cycle tests, routing scenarios, standalone modeling handoff, and round lifecycle simulations across both modes and three archetypes.

## Dependencies

Prerequisite: T05. Blocks T07.

## Implementation Notes and Deliverables

Updated coordinator/navigator instructions, templates, gates, versioned state notes, current skills documentation, and targeted regression tests. Integrate documented procedures and executable validation, not an assumed nonexistent gate runtime.

## References

- [Workflow analysis](../artifacts/Analysis/implementation-analysis.md)
- [Orchestrator](../../../../.github/skills/edps-workflow-orchestrator/SKILL.md)
