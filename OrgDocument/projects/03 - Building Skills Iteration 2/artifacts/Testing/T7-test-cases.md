# T7: Cross-Reference Navigation — Test Cases

**Task ID**: T7  
**Created**: March 14, 2026  
**Status**: All 26 test cases executed and passed (March 14, 2026)

---

## Category 1: Parent → Child Sub-Processes Table (TC-T7-001 – TC-T7-004)

### TC-T7-001: Sub-Processes section created in parent main.md (no prior section)
**Given**: `01-OrderServiceBoundary/` has just been created; parent `main.md` contains no `## Sub-Processes` section  
**When**: Cross-reference navigation maintenance runs (§7a)  
**Then**:  
- A `## Sub-Processes` table with columns Sub-Process, Collaboration, Process Flow, Domain Model is inserted in the parent `main.md`  
- One row present: `[01-OrderServiceBoundary](01-OrderServiceBoundary/main.md)` with relative links to `collaboration.md`, `process.md`, and `domain-model.md`  
- All link targets resolve to existing files  
**Result**: PASS

### TC-T7-002: Second sub-process appended as new row (not duplicated)
**Given**: Parent `main.md` already has a `## Sub-Processes` table with a row for `01-OrderServiceBoundary/`; `02-PaymentEngineBoundary/` is newly created  
**When**: Cross-reference maintenance runs  
**Then**:  
- Table now has exactly two rows (OrderService and PaymentEngine)  
- Rows sorted by ordinal prefix (01 before 02)  
- Pre-existing row for `01-OrderServiceBoundary/` is unchanged  
**Result**: PASS

### TC-T7-003: Re-running maintenance does not duplicate existing rows
**Given**: Parent `main.md` already has a correctly populated `## Sub-Processes` table with two rows  
**When**: Cross-reference maintenance runs again  
**Then**: Table still has exactly two rows; no duplicates; no content modified  
**Result**: PASS

### TC-T7-004: Sub-process physically removed — stale row detected
**Given**: Parent `main.md` has a row linking to `02-PaymentEngineBoundary/` but that folder has been deleted  
**When**: Link Integrity Check runs (§7c)  
**Then**: Broken link reported: `{ file: "main.md", link_text: "02-PaymentEngineBoundary", target_path: "02-PaymentEngineBoundary/main.md", issue: "target-not-found" }`; user is offered option to remove the stale row  
**Result**: PASS

---

## Category 2: Child → Parent Navigation Links and Breadcrumb (TC-T7-005 – TC-T7-009)

### TC-T7-005: Level 1 main.md — correct parent link and breadcrumb
**Given**: `01-OrderServiceBoundary/` is a Level 1 sub-process of the root `SkillDevProcess/`  
**When**: `main.md` is generated (§4)  
**Then**:  
- `**Parent Process**: [Skill Dev Process](../main.md)` present  
- Breadcrumb: `[Skill Dev Process](../main.md) › Order Service Boundary`  
- Current level (`Order Service Boundary`) shown as plain text, not a link  
**Result**: PASS

### TC-T7-006: Level 2 main.md — two-hop breadcrumb
**Given**: `01-OrderServiceBoundary/01-ValidationEngineBoundary/` is Level 2; root is `SkillDevProcess/`  
**When**: `main.md` is generated  
**Then**:  
- `**Parent Process**: [Order Service Boundary](../main.md)` present  
- Breadcrumb: `[Skill Dev Process](../../main.md) › [Order Service Boundary](../main.md) › Validation Engine Boundary`  
- Relative link to root uses `../../main.md` (two hops up)  
**Result**: PASS

### TC-T7-007: Level 5 main.md — five-hop breadcrumb
**Given**: A 5-level deep hierarchy: Root → L1 → L2 → L3 → L4 → L5  
**When**: L5 `main.md` is generated  
**Then**:  
- Breadcrumb contains 5 ancestor links plus the current level as plain text  
- Each ancestor uses the correct number of `../` hops (Root = `../../../../../main.md`)  
- No dead links in the breadcrumb  
**Result**: PASS

### TC-T7-008: Root main.md — no parent link or breadcrumb
**Given**: The root process folder (Level 0) `main.md`  
**When**: Cross-reference maintenance runs  
**Then**: No `**Parent Process**` field and no `## Navigation` section breadcrumb are generated for the root; the `## Sub-Processes` table is still present if children exist  
**Result**: PASS

### TC-T7-009: Level field matches actual folder depth
**Given**: `01-OrderServiceBoundary/01-ValidationEngineBoundary/` is at folder depth 2  
**When**: §7b verification runs  
**Then**: `**Level**: 2` is confirmed in the child `main.md`; if it incorrectly states `Level: 1`, the file is updated and the discrepancy logged  
**Result**: PASS

---

## Category 3: Hierarchy Index Generation (TC-T7-010 – TC-T7-015)

### TC-T7-010: Flat hierarchy — single level of children
**Given**: Root with two Level 1 children: `01-OrderServiceBoundary/` and `02-PaymentEngineBoundary/`; no Level 2  
**When**: Hierarchy Index is generated  
**Then**:  
- `hierarchy-index.md` created at root level  
- Table has 3 rows: Level 0 (root), Level 1 (OrderService), Level 1 (PaymentEngine), in breadth-first order  
- Mermaid diagram shows root → two children  
- Statistics: Total Levels = 2, Total Processes = 3, Leaf Processes = 2  
**Result**: PASS

### TC-T7-011: Deep hierarchy — 3 levels, multiple branches
**Given**: Root → L1A (`01-OrderServiceBoundary/`), L1B (`02-PaymentEngineBoundary/`); L1A → L2A (`01-ValidationEngineBoundary/`)  
**When**: Hierarchy Index is generated  
**Then**:  
- Table has 4 rows (breadth-first: L0, L1A, L1B, L2A)  
- L2A row contains path `01-OrderServiceBoundary/01-ValidationEngineBoundary/main.md`  
- Mermaid diagram has four nodes; L0 → L1A, L0 → L1B, L1A → L2A  
- Level 0 node styled `#e1f5fe`, Level 1 nodes `#e8f5e8`, Level 2 node `#fff3e0`  
**Result**: PASS

### TC-T7-012: Mermaid click directives resolve to correct relative paths
**Given**: 3-level hierarchy (TC-T7-011 scenario)  
**When**: Hierarchy Index is generated  
**Then**: Each `click` directive in the Mermaid block references the path relative to `hierarchy-index.md` (root folder); e.g., `click L2A "01-OrderServiceBoundary/01-ValidationEngineBoundary/main.md"`  
**Result**: PASS

### TC-T7-013: Hierarchy Index does not appear inside sub-folders
**Given**: A 3-level hierarchy where decompositions have been performed at Level 1 and Level 2  
**When**: Hierarchy Index generation completes  
**Then**: `hierarchy-index.md` exists only in the root process folder; no `hierarchy-index.md` files present in any sub-folder  
**Result**: PASS

### TC-T7-014: Hierarchy Index regenerated after new decomposition
**Given**: `hierarchy-index.md` already exists showing root + 2 children; a third child `03-ShippingServiceBoundary/` is created  
**When**: Decomposition completes and Index is regenerated  
**Then**:  
- `hierarchy-index.md` now shows 4 rows (root + 3 children)  
- Statistics row `Total Processes` updated from 3 to 4  
- `Last Updated` timestamp reflects the current date  
- Previously correct rows are unchanged  
**Result**: PASS

### TC-T7-015: Hierarchy Index regenerated after rollback
**Given**: `hierarchy-index.md` shows root + 3 children; `03-ShippingServiceBoundary/` is rolled back  
**When**: Rollback completes and Index is regenerated  
**Then**:  
- `hierarchy-index.md` reverts to 3 rows (root + 2 children)  
- `03-ShippingServiceBoundary/` row is gone  
- Statistics updated accordingly  
**Result**: PASS

---

## Category 4: Link Integrity Check (TC-T7-016 – TC-T7-019)

### TC-T7-016: All links valid — clean confirmation
**Given**: A 3-level hierarchy with no missing files and no broken links  
**When**: Link Integrity Check runs (§7c)  
**Then**: Report states "All navigation links verified ✓"; no broken link list emitted  
**Result**: PASS

### TC-T7-017: Broken parent link in child main.md
**Given**: `01-OrderServiceBoundary/main.md` contains `**Parent Process**: [Root](../main.md)` but the root `main.md` was deleted  
**When**: Link Integrity Check runs  
**Then**: Broken link reported: `{ file: "01-OrderServiceBoundary/main.md", link_text: "Root", target_path: "../main.md", issue: "target-not-found" }` 
**Result**: PASS

### TC-T7-018: Broken breadcrumb link due to ancestor rename
**Given**: `02-ValidationEngineBoundary/main.md` breadcrumb links to `../../main.md` which resolves correctly; but also to `../main.md` which points to a renamed folder `01-OldServiceBoundary/` (now `01-OrderServiceBoundary/`)  
**When**: Link Integrity Check runs  
**Then**: Broken link detected for the renamed ancestor; file, text, resolved path, and issue type (`target-not-found`) all reported; auto-fix offered  
**Result**: PASS

### TC-T7-019: Multiple broken links in one scan — all reported
**Given**: After a bulk folder rename, three different `main.md` files have stale navigation links  
**When**: Link Integrity Check runs  
**Then**: All three broken links reported in a single list; no partial report; user offered option to auto-fix all at once  
**Result**: PASS

---

## Category 5: Auto-Fix Renamed Paths (TC-T7-020 – TC-T7-022)

### TC-T7-020: Renamed folder — auto-fix updates all referencing files
**Given**: `01-OrderServiceBoundary/` renamed to `01-OrderMgmtBoundary/`; two `main.md` files reference the old name (parent's Sub-Processes table and a Level 2 child's breadcrumb)  
**When**: User confirms auto-fix  
**Then**:  
- Both files updated: old path segment `01-OrderServiceBoundary/` replaced with `01-OrderMgmtBoundary/`  
- Link Integrity Check re-run confirms no remaining broken links  
- Two `LINK-UPDATE` entries appended to `folder-creation.log` with old path, new path, and reason `rename`  
**Result**: PASS

### TC-T7-021: Auto-fix does not alter non-navigation links
**Given**: A `main.md` file contains navigation links (breadcrumb, Sub-Processes) and also a free-text external URL  
**When**: Auto-fix updates navigation paths after a rename  
**Then**: Only navigation section links are modified; the external URL and any domain-model or process.md links outside the Navigation/Sub-Processes sections are left unchanged  
**Result**: PASS

### TC-T7-022: Target file genuinely missing (not renamed) — no auto-fix attempted
**Given**: `03-ArchivedBoundary/` was deleted; a parent `main.md` has a stale row referencing it  
**When**: Link Integrity Check runs; no folder with the original name exists anywhere in the tree  
**Then**: Broken link reported with issue `target-not-found`; auto-fix is NOT offered (no matching target found); user is asked to manually remove or correct the row  
**Result**: PASS

---

## Category 6: Rebuild All Links Pass (TC-T7-023 – TC-T7-024)

### TC-T7-023: Existing hierarchy without any navigation — full rebuild
**Given**: A 3-level folder tree where all `main.md` files exist but contain no `## Navigation` section and no `## Sub-Processes` table  
**When**: The "rebuild all navigation links" pass runs against the root  
**Then**:  
- All `main.md` files at Level 1+ receive a `## Navigation` section with correct breadcrumb and parent link  
- Root `main.md` receives a `## Sub-Processes` table with rows for all Level 1 children  
- Each Level 1 `main.md` receives a `## Sub-Processes` table with rows for its children (if any)  
- Link Integrity Check confirms all links valid  
**Result**: PASS

### TC-T7-024: Rebuild pass is idempotent
**Given**: The rebuild pass already ran once; hierarchy has not changed  
**When**: Rebuild pass runs a second time  
**Then**: No files are modified; content of all `main.md` files is byte-for-byte identical before and after; no duplicate sections or rows  
**Result**: PASS

---

## Category 7: Rollback Cross-Reference Cleanup (TC-T7-025 – TC-T7-026)

### TC-T7-025: Rollback removes sub-process row from parent Sub-Processes table
**Given**: Parent `main.md` has a `## Sub-Processes` table with two rows: `01-OrderServiceBoundary/` and `02-PaymentEngineBoundary/`; `02-PaymentEngineBoundary/` is rolled back  
**When**: Rollback completes (§7d)  
**Then**:  
- `## Sub-Processes` table retains exactly one row: `01-OrderServiceBoundary/`  
- Row for `02-PaymentEngineBoundary/` is fully removed  
- Parent breadcrumb and other sections are unchanged  
**Result**: PASS

### TC-T7-026: Rollback removes stale row from hierarchy-index.md
**Given**: `hierarchy-index.md` contains a row for `02-PaymentEngineBoundary/` at Level 1; that sub-process is rolled back  
**When**: Hierarchy Index is regenerated post-rollback  
**Then**: The `02-PaymentEngineBoundary/` row is gone from both the flat table and the Mermaid diagram; statistics updated to reflect one fewer process  
**Result**: PASS

---

## Test Coverage Summary

| Category | Tests |
|----------|-------|
| Parent → Child Sub-Processes Table | 4 |
| Child → Parent Navigation Links and Breadcrumb | 5 |
| Hierarchy Index Generation | 6 |
| Link Integrity Check | 4 |
| Auto-Fix Renamed Paths | 3 |
| Rebuild All Links Pass | 2 |
| Rollback Cross-Reference Cleanup | 2 |
| **Total** | **26** |

**All 26 tests executed and passed — March 14, 2026**

**Requirements Coverage**

| Requirement | Test Cases |
|-------------|-----------|
| FR-T7.1 — Parent link in sub-process main.md | TC-T7-005, TC-T7-006, TC-T7-007, TC-T7-008, TC-T7-009 |
| FR-T7.2 — Sub-process links in parent main.md | TC-T7-001, TC-T7-002, TC-T7-003, TC-T7-004 |
| FR-T7.3 — Hierarchy index at root level | TC-T7-010, TC-T7-011, TC-T7-012, TC-T7-013, TC-T7-014, TC-T7-015 |
| FR-T7.4 — Link integrity on hierarchy changes | TC-T7-016, TC-T7-017, TC-T7-018, TC-T7-019, TC-T7-020, TC-T7-021, TC-T7-022 |
