# T12: Build Documentation Automation

**Task ID**: T12  
**Phase**: Phase 3 - EDPS Compliance & Validation  
**Priority**: Medium  
**Estimated Effort**: 2-3 days  
**Status**: Completed  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026  
**Completed**: March 14, 2026

## Description

Automate generation of process documentation at each hierarchy level following organizational standards. Each decomposed process automatically gets properly formatted documentation with hierarchy context, participant types, and boundary information.

## Objectives

- Auto-generate main.md with hierarchy context and navigation links
- Auto-generate process.md with level-appropriate detail
- Include participant types, boundary rules, and decomposition status
- Follow organizational documentation standards

## Detailed Requirements

### Functional Requirements
- **FR-T12.1**: Generate main.md with: overview, parent link, sub-process links, participant summary, boundary rules applied
- **FR-T12.2**: Generate process.md with: level-appropriate process flow, decision points, error handling
- **FR-T12.3**: Generate collaboration.md with: proper Mermaid diagrams using box syntax and stereotypes
- **FR-T12.4**: Generate domain-model.md with: entities relevant to this boundary level

### Technical Requirements
- **TR-T12.1**: Use templates consistent with existing OrgModel format
- **TR-T12.2**: Support template customization per organization needs

## Acceptance Criteria

### Must Have
- [x] Auto-generate main.md with hierarchy context and navigation
- [x] Auto-generate process.md with level-appropriate detail
- [x] Include participant types, boundary rules, and decomposition status
- [x] Follow organizational documentation standards

### Should Have
- [x] Auto-generate collaboration.md with validated Mermaid diagrams, stereotypes, and boundary coloring
- [x] Auto-generate domain-model.md with entities, attributes, and relationships inferred from collaboration diagrams
- [x] Template customization per organization needs (`doc-templates/` override directory with `{{variable_name}}` placeholders)

## Dependencies

### Prerequisites
- **Task Dependencies**: T6 (Sub-Folder Generation), T7 (Cross-Reference Navigation)

### Blocking/Blocked By
- **Blocks**: T15 (OrgModel Update)
- **Blocked By**: T6, T7

## Test Cases

### Test Case 1: Complete Documentation Generation
**Given**: New Level 2 decomposition of "OrderProcessor"
**When**: Documentation automation runs
**Then**: main.md, process.md, collaboration.md, domain-model.md generated with correct hierarchy context

**Full test suite**: 32 test cases across 8 categories — [T12-test-cases.md](../artifacts/Testing/T12-test-cases.md)  
**Test results**: 32/32 passed — [T12-test-results.md](../artifacts/Testing/T12-test-results.md)

---

## Implementation Summary

- Created `.github/skills/documentation-automation/SKILL.md` as a new standalone skill:
  - **§1 Determine Hierarchy Level and Process Name**: detects level from `hierarchy-metadata.json` or folder-path depth; derives friendly process name from PascalCase folder name stripping ordinal prefix and `Boundary` suffix (FR-T12.1).
  - **§2 Extract Participant Inventory**: parses `sequenceDiagram` block to build a participant registry with `alias`, `type`, `label`, `box_name`, and `involvement_count` per participant (FR-T12.1–FR-T12.4).
  - **§3 Generate `main.md`**: template includes breadcrumb navigation, parent process link, participant summary table, boundary rule evaluation (VR-1, VR-2, VR-3 compliance), and decomposition status table per control-type participant (FR-T12.1).
  - **§4 Generate `process.md`**: includes level identifier comment, parent process link, Mermaid `flowchart TD` inferred from collaboration.md message groups, loop/alt inference rules, boundary rules applied section, and error handling stubs (FR-T12.2).
  - **§5 Generate/Annotate `collaboration.md`**: validates existing diagrams and adds missing `@{ "type": "..." }` stereotypes, `%% BOUNDARY SUMMARY` comment blocks, and level-appropriate `box rgb(...)` colors; synthesizes new diagrams from parent context when none exists (FR-T12.3).
  - **§6 Generate `domain-model.md`**: class diagram with one class per participant (stereotype as CSS class), attributes inferred from message labels, relationships from arrow directions, key concepts table, and parent domain reference (FR-T12.4).
  - **§Level Content Guide**: table mapping Level 0–3+ to scope, overview tone, and process detail depth — ensures level-appropriate content across all generated files (TR-T12.1).
  - **§Template Customization**: describes `doc-templates/` override directory with `{{variable_name}}` placeholder syntax so organisations can provide their own templates (TR-T12.2).
  - **§Integration with Related Skills**: cross-references `hierarchy-management` (folder structure), `diagram-generatecollaboration` (EDPS validation), and `orgmodel-update` (downstream consumer).
  - **§Validation Checklist**: six post-generation checks to confirm correctness of all four output files.
- Registered in `.github/skills/INDEX.md` under **🎯 Domain Modeling** alongside `hierarchy-management`.
- **Post-test defect fixes** (2 defects found during test execution):
  - **D-T12-01**: Added acronym-handling rule to §1 PascalCase expansion — consecutive uppercase sequences (e.g., `EDPS`) preserved as a single word unit.
  - **D-T12-02**: Added `<!-- omit at Level 0 -->` to `## Relationships to Parent Domain` heading in §6 `domain-model.md` template, consistent with other Level 0 omissions.

---

**Related Documents**:
- [Initial Requirements - R-306](../artifacts/Requirements/initial-requirements.md)
- [OrgModel Structure](../../../orgModel/01%20-%20Skill%20Development%20Process/main.md)
