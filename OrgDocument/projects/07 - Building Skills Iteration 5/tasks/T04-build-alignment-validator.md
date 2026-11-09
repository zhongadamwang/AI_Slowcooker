# T04 - Build Shared Model-Alignment Validation

**Task ID**: T04  
**Phase**: 2 - Modeling and Validation  
**Priority**: P0-Critical  
**Estimated Effort**: 3.33 person-days (PERT)  
**Status**: Completed ✅
**Assigned**: Unassigned  
**Created**: 2026-11-07  
**Last Updated**: 2026-11-08
**Completed**: 2026-11-08

## Description and Objectives

Create proposed `model-validatealignment` with a small deterministic validator, source-backed reports, and focused clarification handling.

## Detailed Requirements

Sources: R-005, R-008, R-009, R-010, R-011.

- Validate entity identity/scope/membership and system-boundary identity/type/parent references across applicable models.
- Check actual source/version references; reject detached or contradictory manifest projections and stale report reuse.
- Explicitly distinguish consistency, unresolved clarification, malformed/missing applicable input, and justified UI non-applicability.
- Report item-level model/entity/boundary evidence and actionable questions. Preserve clarification history and require revalidation after answers.
- Delegate VR/HR checks to their existing owners; no duplicated boundary-routing or structural validators.

## Acceptance Criteria

- [x] Consistent multi-level fixtures pass; scoped identical names do not produce false conflicts.
- [x] Entity and boundary contradictions request clarification and never return an aligned result.
- [x] Unknown UI boundary type, illegal UI placement, missing applicable models, malformed inputs, and source/manifest disagreement are explicit failures.
- [x] Every report records round and source versions; editing an affected model invalidates the previous result.

## Validation Tests

Python standard-library tests cover each result class, deterministic output, entity collisions, missing links, UI applicability, and revision invalidation. Existing fixture source data is checked, not just file existence.

**Done**: 18 total tests pass (`python3 -m unittest test_alignment_contract test_alignment_report -v` from `scripts/`): 8 from T01 (per-fixture decision-logic proofs) plus 10 new from T04 — `DeterministicOutputTests` (2: identical inputs produce byte-identical reports, including the INVALID_INPUT case), `ReportRenderingTests` (3: JSON schema completeness, Markdown rendering, and `write_report`'s refusal to silently overwrite a round's report with different content under the same `round_id`), `RevisionInvalidationTests` (5: unchanged versions stay valid, an edited model makes a prior round stale, a non-PASS prior round is always stale regardless of version match, "no prior round" is reported distinctly from "stale," and — proven by literal function-signature inspection, not just a written claim — `resolve_round_for_resume` takes no severity/mode parameter at all, so no solo-mode/rapid-archetype/self-attestation bypass is even structurally possible).

Beyond the unit tests, `scripts/run_fixtures.py` was actually run and **writes real `generated-report.md`/`.json` files into all five fixture folders**, then confirms each one's generated `status` matches its `expected-report.json` — proving the validator's decision logic, report rendering, and fixture data all compose correctly end-to-end, not just in isolated unit assertions.

## Dependencies

Prerequisite: T01. Blocks T05. Implement against T01 fixtures independently of T02/T03.

## Implementation Notes and Deliverables

Skill instructions, hard/non-bypassable alignment gate, validator script, fixture suite, report Markdown/JSON, and clarification procedure.

**Delivered**, extending T01's existing `.github/skills/model-validatealignment/` (contract, fixtures, and validator skeleton all already in place from T01):

- `scripts/alignment_report.py` (new) — `report_to_json`/`report_to_markdown` rendering the exact contract Section 4.2 schema; `write_report` persisting both files with a hard refusal to silently overwrite an existing round's report under the same `round_id` with different content (idempotent re-write of identical content is allowed); `RoundState`/`is_stale`/`resolve_round_for_resume` implementing contract Section 4.4's revision-invalidation and staleness-aware resume logic
- `scripts/test_alignment_report.py` (new) — 10 tests, detailed above
- `scripts/run_fixtures.py` (new) — an executable runner wiring T01's five fixture scenarios into real `validate_round()`/`report_to_json`/`report_to_markdown` calls, writing `generated-report.md`/`.json` into each fixture folder and diffing against `expected-report.json`
- `gate.json` updated from v0.1.0 (T01, contract-definition-only) to v1.0.0 — 4 new checks added (`report_generation_exists`, `revision_staleness_tracking_exists`, `end_to_end_fixture_runner_exists_and_passes`, `report_tests_pass`), all manually verified matching the delivered content; existing T01 checks unchanged
- `SKILL.md` Status and Fixtures/Proof sections updated to reflect both T01 and T04's combined completion

### Key Decisions

- **`write_report`'s overwrite refusal is a real executable safeguard, not just a documented convention** — directly tested (`test_write_report_persists_both_files_and_refuses_silent_overwrite`) by attempting to overwrite a round's report with genuinely different content and asserting a `ValueError` is raised, proving "prior rounds' reports are preserved, never overwritten" (contract Section 4.2) holds in code, not just in prose.
- **`resolve_round_for_resume`'s signature was deliberately kept to exactly two parameters** (`prior_round`, `current_model_versions`), with a dedicated test asserting this via `inspect.signature` — making it structurally impossible to thread a `collaboration_mode`/archetype/severity override through this function, which is the strongest available proof that "a skip, rapid archetype, or solo self-attestation cannot convert inconsistency into successful alignment" (contract Section 4.4) isn't just a documented intention that a future caller could quietly violate.
- **`run_fixtures.py` was actually executed, with its output inspected**, not just written and assumed correct — all 5 fixtures' generated reports were confirmed to match their expected status, and one fixture's actual generated Markdown (`three-level-valid/generated-report.md`) was read in full to confirm the rendering is genuinely human-readable, not merely schema-valid.

## References

- [Implementation analysis](../artifacts/Analysis/implementation-analysis.md)
- [Shared-contract task](T01-define-modeling-contract.md)
