# Issue: T1 - GitHub Issue Create/Update Skill
**State:** ready  
**Labels:** feature, github-integration, mvp  
**Assignees:** adam.wang  
**Milestone:** MVP - GitHub Integration  
**Priority:** High
**Issue Number:** #T1
**Estimated Effort:** 1.5 days

## Description
Implement the github-issue-create-update skill that creates GitHub Issues from local task files and updates existing issues when local task files are modified. This skill enables one-way synchronization from local development tasks to GitHub project management.

## Acceptance Criteria
- [ ] Creates new GitHub Issues from local markdown task files
- [ ] Updates existing GitHub Issues when local task files are modified
- [ ] Extracts title, description, labels, and metadata from task file structure
- [ ] Maps local task metadata to appropriate GitHub Issue fields
- [ ] Handles task file creation, updates, and completion states
- [ ] Manual trigger execution (no automatic file watching)
- [ ] Returns issue URLs and operation status in skill output
- [ ] Integrates with GitHub REST API v3 using Personal Access Token
- [ ] Follows EDPS skills framework patterns and structure
- [ ] Compatible with VS Code and GitHub Copilot environment

## Tasks
- [ ] Design skill architecture following EDPS framework structure
- [ ] Implement GitHub API integration using REST API v3
- [ ] Create task file parsing logic to extract metadata and content
- [ ] Build GitHub Issue field mapping system (title, description, labels, etc.)
- [ ] Implement create vs. update logic based on existing issue tracking
- [ ] Add Personal Access Token authentication mechanism
- [ ] Create skill output formatting for issue URLs and status
- [ ] Test with existing task files from PRJ-01 Building Skills
- [ ] Document skill configuration and usage patterns
- [ ] Add basic error handling for API failures and rate limits

## Dependencies
- GitHub repository with Issues enabled
- Personal Access Token with appropriate permissions
- Existing task file format from PRJ-01 project
- Access to GitHub REST API v3

## Related Changes
<!-- Reference any relevant requirement changes that impact this task -->
- [REQ-001 to REQ-006](../artifacts/Requirements/initial-requirements.md) - Task-to-Issue skill functional requirements
- [REQ-022 to REQ-025](../artifacts/Requirements/initial-requirements.md) - EDPS skills framework integration requirements

## Technical Notes

### Skill Architecture
```
github-issue-create-update/
├── SKILL.md (skill definition and usage)
├── implementation/ (core skill logic)
├── templates/ (GitHub issue templates)
└── tests/ (validation test cases)
```

### Input Processing
- **Input**: Local task file path(s) or directory
- **Parsing**: Extract title, description, state, labels, priority from markdown
- **Metadata**: Map task metadata to GitHub Issue fields

### GitHub API Integration
- **Authentication**: Personal Access Token via environment variable
- **API Endpoints**: 
  - Create: POST /repos/{owner}/{repo}/issues
  - Update: PATCH /repos/{owner}/{repo}/issues/{issue_number}
- **Rate Limiting**: Basic handling with exponential backoff

### Issue Tracking
- **Issue ID Storage**: Store GitHub issue number in task file metadata
- **Create vs Update**: Check for existing issue ID to determine operation
- **Status Mapping**: Map task states to GitHub issue states

### Field Mapping
- **Title**: Extract from task file header
- **Body**: Use description + tasks + acceptance criteria
- **Labels**: Map from task labels and priority
- **State**: Map from task state (open/closed)

## Definition of Done
- [ ] Skill successfully creates GitHub Issues from task files
- [ ] Skill updates existing issues when task files change
- [ ] All field mappings work correctly (title, description, labels, state)
- [ ] Personal Access Token authentication works
- [ ] Basic error handling implemented for common failures
- [ ] Skill follows EDPS framework patterns and structure
- [ ] Documentation complete with usage examples
- [ ] Testing completed with PRJ-01 task files
- [ ] Integration verified in VS Code and Copilot environment
- [ ] Skill output format provides clear operation status and issue URLs