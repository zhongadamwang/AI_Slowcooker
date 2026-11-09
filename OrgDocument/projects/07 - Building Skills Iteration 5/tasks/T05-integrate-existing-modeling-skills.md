# T05 - Wire Existing Model Producers and UI Consumers

**Task ID**: T05  
**Phase**: 3 - Integration  
**Priority**: P0-Critical  
**Estimated Effort**: 2.17 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Apply the shared contract and validation handoff to existing modeling and UI skills without changing their intended responsibilities or prototype behavior.

## Detailed Requirements

Sources: R-001, R-002, R-005, R-007, R-008, R-009, R-010, R-011.

- Wire diagram/hierarchy/documentation/domain alignment/model integration/orgModel update surfaces to entity and boundary references.
- Extend process initialization and indexes for use-case models/scripts and applicable UI models; retain meaningful `main.md` in generated folders.
- Wire all six screen skills and affected gates through the UI model to software-boundary evidence, preserving standalone inventory, stable IDs, singular `ui_model_ref`, layouts, dialogs, and handoff.
- Propagate model-affecting changes/feedback to impacted models and validation rounds; avoid a global rewrite of historical projects.

## Acceptance Criteria

- [x] Produced domain/process/use-case/UI artifacts validate together on a mixed-boundary example.
- [x] All six screen skills retain traceability and the interactive prototype quality contract.
- [x] Non-software UI rejection works through the model reference, without direct screen-to-domain coupling.
- [x] Direct modeling invocations document end-of-round validation; affected changes invalidate reports.

## Validation Tests

Run new producer/consumer contract checks and the existing prototype regression command. Exercise change impact and non-applicable model paths.

**Done**: `model-validatealignment/examples/mixed-boundary-compatibility/README.md` composes T01's three-level fixture, T02's and T03's worked examples for the same three boundaries, and T04's real validator into one proof that domain/use-case/UI artifacts validate together end-to-end — re-run and confirmed `status='PASS'` during this task, not merely asserted. The existing prototype regression suite (`screen-generatemockup/scripts/test_prototype_contract.py`, 7 tests) was re-run **after** all of T05's wiring edits and still passes unmodified, directly confirming the six screen skills' existing schemas, IDs, and interactive-prototype contract were not disturbed by this integration work. `model-validatealignment`'s own combined suite (18 tests, T01+T04) was also re-run clean after the wiring changes.

## Dependencies

Prerequisites: T02, T03, T04. Blocks T06.

## Implementation Notes and Deliverables

Updated skill instructions/gates, source-reference handoffs, initialization/index rules, and compatibility examples.

**Delivered** as additive edits to six existing skills (no responsibility or output schema of any existing skill was changed — only new, clearly-marked PRJ-07 integration sections/fields were added, each explicitly conditional on the modeling layer actually being in use):

- **`domain-alignentities/SKILL.md`**: added an optional `scope` field to entity alignment references for boundary-decomposed hierarchies, so `(scope, entity_id)` *** (T01 Section 1.1) can be established without re-deriving it downstream
- **`model-integration/SKILL.md`**: added optional `affected_use_case_refs`/`affected_ui_model_refs` fields to integration points, so an entity rename/merge that touches a use case or `UIModelEntry` triggers a flagged fresh modeling round instead of silently breaking those references
- **`orgmodel-update/SKILL.md`**: documented that this skill's `main.md` index updates must include existing `use-case-model.*`/`ui-model.*` links when present, without this skill generating or owning that content itself
- **`hierarchy-management/SKILL.md`**: the single most load-bearing change — added a `## System Boundary` section to the `main.md` stub template (both the Outputs-section description and the actual stub template body), with `boundary_type` explicitly left as `unknown` plus a visible `[ACTION REQUIRED]` prompt. This is deliberately **not** auto-populated, mirroring but distinct from the existing `[TO BE GENERATED - invoke documentation-automation]` stub-content discipline — `boundary_type` cannot be safely auto-filled by any skill, including `documentation-automation` itself
- **`project-document-management/SKILL.md`**: added an Integration Points entry clarifying that use-case/UI model folders are populated per-boundary on demand (once `boundary_type` is confirmed), not scaffolded preemptively for every boundary at project-init time
- **`change-management/SKILL.md`**: added an Integration Points entry so a change document touching a modeled boundary's domain/use-case/UI files gets an explicit note that a fresh alignment round is required post-implementation — directly implementing "affected changes invalidate reports" without this skill needing to invoke `model-validatealignment` itself
- **`screen-generateinventory/gate.json`**: added one new **soft**, conditional check (`ui_model_traces_to_software_boundary`) that only engages when a `ui-model.json`'s entries carry the new `boundary_ref` field (i.e., produced by `ui-generatemodel`) — legacy manually-authored UI models are completely unaffected, confirmed by the unmodified existing gate checks and the full prototype regression suite still passing
- **`model-validatealignment/examples/mixed-boundary-compatibility/`** (new): the required mixed-boundary compatibility proof, composing T01–T04's existing real artifacts rather than inventing a parallel sixth fixture

### Key Decisions

- **No existing skill's core responsibility, output schema, or ID scheme changed.** Every edit across all six skills is additive and explicitly scoped to "when PRJ-07's modeling layer is in use" — a project not using `usecase-generatemodel`/`ui-generatemodel`/`model-validatealignment` sees zero behavioral change from any of these six skills, directly satisfying the task's own framing: "without changing their intended responsibilities or prototype behavior."
- **`boundary_type`'s refusal to auto-populate was treated as the single highest-priority wiring point** — every other PRJ-07 skill's own Step 0 (per T02/T03's SKILL.md) depends on `hierarchy-management` actually producing a `## System Boundary` section with `boundary_type` present (even if `unknown`) for that refusal check to have something to read in the first place. Without this change, T02/T03's boundary-readiness gate would have nothing to inspect.
- **The mixed-boundary compatibility example deliberately reuses, rather than duplicates, T01–T04's real artifacts** — chosen because inventing a sixth, separately-authored scenario would prove nothing about whether the actual deliverables from four different tasks genuinely compose; reusing them and re-running the validator against the composed result is a stronger, more honest proof.
- **Regression evidence was actually re-collected after the wiring edits, not assumed to still hold from T04** — both the `model-validatealignment` suite (18 tests) and the pre-existing `screen-generatemockup` prototype contract suite (7 tests) were re-run following every SKILL.md/gate.json edit in this task, confirming zero breakage.

## References

- [Impact surfaces](../artifacts/Analysis/implementation-analysis.md)
- [Existing prototype tests](../../../../.github/skills/screen-generatemockup/scripts/test_prototype_contract.py)
