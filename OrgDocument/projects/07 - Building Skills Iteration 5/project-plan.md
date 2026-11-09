# Project Plan — 07 - Building Skills Iteration 5

**Project ID**: PRJ-07  
**Archetype**: standard  
**Project Created**: 2026-11-07  
**Implementation Start**: Uncommitted  
**Target Completion**: Approximately 23 working days after implementation starts, assuming one full-capacity implementer  
**Status**: Planned - Implementation Not Started

## Executive Summary
Integrate UI prototyping into S5, introduce use-case models and detailed scripts at all system-boundary levels, and align entities/system boundaries across models after every modeling round. UI screens belong only to software boundaries. Unresolved inconsistencies require clarification and revalidation.

The recommended design adds three responsibility-based skills: `usecase-generatemodel`, `ui-generatemodel`, and `model-validatealignment`. The dedicated UI-model producer closes the current manually authored UI Model gap. Existing six screen skills and their behavior remain; only their category moves from S11 to S5. Preserve the unrelated S11 skill ID for `documentation-automation`.

## Planning Artifacts

- [Implementation analysis](artifacts/Analysis/implementation-analysis.md) - Existing framework evidence, contracts, impact surfaces, risks, and proposed design
- [Requirements](artifacts/Analysis/requirements.md), [goals](artifacts/Analysis/goals.md), and [W5H](artifacts/Analysis/w5h-analysis.md) - Scope and rationale
- [Task breakdown](artifacts/Analysis/task-breakdown.md) - Seven tasks, dependencies, and 11/11 requirement coverage
- [Task tracking](tasks/task-tracking.md) - All implementation tasks not started
- [Effort estimates](artifacts/Analysis/effort-estimates.md) and [confidence](artifacts/Analysis/estimation-confidence.md) - Provisional PERT estimate and limitations
- [Schedule](artifacts/Analysis/project-schedule.md), [critical path](artifacts/Analysis/critical-path-analysis.md), and [milestones](artifacts/Analysis/milestone-plan.md) - Resource assumptions and delivery checkpoints

## Project Phases

### Phase 0: Requirements Analysis and Planning
Completed for this planning step: requirements/decisions, framework analysis, goals/W5H, tasks, provisional estimates, and schedule. No implementation tests or modeling release gates are claimed as complete.

### Phase 1: Foundation
**Task**: T01  
**Expected effort**: 2.00 person-days  
**Deliverables**: Shared entity/boundary/version/applicability contract, fixtures, and responsibility/ID decisions

### Phase 2: Modeling and Validation
**Tasks**: T02, T03, T04, each requiring T01  
**Expected effort**: 8.50 person-days  
**Deliverables**: Use-case models/scripts, software-boundary UI-model producer, deterministic source-backed validator and clarification reports

### Phase 3: Integration
**Tasks**: T05 after T02/T03/T04; T06 after T05  
**Expected effort**: 5.50 person-days  
**Deliverables**: Existing producer/consumer/change handoffs, S5 routing/membership, non-bypassable round validation and version-aware resume

### Phase 4: Release Verification
**Task**: T07 after T06  
**Expected effort**: 3.17 person-days  
**Deliverables**: Multi-level worked example, negative tests, observed UI interactions, 11/11 passing evidence, and guide/handoff

## Schedule and Capacity

Expected total: 19.17 person-days plus 3 working days contingency; approximately 23 full working days (about five weeks at five days/week). Staffing and start date are unconfirmed; solo collaboration mode is not proof of one-person capacity. T02/T03/T04 can be implemented in parallel against shared fixtures, giving an unlimited-resource critical path of approximately 14.00 working days before buffer. The baseline assumes serial work by one implementer.

## Risk Management
Highest risks: source-backed validation rather than detached manifests, cross-level identity collisions, category/skill ID confusion, legacy state/type compatibility, and accidental solo/rapid alignment bypass. Reuse current VR/HR validators and prototype contracts; re-estimate after T01 and first validator fixtures. See the [risk table](artifacts/Analysis/implementation-analysis.md).

## Release Exit

All 11 requirements have passing evidence. Fresh/revised/resumed modeling rounds end with current validation; inconsistencies require clarification, not false success. UI screens exist only within software boundaries. Existing inventory shapes, IDs, file-portable prototypes, navigation, dialogs, and feedback routing are preserved.
