# Use-Case Model — Grandchild Boundary

**Boundary ID**: BND-GRANDCHILD
**Boundary Type**: software
**Hierarchy Level**: 2
**Generated**: 2026-11-08T00:00:00Z

## Changelog
- v1.0 (2026-11-08): Initial generation

## Actors

### Technician *(A-001)*
**Kind**: human

**Note (worked example)**: Again a deliberately distinct `actor_id` from the Child Software Boundary's "Technician" (A-002 there) — same real-world role, different Actor Reference, per contract Section 1.3.

## Use Cases

### Log Time Entry *(UC-001)*
**Goal**: Technician logs a block of time spent on a ServiceRequest within this nested time-tracking sub-module
**Primary Actor**: Technician (A-001)
**Script**: [use-case-scripts/UC-001-log-time-entry.md](use-case-scripts/UC-001-log-time-entry.md)
*(Ref: R-904)*

---
**Traceability**: Every use case traces to its boundary, a primary actor, and one or more requirements
**Note (worked example)**: This is the deepest-nested boundary in the fixture (Level 2). Its own use-case model is still fully independent and self-contained — it does not inherit or reference the parent boundary's use cases directly.
**Generated**: 2026-11-08T00:00:00Z
