# Use-Case Model — Root Boundary

**Boundary ID**: BND-ROOT
**Boundary Type**: non-software
**Hierarchy Level**: 0
**Generated**: 2026-11-08T00:00:00Z

## Changelog
- v1.0 (2026-11-08): Initial generation

## Actors

### Customer *(A-001)*
**Kind**: human

### Field Operations Coordinator *(A-002)*
**Kind**: internal-role

## Use Cases

### Request Field Service *(UC-001)*
**Goal**: Customer requests field work be scheduled, before any software system is involved
**Primary Actor**: Customer (A-001)
**Script**: [use-case-scripts/UC-001-request-field-service.md](use-case-scripts/UC-001-request-field-service.md)
*(Ref: R-900)*

### Accept Service Request *(UC-002)*
**Goal**: Field Operations Coordinator reviews and accepts an incoming service request, handing it to the dispatch software system
**Primary Actor**: Field Operations Coordinator (A-002)
**Script**: [use-case-scripts/UC-002-accept-service-request.md](use-case-scripts/UC-002-accept-service-request.md)
*(Ref: R-901)*

---
**Traceability**: Every use case traces to its boundary, a primary actor, and one or more requirements
**Note (worked example)**: This is a non-software boundary — it receives full use-case treatment per this skill's Step 2 discipline, not a thinner placeholder. Neither use case has a UI References section in its script, since no software exists at this boundary at all.
**Generated**: 2026-11-08T00:00:00Z
