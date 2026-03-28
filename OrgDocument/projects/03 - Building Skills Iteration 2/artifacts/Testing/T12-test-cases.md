# T12: Documentation Automation — Test Cases

**Task ID**: T12  
**Created**: March 14, 2026  
**Skill Under Test**: `.github/skills/documentation-automation/SKILL.md`  
**Status**: All 32 test cases executed and passed (March 14, 2026)

---

## Category 1: Hierarchy Level and Process Name Detection (TC-T12-001 – TC-T12-004)

### TC-T12-001: Level detected from `hierarchy-metadata.json` (§1 rule 1)
**Given**: Target folder `01-OrderServiceBoundary/` contains `hierarchy-metadata.json` with `"level": 1` and `"process_name": "Order Service"` for this node  
**When**: Documentation automation runs (§1)  
**Then**:  
- Level is read as `1` (not derived from folder depth)  
- Process name is read as `Order Service` (not parsed from folder name)  
- `main.md` header shows `**Level**: 1` and title `# Order Service Boundary`  
**Result**: PASS

### TC-T12-002: Level derived from folder depth when no `hierarchy-metadata.json` (§1 rule 2)
**Given**: Target folder `01-OrderServiceBoundary/02-ValidationEngineBoundary/` has no `hierarchy-metadata.json`; folder path indicates 2 ancestor `[NN]-[Name]Boundary/` segments  
**When**: Documentation automation runs  
**Then**:  
- Level is computed as 2 (two `[NN]-[Name]Boundary` ancestors)  
- Process name derived: `02-ValidationEngineBoundary` → `Validation Engine`  
- `main.md` shows `**Level**: 2` and title `# Validation Engine Boundary`  
**Result**: PASS

### TC-T12-003: PascalCase expansion of folder name (§1 rule 3)
**Given**: Folder name is `03-EDPSSkillNavigatorBoundary/`  
**When**: Process name is derived  
**Then**: Process name expands to `EDPS Skill Navigator` (spaces inserted at each uppercase boundary after a lowercase letter; all-caps sequences preserved)  
**Result**: PASS

### TC-T12-004: Root Level 0 folder — no parent process name (§1 rule 4)
**Given**: Target folder is the root process folder (no `[NN]-[Name]Boundary/` ancestor)  
**When**: Documentation automation runs  
**Then**:  
- Level is 0  
- Parent process name is `[Root Process]` (placeholder)  
- `main.md` contains no `**Parent Process**` field and no `**Decomposed From**` field  
**Result**: PASS

---

## Category 2: Participant Inventory Extraction (TC-T12-005 – TC-T12-008)

### TC-T12-005: All participant fields extracted correctly (§2 rule 1)
**Given**: `collaboration.md` contains:  
```
participant User@{ "type": "actor", "label": "Developer" }
box rgb(235, 245, 255) EDPS Navigator System
    participant Nav@{ "type": "boundary", "label": "Skill Navigator" }
    participant Skills@{ "type": "control", "label": "AI Agent Skills" }
end
```  
**When**: Participant inventory is extracted (§2)  
**Then**: Registry contains three entries:
- `{ alias: "User", type: "actor", label: "Developer", box_name: "" }`
- `{ alias: "Nav", type: "boundary", label: "Skill Navigator", box_name: "EDPS Navigator System" }`
- `{ alias: "Skills", type: "control", label: "AI Agent Skills", box_name: "EDPS Navigator System" }`  
**Result**: PASS

### TC-T12-006: Message list built with correct arrow types (§2 rule 2)
**Given**: `collaboration.md` contains:  
```
User->>Nav: Submit request
Nav-->>Skills: Process
Skills-xUser: Cancel
```  
**When**: Message list is built  
**Then**: Message list contains three entries:
- `{ from: "User", to: "Nav", label: "Submit request", async: false }`
- `{ from: "Nav", to: "Skills", label: "Process", async: true }`
- `{ from: "Skills", to: "User", label: "Cancel", async: false }`  
**Result**: PASS

### TC-T12-007: `involvement_count` calculated per participant (§2 rule 3)
**Given**: Three messages: `User->>Nav`, `Nav->>Skills`, `Skills-->>Nav`, `Nav-->>User`  
**When**: Involvement counts are calculated  
**Then**:  
- `User`: involvement_count = 2 (sender in msg 1, receiver in msg 4)  
- `Nav`: involvement_count = 4 (receiver in 1, sender in 2, receiver in 3, sender in 4)  
- `Skills`: involvement_count = 2 (receiver in 2, sender in 3)  
**Result**: PASS

### TC-T12-008: Participants outside all boxes have empty `box_name` (§2 rule 1)
**Given**: `collaboration.md` has an actor participant `User` declared before any `box` block  
**When**: Participant inventory is extracted  
**Then**: `User` has `box_name: ""` (empty string)  
**Result**: PASS

---

## Category 3: `main.md` Generation — FR-T12.1 (TC-T12-009 – TC-T12-013)

### TC-T12-009: Complete `main.md` structure for a Level 1 process (§3, FR-T12.1)
**Given**: Level 1 process `Order Service` inside root `Skill Dev Process`; has a control participant `LogicEngine`; no sub-folders yet; VR-1 and VR-2 compliant  
**When**: `main.md` is generated  
**Then**: `main.md` contains all required sections:
- `**Level**: 1`, `**Parent Process**: [Skill Dev Process](../main.md)`, `**Status**: Active`
- `## Navigation` with breadcrumb and parent process link
- `## Overview` section with functional-scope description (Level 1 content guide)
- `## Participant Summary` table
- `## Boundary Rules Applied` table with `✓ Compliant` for VR-1 and VR-2
- `## Decomposition Status` table showing `LogicEngine | control | Available`
- `## Key Documents` links to collaboration.md, process.md, domain-model.md  
**Result**: PASS

### TC-T12-010: VR-1 compliance — exactly one boundary participant (§3 boundary rule evaluation)
**Given**: `collaboration.md` has exactly one boundary-type participant (`OrderEntryPoint`) inside the box and one external actor (`Client`)  
**When**: VR-1 is evaluated  
**Then**: `main.md` Boundary Rules Applied table shows `VR-1: Single External Interface | ✓ Compliant`  
**Result**: PASS

### TC-T12-011: VR-2 compliance — boundary is first recipient (§3 boundary rule evaluation)
**Given**: First message arrow in `collaboration.md` is `Client->>OrderEntryPoint: Place Order` (actor → boundary)  
**When**: VR-2 is evaluated  
**Then**: `main.md` shows `VR-2: Boundary-First Reception | ✓ Compliant`  
**Result**: PASS

### TC-T12-012: VR-2 violation detected — first message does not target boundary (§3 boundary rule evaluation)
**Given**: First message inside the box is `Client->>LogicEngine: Submit` (actor → control, skipping boundary)  
**When**: VR-2 is evaluated  
**Then**: `main.md` shows `VR-2: Boundary-First Reception | ⚠ Review`  
**Result**: PASS

### TC-T12-013: Decomposition status shows `Decomposed` with link when sub-folder exists (§3)
**Given**: Control participant `LogicEngine` has already been decomposed; sub-folder `01-LogicEngineBoundary/` exists  
**When**: `main.md` Decomposition Status table is generated  
**Then**: Row shows `LogicEngine | control | Decomposed → [01-LogicEngineBoundary](01-LogicEngineBoundary/main.md)`  
**Result**: PASS

---

## Category 4: `process.md` Generation — FR-T12.2 (TC-T12-014 – TC-T12-017)

### TC-T12-014: Generated `process.md` includes required structural elements (§4, FR-T12.2)
**Given**: Level 1 `collaboration.md` with an actor → boundary → control → entity sequence  
**When**: `process.md` is generated  
**Then**: `process.md` contains:
- `<!-- Identifier: P-01 -->` comment at top
- Title `# Order Service — Process Flow`
- `**Parent Process**: [Skill Dev Process](../process.md)` and `**Hierarchy Level**: 1`
- A `flowchart TD` Mermaid diagram block
- `## Process Description` with at least two numbered steps
- `## Boundary Rules Applied` section
- `## Error Handling` section  
**Result**: PASS

### TC-T12-015: `loop` block in `collaboration.md` produces decision loop in flowchart (§4 Flowchart Inference Rule 2)
**Given**: `collaboration.md` contains a `loop Learning Activities` block with 2 inner messages  
**When**: `process.md` flowchart is generated  
**Then**: `flowchart TD` contains a looping construct (or a `subgraph` block) for the loop body; terminal condition leads back to the preceding node  
**Result**: PASS

### TC-T12-016: `alt`/`else` block produces decision diamond (§4 Flowchart Inference Rule 3)
**Given**: `collaboration.md` has an `alt Skills Validated` with an `else Need Improvement` branch  
**When**: `process.md` flowchart is generated  
**Then**: `flowchart TD` contains a diamond decision node with two labeled edges (`Skills Validated` and `Need Improvement`)  
**Result**: PASS

### TC-T12-017: Entry and terminal nodes are actor-boundary edges (§4 Flowchart Inference Rules 4–5)
**Given**: First message in `collaboration.md` is `Client->>OrderEntryPoint: Submit Order`; last response is `OrderEntryPoint-->>Client: Confirmation`  
**When**: `process.md` flowchart is generated  
**Then**: Entry node is `Client` sending to `OrderEntryPoint`; terminal node is `OrderEntryPoint` returning to `Client`; no other actor-boundary interactions precede the entry or follow the terminal  
**Result**: PASS

---

## Category 5: `collaboration.md` Annotation — FR-T12.3 (TC-T12-018 – TC-T12-021)

### TC-T12-018: Missing `@{ "type": "..." }` annotation is added to existing participant (§5 annotation rule 1)
**Given**: `collaboration.md` has `participant SM` (no `@{ }` annotation); SM's alias suggests coordinator behavior  
**When**: Annotation pass runs  
**Then**: `participant SM@{ "type": "control", "label": "Skill Manager" }` is written back; label is inferred from alias using hierarchy-management stereotype inference rules  
**Result**: PASS

### TC-T12-019: `%% BOUNDARY SUMMARY` added when absent (§5 annotation rule 2)
**Given**: `collaboration.md` has a `box EDPS Navigator System` block but no `%% BOUNDARY SUMMARY` comment  
**When**: Annotation pass runs  
**Then**: A `%% [B-1] EDPS Navigator System` comment block is inserted before the first `participant` declaration inside the box, listing all participants, decomposable controls, and external actor  
**Result**: PASS

### TC-T12-020: Level-appropriate `box rgb(...)` color applied (§5 annotation rule 3)
**Given**: Level 2 `collaboration.md` has `box OrderService` (no rgb syntax)  
**When**: Annotation pass runs  
**Then**: Box declaration is updated to `box rgb(235, 255, 240) OrderService` (Level 2 = light green)  
**Result**: PASS

### TC-T12-021: New `collaboration.md` synthesized when folder has none (§5 synthesis path)
**Given**: Sub-folder `01-OrderServiceBoundary/` has no `collaboration.md`; parent `hierarchy-metadata.json` shows `OrderService` was decomposed  
**When**: Documentation automation runs  
**Then**: A new `collaboration.md` is synthesized using the hierarchy-management §3 Level N+1 template; an actor participant representing the external caller, a box with boundary/control/entity participants, and at least one message sequence are present; VR-1, VR-2, VR-3 rules pass  
**Result**: PASS

---

## Category 6: `domain-model.md` Generation — FR-T12.4 (TC-T12-022 – TC-T12-025)

### TC-T12-022: One class generated per participant (§6 class inference rule 1)
**Given**: `collaboration.md` has 4 participants: 1 actor, 1 boundary, 1 control, 1 entity  
**When**: `domain-model.md` is generated  
**Then**: `classDiagram` block contains exactly 4 class declarations, each with the correct `:::[type]` stereotype suffix and 2–3 inferred attributes  
**Result**: PASS

### TC-T12-023: Relationships derived from message arrows (§6 inference rule 3)
**Given**: Message `Client->>OrderEntryPoint: Submit Order` (sync `->>`)  
**When**: `domain-model.md` is generated  
**Then**: Relationship line `Client --> OrderEntryPoint : sends Submit Order` is present in `classDiagram`  
**Result**: PASS

### TC-T12-024: Async arrows produce dependency associations (§6 inference rule 3)
**Given**: Message `OrderEntryPoint-->>Client: Confirmation` (async `-->>`)  
**When**: `domain-model.md` is generated  
**Then**: Relationship line `OrderEntryPoint ..> Client : responds Confirmation` is present  
**Result**: PASS

### TC-T12-025: Level 0 `domain-model.md` omits "Relationships to Parent Domain" section (§6 + Level Content Guide)
**Given**: Target folder is the root process (Level 0); no parent domain model exists  
**When**: `domain-model.md` is generated  
**Then**: Generated file does NOT contain a `## Relationships to Parent Domain` section; `**Parent Process**` field is also absent  
**Result**: PASS

---

## Category 7: Level Content Guide Calibration — TR-T12.1 (TC-T12-026 – TC-T12-028)

### TC-T12-026: Level 0 overview is strategic (§Level Content Guide)
**Given**: Target is a Level 0 root process folder  
**When**: `main.md` Overview section is generated  
**Then**: Overview describes business goals, stakeholder groups, and value proposition at the whole-organisation scope; it does NOT contain component-level or algorithm-level language  
**Result**: PASS

### TC-T12-027: Level 2 process.md includes exception paths and retry logic (§Level Content Guide)
**Given**: Target is a Level 2 sub-system component folder  
**When**: `process.md` Process Description is generated  
**Then**: Steps include at least one error/exception path and one retry or rollback step; description uses technical rather than strategic language  
**Result**: PASS

### TC-T12-028: Level 3 process.md uses pseudocode-level granularity (§Level Content Guide)
**Given**: Target is a Level 3 folder  
**When**: `process.md` is generated  
**Then**: Steps describe specific algorithms or SLA constraints; overview tone references implementation details (data structures, timeouts, API contracts)  
**Result**: PASS

---

## Category 8: Template Customization — TR-T12.2 (TC-T12-029 – TC-T12-032)

### TC-T12-029: Custom `main.md.template` used when present (§Template Customization rule 2)
**Given**: `doc-templates/main.md.template` exists in the root process folder; contains `{{ProcessName}}` and `{{BreadcrumbTrail}}` placeholders  
**When**: Documentation automation generates `main.md` for a Level 1 sub-folder  
**Then**: The custom template is used instead of the built-in; `{{ProcessName}}` is replaced with `Order Service`; `{{BreadcrumbTrail}}` is replaced with the resolved breadcrumb string  
**Result**: PASS

### TC-T12-030: Four file types each have independent template overrides (§Template Customization rule 1)
**Given**: `doc-templates/` contains `process.md.template` and `domain-model.md.template` but not `main.md.template` or `collaboration.md.template`  
**When**: Documentation automation runs  
**Then**: `process.md` and `domain-model.md` use their custom templates; `main.md` and `collaboration.md` fall back to built-in templates  
**Result**: PASS

### TC-T12-031: Unknown placeholder in custom template is left as-is (§Template Customization rule 3)
**Given**: `doc-templates/main.md.template` contains `{{UnknownPlaceholder}}`  
**When**: Documentation automation renders the template  
**Then**: `{{UnknownPlaceholder}}` appears verbatim in the output file (no error raised, no substitution attempted)  
**Result**: PASS

### TC-T12-032: Validation checklist passes for fully generated set (§Validation Checklist)
**Given**: All four files have been generated for a Level 1 process with a VR-1/VR-2-compliant `collaboration.md`  
**When**: Post-generation validation checklist is run  
**Then**: All six checklist items are confirmed:
1. All four files exist  
2. Breadcrumb depth matches folder nesting  
3. Flowchart entry/terminal nodes match collaboration.md first/last messages  
4. Every participant in collaboration.md has `@{ "type": "..." }`  
5. Class count in domain-model.md equals participant count in collaboration.md  
6. VR-1 and VR-2 status in main.md reflects actual collaboration.md structure  
**Result**: PASS
