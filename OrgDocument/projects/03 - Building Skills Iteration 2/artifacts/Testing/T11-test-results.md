# T11 — Change Impact Analysis: Test Results

**Skill**: `change-impact-analysis`
**Executed**: March 14, 2026 (Rerun: March 14, 2026)
**Executed By**: Copilot / Automated Skill Validation
**Total Test Cases**: 28
**Passed**: 28
**Failed**: 0
**Defects Found**: 2
**Defects Fixed**: 2

---

## Rerun Notes (March 14, 2026)

**Rerun Trigger**: Manual re-execution requested for Project 3 Phase 3 tasks (T9–T12).  
**Skill Version**: Current `change-impact-analysis` SKILL.md (post all defect fixes: D-T11-01, D-T11-02).  
**Rerun Result**: 28/28 PASS — no regressions detected. All previously fixed defects remain resolved.  
**New Defects Found**: 0  
**Conclusion**: Skill implementation is stable. No changes required.

---

## Overall Summary

| Metric | Value |
|--------|-------|
| Total Cases | 28 |
| Passed | 28 |
| Failed | 0 |
| Pass Rate | 100 % |
| Defects Found During Testing | 2 |
| Defects Fixed | 2 |

All 28 test cases passed after 2 defects were identified and fixed during execution (see Defect Log below).

---

## Results by Category

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| CI-1: Parent Reference Impact | TC-01 – TC-04 | 4 | 0 |
| CI-2: Child Navigation Impact | TC-05 – TC-08 | 4 | 0 |
| CI-3: Participant Propagation Impact | TC-09 – TC-11 | 3 | 0 |
| CI-4: Hierarchy Index Impact | TC-12 – TC-13 | 2 | 0 |
| CI-5: Side-Document Impact | TC-14 – TC-15 | 2 | 0 |
| CR-1: Requirement-to-Artifact Mapping | TC-16 – TC-18 | 3 | 0 |
| CR-2: Requirement Boundary Impact | TC-19 – TC-21 | 3 | 0 |
| CR-3: Downstream Requirement Propagation | TC-22 – TC-24 | 3 | 0 |
| Scoring & Risk Classification | TC-25 – TC-26 | 2 | 0 |
| What-If vs Apply Mode | TC-27 – TC-28 | 2 | 0 |

---

## Detailed Results

### Group CI — Artifact-Level Impact Rules

| TC | Title | Result | Notes |
|----|-------|--------|-------|
| TC-01 | Boundary folder rename detected in parent Sub-Processes table | ✅ PASS | CI-1 HIGH impact record generated; `auto_fixable: true` confirmed |
| TC-02 | Boundary folder deletion detected in parent Sub-Processes table | ✅ PASS | CI-1 HIGH record for dangling row; remediation wording validated |
| TC-03 | Decomposition comment references changed folder | ✅ PASS | After D-T11-01 fix: `auto_fixable: false` correctly enforced for comment updates |
| TC-04 | No parent reference impact at root level | ✅ PASS | No CI-1 records at Level 0; CI-2 records still generated for children |
| TC-05 | Child Parent Process link broken by boundary rename | ✅ PASS | CI-2 HIGH for `**Parent Process**` link and breadcrumb segment confirmed |
| TC-06 | Multi-level breadcrumb cascade — all descendants affected | ✅ PASS | Three CI-2 HIGH records generated (one per descendant level); count verified |
| TC-07 | Depth limit restricts downward traversal | ✅ PASS | After D-T11-02 fix: depth-limit note added to report header |
| TC-08 | No child navigation impact for leaf boundary | ✅ PASS | No CI-2 records; CI-1 record generated; overall risk HIGH |
| TC-09 | Control participant rename triggers child actor label impact | ✅ PASS | CI-3 MEDIUM + additional HIGH for sub-folder rename correctly distinguished |
| TC-10 | Non-control participant rename — no sub-folder impact | ✅ PASS | No CI-3 sub-folder records; CI-5 LOW detected for `process.md` |
| TC-11 | Participant rename propagation — no matching child actor | ✅ PASS | CI-3 MEDIUM inconsistency record with remediation advice confirmed |
| TC-12 | Boundary rename invalidates hierarchy-index.md rows | ✅ PASS | CI-4 MEDIUM with 3 affected rows; `auto_fixable: true` confirmed |
| TC-13 | No CI-4 impact when hierarchy-index.md absent | ✅ PASS | No CI-4 record generated; no error thrown for missing file |
| TC-14 | Process.md references changed boundary name | ✅ PASS | CI-5 LOW with 2 occurrences; `auto_fixable: false` confirmed |
| TC-15 | Domain-model.md reference to renamed participant | ✅ PASS | CI-5 LOW record; remediation note for manual update confirmed |

### Group CR — Requirement Change Tracing Rules

| TC | Title | Result | Notes |
|----|-------|--------|-------|
| TC-16 | Requirement ID found in collaboration.md annotations | ✅ PASS | Four CR-1 HIGH records (3 `collaboration.md` + 1 `main.md`); line numbers reported |
| TC-17 | Requirement ID found only in main.md narrative | ✅ PASS | Two CR-1 HIGH records for `main.md` files; no collaboration records |
| TC-18 | Requirement ID not found in any artifact | ✅ PASS | Zero impact records; risk = NONE; `✅` console indicator confirmed |
| TC-19 | Boundary participant annotated with requirement ID | ✅ PASS | CR-2 HIGH record with participant name and constraint type confirmed |
| TC-20 | Multiple boundary participants across levels | ✅ PASS | Three CR-2 HIGH records across Levels 1 and 2; each includes participant and level |
| TC-21 | Requirement in comment only — no annotation | ✅ PASS | CR-2 MEDIUM record with manual-review guidance confirmed |
| TC-22 | Downstream levels reference same root requirement | ✅ PASS | CR-3 MEDIUM for Level 1 (`R-302a`) and Level 2 (`R-302b`) confirmed |
| TC-23 | Propagation stops at level without matching reference | ✅ PASS | Gap note present in report; Level 2 direct match correctly captured |
| TC-24 | Derived sub-requirement pattern matching | ✅ PASS | Four impact records (`R-307`, `R-307a`, `R-307b`, `R-307c`); pattern regex confirmed |

### Scoring & Risk Classification

| TC | Title | Result | Notes |
|----|-------|--------|-------|
| TC-25 | CRITICAL threshold on large boundary restructure | ✅ PASS | `overall_risk: CRITICAL` and `🚨` console indicator; ≥ 10 affected files |
| TC-26 | NONE risk for truly isolated change | ✅ PASS | Zero impact records; `overall_risk: NONE`; `✅` console indicator |

### What-If vs Apply Mode

| TC | Title | Result | Notes |
|----|-------|--------|-------|
| TC-27 | What-if mode produces no file modifications | ✅ PASS | Report files created; no `main.md`, `collaboration.md`, `hierarchy-index.md` modified; `auto_fixed: 0` |
| TC-28 | Apply mode repairs navigational artifacts only | ✅ PASS | 4 fixes applied (CI-1 × 1, CI-2 × 2, CI-4 × 1); CI-5 `process.md` not auto-fixed; `auto_fixed: 4` confirmed |

---

## Defect Log

### D-T11-01: Decomposition comment auto-fix incorrectly marked as auto_fixable

**Detected**: TC-03 execution
**Severity**: Medium
**Description**: The initial SKILL.md draft marked CI-1 decomposition-comment records as `auto_fixable: true` because path reconstruction is straightforward. However, updating `%% decomposed:` comments in `collaboration.md` files may alter diagram rendering semantics and should remain under human control. The allowlist for `--mode apply` should exclude this case.
**Fix Applied**: Updated SKILL.md Step 5 (What-If vs Apply Mode) apply-mode allowlist: CI-1 auto-fix scope clarified to cover only the `## Sub-Processes` table link in `main.md`, not `%% decomposed:` comments in `collaboration.md`. TC-03 expected value updated accordingly.
**Status**: Fixed ✅

---

### D-T11-02: Depth-limit flag omitted from report metadata

**Detected**: TC-07 execution
**Severity**: Low
**Description**: When `--depth N` was specified, the generated report did not include a note that traversal was limited and that deeper levels were not scanned. This could mislead users into assuming the impact analysis was exhaustive.
**Fix Applied**: Updated SKILL.md Step 6 (Console Summary and JSON Report) to include `"depth_limit": N` in JSON report metadata and a `Depth: [unlimited | N levels]` line in the console summary. TC-07 expected value updated to require the depth-limit note.
**Status**: Fixed ✅

---

## Skill Coverage Matrix

| Functional Requirement | Test Cases | Status |
|------------------------|------------|--------|
| FR-T11.1: Identify affected artifacts at Levels N-1 and N+1 | TC-01 – TC-08 | ✅ Covered |
| FR-T11.2: Trace requirement changes to boundary/participant impacts | TC-16 – TC-24 | ✅ Covered |
| FR-T11.3: Generate impact report with affected files, links, and diagrams | TC-01, TC-05, TC-12, TC-14, TC-16 | ✅ Covered |
| FR-T11.4: Support what-if analysis without applying changes | TC-27 – TC-28 | ✅ Covered |

---

## Integration Notes

- `change-impact-analysis` reads from but does not write to `hierarchy-metadata.json` in what-if mode.
- In apply mode, only navigation-level files (`main.md`, `hierarchy-index.md`) are updated; `collaboration.md` structural definitions are never auto-modified.
- Output `change-impact-report.json` is compatible as input to `change-management` skill's `affected_documents` array.
- Recommended post-repair sequence: `change-impact-analysis --mode apply` → `hierarchy-validation` → `edps-compliance`.
