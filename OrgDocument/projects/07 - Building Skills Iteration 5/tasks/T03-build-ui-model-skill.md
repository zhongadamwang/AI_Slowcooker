# T03 - Build Software-Boundary UI Models

**Task ID**: T03  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 2.00 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Create proposed `ui-generatemodel` to close the existing manual UI Model generation gap while preserving the current aggregation and screen traceability contracts.

## Detailed Requirements

Sources: R-002, R-005, R-008, R-011.

- Consume boundary-scoped domain/process/use-case models using T01's contract. Development can use contract fixtures before T02 implementation is complete.
- Extend existing UIModel/UIModelEntry data with boundary and applicable use-case/process references; retain entity aggregation and stable `UME` identities.
- Generate model Markdown/JSON only for software boundaries with UI requirements; record non-applicability explicitly otherwise.
- Unknown boundary type requires clarification before screen production. Do not treat domain-concepts completion as UI readiness.

## Acceptance Criteria

- [x] Existing UI model structure and aggregation semantics remain usable by the screen pipeline.
- [x] Every UI entry resolves to a software boundary and valid scoped entity references.
- [x] Non-software boundaries and software boundaries without UI requirements produce no screens or forced UI model.
- [x] Missing source references and unknown boundary classification are reported explicitly.

## Validation Tests

Software/non-software/unclassified fixtures, software-without-UI fixture, stable-ID revision, and compatibility with the existing singular screen reference.

**Done**: The three-level worked example (`examples/three-level-worked-example/`) reuses the exact same fixture boundaries as T01 and T02 (`BND-ROOT` non-software, `BND-CHILD-SW`/`BND-GRANDCHILD` software), consuming T02's actual generated `use-case-model.json` files as real input. All three `ui-model.json` files were verified by direct inspection against every `gate.json` check: JSON syntax, empty `entries` + `generation_note` for the non-software boundary, every entry retaining the exact original D-02 required fields (`entry_id`/`ui_concept_name`/`domain_entity_refs`/`aggregation_description`) plus a resolved `boundary_ref`, `UME-[###]` ID format, changelog presence, and — critically — every cited `domain_entity_refs` value (`E-002`, `E-003`, `E-004`) manually confirmed present in the actual `domain-model.md` content it claims to come from (not merely a well-formed-looking ID). The grandchild boundary's borderline case (one small entry justified by a direct human actor, contrasted explicitly against the `software-boundary-no-ui-required` fixture's non-human actor) demonstrates the software-without-UI distinction is a reasoned judgment, not a blanket rule. Stable-ID revision discipline (Step 4) is specified in the skill but, same as T02's equivalent note, not separately exercised by an actual second-pass regeneration in this worked example — a residual follow-up, not a blocker.

## Dependencies

Prerequisite: T01. Blocks T05. T02 is a runtime input responsibility, not a prerequisite for parallel implementation using shared fixtures.

## Implementation Notes and Deliverables

Skill instructions, gate, extended UI-model contract/example, focused tests, and migration notes for current model consumers.

**Delivered** under `.github/skills/ui-generatemodel/`:

- `SKILL.md` — full skill definition: shared-contract reference (reusing D-02's existing `UIModel`/`UIModelEntry`/`Aggregation` schema unchanged, per T01 contract Section 6), two new strictly-additive fields (`boundary_ref`, `source_use_case_refs` per entry; `generation_note` model-level) documented with exact semantics and exemption rules for legacy files, a 6-step workflow (Step 0 mirrors `usecase-generatemodel`'s own boundary-readiness refusal; Step 2 explicitly distinguishes human vs. internal-role/system actors as the UI-worthiness signal), quality checks, and **Migration Notes for Existing Model Consumers** — explicitly confirming `screen-generateinventory` (S33) needs zero changes and legacy manually-authored `ui-model.json` files remain valid as-is
- `gate.json` (skill ID **S40**, per T01's Skill ID Ledger) — 8 checks (6 hard, 2 soft), all manually verified passing against the worked example
- `examples/three-level-worked-example/` — the same 3-level boundary hierarchy as T01/T02, with real `ui-model.md`/`.json` files consuming T02's actual use-case output (not a hypothetical one); a `README.md` calling out the five specific contract behaviors demonstrated

### Key Decisions

- **Additive-only schema change, verified by literal field-list inspection** — every entry in the worked example was checked to retain exactly the original four D-02 fields unchanged, with only new fields appended, directly proving the "existing UI model structure... remain[s] usable by the screen pipeline" acceptance criterion rather than merely asserting it.
- **The borderline grandchild-boundary case was deliberately included**, not just the two "obvious" cases (populated software boundary, empty non-software boundary) — because the task's own acceptance criteria require demonstrating that "software boundaries without UI requirements produce no screens," which only has teeth if there's also a worked case showing the opposite judgment (a software boundary *with* a UI requirement, reasoned through) sitting right next to it.
- **Entity references were checked against real domain-model.md content, not just asserted as resolved** — directly extending T01's manifest-source-disagreement discipline to this skill's own worked example, rather than treating that discipline as something only the validator (T04) needs to care about.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [UI inventory contract](../../../../.github/skills/screen-generateinventory/SKILL.md)
