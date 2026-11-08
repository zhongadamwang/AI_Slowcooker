# T01 - Define Entity, Boundary, and Modeling-Round Contracts

**Task ID**: T01  
**Phase**: 1 - Foundation  
**Priority**: P0-Critical  
**Estimated Effort**: 2.00 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Define one minimal cross-model contract before implementing producers and validation. Reuse existing entity IDs, hierarchy metadata, UIModelEntry aggregation, and artifact ownership.

## Detailed Requirements

Sources: R-002, R-005, R-007, R-008, R-009, R-010, R-011.

- Define scoped entity and system-boundary references, explicit software typing, actor roles relative to a boundary, cross-level mappings, source/version references, and model applicability.
- Specify use-case model/script and UI-model extensions, artifact locations resolved from metadata, and source-backed alignment manifest/report formats.
- Define round scope, revision invalidation, clarification/revalidation, and non-bypassable alignment completion. Do not conflate boundary type with participant stereotype.
- Preserve existing screen IDs, singular `ui_model_ref`, and VR/HR authority; do not require identical entities at every hierarchy level.

## Acceptance Criteria

- [x] Shared contract documents all fields, ownership, applicability, and compatibility rules with valid positive/negative fixtures.
- [x] Three-level fixture includes a non-software parent, software child, and scoped entity-name collision.
- [x] Unknown boundary type, missing applicable model, and source/manifest disagreement have explicit failure/clarification outcomes.
- [x] New responsibility-based names and unused skill IDs are selected without renumbering S11 or S33-S38.

## Validation Tests

Validate fixture schemas/references and demonstrate that boundary stereotype alone cannot authorize UI. Document how references are checked against actual model artifacts.

**Done**: `scripts/test_alignment_contract.py` runs a deterministic validator skeleton against all 5 fixtures; all 8 tests pass (`python3 -m unittest test_alignment_contract -v` from `scripts/`). The manifest-source-disagreement fixture and its paired `test_naive_shape_only_check_would_have_missed_this` test specifically prove references are checked against actual document content, not merely well-formed shape.

## Dependencies

Prerequisites: none. Blocks T02, T03, T04.

## Implementation Notes and Deliverables

Shared modeling contract reference under the responsible skill, schema/examples, applicability table, and compatibility notes. No new generic modeling repository or gate service.

**Delivered** under `.github/skills/model-validatealignment/`:

- `references/cross-model-alignment-contract.md` — the shared contract itself: Scoped Entity Reference, System Boundary Reference, Actor Reference (Section 1); boundary typing with explicit-never-inferred declaration and the UI applicability gate (Section 2); use-case model/script schema (Section 3); the modeling-round contract with PASS/NEEDS_CLARIFICATION/INVALID_INPUT semantics and non-bypassable completion (Section 4); additive file/folder layout (Section 5); compatibility notes for `ui-generatemodel` (Section 6) and the six existing `screen-*` skills (Section 7); the Skill ID Ledger (S32/S39/S40, preserving S11 and S33-S38)
- `fixtures/three-level-valid/` — non-software root → software child → software grandchild, with a deliberate `E-002` entity-ID collision between root and child resolved via `(scope, entity_id)` identity
- `fixtures/unknown-boundary-type/` — undeclared `boundary_type`, with both a use case and an attempted UIModelEntry against it; resolves to `NEEDS_CLARIFICATION`, never a silent default
- `fixtures/missing-applicable-model/` — a software boundary with no use-case model at all; resolves to `INVALID_INPUT`, not a silent not-applicable skip
- `fixtures/manifest-source-disagreement/` — a use-case model claiming an entity is `defined_in` a domain-model.md that does not actually contain it; resolves to `INVALID_INPUT`, proving real document resolution rather than manifest trust
- `fixtures/software-boundary-no-ui-required/` — a software boundary with real use cases but zero UIModelEntries; resolves to `PASS`, proving R-011's "software boundaries do not automatically require a screen" is honored
- `scripts/alignment_validator.py` — deterministic validator skeleton implementing the contract's Section 4.3 decision logic
- `scripts/test_alignment_contract.py` — 8 passing tests proving all 5 fixtures resolve as documented
- `SKILL.md` + `gate.json` (skill ID **S39**) — skill definition and a 7-check gate (6 hard, 1 soft), all checks verified passing against the delivered content

### Key Decisions

- **Boundary typing is a declared field in `main.md`, never inferred** — the single most load-bearing decision in this contract, directly implementing T01's explicit instruction not to conflate boundary type with participant stereotype. `corresponds_to_participant` is optional specifically so a real-world non-software boundary (no diagram presence at all) and a software boundary (which may or may not be a decomposed `control`-type participant) are both representable without forcing a stereotype mapping that doesn't exist.
- **Skill ID Ledger fills the one real gap (S32) before extending past S38** — confirmed via direct inspection of the orchestrator's full S00–S38 catalogue table (only S32 was unused); `usecase-generatemodel` takes S32, `model-validatealignment` takes S39, `ui-generatemodel` (T03's scope) is reserved S40.
- **Alignment completion explicitly excludes `stakeholder_confirmation`/solo-mode/rapid-archetype leniency** (contract Section 4.4) — a deliberate, explicit carve-out from the existing `resolveCheckSeverity()` pattern elsewhere in the framework, because model inconsistency is a factual property of the artifacts, not a stakeholder-satisfaction judgment.
- **A working, tested Python validator skeleton was built now, not deferred** — even though the full generation-time file-tree parser is explicitly scoped to a later task, proving the contract's decision table is actually implementable (not just plausible-sounding prose) was judged necessary to satisfy the Validation Tests requirement for *this* task.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [Requirements](../artifacts/Analysis/requirements.md)
