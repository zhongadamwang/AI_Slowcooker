# Fixture: Missing Applicable Model

**Scenario**: A software-typed boundary where the use-case model is absent entirely (never generated), while domain and process models exist.

## Boundary Main

```markdown
# Order Intake Boundary — Main

## System Boundary

- **Boundary ID**: `BND-ORDER-INTAKE`
- **Boundary Type**: `software`
- **Rationale**: A standalone order-intake web application.
- **Hierarchy Path**: `order-intake-boundary/`
- **Parent Boundary ID**: none
```

## What Exists

- `order-intake-boundary/domain-model.md` — present, defines `Order`, `Customer` entities
- `order-intake-boundary/process.md` — present, documents the intake process flow
- `order-intake-boundary/use-case-model.json` — **absent** (never generated; `usecase-generatemodel` was never run for this boundary)
- `order-intake-boundary/ui-model.json` — absent (would depend on the use-case model per the recommended pipeline order, so its absence here is expected, not a separate problem)

## Why This Is `INVALID_INPUT`, Not `NEEDS_CLARIFICATION` or Silent Skip

Per Section 4.3 of the contract, a **missing required model** for a boundary in scope is reported as `INVALID_INPUT` — distinct from `NEEDS_CLARIFICATION` (which is for genuine ambiguity in content that *does* exist) and distinct from silently treating the use-case model as "not applicable" (which would be wrong — this is a `software` boundary where a use-case model is expected, it simply hasn't been produced yet).
