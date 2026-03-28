<!-- Identifier: I-02 -->

# 02 - Analysis Process

## Business Model Overview

The Analysis Process covers requirements ingestion, domain concept extraction, and entity alignment activities that transform raw requirements into structured domain models. Updated by `orgmodel-update` on 2026-03-15 with 3 new domain entities from project analysis.

## Process Flow
See [process.md](process.md) for detailed activity diagram.

## Collaborations
See [collaboration.md](collaboration.md) for entity interactions.

## Domain Model
See [domain-model.md](domain-model.md) for actors and entities.

## Sub-Processes
- Requirements ingestion pipeline (via `requirements-ingest` skill)
- Domain extraction (via `domain-extractconcepts` skill)
- Entity alignment (via `domain-alignentities` skill)

## Key Entities (added 2026-03-15)

| Entity | Domain Area | Source |
|--------|-------------|--------|
| RequirementChunk | Requirements Analysis | R-10 |
| AlignmentDecision | Domain Alignment | R-11 |
| AnalysisPipeline | Pipeline Orchestration | R-12 |

## Test Coverage
See [test-case-list.md](test-case-list.md) for verification test cases.

## Key Documents

- [Collaboration Diagram](collaboration.md)
- [Process Flow](process.md)
- [Domain Model](domain-model.md)
