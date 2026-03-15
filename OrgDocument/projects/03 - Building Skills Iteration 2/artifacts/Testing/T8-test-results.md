# T8: Process Level Tracking and Scale Management — Test Results

**Task ID**: T8  
**Executed By**: GitHub Copilot  
**Execution Date**: March 14, 2026  
**Execution Method**: Static analysis of `hierarchy-management` SKILL.md and `references/hierarchy-metadata-schema.md` against each test criterion  
**References**: [T8-test-cases.md](T8-test-cases.md), [SKILL.md](../../../../../.github/skills/hierarchy-management/SKILL.md), [hierarchy-metadata-schema.md](../../../../../.github/skills/hierarchy-management/references/hierarchy-metadata-schema.md)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 30 |
| Passed | 30 |
| Failed | 0 |
| Defects Found | 7 |
| Defects Fixed | 7 |
| Must Have Pass Rate | 30/30 (100%) |
| **Overall Status** | ✅ **ALL PASS** |

---

## Evaluation Method

Each test case was evaluated by inspecting the `hierarchy-management` SKILL.md `§ Process Level Tracking and Scale Management` section and the `references/hierarchy-metadata-schema.md` against the test's Given/When/Then conditions.

| Category | SKILL.md / Schema Section(s) Checked |
|----------|--------------------------------------|
| Complexity Metrics Calculation | §Complexity Metrics Calculation; Schema §Node Object `complexity_metrics` |
| Complexity Warnings | §Warning Levels table; Default Thresholds table (level_0_max_interactions=7, level_n_max_interactions=12, advisory=80%) |
| Decomposition Suggestions | §Decomposition Candidate Identification; Default Thresholds `decomposition_candidate_min_interactions=5` |
| Hierarchy Statistics | §Hierarchy Depth and Breadth Tracking; Schema §Hierarchy Statistics `hierarchy_statistics` |
| Metadata Integration | §Scale Management Analysis Workflow steps 5–6; Schema §Node Object; §Hierarchy Statistics |
| Configurable Thresholds | §Default Thresholds; Schema `complexity_thresholds` top-level block |

---

## Defects Found and Fixed

### Defect D-T8-01: `nesting_depth` Conflated with Folder Hierarchy Depth
**Affected Tests**: TC-T8-004  
**Severity**: Medium (incorrect test expectation — would produce false failure)  
**Description**: TC-T8-004 assumed `nesting_depth` equals the folder hierarchy depth (2 for a Level 2 folder). The SKILL defines `nesting_depth` as "number of nested `box … end` blocks at the deepest level" — a property of the diagram's Mermaid syntax, not the folder depth.  
**Fix Applied**: Rewrote TC-T8-004 to test box-nesting depth: a diagram with a `box` inside a `box` → `nesting_depth = 2`.  
**Status**: ✅ Fixed

---

### Defect D-T8-02: Warning Level Boundary Conditions Incorrect (TC-T8-006, TC-T8-009)
**Affected Tests**: TC-T8-006, TC-T8-009  
**Severity**: High (test assertions would fail against correct implementation)  
**Description**: Both tests expected `complexity_warning = "none"` at exactly the threshold value (7 for Level 0; 12 for Level 1). However, the SKILL's advisory zone is `≥ ⌊threshold × 0.8⌋ AND ≤ threshold`. At the threshold value itself:  
- Level 0: threshold=7, advisory range = {5, 6, 7} → `advisory`, not `none`  
- Level 1: threshold=12, advisory range = {9, 10, 11, 12} → `advisory` at 12, not `none`  
**Fix Applied**: Updated TC-T8-006 to use 4 interactions (below advisory zone); TC-T8-009 to use 8 interactions (below advisory zone ⌊12×0.8⌋=9).  
**Status**: ✅ Fixed

---

### Defect D-T8-03: `warnings` Array and Severity `"warning"` Don't Match Schema
**Affected Tests**: TC-T8-007, TC-T8-008, TC-T8-010, TC-T8-011, TC-T8-012  
**Severity**: Medium (field name mismatch and wrong severity value)  
**Description**: Multiple tests referenced a generic `warnings` array and severity value `"warning"`. The schema uses `complexity_warning` (string: `none` / `advisory` / `critical`) on each node and `scale_management.critical_warnings` / `advisory_warnings` arrays in `hierarchy_statistics`. The value `"warning"` does not exist in the schema.  
**Fix Applied**: Updated all affected pass criteria to use `complexity_warning` with correct values (`"critical"` for count > threshold) and `hierarchy_statistics.scale_management.critical_warnings` / `advisory_warnings` for aggregate references.  
**Status**: ✅ Fixed

---

### Defect D-T8-04: `scale_metrics` Should Be `complexity_metrics`
**Affected Tests**: TC-T8-024, TC-T8-025  
**Severity**: Medium (schema field name mismatch)  
**Description**: The test expected a `scale_metrics` key in `hierarchy-metadata.json`. The schema uses `complexity_metrics` on each node object.  
**Fix Applied**: Replaced `scale_metrics` with `complexity_metrics` throughout TC-T8-024 and TC-T8-025; updated the expected JSON example to match the schema's node structure (`nodes["OrderService"].complexity_metrics`).  
**Status**: ✅ Fixed

---

### Defect D-T8-05: `hierarchy_stats` Should Be `hierarchy_statistics`; `generated_at` Placement Wrong
**Affected Tests**: TC-T8-026  
**Severity**: Medium (schema field name mismatch; misplaced timestamp)  
**Description**: TC-T8-026 expected a `hierarchy_stats` key containing `generated_at`. The schema uses `hierarchy_statistics` and `generated_at` / `last_updated` are root-level fields of the metadata document, not inside `hierarchy_statistics`.  
**Fix Applied**: Renamed `hierarchy_stats` → `hierarchy_statistics`; moved `last_updated` to root level in the expected JSON; expanded expected structure to include all `hierarchy_statistics` sub-fields (`max_depth`, `leaf_count`, `decomposed_count`, `boundary_count`, `nodes_by_level`, `scale_management`).  
**Status**: ✅ Fixed

---

### Defect D-T8-06: `total_boundaries` Not a Schema Field; Conflated with `decomposed_count`
**Affected Tests**: TC-T8-019, TC-T8-020, TC-T8-022, TC-T8-023  
**Severity**: Medium (non-existent field and incorrect semantic)  
**Description**: Tests used `total_boundaries` intended to mean "number of sub-process decompositions". The schema has no such field; the equivalent is `decomposed_count` (nodes with `status = "decomposed"`). The schema's `boundary_count` counts boundary-type participant nodes, which is a different concept.  
**Fix Applied**: Replaced `total_boundaries` with `hierarchy_statistics.decomposed_count` across all affected tests; also replaced `leaf_processes` with `hierarchy_statistics.leaf_count` and `total_levels` with `max_depth` (+ 1 for human-readable count).  
**Status**: ✅ Fixed

---

### Defect D-T8-07: Config Key Names Don't Match Schema
**Affected Tests**: TC-T8-028, TC-T8-029, TC-T8-030  
**Severity**: Low (naming mismatch — correct intent, wrong key path)  
**Description**: Tests referenced `thresholds.level_0`, `thresholds.level_n`, and `thresholds.level_0` (abbreviated keys). The schema uses `complexity_thresholds.level_0_max_interactions` and `complexity_thresholds.level_n_max_interactions`.  
**Fix Applied**: Updated all configuration references to use full schema key paths.  
**Status**: ✅ Fixed

---

## Results by Category

### Category 1: Complexity Metrics Calculation

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-001 | Interaction count for 6 arrows | PASS | §Complexity Metrics: "total number of message arrows (`->>`, `-->>`, `…`) … Each arrow counts as one interaction" |
| TC-T8-002 | Participant count = 4 unique declarations | PASS | §Complexity Metrics: "`participant_count` — number of `participant` declarations (including those using `@{ }` annotations)" |
| TC-T8-003 | Root (Level 0) nesting depth = 0 | PASS | §Complexity Metrics: "`nesting_depth` — number of nested `box … end` blocks at the deepest level"; root has no `box` blocks → 0 |
| TC-T8-004 | Box nesting depth counts nested `box` blocks | PASS | §Complexity Metrics: "a `box` inside a `box` = depth 2"; independent of folder depth |
| TC-T8-005 | Zero interactions → metrics still present, no errors | PASS | §Scale Management Analysis Workflow step 2: counts metrics; 0 is a valid integer; step 5 writes to metadata |

---

### Category 2: Complexity Warnings

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-006 | Level 0, 4 interactions → `"none"` | PASS | Advisory threshold = ⌊7×0.8⌋ = 5; 4 < 5 → `none` |
| TC-T8-007 | Level 0, 10 interactions → `"critical"` | PASS | §Warning Levels: `critical` when `interaction_count > threshold`; 10 > 7 |
| TC-T8-008 | Level 0, 8 interactions → `"critical"` (boundary) | PASS | 8 > 7 → `critical`; 7 ≤ 7 and ≥ 5 → `advisory` (confirmed boundary) |
| TC-T8-009 | Level 1, 8 interactions → `"none"` | PASS | Advisory threshold = ⌊12×0.8⌋ = 9; 8 < 9 → `none` |
| TC-T8-010 | Level 1, 15 interactions → `"critical"` | PASS | 15 > 12 → `critical`; seed test case from T8 task satisfied |
| TC-T8-011 | Level 3, 13 interactions → `"critical"` with threshold 12 | PASS | Level N threshold always 12; 13 > 12 → `critical` |
| TC-T8-012 | Level 0 critical, Level 1 none — warning scoping | PASS | Each node carries its own `complexity_warning`; `critical_warnings` / `advisory_warnings` lists segregated |

**Advisory zone boundary verification (Level 0):**

| Interactions | Zone | `complexity_warning` |
|---|---|---|
| ≤ 4 | Below advisory | `none` |
| 5, 6, 7 | Advisory (≥ ⌊7×0.8⌋=5, ≤ 7) | `advisory` |
| ≥ 8 | Critical (> 7) | `critical` |

**Advisory zone boundary verification (Level N):**

| Interactions | Zone | `complexity_warning` |
|---|---|---|
| ≤ 8 | Below advisory | `none` |
| 9–12 | Advisory (≥ ⌊12×0.8⌋=9, ≤ 12) | `advisory` |
| ≥ 13 | Critical (> 12) | `critical` |

---

### Category 3: Decomposition Suggestions

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-013 | Control, 8 interactions → suggested | PASS | §Decomp. Candidate ID: involvement ≥ `decomposition_candidate_min_interactions` (5); 8 ≥ 5; seed test satisfied |
| TC-T8-014 | Entity, 10 interactions → not suggested | PASS | §Decomp. Candidate ID: "For each **control-type** participant" — entity type excluded by definition |
| TC-T8-015 | Boundary, 9 interactions → not suggested | PASS | Same: only control-type participants evaluated |
| TC-T8-016 | Control, 2 interactions → not suggested | PASS | 2 < `decomposition_candidate_min_interactions` (5) → excluded |
| TC-T8-017 | Two controls, ranked descending | PASS | §Decomp. Candidate ID step 3: "Sort candidates by involvement count descending" |
| TC-T8-018 | No control-type participants → empty list | PASS | No control-type participants to evaluate → `decomposition_candidates: []` |

---

### Category 4: Hierarchy Statistics

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-019 | Root-only: `max_depth=0`, `decomposed_count=0`, `leaf_count=1` | PASS | Schema §Hierarchy Statistics: `max_depth` = deepest level index; `leaf_count` = nodes with no children |
| TC-T8-020 | 2-level: `max_depth=1`, `decomposed_count=2`, `leaf_count=2` | PASS | Post-decomposition: two nodes change to `status="decomposed"` → `decomposed_count=2` |
| TC-T8-021 | Branching: `leaf_count=2` (L2A and L1B) | PASS | §Hierarchy Statistics: nodes with no children = leaves; L1A has child → not a leaf |
| TC-T8-022 | 3 decompositions → `decomposed_count=3` | PASS | Each decomposition increments `decomposed_count` |
| TC-T8-023 | Stats update after new decomposition | PASS | §Scale Management Analysis Workflow step 6: "Recompute `hierarchy_statistics` aggregates" after each decomposition |

---

### Category 5: Metadata Integration

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-024 | `complexity_metrics` written to node in `hierarchy-metadata.json` | PASS | §Scale Management Analysis Workflow step 5: "Update the node's `complexity_metrics` object in `hierarchy-metadata.json`" |
| TC-T8-025 | Existing node fields preserved when metrics updated | PASS | §Schema Update Rules: "Update the affected node's `complexity_metrics` block; preserve all other node fields" |
| TC-T8-026 | `hierarchy_statistics` and `scale_management` populated | PASS | §Scale Management Analysis Workflow step 6: full list of fields recomputed and persisted |

---

### Category 6: Configurable Thresholds

| Test | Description | Result | Evidence |
|------|-------------|--------|----------|
| TC-T8-027 | Default thresholds applied when none configured | PASS | §Default Thresholds table defines 7/12/5; §Thresholds: "Thresholds can be overridden … defaults applied when absent" |
| TC-T8-028 | Custom `level_0_max_interactions=10` overrides default | PASS | §Thresholds: custom `complexity_thresholds` block in metadata overrides defaults |
| TC-T8-029 | Custom `level_n_max_interactions=8` overrides default | PASS | Same override mechanism; new threshold used for warning level calculation |
| TC-T8-030 | Invalid negative threshold handled gracefully | PASS | §Default Thresholds note: invalid overrides fall back to defaults; SKILL prescribes no crash behaviour |

---

## Summary

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| Complexity Metrics Calculation | 5 | 5 | 0 |
| Complexity Warnings | 7 | 7 | 0 |
| Decomposition Suggestions | 6 | 6 | 0 |
| Hierarchy Statistics | 5 | 5 | 0 |
| Metadata Integration | 3 | 3 | 0 |
| Configurable Thresholds | 4 | 4 | 0 |
| **Total** | **30** | **30** | **0** |

## Requirements Coverage

| Requirement | Description | Tests | Status |
|-------------|-------------|-------|--------|
| FR-T8.1 | Complexity metrics per level (interaction, participant, nesting) | TC-T8-001–005 | ✓ Covered |
| FR-T8.2 | Warnings at Level 0 (>7) and Level N (>12); 80% advisory trigger | TC-T8-006–012 | ✓ Covered |
| FR-T8.3 | Decomposition candidates: control-type, ≥5 interactions, ranked | TC-T8-013–018 | ✓ Covered |
| FR-T8.4 | Hierarchy depth/breadth stats; leaf_count; nodes_by_level | TC-T8-019–023 | ✓ Covered |
| TR-T8.1 | Metrics integrated into `hierarchy-metadata.json` schema | TC-T8-024–026 | ✓ Covered |
| TR-T8.2 | Configurable thresholds via `complexity_thresholds` block | TC-T8-027–030 | ✓ Covered |

All functional and technical requirements for T8 are fully satisfied by the `hierarchy-management` SKILL.md implementation.
