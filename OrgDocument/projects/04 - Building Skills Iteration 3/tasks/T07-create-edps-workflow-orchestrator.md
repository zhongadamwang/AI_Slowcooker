# Create edps-workflow-orchestrator Skill

**Task ID**: T07  
**Phase**: Phase 3 - Advanced Methodology Enforcement  
**Priority**: P1-High  
**Estimated Effort**: 4-5 days  
**Status**: Not Started  
**Assigned**: [Engineering Team]  
**Created**: March 16, 2026  
**Last Updated**: March 16, 2026

## Description

Create a new `edps-workflow-orchestrator` skill that acts as a central coordinator for complete EDPS methodology workflows. This skill manages the full lifecycle of an EDPS process from requirements ingestion through final documentation, enforcing proper sequencing, validating completion gates, and providing holistic project state awareness across all EDPS skills.

Builds directly on the enhanced orchestration framework delivered by T06.

## Objectives

- **Primary**: Implement end-to-end EDPS workflow orchestration from requirements to final artifacts
- **Primary**: Enforce methodology sequencing rules and prevent skill execution out of order
- **Secondary**: Provide shared project state context across all EDPS skill invocations
- **Secondary**: Generate workflow progress reports with next-step recommendations

## Detailed Requirements

### Functional Requirements
- **FR-07.1**: Define canonical EDPS workflow sequences covering all 30 skills
- **FR-07.2**: Enforce prerequisite gating – blocked skills must not execute until dependencies are satisfied
- **FR-07.3**: Maintain a persistent project state object updated after each skill execution
- **FR-07.4**: Support workflow branching for different EDPS project archetypes (standard, rapid, compliance-focused)
- **FR-07.5**: Provide real-time workflow progress visualization with completed/blocked/available steps
- **FR-07.6**: Emit workflow events consumed by T08 completion gates

### Technical Requirements
- **TR-07.1**: Skill SKILL.md must follow the established skill format from `.github/skills/skill-creator/SKILL.md`
- **TR-07.2**: Workflow state must be serializable to JSON for persistence across Copilot sessions
- **TR-07.3**: Dependency graph must support directed acyclic graph (DAG) structure for complex workflows
- **TR-07.4**: Integration interface must match patterns established by T06 enhanced edps-skill-navigator
- **TR-07.5**: All 30 existing skills must be addressable from the orchestrator without modification

### Non-Functional Requirements
- **NFR-07.1**: Workflow planning must complete within 3 seconds for sequences of up to 15 skills
- **NFR-07.2**: State serialization must not exceed 500KB for typical project contexts
- **NFR-07.3**: Skill SKILL.md must be self-contained with no external runtime dependencies

## Implementation Plan

### Approach
Design the orchestrator as a meta-skill that reads the existing skill catalogue, constructs a dependency graph, and provides guided workflow execution. Use the T06 NLP and orchestration engine for intent resolution, adding a higher-level workflow state machine on top.

### Key Steps
1. **Catalogue existing skills**: Document all 30 EDPS skills, their inputs, outputs, and dependencies
2. **Design workflow DAG schema**: Define JSON schema for workflow definitions and project state
3. **Implement workflow archetypes**: Create standard, rapid, and compliance-focused workflow templates
4. **Build prerequisite gate engine**: Logic to determine which skills are currently available vs. blocked
5. **Implement project state manager**: Persistent context object tracking completed artifacts and decisions
6. **Integrate with T06 navigator**: Connect to enhanced NLP and orchestration from T06
7. **Create progress reporting**: Workflow visualization and next-step recommendation outputs
8. **Write SKILL.md**: Full skill documentation following the SKILL.md format
9. **Integration test**: Validate with Phase 4 T10 testing framework and prior-project scenarios
10. **Register with edps-skill-navigator**: Ensure orchestrator is discoverable by name and intent

### Technical Considerations
- The orchestrator must remain a Copilot-native skill (no server-side state); state serialization in conversation context
- Workflow definitions should be data-driven (JSON/YAML) to allow easy addition of new skills
- Must handle partial execution resumption when a Copilot session is interrupted

## Deliverables

### Primary Deliverables
- **`edps-workflow-orchestrator` SKILL.md** – New skill in `.github/skills/edps-workflow-orchestrator/`
- **Workflow definition templates** – JSON files for standard, rapid, and compliance-focused archetypes
- **Project state schema** – JSON Schema for persistent workflow state

### Supporting Deliverables
- Skill catalogue JSON documenting all 30 EDPS skills and their dependency relationships
- Integration test results with T10 framework

## Acceptance Criteria

### Definition of Done
- [ ] SKILL.md created and follows established skill format
- [ ] All three workflow archetypes defined and tested
- [ ] Prerequisite gate engine correctly blocks out-of-order skill execution
- [ ] Project state persists correctly across simulated session breaks
- [ ] Integration with T06 edps-skill-navigator validated
- [ ] T10 integration tests pass for all workflow archetypes
- [ ] Documentation complete including usage examples

### Validation Tests
- **Test-07.1**: Execute a standard workflow archetype end-to-end; verify skill sequence and gating
- **Test-07.2**: Attempt out-of-order skill execution; verify gate correctly blocks and reports reason
- **Test-07.3**: Serialize and restore project state; verify workflow resumes correctly
- **Test-07.4**: Run rapid archetype; verify optimized skill sequence and parallel opportunities identified
- **Test-07.5**: Verify orchestrator is discoverable via edps-skill-navigator natural language queries

## Dependencies

### Prerequisites
- **T06** ✅ Complete – edps-skill-navigator enhanced orchestration framework
- Access to all 30 existing EDPS skill SKILL.md files for dependency mapping

### Blocks
- T08 – Skill Completion Gates (requires orchestrator event interface)
- T09 – Enhanced User Prompt Pattern Recognition (uses orchestrator workflow definitions)
- T10 – Integration Testing Framework (validates orchestrator workflows)

## Notes

**Parallel execution**: T05 (update project-document-management) can run concurrently with this task.  
**Strategic foundation**: T07 provides the workflow graph and state management that T08 and T09 build upon.
