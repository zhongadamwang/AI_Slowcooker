# Screen Inventory

**Project**: PRJ-07 — T07 Worked Example
**Boundary**: BND-CHILD-SW (software)
**Generated**: 2026-11-08
**Source**: ui-model.json (UIM-CHILD-SW), requirements from use-case-model.json (UCM-CHILD-SW)
**Total Screens**: 2

## Navigation Plan

- **Entry screen**: Dispatch Queue (SCR-101) — the natural landing view for a Coordinator starting their shift
- **Journey 1**: Dispatch Queue (SCR-101) → select a ServiceRequest → Job Status Update (SCR-102), for a Technician updating progress on an assigned job
- No other planned cross-screen journeys in this two-screen set; each screen also functions as a reasonable standalone entry point depending on which actor (Coordinator vs. Technician) is using the system

## Local Interactions

- Dispatch Queue (SCR-101): no local dialogs in this minimal worked example — the "Assign Technician" action directly updates the request's assignment inline (per UC-001's Main Flow steps 1–3) rather than opening a popup
- Job Status Update (SCR-102): a local "Confirm Status Change" dialog before committing a status transition (not in UC-002's original script, added here as a realistic interaction pattern the mockup can demonstrate validation/cancel/save behavior with)

## Screens

### Dispatch Queue *(SCR-101)*
**Purpose**: Let a Field Operations Coordinator see unscheduled ServiceRequests alongside available Technicians, and assign a Technician + time slot to a request
**UI Model Entry**: UME-001
*(Ref: UC-001)*

### Job Status Update *(SCR-102)*
**Purpose**: Let a Technician update a single ServiceRequest's status as field work progresses
**UI Model Entry**: UME-002
*(Ref: UC-002)*

---
**Traceability**: Every screen traces to exactly one UI Model entry and the use case that motivated it
**Generated**: 2026-11-08
