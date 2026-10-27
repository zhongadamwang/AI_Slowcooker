# Sanitized Requirements — Price Book Management System

**Source**: `Source Materials/price-book-test/raw-dictated-requirements.md` (raw dictated transcript, unpunctuated)
**Sanitization Mode**: `transform`
**Target Domain**: Price Book / Price Configuration Management

## Business Context

The system manages a hierarchical price configuration structure for a services company (referred to in the source as "the Sanjel company"). Price configuration is organized into four levels:

1. **Price Book** — the top-level price configuration entity, versioned
2. **Price Category** — organizes prices by service line, within a Price Book
3. **Price Header** — defines parent/child grouping structures to organize Price Items, within a Price Book and Price Category
4. **Price Item** — the actual price record containing price values (Price 1, Price 2), belonging to a specific Price Book, Price Category, and Price Header

## Actors and Stakeholders

- **User** (pricing administrator / configuration manager) — creates, views, copies, edits, and deletes records at every level of the hierarchy

## Business Processes

### Price Book Management
- User can view a list of all Price Book records
- User can create a new Price Book (via "Add")
- User can create a new Price Book by copying an existing one and modifying it (via "Copy to Add")
- User can edit an existing Price Book
- User can delete ("Remove") an existing Price Book
- When a Price Book is created via "Add," its ID is system-assigned as (current maximum ID + 1); its version defaults to 0
- When a Price Book is created via "Copy to Add," the selected record's data is copied into an editable form for modification, then saved as a new record (new ID, version 0)
- When an existing Price Book is edited and saved, its version number increments by 1 (e.g., version 0 → version 1)

### Price Category Management
- User selects a Price Book first; the system then loads the Price Categories associated with that Price Book
- User can view, create, copy, edit, and delete Price Categories (same Add / Copy to Add / Edit / Remove pattern as Price Book)
- When creating a Price Category, the user selects one or more **Service Lines** that the category applies to (see Business Rules for the Service Line list)
- ID and version fields are read-only after creation; version increments by 1 on each edit-save

### Price Header Management
- User selects a Price Book, then a Price Category; the system loads the Price Headers associated with that selection
- Price Headers support a **parent/child grouping structure** (a Price Header may have a parent Price Header, enabling hierarchical/nested organization) and track a **level** indicating depth in that hierarchy
- User can view, create, copy, edit, and delete Price Headers (same Add / Copy to Add / Edit / Remove pattern)
- ID and version fields are read-only after creation; version increments by 1 on each edit-save

### Price Item Management
- User selects a Price Book, Price Category, and Price Header; the system loads the Price Items associated with that selection (additional filtering by price area is also supported)
- A Price Item represents the actual price record and includes values such as Price 1 and Price 2, a unit of measure, and several business-flag attributes (see System Capabilities)
- User can view, create, copy, edit, and delete Price Items (same Add / Copy to Add / Edit / Remove pattern)
- ID and version fields are read-only after creation; version increments by 1 on each edit-save

## Business Rules

- **Service Line enumeration** (used when categorizing a Price Category): Acidization, CBM Coil Tubing, CBM Nitrogen, CO2, Coiled Tubing, Corporate Management, E-Line, Coil Fracturing, Industrial Services, Infrastructure, Interco Billing, MPCT Nitrogen, Nitrogen Coil, Nitrogen Fracturing, Operations, Primary Cementing, Pumping, Remedial Cementing, Technical Services
- **ID assignment rule**: a new record's ID is always (current maximum existing ID for that record type) + 1, and is system-assigned, not user-entered
- **Version rule**: a new record (via Add or Copy to Add) always starts at version 0; each subsequent edit-save increments the version by 1
- **Read-only field rule**: once a record exists, its ID and Version fields become read-only and cannot be directly edited by the user
- **Hierarchical dependency rule**: Price Category selection requires a Price Book to be selected first; Price Header selection requires both a Price Book and Price Category; Price Item selection requires a Price Book, Price Category, and Price Header

## System Capabilities

### Common pattern across all four entity types (Price Book, Price Category, Price Header, Price Item)
Each entity's management page/screen includes:
- A **list section** displaying existing records in a table (columns vary per entity type — see below)
- A set of **action buttons**: Add, Copy to Add, Edit, Remove
- A **detail section** below the list, organized into tabs:
  - **Data tab** — the entity's core fields (varies per entity type)
  - **Effective Info tab** — Start Date/Time, End Date/Time
  - **Currently Version Info tab** — Last Modified User ID, Last Modified User Name, Last Modified Date/Time, Last Operation Type
  - **Original Version Info tab** — Last Modified User ID, Last Modified User Name, Last Modified Date/Time, Last Operation Type
- A **Close** button to close the page

### Price Book
- **List columns**: ID, Version, Description, Version Number, Company
- **Data tab fields**: ID, Description, Version Number, Business Unit

### Price Category
- **Filter**: Price Book dropdown (with a Clear button to reselect)
- **List columns**: ID, Version, Description, Book ID
- **Data tab fields**: ID, Version, Price Book, Description, Service Line

### Price Header
- **Filter**: Price Book filter, Category filter (cascading — category options depend on selected Price Book)
- **List columns**: ID, Version, Description, Book ID, Category ID, Parent Header ID, Level
- **Data tab fields**: ID, Version, Price Book, Description, Category, Price Header (parent reference)

### Price Item
- **Filter**: Price Book, Category, Price Header, Price Area (custom filter)
- **List columns**: ID, Version, Item Number, Description, Price 1, Price 2, Unit of Measure, Book ID, Category ID, Header ID, Price Area
- **Data tab fields**: ID, Version, Price Book, Description, Category, Price Header, Item Number, Account, Bundle Category, Description, Price 1, Price 2, Unit of Measure, Price Area, Customer, Is Discountable (flag), Is Discontinued (flag), Is Taxable/Charge-related (flag — transcription unclear, flagged for review), Is Deep Charge (flag — transcription unclear, flagged for review), Is Product (flag), Is Internal (flag), Service Line (supports multi-select)

## Quality and Compliance Expectations

*(None explicitly stated in the source document.)*

## Out of Scope

*(None explicitly stated in the source document.)*

---

## Items Flagged for Review

Several Price Item data-tab field names were ambiguous in the raw dictated transcript and could not be confidently transcribed. These are preserved above with a `[REVIEW NEEDED]` style flag inline ("Is Taxable/Charge-related," "Is Deep Charge") rather than guessed at — **a real stakeholder (or, in solo mode, the developer self-attesting with lower confidence) should confirm the exact intended field names and semantics** before these are treated as final for implementation. This is a case where solo self-validation per `requirements-sanitize`'s Quality Checks is **not** sufficient, since the actual words are genuinely unclear from the source audio/transcript, not just informally phrased.
