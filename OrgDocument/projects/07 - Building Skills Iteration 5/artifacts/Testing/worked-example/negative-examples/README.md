# Negative Examples Catalog

**Project**: PRJ-07 — T07 Release Verification
**Purpose**: Demonstrate that every category of model inconsistency T07 requires is caught explicitly — never silently treated as aligned — with each claim backed by an actual executed check, not prose alone.

Per the Implementation Analysis's Release Acceptance: "Validate fresh/revised/resumed rounds, entity conflicts, boundary conflicts, unknown typing, unresolved clarification, and stale reports."

## 1. Entity/Boundary Contradictions → `INVALID_INPUT`

**Scenario**: [`manifest-source-disagreement`](../../../../../.github/skills/model-validatealignment/fixtures/manifest-source-disagreement/) (T01)

A use-case model claims entity `E-011` ("DiscountCode") is `defined_in: billing-boundary/domain-model.md`, but that document only actually defines `E-010` ("Invoice"). The validator resolves the claim against real document content and catches the contradiction.

**Proof it was actually executed, not just described**: `scripts/run_fixtures.py` (T04) generates a real `generated-report.json` for this fixture and confirms `status == "INVALID_INPUT"` matches `expected-report.json`. Re-confirmed during T07:
```
[OK] manifest-source-disagreement: generated status='INVALID_INPUT', expected status='INVALID_INPUT'
```
No successful alignment is ever reported for this scenario.

## 2. Illegal UI Placement → Rejected at the Boundary Type Gate

**Scenario**: [`unknown-boundary-type`](../../../../../.github/skills/model-validatealignment/fixtures/unknown-boundary-type/)'s attempted-UIModelEntry sub-case (T01), and the structural R-011 enforcement proven in T01's `three-level-valid`/`software-boundary-no-ui-required` fixtures (T04)

A boundary with `boundary_type: non-software` (or `unknown`) that has a `UIModelEntry` attempted against it is caught by `validate_round()`'s explicit check: *"Boundary {bid} is non-software but has N UIModelEntry/entries referencing it. UI may only exist in explicitly software-typed boundaries."* This is R-011's hardest line.

**Proof**: `test_alignment_contract.py::UnknownBoundaryTypeFixture::test_unknown_type_with_attempted_ui_entry_still_blocks` directly asserts the result is `NEEDS_CLARIFICATION`, never `PASS`, even when a `UIModelEntry` was already (incorrectly) attempted. This is defense-in-depth: `ui-generatemodel` (T03) itself refuses to produce such an entry in the first place (Step 0.2 of its own `SKILL.md`), and the validator independently catches it if that refusal is ever bypassed.

## 3. Unknown Boundary Typing → `NEEDS_CLARIFICATION`, Never Defaulted

**Scenario**: [`unknown-boundary-type`](../../../../../.github/skills/model-validatealignment/fixtures/unknown-boundary-type/) (T01)

A boundary with no declared `boundary_type` at all. The validator reports `NEEDS_CLARIFICATION` with a specific clarification question — never silently defaulting to `software` (which could permit a fabricated screen) or `non-software` (which could silently discard real use cases).

**Proof**: `scripts/run_fixtures.py` confirms:
```
[OK] unknown-boundary-type: generated status='NEEDS_CLARIFICATION', expected status='NEEDS_CLARIFICATION'
```

## 4. Missing Applicable Models → `INVALID_INPUT`, Not Silent Skip

**Scenario**: [`missing-applicable-model`](../../../../../.github/skills/model-validatealignment/fixtures/missing-applicable-model/) (T01)

A software boundary with a domain model and process model, but **no use-case model at all**. Reported as `INVALID_INPUT` — distinct from `NEEDS_CLARIFICATION` (ambiguous existing content) and distinct from silently treating the missing model as "not applicable" (which would be wrong for a software boundary, where a use-case model is expected).

**Proof**:
```
[OK] missing-applicable-model: generated status='INVALID_INPUT', expected status='INVALID_INPUT'
```

## 5. Stale Reports → Resume Detects and Reports Staleness, Never Trusts an Old PASS

**Scenario**: [`stale-report-demo-result.json`](stale-report-demo-result.json) / [`stale_report_demo.py`](stale_report_demo.py) (new, T07)

A boundary (`BND-CHILD-SW`) had a round that reached `PASS`, recorded against `domain_model: v1`. The domain model is then edited (advancing to `v2`). On resume, `resolve_round_for_resume()` is run with the prior round's recorded versions against the new current versions.

**Actual executed result** (not merely described):
```
is_stale(): True
resolve_round_for_resume(): stale
```
A counterfactual (no edit happened) confirms the function correctly returns `valid` when nothing changed — proving this isn't a function that always reports staleness, but one that genuinely compares versions:
```
--- counterfactual: no edit happened ---
is_stale(): False
resolve_round_for_resume(): valid
```
This directly implements the contract's "A later edit invalidates the prior round's success for the affected model set; resume must check versions" (Section 4.4), and is the same function `edps-workflow-orchestrator`'s T06 integration documents calling on every `orchestrate resume`.

## 6. Unresolved Clarification → Remains Unresolved Until Revalidation, Never Silently Closed

**Scenario**: Same as #3 (`unknown-boundary-type`), examined from the clarification-lifecycle angle, plus the explicit non-bypassability proof

The contract (Section 4.3) and T06's orchestrator integration both establish: a round cannot transition from `NEEDS_CLARIFICATION` directly to `PASS` without an intervening revalidation against updated artifacts. This is proven **structurally**, not just by convention:

- `test_alignment_report.py::RevisionInvalidationTests::test_a_skip_or_self_attestation_cannot_fabricate_a_valid_resume` (T04) inspects `resolve_round_for_resume()`'s actual function signature via `inspect.signature` and asserts it takes **exactly** `prior_round` and `current_model_versions` — no `collaboration_mode`, `severity`, or `archetype` parameter exists anywhere in this function's signature, making it structurally impossible for a solo-mode self-attestation or a `rapid`-archetype leniency to short-circuit this check.
- `edps-workflow-orchestrator`'s `resolveCheckSeverity()` (T06) only special-cases `check.type === "stakeholder_confirmation"` checks; every `model-validatealignment` gate check is `artifact_existence`/`content_pattern`/`json_schema` typed, so they all fall through unchanged regardless of `collaboration_mode`.

## Summary Table

| Scenario | Status Produced | Proven By |
|---|---|---|
| Entity/boundary contradiction | `INVALID_INPUT` | `run_fixtures.py` (manifest-source-disagreement) |
| Illegal UI placement | Blocked (`NEEDS_CLARIFICATION` finding + `ui-generatemodel` refusal) | `test_unknown_type_with_attempted_ui_entry_still_blocks` |
| Unknown boundary typing | `NEEDS_CLARIFICATION` | `run_fixtures.py` (unknown-boundary-type) |
| Missing applicable model | `INVALID_INPUT` | `run_fixtures.py` (missing-applicable-model) |
| Stale report | `stale` (resume-time) | `stale_report_demo.py`, actually executed |
| Unresolved clarification cannot be bypassed | Structurally impossible | `inspect.signature` test on `resolve_round_for_resume` |

Every row above has an **executed** proof artifact (a test that was run, or a script whose actual output is reproduced above) — none of these six categories rest on prose description alone.
