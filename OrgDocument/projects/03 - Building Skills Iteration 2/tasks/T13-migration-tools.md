# T13: Create Project 1 Migration Tools

**Task ID**: T13  
**Phase**: Phase 4 - Migration & Integration  
**Priority**: Medium  
**Estimated Effort**: 2-3 days  
**Status**: Completed  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 15, 2026  
**Completed**: March 15, 2026

## Description

Build migration utilities to convert existing flat Project 1 collaboration diagrams to hierarchical format with boundaries. Supports both full migration and incremental enhancement while preserving all existing metadata and requirement links.

## Objectives

- Import Project 1 collaboration diagrams without modification (backward compatibility)
- Convert flat diagrams to hierarchical format with boundary suggestions
- Preserve all existing requirement links and metadata
- Add participant type annotations to existing participants

## Detailed Requirements

### Functional Requirements
- **FR-T13.1**: Parse existing Project 1 collaboration-diagrams.md and collaboration-diagrams.json
- **FR-T13.2**: Analyze participants and suggest boundary groupings using boundary detection algorithms
- **FR-T13.3**: Add participant type annotations to existing participants
- **FR-T13.4**: Generate enhanced version alongside original (non-destructive migration)
- **FR-T13.5**: Preserve all requirement traceability links from original diagrams

### Technical Requirements
- **TR-T13.1**: Support both full batch migration and individual diagram enhancement
- **TR-T13.2**: Generate migration log documenting all changes made

## Acceptance Criteria

### Must Have
- [x] Import Project 1 collaboration diagrams without modification
- [x] Convert flat diagrams to hierarchical format with boundary suggestions
- [x] Preserve all existing requirement links and metadata
- [x] Add participant type annotations to existing participants

### Should Have
- [x] Non-destructive migration (keep originals)
- [x] Migration preview mode (show changes without applying)
- [x] Batch migration for all Project 1 diagrams

## Dependencies

### Prerequisites
- **Task Dependencies**: T1 (Enhanced Collaboration), T5 (Hierarchy Management)

### Blocking/Blocked By
- **Blocks**: T15 (OrgModel Update)
- **Blocked By**: T1, T5

## Test Cases

### Test Case 1: Backward Compatibility
**Given**: Existing Project 1 collaboration-diagrams.md
**When**: Migration tool imports it
**Then**: Original content preserved without any modification

### Test Case 2: Enhancement Migration
**Given**: Flat diagram with User, AuthService, Database participants
**When**: Migration to hierarchical format runs
**Then**: User tagged as actor, AuthService as control, Database as entity; boundary suggested for AuthService+Database

## Completion Notes

- Created new `migration-tools` skill at `.github/skills/migration-tools/SKILL.md`
- Implements 7-step workflow: source loading, stereotype inference (6 priority rules), boundary detection (4 grouping rules), enhanced diagram block generation, requirement traceability preservation, enhanced JSON generation, and migration log generation
- Stereotype inference delegates keyword heuristics from `diagram-generatecollaboration` §Participant Stereotype Classification
- Boundary box color palette aligned with `diagram-generatecollaboration` §Box Syntax Generation
- Non-destructive guarantee: originals never modified; enhanced counterparts written to `*-enhanced.*` files
- Supports `--mode preview` (default) and `--mode apply`; `--scope batch` (default) and `--scope diagram=<id>`
- **Defect fixed**: D-T13-01 — Rule 3 entity-type keywords expanded to include `Report`, `Artifact`, `Artifacts`, `Output`, `Document`, `Storage`, `Journal` (Project 1 participants like `ProjectArtifacts` and `AssessmentReport` were falling through to fallback)
- **Test results**: 22/22 test cases passed; 1 defect found and fixed
- **Test files**: [T13-test-cases.md](../artifacts/Testing/T13-test-cases.md), [T13-test-results.md](../artifacts/Testing/T13-test-results.md)

---

**Related Documents**:
- [Initial Requirements - R-309b](../artifacts/Requirements/initial-requirements.md)
- [Project 1 Collaboration Diagrams](../../01%20-%20Building%20Skills/artifacts/Analysis/collaboration-diagrams.md)
