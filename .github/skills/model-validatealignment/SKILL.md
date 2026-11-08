---
name: model-validatealignment
description: Owns the single cross-model entity/system-boundary alignment contract shared by the use-case model, UI model, domain model, and process model. Validates alignment at the end of every modeling round, reports PASS, NEEDS_CLARIFICATION, or INVALID_INPUT with item-level evidence, and requests clarification for unresolved inconsistencies rather than treating them as aligned. This skill does not generate use-case or UI models itself — see usecase-generatemodel and ui-generatemodel.
license: MIT
version: 0.1.0
---

# Model Validate Alignment

Owns the shared cross-model alignment contract and the end-of-round validation that checks the domain, process, use-case, and UI models actually agree on the entities and system boundaries they jointly reference.

## Status

**T01 deliverable (this file + its references/fixtures/scripts) is complete.** The full generation-time validator that parses real project file trees is scope for this skill's own later build-out task, not T01. T01's job was to define and prove the shared contract (`references/cross-model-alignment-contract.md`) and ship a deterministic, executable validator skeleton (`scripts/alignment_validator.py`) proven against five fixtures (`scripts/test_alignment_contract.py`, all passing).

## Intent

Per the confirmed decisions in PRJ-07's `requirements.md`: entities and system boundaries are the shared alignment contract across UI, use-case, domain, and process models (R-008). Validation runs at the end of every modeling round (R-009). Unresolved inconsistencies are reported for clarification, never silently treated as aligned (R-010).

This skill is the **single owner** of that validation — `usecase-generatemodel` and `ui-generatemodel` produce model content; they do not self-certify alignment. This mirrors `hierarchy-validation`'s own exclusive-ownership pattern for structural/cross-level checks (this skill does not duplicate or replace those checks — see Reuse, below).

## The Shared Contract

**Read in full**: [`references/cross-model-alignment-contract.md`](references/cross-model-alignment-contract.md)

That document is authoritative for:
- Shared reference shapes (Scoped Entity Reference, System Boundary Reference, Actor Reference) and their single-ownership rule
- Boundary typing (`software` | `non-software` | `unknown`) — explicit, never inferred; UI applicability gating (R-011)
- Use-case model/script schema that `usecase-generatemodel` must produce
- The modeling-round contract: scope, round report schema, PASS/NEEDS_CLARIFICATION/INVALID_INPUT semantics, non-bypassable completion, revision invalidation, clarification/revalidation
- File/folder layout additions (additive to existing conventions, not a competing layout)
- Compatibility notes for `ui-generatemodel` and the six existing `screen-*` skills (S33–S38) — no schema changes required there

## Reuse — What This Skill Does NOT Reimplement

- **Hierarchy/file/link structural integrity**: owned exclusively by `hierarchy-validation` (HV/HX/HN rules). This skill's boundary references annotate the same hierarchy tree; it does not re-derive or duplicate structural checks.
- **Diagram-level boundary stereotype classification and VR-1–VR-4 rules**: owned exclusively by `diagram-generatecollaboration`. This skill's `boundary_type` (software/non-software/unknown) is an independent axis from a diagram's `boundary`/`control`/`actor`/`entity` stereotype — see the contract's Section 1.2/2.1 for the precise, non-conflated relationship.
- **UIModel/UIModelEntry/Aggregation schema**: owned by the existing D-02 domain model (PRJ-06). This skill validates references *into* that schema; it does not redefine it.
- **Stakeholder-confirmation gate severity resolution**: explicitly **not** reused for alignment completion (contract Section 4.4). Model inconsistency is a factual, checkable property of the artifacts, independent of `collaboration_mode` or workflow archetype leniency.

## Inputs

- The boundary(ies) in scope for the current modeling round (a `boundary_scope` list, per contract Section 4.2)
- The current content of each in-scope boundary's `domain-model.md`, `process.md`, `use-case-model.json`, and (where applicable) `ui-model.json`
- The prior round's report, if any, for staleness checking (contract Section 4.4)

## Outputs

- `artifacts/Analysis/alignment-report-[round-id].md` (and its JSON companion) — contract Section 4.2's schema, never overwriting a prior round's report
- A `PASS` / `NEEDS_CLARIFICATION` / `INVALID_INPUT` status with item-level findings and, where applicable, specific clarification questions

## Quality Checks

- [ ] Every finding resolves against the *actual* referenced document content, not merely a well-formed reference shape (see the manifest-source-disagreement fixture)
- [ ] `unknown` boundary type is never defaulted to `software` or `non-software` in any code path
- [ ] A `software` boundary with zero UIModelEntries is never reported as a finding (see the software-boundary-no-ui-required fixture)
- [ ] A round cannot be marked `PASS` without an actual validator run against current artifacts — no solo-mode or rapid-archetype bypass applies here

## Fixtures and Proof

See [`fixtures/`](fixtures/) for five worked scenarios (three-level-valid, unknown-boundary-type, missing-applicable-model, manifest-source-disagreement, software-boundary-no-ui-required), each with a `scenario.md` and an `expected-report.json`. [`scripts/test_alignment_contract.py`](scripts/test_alignment_contract.py) runs the validator skeleton against all five and asserts the documented outcome — run `python3 -m unittest test_alignment_contract -v` from `scripts/` to reproduce (all 8 tests pass as of this writing).

## Integration

**Upstream**: `usecase-generatemodel` (use-case model/scripts), `ui-generatemodel` (UI model), `domain-extractconcepts`/`domain-alignentities` (domain model), `hierarchy-management` (boundary structure, hierarchy metadata)

**Downstream**: `edps-workflow-orchestrator` (round-report persistence in project state, staleness checks on resume), the screen-generation pipeline (consumes a validated UI model, unchanged)

**Typical pipeline** (per the Implementation Analysis's Workflow Integration):
```
Requirements + domain concepts
  -> collaboration/hierarchy and boundary identification
  -> scoped domain/process documents
  -> usecase-generatemodel
  -> ui-generatemodel (software boundary with UI requirements only)
  -> model-validatealignment (end-of-round)
  -> screen inventory -> layout -> mockup -> verified flow -> handoff/feedback
  -> any model-affecting feedback starts a new round and revalidation
```
