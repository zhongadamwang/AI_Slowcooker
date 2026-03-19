# Sanjel Energy Services

## Pricing Module (Sales Pricing Module)

Business Requirements Document (BRD) and Functional Requirements Document (FRD)

Version: 2.0

Status: Draft – Pending Stakeholder Review

# PART 1: BUSINESS REQUIREMENTS DOCUMENT (BRD)

## 1. Purpose

The purpose of this document is to define the business and functional requirements for the eProgram – Sales Pricing & Costing Module, which enables Sales to perform controlled, job-level pricing and costing within approved programs, while preserving engineering integrity, workflow governance, auditability, and downstream reporting.

## 2. Business Overview

The eProgram Sales Pricing and Costing Module enables Sales to review, modify, finalize, and manage program pricing at the job-type and well level using a centralized digital platform. This module replaces the current Excel-based pricing workflow and provides controlled pricing adjustments, cost transparency, revision control, and reporting capabilities while maintaining engineering design integrity.

The module integrates pricing, costing, reporting, and client program output functionality while supporting structured workflows between Engineering, Sales, and Operations.

The system enables:

- Job-level and well-level pricing management
- Integration with itemized costs and price books
- Controlled pricing adjustments
- Automated revision management
- Automated SharePoint document storage
- Automated reporting and Power BI integration

## 3. Business Objectives



| ID    | Objective                                          |
| ----- | -------------------------------------------------- |
| BO-01 | Provide centralized pricing and costing management |
| BO-02 | Enable PC/PR pricing per job type                  |
| BO-03 | Enable pricing roll-up per well                    |
| BO-04 | Ensure pricing links to itemized cost components   |
| BO-05 | Enable controlled pricing adjustments              |
| BO-06 | Support tracking and audit history                 |
| BO-07 | Enable automated client program printouts          |
| BO-08 | Enable automated SharePoint storage                |
| BO-09 | Enable automated reporting via Power BI            |
| BO-10 | Eliminate Excel dependency for pricing             |



## 4. Business Scope

### In Scope

- Pricing and Costing
- Integrate PC/PR per Job Type within Program Request
- Pricing Linked to Itemized Costs
- Ability to Modify Pricing and PC/PR
- PC/PR Roll-Up per Well Summary
- Power BI Reporting and Bid Analysis
- Program Printout and SharePoint Integration

### Out of Scope

- Price book maintenance
- Contract generation
- Invoicing

## 5. Stakeholders / User Roles



| Stakeholder              | Role                                              |
| ------------------------ | ------------------------------------------------- |
| Sales Team               | Perform pricing and program submission            |
| Engineering Team         | Create and maintain program designs               |
| Accounting / Finance     | Analyze pricing and margins                       |
| Operations Team          | Execute programs and access program documentation |
| IT / Development / Admin | Implement and maintain system                     |



# PART 2: FUNCTIONAL REQUIREMENTS DOCUMENT (FRD)

This FRD follows the functional solution flow: Pricing & costing → PC/PR per job type → Itemized cost linkage → Pricing modification → Per-well rollups → Analytics and Program printouts

## 6. Program Dashboard Functional Requirements

### FR-01: Program List Display

Description: The system shall display a list of programs with the following attributes:

- Program Number
- Company
- Rig
- Area
- Job Types
- Well Name
- Surface Location
- Downhole Location
- Sales Representative
- Comments
- Status (Saved / Need Review)

### FR-02: Filtering & Search

Users shall be able to filter programs by:

- Program Number
- Company
- Sales Rep
- Engineer
- Area / Service Lines
- Job Type

The system shall support expansion to display Job Types.

### FR-03: Job Type Expansion

Each program row shall include an expansion arrow and Print icon. When expanded, the system displays:

- Job Type Name
- Total Revenue
- PC/PR
- PC/TR
- Pricing Status

### FR-04: Job-Level Costing Access

A $ (Costing) icon is available at the Job Type row. When selected:

- Opens pricing for the selected job type only
- Displays detailed breakdown (Services, H&D, Materials, Plugs, Misc.)
- Pricing is performed job-by-job, not program-wide

## 7. Pricing and Costing Functional Requirements

### FR-05: Display Itemized Costs

When pricing is opened, the system shall display:

- Job header information
- Itemized cost groupings:
  - Services
  - Handling & Delivery
  - Lead Cement
  - Tail Cement
  - Plugs
  - Miscellaneous
  - Supplementary Materials / Services

Each item shall display:

- Unit Cost
- Unit Price
- Quantity
- Total Cost
- Total Price

Pricing shall be traceable to itemized cost components.

Pricing source priority:

1. Client-specific price book (Read-only)
2. Sanjel price book (Editable)
3. Sales override

All engineered items are read-only.

### FR-06: Pricing Edit Capability

Sales may modify:

- PC/PR
- Unit Price
- Job Hours
- Distance
- Handling & Delivery Charges
- Supplementary Items
- Miscellaneous Charges

Sales shall NOT modify:

- Cement blends
- Engineering quantities
- Stick diagram / engineering design data

The system shall automatically recalculate totals when pricing is modified.

## 8. Price Book Integration

### FR-07: Pricing Source Priority

- Priority 1: Client-specific price book (Read-only)
- Priority 2: Sanjel price book (Editable)
- Priority 3: Manual override (Sales input)

## 9. PC/PR Calculation

### FR-08: PC/PR Calculation

Formula: `PC/PR = Total Cost ÷ Total Revenue`

Calculated at:

- Line-item level
- Job type level
- Program level
- Well level

Subtotals and totals update in real time when pricing changes.

## 10. PC/TR Calculation

### FR-09: PC/TR Calculation

Formula: `PC/TR = Line-Item Price ÷ Total Program Revenue`

Calculated at:

- Line-item level
- Job type level
- Program level
- Well level

## 11. Pricing Roll-Up

### FR-10: Pricing Roll-Up

- Job Type: Aggregate pricing and costing across line items
- Program: Aggregate across job types
- Well: Aggregate across all job types within a well

### FR-11: Supplementary Notes

Sales may enter auditable notes including:

- Customer-specific notes
- Explanations for adjustments
- Pricing rationale

## 12. Workflow

### FR-12: Save Pricing

- Saves pricing values
- Updates status to Saved
- Does not restart engineering workflow unless thresholds are exceeded

### FR-13: Request Adjustment

Used when engineering changes are required:

- Notifies assigned Engineer
- Status set to Need Review
- Mandatory justification comment required
- Locks pricing until engineering resubmits

### FR-14: Finalize and Approve

- Locks pricing
- Locks program from editing
- Updates status to Finalized

## 13. Revision Control

### FR-15: Revision Numbering

Format:

- `PRG2600098.00` – Original
- `PRG2600098.01` – Revision 1
- `PRG2600098.02` – Revision 2

System tracks revision history and audit trail.

### FR-16: Revision Creation

A new revision is created when changes are requested after approval.

## 14. Program Printout & SharePoint Integration

### FR-17: Client-Facing Program Printout

- Generates PDF including program info, job types, pricing summary, revision number
- Saves printout to SharePoint
- Generates revision-specific printouts

### FR-18: SharePoint Storage

- Printouts are automatically saved
- Accessible to authorized users
- Can be attached to Call Sheet

### FR-19: SharePoint Storage (TBD)

Folder structure to be defined by Operations.

## 15. Power BI Reporting Integration

### FR-20: Power BI Integration

Exports:

- Program Number, Revision, Client, Area, Job Type
- Cost, Revenue, PC/PR, Status

Supports:

- Bid tracking
- Win/Loss analysis
- PC/PR and PC/TR trends
- Revenue and client pricing analysis
- Job and well-level analysis

## 16. Notification Workflow

### FR-21: Pricing Notifications

- Notify Sales when program is ready for pricing
- Notify Engineering when adjustment is requested
- Notify stakeholders when revisions occur

## 17. Status Management

Supported statuses:

- Draft
- Ready for Pricing
- Saved
- Finalized
- Need Review
- Revision in Progress
- Sent to Client

## 18. Validation Rules



| Rule | Description                                    |
| ---- | ---------------------------------------------- |
| VR01 | Only numeric values accepted in pricing fields |
| VR02 | $/t and PC/PR cannot both be blank             |
| VR03 | No negative values allowed                     |
| VR04 | No product or quantity changes allowed         |
| VR05 | Approval state prevents editing                |



## 19. Role-Based Access



| Role        | Access        |
| ----------- | ------------- |
| Sales       | Access        |
| Engineering | Design access |
| Operations  | Read-only     |
| Admin       | Full access   |



## 20. Audit & Traceability

The system records:

- Original vs updated values
- User making the change
- Date/time (timestamp)
- Action type (Save / Request Adjustment)
- Associated notes

## 21. Non-Functional Requirements

- Page load time < 3 seconds
- Realtime recalculation < 1 second
- Dark theme support
- Role-based UI masking
- Support 50–100 job types per program
- Full traceability required

## 22. Assumptions & Risks

### Assumptions

- Pricing calculations are managed by backend services
- Price Book is maintained outside this module

### Risks

- Uncontrolled overrides without enforcement
- Missing approval linkage

## 23. High-Level Workflow

1. Sales opens eService
2. Sales selects Sales Pricing Module
3. Program list is displayed
4. Program is expanded
5. Job Types are displayed
6. Pricing ($) is selected for a Job Type
7. Costing window opens
8. Sales edits PC/PR or $/t
9. Sales selects Save, Request Adjustment, or Finalize and Approve
10. If adjustment is requested, job re-enters engineering review

## 24. Mockups



> Images from the original document are referenced but not embedded in this Markdown version.