---
name: github-issue-create-update
description: Create GitHub Issues from a project's local task files, or update the issues they already link to, by running the bundled create_update_issues.py - mapping title, description, status, priority, labels, and assignees, and writing the issue number and URL back into each task file. Use when the user wants project tasks published to GitHub, a task's issue refreshed after the task file changed, or a team given GitHub visibility of the plan. The reverse direction (issue state back into task files) is github-issue-sync-status.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# GitHub Issue Create/Update

Publish task files to GitHub Issues with the script in this folder. Run the script; do not call the GitHub API by hand or re-implement it.

## Inputs

- **Task files**: `OrgDocument/projects/[NN] - [Project Name]/tasks/T*.md`. Both formats are read:
  - the project task template (`**Status**: In Progress`, `**Priority**: P1-High`, `**Assigned**: name`), used by current projects
  - the older GitHub-issue format (`**State:** in-progress`, `**Labels:** a, b`, `**Assignees:** name`)
- **Credentials**: `GITHUB_TOKEN` and `GITHUB_REPO` (`owner/repo`) environment variables, or a `github-credentials.json` in the repository root (copy `github-credentials.json.template`; the real file is git-ignored). Never put a token in a task file, a command line that gets logged, or a commit.

## Running it

From the repository root:

```bash
# one task file
python3 .github/skills/github-issue-create-update/create_update_issues.py --file "OrgDocument/projects/[NN] - [Name]/tasks/T03-build-x.md"

# every task in a project
python3 .github/skills/github-issue-create-update/create_update_issues.py --project "OrgDocument/projects/[NN] - [Name]"
```

Options: `--directory <tasks folder>`, `--assignee <login>` to override the assignee, `--milestone <name>`. The script needs the `requests` package.

Creating issues is visible to everyone with access to the repository. Confirm the target repository and the set of tasks with the user before the first run against a project.

## What it does

| From the task file | To the issue |
|---|---|
| First `#` heading | Title |
| Body, minus the title and GitHub metadata lines | Description |
| `Status` / `State` | Open, or closed for Completed / Cancelled |
| `Priority` (`P0`/`P1` → high, `P2` → medium, `P3` → low, or High/Medium/Low) | `priority:` label |
| `Labels` | Labels, plus `auto-generated` |
| `Assignees` / `Assigned` (ignored when "Unassigned") | Assignees |

- A task file without a `**GitHub Issue:** #N` line gets a new issue; the script then writes `**GitHub Issue:** #N` and `**Issue URL:**` into the file.
- A task file with that line updates the existing issue instead of creating a duplicate.

## After running

Report, per task: created, updated, skipped, or failed, with the issue URL or the error. A failed task leaves its file unchanged; re-run it after fixing the cause (most often credentials or a label that cannot be created).

Check:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py github-issue-create-update \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration

**Upstream**: `plan-derivetasks` (task files), `project-planning-tracking` (status)

**Downstream**: `github-issue-sync-status` (pulls issue state back into the task files)
