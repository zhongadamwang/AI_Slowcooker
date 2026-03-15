# T8: Process Level Tracking and Scale Management — Test Cases

**Task ID**: T8  
**Test Case Author**: GitHub Copilot  
**Test Date**: March 14, 2026  
**Status**: All 30 test cases executed and passed (March 14, 2026) — 7 defects found and fixed during execution  
**References**: [T8 Task](../../tasks/T8-process-level-tracking.md), [T8 Test Results](T8-test-results.md)

---

## Category 1: Complexity Metrics Calculation (FR-T8.1)

### TC-T8-001: Interaction count calculated for a single level
**Requirement**: FR-T8.1  
**Given**: A Level 1 `collaboration.md` with the following messages:
```
Platform ->> OrderAPI: Create Order
OrderAPI ->> OrderProcessor: Validate
OrderProcessor ->> OrderRepository: Save
OrderRepository -->> OrderProcessor: Saved
OrderProcessor -->> OrderAPI: Validated
OrderAPI -->> Platform: Order Created
```
**When**: Scale management analysis runs on Level 1  
**Then**: Interaction count reported as `6`

**Pass Criteria:**
- [ ] `metrics.interaction_count` equals `6`
- [ ] Count includes both `->>` (request) and `-->>` (response) arrows
- [ ] No error thrown

---

### TC-T8-002: Participant count calculated correctly
**Requirement**: FR-T8.1  
**Given**: A Level 1 `collaboration.md` with participants `Platform`, `OrderAPI`, `OrderProcessor`, `OrderRepository` (4 unique participants)  
**When**: Scale management analysis runs  
**Then**: Participant count reported as `4`

**Pass Criteria:**
- [ ] `metrics.participant_count` equals `4`
- [ ] External actor (outside `box`) and internal participants both counted
- [ ] Duplicate participant declarations not double-counted

---

### TC-T8-003: Nesting depth reported for root level
**Requirement**: FR-T8.1  
**Given**: The root `collaboration.md` at Level 0  
**When**: Scale management analysis runs  
**Then**: Nesting depth reported as `0`

**Pass Criteria:**
- [ ] `metrics.nesting_depth` equals `0`
- [ ] No parent-level references required

---

### TC-T8-004: Nesting depth counts nested `box` blocks, not folder depth
**Requirement**: FR-T8.1  
**Given**: A `collaboration.md` containing two nested `box…end` blocks (a `box SubProcess…end` containing another `box InnerGroup…end`)  
**When**: Scale management analysis runs  
**Then**: Nesting depth reported as `2`

**Pass Criteria:**
- [ ] `metrics.nesting_depth` equals `2`
- [ ] Depth reflects the deepest `box` nesting level within the Mermaid diagram, not the folder hierarchy depth
- [ ] A diagram at Level 3 folder depth containing only one `box` block reports `nesting_depth = 1`

---

### TC-T8-005: Metrics calculated for diagram with no interactions
**Requirement**: FR-T8.1  
**Given**: A newly scaffolded `collaboration.md` with participants declared but no messages  
**When**: Scale management analysis runs  
**Then**: Interaction count is `0`, participant count matches declared participants, depth matches level

**Pass Criteria:**
- [ ] `metrics.interaction_count` equals `0`
- [ ] No divide-by-zero or null-reference errors
- [ ] Metrics object still present in output

---

## Category 2: Complexity Warnings (FR-T8.2)

### TC-T8-006: Level 0 — no warning below advisory zone (<5 interactions)
**Requirement**: FR-T8.2  
**Given**: Root `collaboration.md` (Level 0) with 4 interactions (below advisory threshold ⌊7 × 0.8⌋ = 5)  
**When**: Scale management analysis runs  
**Then**: `complexity_warning` is `"none"` — no warning of any kind emitted

**Pass Criteria:**
- [ ] `complexity_warning` equals `"none"`
- [ ] `metrics.interaction_count` equals `4`
- [ ] No warning text emitted; no entry in `scale_management.advisory_warnings` or `critical_warnings`

---

### TC-T8-007: Level 0 — critical warning generated above threshold (>7 interactions)
**Requirement**: FR-T8.2  
**Given**: Root `collaboration.md` (Level 0) with 10 interactions  
**When**: Scale management analysis runs  
**Then**: `complexity_warning` is `"critical"`; warning message emitted citing Level 0, threshold 7, actual 10

**Pass Criteria:**
- [ ] `complexity_warning` equals `"critical"` (10 > 7 threshold)
- [ ] Warning message includes level number (`0`), threshold (`7`), and actual count (`10`)
- [ ] Node id present in `hierarchy_statistics.scale_management.critical_warnings`

---

### TC-T8-008: Level 0 — warning at exactly threshold + 1 (8 interactions)
**Requirement**: FR-T8.2  
**Given**: Root `collaboration.md` (Level 0) with 8 interactions  
**When**: Scale management analysis runs  
**Then**: Warning generated (threshold is strict: `> 7`)

**Pass Criteria:**
- [ ] `complexity_warning` equals `"critical"` (8 > 7 threshold)
- [ ] Confirms boundary conditions: at 7 interactions → `"advisory"` (80 % zone: ⌊7×0.8⌋=5 to 7 inclusive); at 8 interactions → `"critical"` (above threshold)

---

### TC-T8-009: Level 1 — no warning below advisory zone (<9 interactions)
**Requirement**: FR-T8.2  
**Given**: Level 1 `collaboration.md` with 8 interactions (below advisory threshold ⌊12 × 0.8⌋ = 9)  
**When**: Scale management analysis runs  
**Then**: `complexity_warning` is `"none"` — no warning of any kind emitted

**Pass Criteria:**
- [ ] `complexity_warning` equals `"none"`
- [ ] `metrics.interaction_count` equals `8`
- [ ] No entry in `scale_management.advisory_warnings` or `critical_warnings` for this node

---

### TC-T8-010: Level 1 — warning generated above threshold (>12 interactions)
**Requirement**: FR-T8.2  
**Given**: Level 1 `collaboration.md` with 15 interactions  
**When**: Scale management analysis runs  
**Then**: Warning generated: `"Level 1 exceeds recommended 12 interactions (actual: 15)"`

**Pass Criteria:**
- [ ] `complexity_warning` equals `"critical"` (15 > 12 threshold)
- [ ] Warning message references level `1`, threshold `12`, actual `15`
- [ ] Existing task seed test case TC from T8 task is satisfied

---

### TC-T8-011: Level N (N ≥ 2) uses the same 12-interaction threshold
**Requirement**: FR-T8.2  
**Given**: Level 3 `collaboration.md` with 13 interactions  
**When**: Scale management analysis runs  
**Then**: Warning generated citing threshold `12`

**Pass Criteria:**
- [ ] `complexity_warning` equals `"critical"` (13 > 12 threshold)
- [ ] Warning message references level `3` and threshold `12`
- [ ] Confirms threshold rule: Level 0 = 7, all other levels = 12

---

### TC-T8-012: Multiple levels analyzed — warnings are level-scoped
**Requirement**: FR-T8.2  
**Given**: A hierarchy where Level 0 has 8 interactions (`critical`: 8 > 7) and Level 1 has 8 interactions (`none`: 8 < advisory threshold of 9)  
**When**: Scale management analysis runs across the full hierarchy  
**Then**: Level 0 reports `complexity_warning = "critical"`; Level 1 reports `complexity_warning = "none"`

**Pass Criteria:**
- [ ] Level 0 node `complexity_warning` equals `"critical"`
- [ ] Level 1 node `complexity_warning` equals `"none"`
- [ ] `hierarchy_statistics.scale_management.critical_warnings` contains Level 0 node id only; Level 1 absent from both warning lists

---

## Category 3: Decomposition Suggestions (FR-T8.3)

### TC-T8-013: Control-type participant with high interactions suggested
**Requirement**: FR-T8.3  
**Given**: `OrderProcessor@{ "type": "control" }` appears in 8 messages (4 incoming + 4 outgoing)  
**When**: Decomposition candidates are identified  
**Then**: `OrderProcessor` is included in the decomposition suggestions

**Pass Criteria:**
- [ ] `decomposition_candidates` array contains `OrderProcessor`
- [ ] Entry includes `participant`, `type: "control"`, and `interaction_count: 8`
- [ ] Existing task seed test case TC from T8 task is satisfied

---

### TC-T8-014: Entity-type participant with high interactions not suggested
**Requirement**: FR-T8.3  
**Given**: `OrderRepository@{ "type": "entity" }` appears in 10 messages  
**When**: Decomposition candidates are identified  
**Then**: `OrderRepository` is NOT included in decomposition suggestions

**Pass Criteria:**
- [ ] `decomposition_candidates` array does not contain `OrderRepository`
- [ ] Confirms entity-type exclusion regardless of interaction count

---

### TC-T8-015: Boundary-type participant with high interactions not suggested
**Requirement**: FR-T8.3  
**Given**: `OrderAPI@{ "type": "boundary" }` appears in 9 messages  
**When**: Decomposition candidates are identified  
**Then**: `OrderAPI` is NOT included in decomposition suggestions

**Pass Criteria:**
- [ ] `decomposition_candidates` array does not contain `OrderAPI`
- [ ] Confirms boundary-type exclusion

---

### TC-T8-016: Control-type participant with low interactions not suggested
**Requirement**: FR-T8.3  
**Given**: `PaymentProcessor@{ "type": "control" }` appears in 2 messages  
**When**: Decomposition candidates are identified  
**Then**: `PaymentProcessor` is NOT included in decomposition suggestions

**Pass Criteria:**
- [ ] `decomposition_candidates` array does not contain `PaymentProcessor`
- [ ] Confirms interaction count threshold filters low-volume controls
- [ ] No error thrown

> **Note**: The minimum interaction count threshold is `decomposition_candidate_min_interactions = 5` (SKILL.md Default Thresholds table). With 2 messages, `PaymentProcessor` is below this threshold and correctly excluded.

---

### TC-T8-017: Multiple control-type candidates ranked by interaction count
**Requirement**: FR-T8.3  
**Given**: Two control-type participants — `OrderProcessor` (12 interactions) and `PaymentService` (8 interactions) — both exceeding the suggestion threshold  
**When**: Decomposition candidates are identified  
**Then**: Both are listed; `OrderProcessor` appears before `PaymentService` (ranked descending by count)

**Pass Criteria:**
- [ ] `decomposition_candidates` has 2 entries
- [ ] Entry order is `OrderProcessor` (12) then `PaymentService` (8)
- [ ] Each entry contains `interaction_count`

---

### TC-T8-018: No control-type participants — empty candidates list
**Requirement**: FR-T8.3  
**Given**: A diagram with only `actor` and `entity` participants  
**When**: Decomposition candidates are identified  
**Then**: `decomposition_candidates` is an empty array; no error thrown

**Pass Criteria:**
- [ ] `decomposition_candidates` equals `[]`
- [ ] No null-reference or undefined errors

---

## Category 4: Hierarchy Statistics (FR-T8.4)

### TC-T8-019: Total levels tracked correctly (flat hierarchy)
**Requirement**: FR-T8.4  
**Given**: A hierarchy with only Level 0 (root, no children)  
**When**: Hierarchy statistics are generated  
**Then**: `max_depth` equals `0` (hierarchy depth is 0-based; 1 total level)

**Pass Criteria:**
- [ ] `hierarchy_statistics.max_depth` equals `0` (total levels = max_depth + 1 = 1)
- [ ] `hierarchy_statistics.decomposed_count` equals `0` (no decompositions performed)
- [ ] `hierarchy_statistics.leaf_count` equals `1` (root is the only node and has no children)

---

### TC-T8-020: Total levels tracked correctly (2-level hierarchy)
**Requirement**: FR-T8.4  
**Given**: Root (Level 0) with two Level 1 children: `01-OrderService/` and `02-PaymentService/`  
**When**: Hierarchy statistics are generated  
**Then**: `total_levels` equals `2`

**Pass Criteria:**
- [ ] `hierarchy_statistics.max_depth` equals `1` (total levels = 2)
- [ ] `hierarchy_statistics.decomposed_count` equals `2` (two control-type nodes decomposed: root's two children)
- [ ] `hierarchy_statistics.leaf_count` equals `2` (both Level 1 nodes have no children)
- [ ] `hierarchy_statistics.nodes_by_level["0"]` equals `1`, `nodes_by_level["1"]` equals `2`

---

### TC-T8-021: Leaf processes identified correctly in branching hierarchy
**Requirement**: FR-T8.4  
**Given**: Root → L1A (`01-OrderService/`), L1B (`02-PaymentService/`); L1A → L2A (`01-ValidationEngine/`); L1B has no children  
**When**: Hierarchy statistics are generated  
**Then**: `leaf_processes` equals `2` (L2A and L1B)

**Pass Criteria:**
- [ ] `hierarchy_statistics.leaf_count` equals `2`
- [ ] L1A is NOT counted as a leaf (it has a child; `status = "decomposed"`)
- [ ] L2A and L1B ARE counted as leaves (`status = "leaf"` or `"available"` with no children)

---

### TC-T8-022: Total boundaries count matches decomposition count
**Requirement**: FR-T8.4  
**Given**: 3 decompositions have been performed, creating 3 sub-process folders  
**When**: Hierarchy statistics are generated  
**Then**: `total_boundaries` equals `3`

**Pass Criteria:**
- [ ] `hierarchy_statistics.decomposed_count` equals `3`
- [ ] Root Level 0 origin node not counted (it has not been decomposed from a parent perspective)

---

### TC-T8-023: Statistics update after a new decomposition
**Requirement**: FR-T8.4  
**Given**: Statistics previously showed `total_levels: 2, leaf_processes: 2`; a new Level 2 sub-process is now created under one of the Level 1 processes  
**When**: Hierarchy statistics are regenerated  
**Then**: `total_levels` becomes `3`; `leaf_processes` becomes `2` (the new L2 node replaces its parent as the leaf)

**Pass Criteria:**
- [ ] `hierarchy_statistics.max_depth` equals `2` (total levels = 3)
- [ ] `hierarchy_statistics.leaf_count` equals `2`
- [ ] Previous Level 1 parent node status updated from `"available"` to `"decomposed"`; removed from `hierarchy_statistics.leaf_count`

---

## Category 5: Metrics Integration into Hierarchy Metadata (TR-T8.1)

### TC-T8-024: Metrics written to hierarchy-metadata.json
**Requirement**: TR-T8.1  
**Given**: Scale management analysis completes for a Level 1 diagram  
**When**: Output is persisted  
**Then**: `hierarchy-metadata.json` contains a `complexity_metrics` object on the analysed node

**Expected JSON structure:**
```json
{
  "nodes": {
    "OrderService": {
      "level": 1,
      "source_diagram": "01-OrderServiceBoundary/collaboration.md",
      "complexity_metrics": {
        "interaction_count": 9,
        "participant_count": 4,
        "nesting_depth": 1,
        "complexity_warning": "none",
        "decomposition_candidates": []
      }
    }
  }
}
```

**Pass Criteria:**
- [ ] `complexity_metrics` key present on the node entry in `nodes`
- [ ] `interaction_count`, `participant_count`, `nesting_depth` all non-null integers
- [ ] `complexity_warning` is one of `"none"` / `"advisory"` / `"critical"`
- [ ] `decomposition_candidates` is an array (may be empty)

---

### TC-T8-025: Metadata updated without overwriting existing hierarchy data
**Requirement**: TR-T8.1  
**Given**: `hierarchy-metadata.json` already contains `parent_path`, `children`, and `level` fields for Level 1  
**When**: Scale management metrics are written  
**Then**: Existing fields are preserved; only `scale_metrics` is added or updated

**Pass Criteria:**
- [ ] `parent_id` field unchanged
- [ ] `children` array unchanged
- [ ] `level` field unchanged
- [ ] `complexity_metrics` added/updated with new values; all other node fields intact

---

### TC-T8-026: Hierarchy-level statistics written to root metadata
**Requirement**: TR-T8.1 + FR-T8.4  
**Given**: Full hierarchy analysis completes  
**When**: Statistics are persisted  
**Then**: Root `hierarchy-metadata.json` contains a populated `hierarchy_statistics` section

**Expected JSON structure:**
```json
{
  "last_updated": "2026-03-14T00:00:00Z",
  "hierarchy_statistics": {
    "total_nodes": 7,
    "max_depth": 2,
    "leaf_count": 3,
    "decomposed_count": 4,
    "boundary_count": 4,
    "nodes_by_level": { "0": 1, "1": 2, "2": 4 },
    "scale_management": {
      "critical_warnings": [],
      "advisory_warnings": [],
      "decomposition_candidates": [],
      "total_interactions_by_level": { "0": 6, "1": 9, "2": 14 }
    }
  }
}
```

**Pass Criteria:**
- [ ] `hierarchy_statistics` key present at root level of the JSON
- [ ] `max_depth`, `leaf_count`, `decomposed_count`, `boundary_count` all present and correct
- [ ] `last_updated` ISO 8601 timestamp present at root level
- [ ] `scale_management` sub-object present with `critical_warnings`, `advisory_warnings`, `decomposition_candidates`, `total_interactions_by_level`

---

## Category 6: Configurable Thresholds (TR-T8.2)

### TC-T8-027: Default thresholds applied when no configuration provided
**Requirement**: TR-T8.2  
**Given**: No custom threshold configuration; Level 0 diagram with 8 interactions  
**When**: Scale management analysis runs  
**Then**: Default Level 0 threshold of `7` applies; warning generated

**Pass Criteria:**
- [ ] Warning generated for Level 0 at 8 interactions
- [ ] Default thresholds (Level 0 = 7, Level N = 12) documented/referenced

---

### TC-T8-028: Custom Level 0 threshold overrides default
**Requirement**: TR-T8.2  
**Given**: `hierarchy-metadata.json` sets `complexity_thresholds.level_0_max_interactions: 10`; Level 0 diagram has 9 interactions  
**When**: Scale management analysis runs  
**Then**: No warning generated (9 ≤ custom threshold of 10 — below advisory zone ⌊10×0.8⌋ = 8)

**Pass Criteria:**
- [ ] `complexity_warning` equals `"none"`
- [ ] Confirms custom threshold takes precedence over default (`7`)

---

### TC-T8-029: Custom Level N threshold overrides default
**Requirement**: TR-T8.2  
**Given**: `hierarchy-metadata.json` sets `complexity_thresholds.level_n_max_interactions: 8`; Level 2 diagram has 10 interactions  
**When**: Scale management analysis runs  
**Then**: `complexity_warning` is `"critical"` citing custom threshold `8`

**Pass Criteria:**
- [ ] `complexity_warning` equals `"critical"` (10 > custom threshold 8)
- [ ] Warning message references threshold `8` (not default `12`) and Level `2`, actual `10`

---

### TC-T8-030: Invalid threshold configuration handled gracefully
**Requirement**: TR-T8.2  
**Given**: `hierarchy-metadata.json` sets `complexity_thresholds.level_0_max_interactions: -1` (invalid negative value)  
**When**: Scale management analysis runs  
**Then**: Error or fallback to default threshold; no crash

**Pass Criteria:**
- [ ] Either: validation error surfaced describing invalid threshold
- [ ] Or: default threshold silently applied with a log/notice
- [ ] No uncaught exception or null-pointer error

---

## Summary

| ID | Category | Requirement | Status |
|----|----------|-------------|--------|
| TC-T8-001 | Metrics Calculation | FR-T8.1 | ✅ Pass |
| TC-T8-002 | Metrics Calculation | FR-T8.1 | ✅ Pass |
| TC-T8-003 | Metrics Calculation | FR-T8.1 | ✅ Pass |
| TC-T8-004 | Metrics Calculation | FR-T8.1 | ✅ Pass |
| TC-T8-005 | Metrics Calculation | FR-T8.1 | ✅ Pass |
| TC-T8-006 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-007 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-008 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-009 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-010 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-011 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-012 | Complexity Warnings | FR-T8.2 | ✅ Pass |
| TC-T8-013 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-014 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-015 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-016 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-017 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-018 | Decomposition Suggestions | FR-T8.3 | ✅ Pass |
| TC-T8-019 | Hierarchy Statistics | FR-T8.4 | ✅ Pass |
| TC-T8-020 | Hierarchy Statistics | FR-T8.4 | ✅ Pass |
| TC-T8-021 | Hierarchy Statistics | FR-T8.4 | ✅ Pass |
| TC-T8-022 | Hierarchy Statistics | FR-T8.4 | ✅ Pass |
| TC-T8-023 | Hierarchy Statistics | FR-T8.4 | ✅ Pass |
| TC-T8-024 | Metadata Integration | TR-T8.1 | ✅ Pass |
| TC-T8-025 | Metadata Integration | TR-T8.1 | ✅ Pass |
| TC-T8-026 | Metadata Integration | TR-T8.1 + FR-T8.4 | ✅ Pass |
| TC-T8-027 | Configurable Thresholds | TR-T8.2 | ✅ Pass |
| TC-T8-028 | Configurable Thresholds | TR-T8.2 | ✅ Pass |
| TC-T8-029 | Configurable Thresholds | TR-T8.2 | ✅ Pass |
| TC-T8-030 | Configurable Thresholds | TR-T8.2 | ✅ Pass |

**Total**: 30 test cases
