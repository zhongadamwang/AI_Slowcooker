# Use Case Script — Update Job Status (UC-002)

**Actor**: Technician (A-002)
**Goal**: Technician updates a ServiceRequest's status as field work progresses
**System Boundary**: Child Software Boundary (BND-CHILD-SW, software)
**Hierarchy Level**: 1
**Requirement References**: R-903

## Changelog
- v1.0 (2026-11-08): Initial generation

## Trigger
Technician arrives on-site or completes a stage of the assigned work.

## Preconditions
- The ServiceRequest is assigned to this Technician

## Main Flow
1. Technician opens their assigned ServiceRequest.
2. Technician updates the status (e.g., en route, on-site, in progress, complete).
3. The system records the status change with a timestamp, creating a TimeEntry (E-004, grandchild-boundary scope) if the status change represents a loggable time block.

## Postconditions
- The ServiceRequest reflects the current status
- A corresponding TimeEntry exists in the Grandchild Boundary's time-tracking sub-module, if applicable
