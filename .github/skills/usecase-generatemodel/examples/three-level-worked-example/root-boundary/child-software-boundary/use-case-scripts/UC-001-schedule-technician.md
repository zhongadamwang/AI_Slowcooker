# Use Case Script — Schedule Technician (UC-001)

**Actor**: Field Operations Coordinator (A-001)
**Goal**: Coordinator assigns a Technician to a dispatch-system ServiceRequest and sets a scheduled time slot
**System Boundary**: Child Software Boundary (BND-CHILD-SW, software)
**Hierarchy Level**: 1
**Requirement References**: R-902

## Changelog
- v1.0 (2026-11-08): Initial generation

## Trigger
A new ServiceRequest (E-002, child-software-boundary scope) exists in the dispatch system, awaiting scheduling.

## Preconditions
- The ServiceRequest exists and has no assigned Technician yet
- At least one Technician (E-003) is available for the requested time window

## Main Flow
1. Coordinator opens the unscheduled ServiceRequest in the dispatch system.
2. Coordinator reviews available Technicians and their current workload.
3. Coordinator selects a Technician and proposes a scheduled time slot.
4. The system records the assignment against the ServiceRequest.

## Alternative / Exception Paths
- **No Technician available for the requested window**: Coordinator either proposes an alternative time slot to the customer (outside this use case's scope) or leaves the request unscheduled pending availability.

## Postconditions
- The ServiceRequest has an assigned Technician and a scheduled time slot

## UI References
*(This section is present only in this worked example's own narrative illustration of how it WOULD be populated once ui-generatemodel/screen-generateinventory have run for this boundary \u2014 at generation time by usecase-generatemodel alone, with no UI model/screens yet existing, this section would correctly be OMITTED per Step 3's discipline. It is shown here, clearly marked, purely to illustrate the eventual shape once the pipeline completes; a real first-pass script from this skill alone would not include it.)*
- Step 1 \u2192 *(illustrative only)* Screen SCR-201 / UIModelEntry UME-101 ("Dispatch Queue")
- Step 3 \u2192 *(illustrative only)* Screen SCR-202 / UIModelEntry UME-102 ("Schedule Assignment")
