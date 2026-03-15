# T11: Add Change Impact Analysis Across Levels

**Task ID**: T11  
**Phase**: Phase 3 - EDPS Compliance & Validation  
**Priority**: Medium  
**Estimated Effort**: 2-3 days  
**Status**: Done  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026

## Description

Implement change impact analysis that traces how changes at one hierarchy level propagate to parent and child levels. Supports what-if analysis for proposed boundary modifications.

## Objectives

- Identify impacted levels when a boundary changes
- Trace requirement changes to affected process levels
- Generate change impact report with affected artifacts
- Support what-if analysis for proposed changes

## Detailed Requirements

### Functional Requirements
- **FR-T11.1**: Given a change at Level N, identify all affected artifacts at Levels N-1 and N+1
- **FR-T11.2**: Trace requirement changes to specific boundary and participant impacts
- **FR-T11.3**: Generate impact report listing affected files, links, and diagrams
- **FR-T11.4**: Support what-if mode: analyze impact of proposed changes without applying them

### Technical Requirements
- **TR-T11.1**: Leverage cross-reference links (T7) for impact tracing
- **TR-T11.2**: Integrate with change-management skill for change tracking

## Acceptance Criteria

### Must Have
- [x] Identify impacted levels when a boundary changes
- [x] Trace requirement changes to affected process levels
- [x] Generate change impact report with affected artifacts
- [x] Support what-if analysis for proposed changes

## Implementation Summary

- Created new `change-impact-analysis` skill at `.github/skills/change-impact-analysis/SKILL.md`
- Implements 8 impact rules across 2 groups:
  - **Group CI** (CI-1 through CI-5): Artifact-level impact tracing — parent reference impact (CI-1), child navigation cascade (CI-2), participant propagation (CI-3), hierarchy index impact (CI-4), and side-document impact (CI-5)
  - **Group CR** (CR-1 through CR-3): Requirement change tracing — artifact mapping (CR-1), boundary impact identification (CR-2), downstream propagation (CR-3)
- Supports `--mode what-if` (default, no file modifications) and `--mode apply` (auto-fixes navigational artifacts)
- Generates `change-impact-report.json` (machine-readable) and `change-impact-report.md` (human-readable) with 5-level risk classification (NONE/LOW/MEDIUM/HIGH/CRITICAL)
- `--depth N` option limits traversal scope for targeted analysis
- Output `change-impact-report.json` is directly compatible with `change-management` skill's `affected_documents` format
- **Test results**: 28/28 test cases passed; 2 defects found and fixed (D-T11-01: comment auto-fix scope; D-T11-02: depth-limit missing from report metadata)
- **Test files**: [T11-test-cases.md](../artifacts/Testing/T11-test-cases.md), [T11-test-results.md](../artifacts/Testing/T11-test-results.md)

## Dependencies

### Prerequisites
- **Task Dependencies**: T5 (Hierarchy Management), T7 (Cross-Reference Navigation)

### Blocking/Blocked By
- **Blocks**: None
- **Blocked By**: T5, T7

## Test Cases

### Test Case 1: Boundary Change Impact
**Given**: Level 1 boundary "OrderService" is restructured
**When**: Impact analysis runs
**Then**: Reports affected Level 0 (parent reference) and Level 2 (sub-processes within OrderService)

### Test Case 2: Requirement Change Trace
**Given**: Requirement R-302 is modified
**When**: Requirement-to-hierarchy tracing runs
**Then**: All hierarchy levels implementing R-302 boundary rules are identified

---

**Related Documents**:
- [Initial Requirements - R-306](../artifacts/Requirements/initial-requirements.md)
