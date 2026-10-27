# T06 — Author screen-generatemockup Skill (Clickable HTML/JS)

**Task ID**: T06
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

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

- [x] SKILL.md authored
- [x] Generated mockup confirmed to open via `file://` on a real browser with zero setup
- [x] Clickable navigation between at least two generated screens confirmed working
- [x] No target-framework references found in generated output

## Dependencies

### Prerequisites
- **T05** — mockup renders the layout spec's content

### Blocks
- T07 (flow diagram must match mockup's actual transitions)
- T08 (design document references the mockup)
- T09 (discussion surface is built on the mockup)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/screen-generatemockup/SKILL.md`** (new, v1.0.0, skill_id S35): renders T05's layout-spec HTML/CSS into a standalone, clickable mockup. Key design points:
  - **Single self-contained file, no separate CSS/JS files** — CSS embeds in `<style>`, JS embeds in `<script>`, both inline in `mockup.html` itself. Justified explicitly: a single file has no relative-path dependencies that could break under an unpredictable `file://` working directory, and no risk of a stakeholder receiving `mockup.html` without its companion files if copied individually.
  - Step 2 explicitly instructs **flagging, not inventing**, a navigation target when no matching screen exists in the inventory — an inline HTML comment marks the gap rather than silently guessing a destination, consistent with the EDPS ambiguity-surfacing principle applied elsewhere (e.g., `process-w5h`'s clarifying-question pattern)
  - Step 3 explicitly prefers plain `<a href>` navigation over JS-driven navigation wherever possible — specifically because plain links are simpler for `screen-generateflow` (T07) to detect and verify against the flow diagram later
  - Step 4 (self-containment) is explicit about the image-asset edge case: omit with a labeled placeholder, or use an inline `data:` URI — never a path assuming a bundler/server
  - Step 5 and the Quality Checks both require the portability test to be **actually performed**, not assumed — matching TR-06.2 literally

- **`.github/skills/screen-generatemockup/gate.json`** (new, skill_id S35, confirmed unique): 5 checks — 4 hard content/existence checks, plus **`portability_tested`**, which reuses the existing `stakeholder_confirmation` gate check type (from Iteration 3/4) as a **self-verification mechanism** rather than inventing a new check type for "did you actually test this." This is the first UI Prototyping skill to use `stakeholder_confirmation`, and it's used here in an adapted sense: the "stakeholder" being confirmed against is the developer's own verification act (did you open the file in a browser), not a separate person's review — still self-attested in solo mode per the existing pattern, just applied to a QA-style check rather than a design-approval check.

- **`.github/skills/README.md`**: S11 section extended with `screen-generatemockup`'s row
- **`.github/skills/INDEX.md`**: skill count 34→35, version 2.3.0→2.4.0, new changelog entry noting the `stakeholder_confirmation` reuse as a self-verification pattern

### Key Decisions

- **Reused `stakeholder_confirmation` for portability testing** rather than inventing a new "self-test" gate check type — the existing mechanism's mode-aware severity (hard in traditional, soft/self-attested in solo) already does exactly what's needed here: in solo mode, the developer self-attests they tested it; the check still exists and is auditable, it just doesn't require a second person
- **Single-file mockup over separate CSS/JS files** — the more conventional web-dev file split was explicitly rejected in favor of inline embedding, purely for portability robustness under `file://`, which is a harder constraint here than typical web development where a local server is assumed
- **Explicit gap-flagging over silent link invention** — when Step 2 can't find a matching screen for an implied navigation target, the skill is instructed to leave visible evidence of the gap (an HTML comment) rather than making something up, so a human reviewing the mockup can actually find and fix it

### Next Steps for Integration

- **T07** (`screen-generateflow`): must read this skill's actual `<a href>` targets (not the layout spec's intent, which may differ slightly after Step 2's gap-flagging) as the ground truth for its consistency check
- **T10**: must register `screen-generatemockup` (S35) in the orchestrator's DAG with a prerequisite on `screen-generatelayout`, and ensure the `stakeholder_confirmation`-based `portability_tested` check resolves correctly against the project's `collaboration_mode`
