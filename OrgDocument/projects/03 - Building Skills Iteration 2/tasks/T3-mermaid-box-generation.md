# T3: Add Mermaid Box Syntax Generation

**Task ID**: T3  
**Phase**: Phase 1 - Foundation Enhancement  
**Priority**: High  
**Estimated Effort**: 2-3 days  
**Status**: Not Started  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

Implement Mermaid `box` syntax generation for creating boundary boxes in collaboration diagrams. This task handles the proper formatting, participant grouping, nesting, and boundary naming conventions required for hierarchical EDPS modeling.

## Objectives

- Generate valid Mermaid `box ... end` syntax for boundary grouping
- Support multiple boundaries within a single diagram
- Implement proper participant ordering within boxes
- Create descriptive boundary naming conventions

## Detailed Requirements

### Functional Requirements
- **FR-T3.1**: Generate `box BoundaryName ... end` syntax blocks with grouped participants
- **FR-T3.2**: Support multiple non-overlapping boundaries in a single sequence diagram
- **FR-T3.3**: Order participants within boxes: boundary-type first, then control-types, then entity-types
- **FR-T3.4**: Generate descriptive boundary names from context (e.g., "E-commerce Platform Boundary")

### Technical Requirements
- **TR-T3.1**: Produce syntactically valid Mermaid that renders in VS Code preview
- **TR-T3.2**: Handle edge cases: single-participant boundaries, external participants outside all boxes
- **TR-T3.3**: Support optional boundary styling/color customization

### Business Requirements
- **BR-T3.1**: Boundary boxes must visually communicate system decomposition to stakeholders
- **BR-T3.2**: Generated syntax must be human-readable and maintainable

## Acceptance Criteria

### Must Have
- [ ] Generate valid Mermaid `box` syntax for boundary grouping
- [ ] Support multiple boundaries in single diagram
- [ ] Proper participant ordering within boxes (boundary → control → entity)
- [ ] Descriptive boundary naming conventions

### Should Have
- [ ] Support boundary color/styling options
- [ ] Handle external participants outside all boundaries correctly
- [ ] Generate boundary summary comments in Mermaid output

### Could Have
- [ ] Support nested box syntax if Mermaid adds support
- [ ] Generate alternative visualization for boundaries exceeding Mermaid limits

## Implementation Approach

### Phase 1: Syntax Design
1. Document Mermaid `box` syntax capabilities and limitations
2. Design boundary grouping algorithm
3. Define naming conventions for auto-generated boundary names

### Phase 2: Generator Implementation
1. Build box syntax template generator
2. Implement participant grouping and ordering logic
3. Add boundary naming from context analysis
4. Handle edge cases (empty boundaries, overlapping requests)

### Phase 3: Validation
1. Test with VS Code Mermaid preview
2. Validate against example diagrams from hierarchy-examples.md
3. Performance test with complex multi-boundary diagrams

## Dependencies

### Prerequisites
- **Task Dependencies**: T1 (Enhance Collaboration Skill)
- **Artifact Dependencies**: Mermaid box syntax documentation, boundary-concepts.md
- **Technical Dependencies**: Mermaid renderer with box syntax support

### Blocking/Blocked By
- **Blocks**: T4 (Boundary Validation Rules)
- **Blocked By**: T1 (Enhance Collaboration Skill)

## Deliverables

### Primary Deliverables
- [ ] Box syntax generation templates and logic
- [ ] Multi-boundary rendering capability
- [ ] Boundary naming convention specification

### Supporting Deliverables
- [ ] Mermaid syntax validation test suite
- [ ] Rendering compatibility report (VS Code)
- [ ] Edge case handling documentation

## Test Cases

### Test Case 1: Single Boundary Generation
**Given**: Participants {User(actor), WebUI(boundary), OrderService(control), DB(entity)}
**When**: Box syntax generation groups WebUI, OrderService, DB into boundary
**Then**: Valid `box ... end` syntax with User external, others inside boundary

### Test Case 2: Multi-Boundary Generation
**Given**: E-commerce system with Platform, Payment, and Fulfillment boundaries
**When**: Box syntax generation creates three separate boundaries
**Then**: Three valid `box ... end` blocks with proper participant distribution

### Test Case 3: Participant Ordering
**Given**: Boundary containing control, entity, and boundary participants
**When**: Participants are ordered within the box
**Then**: Boundary-type first, then control-types, then entity-types

## Risks & Mitigation

### Risk 1: Mermaid Box Syntax Limitations
**Probability**: Medium  
**Impact**: High  
**Mitigation**: Thoroughly test box nesting capabilities; develop fallback notation using `rect` or notes

---

**Related Documents**:
- [Initial Requirements - R-302](../artifacts/Requirements/initial-requirements.md)
- [Boundary Concepts Analysis](../artifacts/Analysis/boundary-concepts.md)
- [Hierarchy Examples](../artifacts/Sample%20Data/hierarchy-examples.md)
