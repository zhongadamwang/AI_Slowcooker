# Requirement Coverage Matrix

**Project**: PRJ-07 — Building Skills Iteration 5
**Purpose**: Demonstrate all 11 requirements (R-001–R-011) against the integrated framework, each with linked, actually-executed passing evidence — not merely a claim of coverage.
**Generated**: 2026-11-08

## Coverage Summary

**11/11 requirements have linked, passing evidence. No unresolved inconsistency is anywhere labeled "aligned."**

| ID | Requirement | Implementing Task(s) | Evidence |
|---|---|---|---|
| R-001 | Integrate the existing UI Prototype skills into S5 - Design & Visualization | T06 | `.github/skills/README.md`'s S5 table lists all six `screen-*` skills alongside `diagram-generatecollaboration`/`hierarchy-management`/`documentation-automation`/`migration-tools` and the three new PRJ-07 skills. Direct grep confirms zero standalone `### S11` category heading remains. |
| R-002 | Treat the UI model as a modeling artifact within the design workflow, not merely a prototype output | T01, T03, T05, T06 | `cross-model-alignment-contract.md` Section 1.4's Ownership Rule table lists `UIModelEntry` as a first-class reference type alongside domain/process/use-case entities; `ui-generatemodel`'s workflow (T03) treats the UI model as *derived from and validated against* the use-case/domain models, not an independent prototype artifact; `model-integration`/`change-management` (T05) both treat UI-model-affecting edits as triggering a fresh modeling round, the same discipline applied to domain/process models. |
| R-003 | Create a use-case skill that builds a use-case model | T02 | `usecase-generatemodel/SKILL.md` + the three-level worked example (`examples/three-level-worked-example/`) — 6 real use cases across 3 boundaries, each with identifiable actors (`A-001`/`A-002`), goals, boundary scoping, and `requirement_refs`. |
| R-004 | The use-case skill shall produce use-case scripts describing the detailed process for each modeled use case | T02 | Every one of the 6 use cases in the worked example has a linked script (`UC-[###]-[slug].md`) with Trigger/Preconditions/Main Flow/Postconditions, and — where applicable — Alternative/Exception Paths (UC-002 at BND-ROOT). Verified by direct gate check (`every_use_case_has_linked_script`). |
| R-005 | Keep the UI model, use-case model, domain model, and process model aligned | T01, T03, T04, T05 | The full chain — [mixed-boundary-compatibility](../../../../../.github/skills/model-validatealignment/examples/mixed-boundary-compatibility/README.md) (T05) — composes real domain/use-case/UI artifacts across 3 boundaries and confirms `status='PASS'` via `run_fixtures.py`'s `three-level-valid` run, re-confirmed during T07. |
| R-006 | Replace S11 - UI Prototyping as a separate category with membership in S5 - Design & Visualization | T06 | Same evidence as R-001. Historical PRJ-06 task records were **not** rewritten, per the requirement's own "Historical records need not be rewritten" note — only the active catalog (`README.md`, `edps-workflow-orchestrator/SKILL.md`) changed. |
| R-007 | Use cases shall describe actor interactions with an identified system boundary at every hierarchy level where such a boundary exists | T02 | The three-level worked example's root boundary (non-software, Level 0) has 2 full use cases with real scripts — demonstrated explicitly as *not* a thinner treatment than the software boundaries, per the worked example's own README.md point #1. |
| R-008 | Use entities and system boundaries as the alignment contract across UI, use-case, domain, and process models | T01, T02, T03, T04, T05 | `cross-model-alignment-contract.md` Section 1 (Scoped Entity Reference, System Boundary Reference) is the single shared shape every one of T02/T03/T04's skills imports and uses; the `three-level-valid` fixture's deliberate `E-002` entity-***-collision resolving correctly via `(scope, entity_id)` is the concrete proof this contract is load-bearing, not decorative. |
| R-009 | Perform model-alignment validation at the end of every modeling round | T01, T04, T05, T06 | `model-validatealignment`'s `validate_round()` (T01/T04) is the sole producer of round status; T06's orchestrator integration documents `S39` as mandatory at the end of every S5 round, with `modeling_rounds` project-state tracking. |
| R-010 | Request clarification for unresolved model inconsistencies rather than treating them as aligned | T01, T04, T06 | `unknown-boundary-type` fixture → `NEEDS_CLARIFICATION` with a specific question, never `PASS`; non-bypassability structurally proven (`inspect.signature` test on `resolve_round_for_resume`, T04) and independently confirmed at the orchestrator level (`resolveCheckSeverity()`'s `stakeholder_confirmation`-only branch, T06). See [negative-examples/README.md](../../../Testing/worked-example/negative-examples/README.md) item 6. |
| R-011 | UI screens shall exist only within software-type boundaries | T01, T03, T04, T05, T06 | `three-level-valid` fixture's non-software `BND-ROOT` has zero `UIModelEntry`s (with a `generation_note` explaining why, T03); `software-boundary-no-ui-required` fixture proves the converse (a software boundary *legitimately needing zero* UI entries is not flagged as a defect) — both halves of R-011 ("only within software" AND "not every software boundary needs one") are demonstrated, not just the first half. |

## "No Unresolved Inconsistency Is Labeled Aligned" — Direct Proof

This is the single most important claim in T07's acceptance criteria, so it is proven here explicitly rather than left implicit in the table above:

- Every fixture that should produce `NEEDS_CLARIFICATION` or `INVALID_INPUT` **actually does**, confirmed by `run_fixtures.py`'s real execution (re-run during T07, see `evidence-log.md`), not merely by an `expected-report.json` file existing.
- The one case that could *in principle* be gamed — converting a `NEEDS_CLARIFICATION`/`INVALID_INPUT` round into a false `PASS` via a mode or archetype override — was tested at the function-signature level (`test_a_skip_or_self_attestation_cannot_fabricate_a_valid_resume`) specifically because this is the failure mode most worth structurally ruling out, not just documenting against.

## Release Acceptance Cross-Check

Per the Implementation Analysis's Release Acceptance section:

> "Demonstrate at least three levels including a non-software parent and software child, plus a software boundary without UI." → ✅ three-level-valid fixture (T01) + its reuse across T02/T03/T05's worked examples.
>
> "Validate fresh/revised/resumed rounds, entity conflicts, boundary conflicts, unknown typing, unresolved clarification, and stale reports." → ✅ see [negative-examples/README.md](../../../Testing/worked-example/negative-examples/README.md), all six categories.
>
> "Prove all 11 requirements have passing evidence and preserve the current UI interaction contract." → ✅ this matrix (11/11) + [browser-verification-report.md](../../../Testing/worked-example/child-software-boundary/UI%20Prototype/browser-verification-report.md) (real DOM interaction, honestly scoped against what visual rendering was/wasn't confirmed) + the existing `screen-generatemockup` prototype regression suite (7/7, re-run unmodified after all PRJ-07 integration work).

---
**See also**: [evidence-log.md](evidence-log.md) for the full re-run transcript of every test suite referenced above
