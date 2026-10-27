# T07 — Author screen-generateflow Skill (Interaction Flow Diagrams)

**Task ID**: T07
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 1 day
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Implements R-603 (Interaction Flow Modeling) — gives the screen set a connective narrative (e.g., "Login → Dashboard → Order Detail"), reusing `diagram-generatecollaboration`'s existing Mermaid conventions rather than inventing a new diagramming approach.

## Objectives

- Author the flow generation skill producing Mermaid interaction-flow diagrams across the screen set

## Detailed Requirements

### Functional Requirements
- **FR-07.1**: Flow diagram's edges correspond to the actual navigation implemented in T06's mockups
- **FR-07.2**: Diagram style/syntax is consistent with `diagram-generatecollaboration`'s existing patterns

### Technical Requirements
- **TR-07.1**: Consistency between flow diagram and mockup is manually verified in MVP (automated check is the Phase 2 Enhancement feature, R-603a) — make this an explicit, non-skippable verification step in this task, not an afterthought

## Acceptance Criteria

- [ ] SKILL.md authored
- [ ] Flow diagram generated for a test screen set
- [ ] Manual verification performed confirming diagram edges match actual mockup transitions

## Dependencies

### Prerequisites
- **T04** — needs the screen set
- **T06** — needs actual mockup transitions to verify against

### Blocks
- T08 (design document summarizes flows)
