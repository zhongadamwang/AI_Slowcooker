# T05 - Wire Existing Model Producers and UI Consumers

**Task ID**: T05  
**Phase**: 3 - Integration  
**Priority**: P0-Critical  
**Estimated Effort**: 2.17 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Apply the shared contract and validation handoff to existing modeling and UI skills without changing their intended responsibilities or prototype behavior.

## Detailed Requirements

Sources: R-001, R-002, R-005, R-007, R-008, R-009, R-010, R-011.

- Wire diagram/hierarchy/documentation/domain alignment/model integration/orgModel update surfaces to entity and boundary references.
- Extend process initialization and indexes for use-case models/scripts and applicable UI models; retain meaningful `main.md` in generated folders.
- Wire all six screen skills and affected gates through the UI model to software-boundary evidence, preserving standalone inventory, stable IDs, singular `ui_model_ref`, layouts, dialogs, and handoff.
- Propagate model-affecting changes/feedback to impacted models and validation rounds; avoid a global rewrite of historical projects.

## Acceptance Criteria

- [ ] Produced domain/process/use-case/UI artifacts validate together on a mixed-boundary example.
- [ ] All six screen skills retain traceability and the interactive prototype quality contract.
- [ ] Non-software UI rejection works through the model reference, without direct screen-to-domain coupling.
- [ ] Direct modeling invocations document end-of-round validation; affected changes invalidate reports.

## Validation Tests

Run new producer/consumer contract checks and the existing prototype regression command. Exercise change impact and non-applicable model paths.

## Dependencies

Prerequisites: T02, T03, T04. Blocks T06.

## Implementation Notes and Deliverables

Updated skill instructions/gates, source-reference handoffs, initialization/index rules, and compatibility examples.

## References

- [Impact surfaces](../artifacts/Analysis/implementation-analysis.md)
- [Existing prototype tests](../../../../.github/skills/screen-generatemockup/scripts/test_prototype_contract.py)
