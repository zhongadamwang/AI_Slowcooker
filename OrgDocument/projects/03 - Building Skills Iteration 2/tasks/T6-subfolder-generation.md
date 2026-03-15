# T6: Implement Sub-Folder Generation

**Task ID**: T6  
**Phase**: Phase 2 - Hierarchy Management  
**Priority**: Medium  
**Estimated Effort**: 2-3 days  
**Status**: Done  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026  
**Completed**: March 14, 2026

## Description

Implement automatic folder structure creation for decomposed processes. Each time a control-type participant is decomposed into a sub-process, a new sub-folder is created with standard files and naming conventions matching the OrgModel structure.

## Objectives

- Auto-create sub-folders for each process decomposition
- Follow consistent naming convention: `NN-BoundaryName/`
- Include standard files: main.md, collaboration.md, process.md, domain-model.md
- Populate templates with hierarchy context

## Detailed Requirements

### Functional Requirements
- **FR-T6.1**: Create sub-folder `NN-BoundaryName/` when a control-type participant is decomposed
- **FR-T6.2**: Generate standard files: main.md (overview), collaboration.md (diagram), process.md (flow), domain-model.md (entities)
- **FR-T6.3**: Populate templates with parent context, level depth, and boundary information
- **FR-T6.4**: Support folder generation at any hierarchy depth

### Technical Requirements
- **TR-T6.1**: Use sequential numbering (01, 02, ...) matching sibling order
- **TR-T6.2**: Handle naming collisions and special characters in boundary names
- **TR-T6.3**: Create folders within the existing OrgModel directory structure

## Acceptance Criteria

### Must Have
- [x] Auto-create `NN-BoundaryName/` sub-folder for each decomposition
- [x] Include main.md, collaboration.md, process.md, domain-model.md in each sub-folder
- [x] Consistent naming convention across all hierarchy levels
- [x] Templates populated with hierarchy context

### Should Have
- [x] Handle naming collisions gracefully
- [ ] Support custom template overrides
- [x] Generate folder creation log for audit

## Dependencies

### Prerequisites
- **Task Dependencies**: T5 (Hierarchy Management)

### Blocking/Blocked By
- **Blocks**: T7 (Cross-Reference Navigation), T12 (Documentation Automation)
- **Blocked By**: T5

## Test Cases

### Test Case 1: Basic Sub-Folder Creation
**Given**: Control-type "OrderService" is decomposed at Level 0
**When**: Sub-folder generation runs
**Then**: `01-OrderServiceBoundary/` created with all standard files

### Test Case 2: Multi-Level Folder Nesting
**Given**: Level 2 decomposition of "ValidationEngine" within OrderService
**When**: Sub-folder generation runs
**Then**: `01-OrderServiceBoundary/01-ValidationEngineBoundary/` created with standard files

---

**Related Documents**:
- [Initial Requirements - R-304](../artifacts/Requirements/initial-requirements.md)
- [Boundary Concepts - Folder Structure](../artifacts/Analysis/boundary-concepts.md)
- [Test Cases](../artifacts/Testing/T6-test-cases.md) — 24 test cases, all passing

## Implementation Notes

- Extended `.github/skills/hierarchy-management/SKILL.md` with:
  - §2a Special Character Sanitization rules and regex contract
  - §2b Naming Collision Resolution (exact/name/ordinal variants)
  - §4b `process.md` template with inferred flowchart from collaboration messages
  - §4c `domain-model.md` template with class diagram from participant types
  - §4d Folder Creation Audit Log (`folder-creation.log`) with `CREATED`/`REMOVED`/`OVERWRITE` entries
  - Updated Outputs section to list all four standard files + audit log
  - Updated Step 5 parent navigation to a four-column Sub-Processes table
  - Updated Rollback procedure to cover new files and log entry
  - Updated multi-level folder tree example to show full file set
