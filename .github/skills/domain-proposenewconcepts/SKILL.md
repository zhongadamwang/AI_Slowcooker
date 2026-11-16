---
name: domain-proposenewconcepts
description: Find what a project's domain model is missing and propose additions: requirements no concept supports, incomplete workflows, and absent relationships, each answered by a proposed entity, pattern, or relationship with its justification, impact, and risk, written as domain-newconcepts.md and domain-newconcepts.json. Use after domain-alignentities when the user asks what is missing from the domain model, whether the model covers all requirements, or what new concepts the organization's model should gain; optional in the standard workflow.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Domain Propose New Concepts

Analyze domain gaps and propose new concepts to enhance model completeness and address emerging requirements not covered by existing organizational domain models.

## Intent
Systematically identify missing concepts in domain models by analyzing alignment gaps, requirement coverage, and emerging patterns. Proposes new domain concepts with clear justification, suggests integration approaches, and assesses impact on existing domain structures.

## Inputs
- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.json` (from domain-alignentities skill)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (from domain-extractconcepts skill)
- **References**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (for gap validation)
- **References**: Organizational domain models (`OrgDocument/orgModel/**/*domain-model.md`)

## Outputs
**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-newconcepts.json` - Structured proposal data for programmatic use
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-newconcepts.md` - Human-readable proposal report and planning

### `domain-newconcepts.json` (top level)

| Key | Content |
|---|---|
| `project_id`, `proposal_metadata` | `generated_at`, `source_alignment_file`, `source_concepts_file`, `reference_requirements`, `total_proposals`, `coverage_improvement`, `risk_assessment` |
| `gap_analysis` | `coverage_gaps` (`GAP-001`), `pattern_gaps` (`PAT-001`), `relationship_gaps` (`RELA-001`) |
| `concept_proposals` | `proposal_id` (`PROP-001`), `concept_type`, `name`, `description`, `fills_gap`, `domain_area`, `attributes`, `relationships`, `business_value`, `requirements_addressed`, `implementation_considerations`, `risk_assessment` |
| `pattern_proposals` | `pattern_id` (`PATP-001`), `pattern_name`, `pattern_type`, `fills_gap`, `description`, `phases`, `business_value`, `implementation_impact`, `requirements_supported` |
| `relationship_proposals` | `relationship_id` (`RELP-001`), `fills_gap`, `source_entity`, `target_entity`, `relationship_type`, `cardinality`, `description`, `business_justification`, `requirements_addressed` |
| `impact_analysis` | `organizational_model_changes`, `project_benefits`, `implementation_requirements` |

Every proposal names the gap it fills (`fills_gap`) and the requirement IDs it addresses.

### `domain-newconcepts.md` (sections)

`## Executive Summary`, `## Gap Analysis`, `## Concept Proposals`, `## Impact Analysis`, `## Risk Assessment & Mitigation`, `## Recommendations`.

The complete templates for both files are in [references/output-format.md](references/output-format.md).

## Core Gap Analysis Process

### 1. Coverage Gap Detection
**Requirement Mapping Analysis**:
- **Unaddressed requirements**: Requirements with no supporting domain concepts  
- **Partially covered requirements**: Requirements with incomplete concept support  
- **Orphaned concepts**: Domain concepts not linked to any requirements  
- **Functional holes**: Missing concepts for complete business workflows  

**Entity Completeness Analysis**:
- **Attribute gaps**: Missing attributes needed for requirement fulfillment  
- **Relationship gaps**: Missing connections between related entities  
- **Lifecycle gaps**: Missing stages in entity lifecycles  
- **Data integrity gaps**: Missing constraints and validation concepts  

### 2. Pattern Gap Identification
**Workflow Pattern Analysis**:
- **Process incompleteness**: Workflows missing start, middle, or end stages  
- **Decision point gaps**: Missing concepts for workflow branching  
- **Exception handling gaps**: Missing error and exception management concepts  
- **Integration pattern gaps**: Missing concepts for system interactions  

**Structural Pattern Analysis**:
- **Hierarchy gaps**: Missing parent-child relationship patterns  
- **Composition gaps**: Missing whole-part relationship patterns  
- **Classification gaps**: Missing categorization and typing concepts  
- **Temporal pattern gaps**: Missing time-based relationship patterns  

### 3. Concept Proposal Generation
**Business Value Assessment**:
- **Requirement coverage improvement**: How much gap coverage increases  
- **Stakeholder value proposition**: Clear benefits to business stakeholders  
- **Reusability potential**: Can concept be useful across multiple projects  
- **Strategic alignment**: Fits with organizational domain model evolution  

**Technical Feasibility Analysis**:
- **Implementation complexity**: Development effort and technical challenges  
- **Integration impact**: Effect on existing systems and processes  
- **Data requirements**: New data needs and migration considerations  
- **Performance implications**: System performance and scalability effects  

### 4. Impact Assessment & Risk Analysis
**Organizational Impact**:
- **Model evolution**: Changes to organizational domain models  
- **Process changes**: Updates to business processes and workflows  
- **Training needs**: New concepts requiring stakeholder education  
- **Tool updates**: Systems requiring modification or extension  

**Implementation Risk Assessment**:
- **Technical risks**: Development challenges and system integration issues  
- **Business risks**: Adoption challenges and process disruption  
- **Resource risks**: Time, effort, and skill requirements  
- **Mitigation strategies**: Approaches to minimize identified risks  

## Quality Assurance

### Proposal Validation
- **Requirement traceability**: All proposals linked to specific requirement gaps  
- **Business justification**: Clear value proposition for each concept  
- **Implementation feasibility**: Realistic assessment of development effort  
- **Organizational alignment**: Consistency with existing domain models and standards  

### Gap Analysis Completeness
- **Systematic coverage**: All domain areas analyzed for gaps  
- **Multiple perspective analysis**: Entities, relationships, patterns, and processes  
- **Stakeholder validation**: Proposals are recommendations until a domain expert (in solo mode, the developer in that role, stated explicitly) accepts them; never mark a proposal accepted on its behalf  
- **Priority ranking**: Proposals prioritized by business value and implementation effort  

For detailed gap analysis methodologies and concept proposal templates, see [gap-analysis-patterns.md](references/gap-analysis-patterns.md).

Check the result against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py domain-proposenewconcepts \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration

**Upstream**: `domain-alignentities` (alignment gaps), `domain-extractconcepts`, `requirements-ingest`

**Downstream**: `model-integration` and `orgmodel-update` (accepted proposals), `diagram-generatecollaboration`