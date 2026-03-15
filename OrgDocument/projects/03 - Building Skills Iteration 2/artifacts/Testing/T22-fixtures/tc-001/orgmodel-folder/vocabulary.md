<!-- Identifier: V-01-01 -->

# Skill Pipeline Execution — Vocabulary

## Canonical Terms

| Term | Definition | Aliases | Context |
|------|------------|---------|---------|
| **Skill Execution Context** | Runtime environment and parameter bundle for a single skill invocation | Invocation Context, Runtime Context | Pipeline execution, skill orchestration |
| **Pipeline Stage Result** | Recorded outcome of one discrete stage within a skill execution pipeline | Stage Output, Stage Record | Pipeline monitoring, audit trails |

## Domain Alignment

Terms sourced from `domain-concepts.json` (project analysis, 2026-03-15). Merged by `orgmodel-update` (guard-exempt path).

## Consistency Rules

- Use "Skill Execution Context" (not "Runtime Context") in all skill pipeline documentation.
- Use "Pipeline Stage Result" (not "Stage Output") as the canonical term in test cases and monitoring docs.
