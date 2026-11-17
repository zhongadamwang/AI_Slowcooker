# Effort Estimates — Output Format

The complete templates for this skill's outputs. Values shown are illustrative.

### JSON Structure (`effort-estimates.json`)
```json
{
  "project_id": "string",
  "generated_at": "ISO_timestamp",
  "estimation_methods": ["PERT", "complexity-points", "analogies"],
  "total_project_estimate": {
    "optimistic_days": 0.0,
    "most_likely_days": 0.0,
    "pessimistic_days": 0.0,
    "expected_days": 0.0,
    "standard_deviation": 0.0,
    "confidence_interval_80": {"min": 0.0, "max": 0.0},
    "confidence_interval_95": {"min": 0.0, "max": 0.0}
  },
  "estimation_factors": {
    "team_experience": "novice|intermediate|expert",
    "technology_familiarity": "new|familiar|expert", 
    "project_complexity": "simple|moderate|complex|very_complex",
    "requirements_clarity": "clear|moderate|unclear",
    "integration_complexity": "simple|moderate|complex"
  },
  "task_estimates": [
    {
      "task_id": "string",
      "title": "string",
      "category": "string",
      "pert_estimate": {
        "optimistic_days": 0.0,
        "most_likely_days": 0.0,
        "pessimistic_days": 0.0,
        "expected_days": 0.0,
        "variance": 0.0
      },
      "complexity_factors": {
        "technical_complexity": "1-5_scale",
        "business_logic_complexity": "1-5_scale",
        "integration_complexity": "1-5_scale",
        "uncertainty_factor": "1-5_scale",
        "total_story_points": 0
      },
      "risk_factors": [
        {
          "risk": "string",
          "impact": "low|medium|high",
          "probability": "low|medium|high",
          "effort_multiplier": 0.0
        }
      ],
      "historical_analogies": [
        {
          "similar_task": "string",
          "similarity_score": "0.0-1.0",
          "actual_effort": 0.0,
          "adjusted_estimate": 0.0
        }
      ],
      "confidence_level": "0-100_percent",
      "rationale": "string",
      "estimation_notes": ["string_list"]
    }
  ],
  "summary_statistics": {
    "total_tasks": 0,
    "tasks_by_category": {
      "development": {"count": 0, "total_effort": 0.0},
      "testing": {"count": 0, "total_effort": 0.0},
      "design": {"count": 0, "total_effort": 0.0},
      "documentation": {"count": 0, "total_effort": 0.0}
    },
    "critical_path_effort": 0.0,
    "parallel_work_potential": 0.0
  }
}
```

### Markdown Structure (`effort-estimates.md`)
```markdown
# Project Effort Estimates

## Executive Summary
- **Total Expected Effort**: [expected_days] days
- **Confidence Range (80%)**: [min_days] - [max_days] days  
- **Critical Path**: [critical_path_days] days
- **Estimation Approach**: PERT + Complexity + Risk Analysis

## Estimation Context
- **Team Experience**: [experience_level]
- **Technology Stack**: [familiarity_level]
- **Project Complexity**: [complexity_level]
- **Requirements Certainty**: [clarity_level]

## Task Estimates Detail
[Individual task breakdown with rationale]

## Risk Factors & Mitigation
[Risk analysis affecting estimates]

## Estimation Methodology
[Documentation of estimation approach]

## Confidence Analysis
[Discussion of estimate reliability]
```
