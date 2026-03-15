# T10: Create Hierarchy Validation Tools

**Task ID**: T10  
**Phase**: Phase 3 - EDPS Compliance & Validation  
**Priority**: High  
**Estimated Effort**: 2-3 days  
**Status**: Completed  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026 (test rerun)  
**Completed**: March 14, 2026

## Description

Create validation tools that ensure hierarchy consistency across all levels. Validates boundary rules, participant type consistency, level appropriateness, and cross-reference integrity throughout the process hierarchy.

## Objectives

- Detect hierarchy inconsistencies across levels
- Validate participant type consistency in decompositions
- Check boundary rule compliance at every level
- Report validation results with actionable suggestions

## Detailed Requirements

### Functional Requirements
- **FR-T10.1**: Validate that decomposed control-type participants correctly appear as external actors at sub-level
- **FR-T10.2**: Verify participant type consistency (a control at Level N remains control context at N+1)
- **FR-T10.3**: Check all boundary rules (single actor, boundary-first, control-only decomposition) at every level
- **FR-T10.4**: Validate cross-reference link integrity between all hierarchy levels
- **FR-T10.5**: Generate validation report with per-level and per-rule results

### Technical Requirements
- **TR-T10.1**: Traverse full hierarchy tree for comprehensive validation
- **TR-T10.2**: Support incremental validation (validate single branch without full tree scan)

## Acceptance Criteria

### Must Have
- [x] Detect hierarchy inconsistencies across levels
- [x] Validate participant type consistency in decompositions
- [x] Check boundary rule compliance at every level
- [x] Report validation results with actionable suggestions

### Should Have
- [x] Incremental validation for single branch changes
- [x] Severity classification (error vs. warning)
- [x] Auto-fix suggestions for common issues

## Implementation Summary

- Created new `hierarchy-validation` skill at `.github/skills/hierarchy-validation/SKILL.md`
- Implements 14 validation rules across 3 groups:
  - **Group HV** (HV-1 through HV-5): Hierarchy structure — participant type consistency across decomposition levels
  - **Group HX** (HX-1 through HX-5): Cross-reference integrity — parent navigation, child sub-process links, and relative path correctness
  - **Group HN** (HN-1 through HN-4): Naming and metadata — folder naming conventions, `hierarchy-metadata.json` integrity, and level-depth consistency
- Supports full-tree scan and incremental validation of a single branch
- Error severity classification: ERROR (structural violations) and WARNING (advisory concerns)
- Generates `hierarchy-validation-report.json` and `hierarchy-validation-report.md` with per-level and per-rule results
- Auto-fix pass reconstructs broken relative paths (HX-1/HX-2); structural ERROR fixes (HV-*, HN-1/2/3) require manual resolution
- **Defect fixed**: D-T10-01 — clarified auto-fix scope; removed HX-1/HX-2 from structural ERROR exclusion list

## Dependencies

### Prerequisites
- **Task Dependencies**: T5 (Hierarchy Management), T4 (Boundary Validation)

### Blocking/Blocked By
- **Blocks**: T16 (Performance Testing)
- **Blocked By**: T5, T4

## Test Cases

### Test Case 1: Cross-Level Type Consistency
**Given**: Level 0 has control-type "PaymentService"; Level 1 decomposes it
**When**: Hierarchy validation runs
**Then**: Validates PaymentService appears as actor at Level 1 with consistent context

### Test Case 2: Broken Cross-Reference
**Given**: Level 1 main.md references deleted Level 2 sub-folder
**When**: Hierarchy validation runs
**Then**: Error reported: broken cross-reference link with location

**Full test suite**: 34 test cases across 7 categories — [T10-test-cases.md](../artifacts/Testing/T10-test-cases.md)  
**Test results**: 34/34 passed (1 defect found and fixed: D-T10-01) — [T10-test-results.md](../artifacts/Testing/T10-test-results.md)  
**Rerun (March 14, 2026)**: 34/34 PASS — no regressions, no new defects

---

**Related Documents**:
- [Initial Requirements - R-306](../artifacts/Requirements/initial-requirements.md)
- [Boundary Concepts - Validation Rules](../artifacts/Analysis/boundary-concepts.md)
