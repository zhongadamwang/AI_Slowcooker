---
name: plan-buildschedule
description: Build a project schedule from the task breakdown and effort estimates - start and finish for every task, the critical path found by forward and backward pass, slack, resource allocation, milestones, and contingency - written as project-schedule.md/.json, critical-path-analysis.md, and milestone-plan.md. Use after plan-estimateeffort when the user asks when the project will finish, what the critical path is, how to fit a deadline or limited staff, or for a Gantt chart; and before project-planning-tracking, which builds the project plan from it.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-17"
---

# Plan Build Schedule

Compute when each task can happen given its dependencies, its estimate, and who is available to do it, and show which tasks decide the finish date.

## Inputs

From `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- **Required**: `task-breakdown.json` (from `plan-derivetasks`), `effort-estimates.json` (from `plan-estimateeffort`)
- **Optional**: team size and availability, a start date, deadlines and fixed milestones, working calendar

When the start date or staffing is not given, schedule in working days from day 0 with the staffing assumption stated, and mark the calendar as uncommitted. Do not invent dates.

## Outputs

- `project-schedule.json` — per task: start, finish, slack, assigned resource; plus project duration, critical path, resource allocation, milestones, and buffers
- `project-schedule.md` — schedule overview, Gantt chart, critical path, resource allocation, milestone schedule
- `critical-path-analysis.md` — the critical path, near-critical paths, and compression options
- `milestone-plan.md` — milestones with their criteria and target dates

The complete templates are in [references/output-format.md](references/output-format.md).

## Workflow

### 1. Build the network

Each task is a node with duration equal to its expected estimate (`E` from `effort-estimates.json`) and edges from `task-breakdown.json`'s dependencies. Stop and report if the graph has a cycle or a dependency on a task that does not exist.

### 2. Forward and backward pass

- **Forward**: Earliest Start (ES) = the maximum Earliest Finish of all predecessors (0 for tasks with none). Earliest Finish (EF) = ES + duration. Project duration = the largest EF.
- **Backward**: Latest Finish (LF) = the minimum Latest Start of all successors (project duration for tasks with none). Latest Start (LS) = LF − duration.
- **Slack** = LS − ES. Tasks with zero slack form the critical path. Tasks with small slack are near-critical; list them, since a modest slip makes them critical.

### 3. Fit to resources

With limited people, two tasks scheduled in parallel may need the same person. Delay the task with more slack until the resource is free, recompute, and repeat. Record each assignment. If no assignment fits the deadline, say so; do not overload anyone silently.

### 4. Add contingency and milestones

- Add a project buffer sized from the estimate uncertainty (the critical path's combined standard deviation from `effort-estimates.json`), and state how it was sized.
- Set milestones at phase ends and at points where stakeholders must review or decide. Each milestone has a checkable criterion.

### 5. Optimize only when asked or needed

If the schedule misses a required date, offer the options with their cost: run critical tasks in parallel (more coordination risk), add people to tasks that can absorb them, or reduce scope through `process-scopemin`. Present them; do not apply one without agreement.

### 6. Write and check

Render the Gantt chart as a Mermaid `gantt` block. Then check:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py plan-buildschedule \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- Every task is scheduled, with no task starting before its predecessors finish.
- The critical path's durations sum to the project duration.
- No person is assigned more than their availability.
- Every date follows from a stated start date, or the schedule is marked uncommitted.

## Integration

**Upstream**: `plan-derivetasks`, `plan-estimateeffort`

**Downstream**: `project-planning-tracking` (project plan and tracking), `project-status-reporting`
