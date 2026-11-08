# Use Case Script — Accept Service Request (UC-002)

**Actor**: Field Operations Coordinator (A-002)
**Goal**: Field Operations Coordinator reviews and accepts an incoming service request, handing it to the dispatch software system
**System Boundary**: Root Boundary (BND-ROOT, non-software)
**Hierarchy Level**: 0
**Requirement References**: R-901

## Changelog
- v1.0 (2026-11-08): Initial generation

## Trigger
A ServiceRequest (root-boundary scope) exists from UC-001, awaiting review.

## Preconditions
- A ServiceRequest exists and has not yet been accepted or rejected

## Main Flow
1. Field Operations Coordinator reviews the ServiceRequest's details (location, urgency, required skill).
2. Coordinator determines whether the request is accepted for scheduling.
3. On acceptance, the request's details are handed off and entered into the dispatch software system (Child Software Boundary, BND-CHILD-SW) as a new, distinct ServiceRequest record scoped to that boundary (see that boundary's own use-case model, not this one).

## Alternative / Exception Paths
- **Request rejected**: Coordinator determines the request cannot be fulfilled (e.g., outside service area); Customer is notified and no handoff to the dispatch system occurs.

## Postconditions
- Either a corresponding software-boundary ServiceRequest now exists in the dispatch system, or the original request is marked rejected with a reason
