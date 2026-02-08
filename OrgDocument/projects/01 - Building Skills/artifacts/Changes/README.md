# Changes Management System

> **Quick Start**: See [quick-reference.md](quick-reference.md) for a condensed overview

## Overview
This folder contains all documented change requests to project requirements and specifications. Rather than directly editing original requirement documents, changes are tracked here to maintain auditability and traceability.

## Purpose
- **Preserve Original Requirements**: Keep the original requirement documents intact as source of truth
- **Track Evolution**: Document how requirements evolve over time
- **Maintain Traceability**: Link changes to impacted tasks and orgModel files
- **Support Reviews**: Enable proper review workflow for requirement changes

## Change Types
1. **Requirement Modifications** (`REQ-CHG-###`) - Changes to existing requirements
2. **Requirement Additions** (`REQ-ADD-###`) - New requirements added
3. **Requirement Removals** (`REQ-REM-###`) - Requirements marked obsolete
4. **Scope Changes** (`SCOPE-CHG-###`) - Project scope adjustments
5. **Process Changes** (`PROC-CHG-###`) - Development process modifications

## Naming Convention
- **Change Files**: `YYYY-MM-DD-{TYPE}-{ID}-{short-description}.md`
- **Change IDs**: `{TYPE}-{3-digit-sequential-number}`
- **Examples**:
  - `2026-02-08-REQ-CHG-001-add-authentication-requirements.md`
  - `2026-02-08-SCOPE-CHG-002-expand-mvp-scope.md`

## Usage Workflow
1. **Identify Change Need**: During AI chat sessions or reviews, identify requirement changes
2. **Create Change Document**: Use the change template to document the change request
3. **Review and Approve**: Stakeholder review of the proposed change
4. **Update References**: Update tasks, orgModel files with change references
5. **Implementation Tracking**: Track implementation status in relevant task files

## File Structure
```
Changes/
├── README.md (this file)
├── quick-reference.md
├── change-template.md
├── orgmodel-referencing-guidelines.md
├── 2026-02-08-PROC-CHG-001-implement-change-management-system.md
├── 2026-02-08-SCOPE-CHG-002-add-change-management-skill.md
└── ...
```

## Referencing Changes
In task files and orgModel documents, reference changes using:
```markdown
### Related Changes
- [REQ-CHG-001](../artifacts/Changes/2026-02-08-REQ-CHG-001-description.md) - Description
- [SCOPE-CHG-002](../artifacts/Changes/2026-02-08-SCOPE-CHG-002-description.md) - Description
```

## Status Tracking
Each change document tracks:
- **Proposed**: Change identified and documented
- **Under Review**: Stakeholder review in progress  
- **Approved**: Change approved for implementation
- **Implemented**: Change fully implemented and tested
- **Rejected**: Change rejected with rationale

## Integration Points
- **Task Files**: Reference relevant changes in task dependencies/context
- **OrgModel Files**: Link changes that impact process or domain models
- **Requirements**: Original requirements remain unchanged; changes provide delta
- **Project Plans**: Major changes may trigger project plan updates