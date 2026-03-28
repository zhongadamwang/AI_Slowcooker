# T5: Test Cases for Hierarchy Management Skill

**Task ID**: T5  
**Test Case Author**: GitHub Copilot  
**Test Date**: March 14, 2026  
**References**: [T5 Task](../../tasks/T5-hierarchy-management.md), [SKILL.md](../../../../../.github/skills/hierarchy-management/SKILL.md)

---

## 1. Decomposition Eligibility Validation (FR-T5.1, VR-3)

### Test Case 1.1: Valid — Control-Type Participant Accepted
**Requirement**: FR-T5.1  
**Given**: A Level 0 `collaboration.md` containing `OrderService@{ "type": "control" }`  
**When**: User requests decomposition of `OrderService`  
**Then**: Decomposition proceeds; no eligibility error is raised

**Input:**
```json
{
  "parent_diagram": "collaboration.md",
  "target_participant": "OrderService",
  "participant_annotation": { "type": "control", "label": "Order Management Service" }
}
```

**Pass Criteria:**
- [x] No `control-only-decomposition` error in output
- [x] Sub-folder `01-OrderServiceBoundary/` is created
- [x] `hierarchy-metadata.json` is written/updated

---

### Test Case 1.2: Invalid — Entity-Type Participant Rejected
**Requirement**: FR-T5.1  
**Given**: A `collaboration.md` containing `CustomerDB@{ "type": "entity" }`  
**When**: User requests decomposition of `CustomerDB`  
**Then**: Skill returns an error and creates no files

**Expected output:**
```json
{
  "error": "control-only-decomposition",
  "participant": "CustomerDB",
  "type": "entity",
  "message": "Only control-type participants can be decomposed into sub-processes."
}
```

**Pass Criteria:**
- [x] `error` field is `"control-only-decomposition"`
- [x] `type` field is `"entity"`
- [x] No sub-folder is created
- [x] `hierarchy-metadata.json` is not modified

---

### Test Case 1.3: Invalid — Boundary-Type Participant Rejected
**Requirement**: FR-T5.1  
**Given**: A `collaboration.md` containing `WebUI@{ "type": "boundary" }`  
**When**: User requests decomposition of `WebUI`  
**Then**: Error returned; no files created

**Pass Criteria:**
- [x] `error` field is `"control-only-decomposition"`
- [x] `type` field is `"boundary"`
- [x] `suggestion` field is present and mentions reclassifying as `control`

---

### Test Case 1.4: Invalid — Actor-Type Participant Rejected
**Requirement**: FR-T5.1  
**Given**: A `collaboration.md` containing `Customer@{ "type": "actor" }`  
**When**: User requests decomposition of `Customer`  
**Then**: Error returned

**Pass Criteria:**
- [x] `error` field is `"control-only-decomposition"`
- [x] `type` field is `"actor"`

---

## 2. Level N+1 Sub-Process Generation (FR-T5.1, FR-T5.2, FR-T5.3)

### Test Case 2.1: Parent Participant Becomes External Actor at Sub-Level
**Requirement**: FR-T5.2  
**Given**: `ECommercePlatform` (control) at Level 0 is decomposed  
**When**: Level 1 `collaboration.md` is generated  
**Then**: The diagram's external actor is the context that called `ECommercePlatform` (i.e. the parent interaction context), and `ECommercePlatform` is represented as the enclosing `box` name

**Pass Criteria:**
- [x] Level 1 diagram contains a `participant [ParentActor]@{ "type": "actor", ... }` declared before any `box`
- [x] The new `box` is named after the decomposed participant (e.g., `E-commerce Platform Boundary`)
- [x] At least one `boundary`-type participant appears first inside the `box`

---

### Test Case 2.2: Boundary-Type Is First Recipient Inside New Sub-Process
**Requirement**: FR-T5.3  
**Given**: A new Level 1 sub-process is generated for `OrderService`  
**When**: The first inter-actor message is traced  
**Then**: The first participant inside the `box` receiving a message from the external actor has `"type": "boundary"`

**Pass Criteria:**
- [x] First inbound message target inside the box resolves to a `boundary`-type participant
- [x] VR-2 validation on the generated diagram returns `PASS`

---

### Test Case 2.3: Inferred Participants from Parent Diagram Messages
**Requirement**: FR-T5.1  
**Given**: Parent diagram has messages `Platform ->> OrderService: Create Order` and `OrderService ->> PaymentAPI: Process Payment`  
**When**: `OrderService` is decomposed  
**Then**: The generated sub-process contains relevant inferred participants (at minimum a boundary entry point, at least one control, and one entity)

**Pass Criteria:**
- [x] Generated `collaboration.md` contains ≥ 3 participants
- [x] Participant types follow `boundary → control(s) → entity` ordering within the box
- [x] Inferred names reflect domain context (e.g., `OrderAPI`, `OrderProcessor`, `OrderRepository`)

---

### Test Case 2.4: Folder Naming Follows NN-ParticipantBoundary Convention
**Requirement**: TR-T5.1  
**Given**: `OrderService` is the first decomposed participant at Level 0  
**When**: Sub-folder is created  
**Then**: Folder name is `01-OrderServiceBoundary`

**Pass Criteria:**
- [x] Folder name matches pattern `[NN]-[PascalCase]Boundary`
- [x] Ordinal is `01` when no prior sub-folders exist
- [x] Ordinal increments to `02`, `03`, etc., for subsequent decompositions at the same level

---

## 3. Hierarchy Metadata (FR-T5.4, TR-T5.3)

### Test Case 3.1: Metadata Created on First Decomposition
**Requirement**: FR-T5.4, TR-T5.3  
**Given**: No `hierarchy-metadata.json` exists at the process root  
**When**: First decomposition is performed  
**Then**: `hierarchy-metadata.json` is created with a valid structure

**Pass Criteria:**
- [x] File exists at `[process-root]/hierarchy-metadata.json`
- [x] `schema_version` field is present
- [x] `root_process.level` is `0`
- [x] `nodes` map contains the decomposed participant with `status: "decomposed"`
- [x] `hierarchy_statistics` fields are all populated

---

### Test Case 3.2: Parent Node Status Updated to `decomposed`
**Requirement**: FR-T5.4  
**Given**: `OrderService` is decomposed  
**When**: `hierarchy-metadata.json` is updated  
**Then**: `nodes.OrderService.status` is `"decomposed"` and `decomposition_link` points to the child diagram

**Pass Criteria:**
- [x] `nodes.OrderService.status` === `"decomposed"`
- [x] `nodes.OrderService.decomposition_link` contains a valid relative path to the new `collaboration.md`
- [x] `nodes.OrderService.children` contains IDs of all participants in the new sub-process

---

### Test Case 3.3: Child Participants Added to Metadata
**Requirement**: FR-T5.4  
**Given**: Level 1 diagram for `OrderService` contains `[OrderAPI (boundary), OrderProcessor (control), OrderDB (entity)]`  
**When**: Metadata is updated  
**Then**: Three new node entries appear in `nodes` at `level: 1`

**Pass Criteria:**
- [x] `nodes.OrderAPI.type` === `"boundary"` and `nodes.OrderAPI.level` === `1`
- [x] `nodes.OrderProcessor.type` === `"control"` and `nodes.OrderProcessor.status` === `"available"`
- [x] `nodes.OrderDB.type` === `"entity"` and `nodes.OrderDB.status` === `"leaf"`
- [x] All three have `parent_id` === `"OrderService"`

---

### Test Case 3.4: Statistics Recomputed After Decomposition
**Requirement**: FR-T5.4  
**Given**: Root has 2 nodes before decomposition (Customer actor + OrderService control)  
**When**: `OrderService` is decomposed into 3 child participants  
**Then**: `hierarchy_statistics` reflects updated counts

**Pass Criteria:**
- [x] `total_nodes` increases from 2 to 5
- [x] `max_depth` increases from 0 to 1
- [x] `decomposed_count` === 1
- [x] `available_count` === 1 (OrderProcessor is still available)
- [x] `nodes_by_level["0"]` === 2, `nodes_by_level["1"]` === 3

---

## 4. Hierarchy Depth (FR-T5.5)

### Test Case 4.1: Level 2 Decomposition (Three Levels Deep)
**Requirement**: FR-T5.5  
**Given**: An existing Level 0 → Level 1 hierarchy where Level 1 contains `OrderProcessor (control)`  
**When**: `OrderProcessor` is decomposed  
**Then**: Level 2 sub-folder created inside the Level 1 folder with correct relative paths

**Pass Criteria:**
- [x] Folder structure: `[root]/01-OrderServiceBoundary/01-OrderProcessorBoundary/collaboration.md`
- [x] Level 2 `collaboration.md` has external actor matching the Level 1 boundary context
- [x] Level 2 node in metadata has `level: 2`
- [x] Root `hierarchy-metadata.json` `max_depth` is `2`

---

### Test Case 4.2: Five-Level Deep Decomposition
**Requirement**: FR-T5.5  
**Given**: A chain of control-type participants decomposed five levels deep  
**When**: Level 5 decomposition is performed  
**Then**: All levels are created correctly with no depth limit error

**Pass Criteria:**
- [x] Level 5 folder exists and contains valid `collaboration.md` and `main.md`
- [x] `hierarchy-metadata.json` `max_depth` === 5
- [x] All parent navigation links (`../main.md`) resolve correctly at each level
- [x] No error or warning related to hierarchy depth

---

## 5. Navigation and Cross-References

### Test Case 5.1: Parent `main.md` Updated with Sub-Process Link
**Requirement**: FR-T5.1  
**Given**: Parent `main.md` has no Sub-Processes section  
**When**: First decomposition at this level  
**Then**: A Sub-Processes section is added containing a link to the new sub-folder's `main.md`

**Pass Criteria:**
- [x] Parent `main.md` contains `## Sub-Processes` section
- [x] Link format: `[ParticipantName](NN-ParticipantBoundary/main.md)`

---

### Test Case 5.2: Parent `collaboration.md` Annotated with Decomposition Comment
**Requirement**: FR-T5.1  
**When**: Decomposition of `OrderService` is performed  
**Then**: Parent `collaboration.md` contains a `%% Decomposition:` comment referencing the child diagram

**Pass Criteria:**
- [x] Comment line: `%% Decomposition: OrderService → 01-OrderServiceBoundary/collaboration.md`
- [x] Comment appears adjacent to the `participant OrderService` declaration

---

### Test Case 5.3: Generated `main.md` Contains Correct Parent Link
**Requirement**: FR-T5.1  
**Given**: Sub-process `main.md` is generated for `01-OrderServiceBoundary`  
**When**: File is read  
**Then**: It contains `**Parent Process**: [Parent Name](../main.md)` pointing to the parent folder

**Pass Criteria:**
- [x] Front-matter line `**Parent Process**: [Parent Name](../main.md)` is present
- [x] Relative path `../main.md` is correct

---

## 6. Hierarchy Tree Visualization (Should Have)

### Test Case 6.1: Tree Diagram Generated from Metadata
**Requirement**: Should Have (hierarchy tree visualization)  
**Given**: A 3-level hierarchy with 7 nodes  
**When**: User requests hierarchy tree visualization  
**Then**: A Mermaid `flowchart TD` is produced with correct parent-child edges

**Pass Criteria:**
- [x] Output is a valid Mermaid `flowchart TD` block
- [x] All 7 nodes appear
- [x] Edges correspond to `children` arrays in `hierarchy-metadata.json`
- [x] Node colors follow level-based color palette (L0: `#e1f5fe`, L1: `#e8f5e8`, L2: `#fff3e0`)

---

### Test Case 6.2: Tree Diagram Validates with Mermaid Validator
**Requirement**: Should Have  
**Given**: Generated `flowchart TD` from Test Case 6.1  
**When**: Diagram is validated  
**Then**: No syntax errors

**Pass Criteria:**
- [x] Mermaid validator returns no errors
- [x] All node IDs are unique

---

## 7. Decomposition Rollback (Should Have)

### Test Case 7.1: Rollback Reverts Parent Metadata to `available`
**Requirement**: Should Have (decomposition rollback)  
**Given**: `OrderService` has been decomposed; `nodes.OrderService.status` === `"decomposed"`  
**When**: User requests rollback of `OrderService` decomposition  
**Then**: `nodes.OrderService.status` is set back to `"available"` and child nodes are removed

**Pass Criteria:**
- [x] `nodes.OrderService.status` === `"available"`
- [x] `nodes.OrderService.children` is empty `[]`
- [x] `nodes.OrderService.decomposition_link` is `null`
- [x] Child node entries (`OrderAPI`, `OrderProcessor`, `OrderDB`) are removed from `nodes`
- [x] `hierarchy_statistics` recomputed correctly

---

### Test Case 7.2: Rollback Removes Sub-Folder References from Parent Files
**Requirement**: Should Have  
**Given**: Parent `main.md` and `collaboration.md` were updated during decomposition  
**When**: Rollback is performed  
**Then**: Sub-process link removed from parent `main.md` and `%% Decomposition:` comment removed from parent `collaboration.md`

**Pass Criteria:**
- [x] Parent `main.md` no longer contains the `01-OrderServiceBoundary/main.md` link
- [x] Parent `collaboration.md` no longer contains the `%% Decomposition: OrderService →` comment

---

## 8. Hierarchy Statistics (Should Have)

### Test Case 8.1: Statistics Reflect Empty Hierarchy
**Requirement**: Should Have  
**Given**: Process root with 1 control-type participant not yet decomposed  
**When**: Statistics are requested  
**Then**: All metrics are correct for a single-node hierarchy

**Pass Criteria:**
- [x] `total_nodes` === 1
- [x] `max_depth` === 0
- [x] `leaf_count` === 0 (control node is available, not a leaf)
- [x] `decomposed_count` === 0
- [x] `available_count` === 1

---

### Test Case 8.2: Statistics Report Returned in Correct Format
**Requirement**: Should Have (hierarchy statistics)  
**When**: User requests statistics for a 5-level hierarchy  
**Then**: A formatted markdown table is produced with all required metrics

**Pass Criteria:**
- [x] Output contains table with columns: Metric, Value
- [x] Rows: Max Depth, Total Nodes, Leaf Nodes, Decomposed Nodes, Available to Decompose, Breadth at Deepest Level
- [x] All values match `hierarchy-metadata.json` `hierarchy_statistics` fields

---

## 9. JSON Metadata Output Format (TR-T5.3)

### Test Case 9.1: Metadata Validates Against Schema
**Requirement**: TR-T5.3  
**Given**: A `hierarchy-metadata.json` produced by T5 after two decompositions  
**When**: File is read and validated against the schema in `references/hierarchy-metadata-schema.md`  
**Then**: All required fields are present and typed correctly

**Pass Criteria:**
- [x] `schema_version` is a string
- [x] `root_process.level` is `0`
- [x] Every node has `id`, `label`, `type`, `level`, `status`, `parent_id`, `children`, `source_diagram`, `decomposition_link`
- [x] `type` is one of `actor | boundary | control | entity`
- [x] `status` is one of `available | decomposed | leaf`
- [x] `hierarchy_statistics` contains all six required fields

---

## Test Summary

| Category | Test Cases | Must Have | Should Have |
|----------|-----------|-----------|-------------|
| 1. Eligibility Validation | 4 | 4 | 0 |
| 2. Sub-Process Generation | 4 | 4 | 0 |
| 3. Hierarchy Metadata | 4 | 4 | 0 |
| 4. Hierarchy Depth | 2 | 2 | 0 |
| 5. Navigation & Cross-Refs | 3 | 3 | 0 |
| 6. Tree Visualization | 2 | 0 | 2 |
| 7. Rollback | 2 | 0 | 2 |
| 8. Statistics | 2 | 0 | 2 |
| 9. Metadata Format | 1 | 1 | 0 |
| **Total** | **24** | **18** | **6** |

**Executed**: March 14, 2026 — **24/24 PASS** (3 defects found and fixed)  
See [T5-test-results.md](T5-test-results.md) for detailed results.
