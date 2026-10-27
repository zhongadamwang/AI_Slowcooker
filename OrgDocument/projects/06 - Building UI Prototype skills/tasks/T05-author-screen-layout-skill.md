# T05 — Author screen-generatelayout Skill (Markdown + HTML/CSS)

**Task ID**: T05
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

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

- [ ] SKILL.md authored
- [ ] Given a screen inventory entry, produces a LayoutSpec with real (not placeholder) HTML/CSS
- [ ] Changelog stub present in every generated LayoutSpec
- [ ] Traceability fields populated correctly

## Dependencies

### Prerequisites
- **T04** — needs a screen inventory to iterate over

### Blocks
- T06 (mockup renders what the layout spec describes)
