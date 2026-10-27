<!-- Identifier: D-02-example -->

# UI Model (Base) — Toy Order Domain Worked Example

**Model ID**: `UIM-BASE-EXAMPLE`
**Model Type**: `base`
**Derives From**: null (this is the base model)
**Role Scope**: null (base models are role-agnostic)
**Source Domain Model**: `./domain-model.md` (toy fixture, this folder)
**Generated**: 2026-10-27 (T03 worked example)

## Changelog

- **v1.0** (2026-10-27): Initial generation for T03 schema validation

## Purpose

This is a **worked example**, not a real project's UI Model. It exists solely to validate the UIModel/UIModelEntry/Aggregation schema from `domain-model.md` (PRJ-06's own orgModel) against a concrete, non-trivial case before T04 commits to generating this structure for real. See `tasks/T03-prototype-ui-model-schema.md` for the task this fulfills.

## UI Model Entries

### UME-001 — Order Summary

**UI Concept Name**: Order Summary
**Domain Entity References**: `Order`, `Customer`, `LineItem`
**Aggregation Description**: Combines a single Order with its placing Customer and all of its LineItems into one coherent "what did this customer order" view — the natural unit a user looks at when reviewing a single order, rather than navigating Order, Customer, and LineItem as three separate records.

```json
{
  "entry_id": "UME-001",
  "ui_concept_name": "Order Summary",
  "domain_entity_refs": ["Order", "Customer", "LineItem"],
  "aggregation_description": "Combines a single Order with its placing Customer and all of its LineItems into one coherent 'what did this customer order' view"
}
```

**Aggregation Record** (AGG-001):
```json
{
  "aggregation_id": "AGG-001",
  "member_entities": ["Order", "Customer", "LineItem"],
  "resulting_ui_concept": "UME-001"
}
```

### UME-002 — Product Catalog Entry

**UI Concept Name**: Product Catalog Entry
**Domain Entity References**: `Product`
**Aggregation Description**: A degenerate (single-entity) aggregation — Product alone is already a coherent UI-facing concept with no combination needed. Included deliberately in this worked example to confirm the schema handles the **1-to-1 case** gracefully, not just genuine multi-entity combinations.

```json
{
  "entry_id": "UME-002",
  "ui_concept_name": "Product Catalog Entry",
  "domain_entity_refs": ["Product"],
  "aggregation_description": "Single-entity pass-through; Product is already a coherent UI concept on its own"
}
```

**Aggregation Record** (AGG-002):
```json
{
  "aggregation_id": "AGG-002",
  "member_entities": ["Product"],
  "resulting_ui_concept": "UME-002"
}
```

### UME-003 — Customer Order History

**UI Concept Name**: Customer Order History
**Domain Entity References**: `Customer`, `Order`
**Aggregation Description**: Combines a Customer with the full list of their Orders (status + date only, not line-item detail) into a list-style view — distinct from UME-001, which is detail-oriented for one specific Order. Included to confirm the schema can represent **two different aggregations that partially overlap in member entities** (both reference `Order` and `Customer`) without conflict, since each UIModelEntry is its own independent record, not a global dedup of entity combinations.

```json
{
  "entry_id": "UME-003",
  "ui_concept_name": "Customer Order History",
  "domain_entity_refs": ["Customer", "Order"],
  "aggregation_description": "List-style view combining a Customer with summary-level data from all their Orders, distinct from UME-001's single-Order detail view"
}
```

**Aggregation Record** (AGG-003):
```json
{
  "aggregation_id": "AGG-003",
  "member_entities": ["Customer", "Order"],
  "resulting_ui_concept": "UME-003"
}
```

## Traceability Chain Demonstration (FR-03.2)

Per T03's FR-03.2, the full chain for UME-001 is traced explicitly below:

```
Order, Customer, LineItem (domain entities, domain-model.md)
    │
    ▼
AGG-001 (Aggregation record: combines the above three)
    │
    ▼
UME-001 "Order Summary" (UIModelEntry: the resulting UI-facing concept)
    │
    ▼
SCR-001 "Order Summary Screen" (hypothetical future Screen, T04 — not generated in this task, shown only to illustrate the next link in the chain)
```

This confirms the chain required by `domain-concepts.md`'s "Key Entity Patterns" section (`Requirement → Aggregation → UIModelEntry → Screen → ...`) is representable end-to-end with the current schema, with no missing link.

## Derived-Model Placeholder (Sketch Only, per TR-03.1 / Objectives)

Per R-630/R-631 and T03's objective to "sketch (not fully implement) the derived-model placeholder structure," here is a minimal, non-functional sketch showing how a derived model *would* reference this base model, without actually building the full derivation logic (deferred to Phase 3 per `scope-analysis.md`):

```json
{
  "model_id": "UIM-DERIVED-EXAMPLE-ADMIN",
  "model_type": "derived",
  "derives_from": "UIM-BASE-EXAMPLE",
  "role_scope": "Admin",
  "entries": [
    {
      "entry_id": "UME-001",
      "derives_from_entry": "UME-001",
      "ui_concept_name": "Order Summary (Admin View)",
      "domain_entity_refs": ["Order", "Customer", "LineItem"],
      "aggregation_description": "Same aggregation as base UME-001, but the Admin-scoped screen generated from this entry would additionally expose internal fields (e.g., margin) not shown to a Customer-role screen — the filtering/adaptation happens at generation time (T04+), not within this placeholder record itself"
    }
  ]
}
```

**Finding**: This placeholder confirms a derived model's entry can reuse the base entry's `entry_id` plus an explicit `derives_from_entry` field without any schema conflict — the base/derived relationship is representable as "same entry_id, different model_id, explicit back-reference," which is simple enough to not require a new notation. Full derivation/filtering logic itself remains out of scope for this task (Phase 3, per the Deferred Backlog in `task-breakdown.md`).

## Schema Validation Findings (TR-03.1)

- ✅ **No new modeling notation required.** All three worked-example entries, their aggregations, and the derived-model placeholder are fully representable using plain Markdown + JSON, consistent with `goals.md`'s ASM-8 assumption. No gap found.
- ✅ **1-to-1 aggregation case (UME-002) representable** without special-casing — a single-member `domain_entity_refs` array works identically to a multi-member one.
- ✅ **Partially-overlapping aggregations (UME-001 and UME-003 both reference `Order`/`Customer`) do not conflict** — each UIModelEntry is independently keyed by `entry_id`, so there is no global uniqueness constraint on `domain_entity_refs` combinations that would need to be enforced or worked around.
- ✅ **Traceability chain (domain entities → Aggregation → UIModelEntry) demonstrated end-to-end** for UME-001, satisfying FR-03.2.
- ⚠️ **Not yet validated in this task** (explicitly deferred, not a gap): the live `syncWithDomainModel()`/`propagateChange()` behavior (R-627a, R-629a) — this worked example is a static snapshot, not a test of the co-evolution/regeneration mechanism itself, which remains a Phase 2 concern per `scope-analysis.md`.

## See Also

- `../../../../../orgModel/02 - UI Prototype Skill Development Process/domain-model.md` — the schema this example validates
- `../../Documentation/ui-prototyping-conventions.md` — ID formats (`UME-[###]`) and traceability conventions applied throughout this example
- `./domain-model.md` — the toy domain fixture this UI Model is built from
