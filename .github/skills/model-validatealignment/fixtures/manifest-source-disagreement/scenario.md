# Fixture: Manifest / Source Disagreement

**Scenario**: A round's alignment manifest (or a use-case/UI model's entity reference) claims an entity exists in a `domain-model.md` that does not actually contain it — testing that the validator actually opens and parses the referenced document rather than trusting a cached or asserted claim.

## Domain Model (actual, authoritative content)

```markdown
# Billing Boundary — Domain Model

## Entities

### Invoice *(E-010)*
A billing record for completed work.
```

Only **one** entity (`Invoice`, `E-010`) actually exists in this document.

## Use-Case Model (as submitted — makes a false claim)

```json
{
  "model_id": "UCM-BILLING",
  "boundary_ref": { "boundary_id": "BND-BILLING", "boundary_type": "software" },
  "use_cases": [
    {
      "use_case_id": "UC-001",
      "name": "Apply Discount",
      "primary_actor_ref": "A-001",
      "requirement_refs": ["R-500"],
      "referenced_entities": [
        { "entity_id": "E-011", "entity_name": "DiscountCode", "scope": "billing-boundary", "defined_in": "billing-boundary/domain-model.md" }
      ]
    }
  ]
}
```

The use-case model references `E-011` ("DiscountCode") claiming it is `defined_in: billing-boundary/domain-model.md` — but that document (shown above) only actually defines `E-010` ("Invoice"). `E-011` does not exist there.

## Why This Matters

Per the Implementation Analysis's named risk ("Validator checks only a detached manifest"), a naive validator might simply trust the `defined_in` claim as a well-formed reference without ever opening and parsing `billing-boundary/domain-model.md` to confirm `E-011` is actually present. This fixture exists specifically to force the validator implementation to **actually resolve** every reference against the real document content, not just check that the JSON shape is well-formed.
