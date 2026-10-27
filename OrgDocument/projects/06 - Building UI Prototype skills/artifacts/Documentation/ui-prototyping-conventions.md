# UI Prototyping Conventions

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Version**: 1.0
**Created**: 2026-10-27
**Status**: Finalized — binding on all subsequent skill-authoring tasks (T03–T09)

## Purpose

This document finalizes the cross-cutting conventions flagged in `requirements.md`/`domain-concepts.md`/`vocabulary.md` as "recommended, not yet enforced" or otherwise left open pending confirmation. Every task from T03 onward must follow these conventions rather than re-deriving its own — consistency across the generation pipeline (T04–T07), the design document (T08), and discussion/feedback (T09) depends on this being settled once, here.

## 1. ID Formats (Finalized)

Per `vocabulary.md`'s proposal, now confirmed:

| Entity | ID Format | Example | Notes |
|---|---|---|---|
| Screen | `SCR-[###]` | `SCR-001` | Zero-padded 3-digit, sequential within a project, scanning existing `screen-inventory.json` for the next available number (same pattern as `change-management`'s `generate_change_id()`) |
| UI Model Entry | `UME-[###]` | `UME-001` | Zero-padded 3-digit, sequential within a UI Model (base or derived — see note below) |
| Layout Spec | `LS-[###]` | `LS-001` | One per Screen; same numeric suffix as its owning Screen for easy pairing (e.g., `SCR-001` ↔ `LS-001`) — **not** independently sequenced |
| Interactive Mockup | `IM-[###]` | `IM-001` | Same pairing rule as Layout Spec — `SCR-001` ↔ `IM-001` |
| Interaction Flow | `IF-[###]` | `IF-001` | Independently sequenced — one flow diagram can span multiple screens, so it does not pair 1:1 with a Screen ID |
| Design Document | `DD-[###]` | `DD-001` | Typically `DD-001` per project (one consolidated document); numbered for consistency with everything else, not because multiples are expected in v1 |
| Feedback Item | `FB-[###]` | `FB-001` | Sequential across the whole discussion history, not reset per session |
| Design Specification (import) | `DS-[###]` | `DS-001` | Sequential per imported spec (Phase 2 feature; reserved now so T03's schema doesn't need a breaking change later) |

**Derived UI Model note**: Since R-630/R-631 establish exactly one base UIModel plus zero or more derived UIModels, `UME-[###]` numbering is **scoped per model** (base and each derived model have their own independent `UME-001, UME-002...` sequence), not globally unique across all models in a project. A derived model's `UME-[###]` entry additionally carries a `derives_from_entry` field pointing to the base model's `UME-[###]` it was filtered/adapted from (see Section 2).

### ID Generation Algorithm (shared across all entity types above)

Reuse the existing `change-management` pattern (`generate_change_id()`) rather than inventing a new one:
1. Scan the existing artifact (e.g., `screen-inventory.json`) for the highest number currently in use for that entity type
2. Increment by 1, zero-pad to 3 digits
3. Verify uniqueness before writing (cross-check against the full inventory, not just the last-seen number, to avoid collisions from manual edits)

## 2. Traceability Tag Format (Finalized)

Every generated entity must carry explicit traceability fields, consistent with the existing EDPS `source_refs` convention (seen throughout `domain-concepts.md` and every other analysis skill's output).

### In JSON output
Traceability is a flat array field directly on the entity, named by what it traces *to*:

```json
{
  "screen_id": "SCR-001",
  "name": "Order Summary",
  "requirement_refs": ["R-614", "R-627"],
  "ui_model_ref": "UME-003"
}
```

- `requirement_refs`: array of requirement IDs (always an array, even if only one)
- `ui_model_ref`: **singular** string, not an array — per R-606/R-628, a Screen traces to exactly one UIModelEntry, never multiple. (Contrast with `requirement_refs`, which may legitimately be many-to-one.)
- `derives_from_entry` (UIModelEntry only, derived models only): singular string, the base model's `UME-[###]` this entry was adapted from

### In Markdown output
Traceability appears inline, immediately following the heading it belongs to, using the existing EDPS *(Ref: ...)* inline-citation style seen in `goals.md`/`w5h-analysis.md`:

```markdown
### Order Summary *(SCR-001)*
**UI Model Entry**: UME-003
*(Ref: R-614, R-627)*
```

This keeps generated Markdown visually consistent with every other EDPS analysis artifact in this repo, rather than introducing a new citation style specific to this skill set.

## 3. Hard-Constraints Checklist (Finalized, Literal, Checkable)

Every skill authored in T04–T09 must verify its own output against this checklist before considering its task complete. This is the literal, checkable form of R-623–R-626, D-5.

- [ ] **Text-only primary output** (R-623): every generated artifact (LayoutSpec, InteractiveMockup, DesignDocument, UIModel) is plain text — Markdown, HTML, CSS, JS, JSON, or Mermaid. No binary files are the *primary* deliverable for any of these entity types.
- [ ] **No design-tool dependency to produce output** (R-624): generation never assumes or requires access to Figma, Sketch, or any other commercial design tool. (Importing *from* such a tool is a separate, explicitly Phase-2-deferred capability — R-615 — and does not violate this constraint.)
- [ ] **No target framework assumption** (R-625): generated HTML/CSS/JS never references React, Vue, Angular, or any other application framework's APIs, imports, or conventions. Plain HTML/CSS/vanilla JS only.
- [ ] **Mockup portability** (R-626): every generated `InteractiveMockup` file opens successfully via `file://` with zero build step, zero package manager, and zero local server. This must be **tested**, not assumed — open the actual generated file in a real browser before marking a task's acceptance criteria met.
- [ ] **Changelog present** (R-610): every `LayoutSpec`, `DesignDocument`, and `UIModel` (base or derived) includes an in-document changelog section, even if it only has one entry ("Initial generation") at first creation.
- [ ] **No direct domain-entity reference** (R-606, R-628): confirm the generated Screen's traceability references a `UME-[###]` (UI Model Entry), never a domain entity ID directly.

## 4. File & Folder Layout (Confirmed)

Per T01's new `UI Prototype` artifact category and R-601a:

```
OrgDocument/projects/[NN] - [Project Name]/
└── artifacts/
    └── UI Prototype/
        ├── main.md
        ├── screen-inventory.md          ← ENT-602, standalone (D-6)
        ├── screen-inventory.json
        ├── design-document.md           ← ENT-608, consolidated (T08)
        ├── design-document.json
        ├── SCR-001/
        │   ├── layout-spec.md           ← LS-001
        │   └── mockup.html              ← IM-001, file://-openable
        ├── SCR-002/
        │   ├── layout-spec.md
        │   └── mockup.html
        └── interaction-flows.md         ← all IF-[###] diagrams, consolidated per project (not per-screen)

OrgDocument/orgModel/[NN] - [Process Name]/
├── domain-model.md                      ← pre-existing, not owned by this skill set
├── ui-model.md                          ← ENT-606, base model (T03)
├── ui-model.json
└── ui-model-derived-[role-slug]/        ← Phase 3, reserved now
    ├── ui-model.md
    └── ui-model.json
```

**Per-screen sub-folders** (`SCR-001/`, `SCR-002/`, ...) were chosen over a flat file-naming scheme (e.g., `SCR-001-layout-spec.md`) because the mockup's clickable navigation (R-603) needs relative links between screen folders that are simpler to generate and reason about than long flat filenames — this is a new layout decision not previously specified in `requirements.md`, made here because T02 is the right place to settle file-layout questions once, rather than leaving each of T04–T07 to invent its own.

## 5. Terminology Cross-Check

No new terms are introduced in this document beyond what `vocabulary.md` already defines. Where this document assigns a concrete ID format or file path to a term `vocabulary.md` only defined conceptually, that assignment is additive, not a redefinition.

---
**Binding scope**: T03 (UI Model schema), T04–T07 (generation skills), T08 (design document assembly), T09 (discussion/feedback) must all conform to Sections 1–4 above. Any deviation discovered during those tasks should be raised as a revision to *this* document, not silently implemented differently per-skill.

**See also**: `../Analysis/domain-concepts.md`, `../Analysis/domain-alignment.md`, `../../orgModel/02 - UI Prototype Skill Development Process/vocabulary.md`
