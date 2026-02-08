# Tasks Folder

This folder contains individual task files formatted as GitHub issues to enable seamless integration with GitHub's issue tracking system.

## Workflow

### Creating Tasks
1. Create new task files using the naming convention: `task-###-brief-description.md`
2. Use the GitHub issue format with all required fields
3. Include clear acceptance criteria and task breakdowns
4. Reference dependencies using issue numbers

### GitHub Integration
1. **Import to GitHub**: Task files can be bulk imported to GitHub Issues
2. **Team Collaboration**: Team members add feedback as issue comments in GitHub
3. **Export from GitHub**: Updated issues with comments can be exported back to update project documents
4. **Sync Process**: Regular sync between local task files and GitHub issues maintains consistency

## File Format
Each task file follows this structure:
- **Header**: Issue title, state, labels, assignees, milestone, priority, issue number
- **Description**: Clear problem statement and context
- **Acceptance Criteria**: Measurable completion criteria
- **Tasks**: Detailed task breakdown with checkboxes
- **Dependencies**: References to other tasks/issues
- **Comments**: Section for GitHub issue comments (populated on export)

## Task Status Management
- **open**: Task is active and being worked on
- **in-progress**: Task is currently being developed
- **review**: Task is complete and under review
- **closed**: Task is completed and verified

## Numbering Convention
Tasks are numbered sequentially starting from #001. Higher-priority or foundational tasks should receive lower numbers.

## Integration with Project Structure
Tasks reference and are referenced by:
- Project requirements (`artifacts/Requirements/`)
- Analysis documents (`artifacts/Analysis/`)
- Project planning documents
- Organizational models (`../../orgModel/`)