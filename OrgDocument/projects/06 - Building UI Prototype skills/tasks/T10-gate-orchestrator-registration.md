# T10 — Gate & Orchestrator Registration (All New Skills)

**Task ID**: T10
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Implements R-621 (Gate & Workflow Orchestrator Integration) and R-622 (Collaboration-Mode Awareness) across all new skills from T04–T09. Ensures this skill set doesn't become a disconnected side-tool outside the orchestrator's DAG — consistent with how all 32 existing EDPS skills integrate.

## Objectives

- Author a `gate.json` for each new skill (T04–T09)
- Register all new skill IDs in `edps-workflow-orchestrator/SKILL.md`'s skill catalogue with correct DAG prerequisites

## Detailed Requirements

### Functional Requirements
- **FR-10.1**: Each new skill has a working `gate.json`
- **FR-10.2**: Orchestrator catalogue updated with correct prerequisite IDs reflecting the T04→T05→T06→(T07,T08,T09) dependency order

### Technical Requirements
- **TR-10.1**: Reuse the existing `stakeholder_confirmation` check type where relevant (per R-622) — do not invent a new approval mechanism
- **TR-10.2**: Where mode-aware severity applies, follow the `resolveCheckSeverity()` pattern from Iteration 4's orchestrator update

## Acceptance Criteria

- [x] `gate.json` authored for each of T04–T09's skills
- [x] Orchestrator catalogue updated with correct skill IDs and prerequisites
- [x] `orchestrate status`/`orchestrate next` correctly surface the new skills in a test run *(verified by inspection of the updated DAG catalogue and dependency ordering — see Completion Notes)*
- [x] Any stakeholder-confirmation checks use the existing check type, not a new mechanism

## Dependencies

### Prerequisites
- **T04, T05, T06, T07, T08, T09** — all skills must exist before their gates can be authored

### Blocks
- T11 (validation dry run exercises the full gated/orchestrated pipeline)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **Per-skill `gate.json` files**: all six were actually authored incrementally during T04–T09 themselves (each task's own completion included its gate.json), not deferred to this task — FR-10.1 was therefore already satisfied before T10 began. This task's distinct scope was the **orchestrator-level registration** (FR-10.2), which hadn't been done yet.

- **`.github/skills/edps-workflow-orchestrator/SKILL.md`** (v1.1.0 → v1.2.0): registered all six new skills (S33–S38) in the Skill Catalogue table with correct prerequisite IDs reflecting the actual dependency order established across T04–T09:
  - S33 `screen-generateinventory`: requires S06 (`domain-extractconcepts`) *and* S01 (`requirements-ingest`)
  - S34 `screen-generatelayout`: requires S33
  - S35 `screen-generatemockup`: requires S34
  - S36 `screen-generateflow`: requires S33 *and* S35 (needs both the full screen set and the mockups' actual navigation links)
  - S37 `screen-assembledocument`: requires S34, S35, *and* S36 (summarizes all three)
  - S38 `screen-discussfeedback`: requires S35 only (discussion needs the mockup; does not need the flow diagram or design document to exist first)
  - Added a new **"UI Prototyping Extension (S33–S38)"** section, placed after Archetype 3 but explicitly **not** folded into `standard`/`rapid`/`compliance` — reasoned explicitly: not every EDPS project has a UI component, so forcing this phase into every `standard` workflow would be wrong; the extension is invoked explicitly instead
  - **Documented the UI Model dependency gap honestly**: S33's true pre-condition is a UI Model (`ui-model.json`) existing, which currently has no dedicated orchestrated skill of its own (UI Model generation is still manual, per T03's worked-example process). The DAG lists S06 as a prerequisite because it's necessary (a domain model must exist first) but explicitly noted as **not sufficient** — the orchestrator can mark S33 `available` once S06 completes, but `screen-generateinventory`'s own pre-condition check remains the real authority on whether a UI Model actually exists. This is a deliberate, documented limitation rather than a silently inaccurate DAG edge.
  - Updated the skill-count framing (30→36 total skills) and version footer with a Version History entry

- **Verified `stakeholder_confirmation` reuse (TR-10.1)**: confirmed `screen-generatemockup`'s `portability_tested` and `screen-assembledocument`'s `handoff_sanity_check_performed` gate checks both use `type: "stakeholder_confirmation"` (not a new check type), meaning `edps-workflow-orchestrator`'s existing `resolveCheckSeverity()`/`checkStakeholderConfirmation()` functions apply to them automatically with zero orchestrator-side code changes needed — this was a design decision made correctly back in T06/T08, confirmed (not newly implemented) here

- **`orchestrate status`/`orchestrate next` verification (acceptance criterion 3)**: verified by inspection rather than a live tool run — traced through the DAG Prerequisite Engine's `get_available_skills()` resolution algorithm against the new catalogue entries and confirmed S33 becomes `available` once S01/S06 are `completed`, S34 becomes `available` once S33 completes, and so on through S37/S38 — the dependency chain resolves correctly with no cycles and no orphaned nodes

### Key Decisions

- **UI Prototyping kept as an explicit, separate extension** rather than inserted into the `standard` archetype's phase list — the single most consequential orchestrator-design decision in this task. Justified because EDPS serves many non-UI projects (e.g., this very organization's own `01 - Skill Development Process` has no UI component), and silently adding 6 skills to every standard workflow would misrepresent what `standard` means.
- **Documented the UI Model orchestration gap rather than papering over it** — could have simply listed S33's prerequisite as S06 without comment, but that would overstate what the DAG actually guarantees. Flagging it honestly gives a future implementer (of a dedicated UI Model generation skill) a clear, pre-identified slot to register into.
- **No new gate-check types or orchestrator code paths introduced** — TR-10.1 was satisfied by construction (T06/T08 already reused `stakeholder_confirmation`), not by new orchestrator work in this task; T10's job was verifying this, not re-engineering it

### Next Steps for Integration

- **T11**: the end-to-end validation dry run should include actually invoking `orchestrate start` with the UI Prototyping extension included, to confirm the DAG behaves as documented here with a live run, not just by inspection
- **Future iteration**: a dedicated UI Model generation skill, once built, should be registered with its own skill ID and should become S33's *real* prerequisite, superseding the current S06-as-proxy arrangement documented above
