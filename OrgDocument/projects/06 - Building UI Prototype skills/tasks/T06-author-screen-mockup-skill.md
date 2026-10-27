# T06 — Author screen-generatemockup Skill (Clickable HTML/JS)

**Task ID**: T06
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Implements R-602a (Literal Interactive Mockup) and R-626 (Mockup Portability) — the second of the two explicitly requested artifacts: "a literal interactive HTML/JS mockup... clickable, not just specified." This is the artifact the user wants to actually discuss requirements/ideas/designs against with stakeholders.

## Objectives

- Author the mockup generation skill producing a standalone, `file://`-openable HTML/JS mockup per screen
- Render what T05's LayoutSpec describes, with genuine clickable navigation

## Detailed Requirements

### Functional Requirements
- **FR-06.1**: Generated mockup opens directly via `file://` with zero build step, package manager, or server
- **FR-06.2**: Mockup is genuinely clickable — real navigation between generated screens' mockup files, not a static render

### Technical Requirements
- **TR-06.1**: No references to a specific target framework (React/Vue/etc.) anywhere in generated output (R-625)
- **TR-06.2**: Portability must be tested on at least one real browser, not just assumed to work

## Acceptance Criteria

- [ ] SKILL.md authored
- [ ] Generated mockup confirmed to open via `file://` on a real browser with zero setup
- [ ] Clickable navigation between at least two generated screens confirmed working
- [ ] No target-framework references found in generated output

## Dependencies

### Prerequisites
- **T05** — mockup renders the layout spec's content

### Blocks
- T07 (flow diagram must match mockup's actual transitions)
- T08 (design document references the mockup)
- T09 (discussion surface is built on the mockup)
