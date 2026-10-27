# Requirements Analysis Report

**Project**: PRICE-BOOK-TEST-001
**Source**: Analysis/price-book-test/sanitized-requirements.md
**Generated**: 2026-10-27T00:00:00Z
**Total Requirements**: 24

## Requirements

| ID | Section | Text | Tags | Confidence |
|----|---------|------|---------|------------|
| R-701 | Business Context | The system shall manage a hierarchical price configuration structure: Price Book → Price Category → Price Header → Price Item | functional | 0.95 |
| R-702 | Business Context | Price Book shall be the top-level price configuration entity and shall be versioned | functional | 0.95 |
| R-703 | Business Context | Price Category shall organize prices by Service Line within a Price Book | functional | 0.9 |
| R-704 | Business Context | Price Header shall define parent/child grouping structures to organize Price Items | functional | 0.9 |
| R-705 | Business Context | Price Item shall be the actual price record, containing price values (Price 1, Price 2) and belonging to a specific Price Book, Price Category, and Price Header | functional | 0.9 |
| R-706 | Price Book Management | Users shall be able to view a list of all Price Book records | functional | 0.95 |
| R-707 | Price Book Management | Users shall be able to create a new Price Book via an "Add" action | functional | 0.95 |
| R-708 | Price Book Management | Users shall be able to create a new Price Book by copying an existing one and modifying it (Copy to Add) | functional | 0.9 |
| R-709 | Price Book Management | Users shall be able to edit an existing Price Book | functional | 0.95 |
| R-710 | Price Book Management | Users shall be able to delete (Remove) an existing Price Book | functional | 0.95 |
| R-711 | Price Category Management | Users shall select a Price Book before the system loads associated Price Categories | functional | 0.9 |
| R-712 | Price Category Management | Users shall be able to view, create (Add/Copy to Add), edit, and delete Price Categories | functional | 0.9 |
| R-713 | Price Category Management | When creating a Price Category, users shall select one or more Service Lines from a defined enumeration | functional | 0.85 |
| R-714 | Price Header Management | Users shall select a Price Book, then a Price Category, before the system loads associated Price Headers | functional | 0.9 |
| R-715 | Price Header Management | Price Headers shall support a parent/child grouping structure, including a parent-header reference and a hierarchy-depth level | functional | 0.85 |
| R-716 | Price Header Management | Users shall be able to view, create (Add/Copy to Add), edit, and delete Price Headers | functional | 0.9 |
| R-717 | Price Item Management | Users shall select a Price Book, Price Category, and Price Header (plus optional Price Area filter) before the system loads associated Price Items | functional | 0.9 |
| R-718 | Price Item Management | Users shall be able to view, create (Add/Copy to Add), edit, and delete Price Items | functional | 0.9 |
| R-719 | Business Rules | A new record's ID shall be system-assigned as (current maximum existing ID for that type) + 1 and shall not be user-entered | constraint | 0.95 |
| R-720 | Business Rules | A new record (via Add or Copy to Add) shall default to version 0; each subsequent edit-save shall increment the version by 1 | constraint | 0.95 |
| R-721 | Business Rules | ID and Version fields shall become read-only once a record exists | constraint | 0.9 |
| R-722 | Business Rules | Price Category/Header/Item selection shall follow a cascading dependency (Book → Category → Header → Item) | constraint | 0.9 |
| R-723 | System Capabilities (UI) | Each entity's management screen shall include a list section (with type-specific columns), Add/Copy to Add/Edit/Remove action buttons, a tabbed detail section (Data, Effective Info, Currently Version Info, Original Version Info), and a Close button | functional | 0.85 |
| R-724 | System Capabilities (UI) | Price Item's Data tab shall include several boolean business-flag fields (Is Discountable, Is Discontinued, Is Product, Is Internal, plus two fields flagged as ambiguous in the source transcript) | functional | 0.6 |

## Glossary Suspects
- Price Book
- Price Category
- Price Header
- Price Item
- Service Line
- Price Area
- Currently Version Info
- Original Version Info

## Notes

- **R-724** carries reduced confidence (0.6) specifically because two of its constituent fields were flagged as `[REVIEW NEEDED]` in the sanitization report — this requirement should not be treated as fully resolved until those two field names are confirmed with the real stakeholder or original source.
- Requirement IDs in this test project use the `R-7xx` range to avoid colliding with the toy-order-domain example's `R-614` used in T03/T11's validation fixtures.
