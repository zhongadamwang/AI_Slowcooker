# OrgModel Change Referencing Guidelines

## Purpose
This document provides guidelines for referencing changes in orgModel files to maintain traceability between process/domain models and requirement changes.

## When to Reference Changes
Reference changes in orgModel files when:
- **Process Changes**: Changes that modify organizational processes, workflows, or methodologies
- **Domain Model Updates**: Changes that affect entities, relationships, or domain concepts  
- **Capability Changes**: Changes that impact organizational skills, competencies, or capabilities
- **Structural Changes**: Changes that affect team organization, roles, or responsibilities

## Referencing Patterns

### In Main OrgModel Files
Add a "Related Changes" section at the end of the main.md file:

```markdown
## Related Changes
<!-- List changes that have impacted this organizational model -->
- [PROC-CHG-001](../../projects/01%20-%20Building%20Skills/artifacts/Changes/2026-02-08-PROC-CHG-001-description.md) - Process change description
- [REQ-CHG-002](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-REQ-CHG-002-description.md) - Requirement change description
```

### In Process Files (process.md)
Reference changes that modify process flows:

```markdown
## Process Evolution  
<!-- Document how this process has evolved through changes -->
### Recent Changes
- [PROC-CHG-001](../../projects/01%20-%20Building%20Skills/artifacts/Changes/2026-02-08-PROC-CHG-001-description.md) - Added change tracking workflow
- [PROC-CHG-002](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-PROC-CHG-002-description.md) - Modified approval workflow
```

### In Domain Model Files (domain-model.md)
Reference changes affecting entities, relationships, or concepts:

```markdown
## Model Evolution
<!-- Track changes that have affected the domain model -->
### Entity Changes
- [REQ-CHG-003](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-REQ-CHG-003-description.md) - Added new entity: ChangeRequest
- [REQ-CHG-004](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-REQ-CHG-004-description.md) - Modified entity relationships
```

### In Collaboration Files (collaboration.md)  
Reference changes affecting actor interactions and workflows:

```markdown
## Collaboration Evolution
<!-- Track changes in how actors interact within this model -->
### Workflow Changes
- [PROC-CHG-005](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-PROC-CHG-005-description.md) - Modified review workflow
- [PROC-CHG-006](../../projects/01%20-%20Building%20Skills/artifacts/Changes/YYYY-MM-DD-PROC-CHG-006-description.md) - Added stakeholder approval step
```

## Section Placement
- **Related Changes**: At end of document
- **Process Evolution**: In process.md after main process description  
- **Model Evolution**: In domain-model.md after main model description
- **Collaboration Evolution**: In collaboration.md after main collaboration description

## Relative Path Calculation
From orgModel files to Changes folder:
```
../../projects/{project-name}/artifacts/Changes/{change-file}.md
```

## Best Practices
1. **Keep Current**: Update references when new changes affect the orgModel
2. **Be Specific**: Describe how each change relates to the orgModel component
3. **Maintain Order**: List changes chronologically (newest first)  
4. **Use Consistent Format**: Follow the referencing patterns consistently
5. **Regular Reviews**: Periodically review and clean up change references

## Integration with Changes
When creating changes that affect orgModel components:
1. **Identify Impact**: Note which orgModel files will be affected
2. **Document in Change**: List affected orgModel files in the change document
3. **Update References**: Add change references to affected orgModel files after implementation