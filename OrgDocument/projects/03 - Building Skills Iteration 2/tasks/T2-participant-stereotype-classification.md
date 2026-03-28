# T2: Implement Participant Stereotype Classification

**Task ID**: T2  
**Phase**: Phase 1 - Foundation Enhancement  
**Priority**: High  
**Estimated Effort**: 2-3 days  
**Status**: Completed  
**Assigned**: GitHub Copilot  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

Add participant type classification (actor, boundary, control, entity) to the enhanced collaboration diagram skill. Each participant in generated Mermaid diagrams will use the `@{ "type" : "..." }` annotation syntax to indicate its stereotype, enabling downstream decomposition rule enforcement.

## Objectives

- Classify all participants using standardized stereotypes (actor, boundary, control, entity)
- Generate Mermaid `@{ "type" : "..." }` annotations in participant definitions
- Apply decomposition rules based on participant type
- Ensure boundary-type participants are positioned as first recipients within boundaries

## Detailed Requirements

### Functional Requirements
- **FR-T2.1**: Classify participants into four types: actor (external initiators), boundary (interface mediators), control (business logic, decomposable), entity (data/resources)
- **FR-T2.2**: Generate Mermaid participant definitions with `@{ "type" : "actor|boundary|control|entity" }` annotation syntax
- **FR-T2.3**: Enforce control-only decomposition rule — only control-type participants can become sub-processes
- **FR-T2.4**: Enforce boundary-first reception rule — boundary-type participants must receive actor messages first within any boundary box

### Technical Requirements
- **TR-T2.1**: Integrate with T1's enhanced collaboration diagram generation
- **TR-T2.2**: Support both automatic type inference and manual type specification
- **TR-T2.3**: Generate valid Mermaid syntax with `@{ "type" }` metadata rendering

### Business Requirements
- **BR-T2.1**: Enable consistent participant classification across all hierarchy levels
- **BR-T2.2**: Support EDPS methodology alignment through typed decomposition rules

## Acceptance Criteria

### Must Have
- [x] Classify participants using actor/boundary/control/entity types
- [x] Generate Mermaid `@{ "type" : "..." }` annotations in participant definitions
- [x] Apply decomposition rules based on participant type
- [x] Ensure boundary participants receive actor messages first within boundaries

### Should Have
- [x] Support automatic type inference from interaction patterns
- [x] Allow manual type override in configuration
- [x] Generate participant type summary in diagram metadata

### Could Have
- [ ] Visual type indicators in generated documentation
- [x] Type statistics and distribution analysis

## Implementation Approach

### Phase 1: Type Classification Design
1. Define type inference rules from interaction patterns
2. Design type annotation syntax integration with Mermaid
3. Map existing Project 1 participants to new type system

### Phase 2: Classification Implementation
1. Implement automatic type classification based on:
   - External interaction patterns → actor
   - First-recipient-in-boundary patterns → boundary
   - Complex business logic patterns → control
   - Data/resource access patterns → entity
2. Add `@{ "type" : "..." }` annotation generation to Mermaid output
3. Implement manual type override mechanism

### Phase 3: Rule Enforcement
1. Implement decomposition eligibility check (control-only)
2. Implement boundary-first reception validation
3. Add type consistency verification across hierarchy levels

## Dependencies

### Prerequisites
- **Task Dependencies**: T1 (Enhance Collaboration Skill)
- **Artifact Dependencies**: Boundary concepts analysis, participant type definitions from requirements
- **Technical Dependencies**: Mermaid participant metadata syntax support

### Blocking/Blocked By
- **Blocks**: T4 (Boundary Validation Rules)
- **Blocked By**: T1 (Enhance Collaboration Skill)

## Deliverables

### Primary Deliverables
- [x] Participant type classification logic in enhanced skill
- [x] Mermaid `@{ "type" }` annotation generation
- [x] Decomposition rule enforcement logic

### Supporting Deliverables
- [x] Type classification test cases
- [x] Participant type reference documentation
- [ ] Type inference accuracy analysis

## Test Cases

### Test Case 1: Automatic Type Classification
**Given**: Collaboration diagram with User, WebUI, OrderService, CustomerDB participants
**When**: Stereotype classification is applied
**Then**: User=actor, WebUI=boundary, OrderService=control, CustomerDB=entity

### Test Case 2: Decomposition Rule Enforcement
**Given**: Participant classified as entity type
**When**: Decomposition into sub-process is attempted
**Then**: Decomposition is blocked with clear error message

### Test Case 3: Boundary-First Reception
**Given**: Boundary with boundary-type and control-type participants
**When**: Actor sends message into boundary
**Then**: Message routes to boundary-type participant first

## Risks & Mitigation

### Risk 1: Ambiguous Type Classification
**Probability**: Medium  
**Impact**: Medium  
**Mitigation**: Provide manual override option; document classification heuristics clearly

### Risk 2: Mermaid @{type} Rendering Issues
**Probability**: Low  
**Impact**: High  
**Mitigation**: Test with VS Code Mermaid preview; provide fallback annotation approach

## Definition of Done
- [x] All acceptance criteria met
- [x] Participant types correctly generated in Mermaid output
- [x] Decomposition rules enforced and tested
- [x] Documentation updated with type classification guide
- [x] Integration with T1 validated

---

**Related Documents**:
- [Initial Requirements - R-310](../artifacts/Requirements/initial-requirements.md)
- [Boundary Concepts Analysis](../artifacts/Analysis/boundary-concepts.md)
- [T1: Enhance Collaboration Skill](T1-enhance-collaboration-skill.md)
