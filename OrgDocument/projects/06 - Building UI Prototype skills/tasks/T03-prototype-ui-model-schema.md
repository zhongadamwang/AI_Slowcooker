# T03 — Prototype UI Model Schema (Base Model + Aggregation)

**Task ID**: T03
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 2-3 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

The UI Model (R-606, R-627, R-628, R-629, R-630) is the single most architecturally significant piece of new modeling work in this project, and `scope-analysis.md` flags it as the **top recommendation**: "treat as the first thing to prototype concretely... several other Core features depend on its shape being settled." `domain-concepts.md` rated this pattern's confidence as only medium, pending a real example.

This task produces a **worked example**, not yet the actual generation skill — the goal is de-risking the schema design before committing to it in T04's instructions.

## Objectives

- Produce at least one concrete `ui-model.md`/`.json` example against a real or toy domain
- Validate that "aggregation" is representable using only Markdown+JSON, with no new modeling notation required
- Sketch (not fully implement) the derived-model placeholder structure so the base-model schema doesn't need breaking changes later

## Detailed Requirements

### Functional Requirements
- **FR-03.1**: Example UI Model contains 2+ `UIModelEntry` items, each aggregating 2+ domain entities
- **FR-03.2**: Example demonstrates the full traceability chain: domain entities → Aggregation → UIModelEntry

### Technical Requirements
- **TR-03.1**: If a new notation genuinely is needed beyond Markdown+JSON, that gap must be explicitly documented as a finding of this task, not silently absorbed into T04

## Acceptance Criteria

- [x] At least one concrete `ui-model.md` worked example published
- [x] Schema confirmed workable using only Markdown+JSON, or gap explicitly documented
- [x] Derived-model placeholder structure sketched

## Dependencies

### Prerequisites
- **T02** — conventions (ID formats, traceability tags) should be settled before schema is finalized

### Blocks
- T04 (screen inventory generation references UI Model entries)

---

## Completion Notes

**Completed**: 2026-10-27

### Deliverables

- **`artifacts/UI Prototype/examples/toy-order-domain/domain-model.md`**: a minimal, explicitly-labeled toy fixture (Customer, Order, LineItem, Product — a simple e-commerce order domain) used solely to exercise the UI Model schema; clearly marked as a fixture, not a real project's domain model
- **`artifacts/UI Prototype/examples/toy-order-domain/ui-model.md` + `.json`**: a worked-example base UI Model with 3 `UIModelEntry` items (exceeds FR-03.1's "2+" requirement):
  - **UME-001 "Order Summary"**: the primary multi-entity aggregation (Order + Customer + LineItem) matching the exact example already used illustratively in `requirements.md`
  - **UME-002 "Product Catalog Entry"**: a deliberate **1-to-1 (single-entity) aggregation**, included to confirm the schema handles the degenerate case gracefully, not just genuine multi-entity combinations
  - **UME-003 "Customer Order History"**: a **partially-overlapping** aggregation (shares `Order`/`Customer` with UME-001 but represents a distinct list-style concept), included to confirm independently-keyed entries don't conflict even when their member-entity sets overlap
  - An explicit **traceability chain demonstration** for UME-001 (domain entities → Aggregation → UIModelEntry → hypothetical Screen), satisfying FR-03.2
  - A **derived-model placeholder sketch** (`UIM-DERIVED-EXAMPLE-ADMIN`) showing a derived entry reusing its base `entry_id` plus an explicit `derives_from_entry` back-reference — confirmed schema-compatible without needing a new notation, while explicitly not implementing full derivation/filtering logic (correctly deferred to Phase 3)

### Key Finding (TR-03.1)

**No new modeling notation is required.** All three worked-example entries, their aggregations, and the derived-model placeholder are fully representable using plain Markdown + JSON, confirming `goals.md`'s ASM-8 assumption. This directly de-risks T04–T09, which can now proceed against the schema already defined in `orgModel/02 .../domain-model.md` without a pending schema-redesign risk hanging over them.

Two sub-findings worth carrying forward into T04's own authoring:
- The 1-to-1 aggregation case (UME-002) needs no special-casing in the schema — a single-member `domain_entity_refs` array works identically to a multi-member one
- Overlapping aggregations (UME-001/UME-003 both referencing `Order`/`Customer`) are fine because there is no global uniqueness constraint on entity-combinations — each `UIModelEntry` is independently keyed by `entry_id`

### Explicitly Not Validated Here (Not a Gap — Correctly Deferred)

- The live `syncWithDomainModel()`/`propagateChange()` co-evolution and regeneration behavior (R-627a, R-629a) — this worked example is a static snapshot, not a test of that mechanism, which remains a Phase 2 concern per `scope-analysis.md`
- Full derived-model derivation/filtering logic — only sketched as a placeholder, per the task's own Objectives ("sketch, not fully implement")

### Next Steps for Integration

- **T04** (`screen-generateinventory`): can now reference `UME-[###]` entries with confidence the schema holds; the toy example's UME-001 is a ready-made test fixture if a concrete walkthrough is useful during T04's own authoring
- No revision to `ui-prototyping-conventions.md` (T02) was needed — its `UME-[###]` format and per-model-scoped numbering rule held up against this worked example exactly as specified
