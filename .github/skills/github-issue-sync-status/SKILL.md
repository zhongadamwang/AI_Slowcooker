---
name: github-issue-sync-status
description: Update local task files from the state of their linked GitHub Issues by running the bundled sync_status.py - marking tasks completed when their issue is closed and reopened when it is reopened, adding completion dates, keeping each file's own format, and stopping for review when local and GitHub status disagree. Use when the user asks to pull issue status into the project, after work was closed out on GitHub, or before reporting progress on a project whose tasks are tracked as GitHub Issues. Publishing tasks to GitHub is github-issue-create-update.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# GitHub Issue Sync Status

Bring issue state from GitHub back into the task files with the script in this folder. Only task files that already carry a `**GitHub Issue:** #N` line (written by `github-issue-create-update`) are synced.

## Inputs

- **Task files** in `OrgDocument/projects/[NN] - [Project Name]/tasks/`, in either format: the project task template (`**Status**: ...`) or the older GitHub-issue format (`**State:** ...`)
- **Credentials**: as for `github-issue-create-update` (`GITHUB_TOKEN` and `GITHUB_REPO`, or `github-credentials.json` in the repository root)

## Running it

From the repository root. Preview first:

```bash
python3 .github/skills/github-issue-sync-status/sync_status.py --project "OrgDocument/projects/[NN] - [Name]" --dry-run
python3 .github/skills/github-issue-sync-status/sync_status.py --project "OrgDocument/projects/[NN] - [Name]"
```

Other targets: `--file <task file>`, `--directory <tasks folder>`, `--issue <number>`. `--conflict-resolution manual|github_wins|local_wins` (default `manual`).

## What it does

| GitHub issue | Task file becomes |
|---|---|
| closed | Completed, with a completion date |
| open | Not Started (template format) or ready (GitHub-issue format) |

- Each file is written back in its own format: `**Status**: Completed` and `**Completed**: [date]` in the template format; `**State:** completed` and `**Completed Date:** [date]` in the older one. Nothing else in the file changes, apart from a `**Last Synced:**` line in files that have an `**Issue URL:**` line.
- **Conflicts**: an issue closed while the task is in progress, or reopened after the task was completed, is reported and left unchanged under `manual`. Put each conflict to the user; under `github_wins` or `local_wins` the stated side wins.

## After running

Report what changed, what was already in sync, and each conflict. If tasks changed status, update `tasks/task-tracking.md` through `project-planning-tracking` so the counts and table match.

Tests for the two task formats (offline): `python3 .github/skills/github-issue-sync-status/test_task_formats.py`.

Check:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py github-issue-sync-status \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration

**Upstream**: `github-issue-create-update` (links tasks to issues)

**Downstream**: `project-planning-tracking` (tracking document), `project-status-reporting`
