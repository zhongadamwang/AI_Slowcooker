````skill
---
name: process-merge
description: Merge new process models with existing organizational models by identifying minimum sub-process overlap and implementing systematic integration following EDP methodology principles.
license: MIT
---

# Process Merge

Intelligently merges new process models with existing organizational model structures by identifying the minimum sub-process overlap and implementing systematic integration that preserves organizational coherence while minimizing disruption to existing processes.

## Core Function

**Input**: New process model + existing orgModel structure + domain entity mappings + integration strategy
**Primary Output**: Integrated orgModel with merged process structure
**Secondary Output**: Integration analysis with impact assessment and change documentation
**Output Destination**: 
- Updated orgModel structure in `OrgDocument/orgModel/`
- Integration analysis: `outputs/projects/{project_id}/Analysis/process-integration-analysis.json`
- Change documentation: `outputs/projects/{project_id}/Changes/` (following change management conventions)
**Directory Structure**: Updates existing orgModel hierarchy while preserving process breakdown structure

## Prerequisites

**Required Skills:**
- Domain.AlignEntities (T6): For domain entity mapping between new and existing models
- Domain.ProposeNewConcepts (T7): For identifying gaps requiring new concepts
- OrgModel-Update (T17): For systematic orgModel structure updates
- Model-Integration (T18): For systematic model integration methodology

**Required Context:**
- Existing orgModel structure with process breakdown hierarchy
- New process model analyzed through requirements analysis pipeline
- Domain entity alignments between new and existing models
- Organizational model vocabulary and terminology standards

## Integration Methodology

**Step 1: Process Overlap Analysis**
- Analyze new process model against existing orgModel process hierarchy
- Identify domain entities shared between new and existing processes
- Map process flows and interaction patterns
- Calculate overlap percentage by domain entity coverage

**Step 2: Minimum Sub-Process Identification**
- Find the minimum sub-process model that matches maximum new process coverage by domain entities
- Identify integration points with least organizational disruption
- Determine optimal integration depth (main process vs sub-process level)
- Assess impact on existing collaboration patterns

**Step 3: Integration Planning**
- Generate integration strategy (replace, extend, or hybrid approach)
- Plan staged integration with rollback capabilities
- Identify stakeholder impact and approval requirements
- Create validation checkpoints for integration success

**Step 4: Model Merging**
- Execute systematic integration following EDP principles
- Update orgModel structure while preserving existing content
- Maintain vocabulary consistency and terminology alignment
- Generate updated collaboration diagrams and process documentation

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill after completing domain analysis and having prerequisites satisfied.
Copilot will identify process overlap and implement systematic integration.

Example prompt:
"Use process-merge skill to integrate the new customer onboarding process model with existing CRM processes. Apply minimal disruption strategy with stakeholder validation checkpoints."

Prerequisites check:
- Domain alignment completed (requires T6-T7 output)
- OrgModel structure current (requires T17 availability) 
- Integration framework ready (requires T18 availability)
```

**Integration Workflow:**
```python
# This represents the intended workflow - actual implementation pending prerequisites
from process_merge import ProcessModelIntegrator

integrator = ProcessModelIntegrator()

# Step 1: Analyze overlap
overlap_analysis = integrator.analyze_overlap(
    new_model_path="outputs/projects/PROJECT-001/Analysis/",
    existing_orgmodel_path="OrgDocument/orgModel/",
    domain_mappings="outputs/projects/PROJECT-001/Analysis/domain-alignment.json"
)

# Step 2: Plan integration
integration_plan = integrator.plan_integration(
    overlap_analysis, 
    strategy="minimal_disruption",
    validation_required=True
)

# Step 3: Execute merge
integration_result = integrator.merge_models(
    integration_plan,
    project_id="PROJECT-001"
)
# Creates: 
#   Updated OrgDocument/orgModel/ structure
#   outputs/projects/PROJECT-001/Analysis/process-integration-analysis.json
#   outputs/projects/PROJECT-001/Changes/YYYY-MM-DD-PROC-CHG-xxx-process-integration.md
```

## Output Schema

**Primary Format** - Updated OrgModel Structure:

The skill updates the existing `OrgDocument/orgModel/` hierarchy while maintaining the process breakdown structure:

```
OrgDocument/orgModel/
├── {Process Name}/
│   ├── main.md                    # Updated with integration summary
│   ├── domain-model.md           # Enhanced with new domain entities  
│   ├── process.md                # Updated with merged process steps
│   ├── collaboration.md          # Updated collaboration patterns
│   ├── vocabulary.md             # Enhanced terminology
│   ├── test-case-list.md         # Updated test scenarios
│   └── {Sub-Process}/            # New or updated sub-processes
│       ├── main.md
│       ├── domain-model.md
│       └── ...
```

**Secondary Format** - Integration Analysis (JSON):

```json
{
  "integration_analysis": {
    "timestamp": "2026-02-18T14:30:00Z",
    "project_id": "PROJECT-001",
    "integration_strategy": "minimal_disruption",
    "overlap_analysis": {
      "matching_processes": [
        {
          "existing_process": "Customer Management/Customer Onboarding",
          "new_process": "Enhanced Customer Registration",
          "overlap_percentage": 85,
          "shared_entities": ["Customer", "Account", "Verification"],
          "integration_depth": "sub_process"
        }
      ],
      "total_overlap_coverage": 73,
      "integration_complexity": "medium"
    },
    "integration_plan": {
      "target_process": "Customer Management/Customer Onboarding",
      "integration_type": "enhance_existing",
      "changes_required": [
        {
          "change_type": "process_step_addition",
          "location": "Customer Management/Customer Onboarding/process.md",
          "description": "Add enhanced verification steps from new model",
          "impact_level": "medium"
        },
        {
          "change_type": "domain_entity_enhancement", 
          "location": "Customer Management/Customer Onboarding/domain-model.md",
          "description": "Add enhanced Customer entity attributes",
          "impact_level": "low"
        }
      ]
    },
    "validation_checkpoints": [
      {
        "checkpoint": "stakeholder_review",
        "description": "Review enhanced customer onboarding process",
        "required_approvers": ["Customer Success Lead", "Compliance Officer"],
        "status": "pending"
      }
    ]
  },
  "implementation_results": {
    "files_updated": ["Customer Management/Customer Onboarding/process.md", "Customer Management/Customer Onboarding/domain-model.md"],
    "new_files_created": [],
    "process_coherence_validated": true,
    "vocabulary_consistency_maintained": true,
    "integration_success": true
  }
}
```

**Change Documentation** - Following existing change management format:

````markdown
# Change Record: Process Integration

**Change ID**: 2026-02-18-PROC-CHG-012-integrate-enhanced-customer-onboarding
**Type**: Process Integration
**Impact**: Medium
**Status**: Implemented
**Approval**: Pending Stakeholder Review

## Overview
Integrated enhanced customer onboarding process model with existing Customer Management processes based on 85% domain entity overlap identification.

## Changes Implemented

### Process Updates
- **Customer Management/Customer Onboarding/process.md**: Added enhanced verification steps (lines 45-67)
- **Customer Management/Customer Onboarding/domain-model.md**: Enhanced Customer entity with additional verification attributes

### Integration Analysis
- **Minimum sub-process overlap**: Customer Management/Customer Onboarding (85% entity match)
- **Integration strategy**: Enhanced existing process rather than replacement
- **Disruption level**: Minimal - no existing process flow modifications

## Validation Status
- [ ] Process coherence validated
- [ ] Vocabulary consistency maintained  
- [ ] Stakeholder approval pending
- [ ] Test case updates required

## Rollback Plan
Integration changes isolated to specific process files with version control tags for easy rollback if validation fails.
````

## Implementation Status

**Current Status**: Skill definition created - Implementation pending prerequisites
**Prerequisites Status**: 
- T17 (OrgModel-Update): Not started 
- T18 (Model-Integration): Not started
- Domain skills (T6-T7): Completed

**Next Steps**:
1. Complete T17 (OrgModel-Update skill) for systematic orgModel management
2. Complete T18 (Model-Integration skill) for integration methodology 
3. Implement process-merge skill with full orgModel integration capabilities
4. Test with complex multi-process integration scenarios

## Technical Notes

- Implementation requires sophisticated process analysis and orgModel manipulation capabilities
- Must preserve existing orgModel structure and content integrity
- Should implement EDP methodology principles for minimal disruption
- Requires coordination with change management system for proper documentation
- Must maintain bidirectional traceability between process models and domain entities
- Should support progressive integration with validation checkpoints

## Dependencies

**Hard Dependencies** (must complete first):
- T17: OrgModel-Update Skill
- T18: Model-Integration Skill  
- T6: Domain.AlignEntities Skill
- T7: Domain.ProposeNewConcepts Skill

**Soft Dependencies** (integration enhanced with):
- Change Management Skill (for change documentation)
- T11: Process.FindTopAndUpdate (for process hierarchy management)
- T19: EDPS-Skill-Navigator (for workflow orchestration)

## Validation Criteria

**Integration Success Criteria:**
- orgModel structure integrity maintained
- Process coherence validated across integration points
- Vocabulary consistency preserved
- Change documentation complete and traceable
- Stakeholder validation checkpoints satisfied
- Rollback capabilities tested and available

**Performance Criteria:**
- Integration analysis completion < 2 minutes for standard process models
- orgModel updates preserve existing content with 100% fidelity
- Change impact assessment accuracy > 90% for disruption predictions
````