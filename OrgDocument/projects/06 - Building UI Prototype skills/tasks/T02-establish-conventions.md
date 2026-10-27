# T02 — Establish Traceability & Format Conventions

**Task ID**: T02
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 0.5 day
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Several requirements (R-605, R-606, R-623–R-626) are cross-cutting constraints that every generation task (T04–T09) must respect, rather than a single standalone feature. Documenting them once now avoids re-deriving them ad-hoc in each later task's own instructions.

## Objectives

- Finalize ID formats for screens and UI Model entries
- Document the traceability tag convention used across generated Markdown/JSON
- Publish a pre-ship checklist covering the hard constraints (text-based, no design tool, no tech stack, `file://` portability)

## Detailed Requirements

### Functional Requirements
- **FR-02.1**: ID format finalized — proposed `SCR-[###]` for screens, `UME-[###]` for UI Model entries (per `vocabulary.md`'s proposal), confirmed rather than left as "recommended, not yet enforced"
- **FR-02.2**: Traceability tag format documented — how `requirement_refs`/`ui_model_ref` are embedded in generated output

### Technical Requirements
- **TR-02.1**: Constraints checklist must be literal and checkable (a real checklist, not prose) so T04–T09 can verify against it directly

## Acceptance Criteria

- [x] Conventions document published at `artifacts/Documentation/ui-prototyping-conventions.md`
- [x] ID formats finalized and cross-referenced from this document
- [x] Hard-constraints checklist present and literal/checkable

## Dependencies

### Prerequisites
- None

### Blocks
- T03, T04, T05, T06, T07, T08, T09 (all reference these conventions)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`artifacts/Documentation/ui-prototyping-conventions.md`** (new, published):
  - **Section 1 — ID Formats (Finalized)**: confirmed `SCR-[###]` (Screen) and `UME-[###]` (UI Model Entry) from `vocabulary.md`'s proposal; added four previously-undefined ID formats needed by later tasks — `LS-[###]` (Layout Spec, paired 1:1 with its Screen), `IM-[###]` (Interactive Mockup, same pairing), `IF-[###]` (Interaction Flow, independently sequenced since one flow spans multiple screens), `DD-[###]` (Design Document), `FB-[###]` (Feedback Item), `DS-[###]` (Design Specification import, reserved for Phase 2). Reused `change-management`'s existing `generate_change_id()` scan-and-increment algorithm rather than inventing a new one.
  - **Derived UI Model numbering rule**: `UME-[###]` is scoped per model (base and each derived model have independent sequences), with derived entries carrying a `derives_from_entry` field — settled now so T03's schema doesn't need a breaking change when Phase 3's derived models are eventually built
  - **Section 2 — Traceability Tag Format**: JSON uses flat `requirement_refs` (array) and `ui_model_ref` (singular — a Screen traces to exactly one UIModelEntry per R-606/R-628); Markdown reuses the existing EDPS inline *(Ref: ...)* citation style already seen in `goals.md`/`w5h-analysis.md`, rather than introducing a new citation convention specific to this skill set
  - **Section 3 — Hard-Constraints Checklist**: literal, checkable form of R-623–R-626/D-5 — six checkboxes covering text-only output, no design-tool dependency, no target-framework assumption, tested (not assumed) mockup portability, changelog presence, and no-direct-domain-reference
  - **Section 4 — File & Folder Layout**: confirmed per-screen sub-folders (`SCR-001/layout-spec.md`, `SCR-001/mockup.html`) over a flat naming scheme, chosen specifically because mockup clickable-navigation (R-603) needs simple relative links between screen folders — a new layout decision made here since no prior document had settled it, rather than leaving T04–T07 to each invent their own
  - **Section 5**: confirmed no new terminology introduced beyond what `vocabulary.md` already defines

- **`artifacts/Documentation/main.md`**: updated from empty stub to reference the new conventions document

### Key Decisions

- **Paired IDs for LayoutSpec/InteractiveMockup** (same numeric suffix as their owning Screen) rather than independent sequencing — makes the 1:1 relationship (R-602/R-602a) visually obvious from the ID alone, and simplifies the per-screen sub-folder layout in Section 4
- **`ui_model_ref` is singular, `requirement_refs` is plural** — directly encodes the cardinality difference already established in `domain-concepts.md`'s REL-601 (many-to-one Screen→UIModelEntry) vs. R-605's potentially-many requirement traceability, rather than treating both as generic arrays
- **Per-screen sub-folders over flat filenames**: a layout decision not previously specified anywhere in `requirements.md`/`domain-concepts.md`; made explicitly here (not deferred to T04) because settling it once in T02 avoids T04–T07 each needing to independently decide file layout and risk inconsistency

### Next Steps for Integration

- **T03**: UI Model schema prototype must use the `UME-[###]` format and the base/derived numbering rule defined here
- **T04–T07**: must write to the `artifacts/UI Prototype/SCR-[###]/` sub-folder layout from Section 4, and verify their own output against Section 3's checklist before marking acceptance criteria met
- **T08**: Design Document assembly uses `DD-[###]` and the same Markdown traceability citation style
