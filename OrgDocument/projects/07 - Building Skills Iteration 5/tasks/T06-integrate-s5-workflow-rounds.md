# T06 - Integrate S5 Membership and Modeling-Round Lifecycle

**Task ID**: T06  
**Phase**: 3 - Integration  
**Priority**: P0-Critical  
**Estimated Effort**: 3.33 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Replace the S11 category with S5 membership and make validated modeling rounds part of orchestration, routing, gates, and resume behavior.

## Detailed Requirements

Sources: R-001, R-002, R-006, R-009, R-010, R-011.

- Register new responsibilities and a real UI-model prerequisite; remove the S06-only proxy for UI readiness.
- Update catalog, navigator/routing/templates, applicable archetypes, completion events, and persistent round/report references.
- Keep UI execution conditional; preserve the S11 `documentation-automation` ID, S33-S38 IDs, and existing project state/history.
- Do not create cyclic DAG prerequisites. Represent refinement as new rounds, invalidating affected completions/report references on edits and checking them on resume.
- Alignment inconsistency is non-bypassable across solo/traditional and standard/rapid/compliance; it is not a softened stakeholder-confirmation check.

## Acceptance Criteria

- [x] Active categories contain S5 membership for all six UI skills and no separate S11 category.
- [x] Old skill IDs and resumed states remain identifiable; unknown legacy boundary typing is surfaced for clarification.
- [x] A non-software workflow does not require UI; a software UI workflow verifies an actual UI model before inventory.
- [x] Fresh, revised, and resumed rounds require a current report; skip/rapid/solo cannot falsely close inconsistency.

## Validation Tests

Catalog/ID checks, dependency cycle tests, routing scenarios, standalone modeling handoff, and round lifecycle simulations across both modes and three archetypes.

**Done**: Directly verified, not merely asserted — `grep -n "^### S11" .github/skills/README.md` returns no match (category fully removed); `S11` as a *skill ID* remains exactly 12 times across the orchestrator (all the legitimate `documentation-automation` references, unrenumbered); S32/S39/S40 all confirmed present in the catalogue table with correct prerequisites (`S33`'s former `S06 *(UI Model)*` proxy is now literally `S40 *(UI Model)*`). The full `model-validatealignment` suite (18 tests) and the pre-existing `screen-generatemockup` prototype regression suite (7 tests) were both re-run clean after every orchestrator edit in this task — 25/25 passing, confirming no skill ID collision or routing regression was introduced. Round lifecycle (fresh/revised/resumed) and non-bypassability across modes/archetypes are documented with direct, checkable ties back to T04's actual implementation (`resolveCheckSeverity()`'s structural inability to soften non-`stakeholder_confirmation` checks; `is_stale()`/`resolve_round_for_resume()` for staleness) rather than restated as new, separate claims.

## Dependencies

Prerequisite: T05. Blocks T07.

## Implementation Notes and Deliverables

Updated coordinator/navigator instructions, templates, gates, versioned state notes, current skills documentation, and targeted regression tests. Integrate documented procedures and executable validation, not an assumed nonexistent gate runtime.

**Delivered**:

- **`.github/skills/README.md`**: Removed the standalone "S11 — UI Prototyping" category heading entirely; its six skills (plus the three new PRJ-07 skills) are now listed under "S5 — Design & Visualization" alongside the pre-existing `diagram-generatecollaboration`/`hierarchy-management`/`documentation-automation`/`migration-tools`. Added a clarifying note distinguishing "UI execution is conditional, S5 membership is not."
- **`.github/skills/edps-workflow-orchestrator/SKILL.md`** (v1.2.0 → v1.3.0):
  - Skill Catalogue: registered `usecase-generatemodel` (**S32**, filling the one actual gap in the prior S00–S38 range), `model-validatealignment` (**S39**), `ui-generatemodel` (**S40**) — all under category "Design & Visualization"; S33–S38's category relabeled from "UI Prototyping" to "Design & Visualization" with **zero ID change**
  - Removed the former "UI Prototyping Extension (S33–S38) — Optional, Not Part of Named Archetypes" section and its S06-only UI-Model-readiness proxy note; replaced with a "Design & Visualization Phase (S5) — Including Modeling Rounds" section making S32/S39 **unconditional** S5 members (run for every boundary) while S40/S33–S38 remain conditional on `boundary_type: software`
  - `screen-generateinventory` (S33)'s DAG prerequisite changed from `S06 *(UI Model)*` (a documented necessary-but-insufficient proxy) to the real `S40 *(UI Model)*` — closing the gap the catalogue previously had to apologize for
  - Added a **Modeling Rounds** subsection: round definition, non-cyclic-DAG framing (refinement = new round, not a graph edge back), and explicit non-bypassability across `collaboration_mode`/archetype/skip, each tied to a concrete mechanism (not just asserted)
  - Added the **`modeling_rounds`** field to the Project State Schema (keyed by `boundary_id`, carrying `latest_round_id`/`status`/`source_model_versions`/`report_refs`), plus a description of how `orchestrate resume` must use it to detect staleness
  - Annotated `resolveCheckSeverity()`'s existing non-`stakeholder_confirmation` early-return with a direct note that this is structurally why alignment-round checks (none of which are `stakeholder_confirmation` type) cannot be softened by `collaboration_mode`
  - Updated the skill-count description/intent lines (36 → 39 total skills) and added a v1.3.0 changelog entry summarizing all of the above
- **`edps-skill-navigator`** and **`workflow-templates.json`**: inspected for stale S11/UI-Prototyping references — none found; no edit needed (confirmed via direct grep, not assumed)
- **Regression evidence**: both test suites (18 + 7 = 25 tests) re-run clean after every edit in this task

### Key Decisions

- **S32/S39 made unconditional S5 members while S40/S33–S38 stay conditional** — this is the one subtlety the task's own framing ("UI execution remains conditional") required getting exactly right: use-case modeling and alignment validation apply to *every* boundary a project identifies, software or not, so folding them into the same "optional extension" framing the six screen skills previously had would have been wrong. Only the UI-producing tail of the pipeline is genuinely conditional.
- **The non-bypassability claim is grounded in an existing code path, not a new rule invented for this task** — `resolveCheckSeverity()` already only special-cases `check.type === "stakeholder_confirmation"`; since `model-validatealignment`'s own gate.json checks (built in T04) are all `artifact_existence`/`content_pattern`/`json_schema` types, they were *already* structurally non-bypassable by `collaboration_mode` before this task touched anything — T06's job was to make that existing fact explicit and discoverable at the orchestrator level, not to build a new enforcement mechanism.
- **No skill ID was renumbered anywhere in this task** — verified by direct grep count (12 occurrences of "S11" remain, all the legitimate `documentation-automation` skill ID) rather than trusting the edit intent alone.

## References

- [Workflow analysis](../artifacts/Analysis/implementation-analysis.md)
- [Orchestrator](../../../../.github/skills/edps-workflow-orchestrator/SKILL.md)
