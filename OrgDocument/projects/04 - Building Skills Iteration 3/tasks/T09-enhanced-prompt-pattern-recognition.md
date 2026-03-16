# Enhanced User Prompt Pattern Recognition

**Task ID**: T09  
**Phase**: Phase 3 - Advanced Methodology Enforcement  
**Priority**: P1-High  
**Estimated Effort**: 2-3 days  
**Status**: Not Started  
**Assigned**: [Engineering Team]  
**Created**: March 16, 2026  
**Last Updated**: March 16, 2026

## Description

Enhance user prompt pattern recognition so that ambiguous or high-level user utterances are automatically resolved to the correct EDPS skill or workflow, reducing the friction of skill invocation. This builds the T06 NLP engine and T07 workflow definitions into a classification layer that intercepts every user request before routing it.

## Objectives

- **Primary**: Map natural language user prompts to specific EDPS skills or workflow archetypes with ≥95% accuracy
- **Primary**: Surface disambiguation prompts when intent confidence is below threshold
- **Secondary**: Learn from user corrections to improve future recognition within a project session
- **Secondary**: Provide intent explanation so users understand which skill was selected and why

## Detailed Requirements

### Functional Requirements
- **FR-09.1**: Classify every user prompt against the full catalogue of 30 skills and 3 workflow archetypes
- **FR-09.2**: Return ranked results (top-3) with confidence scores when confidence < 85%
- **FR-09.3**: Generate disambiguation question when top-2 candidates are within 10% confidence of each other
- **FR-09.4**: Accept user correction and update session-level intent model
- **FR-09.5**: Explain matched intent in plain language before executing matched skill/workflow
- **FR-09.6**: Detect multi-step intent (e.g. "analyse requirements and create diagrams") and map to workflow archetype

### Technical Requirements
- **TR-09.1**: Extend T06 NLP engine patterns with workflow-level intent patterns from T07
- **TR-09.2**: Classification model must be embedded in SKILL.md (no external API calls)
- **TR-09.3**: Session-level corrections stored in project state object from T07
- **TR-09.4**: Disambiguation UI uses Copilot-native question/answer patterns (no custom UI)

### Non-Functional Requirements
- **NFR-09.1**: Classification latency must be < 500ms for single-skill prompts
- **NFR-09.2**: Disambiguation must not require more than one clarifying question per user request
- **NFR-09.3**: Intent explanation must be ≤ 2 sentences

## Implementation Plan

### Key Steps
1. **Collect prompt corpus**: Gather 200+ example prompts from project history and user feedback
2. **Define intent taxonomy**: Map prompts to skills and workflows using T07 workflow definitions
3. **Extend T06 NLP patterns**: Add workflow-level and multi-step intent patterns
4. **Implement classifier**: Build confidence-scored classification against intent taxonomy
5. **Build disambiguation flow**: Design minimal clarifying question generation
6. **Add session correction loop**: Implement correction capture and session-model update
7. **Create intent explanation templates**: Standard plain-language explanation per skill/workflow
8. **Integrate with edps-skill-navigator**: Plug classifier as pre-route interceptor
9. **Evaluate against prompt corpus**: Measure accuracy; iterate until ≥95% achieved
10. **Document recognition patterns**: Publish intent catalogue for user reference

## Deliverables

### Primary Deliverables
- **Enhanced intent classification module** – Integrated into edps-skill-navigator SKILL.md
- **Intent taxonomy document** – Full mapping of prompt patterns to skills/workflows
- **Prompt corpus** – 200+ labelled example prompts used for development and regression testing

### Supporting Deliverables
- Disambiguation flow specification
- Intent explanation templates for all 30 skills and 3 workflow archetypes

## Acceptance Criteria

### Definition of Done
- [ ] Classification accuracy ≥ 95% on prompt corpus (holdout set)
- [ ] Disambiguation question generated correctly when confidence gap < 10%
- [ ] Session correction captured and applied successfully
- [ ] Intent explanation shown before every skill/workflow execution
- [ ] Multi-step intent mapped to correct workflow archetype
- [ ] Integration tests with T10 pass
- [ ] Intent taxonomy document published

### Validation Tests
- **Test-09.1**: Submit 50 holdout prompts; verify ≥ 95% correct top-1 classification
- **Test-09.2**: Submit ambiguous prompt; verify disambiguation question is generated
- **Test-09.3**: Correct a misclassification; verify subsequent similar prompt uses corrected mapping
- **Test-09.4**: Submit multi-step prompt; verify workflow archetype is selected (not single skill)
- **Test-09.5**: Verify intent explanation is shown for every automated skill invocation

## Dependencies

### Prerequisites
- **T07** – edps-workflow-orchestrator (provides workflow archetype definitions used in classification)
- **T06** ✅ Complete – NLP engine extended by this task

### Blocks
- T10 – Integration Testing Framework (tests prompt routing end-to-end)
