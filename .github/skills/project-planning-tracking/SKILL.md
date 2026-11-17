---
name: project-planning-tracking
description: Assemble a project's plan (project-plan.md) from the task breakdown, effort estimates, and schedule produced by the plan-* skills, and keep the task tracking document (tasks/task-tracking.md) and each task file's status current as work proceeds - recording progress, completed and blocked tasks, and slips against the schedule. Use after plan-buildschedule to write or refresh the project plan, whenever a task starts, finishes, or is blocked, when the user asks where the project stands against its plan, or when a change means the plan must be revised.
license: MIT
metadata:
  version: 2.0.0
  last-updated: "2026-11-17"
---

# Project Planning and Tracking

Turn the planning outputs into one readable project plan, then keep the record of progress against it honest.

This skill does not estimate or schedule. Task breakdown is `plan-derivetasks`, effort estimation (including three-point/PERT estimates) is `plan-estimateeffort`, and the schedule and critical path are `plan-buildschedule`. When an estimate or the schedule needs to change, re-run that skill and then refresh the plan here.

## Inputs

From `OrgDocument/projects/[NN] - [Project Name]/`:

- `artifacts/Analysis/task-breakdown.json` and the task files in `tasks/` (from `plan-derivetasks`)
- `artifacts/Analysis/effort-estimates.json` (from `plan-estimateeffort`)
- `artifacts/Analysis/project-schedule.json`, `critical-path-analysis.md`, and `milestone-plan.md` (from `plan-buildschedule`)
- Optional: `goals.json`, `scope-analysis.json`, `w5h-analysis.json` for the plan's summary and phases
- For tracking: what the user reports about task progress

If the plan-* outputs do not exist, run those skills first; do not estimate or schedule here to fill the gap.

## Outputs

In the project root:

- `project-plan.md` — the plan
- `tasks/task-tracking.md` — the tracking document
- Updated `**Status**` and `**Last Updated**` fields in the task files under `tasks/`

### `project-plan.md`

```markdown
# Project Plan — [NN] - [Project Name]

**Project ID**: PRJ-[NN]
**Archetype**: [flat | standard | hierarchical]
**Project Created**: [date]
**Implementation Start**: [date, or "Uncommitted"]
**Target Completion**: [date or duration, as the schedule states it]
**Status**: [Planned | In Progress | Complete | On Hold]

## Executive Summary
[What the project delivers and why, from goals.json]

## Planning Artifacts
- [links to requirements, goals, task breakdown, estimates, schedule, critical path, milestones, task tracking]

## Project Phases
### Phase 1: [Name]
**Tasks**: T01, T02
**Expected effort**: [from effort-estimates.json]
**Deliverables**: [...]

## Milestones
| Milestone | Target | Depends On | Status |

## Schedule and Capacity
[Total expected effort, contingency, staffing and start-date assumptions, critical path summary — from project-schedule.json]

## Risk Management
[Highest risks and mitigations]

## Changelog
- [date]: [what changed in the plan and why]
```

Link to the detailed planning artifacts rather than copying them; the plan is the readable overview.

### `tasks/task-tracking.md`

```markdown
# Task Tracking - [Project Name]

**Project**: [NN] - [Project Name]
**Last Updated**: [date]
**Total Tasks**: [n]
**Completed**: [n]
**In Progress**: [n]
**Not Started**: [n]
**Blocked**: [n]

## Task List

| Task | Title | Phase | Priority | Status | Depends On |
|---|---|---|---|---|---|
| [T01](T01-[slug].md) | [Title] | [Phase] | P0 | ✅ Completed | None |

## Progress Against Schedule
[Critical path status (on track, behind, ahead), slips with their cause, forecast completion]

## Blockers
- [Task]: [what blocks it, and what would unblock it]
```

Status values: `⬜ Not Started`, `🔄 In Progress`, `⛔ Blocked`, `✅ Completed`.

### Task files

Task files use the project's `tasks/task-template.md` (created by `project-document-management`): a `# T## - [Title]` heading followed by `**Task ID**`, `**Phase**`, `**Priority**`, `**Estimated Effort**`, `**Status**`, `**Assigned**`, `**Created**`, and `**Last Updated**` fields, then Description, Detailed Requirements, Acceptance Criteria, and Dependencies sections. When tracking, change only the status, dates, and acceptance-criteria checkboxes; the content belongs to `plan-derivetasks`.

## Workflow

### 1. Write or refresh the plan

1. Read the plan-* outputs. Take phases, effort, the critical path, and milestones from them as they are.
2. Write `project-plan.md` per the template. State unconfirmed assumptions as unconfirmed: if staffing or the start date is not agreed, say "Uncommitted", not a guessed date.
3. Create `tasks/task-tracking.md` with every task from the breakdown at `⬜ Not Started`, or update it if it exists.
4. On a refresh, add a Changelog entry saying what changed and why.

### 2. Record progress

When the user reports progress on a task:

1. Update the task file's `**Status**` and `**Last Updated**`; on completion, add `**Completed**: [date]` and tick the acceptance criteria that are actually met.
2. Update the task's row and the counts in `task-tracking.md`, and its `**Last Updated**`.
3. Mark a task `⛔ Blocked` with the reason under `## Blockers` when it cannot proceed.

Mark a task completed only when its acceptance criteria are met. If some are not, the task is still in progress; say which criteria remain.

### 3. Compare progress with the schedule

Using `project-schedule.json` and `critical-path-analysis.md`:

- A slip on a critical-path task delays the project by the same amount unless something else is changed. Report it as such.
- A slip on a task with slack is absorbed until the slack runs out. Report the remaining slack.
- When the forecast completion moves materially, or a task is added or removed, re-run `plan-buildschedule` (and `plan-estimateeffort` for new tasks), then refresh the plan. Record a scope change through `change-management`.

Report the forecast as the schedule gives it; do not adjust it by judgement.

### 4. Check

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py project-planning-tracking \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- Every figure in the plan (effort, dates, critical path) comes from a plan-* output, and the plan links to it.
- Task counts in `task-tracking.md` match the task list, and each row matches its task file's status.
- No task is marked completed with unmet acceptance criteria.
- Unconfirmed dates and staffing are labelled as unconfirmed.

## Integration

**Upstream**: `plan-derivetasks`, `plan-estimateeffort`, `plan-buildschedule`, `project-document-management` (project folder and task template)

**Downstream**: `project-status-reporting` (reads the plan and tracking document), `github-issue-create-update` / `github-issue-sync-status` (task files to and from GitHub Issues), `change-management` (scope changes)
