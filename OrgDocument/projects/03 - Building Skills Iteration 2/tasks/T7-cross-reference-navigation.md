# T7: Build Cross-Reference Navigation

**Task ID**: T7  
**Phase**: Phase 2 - Hierarchy Management  
**Priority**: Medium  
**Estimated Effort**: 2-3 days  
**Status**: Done  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 14, 2026  
**Completed**: March 14, 2026

## Description

Implement bi-directional navigation between hierarchy levels. Each process level's main.md includes links to parent and child processes, and a hierarchy index provides an overview of the full decomposition tree.

## Objectives

- Generate parent process links in sub-process main.md files
- Generate sub-process links in parent main.md files
- Maintain link integrity when hierarchy changes
- Generate process hierarchy index at root level

## Detailed Requirements

### Functional Requirements
- **FR-T7.1**: Add "Parent Process" section with relative link to parent's main.md
- **FR-T7.2**: Add "Sub-Processes" section with relative links to each child's main.md
- **FR-T7.3**: Generate hierarchy index showing full tree structure with links
- **FR-T7.4**: Update links when hierarchy is restructured (add/remove levels)

### Technical Requirements
- **TR-T7.1**: Use relative markdown links for portability
- **TR-T7.2**: Maintain link integrity through hierarchy modifications

## Acceptance Criteria

### Must Have
- [x] Parent process links in sub-process main.md
- [x] Sub-process links in parent main.md
- [x] Link integrity maintained when hierarchy changes
- [x] Process hierarchy index at root level

### Should Have
- [x] Breadcrumb trail showing full path from root to current level
- [x] Visual hierarchy tree in index using markdown

## Dependencies

### Prerequisites
- **Task Dependencies**: T5 (Hierarchy Management), T6 (Sub-Folder Generation)

### Blocking/Blocked By
- **Blocks**: T11 (Change Impact Analysis), T12 (Documentation Automation)
- **Blocked By**: T5, T6

## Test Cases

### Test Case 1: Bi-Directional Links
**Given**: Level 0 → Level 1 decomposition
**When**: Cross-references are generated
**Then**: Level 0 main.md links to Level 1; Level 1 main.md links back to Level 0

### Test Case 2: Hierarchy Index
**Given**: 3-level hierarchy with multiple branches
**When**: Index is generated at root
**Then**: Full tree structure displayed with working links to all levels

## Implementation Notes

- Extended `.github/skills/hierarchy-management/SKILL.md` with:
  - **§4 `main.md` template**: Added `## Navigation` section containing breadcrumb trail, **Parent Process** link, and a **Sub-Processes** notice (FR-T7.1). Breadcrumb construction rules specify how to walk the folder hierarchy and build relative `../` paths to all ancestor levels.
  - **§7 Cross-Reference Navigation Maintenance** (new workflow step): 
    - §7a — parent → child links: ensures `## Sub-Processes` table in parent `main.md` is complete and de-duplicated (FR-T7.2)
    - §7b — child → parent links: verifies parent link and breadcrumb depth match actual folder nesting (FR-T7.1)
    - §7c — Link Integrity Check: walks all `main.md` files, resolves every navigation link, reports broken links, and auto-fixes renamed paths; logs changes to `folder-creation.log` (FR-T7.4)
    - §7d — rollback cross-reference cleanup
  - **§Cross-Reference Navigation** (new top-level section):
    - Rebuild-all-links pass for pre-existing hierarchies without navigation
    - **Hierarchy Index at Root Level** (`hierarchy-index.md`): flat table (sorted breadth-first), Mermaid `flowchart TD` with `click` directives, and summary statistics table (FR-T7.3); regenerated after every decomposition and rollback
- 24 test cases written and passing (see artifacts/Testing/T7-test-cases.md)

---

**Related Documents**:
- [Initial Requirements - R-304](../artifacts/Requirements/initial-requirements.md)
- [Hierarchy Examples - Navigation](../artifacts/Sample%20Data/hierarchy-examples.md)
- [Test Cases](../artifacts/Testing/T7-test-cases.md) — 26 test cases across 7 categories, all passing
- [Test Results](../artifacts/Testing/T7-test-results.md) — 26/26 passed, March 14, 2026
