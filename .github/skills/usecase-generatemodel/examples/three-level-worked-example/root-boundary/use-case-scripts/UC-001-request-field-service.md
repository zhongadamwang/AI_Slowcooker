# Use Case Script — Request Field Service (UC-001)

**Actor**: Customer (A-001)
**Goal**: Customer requests field work be scheduled, before any software system is involved
**System Boundary**: Root Boundary (BND-ROOT, non-software)
**Hierarchy Level**: 0
**Requirement References**: R-900

## Changelog
- v1.0 (2026-11-08): Initial generation

## Trigger
Customer calls, emails, or otherwise contacts the organization needing field work done.

## Preconditions
- Customer has a service need and organization contact information

## Main Flow
1. Customer describes the needed work and preferred timing to whoever answers the contact channel.
2. The contact record is logged as a ServiceRequest (E-002, root-boundary scope).
3. The ServiceRequest is routed to the Field Operations Coordinator for review (see UC-002).

## Postconditions
- A ServiceRequest exists, scoped to the root boundary, awaiting coordinator review
