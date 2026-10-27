# UI Design Document

**Project**: PRICE-BOOK-TEST-001
**Generated**: 2026-10-27
**Source**: screen-inventory.json, SCR-*/layout-spec.md, SCR-*/mockup.html, interaction-flows.md

## Changelog

- **v1.0** (2026-10-27): Initial consolidated generation

## Overview

This is a price configuration management UI for a services company, covering a four-level hierarchical structure: **Price Book** (top-level, versioned configuration) → **Price Category** (organizes prices by Service Line) → **Price Header** (hierarchical grouping of price items, with parent/child nesting) → **Price Item** (the actual price records, with Price 1/Price 2 values and several business-flag attributes). All four levels share an identical list+tabbed-detail UI pattern (Data / Effective Info / Currently Version Info / Original Version Info), reflecting the original requirements' own repeated description of this structure across every entity. Navigation between the four screens follows a strict drill-down chain matching the business's cascading-selection rule.

## Screens

*(See [screen-inventory.md](screen-inventory.md) for the full standalone inventory — this section summarizes, not duplicates.)*

| Screen | Purpose | UI Model Entry | Layout Spec | Mockup |
|---|---|---|---|---|
| Price Book Management *(SCR-101)* | Manage top-level, versioned price book records | UME-101 | [layout-spec.md](SCR-101/layout-spec.md) | [mockup.html](SCR-101/mockup.html) |
| Price Category Management *(SCR-102)* | Manage Service-Line-organized categories within a selected Price Book | UME-102 | [layout-spec.md](SCR-102/layout-spec.md) | [mockup.html](SCR-102/mockup.html) |
| Price Header Management *(SCR-103)* | Manage hierarchical grouping headers within a selected Book/Category | UME-103 | [layout-spec.md](SCR-103/layout-spec.md) | [mockup.html](SCR-103/mockup.html) |
| Price Item Management *(SCR-104)* | Manage actual price records within a selected Book/Category/Header | UME-104 | [layout-spec.md](SCR-104/layout-spec.md) | [mockup.html](SCR-104/mockup.html) |

## Interaction Flows

*(See [interaction-flows.md](interaction-flows.md) for the full diagram and Verification Log — this section summarizes, not duplicates.)*

- **IF-101**: Price Book → Price Category → Price Header → Price Item — a strict four-level drill-down chain, [full diagram](interaction-flows.md#primary-navigation-flow-if-101)

## Component Notes

All four screens share: a `.list-toolbar` with Add/Copy to Add/Edit/Remove buttons, a `.record-list` table, a `.detail-tabs` four-tab panel (Data/Effective Info/Currently Version Info/Original Version Info), and a `.field--readonly` style for ID/Version fields. SCR-102/103/104 additionally share a `.screen__filter` cascading-dropdown pattern. This consistency was not invented by the generation pipeline — it directly mirrors the source requirements document's own repeated description of an identical structure across all four entities.

## Design Rationale Highlights

- **One consistent layout pattern reused across all four screens**, rather than four different designs, because the source requirements described the exact same list+tabbed-detail structure for every entity — reusing a single pattern most faithfully represents what was actually asked for.
- **Cascading filter chain (Book → Category → Header → Price Area) on Price Item's screen** is the deepest of the four, directly reflecting R-717's explicit multi-level dependency.
- **Two Price Item fields are rendered with a visible `[REVIEW NEEDED]` marker** rather than a guessed name — a deliberate choice carried through from the sanitization stage, to avoid presenting an invented field name as if it were confirmed.

## Known Open Item

Two Price Item boolean flag field names remain unconfirmed (see `sanitization-report.md` and `domain-concepts.md`'s Review Needed sections) — this should be resolved with the real stakeholder before SCR-104's Price Item screen is treated as implementation-ready. All other screens have no outstanding ambiguities.

---
**Traceability**: Summarizes screen-inventory.json (4 screens), interaction-flows.md (1 flow)
**JSON Companion**: [design-document.json](design-document.json)
**Generated**: 2026-10-27T00:00:00Z
