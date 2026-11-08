# T02 - Build Boundary-Scoped Use-Case Models and Scripts

**Task ID**: T02  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 3.17 person-days (PERT)  
**Status**: Not Started  
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-07

## Description and Objectives

Create proposed `usecase-generatemodel` to describe actor interactions at every identified system-boundary level, with linked scripts explaining the detailed process.

## Detailed Requirements

Sources: R-003, R-004, R-007, R-008.

- Consume requirements, scoped process/domain/collaboration documents, and the shared boundary contract.
- Produce model Markdown/JSON and one script per modeled use case; identify actors, goals, boundary, hierarchy level, and source requirements.
- Scripts cover trigger, preconditions, ordered actor/system steps, applicable alternatives/exceptions, and postconditions. Link applicable process activities and entities.
- Preserve IDs and authored content on revisions; do not restrict actors to humans or use cases to software/leaf boundaries. UI links are optional by applicability.

## Acceptance Criteria

- [ ] Model has complete boundary/actor/requirement references at three hierarchy levels.
- [ ] Every modeled use case has a linked detailed script with the required sections.
- [ ] Non-software and system-actor interactions generate use cases without invented UI screens.
- [ ] Revision preserves existing identities and exposes unresolved references rather than silently guessing.

## Validation Tests

Valid and incomplete-input examples; script/model coverage; non-software parent and software child scenarios; repeated generation preserving IDs.

## Dependencies

Prerequisite: T01. Blocks T05.

## Implementation Notes and Deliverables

Skill instructions, gate, model/script templates, examples, and focused contract tests; meaningful indexes in generated script directories.

## References

- [Shared-contract task](T01-define-modeling-contract.md)
- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
