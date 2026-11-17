# Project Schedule — Output Format

The complete templates for this skill's outputs. Values shown are illustrative.

### JSON Structure (`project-schedule.json`)
```json
{
  "project_id": "string",
  "generated_at": "ISO_timestamp",
  "schedule_version": "string",
  "project_duration": {
    "start_date": "ISO_date",
    "end_date": "ISO_date",
    "total_duration_days": 0.0,
    "working_days": 0.0,
    "buffer_days": 0.0
  },
  "critical_path": {
    "duration_days": 0.0,
    "tasks": ["task_id_list"],
    "slack_analysis": {
      "total_slack": 0.0,
      "free_slack": 0.0,
      "critical_tasks": ["task_id_list"]
    }
  },
  "resource_allocation": {
    "total_effort_days": 0.0,
    "peak_resource_demand": 0.0,
    "resource_leveling_applied": true,
    "team_assignments": [
      {
        "resource_id": "string",
        "resource_type": "developer|designer|tester|analyst",
        "allocation_percentage": 0.0,
        "assigned_tasks": ["task_id_list"],
        "workload_distribution": {
          "peak_utilization": 0.0,
          "average_utilization": 0.0,
          "utilization_by_week": [0.0]
        }
      }
    ]
  },
  "milestones": [
    {
      "milestone_id": "string",
      "name": "string",
      "description": "string",
      "target_date": "ISO_date",
      "milestone_type": "phase_completion|delivery|review|approval",
      "dependencies": ["milestone_id_list"],
      "deliverables": ["string_list"],
      "success_criteria": ["string_list"],
      "stakeholders": ["string_list"],
      "risk_assessment": {
        "probability_on_time": 0.0,
        "risk_factors": ["string_list"],
        "mitigation_strategies": ["string_list"]
      }
    }
  ],
  "schedule_tasks": [
    {
      "task_id": "string",
      "title": "string",
      "scheduled_start": "ISO_date",
      "scheduled_end": "ISO_date",
      "duration_days": 0.0,
      "actual_effort_days": 0.0,
      "dependencies": [
        {
          "predecessor_id": "string",
          "dependency_type": "finish_to_start|start_to_start|finish_to_finish|start_to_finish",
          "lag_days": 0.0
        }
      ],
      "resource_assignments": [
        {
          "resource_id": "string",
          "allocation_percentage": 0.0,
          "scheduled_effort_days": 0.0
        }
      ],
      "schedule_flexibility": {
        "early_start": "ISO_date",
        "early_finish": "ISO_date",
        "late_start": "ISO_date",
        "late_finish": "ISO_date",
        "total_slack_days": 0.0,
        "free_slack_days": 0.0,
        "is_critical": true
      },
      "milestone_deliverable": "milestone_id_or_null"
    }
  ],
  "schedule_optimization": {
    "optimization_applied": ["resource_leveling", "fast_tracking", "crashing"],
    "baseline_duration": 0.0,
    "optimized_duration": 0.0,
    "time_savings": 0.0,
    "cost_impact": "string",
    "risk_impact": "string"
  },
  "what_if_scenarios": [
    {
      "scenario_name": "string",
      "scenario_type": "best_case|worst_case|resource_constrained|accelerated",
      "assumptions": ["string_list"],
      "duration_impact": 0.0,
      "resource_impact": 0.0,
      "risk_assessment": "string"
    }
  ]
}
```

### Markdown Structure (`project-schedule.md`)
```markdown
# Project Schedule

## Schedule Overview
- **Project**: [project_name]
- **Duration**: [total_days] days ([start_date] to [end_date])
- **Critical Path Length**: [critical_path_days] days
- **Total Effort**: [total_effort] person-days
- **Schedule Buffer**: [buffer_percentage]%

## Gantt Chart (Text Representation)

```
Task                    | Start     | End       | Duration |████████████████████████████
T001 - Setup Auth       | 2026-02-21| 2026-02-23|  2.0d    |██████░░░░░░░░░░░░░░░░░░░░░░
T002 - User Registration| 2026-02-24| 2026-02-25|  1.5d    |      ████░░░░░░░░░░░░░░░░░░
T003 - Profile UI       | 2026-02-21| 2026-02-21|  1.0d    |██░░░░░░░░░░░░░░░░░░░░░░░░░░
T004 - Profile API      | 2026-02-26| 2026-02-27|  1.5d    |          ████░░░░░░░░░░░░░░
T005 - Data Viz         | 2026-02-21| 2026-02-25|  3.0d    |████████████░░░░░░░░░░░░░░
T006 - Integration Test | 2026-02-28| 2026-03-02|  2.0d    |              ██████░░░░░░
```

## Critical Path Analysis

### Critical Tasks
[List of critical path tasks with zero slack]

### Schedule Risks
[Identified scheduling risks and mitigation strategies]

### Optimization Opportunities
[Potential schedule improvements and trade-offs]

## Resource Allocation

### Team Assignments
[Resource allocation by person/role with utilization levels]

### Workload Distribution
[Peak utilization periods and resource leveling recommendations]

## Milestone Schedule

### Major Deliverables
[Timeline of key milestones and delivery checkpoints]

### Stakeholder Reviews
[Scheduled review points and approval gates]
```
