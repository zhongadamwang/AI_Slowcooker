<!-- Identifier: V-02 -->

# UI Prototype Skill Development Process Vocabulary

## Canonical Terms and Definitions

### Core Generation Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Screen** | A single distinct view/page in the prototyped UI; the fundamental unit of generation | View, Page | Always traces to a UIModelEntry, never a domain entity directly |
| **Screen Inventory** | The standalone artifact listing all identified screens for a project | Screen List, Prototype Index | Stored in `artifacts/UI Prototype/`, not embedded in the consolidated design document |
| **Layout Specification** | A Markdown document with embedded HTML/CSS code for a single screen, literal enough to guide implementation | Layout Spec | Distinct from a descriptive wireframe — must contain real, usable markup/styling |
| **Interactive Mockup** | A standalone, clickable HTML/JS file a stakeholder can open directly in a browser | Clickable Mockup, Prototype File | Must run via `file://` with zero build step, package manager, or server |
| **Interaction Flow** | A Mermaid-diagrammed model of navigation between screens | Flow Diagram, Navigation Flow | Follows `diagram-generatecollaboration`'s existing Mermaid conventions |
| **Flow/Mockup Consistency Check** | Automated verification that a flow diagram's edges match the mockup's actual clickable transitions | Consistency Gate, Flow Validation | Implemented as a gate check, not a manual review step |

### Domain-UI Alignment Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **UI Model** | A durable, evolving artifact mapping domain entities and their aggregations into UI-facing concepts | UIModel | Not a subtype of the generic `DomainModel` concept — a distinct, derived model that consumes a domain model as input (see `domain-alignment.md` REC-001) |
| **Base UI Model** | The single, role-agnostic UI Model per project that all derived models filter/adapt from | Root UI Model | Exactly one per project |
| **Derived UI Model** | A role/context-scoped UI Model (e.g., Admin, Customer) adapted from the base | Role-Based UI Model | Filtered/adapted view, never independently authored |
| **UI Model Entry** | A single aggregation record within a UI Model — one UI-facing concept and the domain entities it combines | Model Entry | The direct traceability target for Screens |
| **Aggregation** | The conceptual operation by which multiple domain entities combine into one UI-facing concept | Domain Aggregation | Core mechanism the UI Model exists to capture |
| **Co-Evolution** | The requirement that UI Model changes and domain model changes stay synchronized through coordination with `domain-alignentities`/`model-integration` | Synchronized Evolution | Prevents the UI Model from silently diverging from the domain model |
| **Regenerate-on-Change** | The policy that dependent Screens/derived models are regenerated (not merely flagged stale) when their upstream UI Model or base model changes | Auto-Regeneration Policy | Each regeneration appends a Changelog entry |

### Design Document Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Design Document** | The consolidated, human-readable Markdown+HTML/CSS document summarizing screens, flows, components, and rationale | Consolidated Design Doc | Primary deliverable handed to a future developer; does not own screen storage (see Screen Inventory) |
| **Design Rationale** | Captured explanation for why a design decision was made, stored alongside the resulting artifact | Design Justification | Not just the artifact — the reasoning behind it |
| **In-Document Changelog** | A changelog section embedded within a design document, layout spec, or UI Model, recording its own version history | Embedded Changelog | Chosen over relying solely on git history to reconstruct design evolution |

### Discussion & Feedback Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Mockup-Driven Discussion** | Using the literal clickable mockup as the basis for stakeholder conversation, including following observed navigation | Prototype Walkthrough | Observed clicks/paths can surface where the flow diagram needs correction |
| **Feedback Item** | A single piece of structured stakeholder feedback captured during a mockup discussion | Structured Feedback | Routed into `change-management`'s existing structured change-document workflow, not a separate ad-hoc mechanism |
| **Solo-Mode Role-Play** | The developer assuming a stakeholder role perspective during discussion when no real stakeholder is available | Role-Played Review | Assumptions documented inline; applies the existing `process-w5h` solo-mode pattern (Iteration 4) |

### Import & Conformance Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Design Specification** | An externally authored UI design spec, in the same Markdown+HTML/CSS format, imported as a conformance seed | Imported Spec | Parsed into the same internal representation used for generated output |
| **Strict Conformance** | When a design spec is imported, the rule that generation must reuse exactly what's observed, with no invention of divergent styling/terminology | Import Fidelity | Contrast with the default "evolving" component inventory rigor used when no import exists |
| **Component Inventory** | The tracked set of reusable UI components; rigor depends on whether a Design Specification has been imported | Component Library (informal) | `evolving` by default; `strict-conformance` once an import exists |
| **Partial Import / Gap Detection** | Identifying which required screens/flows are not covered by an imported spec | Coverage Gap Analysis | Flags gaps for generation or stakeholder clarification |

## Naming Standards

### File Naming
- Screen inventory: `screen-inventory.md`/`.json` in `artifacts/UI Prototype/`
- UI Model: `ui-model.md`/`.json` alongside `domain-model.md` in `orgModel/[NN] - [Process Name]/`
- Layout specs and mockups: per-screen files within `artifacts/UI Prototype/`

### ID Formats
- Screen IDs: `SCR-[###]` (recommended, not yet enforced — to be finalized during skill design)
- UI Model Entry IDs: `UME-[###]` (recommended, not yet enforced)

## Relationship to Existing Organizational Vocabulary

This vocabulary introduces an entirely new terminology set relative to `orgModel/01 - Skill Development Process/vocabulary.md`, which is scoped to skill/competency development and the general EDPS pipeline. No conflicting definitions were found during alignment (see `artifacts/Analysis/domain-alignment.md`), with one note: this process area's **Flow/Mockup Consistency Check** should stay consistent with the existing **Hierarchy Validation**/**Boundary Validator** convention of pass/fail/warn reporting, rather than introducing a bespoke validation semantics.

## Abbreviations

| Abbreviation | Full Term | Usage Context |
|-------------|-----------|---------------|
| **UI** | User Interface | Throughout this vocabulary |
| **SCR** | Screen | Proposed ID prefix |
| **UME** | UI Model Entry | Proposed ID prefix |
