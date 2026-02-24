# Issue: T2 - GitHub Issue Sync Status Skill
**State:** ready  
**Labels:** feature, github-integration, mvp  
**Assignees:** adam.wang  
**Milestone:** MVP - GitHub Integration  
**Priority:** High
**Issue Number:** #T2
**Estimated Effort:** 1.5 days

## Description
Implement the github-issue-sync-status skill that updates local task status based on GitHub Issue state changes. This skill enables one-way synchronization from GitHub project management back to local development tasks, preserving local file format and metadata.

## Acceptance Criteria
- [ ] Updates local task status from GitHub Issue state (open, closed, etc.)
- [ ] Syncs issue state changes to corresponding local task files
- [ ] Preserves local task file format and existing metadata
- [ ] Updates task completion status based on issue state
- [ ] Manual trigger execution (no automatic webhook integration)
- [ ] Handles multiple task files in batch operations
- [ ] Returns sync status and updated file list in skill output
- [ ] Integrates with GitHub REST API v3 using Personal Access Token
- [ ] Follows EDPS skills framework patterns and structure
- [ ] Compatible with VS Code and GitHub Copilot environment

## Tasks
- [ ] Design skill architecture following EDPS framework structure
- [ ] Implement GitHub API integration for reading issue states
- [ ] Create issue-to-task mapping logic using stored issue IDs
- [ ] Build local task file update mechanism preserving format
- [ ] Implement status synchronization logic (issue state → task state)
- [ ] Add batch processing for multiple tasks/issues
- [ ] Create skill input processing for issue URLs or repository scanning
- [ ] Implement Personal Access Token authentication mechanism
- [ ] Create skill output formatting for sync status and file changes
- [ ] Test with task files containing GitHub issue references
- [ ] Document skill configuration and usage patterns
- [ ] Add error handling for missing files and API failures

## Dependencies
- T1-github-issue-create-update-skill (provides issue ID tracking)
- GitHub repository with Issues enabled
- Personal Access Token with read permissions
- Local task files with GitHub issue ID metadata
- Access to GitHub REST API v3

## Related Changes
<!-- Reference any relevant requirement changes that impact this task -->
- [REQ-007 to REQ-011](../artifacts/Requirements/initial-requirements.md) - Issue-to-Task skill functional requirements
- [REQ-022 to REQ-025](../artifacts/Requirements/initial-requirements.md) - EDPS skills framework integration requirements

## Technical Notes

### Skill Architecture
```
github-issue-sync-status/
├── SKILL.md (skill definition and usage)
├── implementation/ (core skill logic)
├── mappings/ (state mapping configurations)
└── tests/ (validation test cases)
```

### Input Processing
- **Input Options**:
  - Specific GitHub issue URL(s)
  - Repository scan for all tracked issues
  - Local task directory scan
- **Issue Discovery**: Find issues linked to local task files

### GitHub API Integration
- **Authentication**: Personal Access Token via environment variable
- **API Endpoints**: 
  - Get issue: GET /repos/{owner}/{repo}/issues/{issue_number}
  - List issues: GET /repos/{owner}/{repo}/issues
- **Rate Limiting**: Basic handling with exponential backoff

### Task File Updates
- **Issue ID Lookup**: Find local tasks with stored GitHub issue IDs
- **Selective Updates**: Only update status-related fields
- **Format Preservation**: Maintain all existing task file structure
- **Backup**: Optional backup before modifications

### State Mapping
- **Issue State → Task State**:
  - `open` → `in-progress` or `ready`
  - `closed` → `completed`
- **Status Field Updates**: Update state, completion checkboxes
- **Metadata Preservation**: Keep all other task metadata intact

### Batch Processing
- **Multiple Issues**: Process several issues in single execution
- **Progress Tracking**: Report progress for large batch operations
- **Error Recovery**: Continue processing if individual files fail

## Definition of Done
- [ ] Skill successfully syncs GitHub issue states to local task files
- [ ] Local task file format and metadata preserved during updates
- [ ] State mapping works correctly (open/closed → task states)
- [ ] Personal Access Token authentication works
- [ ] Batch processing handles multiple tasks efficiently
- [ ] Error handling implemented for missing files and API failures
- [ ] Skill follows EDPS framework patterns and structure
- [ ] Documentation complete with usage examples
- [ ] Testing completed with existing GitHub issues
- [ ] Integration verified in VS Code and Copilot environment
- [ ] Skill output provides clear sync status and file change summary