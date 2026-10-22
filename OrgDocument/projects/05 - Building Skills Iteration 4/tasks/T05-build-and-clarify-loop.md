# T05 — Build-and-Clarify Loop for Change Management & Planning

**Task ID**: T05
**Phase**: Phase 2 - Orchestration
**Priority**: P1-High
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22

## Description

`change-management` and `project-planning-tracking` both assume a "communicate changes to stakeholders" step aimed at a separate audience. In solo mode this becomes an internal build-and-clarify loop: the developer logs the change from each affected role's perspective and only reaches out externally when a role represents a real third party whose buy-in actually matters (e.g., an actual client, not an internal "QA" role the developer is also playing).

## Objectives

- Replace the implicit "notify stakeholders" step with a mode-conditional one in both skills
- Introduce the concept of a "real external stakeholder" flag per role (distinguishes roles the developer can self-represent from roles tied to an actual separate person, e.g., "Client/Sponsor") — this flag matters in solo mode to decide when a real check-in is still required

## Detailed Requirements

### Functional Requirements
- **FR-05.1**: `change-management/SKILL.md` — "Communicate Changes: Update stakeholders on schedule impact" becomes mode-conditional: traditional → formal stakeholder communication; solo → self-logged role-perspective note, **unless** the affected role is flagged as a real external stakeholder, in which case an actual check-in is still prompted
- **FR-05.2**: `project-planning-tracking/SKILL.md` — same treatment for its "Communicate Changes" step in the Re-baselining Process
- **FR-05.3**: Define the "real external stakeholder" role flag in `collaboration-mode-reference.md` (links back to T01) and give 2-3 worked examples (e.g., "Client" = real external; "QA", "DevOps" = developer-played in solo mode)

### Technical Requirements
- **TR-05.1**: No schema changes to project-state; this is skill-instruction level, consistent with T04's approach

## Acceptance Criteria

### Definition of Done
- [ ] `change-management/SKILL.md` updated with mode-conditional stakeholder communication step
- [ ] `project-planning-tracking/SKILL.md` updated similarly
- [ ] "real external stakeholder" flag concept documented with examples in `collaboration-mode-reference.md`

## Dependencies

### Prerequisites
- **T01** — mode definitions
- **T04** — establishes the pattern for mode-conditional skill instructions (do this one second so the pattern is proven)

### Blocks
- None
