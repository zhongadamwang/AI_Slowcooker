# Domain Concepts Analysis

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Generated**: 2026-10-26
**Source**: requirements.md (v1.3), goals.md, w5h-analysis.md
**Total Entities**: 14 | **Total Concepts**: 12

## Domain Areas

### UI Prototype Generation
**Key Entities**: Screen, ScreenInventory, LayoutSpec, InteractiveMockup, InteractionFlow
**Core Concepts**: ScreenGeneration, MockupGeneration, FlowModeling
**Primary Processes**: Screen Inventory Generation, Layout Specification, Mockup Generation, Flow Diagramming

### Domain-UI Alignment
**Key Entities**: UIModel, UIModelEntry, Aggregation
**Core Concepts**: DomainUIAlignment, Aggregation, CoEvolution, RegenerateOnChange
**Primary Processes**: UI Model Generation, Base/Derived Model Derivation, Regeneration on Domain Change

### Design Document Output
**Key Entities**: DesignDocument, Changelog
**Core Concepts**: DesignRationale, InDocumentVersioning
**Primary Processes**: Consolidated Document Assembly, Changelog Maintenance

### Discussion & Feedback
**Key Entities**: FeedbackItem
**Core Concepts**: MockupDrivenDiscussion, ClarifyingQuestion, SoloModeRolePlay
**Primary Processes**: Stakeholder Discussion, Feedback Capture, Change Routing

### Import & Conformance
**Key Entities**: DesignSpecification, ComponentInventory
**Core Concepts**: StrictConformance, PartialImportGapDetection, ImportSourceTraceability
**Primary Processes**: Design Spec Import, Conformance Enforcement, Gap Detection

### EDPS Pipeline Integration
**Key Entities**: GateCheck
**Core Concepts**: OrchestratorRegistration, CollaborationModeAwareness
**Primary Processes**: Gate Validation, DAG Registration, Stakeholder Confirmation

## Entities

### Screen *(ENT-601)*
**Domain Area**: UI Prototype Generation
**Description**: A single distinct view/page in the prototyped UI, the fundamental unit of generation

**Attributes**:
- `screen_id` (identifier): Unique screen identifier
- `name` (string): Human-readable screen name
- `purpose` (string): Why this screen exists, in business terms
- `ui_model_ref` (reference): Link to the UIModelEntry this screen represents *(see R-606, R-628)*
- `requirement_refs` (array): Source requirement IDs justifying this screen *(see R-605)*
- `import_origin` (enumeration): Whether this screen originated from an imported spec or was newly generated [imported, generated] *(see R-618)*

**Operations**:
- `generateLayoutSpec()` → LayoutSpec: Produce the Markdown+HTML/CSS layout document for this screen
- `generateMockup()` → InteractiveMockup: Produce the clickable HTML/JS mockup for this screen
- `regenerate(reason)` → void: Regenerate this screen's artifacts, triggered by a UI Model change *(see R-629a)*

**Source References**: [R-601, R-602, R-602a, R-605, R-606]

### ScreenInventory *(ENT-602)*
**Domain Area**: UI Prototype Generation
**Description**: The standalone artifact listing all identified screens for a project; the entry point into the generated prototype set

**Attributes**:
- `inventory_id` (identifier): Unique inventory identifier
- `screens` (array): List of Screen references
- `generated_at` (timestamp): When this inventory was last produced
- `storage_location` (string): Fixed as `artifacts/UI Prototype/screen-inventory.md`/`.json` *(see R-601, R-601a, D-6)*

**Source References**: [R-601, R-601a]

### LayoutSpec *(ENT-603)*
**Domain Area**: UI Prototype Generation
**Description**: The Markdown document with embedded HTML/CSS code for a single screen — the literal, implementation-guiding artifact

**Attributes**:
- `spec_id` (identifier): Unique layout spec identifier
- `screen_ref` (reference): The Screen this spec belongs to
- `embedded_html` (string): Literal HTML markup for the screen
- `embedded_css` (string): Literal CSS styling for the screen
- `changelog` (array): In-document changelog entries *(see R-610)*
- `design_rationale` (array): Captured rationale for design decisions on this screen *(see R-609)*

**Source References**: [R-602, R-609, R-610]

### InteractiveMockup *(ENT-604)*
**Domain Area**: UI Prototype Generation
**Description**: A standalone, literal, clickable HTML/JS file a stakeholder can open directly in a browser — the "discuss with" artifact

**Attributes**:
- `mockup_id` (identifier): Unique mockup identifier
- `screen_ref` (reference): The Screen this mockup renders
- `file_path` (string): Standalone HTML/JS file location, `file://`-openable *(see R-626)*
- `clickable_transitions` (array): Actual implemented navigation links/JS transitions *(see R-603a)*

**Source References**: [R-602a, R-626]

### InteractionFlow *(ENT-605)*
**Domain Area**: UI Prototype Generation
**Description**: A Mermaid-diagrammed model of navigation/interaction between screens

**Attributes**:
- `flow_id` (identifier): Unique flow identifier
- `mermaid_diagram` (string): The Mermaid source for this flow
- `edges` (array): Screen-to-screen transitions represented in the diagram
- `consistency_status` (enumeration): Result of the automated consistency check against the mockup's actual transitions [consistent, divergent, unchecked] *(see R-603a)*

**Source References**: [R-603, R-603a, R-611a]

### UIModel *(ENT-606)*
**Domain Area**: Domain-UI Alignment
**Description**: The durable, evolving artifact mapping domain entities and their aggregations into UI-facing concepts; stored alongside `domain-model.md`. May exist as one base model plus multiple derived role-based models

**Attributes**:
- `model_id` (identifier): Unique UI Model identifier
- `model_type` (enumeration): Whether this is the base model or a derived model [base, derived] *(see R-630, R-631)*
- `derives_from` (reference, nullable): For derived models, the base UIModel it filters/adapts; null for the base model *(see R-632)*
- `role_scope` (string, nullable): For derived models, the user role/context this model is scoped to (e.g., "Admin", "Customer")
- `entries` (array): UIModelEntry items this model contains
- `storage_location` (string): `orgModel/[NN] - [Process Name]/ui-model.md`/`.json`

**Operations**:
- `syncWithDomainModel()` → void: Co-evolve with `domain-model.md` changes via `domain-alignentities`/`model-integration` *(see R-627a)*
- `propagateChange()` → void: Trigger regeneration of dependent screens/derived models *(see R-629a, R-632)*

**Source References**: [R-627, R-627a, R-629, R-630, R-631, R-632]

### UIModelEntry *(ENT-607)*
**Domain Area**: Domain-UI Alignment
**Description**: A single aggregation record within a UIModel — one UI-facing concept and the domain entities it combines

**Attributes**:
- `entry_id` (identifier): Unique entry identifier
- `ui_concept_name` (string): The UI-facing name for this aggregation (e.g., "Order Summary")
- `domain_entity_refs` (array): Domain entities this entry aggregates (e.g., `Order`, `Customer`, `LineItem`)
- `aggregation_description` (string): How/why these entities combine into this one concept

**Source References**: [R-627, R-628]

### DesignDocument *(ENT-608)*
**Domain Area**: Design Document Output
**Description**: The consolidated, human-readable Markdown+HTML/CSS document summarizing screens, flows, components, and rationale — the primary deliverable handed to a future developer

**Attributes**:
- `document_id` (identifier): Unique design document identifier
- `screens_summary` (array): Summarized references to all Screens
- `flows_summary` (array): Summarized references to all InteractionFlows
- `component_summary` (array): Summarized ComponentInventory contents
- `changelog` (array): In-document changelog, same pattern as LayoutSpec *(see R-610)*
- `json_companion_ref` (reference): Pointer to the machine-readable JSON output *(see R-608)*

**Source References**: [R-607, R-608, R-610]

### FeedbackItem *(ENT-609)*
**Domain Area**: Discussion & Feedback
**Description**: A single piece of structured stakeholder feedback captured during a mockup discussion, destined for `change-management`

**Attributes**:
- `feedback_id` (identifier): Unique feedback identifier
- `screen_ref` (reference): The Screen this feedback concerns
- `feedback_text` (string): The structured feedback statement (e.g., "change field Y from optional to required")
- `source_mode` (enumeration): Whether this was given by a real stakeholder or role-played [real, role-played] *(see R-614)*
- `change_management_ref` (reference, nullable): Link to the resulting `change-management` structured change document, once routed *(see R-612, R-620)*

**Source References**: [R-612, R-614, R-620]

### DesignSpecification *(ENT-610)*
**Domain Area**: Import & Conformance
**Description**: An externally authored UI design spec, in the same Markdown+HTML/CSS format, imported as a conformance seed

**Attributes**:
- `spec_id` (identifier): Unique imported spec identifier
- `source_screens` (array): Screens/components parsed from the import
- `coverage_gaps` (array): Required screens/flows *not* covered by this import *(see R-617)*
- `imported_at` (timestamp): When this spec was imported

**Source References**: [R-615, R-616, R-617, R-618]

### ComponentInventory *(ENT-611)*
**Domain Area**: Import & Conformance
**Description**: The tracked set of reusable UI components (buttons, forms, cards, nav patterns); rigor depends on whether a DesignSpecification has been imported

**Attributes**:
- `inventory_id` (identifier): Unique component inventory identifier
- `components` (array): Named component entries observed or generated
- `rigor_mode` (enumeration): Governs whether new components may be freely invented or must strictly match the import [evolving, strict-conformance] *(see R-604, R-616, D-8)*

**Source References**: [R-604, R-616]

### GateCheck *(ENT-612)*
**Domain Area**: EDPS Pipeline Integration
**Description**: A validation check run by `edps-workflow-orchestrator` against this skill set's outputs, including the new automated flow/mockup consistency check and mode-aware stakeholder confirmation

**Attributes**:
- `check_id` (identifier): Unique gate check identifier
- `check_type` (enumeration): Includes the new `flow_mockup_consistency` type alongside existing types (artifact_existence, content_pattern, json_schema, stakeholder_confirmation) *(see R-603a, R-622)*
- `severity` (enumeration, mode-resolved for stakeholder_confirmation type): [hard, soft]

**Source References**: [R-603a, R-621, R-622]

### Changelog *(ENT-613)*
**Domain Area**: Design Document Output
**Description**: The reusable in-document versioning pattern applied to every design document, layout spec, and UI Model — not a standalone file, but a required structural element within other entities

**Attributes**:
- `entries` (array): Ordered list of version entries, each with version number, date, and change description
- `owner_entity_ref` (reference): Which entity (DesignDocument, LayoutSpec, UIModel) this changelog belongs to

**Source References**: [R-610, R-629a]

### Aggregation *(ENT-614)*
**Domain Area**: Domain-UI Alignment
**Description**: The conceptual relationship/operation by which multiple domain entities combine into a single UI-facing concept; the core mechanism the UIModel exists to capture (modeled as a first-class concept here because it's referenced throughout, not merely an attribute of UIModelEntry)

**Attributes**:
- `aggregation_id` (identifier): Unique aggregation identifier
- `member_entities` (array): Domain entities being combined
- `resulting_ui_concept` (reference): The UIModelEntry this aggregation produces

**Source References**: [R-627, R-628]

## Business Concepts

### ScreenGeneration *(CON-601)*
**Domain Area**: UI Prototype Generation
**Definition**: The process of deriving a complete screen inventory and per-screen layout specs from requirements and UI Model input
**Synonyms**: prototype generation, screen derivation
**Source References**: [R-601, R-602]

### MockupGeneration *(CON-602)*
**Domain Area**: UI Prototype Generation
**Definition**: The process of producing a literal, standalone, clickable HTML/JS file per screen or flow
**Synonyms**: prototype rendering, clickable mockup creation
**Source References**: [R-602a, R-626]

### FlowModeling *(CON-603)*
**Domain Area**: UI Prototype Generation
**Definition**: Representing navigation/interaction between screens as a Mermaid diagram, kept consistent with the actual mockup's transitions
**Synonyms**: interaction modeling, navigation flow diagramming
**Source References**: [R-603, R-603a]

### DomainUIAlignment *(CON-604)*
**Domain Area**: Domain-UI Alignment
**Definition**: The overarching practice of keeping UI-facing concepts traceable to and synchronized with the underlying domain model, via the UI Model
**Synonyms**: domain-UI traceability, model alignment
**Source References**: [R-606, R-627, R-628]

### CoEvolution *(CON-605)*
**Domain Area**: Domain-UI Alignment
**Definition**: The requirement that UI Model changes and domain model changes stay synchronized through coordination with existing modeling skills, rather than evolving independently
**Synonyms**: synchronized evolution, model co-maintenance
**Source References**: [R-627a]

### RegenerateOnChange *(CON-606)*
**Domain Area**: Domain-UI Alignment
**Definition**: The policy that screens/derived models are regenerated (not merely flagged stale) when their upstream UI Model or base model changes
**Synonyms**: auto-regeneration policy, propagated regeneration
**Source References**: [R-629a, R-632]

### DesignRationale *(CON-607)*
**Domain Area**: Design Document Output
**Definition**: Captured explanation for *why* a design decision was made, stored alongside the resulting artifact rather than only the artifact itself
**Synonyms**: design justification, decision log
**Source References**: [R-609]

### InDocumentVersioning *(CON-608)*
**Domain Area**: Design Document Output
**Definition**: The practice of each design document carrying its own changelog section, rather than relying solely on git history to reconstruct design evolution
**Synonyms**: embedded changelog, self-documenting versioning
**Source References**: [R-610]

### MockupDrivenDiscussion *(CON-609)*
**Domain Area**: Discussion & Feedback
**Definition**: Using the literal clickable mockup as the basis for stakeholder conversation, including following their actual observed navigation/clicks
**Synonyms**: prototype walkthrough, click-driven review
**Source References**: [R-611, R-611a]

### SoloModeRolePlay *(CON-610)*
**Domain Area**: Discussion & Feedback
**Definition**: The practice of the developer assuming a stakeholder role perspective when discussing the prototype in solo collaboration mode, with assumptions documented inline
**Synonyms**: role-played review, self-attested stakeholder review
**Source References**: [R-614]

### StrictConformance *(CON-611)*
**Domain Area**: Import & Conformance
**Definition**: When a design spec is imported, the rule that generation must reuse exactly what is observed in the import, with no new or divergent styling/terminology introduced
**Synonyms**: strict reuse, import fidelity
**Source References**: [R-616]

### PartialImportGapDetection *(CON-612)*
**Domain Area**: Import & Conformance
**Definition**: The process of identifying which required screens/flows are not covered by an imported design spec, flagging them for generation or clarification
**Synonyms**: coverage gap analysis, import completeness check
**Source References**: [R-617]

## Terminology Glossary

| Term | Definition | Domain Area | Context |
|------|------------|-------------|---------|
| Base UI Model | The single, role-agnostic UI Model per project that all derived models filter/adapt from | Domain-UI Alignment | Model hierarchy root |
| Derived UI Model | A role/context-scoped UI Model (e.g., Admin, Customer) adapted from the base | Domain-UI Alignment | Model hierarchy leaf |
| Stakeholder Confirmation (gate check type) | Existing EDPS gate check type (from Iteration 4) whose severity resolves based on `collaboration_mode`; reused here rather than reinvented | EDPS Pipeline Integration | Cross-references T03 of Iteration 4 |
| Collaboration Mode | Existing EDPS project setting (`solo`\|`traditional`) governing stakeholder-confirmation mechanics; this project currently runs in `solo` mode | EDPS Pipeline Integration | Cross-references Iteration 4 |
| `file://` portability | The requirement that mockups open directly from the local filesystem with no server | UI Prototype Generation | NFR, R-626 |

## Entity Relationships

### Screen ↔ UIModelEntry *(REL-601)*
**Type**: Traceability (many-to-one)
**Description**: Each screen references exactly one UIModelEntry as its primary traceability target, rather than referencing domain entities directly
**Source**: [R-606, R-628]

### UIModelEntry ↔ Aggregation *(REL-602)*
**Type**: Composition (one-to-one)
**Description**: Each UIModelEntry is produced by exactly one Aggregation operation combining domain entities
**Source**: [R-627, R-628]

### UIModel (derived) ↔ UIModel (base) *(REL-603)*
**Type**: Derivation (many-to-one)
**Description**: Every derived UIModel traces back to and is filtered/adapted from the single base UIModel
**Source**: [R-630, R-631, R-632]

### Screen ↔ LayoutSpec *(REL-604)*
**Type**: Composition (one-to-one)
**Description**: Each screen has exactly one corresponding layout specification
**Source**: [R-602]

### Screen ↔ InteractiveMockup *(REL-605)*
**Type**: Composition (one-to-one)
**Description**: Each screen has exactly one corresponding interactive mockup
**Source**: [R-602a]

### InteractionFlow ↔ InteractiveMockup *(REL-606)*
**Type**: Consistency Validation (many-to-many)
**Description**: Flow diagram edges are automatically checked against mockup transitions via GateCheck
**Source**: [R-603a]

### FeedbackItem ↔ Screen *(REL-607)*
**Type**: Reference (many-to-one)
**Description**: Feedback items concern a specific screen under discussion
**Source**: [R-612]

### DesignSpecification ↔ Screen *(REL-608)*
**Type**: Origin (one-to-many)
**Description**: An imported design specification may be the origin for one or more generated screens; import-origin is tracked per screen
**Source**: [R-615, R-618]

### ScreenInventory ↔ Screen *(REL-609)*
**Type**: Composition (one-to-many)
**Description**: A screen inventory contains all screens for the project
**Source**: [R-601]

### DesignDocument ↔ Screen, InteractionFlow, ComponentInventory *(REL-610)*
**Type**: Aggregation/Summary (one-to-many)
**Description**: The consolidated design document summarizes all screens, flows, and components, without being their sole storage location (see D-6: screen inventory is standalone)
**Source**: [R-607]

## Domain Analysis Summary

### Core Domain Structure
This project's domain splits cleanly into three layers: **Domain-UI Alignment** (UIModel, UIModelEntry, Aggregation) sits between the pre-existing domain model and the **UI Prototype Generation** layer (Screen, LayoutSpec, InteractiveMockup, InteractionFlow); **Design Document Output** and **Discussion & Feedback** are consumer-facing layers built on top of generation; **Import & Conformance** and **EDPS Pipeline Integration** are cross-cutting concerns that modify how generation and discussion behave rather than being independent layers.

### Key Entity Patterns
- **Traceability Chain**: `Requirement → Aggregation → UIModelEntry → Screen → (LayoutSpec, InteractiveMockup)` — every generated artifact has an unbroken path back to a requirement, per R-605/R-606/R-628
- **Base/Derived Pattern**: UIModel is the first entity in this project's domain to need an explicit base/derived relationship (REL-603) — mirrors how `domain-model.md` itself might one day need role-scoped views, worth watching as a reusable pattern
- **Regeneration as a First-Class Concern**: RegenerateOnChange (CON-606) isn't a side effect but a modeled policy, because D-11's decision explicitly rejected a "flag stale" alternative — regeneration behavior deserves its own attention in later skill design, not just a Screen method
- **Reused, Not Reinvented, Pipeline Concepts**: GateCheck and CollaborationMode are intentionally *referenced* from Iteration 3/4 rather than remodeled here — this project's domain model should stay small and not duplicate concepts that already exist elsewhere in the framework

### Critical Relationships
- Screen never references a domain entity directly (CON-8 in goals.md) — all traceability routes through UIModelEntry
- FeedbackItem is the connective tissue to `change-management` — not modeled here as owning the full change-document schema, since that already belongs to `change-management`'s own domain
- DesignSpecification's `coverage_gaps` field is where R-617's "partial import" requirement becomes concrete data, not just a described behavior

### Domain Complexity Assessment
**High Complexity Areas**:
- Domain-UI Alignment (UIModel/UIModelEntry/Aggregation) — base/derived relationships, co-evolution with existing skills, regeneration propagation
- UI Prototype Generation — five tightly coupled entities (Screen, ScreenInventory, LayoutSpec, InteractiveMockup, InteractionFlow) with a consistency-checking relationship between two of them

**Medium Complexity Areas**:
- Import & Conformance — conditional behavior (strict vs. evolving) based on DesignSpecification presence
- EDPS Pipeline Integration — mostly a reference/reuse of existing Iteration 3/4 concepts rather than new complexity

**Lower Complexity Areas**:
- Discussion & Feedback — FeedbackItem is a relatively simple structured-capture entity, with the heavy lifting delegated to `change-management`
- Design Document Output — mostly a summarization/assembly layer over already-modeled entities

---
**Traceability**: Extracted from requirements R-601–R-632 and w5h-analysis.md (`artifacts/Analysis/requirements.md` v1.3)
**Confidence Score**: 0.88/1.0 — high confidence on entities directly named in requirements (Screen, UIModel, InteractiveMockup); medium confidence on relationship cardinalities for the base/derived UIModel pattern, since no real example has been generated yet to validate against
**Generated**: 2026-10-26

## Next Steps for Domain Modeling

### Immediate Actions
1. **Entity Validation**: Review this domain model, especially the UIModel/UIModelEntry/Aggregation split — confirm it's not over-modeling a concept that could be simpler in practice
2. **Relationship Refinement**: Validate the base/derived UIModel cardinality (REL-603) once a real multi-role example exists
3. **Resolve OQ-G5's practical mechanics**: now that domain-extractconcepts is complete, the co-evolution relationship with `domain-alignentities`/`model-integration` (R-627a) needs a concrete integration contract — likely the next real design question

### Downstream Integration
- **domain-alignentities**: Should review this domain-concepts.md to confirm compatibility before UI Model generation is actually implemented, per R-627a's co-evolution requirement
- **process-scopemin**: Recommended next step — this domain model is intentionally broad (14 entities); `process-scopemin` should identify which of these are true v1 MVP vs. deferred (candidates for deferral: derived/role-based UIModel support, the automated flow/mockup consistency GateCheck, partial-import gap detection)
- **diagram-generatecollaboration**: Once scope is settled, generate a collaboration diagram visualizing how these entities interact
