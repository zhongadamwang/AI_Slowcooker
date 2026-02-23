# Task Template

Use this template when creating new task files for the Integration with GitHub project.

## File Naming Convention
- Use format: `T##-task-name.md` 
- Example: `T01-requirements-gathering.md`
- Align numbering with project plan phases and timeline

## Task File Structure

```markdown
# Task T## - [Task Name]

## GitHub Issue Information
- **Title**: [Clear, descriptive title]
- **Labels**: `enhancement`, `integration`, `github-api` (use appropriate labels)
- **Priority**: High/Medium/Low
- **Estimated Effort**: [X] hours/days
- **Sprint/Milestone**: [Sprint name or milestone]

## Description

[Detailed description of the task, including context and background]

## Acceptance Criteria

- [ ] Criterion 1: [Specific, measurable outcome]
- [ ] Criterion 2: [Specific, measurable outcome]  
- [ ] Criterion 3: [Specific, measurable outcome]
- [ ] Documentation updated
- [ ] Tests added/updated (if applicable)
- [ ] Code review completed

## Task Breakdown

1. **Subtask 1**: [Description] - [Time estimate]
2. **Subtask 2**: [Description] - [Time estimate]
3. **Subtask 3**: [Description] - [Time estimate]

## Dependencies

- **Blocks**: [List of tasks this task blocks]
- **Blocked By**: [List of tasks blocking this task]
- **Related**: [Related tasks or issues]

## Technical Notes

[Any technical considerations, constraints, or implementation notes]

## Testing Strategy

[How this task will be tested and validated]

## Documentation Requirements

[What documentation needs to be created or updated]

## Definition of Done

- [ ] All acceptance criteria met
- [ ] Code reviewed and approved
- [ ] Tests pass
- [ ] Documentation complete
- [ ] Integration tested
- [ ] Stakeholder approval received
```

## Usage Notes

1. **Create task files** in the `tasks/` folder using this template
2. **Update project plan** to reference new tasks
3. **Import to GitHub** for team collaboration
4. **Track progress** by updating task status and checklist items
5. **Export from GitHub** to sync comments and updates back to local files

## Integration with GitHub Issues

- Task files can be imported directly to GitHub Issues
- Team collaboration happens through GitHub issue comments
- Status updates and progress tracking sync between local and GitHub
- Labels and metadata help with project organization and filtering