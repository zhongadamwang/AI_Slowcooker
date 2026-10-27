# Collaboration Diagrams

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Generated**: 2026-10-26
**Source**: domain-concepts.md, requirements.md (v1.3), domain-alignment.md

## Domain Class Model

### Entity Relationship Overview *(Diagram D-601)*
**Source Requirements**: [R-601, R-602, R-602a, R-603, R-606, R-627, R-628]
**Domain Source**: `orgModel/02 - UI Prototype Skill Development Process/domain-model.md`

```mermaid
classDiagram
    class Screen:::core {
        +screen_id: String
        +name: String
        +purpose: String
        +ui_model_ref: UIModelEntry
        +requirement_refs: String[]
        +import_origin: String
        +generateLayoutSpec()
        +generateMockup()
        +regenerate(reason)
    }

    class ScreenInventory:::entity {
        +inventory_id: String
        +screens: Screen[]
        +storage_location: String
    }

    class LayoutSpec:::entity {
        +spec_id: String
        +embedded_html: String
        +embedded_css: String
        +changelog: Changelog
        +design_rationale: String[]
    }

    class InteractiveMockup:::entity {
        +mockup_id: String
        +file_path: String
        +clickable_transitions: String[]
    }

    class InteractionFlow:::entity {
        +flow_id: String
        +mermaid_diagram: String
        +edges: String[]
        +consistency_status: String
    }

    class UIModel:::control {
        +model_id: String
        +model_type: String
        +derives_from: UIModel
        +role_scope: String
        +entries: UIModelEntry[]
        +syncWithDomainModel()
        +propagateChange()
    }

    class UIModelEntry:::core {
        +entry_id: String
        +ui_concept_name: String
        +domain_entity_refs: String[]
        +aggregation_description: String
    }

    class Aggregation:::ai {
        +aggregation_id: String
        +member_entities: String[]
        +resulting_ui_concept: UIModelEntry
    }

    class DesignDocument:::entity {
        +document_id: String
        +changelog: Changelog
        +json_companion_ref: String
    }

    class Changelog:::entity {
        +entries: String[]
        +owner_entity_ref: String
    }

    class FeedbackItem:::entity {
        +feedback_id: String
        +feedback_text: String
        +source_mode: String
        +change_management_ref: String
    }

    class DesignSpecification:::entity {
        +spec_id: String
        +coverage_gaps: String[]
        +imported_at: DateTime
    }

    class ComponentInventory:::entity {
        +inventory_id: String
        +components: String[]
        +rigor_mode: String
    }

    Screen "many" --> "1" UIModelEntry : traces to
    UIModelEntry "1" --> "1" Aggregation : produced by
    UIModel "many (derived)" --> "1" UIModel : base
    Screen "1" --> "1" LayoutSpec : has
    Screen "1" --> "1" InteractiveMockup : has
    InteractionFlow "many" --> "many" InteractiveMockup : consistency-checked against
    FeedbackItem "many" --> "1" Screen : concerns
    DesignSpecification "1" --> "many" Screen : origin of
    ScreenInventory "1" --> "many" Screen : contains
    DesignDocument "1" --> "many" Screen : summarizes
    DesignDocument "1" --> "many" InteractionFlow : summarizes
    DesignDocument "1" --> "1" ComponentInventory : summarizes

    %% Styling Definitions
    classDef core fill:#e1f5fe
    classDef entity fill:#f3e5f5
    classDef control fill:#fce4ec
    classDef ai fill:#e8f5e8
```

**Note**: This class diagram is identical in substance to the one already embedded in `orgModel/02 - UI Prototype Skill Development Process/domain-model.md`; it is duplicated here per `diagram-generatecollaboration`'s own convention of keeping a project-level analysis copy alongside the organizational-model copy, so this project's `artifacts/Analysis/` folder is self-contained for review purposes.

## Developer–System Interactions

### MVP Generation Flow *(Diagram D-602)*
**Source Requirements**: [R-601, R-602, R-602a, R-603, R-606, R-627]
**Entities Involved**: Solo Developer, UIModel, Screen, LayoutSpec, InteractiveMockup, InteractionFlow

```mermaid
sequenceDiagram
    participant Dev as Solo Developer
    participant UM as UIModel
    participant SCR as Screen
    participant LS as LayoutSpec
    participant IM as InteractiveMockup
    participant IF as InteractionFlow

    Dev->>UM: Generate base UI Model (from domain-model.md)
    UM-->>Dev: UIModelEntry set (aggregations)
    Dev->>SCR: Generate ScreenInventory from UIModelEntry set
    loop For each Screen
        SCR->>LS: generateLayoutSpec()
        LS-->>SCR: Markdown + embedded HTML/CSS
        SCR->>IM: generateMockup()
        IM-->>SCR: Standalone clickable HTML/JS file
    end
    Dev->>IF: Model interaction flows across generated Screens
    IF-->>Dev: Mermaid diagram (edges match mockup transitions)

    Note over LS,IM: Both trace back to the same Screen and UIModelEntry
    Note over Dev,IF: Manual review of flow/mockup consistency in MVP (R-603a automated check deferred to Phase 2)
```

### Mockup-Driven Discussion Flow *(Diagram D-603)*
**Source Requirements**: [R-611, R-611a, R-612, R-614, R-620]
**Entities Involved**: Business/Product Stakeholder (or role-played), InteractiveMockup, FeedbackItem, change-management (external skill)

```mermaid
sequenceDiagram
    participant S as Stakeholder (real or role-played)
    participant IM as InteractiveMockup
    participant FB as FeedbackItem
    participant CM as change-management (external)

    S->>IM: Click through screens
    IM-->>S: Observed navigation / actual behavior
    alt Observed nav diverges from InteractionFlow
        S->>FB: Flag flow correction needed
    end
    S->>FB: Give structured feedback (e.g., "make field Y required")
    FB->>FB: Record source_mode (real | role-played)
    FB->>CM: Route as structured change input
    CM-->>FB: change_management_ref (linked change document)

    Note over S,IM: In solo mode, Stakeholder role is played by the developer per process-w5h's existing pattern
    Note over FB,CM: change-management owns the actual change-document schema, and FeedbackItem only captures and routes
```

### Regeneration-on-Change Flow *(Diagram D-604)*
**Source Requirements**: [R-627a, R-629, R-629a, D-10, D-11]
**Entities Involved**: domain-alignentities / model-integration (external), UIModel, Screen, Changelog

```mermaid
sequenceDiagram
    participant DA as domain-alignentities / model-integration (external)
    participant UM as UIModel
    participant SCR as Screen
    participant CL as Changelog

    DA->>UM: Domain model changed
    UM->>UM: syncWithDomainModel() — co-evolve (R-627a)
    UM->>UM: Identify affected UIModelEntry items
    UM->>SCR: propagateChange() for each affected Screen
    SCR->>SCR: regenerate(reason)
    SCR->>CL: Append changelog entry (not silently destructive)

    Note over DA,UM: MVP implements this manually (developer re-runs), while Phase 2 automates detection (R-627a enhancement)
    Note over SCR,CL: Regeneration always logged — satisfies D-11's "regenerate, don't just flag" decision while preserving traceability
```

### Import & Conformance Flow *(Diagram D-605, Phase 2 feature)*
**Source Requirements**: [R-615, R-616, R-617, R-618]
**Entities Involved**: Design-Spec Author (external, historical), DesignSpecification, ComponentInventory, Screen

```mermaid
sequenceDiagram
    participant Author as Design-Spec Author (historical, external)
    participant DS as DesignSpecification
    participant CI as ComponentInventory
    participant SCR as Screen

    Author-->>DS: (Pre-existing) Markdown + embedded HTML/CSS spec
    DS->>DS: Parse into internal screen/component/flow representation
    DS->>CI: Set rigor_mode = strict-conformance
    DS->>SCR: Identify covered screens (import_origin = imported)
    DS->>DS: Identify coverage_gaps (screens not covered)
    alt Gaps exist
        DS-->>SCR: Flag gap screens for generation or stakeholder clarification
    end

    Note over CI: Once imported, no new/divergent styling is invented — reuse what's literally observed (D-8)
    Note over DS,SCR: This flow is a Phase 2 Enhancement feature per scope-analysis.md — MVP is generation-only
```

## System-System Interactions

### Pipeline Position *(Diagram D-606)*
**Source Requirements**: [R-619, R-620, R-621, R-622]
**Entities Involved**: requirements-ingest, domain-extractconcepts, goals-extract, diagram-generatecollaboration (this project itself), UI Prototyping skill set, edps-workflow-orchestrator, change-management

```mermaid
flowchart LR
    RI[requirements-ingest] --> UIP[UI Prototyping Skill Set]
    DE[domain-extractconcepts] --> UIP
    GE[goals-extract] --> UIP
    DGC[diagram-generatecollaboration] -.optional.-> UIP

    UIP -->|screen-inventory, design-document, ui-model| Orch[edps-workflow-orchestrator]
    UIP -->|FeedbackItem routed as structured change| CM[change-management]

    Orch -->|stakeholder_confirmation gate, collaboration_mode| UIP

    classDef existing fill:#e1f5fe
    classDef new fill:#fce4ec
    class RI,DE,GE,DGC,Orch,CM existing
    class UIP new
```

**Note**: This diagram makes explicit what `domain-alignment.md`'s REC-003 argued against modeling as a new shared entity — the gate/orchestrator relationship is a *process* integration point, not a domain entity, and is visualized here rather than added to the class diagram.

---
**Traceability**: Diagrams generated from `domain-concepts.md` entities and `requirements.md` v1.3 requirement IDs as annotated per diagram
**Generated**: 2026-10-26
