# T14 Skills Integration — Test Cases

**Skill Under Test**: Cross-skill framework integration for all Project 3 skills  
**Created**: March 15, 2026  
**Total Test Cases**: 24  
**Categories**: Backward Compatibility Invocation, Cross-Skill Data Flow, Skill Registration, End-to-End Workflow, Interface Contracts, Navigator Integration

---

## Category 1: Backward Compatible Invocation (FR-T14.1)

### TC-T14-001 — diagram-generatecollaboration: Project 1 Input Accepted
**Given**: Project 1 invocation parameters (no `--mode`, no boundary parameters, flat sequenceDiagram output expected)  
**When**: Enhanced `diagram-generatecollaboration` SKILL.md is invoked  
**Then**:
- Skill produces a functionally equivalent flat `sequenceDiagram` (same messages, same participant aliases)
- No boundary boxes injected when not requested
- No error for missing `--mode` parameter (defaults to flat/legacy mode)
- **Expected result**: PASS

### TC-T14-002 — diagram-generatecollaboration: New Hierarchical Mode Does Not Break Old Mode
**Given**: Same requirements as TC-T14-001; skill invoked with `--mode hierarchical`  
**When**: Skill processes request  
**Then**:
- Output is hierarchical (with boundary boxes) — not identical to Project 1 output
- Old mode (no `--mode` flag) still produces flat output
- Both modes coexist without conflict
- **Expected result**: PASS

### TC-T14-003 — hierarchy-management: No Side Effects on Non-Hierarchy Processes
**Given**: A process folder that does NOT contain a `control`-type participant  
**When**: `hierarchy-management` is invoked  
**Then**:
- Skill emits eligibility check failure (`ERR_NOT_ELIGIBLE`) without modifying any files
- No `hierarchy-metadata.json` created for ineligible processes
- **Expected result**: PASS

---

## Category 2: Cross-Skill Data Flow Compatibility (FR-T14.2, FR-T14.3)

### TC-T14-004 — diagram-generatecollaboration → hierarchy-management Data Flow
**Given**: `diagram-generatecollaboration` output in hierarchical mode generates `collaboration.md` with boundary boxes and `@{ "type": "control" }` annotation  
**When**: `hierarchy-management` consumes that `collaboration.md`  
**Then**:
- `hierarchy-management` correctly identifies the `control`-type participant
- Decomposition proceeds without parsing errors
- **Expected result**: PASS

### TC-T14-005 — hierarchy-management → documentation-automation Data Flow
**Given**: `hierarchy-management` creates a sub-process folder with stub files (containing `[TO BE GENERATED - invoke documentation-automation]` marker)  
**When**: `documentation-automation` is invoked on that folder  
**Then**:
- Skill detects stub marker in all four files
- Content Guard Pre-Check passes (stub content < 10-line threshold)
- Full documentation generated without overwrite prompt
- **Expected result**: PASS

### TC-T14-006 — documentation-automation Output → edps-compliance Input
**Given**: `documentation-automation` generates `collaboration.md` with boundary boxes and `@{ "type": "..." }` stereotypes  
**When**: `edps-compliance` validates that `collaboration.md`  
**Then**:
- Skill reads boundary boxes and participant stereotypes correctly
- VR-1–VR-4 checks run (via delegation to `diagram-generatecollaboration --mode boundary-validation-only`)
- No JSON schema parse errors
- **Expected result**: PASS

### TC-T14-007 — edps-compliance Pre-Condition Gate (→ hierarchy-validation)
**Given**: `edps-compliance` invoked with `--pre-condition hierarchy-validation`  
**When**: `hierarchy-validation` has NOT been run yet  
**Then**:
- `edps-compliance` emits `pre-condition-not-met` error with code `BLOCKED`
- Directs user to run `hierarchy-validation` first
- **Expected result**: PASS

### TC-T14-008 — change-impact-analysis → change-management Data Flow
**Given**: `change-impact-analysis` generates report with `normalized_risk_level` and `critical_flag` fields  
**When**: `change-management` reads the `affected_documents` from the impact report  
**Then**:
- All new fields (`normalized_risk_level`, `critical_flag`, `summary.critical_count`) are successfully parsed
- No schema validation errors in `change-management` consumer
- **Expected result**: PASS

### TC-T14-009 — migration-tools → hierarchy-management Data Flow
**Given**: `migration-tools --mode apply` produces `collaboration-diagrams-enhanced.md` with boundary boxes and participant type annotations  
**When**: `hierarchy-management` is invoked on an enhanced diagram  
**Then**:
- `hierarchy-management` correctly reads `@{ "type": "control" }` annotations from the enhanced diagram
- Decomposition eligible participants identified correctly
- **Expected result**: PASS

### TC-T14-010 — change-impact-analysis → orgmodel-update Data Flow
**Given**: `change-impact-analysis --mode apply` auto-repairs navigational artifacts and produces report  
**When**: `orgmodel-update` is subsequently invoked  
**Then**:
- `orgmodel-update` EDPS-Hierarchy Guard (Step 0) finds `hierarchy-metadata.json` and activates guard
- `orgmodel-update` does not overwrite hierarchy-managed documents without `--force-overwrite`
- **Expected result**: PASS

---

## Category 3: Skill Registration in EDPS Framework (FR-T14.5)

### TC-T14-011 — hierarchy-management Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "decompose process" to navigator  
**Then**:
- Navigator maps intent to `hierarchy-management`
- Skill appears in Available Skills Catalog under "Hierarchy Management" category
- **Expected result**: PASS

### TC-T14-012 — documentation-automation Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "generate documentation" to navigator  
**Then**:
- Navigator maps intent to `documentation-automation`
- **Expected result**: PASS

### TC-T14-013 — edps-compliance Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "check compliance" to navigator  
**Then**:
- Navigator maps intent to `edps-compliance`
- Skill appears under "Compliance & Validation" category
- **Expected result**: PASS

### TC-T14-014 — hierarchy-validation Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "validate hierarchy" to navigator  
**Then**:
- Navigator maps intent → `hierarchy-validation`
- **Expected result**: PASS

### TC-T14-015 — change-impact-analysis Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "analyze change impact" to navigator  
**Then**:
- Navigator maps intent → `change-impact-analysis`
- **Expected result**: PASS

### TC-T14-016 — migration-tools Registered in edps-skill-navigator
**Given**: Updated `edps-skill-navigator/SKILL.md`  
**When**: User says "migrate diagrams" or "upgrade legacy diagrams" to navigator  
**Then**:
- Navigator maps intent → `migration-tools`
- Skill appears under "Hierarchy Management" category
- **Expected result**: PASS

---

## Category 4: SKILL.md Format Standards (TR-T14.1)

### TC-T14-017 — migration-tools SKILL.md Follows Format Standards
**Given**: `migration-tools/SKILL.md`  
**When**: Format audit runs  
**Then**:
- File begins with YAML front-matter (`---` block) containing `name`, `description`, `license`
- `## Core Function` section present with Purpose, Input, Output, Integration fields
- Inputs and Outputs described in tables
- Usage Examples section present
- Version and Last Updated footer present
- **Expected result**: PASS

### TC-T14-018 — All New Project 3 Skills Have SKILL.md Format Compliance
**Given**: SKILL.md files for `hierarchy-management`, `documentation-automation`, `edps-compliance`, `hierarchy-validation`, `change-impact-analysis`, `migration-tools`  
**When**: Format audit runs  
**Then**:
- Each file has YAML front-matter with `name` and `description`
- Each file has at least one Inputs and one Outputs specification section
- **Expected result**: PASS

---

## Category 5: JSON Schema Compatibility (TR-T14.2)

### TC-T14-019 — edps-compliance Report Schema Compatible with Consumers
**Given**: `edps-compliance-report.json` generated by `edps-compliance`  
**When**: Any downstream skill (e.g., `orgmodel-update`, `integration-testing`) reads it  
**Then**:
- `overall_status` field present and one of `COMPLIANT`, `NON_COMPLIANT`, `PARTIALLY_COMPLIANT`, `BLOCKED`
- `score` field present as numeric 0–100
- `rules` array present with per-rule objects
- **Expected result**: PASS

### TC-T14-020 — migration-tools Enhanced JSON Schema Valid
**Given**: `collaboration-diagrams-enhanced.json` produced by `migration-tools`  
**When**: Any downstream skill (`hierarchy-management`, `edps-compliance`) reads it  
**Then**:
- Each enhanced diagram object has `diagram_id`, `migrated_from`, `participants` array, `boundaries` array, `migration_metadata`
- Each participant has `alias`, `label`, `type`, `boundary`, `inference_confidence`
- **Expected result**: PASS

---

## Category 6: End-to-End Workflow (FR-T14.4)

### TC-T14-021 — End-to-End New Hierarchy Workflow
**Given**: Requirements document for a complex system with multi-service interactions  
**When**: Full EDPS workflow runs: `requirements-ingest → goals-extract → domain-extractconcepts → diagram-generatecollaboration (hierarchical) → hierarchy-management → documentation-automation → hierarchy-validation → edps-compliance`  
**Then**:
- Each skill produces valid output consumed by the next
- `hierarchy-validation` report: VALID or MOSTLY_VALID
- `edps-compliance` report: COMPLIANT or PARTIALLY_COMPLIANT (no BLOCKED)
- No schema errors at any skill boundary
- **Expected result**: PASS

### TC-T14-022 — End-to-End Legacy Migration Workflow
**Given**: Project 1 `collaboration-diagrams.md` (flat sequenceDiagrams)  
**When**: Workflow runs: `migration-tools (apply) → hierarchy-management → edps-compliance`  
**Then**:
- Enhanced diagrams produced with boundaries and participant types
- `hierarchy-management` successfully decomposes one control participant
- `edps-compliance` report generated without `ERR_NO_SOURCE`
- **Expected result**: PASS

### TC-T14-023 — Change Impact Workflow Integration
**Given**: A modification to a Level 1 `collaboration.md` file  
**When**: `change-impact-analysis (what-if) → [review] → change-impact-analysis (apply) → orgmodel-update`  
**Then**:
- What-if report shows impacted parent and child artifacts
- Apply mode repairs navigational links
- `orgmodel-update` EDPS-Hierarchy Guard activates and respects hierarchy ownership
- **Expected result**: PASS

---

## Category 7: Navigator Workflow Templates

### TC-T14-024 — Hierarchical Diagram Workflow Template Complete
**Given**: Updated `edps-skill-navigator/SKILL.md` Workflow Templates section  
**When**: Template for "Hierarchical Diagram Workflow" is read  
**Then**:
- Template includes all 5 skill steps: `diagram-generatecollaboration → hierarchy-management → documentation-automation → hierarchy-validation → edps-compliance`
- Legacy Migration Workflow template present with `migration-tools` as first step
- **Expected result**: PASS
