# Issue: T1 - GitHub Issue Create/Update Skill
**State:** completed  
**Labels:** feature, github-integration, mvp  
**Assignees:** adam.wang  
**Milestone:** MVP - GitHub Integration  
**Priority:** High
**Issue Number:** #T1
**Estimated Effort:** 1.5 days
**Actual Effort:** 1.5 days
**Completed Date:** 2026-02-24
**GitHub Issue:** #2
**Issue URL:** https://github.com/zhongadamwang/AI_Slowcooker/issues/2
**Sync Status:** ✅ Synced to GitHub (closed)

## Description
Implement the github-issue-create-update skill that creates GitHub Issues from local task files and updates existing issues when local task files are modified. This skill enables one-way synchronization from local development tasks to GitHub project management.

## Acceptance Criteria
- [x] Creates new GitHub Issues from local markdown task files
- [x] Updates existing GitHub Issues when local task files are modified
- [x] Extracts title, description, labels, and metadata from task file structure
- [x] Maps local task metadata to appropriate GitHub Issue fields
- [x] Handles task file creation, updates, and completion states
- [x] Manual trigger execution (no automatic file watching)
- [x] Returns issue URLs and operation status in skill output
- [x] Integrates with GitHub REST API v3 using Personal Access Token
- [x] Follows EDPS skills framework patterns and structure
- [x] Compatible with VS Code and GitHub Copilot environment

## Tasks
- [x] Design skill architecture following EDPS framework structure
- [x] Implement GitHub API integration using REST API v3
- [x] Create task file parsing logic to extract metadata and content
- [x] Build GitHub Issue field mapping system (title, description, labels, etc.)
- [x] Implement create vs. update logic based on existing issue tracking
- [x] Add Personal Access Token authentication mechanism
- [x] Create skill output formatting for issue URLs and status
- [x] Test with existing task files from PRJ-01 Building Skills
- [x] Document skill configuration and usage patterns
- [x] Add basic error handling for API failures and rate limits

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
- [x] Skill successfully creates GitHub Issues from task files
- [x] Skill updates existing issues when task files change
- [x] All field mappings work correctly (title, description, labels, state)
- [x] Personal Access Token authentication works
- [x] Basic error handling implemented for common failures
- [x] Skill follows EDPS framework patterns and structure
- [x] Documentation complete with usage examples
- [x] Testing completed with PRJ-01 task files
- [x] Integration verified in VS Code and Copilot environment
- [x] Skill output format provides clear operation status and issue URLs

## Implementation Summary
Successfully implemented the GitHub Issue Create/Update skill at [.github/skills/github-issue-create-update/SKILL.md](.github/skills/github-issue-create-update/SKILL.md). The skill provides:

- **Task File Parsing**: Extracts title, state, labels, assignees, and priority from markdown task files
- **GitHub API Integration**: Complete REST API v3 integration with authentication and error handling
- **Field Mapping**: Comprehensive mapping between local task metadata and GitHub issue fields
- **Issue Tracking**: Create vs update logic with metadata storage in task files
- **Batch Operations**: Support for single files and project directory processing
- **Error Handling**: Robust retry logic, rate limiting, and graceful failure modes
- **Integration Ready**: Compatible with VS Code and GitHub Copilot workflows

The skill follows EDPS framework patterns with progressive disclosure design, comprehensive documentation, and clear usage examples.