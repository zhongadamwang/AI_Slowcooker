# T10 — Gate & Orchestrator Registration (All New Skills)

**Task ID**: T10
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Implements R-621 (Gate & Workflow Orchestrator Integration) and R-622 (Collaboration-Mode Awareness) across all new skills from T04–T09. Ensures this skill set doesn't become a disconnected side-tool outside the orchestrator's DAG — consistent with how all 32 existing EDPS skills integrate.

## Objectives

- Author a `gate.json` for each new skill (T04–T09)
- Register all new skill IDs in `edps-workflow-orchestrator/SKILL.md`'s skill catalogue with correct DAG prerequisites

## Detailed Requirements

### Functional Requirements
- **FR-10.1**: Each new skill has a working `gate.json`
- **FR-10.2**: Orchestrator catalogue updated with correct prerequisite IDs reflecting the T04→T05→T06→(T07,T08,T09) dependency order

### Technical Requirements
- **TR-10.1**: Reuse the existing `stakeholder_confirmation` check type where relevant (per R-622) — do not invent a new approval mechanism
- **TR-10.2**: Where mode-aware severity applies, follow the `resolveCheckSeverity()` pattern from Iteration 4's orchestrator update

## Acceptance Criteria

- [ ] `gate.json` authored for each of T04–T09's skills
- [ ] Orchestrator catalogue updated with correct skill IDs and prerequisites
- [ ] `orchestrate status`/`orchestrate next` correctly surface the new skills in a test run
- [ ] Any stakeholder-confirmation checks use the existing check type, not a new mechanism

## Dependencies

### Prerequisites
- **T04, T05, T06, T07, T08, T09** — all skills must exist before their gates can be authored

### Blocks
- T11 (validation dry run exercises the full gated/orchestrated pipeline)
