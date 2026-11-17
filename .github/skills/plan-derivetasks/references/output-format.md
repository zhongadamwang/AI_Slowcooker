# Task Breakdown — Output Format

The complete templates for this skill's outputs. Values shown are illustrative.

### JSON Structure (`task-breakdown.json`)
```json
{
  "project_id": "string",
  "generated_at": "ISO_timestamp",
  "total_tasks": 0,
  "task_categories": [
    "development",
    "design", 
    "testing",
    "documentation",
    "integration",
    "deployment",
    "research"
  ],
  "phases": [
    {
      "phase_id": "string",
      "phase_name": "string", 
      "description": "string",
      "tasks": ["task_id_list"],
      "dependencies": ["phase_id_list"],
      "estimated_duration": "string"
    }
  ],
  "tasks": [
    {
      "task_id": "string",
      "title": "string",
      "description": "string",
      "category": "string",
      "phase": "string",
      "priority": "high|medium|low",
      "estimated_effort": "float (days)",
      "acceptance_criteria": [
        {
          "criterion": "string",
          "testable": true,
          "definition_of_done": "string"
        }
      ],
      "dependencies": [
        {
          "depends_on": "task_id",
          "dependency_type": "prerequisite|blocked_by|related"
        }
      ],
      "source_requirements": ["req_id_list"],
      "source_goals": ["goal_criteria_list"],
      "deliverables": ["string_list"],
      "risk_factors": [
        {
          "risk": "string",
          "mitigation": "string"
        }
      ]
    }
  ],
  "dependency_graph": {
    "critical_path": ["task_id_list"],
    "parallel_tracks": [
      {
        "track_name": "string",
        "tasks": ["task_id_list"]
      }
    ]
  }
}
```

### Markdown Structure (`task-breakdown.md`)
```markdown
# Task Breakdown Structure

## Project Overview
- **Project**: [project_name]
- **Total Tasks**: [count]
- **Estimated Timeline**: [duration]
- **Critical Path Length**: [duration]

## Phase Breakdown

### Phase 1: [Phase Name]
**Description**: [phase description]
**Dependencies**: [list]
**Duration**: [estimate]

#### Tasks
- **T001** - [Task Title] (*category*, *priority*, *effort*)
  - **Description**: [description]
  - **Acceptance Criteria**:
    - [ ] [criterion 1]
    - [ ] [criterion 2]
  - **Dependencies**: [list]
  - **Deliverables**: [list]

## Dependency Analysis

### Critical Path
[ordered list of critical path tasks]

### Parallel Execution Opportunities
- **Track 1**: [parallel tasks]
- **Track 2**: [parallel tasks]

## Risk Assessment
[identified risks and mitigations]
```
