# Use Case Script — Apply Discount (UC-001)

**Actor**: Billing Clerk (A-001)
**Goal**: Billing Clerk applies a discount to an invoice
**System Boundary**: Billing Boundary (BND-BILLING, software)
**Hierarchy Level**: 0
**Requirement References**: R-500

## Trigger
A customer presents a discount code for an open Invoice (E-010).

## Preconditions
- The Invoice is not yet paid

## Main Flow
1. Billing Clerk opens the Invoice.
2. Billing Clerk enters the discount code.
3. The system reduces the Invoice total.

## Postconditions
- The Invoice total reflects the discount
