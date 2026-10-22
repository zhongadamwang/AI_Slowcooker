# T05 — Build-and-Clarify Loop for Change Management & Planning

**Task ID**: T05
**Phase**: Phase 2 - Orchestration
**Priority**: P1-High
**Estimated Effort**: 1-2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22
**Completed**: 2026-10-22

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
- [x] `change-management/SKILL.md` updated with mode-conditional stakeholder communication step
- [x] `project-planning-tracking/SKILL.md` updated similarly
- [x] "real external stakeholder" flag concept documented with examples in `collaboration-mode-reference.md`

## Dependencies

### Prerequisites
- **T01** — mode definitions
- **T04** — establishes the pattern for mode-conditional skill instructions (do this one second so the pattern is proven)

### Blocks
- None

---

## Completion Notes

**Completed**: 2026-10-22

### Changes Made

- **`.github/skills/change-management/SKILL.md`**:
  - "Project Phase Context" — Deployment Phase's "require stakeholder approval" annotated: in solo mode, deployment-phase changes always require a real external check-in regardless of role flag, since deployment risk is too high for self-attestation alone
  - New **Mode-Conditional Stakeholder Communication** section (after Processing Rules): defines the three-way behavior (traditional: formal communication; solo + developer-played role: self-perspective note; solo + real external role: genuine check-in, same as traditional)
  - New **Real External Stakeholder Flag** subsection with the role/flag/rationale table (FR-05.3) — also mirrored into `collaboration-mode-reference.md` as the canonical source, with this skill cross-referencing it
  - Quality Checks — "Critical changes require immediate stakeholder notification" made mode-conditional

- **`.github/skills/project-planning-tracking/SKILL.md`**:
  - "Estimation Update Process" Step 5 ("Communicate Changes") made mode-conditional, cross-referencing `change-management`'s flag table rather than duplicating it
  - "Change Management Integration" → Step 4 Implementation Planning's "Stakeholder Communication: Notify affected parties" made mode-conditional, same cross-reference pattern

- **`artifacts/Documentation/collaboration-mode-reference.md`** (canonical source for the flag, per FR-05.3):
  - New **Real External Stakeholder Flag** section: formal definition (real external vs. developer-played), the governing rule (build-and-clarify loop only applies to developer-played roles), the same role/flag/rationale table, the "default to real external when unclear" safety rule, and a note on where it's applied

### Key Decisions

- Defined the flag **once**, canonically, in `collaboration-mode-reference.md`, and had both `change-management` and `project-planning-tracking` cross-reference it rather than duplicating the table in three places — avoids the table drifting out of sync across skills
- Added the **deployment-phase exception** in `change-management` (always require a real check-in for deployment-phase changes, regardless of flag) as a deliberate escalation beyond the base FR-05.1 requirement — judged that the existing "Only critical changes allowed, require stakeholder approval" language for Deployment Phase already signals higher stakes than the flag mechanism alone should fully delegate to self-attestation
- Kept `TR-05.1` (no project-state schema changes) — this task is entirely skill-instruction and reference-documentation level, consistent with T04's approach

### Next Steps for Integration

- **T06**: Publish `solo-mode-guide.md`, migration notes, and run an end-to-end validation walkthrough that exercises a change request through `change-management` in solo mode, with at least one developer-played role and one real-external role, to confirm the flag table reads clearly in practice
