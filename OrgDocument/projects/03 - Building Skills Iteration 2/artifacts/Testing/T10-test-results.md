# T10: Hierarchy Validation — Test Results

**Task ID**: T10  
**Executed By**: GitHub Copilot  
**Execution Date**: March 14, 2026 (Rerun: March 14, 2026)  
**Execution Method**: Static analysis of `hierarchy-validation` SKILL.md against each test criterion  
**References**: [T10-test-cases.md](T10-test-cases.md), [SKILL.md](../../../../../.github/skills/hierarchy-validation/SKILL.md)

---

## Rerun Notes (March 14, 2026)

**Rerun Trigger**: Manual re-execution requested for Project 3 Phase 3 tasks (T9–T12).  
**Skill Version**: Current `hierarchy-validation` SKILL.md (post all defect fixes: D-T10-01).  
**Rerun Result**: 34/34 PASS — no regressions detected. Previously fixed defect D-T10-01 remains resolved.  
**New Defects Found**: 0  
**Conclusion**: Skill implementation is stable. No changes required.

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 34 |
| Passed | 34 |
| Failed | 0 |
| Defects Found | 1 |
| Defects Fixed | 1 |
| Must Have Pass Rate | 28/28 (100%) |
| Should Have Pass Rate | 6/6 (100%) |
| **Overall Status** | ✅ **ALL PASS** |

---

## Evaluation Method

Each test case was evaluated by reading the `hierarchy-validation` SKILL.md rule catalogue, workflow steps (Steps 1–7), scoring formula, incremental validation section, and auto-fix pass against the test's Given/When/Then conditions and pass criteria.

| Category | SKILL.md Section(s) Checked |
|----------|-----------------------------|
| Group HV — HV-1 through HV-5 | §Validation Rule Catalogue Group HV; §Step 2: Apply Group HV Rules |
| Group HX — HX-1 through HX-5 | §Validation Rule Catalogue Group HX; §Step 3: Apply Group HX Rules |
| Group HN — HN-1 through HN-4 | §Validation Rule Catalogue Group HN; §Step 4: Apply Group HN Rules |
| Validation Scoring & Status | §Step 5: Score and Aggregate |
| Auto-Fix | §Step 6: Auto-Fix Pass |
| Report Generation | §Step 7: Generate Reports |
| Incremental Mode | §Incremental Validation section |

---

## Defects Found and Fixed

### Defect D-T10-01: Auto-Fix Table Contradicts the ERROR-Rule Exclusion Note for HX-1 and HX-2

**Affected Tests**: TC-T10-034 (auto-fix boundary behaviour)  
**Severity**: Medium (inconsistent behaviour specification — implementers would receive conflicting instructions)  
**Description**: Step 6 (Auto-Fix Pass) listed `HX-1` and `HX-2` in the auto-fix table with concrete fix descriptions:

> HX-1 — "If the parent `main.md` exists at the expected depth, reconstruct the relative path and update `main.md`"  
> HX-2 — "If a sub-process folder exists but is listed with a wrong relative path, correct the path in the parent `main.md`"

However, the note immediately below the table stated: _"Fixes for ERROR-severity rules **(HV-\*, HX-1/2, HN-1/2/3)** are **not** auto-applied"_. Because HX-1 (severity ERROR) and HX-2 (severity ERROR) were explicitly named in the exclusion, this directly contradicted their presence in the fix table — leaving it undefined whether path-reconstruction for broken parent/child links would be auto-applied.

The intent behind the auto-fix table entries for HX-1 and HX-2 is that **relative path reconstruction** (verifying the target file exists, recalculating the correct `../` depth, and rewriting the link) is a mechanical and safe operation that does not alter hierarchy structure. It is meaningfully different from structural ERROR fixes such as creating missing files (HN-2), renaming folders (HN-1), or reclassifying participant types (HV-1). Including HX-1/2 in the structural-fix exclusion category was therefore an over-broad restriction.

**Fix Applied**: Updated the exclusion note in Step 6 to remove `HX-1/2` from the list of non-auto-fixable rules:  
  ~~"Fixes for ERROR-severity rules (HV-\*, HX-1/2, HN-1/2/3)"~~  
  → **"Fixes for structural ERROR-severity rules (HV-\*, HN-1/2/3)"**

HX-1 and HX-2 remain in the auto-fix table and are now consistently described as auto-applicable (path reconstruction only).  
**Status**: ✅ Fixed — Step 6 note updated in `hierarchy-validation` SKILL.md

---

## Per-Category Results

### Category 1: HV-1 — Decomposed-Participant Is Control

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-001 | Valid — sub-folder matches control-type participant | ✅ PASS | §HV-1 Check correctly strips ordinal prefix and `Boundary` suffix; PascalCase case-insensitive compare confirmed |
| TC-T10-002 | Invalid — sub-folder has entity-type participant only | ✅ PASS | §HV-1 Check FAILs if matched participant is `entity` not `control`; violation fields `folder`, `detail`, `remediation` all match |

### Category 2: HV-2 — Parent Actor Appearance

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-003 | Valid — decomposed participant is `actor` outside all boxes | ✅ PASS | §HV-2 Check confirmed: looks for actor outside `box … end` blocks with matching name/label |
| TC-T10-004 | Invalid — parent participant absent in child as actor | ✅ PASS | FAIL triggered; remediation instructs adding `@{ "type": "actor" }` declaration outside boxes |

### Category 3: HV-3 — Actor Label Consistency

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-005 | Valid — label overlap ≥ 50 % (passes) | ✅ PASS | §HV-3 Check uses 50 % character overlap threshold; common suffixes (`Service`, `Manager`, `Boundary`) excluded |
| TC-T10-006 | Warning — label overlap < 50 % | ✅ PASS | FAIL severity WARNING; violation identifies both parent label and child actor label |

### Category 4: HV-4 — Entry-Point Type Integrity

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-007 | Valid — first message recipient is `boundary`-type | ✅ PASS | §HV-4 Check confirmed: identifies first inbound message from external actor inside each `box` |
| TC-T10-008 | Invalid — first message recipient is `control`-type | ✅ PASS | FAIL; violation names the bypassed participant and its actual type; remediation matches |

### Category 5: HV-5 — No Internal Leakage

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-009 | Valid — no child internals in parent; decomposed control expected | ✅ PASS | §HV-5 Check confirmed: decomposed `control` participant in parent is expected and NOT flagged; only non-entry internal participants checked |
| TC-T10-010 | Invalid — child internal participant found in parent | ✅ PASS | FAIL; `ValidationEngine` flagged; boundary entry-point exemption applies correctly |

### Category 6: HX-1 — Parent Link Resolves

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-011 | Valid — parent link resolves | ✅ PASS | §HX-1 Check resolves relative path from file's directory |
| TC-T10-012 | Invalid — parent link does not resolve (extra `../`) | ✅ PASS | FAIL; violation includes broken path; remediation matches HX-1 remediation reference table entry |

### Category 7: HX-2 — Child Links Resolve

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-013 | Valid — all Sub-Processes entries resolve | ✅ PASS | §HX-2 Check reads `## Sub-Processes` table, verifies each link |
| TC-T10-014 | Invalid — one Sub-Processes link resolves to non-existent folder | ✅ PASS | FAIL; violation names the unresolvable path |

### Category 8: HX-3 — Breadcrumb Path Integrity

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-015 | Valid — all breadcrumb links resolve | ✅ PASS | §HX-3 Check parses breadcrumb, resolves each linked path |
| TC-T10-016 | Warning — one breadcrumb link broken | ✅ PASS | FAIL severity WARNING; broken path referenced in violation |

### Category 9: HX-4 — Decomposition Comment Matches Folder

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-017 | Valid — decomposition comment references existing folder | ✅ PASS | Both `%% decomposed:` and `%% Decomposition:` variants matched by regex in §HX-4 Check |
| TC-T10-018 | Warning — decomposition comment references deleted folder | ✅ PASS | FAIL severity WARNING; regex correctly matches both comment variants; stale path flagged |

### Category 10: HX-5 — Hierarchy Index Currency

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-019 | Valid — index lists all folders | ✅ PASS | §HX-5 Check parses `hierarchy-index.md` Full Hierarchy Tree table; compares to filesystem walk |
| TC-T10-020 | Warning — index missing a new sub-folder | ✅ PASS | FAIL severity WARNING; missing folder identified by name |

### Category 11: HN-1 — Folder Name Convention

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-021 | Valid — `01-OrderProcessorBoundary` matches pattern | ✅ PASS | Regex `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$` confirmed to match |
| TC-T10-022 | Invalid — `orderprocessor-boundary` does not match | ✅ PASS | FAIL; regex and renaming instruction in remediation confirmed |

### Category 12: HN-2 — Required Files Present

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-023 | Valid — both `collaboration.md` and `main.md` present | ✅ PASS | `process.md`/`domain-model.md` absence correctly NOT flagged (optional) |
| TC-T10-024 | Invalid — `collaboration.md` missing | ✅ PASS | FAIL limited to missing required files; optional files not mentioned in violation |

### Category 13: HN-3 — Ordinal Uniqueness

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-025 | Valid — all sibling ordinals unique | ✅ PASS | Siblings grouped per parent; all ordinals `01`, `02`, `03` distinct |
| TC-T10-026 | Invalid — two siblings share ordinal `01` | ✅ PASS | FAIL; both conflicting folder names and duplicate ordinal identified |

### Category 14: HN-4 — Level Number Consistency

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-027 | Valid — `**Level**: 1` matches computed depth 1 | ✅ PASS | §Step 1 computes depth; §HN-4 compares declared value |
| TC-T10-028 | Warning — declared level 1 but actual depth is 2 | ✅ PASS | FAIL severity WARNING; stated vs. computed values both shown in violation |

### Category 15: Validation Scoring and Overall Status

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-029 | VALID — 14/14 pass, score 100 % | ✅ PASS | Formula: errors=0, score≥90 → VALID |
| TC-T10-030 | NEEDS_ATTENTION — 2 errors, score ≈ 85.7 % | ✅ PASS | Formula: errors>0, errors≤3 → NEEDS_ATTENTION; 12/14 = 85.7 % confirmed |
| TC-T10-031 | INVALID — 5 errors | ✅ PASS | Formula: errors>3 → INVALID (first-match wins ordering; checked before NEEDS_ATTENTION) |
| TC-T10-032 | MOSTLY_VALID — 0 errors, 3 warnings, score ≈ 78.6 % | ✅ PASS | Formula: errors=0, score≥70 (but <90) → MOSTLY_VALID; 11/14 = 78.6 % confirmed |

### Category 16: Incremental Validation Mode

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-033 | Incremental — only targeted branch + parent partial check | ✅ PASS | §Incremental Validation: HV-1, HV-2, HX-2 run against immediate parent; sibling branches excluded; scope label includes `(incremental)` |

### Category 17: Auto-Fix Behaviour

| TC | Description | Status | Notes |
|----|-------------|--------|-------|
| TC-T10-034 | Auto-fix corrects WARNING rules (HN-4, HX-3); leaves ERROR rule (HV-1) untouched | ✅ PASS | After D-T10-01 fix: HX-1/HX-2 path reconstruction is auto-applied; structural ERRORs (HV-*, HN-1/2/3) are not. HN-4 (WARNING) and HX-3 (WARNING) auto-fixed as expected. `summary.auto_fixed = 2` confirmed. |

---

## Full Pass/Fail Summary

| Group | Rule | Severity | Covered By | Status |
|-------|------|----------|------------|--------|
| HV | HV-1 Decomposed-Participant Is Control | ERROR | TC-T10-001, TC-T10-002 | ✅ |
| HV | HV-2 Parent Actor Appearance | ERROR | TC-T10-003, TC-T10-004 | ✅ |
| HV | HV-3 Actor Label Consistency | WARNING | TC-T10-005, TC-T10-006 | ✅ |
| HV | HV-4 Entry-Point Type Integrity | ERROR | TC-T10-007, TC-T10-008 | ✅ |
| HV | HV-5 No Internal Leakage | ERROR | TC-T10-009, TC-T10-010 | ✅ |
| HX | HX-1 Parent Link Resolves | ERROR | TC-T10-011, TC-T10-012 | ✅ |
| HX | HX-2 Child Links Resolve | ERROR | TC-T10-013, TC-T10-014 | ✅ |
| HX | HX-3 Breadcrumb Path Integrity | WARNING | TC-T10-015, TC-T10-016 | ✅ |
| HX | HX-4 Decomposition Comment Matches Folder | WARNING | TC-T10-017, TC-T10-018 | ✅ |
| HX | HX-5 Hierarchy Index Currency | WARNING | TC-T10-019, TC-T10-020 | ✅ |
| HN | HN-1 Folder Name Convention | ERROR | TC-T10-021, TC-T10-022 | ✅ |
| HN | HN-2 Required Files Present | ERROR | TC-T10-023, TC-T10-024 | ✅ |
| HN | HN-3 Ordinal Uniqueness | ERROR | TC-T10-025, TC-T10-026 | ✅ |
| HN | HN-4 Level Number Consistency | WARNING | TC-T10-027, TC-T10-028 | ✅ |
| — | Scoring / Status VALID | — | TC-T10-029 | ✅ |
| — | Scoring / Status NEEDS_ATTENTION | — | TC-T10-030 | ✅ |
| — | Scoring / Status INVALID | — | TC-T10-031 | ✅ |
| — | Scoring / Status MOSTLY_VALID | — | TC-T10-032 | ✅ |
| — | Incremental mode | — | TC-T10-033 | ✅ |
| — | Auto-fix (--fix flag) | — | TC-T10-034 | ✅ |
