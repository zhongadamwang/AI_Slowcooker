# UI Design Document

**Project**: PRICE-BOOK-TEST-001
**Generated**: 2026-11-01
**Source**: screen-inventory.json, SCR-*/layout-spec.md, SCR-*/mockup.html, interaction-flows.md

## Changelog

- **v1.0** (2026-10-27): Initial consolidated generation
- **v1.1** (2026-11-01): Reconciled the handoff with the recreated prototypes, verified flows, responsive behavior, and browser test results.

## Overview

Northstar Pricing is a browser-based prototype for managing a service company's four-level price configuration: Price Books contain Price Categories, which contain hierarchical Price Headers, which contain Price Items. Users can review and maintain sample records through a consistent list-and-detail interface, use cascading filters to narrow child records, and move between levels with the progression links. The prototype is a local interaction model, not a connected pricing system.

## Screens

*(See [screen-inventory.md](screen-inventory.md) for the full standalone inventory — this section summarizes, not duplicates.)*

| Screen | Purpose | UI Model Entry | Layout Spec | Mockup |
|---|---|---|---|---|
| Price Book Management *(SCR-101)* | Manage top-level, versioned price book records | UME-101 | [layout-spec.md](SCR-101/layout-spec.md) | [mockup.html](SCR-101/mockup.html) |
| Price Category Management *(SCR-102)* | Manage Service-Line-organized categories within a selected Price Book | UME-102 | [layout-spec.md](SCR-102/layout-spec.md) | [mockup.html](SCR-102/mockup.html) |
| Price Header Management *(SCR-103)* | Manage hierarchical grouping headers within a selected Book and Category | UME-103 | [layout-spec.md](SCR-103/layout-spec.md) | [mockup.html](SCR-103/mockup.html) |
| Price Item Management *(SCR-104)* | Manage price records within a selected Book, Category, and Header | UME-104 | [layout-spec.md](SCR-104/layout-spec.md) | [mockup.html](SCR-104/mockup.html) |

## Interaction Flows

*(See [interaction-flows.md](interaction-flows.md) for the complete diagrams and Verification Log.)*

- **IF-101**: Price Book → Price Category → Price Header → Price Item navigation — [verified flow](interaction-flows.md#if-101)
- **IF-102**: Shared record create, copy, edit, validation, discard, and remove states — [verified flow](interaction-flows.md#if-102)

## Component Notes

All screens use the same Northstar shell, progression navigation, record-action toolbar, scroll-contained data table, tabbed detail card, status messaging, and accessible remove-confirmation dialog. SCR-102 through SCR-104 add progressively deeper cascading selectors. On narrow screens the page remains within the viewport while wide tables and tab strips scroll within their own containers.

## Design Rationale Highlights

- A shared list-and-detail pattern across the four entities reflects the repeated structure in the source requirements and keeps the journey consistent.
- Cascading filters expose the parent-child dependencies directly. SCR-103 also computes a nested header's level from its selected parent.
- The two unresolved Price Item flag names remain visibly marked `[REVIEW NEEDED]` and disabled rather than guessed.

## Prototype Guide

- **Entry point**: Open [SCR-101/mockup.html](SCR-101/mockup.html) directly in a modern browser. Keep the four `SCR-###` directories together so relative navigation links continue to resolve.
- **Primary journey**: Follow the progression navigation from Price Book to Category, Header, and Item. Back links and browser history were exercised.
- **Visual and interaction references**: See [SCR-101 visual design](SCR-101/layout-spec.md#visual-design), all four layout specs, and the [verified interaction flows](interaction-flows.md).
- **Verified behavior**: Browser interactions covered add, copy, edit, required-description validation, version changes, close/discard, removal confirmation, cancellation and Escape dismissal, filter behavior, and navigation. Responsive layouts were visually reviewed at 375x844 and 1440x900.
- **Limitations**: Records are in-memory sample data and reset on reload. No backend, persistence, or external resources are connected. The two unresolved Price Item flag fields remain disabled until their names are confirmed.
- **Open issue**: Confirm the two Price Item flag names with the business stakeholder before treating SCR-104 as implementation-ready.

## Handoff Check

Read this document as a developer unfamiliar with the generation session. The overview establishes the domain hierarchy and prototype boundary, each screen row explains its purpose and links to implementation detail, and the guide identifies the entry page, tested journey, verified behavior, limitations, and unresolved fields without relying on conversation history.

---
**Traceability**: Summarizes screen-inventory.json (4 screens) and interaction-flows.md (2 verified flows).
**JSON Companion**: [design-document.json](design-document.json)
**Generated**: 2026-11-01T14:07:40-06:00
