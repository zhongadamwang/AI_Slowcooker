# Integration Testing Framework

**Task ID**: T10  
**Phase**: Phase 4 - Integration and Testing (Continuous)  
**Priority**: P2-Medium  
**Estimated Effort**: 3-4 days  
**Status**: Not Started  
**Assigned**: [Engineering Team]  
**Created**: March 16, 2026  
**Last Updated**: March 16, 2026

## Description

Build a comprehensive integration testing framework that validates the complete EDPS skill orchestration system introduced in Project 04. The framework tests end-to-end workflows spanning multiple skills, verifies skill completion gates, validates prompt pattern routing, and ensures the edps-workflow-orchestrator coordinates all skills correctly.

This task runs continuously alongside other phases and provides shared test infrastructure for T11 and T12.

## Objectives

- **Primary**: Define and execute end-to-end workflow test scenarios covering each workflow archetype
- **Primary**: Validate skill completion gate behavior (hard blocks, soft warnings, bypass logging)
- **Secondary**: Establish reusable test fixtures and scenario templates for regression testing in T12
- **Secondary**: Produce a living test report updated after every skill enhancement

## Detailed Requirements

### Functional Requirements
- **FR-10.1**: Define ≥ 5 end-to-end workflow test scenarios (one per archetype + edge cases)
- **FR-10.2**: Test all 30 completion gate schemas with known-good and known-bad skill outputs
- **FR-10.3**: Validate prompt classifier routing for 50+ representative user prompts
- **FR-10.4**: Test workflow state persistence (serialize → restore → continue)
- **FR-10.5**: Validate parallel execution correctness for skills identified as independent
- **FR-10.6**: Produce structured test report in both JSON and Markdown formats

### Technical Requirements
- **TR-10.1**: Test scenarios defined as self-contained markdown documents in `artifacts/Testing/`
- **TR-10.2**: Test fixtures (sample inputs/outputs) stored in `artifacts/Sample Data/`
- **TR-10.3**: Test reports follow the format established in Project 03 validation reports
- **TR-10.4**: Each test scenario must be independently executable without shared mutable state

### Non-Functional Requirements
- **NFR-10.1**: Full test suite must complete in < 60 minutes
- **NFR-10.2**: Test coverage must touch every Phase 3 deliverable at least once
- **NFR-10.3**: Test report must be human-reviewable without additional tooling

## Implementation Plan

### Key Steps
1. **Define test scenarios**: One scenario per workflow archetype + 2 edge-case scenarios
2. **Create test fixtures**: Sample inputs and expected outputs for each scenario
3. **Develop gate test suite**: Known-good and known-bad outputs for all 30 gate schemas
4. **Build prompt routing test set**: 50+ labelled prompts for classifier validation (reuse T09 corpus)
5. **Implement state persistence tests**: Serialize/restore/resume workflow test cases
6. **Execute tests against Phase 3 deliverables**: Run as T07/T08/T09 become available
7. **Generate initial test report**: Baseline report for Phase 4 comparison
8. **Iterate based on failures**: Report issues back to owning tasks for remediation
9. **Publish final test report**: Complete report upon Phase 3 completion

## Deliverables

### Primary Deliverables
- **Integration test suite** – Scenario documents in `artifacts/Testing/integration-test-suite-v2.md`
- **Test fixtures** – Sample data in `artifacts/Sample Data/`
- **Integration test report** – JSON + Markdown in `artifacts/Testing/`

### Supporting Deliverables
- Gate test matrix (30 skills × known-good/known-bad)
- Prompt routing validation set (50+ labelled prompts)

## Acceptance Criteria

### Definition of Done
- [ ] ≥ 5 end-to-end workflow test scenarios defined and executed
- [ ] All 30 gate schemas tested with known-good and known-bad outputs
- [ ] 50+ prompt routing tests executed; ≥ 95% correct routing
- [ ] State persistence test passes (serialize → restore → resume)
- [ ] Test report generated in JSON and Markdown formats
- [ ] All Phase 3 deliverables touched by at least one test scenario
- [ ] No critical (P0) failures unresolved at phrase completion

### Validation Tests
- **Test-10.1**: Standard workflow archetype end-to-end passes without gate failures
- **Test-10.2**: Rapid archetype completes in expected time window with parallel optimization
- **Test-10.3**: Gate hard-block triggers correctly for missing required artifact
- **Test-10.4**: Prompt classifier routes 50+ holdout prompts with ≥ 95% accuracy
- **Test-10.5**: Workflow state serializes and restores without data loss

## Dependencies

### Prerequisites
- **T07** – edps-workflow-orchestrator (workflow archetypes to test)
- **T08** – Skill Completion Gates (gate schemas to test)
- **T09** – Enhanced User Prompt Pattern Recognition (prompt routing to test)

### Parallel execution
Can be developed in parallel with T07-T09; full execution requires their completion.

### Blocks
- T11 – Performance Validation (uses test infrastructure from T10)
- T12 – Regression Testing (uses test fixtures from T10)
