# T08 — Author screen-assembledocument Skill (Consolidated Design Doc)

**Task ID**: T08
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Implements R-607 (UI Design Document Output), R-608 (JSON Companion), and R-610 (In-Document Changelog) at the consolidated-document level. This is the durable deliverable "suitable for handing to a future developer without requiring the original AI session" — one of the project's core stated goals.

## Objectives

- Author a skill that assembles the consolidated `DesignDocument` (Markdown + JSON) summarizing all screens/flows/components from T04–T07
- Include a top-level in-document changelog

## Detailed Requirements

### Functional Requirements
- **FR-08.1**: Consolidated document summarizes screens/flows/components without duplicating full storage — screen inventory (T04) remains the standalone source of truth; this document references it
- **FR-08.2**: JSON companion output mirrors the Markdown content

### Technical Requirements
- **TR-08.1**: Document must pass a "handoff" sanity check — readable and actionable by someone unfamiliar with the generating session (or self-reviewed from that lens in solo mode)

## Acceptance Criteria

- [x] SKILL.md authored
- [x] Consolidated design document generated from a test screen/flow/component set
- [x] JSON companion well-formed and consistent with Markdown content
- [x] Handoff sanity check performed and passed

## Dependencies

### Prerequisites
- **T05, T06, T07** — needs layout specs, mockups, and flows to summarize

### Blocks
- T10 (gate registration needs a stable output to validate against)
- T11 (validation dry run exercises this skill)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/screen-assembledocument/SKILL.md`** (new, v1.0.0, skill_id S37): the pipeline's terminal consumer — the first skill in this set that generates nothing new, only summarizes/links to what T04–T07 already produced. Key design points:
  - **Explicit "Critical distinction" callout** up front contrasting this skill with every prior one: it does not generate screens/layouts/mockups/flows, only consolidates them — stated plainly so an implementer doesn't accidentally re-derive content generation logic here
  - **JSON's `screens_summary`/`flows_summary` are reference objects** (IDs + file paths), not copies of the underlying content — makes FR-08.1's "summarize without duplicating" concrete in the JSON schema itself, not just a Markdown-only discipline
  - **Component Notes (Step 4) explicitly kept non-rigorous**, consistent with R-604/CON-5's informal component-inventory philosophy — a short prose summary, not a formal catalogue
  - **Design Rationale Highlights (Step 5) explicitly selective**, not an exhaustive re-listing of every screen's rationale — only what matters at the project level
  - **Handoff sanity check (Step 8) given real process detail**, not just named: re-read the document as someone unfamiliar with the generating session, explicitly checking for session-dependent language ("as we discussed") that would silently fail for a real future reader; made non-skippable and required to leave evidence
  - Explicitly notes this skill is a genuine pipeline terminus in MVP — `screen-discussfeedback` (T09) consumes mockups directly, not this document, since discussion needs the live clickable artifact

- **`.github/skills/screen-assembledocument/gate.json`** (new, skill_id S37, confirmed unique): 6 checks — 4 hard content/existence checks including `no_full_duplication` (a regex guard against re-embedding Mermaid diagrams or full per-screen inventory listings) and `links_to_source_artifacts` (confirms the document actually links out rather than inlining), `handoff_sanity_check_performed` (reuses `stakeholder_confirmation` as a self-verification mechanism, the second UI Prototyping skill to do so after T06's `portability_tested`), and 1 soft `id_format_valid`

- **`.github/skills/README.md`**: S11 section extended with `screen-assembledocument`'s row
- **`.github/skills/INDEX.md`**: skill count 36→37, version 2.5.0→2.6.0, new changelog entry

### Key Decisions

- **No-duplication enforced at the gate level, not just as authoring guidance** — the `no_full_duplication` regex check means an implementation that accidentally re-embeds full content (e.g., copy-pasting a screen's full detail instead of linking) fails the gate automatically, rather than relying solely on the SKILL.md's prose discipline
- **Second reuse of `stakeholder_confirmation` for a QA-style self-check** (handoff sanity, following T06's portability-test precedent) — reinforces this as the emerging pattern for "did the developer actually verify this" checks across the UI Prototyping skill set, rather than each skill inventing its own ad-hoc verification mechanism
- **Explicitly scoped this skill as the MVP pipeline's terminus** — avoided the temptation to have it feed into T09 as well; discussion operates on mockups directly, keeping this document's role purely as the static handoff artifact

### Next Steps for Integration

- **T09** (`screen-discussfeedback`): operates on mockups, not this document — should not be designed to consume `design-document.json`
- **T10**: must register `screen-assembledocument` (S37) in the orchestrator's DAG with prerequisites on `screen-generatelayout`, `screen-generatemockup`, and `screen-generateflow`
- **T11**: the end-to-end validation dry run should specifically exercise this skill's handoff sanity check as a real, not simulated, step
