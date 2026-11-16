---
name: domain-alignentities
description: Compare a project's extracted domain concepts with the organization's existing domain models and vocabularies: map each entity, operation, term, and relationship to an existing one where it matches, flag naming and definition conflicts, and recommend how to standardize, written as domain-alignment.md and domain-alignment.json. Use after domain-extractconcepts when the user asks whether new concepts already exist in the orgModel, wants terminology made consistent across projects, or needs conflicts with existing models found before integrating; and before domain-proposenewconcepts or model-integration.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Domain Align Entities

Align extracted domain concepts with existing organizational domain models and standards to ensure consistency and reuse across projects.

## Intent
Systematically compare new domain concepts extracted from requirements against existing organizational domain models, vocabularies, and standards. Identifies mappings, conflicts, and alignment opportunities to maintain consistency across projects while supporting domain model evolution.

### Boundary-Scoped Entity References (PRJ-07 integration)

When the target organizational model is boundary-decomposed (per `hierarchy-management`'s `[NN]-[Name]Boundary/` structure), every `extracted_entity`/`target_entity` in this skill's output must additionally resolve to a [Scoped Entity Reference](../model-validatealignment/references/cross-model-alignment-contract.md#11-scoped-entity-reference) — `(scope, entity_id)`, never `entity_id` alone — so that `model-validatealignment` can check alignment without re-deriving which boundary an entity belongs to. This does not change this skill's existing alignment logic or output schema; it adds a `scope` field (the boundary path, e.g., `root-boundary/child-software-boundary/`) alongside each existing `extracted_entity`/`target_entity` object, populated from the boundary folder this skill is currently operating within. A flat (non-hierarchical) project has a single implicit scope and may omit this field, exactly as the contract's own Section 1.1 describes scope as meaningful primarily when entity-name collisions across boundaries are possible.

## Inputs
- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-concepts.json` (from domain-extractconcepts skill)
- **References**: Organizational domain models (`OrgDocument/orgModel/**/*domain-model.md`)
- **References**: Organizational vocabularies (`OrgDocument/orgModel/**/*vocabulary.md`)
- **References**: Organizational class diagrams (`OrgDocument/orgModel/**/*domain-model.md` containing Mermaid class diagrams)
- **Format**: Structured domain concepts with entities, terminology, relationships, operations, and metadata

## Outputs
**Files Generated:**
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.json` - Structured alignment data for programmatic use
- `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/domain-alignment.md` - Human-readable alignment report and recommendations

### `domain-alignment.json` (top level)

| Key | Content |
|---|---|
| `project_id`, `alignment_metadata` | `generated_at`, `source_concepts_file`, `reference_models`, `reference_vocabularies`, `total_alignments`, `conflict_count`, `alignment_confidence` |
| `entity_alignments` | Per extracted entity: `extracted_entity`, `alignment_result` (match type, target entity, confidence, rationale) |
| `operation_alignments` | Per extracted operation: `extracted_operation`, `alignment_result` |
| `terminology_alignments` | Per extracted term: `extracted_term`, `alignment_result` |
| `relationship_alignments` | Per extracted relationship: `extracted_relationship`, `alignment_result` |
| `conflicts_detected` | `conflict_id` (`CONF-001`), `type`, `description`, `affected_items`, `severity`, `resolution_options` |
| `recommendations` | `id`, `type`, `priority`, `description`, `impact`, `implementation` |

### `domain-alignment.md` (sections)

`## Executive Summary`, `## Entity Alignments` (direct matches, partial matches, new entities), `## Operation Alignments`, `## Terminology Alignments`, `## Relationship Patterns`, `## Conflicts & Resolutions`, `## Recommendations`.

The complete templates for both files are in [references/output-format.md](references/output-format.md).

## Core Alignment Process

### 1. Entity Mapping
**Pattern Matching**:
- **Direct name matches**: Identical or near-identical entity names
- **Semantic similarity**: Entities with similar descriptions and attributes
- **Functional equivalence**: Entities serving similar roles in domain
- **Structural patterns**: Entities with comparable attribute sets

**Conflict Detection**:
- **Naming conflicts**: Same name, different meanings
- **Definition conflicts**: Similar entities, incompatible definitions  
- **Attribute mismatches**: Same entity, different attribute sets
- **Relationship inconsistencies**: Conflicting relationship patterns

### 2. Terminology Standardization
**Vocabulary Alignment**:
- **Exact matches**: Terms with identical definitions
- **Synonym detection**: Different terms, same meaning
- **Broader/narrower relationships**: Hierarchical term relationships
- **Context conflicts**: Same term, different contexts

**Standardization Rules**:
- **Prefer organizational terms** over project-specific variants
- **Maintain precision** - don't force inappropriate generalizations
- **Document distinctions** when terms serve different purposes
- **Suggest vocabulary extensions** for valuable new concepts

### 3. Relationship Pattern Analysis
**Pattern Recognition**:
- **Ownership patterns**: Entity A "has" Entity B
- **Dependency patterns**: Entity A "requires" Entity B
- **Hierarchy patterns**: Entity A "contains" Entity B
- **Process patterns**: Entity A "triggers" Entity B

**Consistency Checking**:
- **Verify similar relationships** use consistent naming
- **Check cardinality consistency** across similar patterns
- **Validate relationship semantics** against organizational models

### 4. Incremental Model Evolution
**Model Extension Strategy**:
- **Assess new concept value** for organizational reuse
- **Propose model additions** for broadly applicable concepts
- **Document specializations** for project-specific needs
- **Maintain backward compatibility** with existing models

**Change Management**:
- **Track proposed changes** to organizational models
- **Document impact assessment** for model modifications
- **Coordinate with domain stakeholders** for approval process
- **Version control integration** for model evolution tracking

## Quality Assurance

### Alignment Validation
- **Semantic consistency**: Aligned entities maintain coherent meaning
- **Relationship integrity**: Mapped relationships preserve logical structure
- **Terminology accuracy**: Aligned terms maintain definitional precision
- **Completeness checking**: All extracted concepts processed for alignment

### Confidence Scoring
- **High (0.8-1.0)**: Clear semantic match with strong evidence
- **Medium (0.5-0.79)**: Reasonable match with some uncertainty
- **Low (0.2-0.49)**: Weak match requiring human review

For detailed alignment patterns and conflict resolution strategies, see [alignment-patterns.md](references/alignment-patterns.md).

Check the result against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py domain-alignentities \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration with Diagram Updates
This skill reports and recommends; it does not edit organizational models. When its recommendations are accepted, `orgmodel-update` applies them and the class diagrams are updated as follows:

### Class Diagram Alignment Process
1. **Identify diagram impacts** from entity and operation alignments
2. **Generate updated class diagrams** reflecting organizational standards
3. **Update domain-model.md** with aligned entity names and relationships
4. **Maintain diagram consistency** across organizational models
5. **Preserve existing styling** and layout where possible

## Cross-Skill Integration

### Boundary-Scoped Alignment (PRJ-07 integration)

This skill's entity alignments are a direct input to [`model-validatealignment`](../model-validatealignment/SKILL.md)'s end-of-round validation — specifically, its check that a `UIModelEntry`'s `domain_entity_refs` resolve to entities actually defined in the cited boundary's `domain-model.md` (contract Section 6). Nothing in this skill's own responsibility changes: it still produces alignment mappings between extracted and organizational entities. The only addition is populating `scope` on each entity reference when operating within a boundary-decomposed hierarchy, so downstream validation has a *** to check without re-deriving it.

### Input Dependencies:
- domain-extractconcepts skill → domain-concepts.json
- Organizational domain models (OrgDocument/orgModel/**/*domain-model.md)
- Organizational vocabularies (OrgDocument/orgModel/**/*vocabulary.md)

### Output Consumers:
- domain-proposenewconcepts skill ← domain-alignment.json
- model-integration skill ← domain-alignment.json
- diagram-generatecollaboration skill ← alignment results (for diagram updates)
- orgmodel-update skill ← alignment recommendations

### Diagram Generation Integration:
When updating domain models based on alignment results:
- Entity alignments trigger class diagram updates with proper styling categories
- Operation alignments modify method signatures in diagrams
- Terminology standardization updates entity and attribute names
- Relationship alignments adjust diagram associations
- Styling consistency maintained with organizational standards:
  - `classDef actor fill:#e1f5fe` - for actors and user roles
  - `classDef entity fill:#f3e5f5` - for business entities and data structures  
  - `classDef enum fill:#fff3e0` - for enumeration and value types
  - `classDef ai fill:#e8f5e8` - for AI and automation components