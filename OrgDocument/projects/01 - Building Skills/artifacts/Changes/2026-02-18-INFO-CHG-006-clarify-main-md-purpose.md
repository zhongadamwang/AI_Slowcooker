# INFO-CHG-006: Clarify main.md Purpose in orgModel Folders

**Change ID**: INFO-CHG-006  
**Date Created**: 2026-02-18  
**Status**: Approved  
**Priority**: Medium  
**Requested By**: Project Requirements Review

## Summary
Clarify that main.md files in orgModel folders should contain business model descriptions and requirements overview for the current process level, rather than folder structure and file convention guidelines.

## Change Details

### Current State
Current instructions describe main.md as "Main documentation of each sub-folder or process. It should provide an overview of the folder's purpose and link to related documents or subfolders."

### Proposed State  
main.md should contain the description of the current model granular level - a summary of the business model that provides an overview and source of requirements for the current level of model, not folder structure and file convention guidelines.

### Rationale
The main.md file should focus on business content rather than documentation conventions. This creates clearer separation between:
- Business model content (main.md)
- Process workflows (process.md)
- Entity interactions (collaboration.md)
- Domain concepts (domain-model.md)

## Impact Analysis

### Affected Documents
- [x] [instructions.md](../../instructions.md) - Update main.md definition
- [x] [project-document-management SKILL.md](../../../../.github/skills/project-document-management/SKILL.md) - Update template guidance

### Affected Tasks  
- [x] [T17-orgmodel-update-skill.md](../../tasks/T17-orgmodel-update-skill.md) - Update skill requirements for main.md generation

### Risk Assessment
**Low Risk**: Clarification change that improves content focus without breaking existing structure.

## Implementation Plan
1. Update instructions.md definition of main.md
2. Update project-document-management skill template
3. Review existing main.md files for alignment
4. Update related skill documentation

## Acceptance Criteria
- [x] main.md definition clearly focuses on business model content
- [x] Distinction made between business content and structural documentation
- [x] Templates updated to reflect business model focus
- [x] Related skills documentation updated

## Implementation Status
**Completed**: 2026-02-18
- Updated instructions.md line 16 and summary section
- Updated project-document-management skill template for process main.md
- Files now clearly distinguish business model content from structural documentation