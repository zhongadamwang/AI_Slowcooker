# Change Management System - Quick Reference

## System Overview
The change management system preserves original requirements while tracking evolution through dedicated change documents with full traceability.

## Quick Workflow
1. **Identify Change** → Document in Changes folder
2. **Use Template** → Copy and customize `change-template.md`  
3. **Review & Approve** → Update status in change document
4. **Reference Changes** → Update tasks and orgModel files
5. **Track Implementation** → Monitor progress in related tasks

## File Naming
```
YYYY-MM-DD-{TYPE}-{ID}-{description}.md
```

**Types**: `REQ-CHG`, `REQ-ADD`, `REQ-REM`, `SCOPE-CHG`, `PROC-CHG`  
**IDs**: Sequential 3-digit numbers (`001`, `002`, etc.)

## Referencing Syntax

### In Task Files
```markdown
## Related Changes
- [PROC-CHG-001](../artifacts/Changes/2026-02-08-PROC-CHG-001-description.md) - Description
```

### In OrgModel Files  
```markdown
## Related Changes
- [PROC-CHG-001](../../projects/01%20-%20Building%20Skills/artifacts/Changes/2026-02-08-PROC-CHG-001-description.md) - Description
```

## Path Patterns
- **From Tasks to Changes**: `../artifacts/Changes/`
- **From OrgModel to Changes**: `../../projects/{project-name}/artifacts/Changes/`

## Key Files
- [`README.md`](README.md) - Complete system documentation
- [`change-template.md`](change-template.md) - Template for new changes
- [`orgmodel-referencing-guidelines.md`](orgmodel-referencing-guidelines.md) - OrgModel referencing patterns
- [`../../tasks/task-template.md`](../../tasks/task-template.md) - Updated task template with change referencing

## Status Values
- **Proposed** - Change identified, awaiting review
- **Under Review** - Stakeholder review in progress
- **Approved** - Ready for implementation  
- **Implemented** - Change fully completed
- **Rejected** - Change rejected with rationale

## Best Practices
✅ **Do:** Use AI chat to identify changes, then document formally  
✅ **Do:** Reference changes in affected tasks and models  
✅ **Do:** Keep original requirements intact as baseline  
✅ **Do:** Update change status as progress is made  

❌ **Don't:** Edit original requirement documents directly  
❌ **Don't:** Create changes for trivial formatting fixes  
❌ **Don't:** Skip the review process for significant changes  
❌ **Don't:** Forget to update referencing documents after implementation