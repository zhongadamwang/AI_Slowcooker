# T09 — Author screen-discussfeedback Skill (Discussion + change-management Routing)

**Task ID**: T09
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

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

- [x] Schema compatibility with `change-management` confirmed early (per TR-09.1) before deeper implementation
- [x] SKILL.md (or instruction addition) authored
- [x] At least one feedback item successfully routed to a valid change-management structured change document
- [x] Solo-mode role-play guidance present and consistent with `process-w5h`'s pattern

## Dependencies

### Prerequisites
- **T06** — discussion surface is built on the mockup

### Blocks
- T10 (gate registration needs a stable output to validate against)
- T11 (validation dry run exercises this skill)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **Schema compatibility check (TR-09.1) performed and documented first**, before SKILL.md's deeper design, per the task's own instruction to front-load this risk: `change-management`'s existing `change_type` taxonomy (`REQ-CHG`/`REQ-ADD`/`REQ-REM`/`SCOPE-CHG`/`PROC-CHG`) and `impact_analysis.affected_documents[].file_path` field fully accommodate UI-specific feedback — e.g., "change field Y from optional to required on Screen X" maps to `REQ-CHG` with the screen's `layout-spec.md` as the affected document. **No schema extension to `change-management` was needed.** This finding is recorded both in the task's completion log and directly in the SKILL.md itself (its own "Schema Compatibility Confirmation" section), so the finding is visible to anyone reading the skill later, not just archived in this task file.

- **`.github/skills/screen-discussfeedback/SKILL.md`** (new, v1.0.0, skill_id S38): authored as a standalone skill (the task left this an open decision; chosen over an instruction-level addition to an existing skill since this capability has its own distinct inputs/outputs/process worth documenting on its own). Key design points:
  - **Explicitly never generates `artifacts/Changes/*.md` files itself** — hands off `feedback_text` to `change-management`, which remains the sole owner of that file's generation; this boundary is stated plainly and enforced at the gate level (see below)
  - **`feedback-log.md` is append-only**, explicitly contrasted with `screen-inventory.json`'s regenerate-fresh convention — feedback history should accumulate across sessions, not reset, since it's a discussion record, not a derived index
  - **Step 2 reuses `process-w5h`'s exact solo-mode documentation pattern** (role lens + assumption, inline) rather than inventing a new format, and reuses `process-w5h`'s own "when to break out of solo mode" criteria rather than redefining them — satisfies FR-09.2 by pointing at an existing, already-validated pattern
  - **Step 5 makes "no manual re-transcription" literal**: the same `feedback_text` captured in Step 3 is the exact text handed to `change-management`, not a re-derived paraphrase — FR-09.1's requirement made mechanically checkable rather than just an intention
  - **Not every discussion comment becomes a FeedbackItem** — explicitly distinguishes actionable commentary (implies a change) from general praise/confirmation, avoiding a flood of trivial change documents for routine positive feedback

- **`.github/skills/screen-discussfeedback/gate.json`** (new, skill_id S38, confirmed unique): 5 checks — `feedback_log_exists` (soft, since a project may not yet have had a discussion session), `feedback_items_traced_to_screen` and `source_mode_declared` (hard, enforcing R-612/R-614's structured capture), **`no_changes_file_authored_directly`** (hard — a distinctive guard confirming this skill respects the ownership boundary with `change-management` rather than silently generating `Changes/` files itself), `routing_recorded` (soft, since routing may lag capture)

- **`.github/skills/README.md`**: S11 section extended with `screen-discussfeedback`'s row, and explicitly notes this completes the MVP generation-and-discussion pipeline
- **`.github/skills/INDEX.md`**: skill count 37→38, version 2.6.0→2.7.0, new changelog entry highlighting the TR-09.1 schema-compatibility finding

### Key Decisions

- **Authored as a standalone skill**, resolving the task's open "standalone vs. instruction-addition" question — justified because discussion/feedback-routing has genuinely distinct inputs (mockups + stakeholder commentary), outputs (`feedback-log.md` + a `change-management` handoff), and process steps worth documenting independently, rather than being a minor addendum to an existing skill's instructions
- **`no_changes_file_authored_directly` as a hard gate check** — a cross-skill ownership boundary (this skill vs. `change-management`) is important enough to verify automatically, not just state in prose, since a future implementer might otherwise be tempted to shortcut the handoff by writing the change document directly
- **feedback-log.md explicitly append-only** — a deliberate asymmetry from this pipeline's other artifacts (most of which regenerate fresh), justified because discussion history has intrinsic value that a fresh-regeneration model would destroy

### Next Steps for Integration

- **T10**: must register `screen-discussfeedback` (S38) in the orchestrator's DAG with a prerequisite on `screen-generatemockup`; this is also the last new skill T10 needs to register before gate/orchestrator work is complete for the MVP
- **T11**: the end-to-end validation dry run should specifically exercise at least one real feedback-to-change-document routing, confirming FR-09.1's "no manual re-transcription" holds in practice, not just in the skill's own design
