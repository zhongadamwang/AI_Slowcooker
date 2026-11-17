---
name: model-integration
description: Plan how a project's new and aligned domain concepts integrate into the organization's existing domain models: integration points, entity-mapping conflicts and their resolution, the least disruptive integration strategy, coherence checks across affected processes, and stakeholder impact, written as model-integration.md/.json, integration-impact-assessment.md, and integration-validation.json. Use after domain-alignentities (and domain-proposenewconcepts, if run) when new domain concepts must be merged into OrgDocument/orgModel, or when the user asks what integrating them would affect. Produces a plan for orgmodel-update to apply; it does not edit the orgModel.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# Model Integration

Systematically combine new domain models and processes into existing organizational model structures while maintaining coherence and minimizing disruption through sophisticated conflict resolution and progressive integration strategies.

## Intent
Implement comprehensive model integration that analyzes integration points, resolves entity mapping conflicts, maintains model coherence, and plans a progressive integration that `orgmodel-update` applies. Follows EDP methodology principles for minimal disruption while ensuring cross-process consistency and stakeholder impact analysis.

### Boundary and Use-Case/UI Model Awareness

When target models include boundary-decomposed hierarchies with use-case and/or UI models (per `usecase-generatemodel`/`ui-generatemodel`, PRJ-07), integration points touching entities that a use case or `UIModelEntry` already references must preserve those references rather than silently breaking them. Specifically: if this skill's `entity_integration` renames, merges, or specializes an entity that appears in a boundary's `use-case-model.json` (`referenced_entities`, via its scripts' Main Flow entity citations) or `ui-model.json` (`domain_entity_refs`), the integration plan must flag those as **affected use cases/UI entries requiring a fresh modeling round** (see [cross-model-alignment-contract.md](../model-validatealignment/references/cross-model-alignment-contract.md) Section 4.1) — not merely as a stakeholder-impact note. This is additive to the existing `integration_points`/`conflict_resolutions` schema: add an optional `affected_use_case_refs`/`affected_ui_model_refs` array to an integration point when applicable; omit entirely when a boundary has no use-case/UI model yet (most integrations, especially early in a project, will have nothing to flag here).

## Role: Plans Only

This skill **plans**; it does not edit `OrgDocument/orgModel/`. Its outputs say what should change and why. `orgmodel-update` is the only skill that writes organizational model documents, and it applies a plan only after the plan is accepted (in `traditional` collaboration mode by the process owner; in `solo` mode by the developer, stated explicitly).

Do not keep backups or rollback data: the orgModel is under version control, so a plan names the files and sections to change, and undoing an applied change is a revert of that commit. Never record a change, validation, or approval in the plan as done when it has not happened.

## Inputs
- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.json` (from domain-alignentities skill)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-newconcepts.json` (from domain-proposenewconcepts skill)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (source concepts)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (for impact traceability)
- **Existing**: `OrgDocument/orgModel/**/*domain-model.md` (target organizational models)
- **Existing**: `OrgDocument/orgModel/**/*process.md` (existing process flows)
- **Existing**: `OrgDocument/orgModel/**/*vocabulary.md` (organizational terminology)

## Outputs
**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/model-integration.json` - Structured integration plan and results
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/model-integration.md` - Human-readable integration report
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/integration-impact-assessment.md` - Stakeholder impact analysis
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/integration-validation.json` - Planned coherence checks and their expected results

The complete JSON and Markdown templates are in [references/output-format.md](references/output-format.md).

## Core Functions

### 1. Integration Analysis Framework

**Integration Point Detection**
- Analyze alignment results to identify integration opportunities
- Map source concepts to target model structures
- Detect potential conflicts and dependencies
- Assess integration complexity and risk levels

**Conflict Detection Algorithm**
```
for each aligned_entity in domain_alignment:
    if alignment_result.type == "conflict":
        analyze_conflict_type()
        determine_resolution_strategy()
        assess_stakeholder_impact()
        validate_resolution_feasibility()
```

### 2. Minimal Disruption Integration (EDP Methodology)

**Integration Strategies**
- **Additive**: Add new elements without modifying existing structure
- **Replacement**: Replace obsolete elements with minimal impact  
- **Merge**: Combine similar elements with conflict resolution
- **Hybrid**: Combination approach for complex scenarios

**EDP Compliance Checks**
- Preserve existing functionality during integration
- Maintain backward compatibility where possible
- Implement staged deployment with validation checkpoints

### 3. Progressive Integration Support

**Phased Integration Planning**
1. **Phase 1**: Terminology and vocabulary alignment
2. **Phase 2**: Entity integration with conflict resolution
3. **Phase 3**: Relationship and process integration
4. **Phase 4**: Validation and coherence checking

**Staged Deployment**
- Integration checkpoints with validation gates
- Stakeholder approval workflow
- Automated validation testing

### 4. Model Coherence Validation

**Consistency Checks**
- Entity name uniqueness across models
- Relationship integrity and circular dependency detection
- Terminology consistency validation
- Process flow completeness verification

**Cross-Model Validation**
```
validation_rules = {
    "entity_consistency": check_duplicate_entities(),
    "relationship_integrity": validate_all_relationships(),
    "terminology_alignment": verify_vocabulary_consistency(),
    "process_completeness": validate_process_flows()
}
```

### 5. Integration Impact Assessment

**Stakeholder Analysis**
- Identify affected processes and systems
- Assess training and communication requirements
- Evaluate business process impacts
- Determine approval workflow requirements

**Impact Categories**
- **Technical**: System changes, interface modifications
- **Process**: Business workflow adjustments
- **Training**: User education requirements
- **Communication**: Stakeholder notification needs

## Usage Workflow

### Input Validation
```
required_inputs = [
    "domain-alignment.json",
    "target orgModel structure"
]
validate_input_completeness()
load_existing_models()
analyze_integration_complexity()
```

### Integration Execution
```
1. Plan integration phases
2. Resolve conflicts systematically
3. Apply minimal disruption strategies
4. Validate model coherence
5. Generate integration documentation
6. Assess stakeholder impact
```

## Integration Patterns

### Entity Integration Pattern
```markdown
## Existing Entity: [Entity Name]
[Original definition and relationships]

### Integration Changes
- **New Attributes**: [Added attributes from source concepts]
- **Modified Relationships**: [Updated relationship definitions]  
- **Specializations**: [New specialized subtypes]

### Backward Compatibility
- [Existing functionality preserved]
- [Migration path for dependent systems]
```

### Process Integration Pattern
```markdown
## Process: [Process Name]
### Original Process Flow
[Existing process description]

### Integrated Enhancements
[New activities and decision points from requirements]

### Impact Assessment
- **Modified Activities**: [List of changed activities]
- **New Dependencies**: [Additional process dependencies]
- **Stakeholder Effects**: [Affected roles and responsibilities]
```

## Error Handling

### Integration Failures
- **Circular Dependencies**: Detect and report dependency cycles
- **Conflicting Requirements**: Document irreconcilable conflicts
- **Model Inconsistencies**: Validate structural integrity

### Validation Failures
- **Entity Conflicts**: Resolve naming and definitional conflicts
- **Relationship Violations**: Fix broken or invalid relationships
- **Process Inconsistencies**: Align process flow requirements
- **Terminology Mismatches**: Standardize vocabulary usage

## Dependencies
- **domain-alignentities**: Entity mapping and conflict identification
- **domain-proposenewconcepts**: Gap analysis and new concept definitions
- **orgmodel-update**: Applies the accepted integration plan (the only writer to the orgModel)
- **change-management**: Integration tracking and approval workflow
- **model-validatealignment** *(conditional)*: when a boundary has a use-case/UI model, this skill's entity-integration plan should flag affected `use_case_id`/`entry_id` references per the Boundary and Use-Case/UI Model Awareness section above, so a fresh alignment round can be triggered rather than silently invalidating those references

## Success Criteria
- Every integration point has a planned resolution
- Model coherence validation passes
- Stakeholder impact assessment complete
- EDP methodology compliance verified
- Progressive integration milestones achieved

## Completion Gate

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py model-integration \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```
