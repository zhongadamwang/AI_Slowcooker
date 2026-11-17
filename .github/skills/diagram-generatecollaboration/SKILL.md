---
name: diagram-generatecollaboration
description: Generate Mermaid diagrams from a project's domain concepts and requirements - class diagrams of the domain model, sequence diagrams of user-system and system-system interactions, flowcharts of business processes, and hierarchical collaboration diagrams with system boundaries (box syntax) and actor/boundary/control/entity participant stereotypes - each traced to requirement IDs, written as collaboration-diagrams.md and collaboration-diagrams.json. Owns boundary validation rules VR-1 to VR-4. Use after domain-extractconcepts when the user asks for a collaboration, sequence, class, or interaction diagram, wants a process or system visualized, or wants a diagram's boundaries validated; and before hierarchy-management, which decomposes its control participants.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-16"
---

# Diagram Generate Collaboration

Turn analysed domain concepts and requirements into diagrams that show who interacts with what, in what order, across which system boundaries.

This skill is the single owner of the participant stereotype rules and of boundary validation rules VR-1 to VR-4. Other skills (`edps-compliance`, `hierarchy-management`, `migration-tools`) apply these rules by reference; they do not restate them.

## Inputs
- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (from `domain-extractconcepts`)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (from `requirements-ingest`)
- **Tertiary**: `OrgDocument/orgModel/**/domain-model.md` (existing domain models, for class diagrams)
- **Optional**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/goals.json` (from `goals-extract`)

## Outputs
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/collaboration-diagrams.md` — Markdown with embedded Mermaid diagrams, each under a heading carrying its diagram ID (`D-001`) and source requirements
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/collaboration-diagrams.json` — diagram metadata: `project_id`, `generation_metadata`, and a `diagrams` array (`id`, `title`, `type`, `category`, `description`, `entities`, `source_requirements`, `mermaid_code`, `complexity`, `maintenance_priority`). For hierarchical diagrams it also carries `box_syntax_metadata` and `boundary_validation_report`
- `OrgDocument/orgModel/**/domain-model.md` — updated class diagram section, only in Domain Model Integration Mode

The complete templates are in [references/output-format.md](references/output-format.md).

## Processing Workflow

### 1. Input Analysis
**From `domain-concepts.json`:**
- Extract entities with their relationships
- Identify domain areas and key processes
- Map entity interactions and dependencies

**From `requirements.json`:**
- Find interaction patterns in requirement text
- Identify user journeys and system flows
- Extract temporal sequences and decision points

**For Hierarchical Diagrams (Optional):**
- Identify participant stereotypes (`<<Actor>>`, `<<System>>`, `<<UI>>`, `<<Entity>>`) from domain concepts
- **Classify participants** using stereotype inference rules (see [Participant Stereotypes](#participant-stereotypes))
- Detect boundary definitions from configuration or automatic analysis
- Map decomposition links between parent and child diagrams
- **Validate decomposition eligibility** — only control-type participants may become sub-processes
- **Validate boundary-first reception** — boundary-type participants must receive actor messages first

### 2. Diagram Type Selection
**Domain Class Models:**
- Use class diagrams to visualize entity relationships and domain structure
- Include core entities with attributes and operations
- Show inheritance, composition, and association relationships
- Add styling to distinguish entity types (actors, core entities, enums)

**User-System Interactions:**
- Use sequence diagrams for user workflows
- Include system responses and error paths
- Show authentication, authorization flows

**System-System Interactions:**
- Use sequence diagrams for API communications
- Include timeouts, retries, and failure scenarios
- Show data flow between services

**Business Process Workflows:**
- Use flowcharts for decision trees and branching logic
- Include parallel processes and synchronization points
- Show approval workflows and state transitions

**Hierarchical Diagrams:**
- Use `box` syntax to represent system boundaries
- Generate Level 0 diagrams showing high-level system interactions
- Decompose `<<System>>` participants into Level 1+ diagrams
- Follow EDPS decomposition rules for participant stereotypes
- **Apply stereotype classification** to all participants before generating diagrams
- **Enforce decomposition rules** — block decomposition of non-control participants

### 3. Mermaid Generation Rules

**Class Diagrams:**
```
classDiagram
    class [EntityName]:::[styleCategory] {
        +attribute_name: Type
        -private_attribute: Type
        +operation_name()
        -private_operation()
    }
    
    %% UML Relationship Notation (MANDATORY — do NOT use ER notation like ||--o{ )
    %% Association:   ClassA "1" --> "*" ClassB : label
    %% Composition:   Parent "1" *-- "*" Child : label
    %% Aggregation:   Whole "1" o-- "*" Part : label
    %% Inheritance:   Parent <|-- Child
    %% Dependency:    Client ..> Service : uses
    %% Realization:   Interface <|.. Implementation
    %%
    %% Multiplicity: "1", "*", "0..1", "1..*", "0..*"
    %% FORBIDDEN: ||--o{  }o--||  }o--o{  ||--||  (these are ER notation, not UML)
    
    [SourceEntity] "1" --> "*" [TargetEntity] : relationship_label
    [ParentEntity] <|-- [ChildEntity]
    [CompositeEntity] "1" *-- "*" [ComponentEntity] : contains
    [AggregateEntity] "1" o-- "*" [PartEntity] : has
    [Client] ..> [Service] : uses
    
    %% Apply :::style directly on class body declarations
    %% RIGHT:  class User:::core { +name: String }
    %% WRONG:  class User { +name: String }  then  User:::core
    
    %% Styling Definitions
    classDef [styleCategory] fill:#[color]
    classDef actor fill:#e1f5fe
    classDef entity fill:#f3e5f5
    classDef enum fill:#fff3e0
    classDef ai fill:#e8f5e8
```

**Naming Conventions for Class Diagrams:**
- Entity names: PascalCase (User, UserProfile, PaymentGateway)
- Attributes: snake_case (user_id, created_at, is_active)
- Methods: camelCase (authenticate(), updateProfile(), calculateTotal())
- Relationships: **Use UML notation only** — `-->` (association), `*--` (composition), `o--` (aggregation), `<|--` (inheritance), `..>` (dependency)
- Multiplicity: Always annotate with `"1"`, `"*"`, `"0..1"`, etc. on both sides of the relationship
- **NEVER use ER notation** (`||--o{`, `}o--||`, `}o--o{`, `||--||`) in class diagrams — those belong in `erDiagram` blocks only
- Styling: Apply `:::styleCategory` directly on class body declarations: `class Name:::style { }` — this is the preferred format
- Style categories: actor, entity, enum, ai (or custom categories as needed)
- Standard colors: actor (#e1f5fe), entity (#f3e5f5), enum (#fff3e0), ai (#e8f5e8)

**Sequence Diagrams:**
```
participant [ShortName] as [Full Entity Name]
[Actor]->>+[Target]: [Action description]
[Target]-->>-[Actor]: [Response description]
Note over [Entity]: [Important information]
alt [Condition]
    [Alternative flow]
else [Other condition]
    [Alternative flow]
end
```

**Naming Conventions:**
- Entity names: PascalCase (UserService, PaymentGateway)
- Messages: Action-oriented (Validate credentials, Process payment)
- Notes: Clarify business rules, timeouts, constraints
- Alt blocks: Show error handling and edge cases

**Mermaid text and render checks:**
- Do not place literal semicolons (`;`) inside Mermaid labels, messages, or notes, especially sequence-diagram text. Mermaid can interpret them as statement separators and fail to parse the diagram; use a comma, conjunction, or a separate statement instead.
- Before finalizing output, parse and render every fenced Mermaid block with the target renderer (for example, the project's VS Code Markdown preview). Fix render errors and repeat the check; EDPS boundary validation does not validate Mermaid syntax.

**Hierarchical Sequence Diagrams (with Boundaries):**
```
sequenceDiagram
    %% Stereotypes: [ActorAlias]=actor | [BoundaryAlias]=boundary, [ControlAlias]=control, [EntityAlias]=entity
    participant [ActorName] as "[Full Actor Name]"
    
    box "[BoundaryName]"
        participant [BoundaryAlias] as "[Full Participant Name]"
        participant [ControlAlias] as "[Full Participant Name]"
        participant [EntityAlias] as "[Full Participant Name]"
    end
    
    [ActorName]->>[BoundaryAlias]: [Interaction]
```

**Naming and Stereotype Conventions:**
- Use `participant [Alias] as "[Label]"` syntax for all participants
- Track stereotypes in a `%% Stereotypes:` comment at the top of the diagram, using the format: `Alias=type` separated by commas within a boundary and `|` between boundaries
- Valid stereotype types: `actor`, `boundary`, `control`, `entity`
- **actor**: External participants, cannot be decomposed
- **boundary**: Entry point to a boundary (e.g., UI, API Gateway)
- **control**: Decomposable system/service component
- **entity**: Stable data store or resource
- Quote box labels: `box "Boundary Name"` for maximum renderer compatibility
- Boundary names should reflect the encapsulated capability
- See [Participant Stereotypes](#participant-stereotypes) for inference and enforcement rules

### 4. Traceability Integration
**Requirement References:**
- Link each diagram to source requirements using `[R-XXX]` format
- Include entity references using `ENT-XXX` identifiers from domain concepts
- Maintain bidirectional traceability for change impact analysis
- Reference domain models using `OrgDocument/orgModel/**/*domain-model.md` paths for class diagrams

**Diagram Metadata:**
- Assign unique diagram IDs (`D-001`, `D-002`, etc.)
- Track complexity level (simple/medium/complex)
- Set maintenance priority based on business criticality
- Category classification: domain-model, user-system, system-system, process-workflow

**For Hierarchical Diagrams:**
- Add `decomposition` field in diagram metadata to link to child diagrams
- Ensure participant names are consistent across hierarchy levels
- Propagate requirement traceability down the decomposition chain

## Participant Stereotypes

Every participant in a hierarchical collaboration diagram has exactly one stereotype. It decides how the participant is annotated, whether it can be decomposed, and how messages may be routed.

| Stereotype | Role | Decomposable? |
|-----------|------|---------------|
| `actor` | External party that initiates interactions; always outside every `box` | No |
| `boundary` | Entry point of a boundary; mediates between actors and internals (UI, API, gateway) | No |
| `control` | Business logic or orchestration | **Yes** |
| `entity` | Data store or passive resource | No |

Classify by explicit stereotype where one is given, otherwise infer in this order: actor, boundary, entity, then control as the default. Four rules are enforced before any decomposition: only `control` participants are decomposed; an actor's first message into a boundary is received by a `boundary` participant; actors never appear inside a `box`; entities are not decomposed.

Annotate with a `%% Stereotypes:` comment and plain `participant [Alias] as "[Label]"` declarations. Never use the `@{ "type": ... }` form; most Mermaid renderers reject it.

```
sequenceDiagram
    %% Stereotypes: Customer=actor | API=boundary, OrderSvc=control, OrderDB=entity
    participant Customer as "Customer"

    box "Order Processing"
        participant API as "Order API"
        participant OrderSvc as "Order Service"
        participant OrderDB as "Order Database"
    end

    Customer->>API: Place Order
    API->>OrderSvc: Process Order
    OrderSvc->>OrderDB: Store Order
```

Read [references/stereotype-classification.md](references/stereotype-classification.md) for the full inference rules, manual overrides, the validation error formats, and type consistency across hierarchy levels.

## Box Syntax

Each boundary is one `box "[Name]" ... end` block with a quoted label. Actors are declared before any box. Inside a box, participants are ordered `boundary` first, then `control`, then `entity`. Boxes are ordered by when they first receive a message. Mermaid has no nested boxes: a sub-boundary is a separate diagram linked by a decomposition reference.

Read [references/box-syntax.md](references/box-syntax.md) for multi-boundary generation, naming and colour conventions, summary comments, edge cases, and the `box_syntax_metadata` block written to the JSON output.

## Boundary Validation

After classification and box generation, and before writing the final Mermaid, validate every hierarchical diagram against four rules:

| Rule | Name | Default severity |
|------|------|-----------------|
| VR-1 | Single External Interface | Error |
| VR-2 | Boundary-First Reception | Error |
| VR-3 | Control-Only Decomposition | Error |
| VR-4 | Cohesive Responsibility | Warning |

- **Advisory mode** (default): all findings are reported, generation continues, and each violation is marked with a `%% [VR-n ERROR] ...` comment at the offending line.
- **Strict mode**: an error-level violation blocks generation; only the validation report is produced.

The result is written as a `boundary_validation_report` block in `collaboration-diagrams.json` (`overall_status` of `PASS`, `PASS_WITH_WARNINGS`, `FAIL`, or `BLOCKED`, with per-rule results) and as a summary above the first diagram in `collaboration-diagrams.md`.

To validate an existing `collaboration.md` without regenerating it (as `edps-compliance` requests), apply the same four rules to the file as it stands and write the same report block to `boundary-validation-report.json` beside that file.

Read [references/boundary-validation.md](references/boundary-validation.md) for each rule's definition, check algorithm, and examples, the report schema, and the configuration options. Boundary validation does not check Mermaid syntax; that is the render check in the workflow above.

## Quality Guidelines

### Readability Standards
- **Class diagrams**: Limit to 10-15 entities maximum for clarity
- **Sequence diagrams**: Limit to 8-10 participants maximum  
- For hierarchical diagrams, Level 0 should have 2-5 boundaries
- Use meaningful, business-friendly entity names
- Include essential attributes and methods only
- Include notes for non-obvious business rules
- Show both happy path and key error scenarios

### Technical Standards  
- Valid Mermaid syntax that renders in VS Code
- Parse and render every generated Mermaid block before publishing; do not rely on visual inspection of source alone.
- Consistent naming conventions across all diagram types
- Appropriate use of visibility markers (+/- for public/private)
- Clear distinction between inheritance, composition, and association
- Proper use of inline styling with :::category syntax AND corresponding classDef definitions
- Consistent participant naming across related diagrams
- Appropriate use of activation boxes for long-running operations
- Clear distinction between synchronous and asynchronous calls
- For hierarchical diagrams, validate against EDPS boundary rules (e.g., single external interface)

### Business Value
- **Class diagrams**: Focus on core business entities and critical relationships
- **Interaction diagrams**: Focus on high-value interactions that need visualization
- Prioritize user-facing workflows and critical system integrations
- Include compliance and security-related flows
- Show cross-system dependencies that affect architecture decisions
- Ensure domain models align with organizational standards and terminology
- Use boundaries to model complex systems and hide internal details, improving clarity for different stakeholders

## Hierarchical Decomposition Mode
When called with `hierarchical_decomposition: true`, this skill:

1. **Analyzes participant stereotypes** and interaction patterns to detect boundaries
2. **Generates a Level 0 diagram** with high-level system boundaries
3. **Decomposes each `<<System>>` participant** into a separate Level 1 collaboration diagram in a corresponding subfolder
4. **Creates a folder structure** that mirrors the decomposition hierarchy
5. **Maintains traceability** and context across all levels

### Hierarchical Input Parameters
```json
{
  "hierarchical_decomposition": true,
  "root_diagram_name": "SystemOverview",
  "auto_boundary_detection": true,
  "manual_boundaries": [
    {
      "name": "Payment Gateway",
      "participants": ["PaymentAPI", "TransactionProcessor"]
    }
  ]
}
```

## Domain Model Integration Mode
When called with `domain_model_integration: true`, this skill:

1. **Extracts existing domain model structure** from `OrgDocument/orgModel/**/domain-model.md`
2. **Generates enhanced class diagrams** based on textual domain descriptions
3. **Updates domain-model.md** by adding or replacing the "Domain Class Diagram" section
4. **Maintains consistency** with existing textual domain descriptions
5. **Preserves traceability** links to requirements and domain concepts

### Integration Input Parameters
```json
{
  "domain_model_integration": true,
  "target_domain_model": "OrgDocument/orgModel/[NN] - [Process Name]/domain-model.md",
  "diagram_placement": "after_title|before_actors|replace_existing",
  "sync_with_text": true
}
```

## Integration Notes
- **Domain Model Sync**: Class diagrams complement and enhance textual domain models
- **Cross-Skill Integration**: Works with domain-extractconcepts, domain-alignentities, and orgmodel-update
- **Bidirectional Updates**: Can generate diagrams from text or update text from aligned concepts
- **Organizational Standards**: Domain class diagrams align with organizational domain model standards
- **Iterative Refinement**: Supports incremental updates as requirements and domain understanding evolve
- **VS Code Compatible**: All diagrams render properly in VS Code Mermaid preview

## Cross-Skill Workflow Integration

### With domain-extractconcepts:
- Consume `domain-concepts.json` as primary input
- Generate class diagrams from extracted entities and relationships
- Maintain entity IDs and traceability to source requirements

### With domain-alignentities:
- Use alignment results to update class diagrams with organizational standards
- Incorporate entity mappings and terminology standardization
- Reflect alignment recommendations in diagram structure

### With orgmodel-update:
- Coordinate domain-model.md updates to avoid conflicts
- Ensure diagram updates align with organizational model changes
- Support rollback capabilities for diagram modifications

## Completion Gate

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py diagram-generatecollaboration \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```
