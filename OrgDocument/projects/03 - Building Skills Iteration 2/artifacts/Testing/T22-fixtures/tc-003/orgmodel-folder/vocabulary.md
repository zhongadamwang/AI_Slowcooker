<!-- Identifier: V-01-01-TC3 -->

# Skill Pipeline Execution — Vocabulary

## Canonical Terms

| Term | Definition | Aliases | Context |
|------|------------|---------|---------|
| **Pipeline Stage** | A discrete, ordered unit of work within a skill execution pipeline | Stage, Execution Step | Pipeline orchestration |
| **Skill Invocation** | A single call to execute a named skill with provided inputs | Skill Call, Skill Execution Request | Skill runtime, practitioner workflow |
| **Boundary Participant** | An EDPS sequence diagram participant with `type: boundary` that acts as the entry point for external messages | Boundary | Collaboration design, hierarchy management |
| **Control Participant** | An EDPS sequence diagram participant with `type: control` that orchestrates internal logic and is eligible for decomposition | Control, Orchestrator | Collaboration design, hierarchy management |
| **Entity Participant** | An EDPS sequence diagram participant with `type: entity` representing a data store or passive record | Entity, Data Store | Collaboration design, domain modeling |
| **Skill Invocation Log** | Audit record capturing the full context of a single skill invocation | Invocation Audit, Skill Audit Record | Audit trail, traceability, compliance |
| **Outcome Status** | Enumerated result of a skill invocation: success, failure, or skip | Invocation Outcome, Execution Status | Pipeline monitoring, reporting |

## Domain Alignment

Terms in rows 6–7 sourced from `domain-concepts.json` (project analysis, 2026-03-15). Updated by `orgmodel-update` EDPS-hierarchy guard-exempt path (vocabulary.md always updated regardless of guard).

## Consistency Rules

- Use "Skill Invocation Log" (not "Invocation Audit") as the canonical term for audit records.
- Use "Outcome Status" (not "Execution Status") in all reporting and monitoring contexts.
