# T5: Create Hierarchy Management Skill

**Task ID**: T5  
**Phase**: Phase 2 - Hierarchy Management  
**Priority**: High  
**Estimated Effort**: 3-4 days  
**Status**: Not Started  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

Create a new `hierarchy-management` skill for managing hierarchical process decomposition. This skill enables control-type participants to become sub-processes at Level N+1, tracks parent-child relationships between process levels, and orchestrates the creation of decomposed process artifacts.

## Objectives

- Decompose control-type participants into sub-processes with their own collaboration diagrams
- Support unlimited hierarchy depth (tested to 5+ levels)
- Maintain consistent modeling patterns across hierarchy levels
- Track parent-child relationships between process levels

## Detailed Requirements

### Functional Requirements
- **FR-T5.1**: Accept a control-type participant and generate a Level N+1 sub-process with its own collaboration diagram
- **FR-T5.2**: When decomposing, the parent participant becomes the external actor at the sub-level
- **FR-T5.3**: Sub-process must include a boundary-type participant as first recipient
- **FR-T5.4**: Track hierarchy metadata: level depth, parent process, child processes, decomposition status
- **FR-T5.5**: Support unlimited depth with practical testing to 5+ levels

### Technical Requirements
- **TR-T5.1**: Create new skill file at `.github/skills/hierarchy-management/SKILL.md`
- **TR-T5.2**: Integrate with enhanced diagram-generatecollaboration for diagram generation
- **TR-T5.3**: Output hierarchy metadata in JSON format for cross-referencing

### Business Requirements
- **BR-T5.1**: Enable progressive complexity management through incremental decomposition
- **BR-T5.2**: Support EDPS evolutionary development through iterative hierarchy refinement

## Acceptance Criteria

### Must Have
- [ ] Decompose control-type participants into sub-processes with own collaboration diagrams
- [ ] Support 5+ levels of hierarchy depth
- [ ] Maintain consistent patterns across levels (boundary-first, typed participants)
- [ ] Track parent-child relationships in hierarchy metadata

### Should Have
- [ ] Generate hierarchy tree visualization
- [ ] Support decomposition rollback (collapse sub-process back)
- [ ] Provide hierarchy statistics (depth, breadth, leaf count)

## Dependencies

### Prerequisites
- **Task Dependencies**: T1 (Enhanced Collaboration), T4 (Boundary Validation)
- **Artifact Dependencies**: Hierarchy examples, boundary concepts analysis

### Blocking/Blocked By
- **Blocks**: T6, T7, T8, T9, T10, T11
- **Blocked By**: T1, T4

## Test Cases

### Test Case 1: Basic Decomposition
**Given**: Level 0 diagram with control-type "OrderService" participant
**When**: OrderService is decomposed
**Then**: Level 1 sub-process created with OrderService as external actor and internal boundary+control+entity participants

### Test Case 2: Multi-Level Decomposition
**Given**: Level 0 → Level 1 → Level 2 hierarchy chain
**When**: A control-type at Level 2 is decomposed
**Then**: Level 3 sub-process created maintaining all boundary and type rules

### Test Case 3: Non-Decomposable Rejection
**Given**: Entity-type participant "CustomerDB"
**When**: Decomposition is attempted
**Then**: Rejection with message: "Only control-type participants can be decomposed"

---

**Related Documents**:
- [Initial Requirements - R-301](../artifacts/Requirements/initial-requirements.md)
- [Hierarchy Examples](../artifacts/Sample%20Data/hierarchy-examples.md)
- [Boundary Concepts Analysis](../artifacts/Analysis/boundary-concepts.md)
