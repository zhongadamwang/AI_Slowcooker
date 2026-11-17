---
name: process-findtopandupdate
description: Find the top-level requirements in a project's requirement hierarchy and propose how they should change in light of later analysis (domain concepts, alignment, process-merge results, goals), checking that parent and child requirements stay consistent and listing the orgModel documents each change affects, written as top-requirements-update.md/.json, orgmodel-update-plan.md, and requirement-consistency-report.md. Use after process-merge when detailed analysis has outgrown the original high-level requirements, or when the user asks whether the top-level requirements still hold. Produces proposals; requirement changes go through change-management and orgModel edits through orgmodel-update.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# Process Find Top And Update

Systematically identifies the highest-level requirements in requirement hierarchies and updates them based on comprehensive analysis insights from domain modeling, process integration, and detailed requirement analysis. Ensures consistency across requirement levels while maintaining orgModel document coherence through coordinated updates and traceability preservation.

## Intent

Implement intelligent requirement hierarchy analysis that identifies top-level requirements, applies insights from detailed analysis processes, and updates both requirement documentation and corresponding orgModel elements. Maintains bidirectional consistency between high-level strategic requirements and detailed implementation requirements while preserving change traceability throughout the organizational model structure.

## Role: Plans Only

This skill **plans**; it does not edit `OrgDocument/orgModel/`. Its outputs say what should change and why. `orgmodel-update` is the only skill that writes organizational model documents, and it applies a plan only after the plan is accepted (in `traditional` collaboration mode by the process owner; in `solo` mode by the developer, stated explicitly).

Do not keep backups or rollback data: the orgModel is under version control, so a plan names the files and sections to change, and undoing an applied change is a revert of that commit. Never record a change, validation, or approval in the plan as done when it has not happened.

## Inputs

- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (processed requirements with hierarchy metadata)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (domain entities from analysis)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.json` (entity mappings and alignments)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/process-merge.json` (process integration results)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/w5h-analysis.json` (comprehensive requirement context)
- **Context**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/goals.json` (business goals and success criteria)
- **Existing**: `OrgDocument/orgModel/*/main.md` (existing high-level organizational processes)
- **Existing**: `OrgDocument/orgModel/*/process.md` (detailed process flows)
- **Existing**: `OrgDocument/orgModel/*/domain-model.md` (organizational domain models)

## Outputs

**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/top-requirements-update.json` - Structured hierarchy analysis and update plan
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/top-requirements-update.md` - Human-readable requirement update report
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/orgmodel-update-plan.md` - OrgModel update coordination plan
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirement-consistency-report.md` - Consistency validation and traceability report

The complete JSON and Markdown templates are in [references/output-format.md](references/output-format.md).

## Core Workflow

### 1. Requirement Hierarchy Analysis

**Identification Process:**
- Parse requirement dependency graphs from processed requirements
- Identify top-level requirements with minimal or no dependencies
- Classify requirements by hierarchy level and strategic importance
- Map requirement relationships and influence patterns

**Hierarchy Classification:**
- **Level 1**: Strategic business goals and high-level outcomes
- **Level 2**: Major functional areas and process definitions  
- **Level 3**: Detailed functional and non-functional requirements
- **Level 4**: Implementation-specific requirements and constraints

### 2. Insight Integration Analysis

**Source Integration:**
- Extract relevant insights from domain concept analysis
- Incorporate process integration findings and alignment results
- Apply W5H analysis context for stakeholder and implementation insights
- Align with extracted business goals and success criteria

**Update Strategy:**
- **Refinement**: Enhance requirement clarity and precision
- **Expansion**: Add scope based on discovered domain concepts
- **Alignment**: Adjust terminology and approach for consistency
- **Simplification**: Reduce complexity based on process integration findings

### 3. Consistency Validation

**Hierarchical Consistency:**
- Validate that updated top-level requirements align with child requirements
- Check for conflicting objectives or contradictory specifications
- Ensure requirement decomposition remains logical and complete
- Verify that changes preserve requirement completeness

**Cross-Reference Validation:**
- Validate consistency with domain models and entity definitions
- Check alignment with process integration results
- Verify stakeholder and goal alignment across requirement levels
- Ensure terminology consistency across all requirement levels

### 4. OrgModel Coordination

**Document Identification:**
- Identify orgModel documents affected by requirement updates
- Map requirement changes to corresponding organizational processes
- Determine cross-document consistency requirements
- Plan coordinated update sequences to maintain coherence

**Update Plan:**
- Hand the affected-document list to `orgmodel-update` as `orgmodel-update-plan.md`
- Maintain consistency across main.md, process.md, and domain-model.md files
- Ensure terminology alignment across organizational documentation
- Preserve existing organizational workflows and approval processes

## Usage Patterns

### Integration Sequence

**Recommended Workflow:**
1. Complete requirements-ingest and basic analysis
2. Run domain-extractconcepts and domain-alignentities
3. Execute process-merge for process integration analysis
4. Apply process-findtopandupdate for hierarchy updates
5. Coordinate with orgmodel-update for organizational consistency

## Output Format

### Human-Readable Report (Markdown)

```markdown
# Top-Level Requirements Update Report

**Project**: PROJECT-001
**Generated**: 2026-02-19T10:30:00Z
**Analysis Sources**: domain-concepts, process-merge, w5h-analysis
**Requirements Updated**: 3 of 15 top-level requirements

## Executive Summary

Updated 3 strategic requirements based on domain analysis and process integration insights. Key changes include terminology alignment with identified domain entities and process refinement approach based on existing organizational capabilities.

## Updated Requirements

### REQ-TOP-001: Evolutionary Development Capability
**Previous**: Enable team to adapt development practices based on changing requirements
**Updated**: Implement skill-based evolutionary development framework that extends existing training processes to enable adaptive development practices

**Change Rationale**: Domain analysis identified 'Skill' as central entity; process integration revealed extension opportunity rather than replacement approach.

**Impact Assessment**:
- Scope: Expanded to include skill framework
- Complexity: Increased due to framework requirements
- Risk: Decreased through existing process extension
- Stakeholder Alignment: Improved through terminology consistency

## OrgModel Coordination

### Documents Requiring Updates
- `OrgDocument/orgModel/01-skill-development/main.md`: Strategic alignment updates
- `OrgDocument/orgModel/02-training/process.md`: Terminology consistency updates

### Cross-Document Consistency
- Skill terminology standardization across training and development processes
- Process extension approach alignment with existing organizational workflows

## Validation Results

### Hierarchical Consistency: ✅ PASSED
- All child requirements align with updated parent requirements
- No contradictory objectives identified
- Requirement decomposition remains complete

### Stakeholder Alignment: ✅ VALIDATED
- Updated requirements maintain stakeholder value propositions
- Strategic goals preserved with enhanced implementation approach
```

## Error Handling

**Common Issues:**
- **Circular Dependencies**: Detected through graph analysis with resolution suggestions
- **Inconsistent Updates**: Report the inconsistency and leave the proposal unaccepted until it is resolved
- **OrgModel Conflicts**: Coordination failure handling with manual resolution paths
- **Missing Context**: Graceful degradation with partial analysis completion

**Recovery Procedures:**
- Automatic validation checkpoint restoration
- Stakeholder notification for manual review requirements
- Partial update completion with clear status reporting
- Integration retry mechanisms for temporary failures

## Dependencies

**Required Prior Skills:**
- requirements-ingest: For normalized requirement input
- domain-extractconcepts: For domain entity identification
- process-merge: For process integration insights

**Coordination Skills:**
- orgmodel-update: For organizational document consistency
- change-management: For tracking requirement evolution

**Supporting Skills:**
- domain-alignentities: For terminology consistency
- goals-extract: For business alignment validation

## Completion Gate

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py process-findtopandupdate \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```
