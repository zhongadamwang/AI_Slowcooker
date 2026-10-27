# T05 — Author screen-generatelayout Skill (Markdown + HTML/CSS)

**Task ID**: T05
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Implements R-602 (Layout Specification with Embedded Implementation Code) — one of the two artifacts the user explicitly asked for: "generate a set of UI design documents that can be used for future development." This is the core "hard problem" of the skill set — generating literal, implementation-ready HTML/CSS, not descriptive placeholders.

## Objectives

- Author the layout generation skill producing one `LayoutSpec` (Markdown + embedded HTML/CSS) per screen in the inventory
- Include an in-document changelog stub per R-610

## Detailed Requirements

### Functional Requirements
- **FR-05.1**: Generated HTML/CSS is literal and usable, not placeholder/descriptive text
- **FR-05.2**: Each LayoutSpec includes an in-document changelog section stub, ready for future iteration entries
- **FR-05.3**: Each LayoutSpec traces to its Screen's `requirement_refs` and `ui_model_ref`

### Technical Requirements
- **TR-05.1**: Output format and location follow T02's conventions

## Acceptance Criteria

- [x] SKILL.md authored
- [x] Given a screen inventory entry, produces a LayoutSpec with real (not placeholder) HTML/CSS
- [x] Changelog stub present in every generated LayoutSpec
- [x] Traceability fields populated correctly

## Dependencies

### Prerequisites
- **T04** — needs a screen inventory to iterate over

### Blocks
- T06 (mockup renders what the layout spec describes)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/screen-generatelayout/SKILL.md`** (new, v1.0.0, skill_id S34): the core "hard problem" skill — first point in the pipeline where abstract requirements/UI-Model data becomes a concrete, renderable design. Key design points:
  - LayoutSpec's output is **Markdown with embedded HTML/CSS directly**, not a separate JSON companion — unlike ScreenInventory/UIModel, R-602 calls for a Markdown artifact and HTML/CSS naturally embeds as fenced code blocks, so a parallel JSON representation would be redundant for this entity type specifically
  - Step 1 explicitly uses the referenced `UIModelEntry`'s `domain_entity_refs`/`aggregation_description` to determine *what content* a screen needs (e.g., a screen aggregating Order+Customer+LineItem needs sections for each), rather than generating a generic layout
  - Step 4 (Design Rationale) explicitly marked **best-effort** in MVP, consistent with `scope-analysis.md`'s classification of R-609 as an Enhancement (Phase 2) feature, not Core — a LayoutSpec without rich rationale is still valid; this step must not block generation
  - Step 5 makes the changelog **unconditional from first generation** ("v1.0: Initial generation"), not something added only on a later revision — matches T02's checklist literally
  - Quality Checks include an explicit **literalness scan** for placeholder language (TODO, "content here", Lorem ipsum, "[insert...]") and a **framework-leakage check** (no JSX/Vue SFC/Angular directives), both made concrete and checkable rather than left as prose guidance
  - Mockup portability explicitly noted as **not applicable** to this skill's own output (layout-spec.md isn't itself `file://`-opened) — correctly scoped to T06 instead, avoiding a checklist item this skill can't actually satisfy

- **`.github/skills/screen-generatelayout/gate.json`** (new, skill_id S34, confirmed unique): 6 checks — 4 hard (`layout_spec_exists`, `no_placeholder_content`, `no_framework_leakage`, `changelog_present`, `traceability_preserved` — 5 actually, all hard except the last), 1 soft (`id_format_valid`). The `no_placeholder_content` and `no_framework_leakage` checks directly encode the SKILL.md's own literalness/framework-leakage quality checks as automatable gate patterns, not just prose guidance left to the author's discretion.

- **`.github/skills/README.md`**: S11 section extended with `screen-generatelayout`'s row
- **`.github/skills/INDEX.md`**: skill count 33→34, version 2.2.0→2.3.0, new changelog entry

### Key Decisions

- **No separate JSON output for LayoutSpec** — a deliberate asymmetry from `screen-generateinventory`'s Markdown+JSON pair, justified because R-602 is explicitly a Markdown-with-embedded-code artifact; a parallel JSON file would just be a lossy re-serialization of the same HTML/CSS strings, adding maintenance surface without real downstream consumer need (unlike ScreenInventory/UIModel's JSON, which genuinely serves distinct machine-processing needs)
- **Gate checks encode the same literalness/framework-leakage concerns as the SKILL.md's own Quality Checks section**, turning prose guidance into regex-checkable patterns — keeps the gate meaningfully enforcing the skill's actual quality bar rather than only checking file existence
- **Explicitly deferred Design Rationale rigor to Phase 2**, consistent with `scope-analysis.md`'s own classification, rather than quietly treating it as mandatory in this skill's acceptance bar

### Next Steps for Integration

- **T06** (`screen-generatemockup`): consumes this skill's `layout-spec.md` HTML/CSS directly to produce the clickable, standalone mockup; must inherit the same literalness and no-framework-leakage constraints, plus add the mockup-portability (`file://`) constraint this skill explicitly didn't need to satisfy
- **T10**: must register `screen-generatelayout` (S34) in the orchestrator's DAG with a prerequisite on `screen-generateinventory`
