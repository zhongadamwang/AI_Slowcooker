# T09 — Author screen-discussfeedback Skill (Discussion + change-management Routing)

**Task ID**: T09
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Implements R-611 (Discussion Surface), R-612 (Feedback Capture), R-614 (Solo-Mode Role-Play), and R-620 (Change Loop) — the third pillar of the user's original ask: using the mockup to "discuss requirements, ideas, designs with stakeholders." Decide during authoring whether this is a standalone skill or an instruction-level addition to an existing skill.

## Objectives

- Present the mockup set as a discussion surface
- Capture `FeedbackItem`s and produce structured input compatible with `change-management`'s existing change-document schema
- Support solo-mode role-play per `process-w5h`'s existing pattern

## Detailed Requirements

### Functional Requirements
- **FR-09.1**: At least one real or simulated feedback item successfully produces a valid `change-management`-compatible structured change document, with no manual re-transcription step
- **FR-09.2**: Solo-mode role-play guidance present, including its own "when to break out of solo mode" note

### Technical Requirements
- **TR-09.1**: **Front-load the schema compatibility check** (flagged as Medium risk in scope-analysis.md) — confirm early in this task, not after full implementation, that `change-management`'s schema can represent UI-specific feedback (e.g., "change field Y from optional to required on Screen X") without needing a new change type

## Acceptance Criteria

- [ ] Schema compatibility with `change-management` confirmed early (per TR-09.1) before deeper implementation
- [ ] SKILL.md (or instruction addition) authored
- [ ] At least one feedback item successfully routed to a valid change-management structured change document
- [ ] Solo-mode role-play guidance present and consistent with `process-w5h`'s pattern

## Dependencies

### Prerequisites
- **T06** — discussion surface is built on the mockup

### Blocks
- T10 (gate registration needs a stable output to validate against)
- T11 (validation dry run exercises this skill)
