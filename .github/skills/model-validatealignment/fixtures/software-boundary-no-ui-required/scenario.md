# Fixture: Software Boundary, No UI Required

**Scenario**: A `software`-typed boundary with real use cases and process activities, but deliberately **zero** UIModelEntries — demonstrating that R-011's "software boundaries do not automatically require a screen" is respected rather than silently flagged as incomplete.

## Boundary Main

```markdown
# Batch Reconciliation Boundary — Main

## System Boundary

- **Boundary ID**: `BND-BATCH-RECON`
- **Boundary Type**: `software`
- **Rationale**: A backend batch-processing system with no end-user-facing screens at all -- it runs on a schedule and its only "actors" are other internal systems and a scheduled trigger.
```

## Use-Case Model (exists, valid)

```json
{
  "model_id": "UCM-BATCH-RECON",
  "boundary_ref": { "boundary_id": "BND-BATCH-RECON", "boundary_type": "software" },
  "actors": [
    { "actor_id": "A-001", "actor_name": "Nightly Scheduler", "boundary_id": "BND-BATCH-RECON", "actor_kind": "internal-role" }
  ],
  "use_cases": [
    {
      "use_case_id": "UC-001",
      "name": "Reconcile Daily Transactions",
      "goal": "Nightly Scheduler triggers reconciliation of the day's transactions against the ledger",
      "primary_actor_ref": "A-001",
      "boundary_ref": { "boundary_id": "BND-BATCH-RECON" },
      "requirement_refs": ["R-700"],
      "script_ref": "use-case-scripts/UC-001-reconcile-daily-transactions.md"
    }
  ]
}
```

## UI Model (exists, deliberately empty of entries)

```json
{
  "model_id": "UIM-BATCH-RECON",
  "model_type": "base",
  "entries": [],
  "aggregations": []
}
```

An empty `entries` array is the correct, deliberate outcome here — not a sign that `ui-generatemodel` failed or that `screen-generateinventory` has nothing to work from because of an error. `ui-generatemodel` examined this boundary's use cases and determined none warrant a screen (there is no human actor with anything to look at), consistent with `screen-generateinventory`'s own existing convention that an orphaned/empty situation should be a deliberate, noted decision rather than silently treated as broken.
