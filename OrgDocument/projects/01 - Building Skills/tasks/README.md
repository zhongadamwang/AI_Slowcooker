# Tasks Folder

This folder contains individual task files formatted as GitHub issues to enable seamless integration with GitHub's issue tracking system.

## Workflow

### Creating Tasks
1. Create new task files using the naming convention: `T##-skill-name.md` (aligned with project plan)
2. Use the GitHub issue format with all required fields
3. Include clear acceptance criteria and task breakdowns
4. Reference dependencies using T## task numbers from project plan

### GitHub Integration
1. **Import to GitHub**: Task files can be bulk imported to GitHub Issues
2. **Team Collaboration**: Team members add feedback as issue comments in GitHub
3. **Export from GitHub**: Updated issues with comments can be exported back to update project documents
4. **Sync Process**: Regular sync between local task files and GitHub issues maintains consistency

## Task Overview

### Phase 1: Foundation & Core Skills
- **T1**: Skill Framework Setup (1.1 days) - Foundation for all skills
- **T2**: Requirements.Ingest Skill (2.0 days) - Process markdown requirements
- **T3**: Goals.Extract Skill (1.1 days) - Extract business goals and success criteria  
- **T4**: Process.W5H Skill (1.1 days) - Who, What, When, Where, Why, How analysis

### Phase 2: Domain & Process Skills  
- **T5**: Domain.ExtractConcepts Skill (2.0 days) - Extract domain entities and concepts
- **T6**: Domain.AlignEntities Skill (2.2 days) - Align concepts with existing models
- **T7**: Domain.ProposeNewConcepts Skill (1.1 days) - Suggest new domain concepts
- **T8**: Diagram.GenerateCollaboration Skill (2.0 days) - Create Mermaid diagrams
- **T9**: Process.ScopeMin Skill (1.1 days) - Identify MVP scope
- **T10**: Process.Merge Skill (2.2 days) - Merge multiple requirement sources
- **T11**: Process.FindTopAndUpdate Skill (1.1 days) - Update top-level requirements

### Phase 3: Planning & Integration  
- **T12**: Plan.DeriveTasks Skill (2.0 days) - Convert requirements to actionable tasks
- **T13**: Plan.EstimateEffort Skill (1.1 days) - Multi-method effort estimation
- **T14**: Plan.BuildSchedule Skill (2.0 days) - Generate project schedule with critical path
- **T15**: Integration & Testing (3.2 days) - End-to-end integration and VS Code testing

**Total Estimated Effort**: 24.3 days (~5 weeks)

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
Tasks follow the project plan's T1-T15 structure corresponding to the PERT analysis:
- **T1-T4**: Phase 1 - Foundation & Core Skills  
- **T5-T11**: Phase 2 - Domain & Process Skills
- **T12-T15**: Phase 3 - Planning & Integration

Task numbering aligns directly with project plan dependencies and critical path analysis.

## Integration with Project Structure
Tasks reference and are referenced by:
- Project requirements (`artifacts/Requirements/`)
- Analysis documents (`artifacts/Analysis/`)
- Project planning documents
- Organizational models (`../../orgModel/`)