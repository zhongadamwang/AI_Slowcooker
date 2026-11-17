---
name: plan-derivetasks
description: Break a project's requirements and goals into actionable tasks - grouped into phases, each with a description, category, priority, testable acceptance criteria, dependencies, and the requirement IDs it covers - written as task-breakdown.md and task-breakdown.json plus one task file per task in tasks/. Use after requirements-ingest and goals-extract (and process-scopemin, when an MVP was defined) when the user asks for a work breakdown, a task list, or a plan of work; and before plan-estimateeffort, which estimates these tasks.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# Plan Derive Tasks

Turn what the project must achieve into the work that achieves it: tasks small enough to estimate and finish, each traceable to the requirements it satisfies.

## Inputs

From `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- **Required**: `requirements.json` (from `requirements-ingest`), `goals.json` (from `goals-extract`)
- **Recommended**: `scope-analysis.json` (from `process-scopemin`). When it exists, derive tasks for the MVP scope it defines and list deferred features separately; do not plan work the scope decision excluded
- **Optional**: `w5h-analysis.json` (context and constraints)

## Outputs

- `artifacts/Analysis/task-breakdown.json` — phases, tasks, dependencies, critical path, parallel tracks
- `artifacts/Analysis/task-breakdown.md` — the same, readable: `## Project Overview`, `## Phase Breakdown`, `## Dependency Analysis`, `## Risk Assessment`
- `tasks/T##-[slug].md` — one file per task

Each task in the JSON carries `task_id` (`T01`), `title`, `description`, `category`, `phase`, `priority`, `acceptance_criteria` (each `criterion`, `testable`, `definition_of_done`), `dependencies` (`depends_on`, `dependency_type`), `source_requirements`, `source_goals`, `deliverables`, and `risk_factors`. The complete templates are in [references/output-format.md](references/output-format.md).

Task files follow the project's `tasks/task-template.md` (created by `project-document-management`): a `# T## - [Title]` heading, then `**Task ID**`, `**Phase**`, `**Priority**`, `**Estimated Effort**`, `**Status**: Not Started`, `**Assigned**`, `**Created**`, `**Last Updated**`, and sections for Description, Detailed Requirements (citing requirement IDs), Acceptance Criteria, and Dependencies. Leave `**Estimated Effort**` as `TBD` until `plan-estimateeffort` fills it.

## Workflow

### 1. Group requirements into deliverable work

Group requirements that are built and verified together (one feature, one integration, one data concern) and derive tasks from each group. Use whichever decomposition fits the project: by function (data, logic, interface), by feature, or by the structure of the existing system. Add the enabling work the requirements imply but do not state: setup, integration, test, documentation, deployment.

### 2. Size each task

A task should be completable by one person in roughly half a day to ten days. Split larger ones; merge trivial ones into their neighbour. Each task produces something checkable.

### 3. Write acceptance criteria

Each criterion is testable: someone could check it and agree whether it holds. Prefer observable outcomes ("Given an expired session, when the user submits, then they are returned to sign-in") over activity ("Implement session handling"). Carry measurable targets from the requirements and goals; do not invent new ones. Add the non-functional criteria the source requirements call for.

### 4. Categorize and prioritize

| Category | For |
|---|---|
| `development` | Implementing functional behaviour |
| `design` | User experience and system design |
| `testing` | Verification and validation |
| `documentation` | Guides and technical documentation |
| `integration` | Connecting systems, data migration |
| `deployment` | Release and environment setup |
| `research` | Spikes and evaluations that resolve an unknown |

Priority follows the scope decision and the requirements: work on the critical MVP path is `P0`, down to `P3` for optional work.

### 5. Map dependencies

Record which tasks must finish before others can start, and why (data, technical, or decision dependency). The graph must be acyclic. Identify the longest chain of dependent tasks as a provisional critical path, and the tracks that can run in parallel; `plan-buildschedule` computes the real critical path once estimates exist.

### 6. Check coverage, then write

Every in-scope requirement is covered by at least one task's `source_requirements`; list any that are not, with the reason. Then write the breakdown files and one task file per task, and check:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py plan-derivetasks \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

Do not estimate effort here; that is `plan-estimateeffort`.

## Quality checks

- Every in-scope requirement maps to a task, and every task cites the requirements it serves.
- Every acceptance criterion is testable.
- The dependency graph has no cycles, and no task depends on one in a later phase.
- Task files and `task-breakdown.json` agree.

## Integration

**Upstream**: `requirements-ingest`, `goals-extract`, `process-scopemin`, `process-w5h`, `project-document-management` (task template)

**Downstream**: `plan-estimateeffort`, `plan-buildschedule`, `project-planning-tracking`, `github-issue-create-update`
