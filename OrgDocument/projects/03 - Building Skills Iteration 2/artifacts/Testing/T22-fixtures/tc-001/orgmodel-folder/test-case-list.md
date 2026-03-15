<!-- Identifier: TCL-01-01 -->

# Skill Pipeline Execution — Test Case List

## Test Coverage Overview

Test cases derived from `domain-concepts.json` entities: `SkillExecutionContext` and `PipelineStageResult`. Updated by `orgmodel-update` (guard-exempt path — vocabulary and test cases always updated).

## Test Cases

| TC ID | Test Category | Title | Priority | Source Requirement |
|-------|---------------|-------|----------|--------------------|
| tc-spe-ctx-001 | Functional | SkillExecutionContext carries correct user_id on invocation | High | R-42 |
| tc-spe-ctx-002 | Functional | SkillExecutionContext captures environment enum (dev/prod) correctly | Medium | R-42 |
| tc-spe-ctx-003 | Integration | SkillExecutionContext associated with SkillOutputEntity post-pipeline | High | R-42 |
| tc-spe-result-001 | Functional | PipelineStageResult records stage_name and status on completion | High | R-43 |
| tc-spe-result-002 | Functional | PipelineStageResult status = fail when stage throws exception | High | R-43 |
| tc-spe-result-003 | Integration | All PipelineStageResults aggregated by SkillOutputEntity | Medium | R-43 |

## Validation Criteria

- All stage results must have a non-null `stage_name`.
- `SkillExecutionContext.environment` must be one of `dev` or `prod`.
