# W5H Requirements Analysis

**Project**: PRJ-07  
**Date**: 2026-11-07  
**Sources**: [Requirements](requirements.md), [goals](goals.md), [implementation analysis](implementation-analysis.md)

## Who

Solo-mode role assumptions, not externally confirmed stakeholder claims:

- **Framework maintainer lens**: assume responsibility for contracts, skill registration, and backward-compatible workflow updates.
- **Model author lens**: assume need for consistent entities, boundaries, and actor interactions across levels.
- **Reviewer/QA lens**: assume need for explicit validation evidence and focused clarification rather than success-shaped defaults.
- **Prototype consumer lens**: assume need for preserved clickable navigation, dialogs, and reusable handoff.

No real external approval authority or fixed staffing was specified.

## What

Three proposed responsibilities: use-case generation/scripts, UI-model generation, and shared alignment validation. Integrate existing six UI skills into S5 and connect modeling/change workflows. All R-001 through R-011 are in scope; production application implementation, external services, broad historical migration, and a new gate engine are not.

## When

At the end of every modeling round, including revisions and resumed work, require current validation. Implementation follows seven dependency-linked tasks; provisional solo effort is 19.17 person-days plus 3 working days of contingency. No committed start or end date.

## Where

Implement in the existing `.github/skills/` framework. Models belong to the identified process/boundary folders resolved from project and hierarchy metadata; reports belong to project analysis artifacts; prototypes retain their existing artifact category. Use cases cover all identified boundary levels; UI exists only in software boundaries.

## Why

Make design understandable across actors, processes, entities, and screens while preventing divergent models from being treated as aligned. Release measures are in [goals.md](goals.md); no unsupported time-saving or financial KPI is claimed.

## How

Define the shared contract first. Build use-case generation, UI-model generation, and deterministic validation against that contract. Wire existing producers/consumers, then integrate round lifecycle into orchestration and direct skill use. Demonstrate positive and negative multi-level examples and preserve prototype behavior. Solo self-attestation does not resolve entity or boundary contradictions.
