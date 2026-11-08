# Use-Case Model — Child Software Boundary

**Boundary ID**: BND-CHILD-SW
**Boundary Type**: software
**Hierarchy Level**: 1
**Generated**: 2026-11-08T00:00:00Z

## Changelog
- v1.0 (2026-11-08): Initial generation

## Actors

### Field Operations Coordinator *(A-001)*
**Kind**: internal-role

### Technician *(A-002)*
**Kind**: human

**Note (worked example)**: "Field Operations Coordinator" also exists as an actor at the root boundary (A-002 there). These are deliberately **different Actor References** — same real-world role, but a distinct actor_id local to this boundary's own use-case model, per contract Section 1.3. This boundary's A-001 is not "the same" as root's A-002; they are independently defined.

## Use Cases

### Schedule Technician *(UC-001)*
**Goal**: Coordinator assigns a Technician to a dispatch-system ServiceRequest and sets a scheduled time slot
**Primary Actor**: Field Operations Coordinator (A-001)
**Script**: [use-case-scripts/UC-001-schedule-technician.md](use-case-scripts/UC-001-schedule-technician.md)
*(Ref: R-902)*

### Update Job Status *(UC-002)*
**Goal**: Technician updates a ServiceRequest's status as field work progresses
**Primary Actor**: Technician (A-002)
**Script**: [use-case-scripts/UC-002-update-job-status.md](use-case-scripts/UC-002-update-job-status.md)
*(Ref: R-903)*

---
**Traceability**: Every use case traces to its boundary, a primary actor, and one or more requirements
**Generated**: 2026-11-08T00:00:00Z
