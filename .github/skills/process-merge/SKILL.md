---
name: process-merge
description: Plan how a project's new processes fit the organization's existing process models: find the minimum overlap between new and existing sub-processes by matching domain entities, activities, and decision points, choose the least disruptive strategy for each (extend, specialize, merge, or create), and set out the steps and stakeholder checkpoints, written as process-merge.md/.json and process-integration-plan.md. Use after domain-alignentities when a project introduces or changes processes that may already exist in OrgDocument/orgModel, or when the user asks how new work fits existing processes. Produces a plan for orgmodel-update to apply; it does not edit the orgModel.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# Process Merge

Systematically merges new process models derived from requirements with existing organizational model structures through intelligent overlap analysis, minimal disruption integration, and comprehensive stakeholder validation workflows.

## Intent
Implement true process model integration that analyzes new process elements against existing orgModel structure, identifies minimum sub-process overlap using domain entity matching, and executes systematic integration following EDP methodology principles. Maintains process coherence while preserving existing organizational content and ensuring stakeholder validation at critical integration points.

## Role: Plans Only

This skill **plans**; it does not edit `OrgDocument/orgModel/`. Its outputs say what should change and why. `orgmodel-update` is the only skill that writes organizational model documents, and it applies a plan only after the plan is accepted (in `traditional` collaboration mode by the process owner; in `solo` mode by the developer, stated explicitly).

Do not keep backups or rollback data: the orgModel is under version control, so a plan names the files and sections to change, and undoing an applied change is a revert of that commit. Never record a change, validation, or approval in the plan as done when it has not happened.

## Inputs
- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (new process entities from domain-extractconcepts skill)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.json` (entity mappings from domain-alignentities skill)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (source requirements for traceability)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/w5h-analysis.json` (process context understanding)
- **Existing**: `OrgDocument/orgModel/*/process.md` (existing organizational process flows)
- **Existing**: `OrgDocument/orgModel/*/domain-model.md` (existing domain models for entity mapping)
- **Existing**: `OrgDocument/orgModel/*/vocabulary.md` (organizational terminology consistency)

## Outputs
**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/process-merge.json` - Structured merge plan and overlap analysis
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/process-merge.md` - Human-readable integration report
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/process-integration-plan.md` - Stakeholder review and approval workflow

The complete JSON and Markdown templates are in [references/output-format.md](references/output-format.md).

## Core Functions

### 1. Process Overlap Analysis

**Identifies minimum sub-process overlap through sophisticated entity matching:**

- **Entity-Based Mapping**: Matches new process entities with existing domain models using fuzzy matching and semantic analysis
- **Activity Flow Analysis**: Compares process activities and workflows to identify shared patterns and integration opportunities
- **Decision Point Alignment**: Maps decision criteria and branching logic between new and existing processes
- **Impact Assessment**: Evaluates integration complexity and potential disruption to existing organizational flows

**Algorithm**: Domain entity mapping with coverage optimization to identify minimal viable integration points that preserve maximum existing process integrity.

### 2. EDP Methodology Integration

**Implements Evolutionary Development Process principles for minimal disruption:**

- **Incremental Integration**: Phases integration into digestible stages with validation checkpoints
- **Stakeholder-Driven Validation**: Requires explicit approval at critical integration points
- **Progressive Enhancement**: Extensions over replacements wherever possible

**Philosophy**: "Extend rather than replace, validate before committing, preserve organizational investment."

### 3. Systematic Integration Planning

**Orchestrates integration with comprehensive planning and risk management:**

```markdown
## Integration Strategy Selection

### Minimal Disruption Hierarchy (Preferred Order):
1. **Extension**: Add capabilities to existing processes (lowest risk)
2. **Specialization**: Create specialized variants of existing processes  
3. **Merger**: Combine compatible processes with careful conflict resolution
4. **New Creation**: Establish separate processes only when integration impossible

### Risk Assessment Matrix:
- **Low Risk**: Entity extensions, terminology alignment, documentation updates
- **Medium Risk**: Activity integration, decision point modifications, workflow changes
- **High Risk**: Core process replacement, entity restructuring, fundamental logic changes
```

### 4. OrgModel Structure Preservation

**Maintains existing organizational model integrity during integration:**

- **Content Preservation**: Existing process documentation remains intact unless explicitly changed
- **Cross-Reference Maintenance**: Lists every internal reference and link the change will affect
- **Vocabulary Consistency**: Ensures terminology alignment across all affected organizational models
- **Test Case Continuity**: Lists the test cases the change affects so coverage is preserved

### 5. Stakeholder Validation Workflow

**Implements comprehensive validation and approval process:**

```markdown
## Validation Checkpoints

### Phase 1: Pre-Integration Validation
- Entity mapping review with domain experts
- Process flow compatibility assessment
- Risk assessment validation with process owners
- **Go/No-Go Decision Point**

### Phase 2: Integration Validation  
- Integration results review with stakeholders
- Performance impact assessment
- Business continuity validation
- **Deployment Approval Checkpoint**

### Phase 3: Post-Integration Validation
- Operational validation with end users
- Integration success metrics review
- **Final Acceptance Checkpoint**
```

### Integration with Model-Integration Skill

**Collaborative Workflow:**
```markdown
process-merge skill focuses on process flow integration and overlap analysis
model-integration skill handles entity relationship conflicts and cross-process consistency
orgmodel-update skill applies accepted plans to the organizational model (the only skill that writes it)

Recommended sequence:
1. process-merge → generates integration plan
2. model-integration → resolves entity conflicts  
3. orgmodel-update → applies changes systematically
```

## Completion Gate

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py process-merge \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```
