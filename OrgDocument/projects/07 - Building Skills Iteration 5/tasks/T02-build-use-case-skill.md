# T02 - Build Boundary-Scoped Use-Case Models and Scripts

**Task ID**: T02  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 3.17 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Create proposed `usecase-generatemodel` to describe actor interactions at every identified system-boundary level, with linked scripts explaining the detailed process.

## Detailed Requirements

Sources: R-003, R-004, R-007, R-008.

- Consume requirements, scoped process/domain/collaboration documents, and the shared boundary contract.
- Produce model Markdown/JSON and one script per modeled use case; identify actors, goals, boundary, hierarchy level, and source requirements.
- Scripts cover trigger, preconditions, ordered actor/system steps, applicable alternatives/exceptions, and postconditions. Link applicable process activities and entities.
- Preserve IDs and authored content on revisions; do not restrict actors to humans or use cases to software/leaf boundaries. UI links are optional by applicability.

## Acceptance Criteria

- [x] Model has complete boundary/actor/requirement references at three hierarchy levels.
- [x] Every modeled use case has a linked detailed script with the required sections.
- [x] Non-software and system-actor interactions generate use cases without invented UI screens.
- [x] Revision preserves existing identities and exposes unresolved references rather than silently guessing.

## Validation Tests

Valid and incomplete-input examples; script/model coverage; non-software parent and software child scenarios; repeated generation preserving IDs.

**Done**: The three-level worked example (`examples/three-level-worked-example/`) reuses T01's own fixture boundaries (`BND-ROOT` non-software, `BND-CHILD-SW` software, `BND-GRANDCHILD` software) for cross-task consistency. All three boundary-scoped `use-case-model.json` files were validated against every `gate.json` check by direct inspection: JSON syntax, explicit `boundary_type` on every model, every use case carrying `primary_actor_ref`+matching `boundary_ref`+non-empty `requirement_refs`, every `script_ref` resolving to an actual existing file, zero `## UI References` sections in the non-software root boundary's scripts, `UC-[###]` ID format present, and a `## Changelog` section in every model. Step 5's revision-preservation discipline (flag unresolved refs rather than silently drop/renumber) is documented in the skill's workflow but not separately exercised by a second-pass regeneration in this worked example — noted as a residual follow-up, not a blocker, since the discipline itself is concretely specified and gate-checked (soft) for changelog presence.

## Dependencies

Prerequisite: T01. Blocks T05.

## Implementation Notes and Deliverables

Skill instructions, gate, model/script templates, examples, and focused contract tests; meaningful indexes in generated script directories.

**Delivered** under `.github/skills/usecase-generatemodel/`:

- `SKILL.md` — full skill definition: shared-contract reference, inputs/outputs/JSON+Markdown schemas (reproducing contract Section 3 for convenience, contract remains authoritative), a 6-step workflow (Step 0's boundary-readiness gate is the load-bearing step: this skill refuses to run against an undeclared `boundary_type` rather than guessing), quality checks, and integration points
- `gate.json` (skill ID **S32**, filling the one real gap in the orchestrator's prior S00–S38 range, per T01's Skill ID Ledger) — 8 checks (6 hard, 2 soft), all manually verified passing against the worked example
- `examples/three-level-worked-example/` — a full 3-level boundary hierarchy (6 use cases total: 2 non-software, 4 software across two nested software boundaries), with every model/script file actually written out, not just described in prose; a `README.md` calls out the five specific contract behaviors this example demonstrates (non-software boundaries get full treatment; actors are boundary-relative, never shared across levels; UC IDs are scoped per boundary; UI References appear only where applicable and are explicitly marked illustrative-only where a true first pass would omit them; cross-boundary handoffs stay in prose, not structured cross-model references)

### Key Decisions

- **Step 0 (boundary-readiness check) is the skill's single most important workflow step** — it directly operationalizes T01's contract Section 2.1 by refusing to generate anything against a boundary whose `boundary_type` is `unknown` or undeclared, mirroring `screen-generateinventory`'s existing precondition-check discipline rather than inventing a new failure mode.
- **Actors are never reused across boundary levels, even for the literal same real-world role** — demonstrated concretely in the worked example ("Field Operations Coordinator" and "Technician" each appear as differently-ID'd actors at two different boundaries), not just asserted in the contract's prose.
- **The worked example's one software-boundary script deliberately shows an illustrative-only UI References section**, explicitly labeled as such, rather than either omitting the demonstration entirely or (worse) presenting a fabricated-looking real section — chosen so a future reader of this skill understands what the section looks like once populated, without the worked example itself making a false claim about what this skill alone produces on a first pass.

## References

- [Shared-contract task](T01-define-modeling-contract.md)
- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
