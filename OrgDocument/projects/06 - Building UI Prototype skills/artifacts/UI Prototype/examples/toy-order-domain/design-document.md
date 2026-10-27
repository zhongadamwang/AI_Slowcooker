# UI Design Document

**Project**: UI-PROTO-VALIDATION-001 *(T11 end-to-end validation run)*
**Generated**: 2026-10-27
**Source**: screen-inventory.json, SCR-*/layout-spec.md, SCR-*/mockup.html, interaction-flows.md

## Changelog

- **v1.0** (2026-10-27): Initial consolidated generation

## Overview

This is a small order-management UI consisting of two connected screens: an **Order Summary** view for reviewing a single order's full detail, and a **Customer Order History** view for browsing all orders placed by a customer and navigating into any one of them. The UI is generated from a toy domain (Customer, Order, LineItem, Product) via a UI Model that aggregates these domain entities into the two screen-facing concepts above.

## Screens

*(See [screen-inventory.md](screen-inventory.md) for the full standalone inventory — this section summarizes, not duplicates.)*

| Screen | Purpose | UI Model Entry | Layout Spec | Mockup |
|---|---|---|---|---|
| Order Summary *(SCR-001)* | Review a single order's full detail (customer, metadata, line items) | UME-001 | [layout-spec.md](SCR-001/layout-spec.md) | [mockup.html](SCR-001/mockup.html) |
| Customer Order History *(SCR-002)* | Browse all of a customer's orders, navigate into any one for detail | UME-003 | [layout-spec.md](SCR-002/layout-spec.md) | [mockup.html](SCR-002/mockup.html) |

## Interaction Flows

*(See [interaction-flows.md](interaction-flows.md) for the full diagram and Verification Log — this section summarizes, not duplicates.)*

- **IF-001**: Order Summary ↔ Customer Order History — [full diagram](interaction-flows.md#primary-navigation-flow-if-001)

## Component Notes

Both screens reuse a consistent `.screen__header` / `.screen__nav-link` pattern for top-level navigation, and a shared `.status-badge` component (with modifier classes `--shipped`/`--delivered`) for order status display. This is an informal, observed pattern — not an enforced design system — consistent with R-604/CON-5's deliberately non-rigorous component-inventory approach for a project with no imported design spec.

## Design Rationale Highlights

- **Two-column layout for Order Summary** (SCR-001): chosen specifically because its UI Model entry (UME-001) aggregates three domain entities (Order, Customer, LineItem) that read better separated into "about this order" vs. "what's in this order" rather than one long vertical list.
- **Plain `<a href>` navigation preferred over JS click handlers** throughout: both screens use real anchor links for all cross-screen navigation, specifically chosen because plain links are simpler for `screen-generateflow` to detect and verify — this held up in practice: the flow diagram's edges were verified via a simple grep-based cross-check against both mockups' actual `href` attributes, with zero ambiguity.

---
**Traceability**: Summarizes screen-inventory.json (2 screens), interaction-flows.md (1 flow)
**JSON Companion**: [design-document.json](design-document.json)
**Generated**: 2026-10-27T00:00:00Z
