<!-- Identifier: TCL-01-01-TC3 -->

# Skill Pipeline Execution — Test Case List

## Test Cases

| TC ID | Test Category | Title | Priority | Source Requirement |
|-------|---------------|-------|----------|--------------------|
| tc-spe-001 | Functional | Boundary receives invocation request | High | R-40 |
| tc-spe-002 | Functional | Control orchestrates pipeline stages in order | High | R-41 |
| tc-spe-003 | Integration | Output entity stores all stage results | Medium | R-41 |
| tc-spe-004 | Exception | Pipeline halts and reports error on stage failure | High | R-41 |
| tc-spe-log-001 | Functional | SkillInvocationLog records skill_name and invoked_by on success | High | R-44 |
| tc-spe-log-002 | Functional | SkillInvocationLog.outcome = failure when pipeline throws exception | High | R-44 |
| tc-spe-log-003 | Integration | SkillInvocationLog linked to correct PractitionerActor | Medium | R-44 |

## Test Categories

- **Functional**: Core process functionality
- **Integration**: Cross-entity interactions
- **Exception**: Error handling and recovery

## Validation Criteria

- `SkillInvocationLog` must be created for every `success` and `failure` outcome.
- `SkillInvocationLog.timestamp` must be set at invocation start, not completion.

---

_Rows 5–7 added by `orgmodel-update` EDPS-hierarchy guard-exempt path (test-case-list.md always updated). Updated: 2026-03-15._
