# Use Case Script — Review Pending Item (UC-001)

**Actor**: Operator (A-001)
**Goal**: Operator reviews a pending item
**System Boundary**: Unclassified Boundary (BND-UNCLASSIFIED, unknown)
**Hierarchy Level**: 0
**Requirement References**: R-900

## Trigger
A PendingItem (E-900) is waiting for review.

## Preconditions
- At least one PendingItem exists

## Main Flow
1. Operator opens the pending item.
2. Operator records a decision.

## Postconditions
- The PendingItem has a recorded decision
