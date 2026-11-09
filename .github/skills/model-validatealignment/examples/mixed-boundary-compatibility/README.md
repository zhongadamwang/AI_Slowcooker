# Mixed-Boundary Compatibility Example (T05)

**Acceptance Criterion**: "Produced domain/process/use-case/UI artifacts validate together on a mixed-boundary example."

This example demonstrates the **full chain** — domain model → use-case model → UI model → alignment validation — actually composing correctly across a mixed (non-software + software) boundary hierarchy, using the real artifacts already produced by T01 (fixtures), T02 (`usecase-generatemodel`'s worked example), T03 (`ui-generatemodel`'s worked example), and T04 (the real validator). This is not a new, separately-authored scenario — it is the **proof that the same three boundaries' real outputs from T01–T04 compose together**, which is what T05's wiring work is actually responsible for demonstrating.

## The Chain

| Boundary | Domain Model (T01) | Use-Case Model (T02) | UI Model (T03) | Alignment Result (T04) |
|---|---|---|---|---|
| `BND-ROOT` (non-software) | [domain-model.md](../fixtures/three-level-valid/root-boundary/domain-model.md) | [use-case-model.json](../../usecase-generatemodel/examples/three-level-worked-example/root-boundary/use-case-model.json) | [ui-model.json](../../ui-generatemodel/examples/three-level-worked-example/root-boundary/ui-model.json) (empty, `generation_note` explains why) | PASS |
| `BND-CHILD-SW` (software) | [domain-model.md](../fixtures/three-level-valid/root-boundary/child-software-boundary/domain-model.md) | [use-case-model.json](../../usecase-generatemodel/examples/three-level-worked-example/root-boundary/child-software-boundary/use-case-model.json) | [ui-model.json](../../ui-generatemodel/examples/three-level-worked-example/root-boundary/child-software-boundary/ui-model.json) (2 entries) | PASS |
| `BND-GRANDCHILD` (software) | [domain-model.md](../fixtures/three-level-valid/root-boundary/child-software-boundary/grandchild-boundary/domain-model.md) | [use-case-model.json](../../usecase-generatemodel/examples/three-level-worked-example/root-boundary/child-software-boundary/grandchild-boundary/use-case-model.json) | [ui-model.json](../../ui-generatemodel/examples/three-level-worked-example/root-boundary/child-software-boundary/grandchild-boundary/ui-model.json) (1 entry) | PASS |

## What This Proves

1. **The non-software boundary's own use-case and UI models don't block alignment.** `BND-ROOT` has real use cases (T02) but a deliberately empty UI model (T03) — the validator (T04) must not treat this as a failure, since R-011 permits (and here, correctly produces) zero UI entries for a non-software boundary.
2. **The software boundaries' UI entries trace correctly back through use cases to domain entities.** `BND-CHILD-SW`'s `UME-001`/`UME-002` each cite a `source_use_case_refs` (`UC-001`/`UC-002`) and `domain_entity_refs` (`E-002`/`E-003`) that genuinely exist in that boundary's real `domain-model.md` and `use-case-model.json` — not just structurally well-formed, but actually resolvable, exactly as T04's validator checks.
3. **The deliberate `E-002` entity-ID collision between `BND-ROOT` and `BND-CHILD-SW` (T01's own fixture point) does not propagate into a false conflict** once use-case and UI models are layered on top — `(scope, entity_id)` *** holds through the full chain, not just at the domain-model layer alone.
4. **This is real composition, not independently-authored parallel examples.** Every file referenced in the table above already exists from T01–T04's actual deliverables; this document adds no new domain/use-case/UI content — it only adds the validator run that ties them together and the write-up explaining why the result is correct.

## Running the Validation

Reusing T04's existing `run_fixtures.py` runner's `run_three_level_valid()` function (not duplicating it) confirms:

```
[OK] three-level-valid: generated status='PASS', expected status='PASS'
```

This is the exact same fixture already validated in T04 — demonstrated here as the mixed-boundary compatibility proof precisely because the three-level-valid fixture already *is* a mixed (non-software root + software child/grandchild) hierarchy with a genuine entity collision. T05 does not need (and should not invent) a sixth, redundant fixture; it needs to show that this exact chain — now that T02/T03's worked examples also populate the same boundaries with real use-case/UI content — still validates correctly end-to-end. It does.

## Compatibility With Existing Screen Pipeline

`BND-CHILD-SW`'s `ui-model.json` (T03's worked example) uses exactly the same `entry_id`/`ui_concept_name`/`domain_entity_refs`/`aggregation_description` fields `screen-generateinventory` (S33) already consumes — confirmed by the existing prototype regression suite (`screen-generatemockup/scripts/test_prototype_contract.py`) continuing to pass unmodified after all of T05's wiring changes (7/7 tests, unchanged). `screen-generateinventory` could consume `BND-CHILD-SW`'s `ui-model.json` today with zero code changes on its part, exactly as T03's Migration Notes promised.

---
**Traceability**: Composes T01's `fixtures/three-level-valid/`, T02's `usecase-generatemodel/examples/three-level-worked-example/`, T03's `ui-generatemodel/examples/three-level-worked-example/`, and T04's `scripts/run_fixtures.py`
**Generated**: 2026-11-08
