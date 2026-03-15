# T7: Cross-Reference Navigation — Test Results

**Task ID**: T7  
**Executed**: March 14, 2026  
**Skill Under Test**: `.github/skills/hierarchy-management/SKILL.md` (§4 Navigation template, §7 Cross-Reference Maintenance, §Cross-Reference Navigation)  
**Overall Result**: ✓ ALL PASSED — 26/26

---

## Evaluation Method

Each test case was evaluated by inspecting the `hierarchy-management` SKILL.md against the test's Given/When/Then conditions. The following sections of the skill were checked for each category:

| Category | SKILL.md Section(s) Checked |
|----------|----------------------------|
| Parent → Child Sub-Processes Table | §7a, §5 (parent main.md update) |
| Child → Parent Navigation Links & Breadcrumb | §4 main.md template, §4 Breadcrumb Construction Rules, §7b |
| Hierarchy Index Generation | §Cross-Reference Navigation / Hierarchy Index at Root Level |
| Link Integrity Check | §7c |
| Auto-Fix Renamed Paths | §7c (rename fix), §7c LINK-UPDATE log |
| Rebuild All Links Pass | §Cross-Reference Navigation / Generate Navigation Links for an Existing Hierarchy |
| Rollback Cross-Reference Cleanup | §7d, §Decomposition Rollback, §Cross-Reference Navigation / Hierarchy Index |

---

## Results by Category

### Category 1: Parent → Child Sub-Processes Table

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-001 | Sub-Processes section created when absent | PASS | §7a: "Locate (or create) the ## Sub-Processes section"; format matches §5 template exactly |
| TC-T7-002 | Second sub-process appended, not duplicated | PASS | §7a: "Add one row per sub-process sorted by ordinal prefix. If a row already exists … do not duplicate it." |
| TC-T7-003 | Re-running maintenance is idempotent | PASS | Same de-duplication rule; no changes emitted when all rows already present |
| TC-T7-004 | Stale row detected when folder deleted | PASS | §7c collects `{ file, link_text, target_path, issue }` and offers to remove stale row |

### Category 2: Child → Parent Navigation Links and Breadcrumb

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-005 | Level 1 parent link and breadcrumb | PASS | §4 template: `**Parent Process**: [[ParentProcessName]](../main.md)`; breadcrumb current level = plain text |
| TC-T7-006 | Level 2 two-hop breadcrumb | PASS | §4 Breadcrumb Construction Rules: count `../` steps per ancestor; root = `../../main.md` at L2 |
| TC-T7-007 | Level 5 five-hop breadcrumb | PASS | Same rules — no depth limit; root at L5 = `../../../../../main.md` |
| TC-T7-008 | Root has no parent link or breadcrumb | PASS | §Cross-Reference Navigation rebuild pass: "skip for root"; §4 template applies only to Level N+1 |
| TC-T7-009 | Level field corrected if mismatched | PASS | §7b: "Confirm **Level**: [N+1] matches folder depth. If discrepancy found, update in place." |

### Category 3: Hierarchy Index Generation

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-010 | Flat hierarchy index — 3 rows, correct stats | PASS | §Hierarchy Index: breadth-first table, Statistics section with Total Levels/Processes/Leaf Processes |
| TC-T7-011 | 3-level multi-branch — 4 rows, correct styles | PASS | §Hierarchy Index: node colors per level `#e1f5fe`, `#e8f5e8`, `#fff3e0` |
| TC-T7-012 | Mermaid click directives use root-relative paths | PASS | §Hierarchy Index template: `click L2A "01-OrderServiceBoundary/01-ValidationEngineBoundary/main.md"` |
| TC-T7-013 | hierarchy-index.md only at root | PASS | §Hierarchy Index: "`hierarchy-index.md` is always at the root process folder; it is **not** created inside sub-folders." |
| TC-T7-014 | Index regenerated after new decomposition | PASS | §Hierarchy Index: "Regenerate `hierarchy-index.md` after every decomposition and every rollback." |
| TC-T7-015 | Index regenerated after rollback | PASS | Same regeneration rule; §Decomposition Rollback triggers index rebuild |

### Category 4: Link Integrity Check

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-016 | Clean hierarchy — "All navigation links verified ✓" | PASS | §7c: "If no broken links: confirm 'All navigation links verified ✓'." |
| TC-T7-017 | Broken parent link detected | PASS | §7c: walks all main.md, resolves each link in Navigation and Sub-Processes, reports `target-not-found` |
| TC-T7-018 | Broken breadcrumb after rename — auto-fix offered | PASS | §7c: "Offer to auto-fix relative paths where the target file exists but the path changed" |
| TC-T7-019 | All broken links reported in single scan | PASS | §7c: collects full broken-link list before reporting; no early exit |

### Category 5: Auto-Fix Renamed Paths

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-020 | Renamed folder — all referencing files updated, LINK-UPDATE log written | PASS | §7c: "Replace the old ordinal/name segment in every affected path"; LINK-UPDATE log entry with old/new/reason |
| TC-T7-021 | Auto-fix only touches Navigation/Sub-Processes links | PASS | §7c: "For each `[text](path)` link in `## Navigation` and `## Sub-Processes`" — scope limited to those sections |
| TC-T7-022 | Genuinely deleted target — no auto-fix offered | PASS | §7c: "Offer to auto-fix … where the target file exists but the path changed" — target must exist for offer to trigger |

### Category 6: Rebuild All Links Pass

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-023 | Full rebuild on hierarchy with no existing navigation | PASS | §Cross-Reference Navigation: discover all main.md → build parent/children maps → write Navigation + Sub-Processes → run integrity check |
| TC-T7-024 | Rebuild pass is idempotent | PASS | De-duplication rule (§7a) + §7b no-change-if-matches ensures second pass produces no modifications |

### Category 7: Rollback Cross-Reference Cleanup

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T7-025 | Rollback removes sub-process row from parent | PASS | §7d: "Remove the sub-process row from the parent's ## Sub-Processes table." |
| TC-T7-026 | Rollback triggers hierarchy-index.md regeneration | PASS | §Hierarchy Index: "Regenerate after every decomposition and every rollback"; §Decomposition Rollback triggers this |

---

## Summary

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| Parent → Child Sub-Processes Table | 4 | 4 | 0 |
| Child → Parent Navigation Links and Breadcrumb | 5 | 5 | 0 |
| Hierarchy Index Generation | 6 | 6 | 0 |
| Link Integrity Check | 4 | 4 | 0 |
| Auto-Fix Renamed Paths | 3 | 3 | 0 |
| Rebuild All Links Pass | 2 | 2 | 0 |
| Rollback Cross-Reference Cleanup | 2 | 2 | 0 |
| **Total** | **26** | **26** | **0** |

**Requirements Coverage Result**

| FR | Description | Tests | Status |
|----|-------------|-------|--------|
| FR-T7.1 | Parent link in sub-process main.md | TC-T7-005 – TC-T7-009 | ✓ Covered |
| FR-T7.2 | Sub-process links in parent main.md | TC-T7-001 – TC-T7-004 | ✓ Covered |
| FR-T7.3 | Hierarchy index at root level | TC-T7-010 – TC-T7-015 | ✓ Covered |
| FR-T7.4 | Link integrity on hierarchy changes | TC-T7-016 – TC-T7-022 | ✓ Covered |

No defects found. All functional requirements fully satisfied by the SKILL.md implementation.
