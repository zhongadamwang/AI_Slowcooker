# Fixture: Unknown Boundary Type

**Scenario**: A boundary whose `boundary_type` has not been explicitly declared, with a use case and a UIModelEntry attempted against it.

## Boundary Main (`main.md`, as it would exist in the project)

```markdown
# Unclassified Boundary — Main

## System Boundary

- **Boundary ID**: `BND-UNCLASSIFIED`
- **Boundary Type**: *(not yet declared — no Boundary Type line present)*
- **Hierarchy Path**: `unclassified-boundary/`
- **Parent Boundary ID**: none
```

Note the **absence** of a `Boundary Type` line — this is the fixture's point: `hierarchy-management` created this boundary's folder during decomposition, but no one has yet explicitly classified it as `software`/`non-software`. Per Section 2.1 of the contract, this must be treated as `unknown`, not defaulted to `non-software` just because it has no screens yet, and not defaulted to `software` just because it was decomposed from a `control`-type participant (HV-1 eligibility is orthogonal to software status).

## Attempted Use Case (`use-case-model.json`, as submitted for validation)

```json
{
  "model_id": "UCM-UNCLASSIFIED",
  "boundary_ref": { "boundary_id": "BND-UNCLASSIFIED", "boundary_type": "unknown", "hierarchy_level": 0, "hierarchy_path": "unclassified-boundary/", "parent_boundary_id": null },
  "actors": [{ "actor_id": "A-001", "actor_name": "Operator", "boundary_id": "BND-UNCLASSIFIED", "actor_kind": "human" }],
  "use_cases": [
    { "use_case_id": "UC-001", "name": "Review Pending Item", "goal": "Operator reviews a pending item", "primary_actor_ref": "A-001", "boundary_ref": { "boundary_id": "BND-UNCLASSIFIED" }, "requirement_refs": ["R-900"], "script_ref": "use-case-scripts/UC-001-review-pending-item.md" }
  ]
}
```

The use case itself is valid in shape — the problem is purely that its boundary's type is undeclared.

## Attempted UIModelEntry (rejected, not created)

A separate attempt to generate `ui-model.json` with a UIModelEntry referencing `BND-UNCLASSIFIED` **must be rejected outright by `ui-generatemodel`** (per Section 2.2 — UI may only exist in explicitly `software`-typed boundaries) rather than generated and then merely flagged by the validator afterward. This fixture's `expected-report.json` reflects the validator catching this as defense-in-depth, but `ui-generatemodel` itself should refuse to produce the entry in the first place.
