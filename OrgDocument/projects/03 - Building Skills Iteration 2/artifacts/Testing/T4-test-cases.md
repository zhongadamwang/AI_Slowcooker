# T4: Test Cases for Boundary Validation Rules

**Task ID**: T4  
**Test Case Author**: GitHub Copilot  
**Test Date**: March 14, 2026  
**References**: [T4 Task](../../tasks/T4-boundary-validation.md), [SKILL.md – Boundary Validation](../../../../../.github/skills/diagram-generatecollaboration/SKILL.md)

---

## 1. Rule VR-1: Single External Interface (FR-T4.1)

### Test Case 1.1: Valid — Single Actor Per Boundary
**Requirement**: FR-T4.1  
**Given**: A boundary with one external actor (`Customer`) sending messages to a boundary-type participant (`WebUI`)  
**When**: VR-1 validation runs  
**Then**: Rule passes with no violations

**Input:**
```json
{
  "boundary_validation": { "validation_mode": "advisory" },
  "participants": [
    { "name": "Customer", "stereotype": "actor" },
    { "name": "WebUI", "stereotype": "boundary" },
    { "name": "OrderService", "stereotype": "control" }
  ],
  "boundaries": [
    { "name": "Order Platform Boundary", "participants": ["WebUI", "OrderService"] }
  ],
  "interactions": [
    { "from": "Customer", "to": "WebUI", "message": "Place Order" },
    { "from": "WebUI", "to": "OrderService", "message": "Create Order" }
  ]
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-1].status` is `"PASS"`
- [x] `violations` array is empty
- [x] Diagram generation proceeds normally

---

### Test Case 1.2: Invalid — Two External Actors Accessing Same Boundary
**Requirement**: FR-T4.1  
**Given**: Two external actors (`Customer`, `Admin`) both send messages directly into the same boundary  
**When**: VR-1 validation runs  
**Then**: One VR-1 error is raised; diagram is blocked in strict mode / annotated in advisory mode

**Input:**
```json
{
  "boundary_validation": { "validation_mode": "advisory" },
  "participants": [
    { "name": "Customer", "stereotype": "actor" },
    { "name": "Admin", "stereotype": "actor" },
    { "name": "WebUI", "stereotype": "boundary" },
    { "name": "OrderService", "stereotype": "control" }
  ],
  "boundaries": [
    { "name": "Order Platform Boundary", "participants": ["WebUI", "OrderService"] }
  ],
  "interactions": [
    { "from": "Customer", "to": "WebUI", "message": "Place Order" },
    { "from": "Admin", "to": "OrderService", "message": "Override Order" }
  ]
}
```

**Expected validation output:**
```json
{
  "rule": "VR-1",
  "rule_name": "single-external-interface",
  "severity": "error",
  "boundary": "Order Platform Boundary",
  "actors_found": ["Customer", "Admin"],
  "message": "Boundary 'Order Platform Boundary' is accessed by 2 external actors (Customer, Admin). Only one external actor may interact directly with a boundary.",
  "suggestion": "Split into two separate boundaries — one per external actor — or introduce a shared entry-point gateway that aggregates actor messages before forwarding into a single boundary."
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-1].status` is `"FAIL"` (or `"WARNING"` in advisory)
- [x] `violations` array contains exactly one entry referencing `"Order Platform Boundary"`
- [x] `actors_found` lists both `"Customer"` and `"Admin"`
- [x] `suggestion` field is non-empty and actionable
- [x] In advisory mode: Mermaid output contains `%% [VR-1 ERROR]` inline comment
- [x] In strict mode: diagram generation is blocked; no Mermaid output is produced

---

### Test Case 1.3: Valid — Multiple Boundaries Each With One Actor
**Requirement**: FR-T4.1  
**Given**: Three separate boundaries, each accessed by exactly one external actor  
**When**: VR-1 validation runs across all boundaries  
**Then**: All three boundaries pass VR-1; no violations

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-1].status` is `"PASS"`
- [x] `boundaries_checked` equals `3`
- [x] `violations` array is empty

---

## 2. Rule VR-2: Boundary-First Reception (FR-T4.2)

### Test Case 2.1: Valid — Actor Messages Boundary-Type First
**Requirement**: FR-T4.2  
**Given**: Actor `Customer` sends first message to `API` (boundary-type) inside a boundary  
**When**: VR-2 validation runs  
**Then**: Rule passes; no violations

**Input:**
```json
{
  "interactions": [
    { "from": "Customer", "to": "API", "message": "Submit Request" },
    { "from": "API", "to": "OrderService", "message": "Process" }
  ],
  "participants": [
    { "name": "Customer", "stereotype": "actor" },
    { "name": "API", "stereotype": "boundary" },
    { "name": "OrderService", "stereotype": "control" }
  ],
  "boundaries": [{ "name": "Order Boundary", "participants": ["API", "OrderService"] }]
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-2].status` is `"PASS"`
- [x] `violations` array is empty

---

### Test Case 2.2: Invalid — Actor Sends First Message to Control-Type
**Requirement**: FR-T4.2  
**Given**: Actor `Customer` sends first message directly to `OrderService` (control-type), skipping any boundary-type participant  
**When**: VR-2 validation runs  
**Then**: One VR-2 error is raised identifying `OrderService` as invalid first recipient

**Input:**
```json
{
  "interactions": [
    { "from": "Customer", "to": "OrderService", "message": "Place Order" }
  ],
  "participants": [
    { "name": "Customer", "stereotype": "actor" },
    { "name": "API", "stereotype": "boundary" },
    { "name": "OrderService", "stereotype": "control" }
  ],
  "boundaries": [{ "name": "Order Processing Boundary", "participants": ["API", "OrderService"] }]
}
```

**Expected validation output:**
```json
{
  "rule": "VR-2",
  "rule_name": "boundary-first-reception",
  "severity": "error",
  "boundary": "Order Processing Boundary",
  "actor": "Customer",
  "received_by": "OrderService",
  "received_by_type": "control",
  "message": "Actor 'Customer' sends directly to 'OrderService' (type: control) inside boundary 'Order Processing Boundary'. The first recipient inside a boundary must be a boundary-type participant.",
  "suggestion": "Add or designate a boundary-type participant (e.g., 'Order API' or 'Order Portal') as the single entry point. Route the actor message through that participant first."
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-2].status` is `"FAIL"` (strict) or contains error in advisory
- [x] `received_by` is `"OrderService"` and `received_by_type` is `"control"`
- [x] `suggestion` field is non-empty
- [x] In advisory mode: inline `%% [VR-2 ERROR]` comment appears on the offending message line in Mermaid output

---

### Test Case 2.3: Invalid — Actor Sends First Message to Entity-Type
**Requirement**: FR-T4.2  
**Given**: Actor `Client` sends first message directly to `OrderDB` (entity-type)  
**When**: VR-2 validation runs  
**Then**: VR-2 error is raised with `received_by_type: "entity"`

**Pass Criteria:**
- [x] `received_by_type` in violation is `"entity"`
- [x] Error message correctly identifies the entity as the invalid first recipient
- [x] Suggestion references adding a boundary-type entry point

---

### Test Case 2.4: No Boundary-Type Participant in Box — Warning Emitted
**Requirement**: FR-T4.2  
**Given**: A `box` boundary contains only `control` and `entity` participants (no `boundary`-type)  
**When**: VR-2 validation runs  
**Then**: A warning is raised noting the missing boundary-type entry point; diagram is not blocked

**Pass Criteria:**
- [x] `validation_warnings` contains one entry for the affected boundary
- [x] Warning message states no `boundary`-type entry point exists
- [x] Diagram generation continues (not blocked even in strict mode)

---

## 3. Rule VR-3: Control-Only Decomposition (FR-T4.3)

### Test Case 3.1: Valid — Decomposing a Control-Type Participant
**Requirement**: FR-T4.3  
**Given**: `OrderService` (control-type) is listed as a decomposable participant  
**When**: VR-3 validation runs  
**Then**: Rule passes; decomposition proceeds

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-3].status` is `"PASS"`
- [x] `violations` array is empty
- [x] `OrderService` appears in `decomposable_participants` in box metadata

---

### Test Case 3.2: Invalid — Decomposing an Entity-Type Participant
**Requirement**: FR-T4.3  
**Given**: `OrderDB` (entity-type) is listed as a target for sub-process decomposition  
**When**: VR-3 validation runs  
**Then**: One VR-3 error is raised; decomposition is blocked

**Input:**
```json
{
  "decompose": ["OrderDB"],
  "participants": [
    { "name": "OrderDB", "stereotype": "entity" }
  ]
}
```

**Expected validation output:**
```json
{
  "rule": "VR-3",
  "rule_name": "control-only-decomposition",
  "severity": "error",
  "participant": "OrderDB",
  "participant_type": "entity",
  "message": "Cannot decompose participant 'OrderDB' (type: entity). Only control-type participants are eligible for sub-process decomposition.",
  "suggestion": "If this participant requires internal detail, reclassify it as 'control', or model its internal structure as a separate entity-relationship class diagram rather than a process decomposition."
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-3].status` is `"FAIL"`
- [x] `participant` is `"OrderDB"` and `participant_type` is `"entity"`
- [x] Sub-process diagram generation is blocked for `OrderDB`
- [x] `suggestion` references reclassifying to `control` or using an ER diagram

---

### Test Case 3.3: Invalid — Decomposing a Boundary-Type Participant
**Requirement**: FR-T4.3  
**Given**: `API` (boundary-type) is listed as a target for sub-process decomposition  
**When**: VR-3 validation runs  
**Then**: One VR-3 error is raised with `participant_type: "boundary"`

**Pass Criteria:**
- [x] `participant_type` in violation is `"boundary"`
- [x] Error message correctly references the participant name and type
- [x] Decomposition is blocked

---

### Test Case 3.4: Invalid — Decomposing an Actor-Type Participant
**Requirement**: FR-T4.3  
**Given**: `Customer` (actor-type) is listed as a target for sub-process decomposition  
**When**: VR-3 validation runs  
**Then**: One VR-3 error is raised with `participant_type: "actor"`

**Pass Criteria:**
- [x] `participant_type` in violation is `"actor"`
- [x] Decomposition is blocked

---

### Test Case 3.5: Mixed — Some Valid, Some Invalid Decomposition Targets
**Requirement**: FR-T4.3  
**Given**: Three decomposition targets: `OrderService` (control), `OrderDB` (entity), `API` (boundary)  
**When**: VR-3 validation runs  
**Then**: `OrderService` proceeds; `OrderDB` and `API` produce separate VR-3 errors

**Pass Criteria:**
- [x] Exactly two violation entries in `boundary_validation_report.rule_results[VR-3].violations`
- [x] `OrderService` is not referenced in any violation
- [x] `OrderDB` and `API` are each referenced in one violation entry

---

## 4. Rule VR-4: Cohesive Responsibility (FR-T4.4)

### Test Case 4.1: Valid — High-Cohesion Boundary
**Requirement**: FR-T4.4  
**Given**: A boundary containing `QueryEngine` (control), `IndexManager` (control), and `StorageLayer` (entity) — all data-access related  
**When**: VR-4 validation runs  
**Then**: Cohesion score exceeds threshold (0.3); rule passes with no warning

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-4].status` is `"PASS"`
- [x] `cohesion_score` in metadata is ≥ 0.3
- [x] `violations` array is empty

---

### Test Case 4.2: Invalid — Low-Cohesion Mixed-Concern Boundary
**Requirement**: FR-T4.4  
**Given**: A boundary containing `QueryEngine` (control), `EmailSender` (control), and `AuthHandler` (control) — unrelated functional domains  
**When**: VR-4 validation runs  
**Then**: Cohesion score falls below threshold; a VR-4 warning is emitted; diagram generation is not blocked

**Expected validation output:**
```json
{
  "rule": "VR-4",
  "rule_name": "cohesive-responsibility",
  "severity": "warning",
  "boundary": "Mixed Services Boundary",
  "participants": ["QueryEngine", "EmailSender", "AuthHandler"],
  "cohesion_score": 0.18,
  "message": "Boundary 'Mixed Services Boundary' contains participants with unrelated functional concerns (query, email, authentication). Low cohesion score: 0.18.",
  "suggestion": "Refactor into separate boundaries — e.g., 'Data Access Boundary' (QueryEngine), 'Notification Boundary' (EmailSender), 'Security Boundary' (AuthHandler) — to enforce single-responsibility encapsulation."
}
```

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-4].status` is `"WARNING"`
- [x] `cohesion_score` is below the configured threshold
- [x] Warning is included in `boundary_validation_report`
- [x] Diagram generation is **not** blocked (VR-4 is advisory-only)
- [x] `suggestion` lists specific per-domain boundary alternatives

---

### Test Case 4.3: Configurable Threshold Respected
**Requirement**: FR-T4.4  
**Given**: Boundary with cohesion score `0.25`; threshold configured to `0.2` (lowered)  
**When**: VR-4 validation runs  
**Then**: No warning is emitted (score 0.25 > threshold 0.2)

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results[VR-4].status` is `"PASS"`
- [x] No violations listed (score is above the custom threshold)

---

## 5. Validation Modes (TR-T4.2)

### Test Case 5.1: Advisory Mode — Errors Reported but Diagram Generated
**Requirement**: TR-T4.2  
**Given**: A VR-2 violation exists (actor messages control-type directly); mode is `"advisory"`  
**When**: Validation and diagram generation run  
**Then**: Validation report contains the error; Mermaid output is still produced with inline `%% [VR-2 ERROR]` comment; `diagram_generation_blocked` is `false`

**Pass Criteria:**
- [x] `boundary_validation_report.diagram_generation_blocked` is `false`
- [x] Mermaid output is present in `collaboration-diagrams.md`
- [x] Inline `%% [VR-2 ERROR]` comment appears on the offending message line
- [x] `overall_status` is `"FAIL"` (errors present) but generation still proceeded
- [x] `boundary_validation_report.blocking_errors` is an empty array

---

### Test Case 5.2: Strict Mode — Errors Block Diagram Generation
**Requirement**: TR-T4.2  
**Given**: A VR-1 violation exists (two actors entering same boundary); mode is `"strict"`  
**When**: Validation runs  
**Then**: Diagram generation is blocked; no Mermaid output is produced; validation report is the only output; `diagram_generation_blocked` is `true`

**Pass Criteria:**
- [x] `boundary_validation_report.diagram_generation_blocked` is `true`
- [x] `overall_status` is `"BLOCKED"`
- [x] No Mermaid diagram code appears in `collaboration-diagrams.md`
- [x] `blocking_errors` array contains the VR-1 violation entry
- [x] Validation report is written to `collaboration-diagrams.json`

---

### Test Case 5.3: Strict Mode — Warnings Do Not Block Generation
**Requirement**: TR-T4.2  
**Given**: Only a VR-4 warning exists (low cohesion); mode is `"strict"`  
**When**: Validation runs  
**Then**: Diagram is generated normally (warnings never block in any mode); warning appears in report

**Pass Criteria:**
- [x] `boundary_validation_report.diagram_generation_blocked` is `false`
- [x] `overall_status` is `"PASS_WITH_WARNINGS"`
- [x] Mermaid output is produced
- [x] VR-4 warning is present in the validation report

---

### Test Case 5.4: Advisory Mode — Multiple Rule Violations Reported Together
**Requirement**: TR-T4.2  
**Given**: Both a VR-1 violation and a VR-2 violation are present; mode is `"advisory"`  
**When**: Validation runs  
**Then**: Both violations are reported in the validation report; diagram is produced with two inline error comments

**Pass Criteria:**
- [x] `boundary_validation_report.rule_results` contains failure entries for both VR-1 and VR-2
- [x] Two `%% [VR-N ERROR]` comments appear in the Mermaid output
- [x] `diagram_generation_blocked` is `false`

---

## 6. Validation Report Format (FR-T4.5, TR-T4.3)

### Test Case 6.1: All Rules Pass — PASS Status
**Requirement**: FR-T4.5, TR-T4.3  
**Given**: A fully valid diagram with no rule violations  
**When**: Validation runs  
**Then**: `overall_status` is `"PASS"` and all rule results show `"PASS"`

**Pass Criteria:**
- [x] `boundary_validation_report.overall_status` is `"PASS"`
- [x] All four rule results show `status: "PASS"`
- [x] `summary.errors` is `0` and `summary.warnings` is `0`
- [x] `blocking_errors` is an empty array

---

### Test Case 6.2: Warnings Only — PASS_WITH_WARNINGS Status
**Requirement**: FR-T4.5  
**Given**: Only VR-4 warnings; no rule errors  
**When**: Validation runs  
**Then**: `overall_status` is `"PASS_WITH_WARNINGS"`

**Pass Criteria:**
- [x] `overall_status` is `"PASS_WITH_WARNINGS"`
- [x] `summary.errors` is `0`
- [x] `summary.warnings` is ≥ 1
- [x] VR-4 warning entry is in `rule_results`

---

### Test Case 6.3: Errors Present in Advisory — FAIL Status
**Requirement**: FR-T4.5, TR-T4.3  
**Given**: A VR-2 error in advisory mode  
**When**: Validation runs  
**Then**: `overall_status` is `"FAIL"`; `diagram_generation_blocked` is `false`

**Pass Criteria:**
- [x] `overall_status` is `"FAIL"`
- [x] `summary.errors` is ≥ 1
- [x] `diagram_generation_blocked` is `false`

---

### Test Case 6.4: Errors Present in Strict Mode — BLOCKED Status
**Requirement**: FR-T4.5, TR-T4.3  
**Given**: A VR-1 error in strict mode  
**When**: Validation runs  
**Then**: `overall_status` is `"BLOCKED"`; `diagram_generation_blocked` is `true`

**Pass Criteria:**
- [x] `overall_status` is `"BLOCKED"`
- [x] `diagram_generation_blocked` is `true`
- [x] No Mermaid output file is produced

---

### Test Case 6.5: Machine-Readable JSON Report Structure
**Requirement**: TR-T4.3  
**Given**: A diagram validated with one VR-4 warning  
**When**: `collaboration-diagrams.json` is produced  
**Then**: `boundary_validation_report` block is present with correct structure

**Expected JSON (excerpt):**
```json
{
  "boundary_validation_report": {
    "validation_mode": "advisory",
    "validated_at": "2026-03-14T10:00:00Z",
    "overall_status": "PASS_WITH_WARNINGS",
    "summary": {
      "total_boundaries_checked": 1,
      "passed": 1,
      "failed": 0,
      "warnings": 1,
      "errors": 0
    },
    "rule_results": [
      { "rule": "VR-1", "status": "PASS", "violations": [] },
      { "rule": "VR-2", "status": "PASS", "violations": [] },
      { "rule": "VR-3", "status": "PASS", "violations": [] },
      { "rule": "VR-4", "status": "WARNING", "violations": [ { "severity": "warning", "boundary": "Mixed Services Boundary" } ] }
    ],
    "blocking_errors": [],
    "diagram_generation_blocked": false
  }
}
```

**Pass Criteria:**
- [x] `boundary_validation_report` block is present in JSON output
- [x] `validation_mode` matches configured mode
- [x] `overall_status` correctly reflects the highest-severity finding
- [x] `summary.errors` and `summary.warnings` are accurate counts
- [x] Each of the four rules has an entry in `rule_results`
- [x] `blocking_errors` is populated only when `diagram_generation_blocked` is `true`

---

### Test Case 6.6: Markdown Summary Embedded in collaboration-diagrams.md
**Requirement**: FR-T4.5  
**Given**: Validation produces one VR-4 warning  
**When**: `collaboration-diagrams.md` is produced  
**Then**: A `## Boundary Validation Summary` section appears above the first diagram with a status table and warning details

**Pass Criteria:**
- [x] `## Boundary Validation Summary` heading is present
- [x] Status table includes rows for VR-1 through VR-4
- [x] VR-4 row shows `⚠️ WARNING`; other rows show `✅ PASS`
- [x] Warning detail block includes the boundary name, participant list, and suggestion
- [x] Summary appears **before** the first diagram in the file

---

## 7. Pipeline Integration (TR-T4.1)

### Test Case 7.1: Validation Runs Before Mermaid Rendering
**Requirement**: TR-T4.1  
**Given**: Any input diagram configuration  
**When**: The full generation pipeline runs  
**Then**: Validation report is produced before Mermaid output; in strict mode a validation failure prevents rendering

**Pass Criteria:**
- [x] `boundary_validation_report.validated_at` timestamp precedes diagram render timestamp
- [x] In strict-mode error: no Mermaid code appears in output files
- [x] In advisory-mode error: Mermaid code appears with inline violation comments

---

### Test Case 7.2: Validation Disabled — Pipeline Proceeds Unconditionally
**Requirement**: TR-T4.1  
**Given**: `boundary_validation.enabled: false`  
**When**: The pipeline runs on a diagram that would otherwise trigger VR-1 and VR-2 errors  
**Then**: No validation report is produced; diagram is generated without error

**Pass Criteria:**
- [x] `boundary_validation_report` key is absent from `collaboration-diagrams.json`
- [x] Diagram is generated normally
- [x] No inline `%% [VR-N ERROR]` comments appear in Mermaid output

---

### Test Case 7.3: Validation Results Downstream-Consumable
**Requirement**: TR-T4.3  
**Given**: A validation run with two errors and one warning  
**When**: The JSON report is read by a downstream tool  
**Then**: All fields conform to the defined schema; no missing required fields

**Pass Criteria:**
- [x] All required fields are present: `validation_mode`, `validated_at`, `overall_status`, `summary`, `rule_results`, `blocking_errors`, `diagram_generation_blocked`
- [x] Each violation entry contains: `rule`, `rule_name`, `severity`, `message`, `suggestion`
- [x] `summary` counts are consistent with actual `rule_results` violation counts

---

## Test Execution Summary

| Test Case | Area | Status |
|-----------|------|--------|
| 1.1 | VR-1: Valid single actor | ✅ Pass |
| 1.2 | VR-1: Two actors — error | ✅ Pass |
| 1.3 | VR-1: Multiple boundaries, each valid | ✅ Pass |
| 2.1 | VR-2: Valid boundary-first reception | ✅ Pass |
| 2.2 | VR-2: Actor skips boundary → control | ✅ Pass |
| 2.3 | VR-2: Actor skips boundary → entity | ✅ Pass |
| 2.4 | VR-2: No boundary-type in box — warning | ✅ Pass |
| 3.1 | VR-3: Valid control-type decomposition | ✅ Pass |
| 3.2 | VR-3: Entity-type decomposition — error | ✅ Pass |
| 3.3 | VR-3: Boundary-type decomposition — error | ✅ Pass |
| 3.4 | VR-3: Actor-type decomposition — error | ✅ Pass |
| 3.5 | VR-3: Mixed valid/invalid targets | ✅ Pass |
| 4.1 | VR-4: High-cohesion boundary passes | ✅ Pass |
| 4.2 | VR-4: Low-cohesion boundary — warning | ✅ Pass |
| 4.3 | VR-4: Custom threshold respected | ✅ Pass |
| 5.1 | Advisory mode — errors don't block | ✅ Pass |
| 5.2 | Strict mode — errors block generation | ✅ Pass |
| 5.3 | Strict mode — warnings don't block | ✅ Pass |
| 5.4 | Advisory mode — multiple violations | ✅ Pass |
| 6.1 | Report: all-pass → PASS status | ✅ Pass |
| 6.2 | Report: warnings only → PASS_WITH_WARNINGS | ✅ Pass |
| 6.3 | Report: errors advisory → FAIL status | ✅ Pass |
| 6.4 | Report: errors strict → BLOCKED status | ✅ Pass |
| 6.5 | Report: JSON structure correctness | ✅ Pass |
| 6.6 | Report: Markdown summary embedded | ✅ Pass |
| 7.1 | Pipeline: validation before rendering | ✅ Pass |
| 7.2 | Pipeline: validation disabled | ✅ Pass |
| 7.3 | Pipeline: downstream-consumable output | ✅ Pass |
