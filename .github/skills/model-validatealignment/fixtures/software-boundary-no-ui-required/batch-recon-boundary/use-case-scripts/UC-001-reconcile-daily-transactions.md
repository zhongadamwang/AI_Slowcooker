# Use Case Script — Reconcile Daily Transactions (UC-001)

**Actor**: Nightly Scheduler (A-001)
**Goal**: Nightly Scheduler triggers reconciliation of the day's transactions against the ledger
**System Boundary**: Batch Reconciliation Boundary (BND-BATCH-RECON, software)
**Hierarchy Level**: 0
**Requirement References**: R-700

## Trigger
The nightly schedule fires.

## Preconditions
- The day's Transactions (E-020) are closed

## Main Flow
1. The scheduler starts the reconciliation job.
2. The system matches each Transaction (E-020) to a LedgerEntry (E-021).
3. The system records unmatched Transactions for follow-up.

## Postconditions
- Every Transaction is marked matched or unmatched
