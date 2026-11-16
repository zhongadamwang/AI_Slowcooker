# UI Model — Child Software Boundary

**Model ID**: UIM-CHILD-SW
**Model Type**: base
**Boundary**: BND-CHILD-SW (software)
**Generated**: 2026-11-08T00:00:00Z

## Changelog
- v1.0 (2026-11-08): Initial generation from use-case-model.json (UCM-CHILD-SW)

## Entries

### Dispatch Queue *(UME-001)*
**Aggregates**: ServiceRequest (E-002, child-software-boundary scope), Technician (E-003)
*(Boundary: BND-CHILD-SW; Ref: UC-001)*

Aggregates ServiceRequest and Technician so a Coordinator can see unscheduled requests alongside available technicians in one view, supporting the Schedule Technician use case.

### Job Status Update *(UME-002)*
**Aggregates**: ServiceRequest (E-002)
*(Boundary: BND-CHILD-SW; Ref: UC-002)*

A focused view of a single ServiceRequest for a Technician to update its status as field work progresses, supporting the Update Job Status use case.

---
**Traceability**: Every entry traces to its boundary and the use case(s) that motivated it
**Generated**: 2026-11-08T00:00:00Z
