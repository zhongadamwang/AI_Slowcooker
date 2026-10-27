# Order Summary — Add Status Actions Indicator

**Change ID**: PROC-CHG-001
**Date Created**: 2026-10-27
**Status**: Proposed
**Priority**: Low
**Requested By**: Customer (role-played, solo mode) — via screen-discussfeedback (FB-001)

## Summary
Add a visible "Available Actions" indicator near the Order Summary screen's Status field so a customer can tell what they can still do (e.g., cancel) at the order's current status.

## Change Details

### Current State
`SCR-001` (Order Summary) displays the order's `Status` field (e.g., "Shipped") as a plain badge with no indication of what actions remain available to the customer at that status.

### Proposed State
Add a short inline note or secondary indicator next to the Status badge reflecting available actions at that status — e.g., "Shipped — tracking only, cancellation no longer available" — so a customer understands their options without needing to guess or contact support.

### Rationale
Captured during a role-played (solo-mode) mockup discussion of `SCR-001`: a customer reviewing their own order would reasonably want to know whether they can still act on it (e.g., cancel), and the current design gives no such signal. This directly serves requirement R-614's general intent of letting a customer meaningfully understand their order, not just view static data.

## Impact Analysis

### Affected Documents
- **File**: `artifacts/UI Prototype/examples/toy-order-domain/SCR-001/layout-spec.md`
  **Impact**: The Status section's HTML/CSS needs a new element (or modifier) to display the actions indicator; update required
- **File**: `artifacts/UI Prototype/examples/toy-order-domain/SCR-001/mockup.html`
  **Impact**: Mockup must be regenerated from the updated layout spec once the change is implemented; update required

### Affected Tasks
*(None — this change applies to the T11 validation example, not to the pipeline's own task set T01–T11)*

- **Risk Level**: Low
- **Estimated Effort**: 1-2 hours

## Implementation Plan
1. Update `SCR-001/layout-spec.md`'s Status section to include the new indicator, with a short design-rationale note explaining the addition
2. Append a new changelog entry to `layout-spec.md` ("v1.1: Added status-actions indicator per PROC-CHG-001")
3. Regenerate `SCR-001/mockup.html` from the updated layout spec (manual regeneration in MVP, per T03/scope-analysis.md's Phase 2 note on automated regeneration)
4. Re-verify `interaction-flows.md`'s edges still hold (this change doesn't add/remove navigation, so no diagram update expected, but worth a quick re-check)

## Acceptance Criteria
- [ ] Status field visually communicates available actions at the current status
- [ ] Change does not alter existing navigation (SCR-001 ↔ SCR-002 links unaffected)
- [ ] `layout-spec.md` changelog updated to reflect this change (v1.1)

---
**Validation Note (T11)**: This change document was generated directly from `FB-001`'s `feedback_text` in `feedback-log.md` with no manual re-transcription — the Rationale section above is the same statement captured during the (role-played) discussion, not a re-derived paraphrase, confirming `screen-discussfeedback`'s FR-09.1 requirement holds in a real routing. `change-management`'s existing `REQ-CHG`-adjacent classification (used here as `PROC-CHG` since this affects a design artifact/process, not a formal requirement text itself) accommodated this UI-specific feedback without needing any schema extension, confirming T09's TR-09.1 finding in practice.
