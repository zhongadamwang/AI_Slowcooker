# Screen Inventory

**Project**: PRICE-BOOK-TEST-001
**Generated**: 2026-10-27
**Source**: ui-model.json (price-book-test), requirements.json (R-706–R-724)
**Total Screens**: 4

## Screens

### Price Book Management *(SCR-101)*
**Purpose**: Let a user view, create, copy, edit, and delete Price Book records, including version history metadata
**UI Model Entry**: UME-101
*(Ref: R-706, R-707, R-708, R-709, R-710, R-719, R-720, R-721, R-723)*

### Price Category Management *(SCR-102)*
**Purpose**: Let a user, after selecting a Price Book, view, create, copy, edit, and delete Price Categories organized by Service Line
**UI Model Entry**: UME-102
*(Ref: R-703, R-711, R-712, R-713, R-719, R-720, R-721, R-723)*

### Price Header Management *(SCR-103)*
**Purpose**: Let a user, after selecting a Price Book and Price Category, view, create, copy, edit, and delete hierarchical Price Headers (with parent/child grouping)
**UI Model Entry**: UME-103
*(Ref: R-704, R-714, R-715, R-716, R-719, R-720, R-721, R-722, R-723)*

### Price Item Management *(SCR-104)*
**Purpose**: Let a user, after selecting a Price Book, Price Category, and Price Header, view, create, copy, edit, and delete the actual Price Item records
**UI Model Entry**: UME-104
*(Ref: R-705, R-717, R-718, R-719, R-720, R-721, R-722, R-723, R-724)*

---
**Traceability**: Every screen traces to exactly one UI Model entry and one or more requirements
**Note (real-world pipeline test)**: Each of the four domain entities (PriceBook, PriceCategory, PriceHeader, PriceItem) maps to exactly one management screen, a 1:1 correspondence — this matched the source document's own structure (it described four separate "pages," one per entity), so no splitting or merging decision was needed per `screen-generateinventory`'s Step 1 guidance.
**Generated**: 2026-10-27T00:00:00Z
