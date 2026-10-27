# Domain Concepts — Price Book Management System

**Project**: PRICE-BOOK-TEST-001
**Source**: requirements.json (R-701–R-724)
**Generated**: 2026-10-27

## Domain Entities

### PriceBook
**Description**: Top-level price configuration entity; versioned.
**Attributes**: ID, Description, Version, VersionNumber, BusinessUnit, Company
**Source Requirements**: R-701, R-702, R-706–R-710, R-719–R-721
**Relationships**: Has many PriceCategory

### PriceCategory
**Description**: Organizes prices by Service Line, within a Price Book.
**Attributes**: ID, Version, Description, ServiceLine (multi-select), BookID (FK → PriceBook)
**Source Requirements**: R-703, R-711–R-713
**Relationships**: Belongs to one PriceBook; has many PriceHeader

### PriceHeader
**Description**: Defines parent/child grouping structure to organize Price Items; supports hierarchical nesting via a self-referential parent reference and a depth Level.
**Attributes**: ID, Version, Description, BookID (FK → PriceBook), CategoryID (FK → PriceCategory), ParentHeaderID (FK → PriceHeader, nullable), Level
**Source Requirements**: R-704, R-714–R-716, R-722
**Relationships**: Belongs to one PriceBook and one PriceCategory; may have one parent PriceHeader; has many child PriceHeader; has many PriceItem

### PriceItem
**Description**: The actual price record, containing price values and several business-flag attributes.
**Attributes**: ID, Version, ItemNumber, Description, Price1, Price2, UnitOfMeasure, PriceArea, BookID (FK), CategoryID (FK), HeaderID (FK), Account, BundleCategory, Customer, IsDiscountable, IsDiscontinued, IsProduct, IsInternal, ServiceLine (multi-select), *[two ambiguous flag fields — see Review Needed below]*
**Source Requirements**: R-705, R-717, R-718, R-724
**Relationships**: Belongs to one PriceBook, one PriceCategory, and one PriceHeader

## Cross-Cutting Audit Attributes (all four entities)
Every entity above additionally carries, per R-723:
- EffectiveStartDateTime, EffectiveEndDateTime (Effective Info)
- CurrentVersionLastModifiedUserID, CurrentVersionLastModifiedUserName, CurrentVersionLastModifiedDateTime, CurrentVersionLastOperationType (Currently Version Info)
- OriginalVersionLastModifiedUserID, OriginalVersionLastModifiedUserName, OriginalVersionLastModifiedDateTime, OriginalVersionLastOperationType (Original Version Info)

These are modeled as a shared `VersionAuditInfo` value object (embedded in each entity) rather than four separately-named attribute sets, since the structure is identical across all four entities.

## Business Rules (Domain-Level)

- **ID assignment**: max(existing IDs for type) + 1, system-assigned (R-719)
- **Versioning**: new record starts at version 0; each edit increments by 1 (R-720)
- **Immutability**: ID and Version are read-only post-creation (R-721)
- **Cascading selection**: PriceBook → PriceCategory → PriceHeader → PriceItem, each level's options depend on the parent selection (R-722)

## Review Needed

Two `PriceItem` boolean flag attributes remain unresolved pending stakeholder confirmation (per `sanitization-report.md`'s flagged items) — modeled here as placeholders (`FlagAttribute5`, `FlagAttribute6`) rather than guessed names, to avoid baking an incorrect field name into the domain model.
