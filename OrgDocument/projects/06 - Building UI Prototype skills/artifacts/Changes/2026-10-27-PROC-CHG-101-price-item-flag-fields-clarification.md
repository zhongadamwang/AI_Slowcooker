# Price Item Flag Fields — Clarification Needed

**Change ID**: PROC-CHG-101
**Date Created**: 2026-10-27
**Status**: Proposed
**Priority**: Medium
**Requested By**: Pricing Administrator (role-played, solo mode) — via screen-discussfeedback (FB-101)

## Summary
Two Price Item boolean flag fields, currently shown as placeholder labels "[REVIEW NEEDED] Field A" and "[REVIEW NEEDED] Field B," need their actual intended names and semantics confirmed before this screen is implementation-ready.

## Change Details

### Current State
`SCR-104` (Price Item Management)'s Data tab displays two flag fields using visible placeholder labels, rather than confirmed field names. These originated from a raw dictated transcript where the relevant phrases ("is travel change," "is a deep change") could not be confidently transcribed during sanitization (see `sanitization-report.md`'s Flagged Items).

### Proposed State
Confirm the exact field names and business semantics with the original requirements source (ideally the person who dictated the original transcript, or a business stakeholder familiar with this pricing system), then:
1. Update `domain-concepts.md`'s `PriceItem` entity to replace `FlagAttribute5`/`FlagAttribute6` placeholders with confirmed names
2. Update `SCR-104/layout-spec.md`'s Data tab to replace the `[REVIEW NEEDED]` labels with the confirmed field names
3. Regenerate `SCR-104/mockup.html` to reflect the same

### Rationale
A pricing administrator configuring real price items cannot trust or correctly use two fields whose meaning is unknown. Leaving these as visible placeholders (rather than silently guessing) was the correct choice during generation, but a real implementation cannot ship with unresolved field semantics — this is a required clarification before SCR-104 is considered complete, not an optional enhancement.

## Impact Analysis

### Affected Documents
- **File**: `artifacts/Analysis/price-book-test/domain-concepts.md`
  **Impact**: `PriceItem` entity's attribute list needs the two placeholder names replaced; update required
- **File**: `artifacts/UI Prototype/examples/price-book-test/SCR-104/layout-spec.md`
  **Impact**: Data tab's two `[REVIEW NEEDED]` fields need real labels; update required
- **File**: `artifacts/UI Prototype/examples/price-book-test/SCR-104/mockup.html`
  **Impact**: Must be regenerated from the updated layout spec once names are confirmed; update required

### Affected Tasks
*(None — applies to this pipeline test example, not to the UI Prototyping skill set's own task plan)*

- **Risk Level**: Low (isolated to 2 fields on 1 screen; does not affect navigation, other screens, or the overall data model structure)
- **Estimated Effort**: 1 hour (once the real field names are confirmed — the bulk of the "effort" here is the stakeholder confirmation itself, not the mechanical update)

## Implementation Plan
1. Reach out to the original requirements source (or a business stakeholder with equivalent knowledge) to confirm the two field names and their business meaning
2. Update the three affected files listed above with the confirmed names
3. Re-verify `screen-inventory.json`'s R-724 traceability note (currently flagged at reduced confidence, 0.6) — once resolved, confidence should be raised to reflect the clarified requirement

## Acceptance Criteria
- [ ] Both flag fields have confirmed, non-placeholder names
- [ ] `domain-concepts.md`, `layout-spec.md`, and `mockup.html` are all updated consistently
- [ ] R-724's confidence score in `requirements.json` is updated to reflect the resolved ambiguity

---
**Validation Note**: This change document demonstrates the feedback→change-management routing path working against a second, independent project (price-book-test), confirming the mechanism is not merely a one-off fit to the toy-order-domain fixture used in T11's original validation. The Rationale section is a direct carry-forward of `FB-101`'s `feedback_text` with no re-transcription.
