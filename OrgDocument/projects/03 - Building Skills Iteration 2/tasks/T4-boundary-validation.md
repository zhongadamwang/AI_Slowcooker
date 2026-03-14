# T4: Create Boundary Validation Rules

**Task ID**: T4  
**Phase**: Phase 1 - Foundation Enhancement  
**Priority**: High  
**Estimated Effort**: 2-3 days  
**Status**: Done  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026
**Completed**: March 14, 2026

## Description

Implement boundary validation rules ensuring correctness of generated hierarchical collaboration diagrams. Rules enforce single external interface, cohesive responsibility, boundary-first reception, and control-only decomposition patterns as defined by EDPS methodology.

## Objectives

- Enforce single-actor-to-boundary interaction rule
- Validate boundary-type participants receive actor messages first
- Validate only control-type participants are marked for decomposition
- Generate clear warnings and error messages for boundary rule violations

## Detailed Requirements

### Functional Requirements
- **FR-T4.1**: Validate that each boundary has exactly one external actor interface
- **FR-T4.2**: Validate boundary-type participants are first message recipients from actors
- **FR-T4.3**: Validate only control-type participants are flagged for decomposition
- **FR-T4.4**: Validate cohesive responsibility — all participants in a boundary should share related functionality
- **FR-T4.5**: Generate validation report with pass/fail indicators and actionable suggestions

### Technical Requirements
- **TR-T4.1**: Integrate validation into diagram generation pipeline (pre-render check)
- **TR-T4.2**: Support both strict mode (block invalid diagrams) and advisory mode (warn only)
- **TR-T4.3**: Produce machine-readable validation results for downstream processing

### Business Requirements
- **BR-T4.1**: Ensure all generated diagrams comply with EDPS boundary rules
- **BR-T4.2**: Provide actionable feedback to help users correct boundary issues

## Acceptance Criteria

### Must Have
- [x] Enforce single-actor-to-boundary interaction rule
- [x] Validate boundary-type participant receives actor messages first
- [x] Validate only control-type participants marked for decomposition
- [x] Generate clear warnings for boundary rule violations

### Should Have
- [x] Support strict and advisory validation modes
- [x] Validate cohesive responsibility within boundaries
- [x] Generate validation summary with pass/fail indicators

### Could Have
- [ ] Auto-fix simple boundary violations (reorder message recipients)
- [ ] Suggest boundary reorganization for complex violations

## Dependencies

### Prerequisites
- **Task Dependencies**: T1, T2, T3
- **Artifact Dependencies**: Boundary validation rules from boundary-concepts.md

### Blocking/Blocked By
- **Blocks**: T5 (Hierarchy Management), T10 (Hierarchy Validation)
- **Blocked By**: T1, T2, T3

## Test Cases

### Test Case 1: Valid Single-Actor Boundary
**Given**: Boundary with one external actor and properly typed internal participants
**When**: Validation is run
**Then**: All rules pass, no warnings

### Test Case 2: Invalid Multi-Actor Boundary
**Given**: Boundary where two external actors send messages directly inside
**When**: Validation is run
**Then**: Failure on single-actor rule with suggestion to split boundary

### Test Case 3: Invalid Decomposition Target
**Given**: Entity-type participant marked for decomposition
**When**: Validation is run
**Then**: Failure on control-only decomposition rule

### Test Case 4: Boundary-First Reception Violation
**Given**: Actor sends first message to control-type (skipping boundary-type)
**When**: Validation is run
**Then**: Warning with suggestion to route through boundary-type first

---

**Related Documents**:
- [Initial Requirements - R-302, R-310](../artifacts/Requirements/initial-requirements.md)
- [Boundary Concepts Analysis - Validation Rules](../artifacts/Analysis/boundary-concepts.md)
- [Test Cases](../artifacts/Testing/T4-test-cases.md)
- [Test Results](../artifacts/Testing/T4-test-results.md)
