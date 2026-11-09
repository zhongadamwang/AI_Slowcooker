# Use Case Script — Log Time Entry (UC-001)

**Actor**: Technician (A-001)
**Goal**: Technician logs a block of time spent on a ServiceRequest within this nested time-tracking sub-module
**System Boundary**: Grandchild Boundary (BND-GRANDCHILD, software)
**Hierarchy Level**: 2
**Requirement References**: R-904

## Changelog
- v1.0 (2026-11-08): Initial generation

## Trigger
Technician finishes a block of work on a ServiceRequest and needs to record the time spent.

## Preconditions
- The ServiceRequest exists and is assigned to this Technician (per the parent Child Software Boundary's UC-002, which this use case is downstream of, though it does not reference that use case's model directly — it only consumes the resulting ServiceRequest/Technician entities already defined in this boundary's own domain-model.md)

## Main Flow
1. Technician opens the time-entry log for the relevant ServiceRequest.
2. Technician enters the start time, end time, and a brief work description.
3. The system creates a TimeEntry (E-004) recording this logged block.

## Postconditions
- A TimeEntry exists, linked to the ServiceRequest and this Technician
