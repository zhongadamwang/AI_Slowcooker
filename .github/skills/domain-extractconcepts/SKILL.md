---
name: domain-extractconcepts
description: Extract the domain entities (with attributes and operations), business concepts, terminology, and relationships from a project's requirements, grouped by domain area and traced to requirement IDs, written as domain-concepts.md and domain-concepts.json. Use after requirements-ingest when the user asks for a domain model, the entities or concepts in a set of requirements, a glossary, or a class diagram's raw material; and before domain-alignentities or diagram-generatecollaboration, which read domain-concepts.json.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Domain Extract Concepts

Extract and structure domain-specific concepts, entities, and terminology from requirements to build foundational domain models.

## Intent
Systematically identify and extract domain entities, business concepts, terminology, and relationships from structured requirements. Creates comprehensive domain concept maps with categorization, definitions, and traceability for downstream domain modeling tasks.

## Inputs
- **Source**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (from requirements-ingest skill)
- **Secondary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/goals.json` (from goals-extract skill, optional)
- **Format**: Structured requirements with IDs, classifications, and text content

## Outputs
**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` - Structured domain data for programmatic use
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.md` - Human-readable domain documentation

### `domain-concepts.json` (top level)

| Key | Content |
|---|---|
| `project_id`, `extraction_metadata` | `generated_at`, `source_files`, `total_concepts`, `total_entities`, `confidence_score` |
| `domain_entities` | `id` (`ENT-001`), `name`, `description`, `attributes`, `operations`, `domain_area`, `source_refs`, `confidence` |
| `business_concepts` | `id` (`CON-001`), `name`, `definition`, `synonyms`, `domain_area`, `source_refs`, `confidence` |
| `terminology` | `term`, `definition`, `context`, `domain_area`, `source_refs` |
| `relationships` | `id` (`REL-001`), `type`, `source_entity`, `target_entity`, `description`, `cardinality`, `source_refs` |
| `domain_areas` | `name`, `description`, `entities`, `concepts`, `key_processes` |

`source_refs` holds requirement IDs from `requirements.json`.

### `domain-concepts.md` (sections)

`## Domain Areas`, `## Entities` (one `### Name *(ENT-001)*` per entity), `## Business Concepts`, `## Terminology Glossary`, `## Entity Relationships`.

The complete templates for both files are in [references/output-format.md](references/output-format.md).

## Core Extraction Process

### 1. Entity Identification
**Pattern Recognition**:
- **Nouns as entities**: User, Order, Product, Payment
- **Process actors**: Customer, Administrator, System
- **Data containers**: Profile, Transaction, Report
- **Physical objects**: Card, Device, Document

**Attribute Discovery**:
- **Identifiers**: ID fields, unique keys, reference numbers
- **Properties**: Names, descriptions, status fields
- **Relationships**: Foreign keys, associations, dependencies
- **Constraints**: Required fields, validation rules, business rules

### 2. Concept Extraction
**Business Process Identification**:
- **Actions**: Create, Update, Delete, Process, Validate
- **Workflows**: Registration, Checkout, Approval, Notifications
- **States**: Active, Pending, Completed, Cancelled
- **Rules**: Business logic, validation criteria, approval processes

**Terminology Mining**:
- **Domain-specific terms**: Technical jargon, industry terminology
- **Acronyms**: API, REST, SSL, PCI, GDPR
- **Business language**: KPIs, SLAs, ROI, conversion rates
- **Synonyms**: Multiple terms for same concept

### 3. Relationship Discovery
**Association Patterns**:
- **Ownership**: User owns Account, Account contains Transactions
- **Hierarchy**: Organization has Departments, Departments have Teams
- **Dependencies**: Order requires Payment, Payment needs Validation
- **Temporal**: Event triggers Action, Action produces Result

### 4. Categorization Strategy
**Domain Areas**:
- **Core Business**: Primary business functions and processes
- **Supporting Systems**: Authentication, reporting, configuration
- **Technical Infrastructure**: APIs, databases, integrations
- **Compliance & Security**: Audit, permissions, data protection

## Processing Guidelines

### Entity Extraction Rules
1. **Focus on business-relevant nouns** that represent persistent data or active system participants
2. **Abstract concrete implementations** - prefer "Payment" over "CreditCardPayment" for initial modeling
3. **Prioritize entities with attributes and operations** - standalone terms may be concepts rather than entities
4. **Extract behavioral aspects** - identify key operations/methods that entities perform
5. **Capture visibility indicators** - distinguish between public and private attributes/operations
6. **Maintain traceability** to source requirements for validation and refinement

### Operation/Method Extraction
1. **Identify entity behaviors** from action verbs in requirements (authenticate, validate, process)
2. **Extract parameters** from context - what data does the operation need
3. **Determine return types** based on expected outcomes
4. **Infer visibility** from business context - public for external interactions, private for internal logic
5. **Group related operations** to understand entity responsibilities

### Concept Classification
1. **Business Concepts**: Domain-specific processes, rules, and workflows
2. **Technical Concepts**: Implementation patterns, protocols, standards
3. **Data Concepts**: Information structures, formats, validation rules
4. **Process Concepts**: Workflows, state transitions, business logic

### Relationship Identification
1. **Explicit relationships**: Clearly stated associations in requirements
2. **Implied relationships**: Logical connections based on context
3. **Temporal relationships**: Process flows and state transitions
4. **Hierarchical relationships**: Parent-child, container-contained patterns

## Quality Assurance

### Validation Checks
- **Entity completeness**: All major business objects identified
- **Attribute coverage**: Key properties captured for each entity
- **Operation completeness**: Essential behaviors and methods identified
- **Relationship consistency**: Bidirectional associations properly mapped
- **Terminology accuracy**: Definitions align with business context
- **Traceability integrity**: All extractions linked to source requirements
- **Diagram readiness**: Entities structured for effective class diagram generation

### Confidence Scoring
- **High (0.8-1.0)**: Explicitly stated in requirements with clear definitions
- **Medium (0.5-0.79)**: Strongly implied or partially defined
- **Low (0.2-0.49)**: Inferred from context or weakly supported

For detailed extraction patterns and advanced analysis techniques, see [extraction-patterns.md](references/extraction-patterns.md).

Check the result against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py domain-extractconcepts \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration with Diagram Generation
When the user also wants a class diagram, hand `domain-concepts.json` to `diagram-generatecollaboration` after this skill finishes:

### Class Diagram Generation Flow
1. **Extract entities with operations** - Capture both static and behavioral aspects
2. **Generate domain-concepts.json** - Include detailed entity metadata
3. **Call diagram-generatecollaboration** - Create class diagram from extracted concepts
4. **Update domain-model.md** - Embed generated diagram in organizational model
5. **Maintain traceability** - Link diagram elements back to source requirements

## Cross-Skill Integration

### Input Dependencies:
- requirements-ingest skill → requirements.json
- goals-extract skill → goals.json (optional)

### Output Consumers:
- domain-alignentities skill ← domain-concepts.json
- diagram-generatecollaboration skill ← domain-concepts.json (for class diagrams)
- domain-proposenewconcepts skill ← domain-concepts.json

### Diagram Generation Integration:
When integrated with diagram-generatecollaboration skill:
- Extracted entities automatically generate class diagram elements with inline styling (`:::category`)
- Operations and attributes populate class diagram structure with proper visibility markers
- Relationships become diagram associations and inheritance with clear labels
- Domain areas organize diagram layout and grouping
- Styling definitions (`classDef`) must be included for proper rendering:
  - `classDef actor fill:#e1f5fe` - for primary and supporting actors
  - `classDef entity fill:#f3e5f5` - for core business entities
  - `classDef enum fill:#fff3e0` - for enumeration types
  - `classDef ai fill:#e8f5e8` - for AI-specific entities and components