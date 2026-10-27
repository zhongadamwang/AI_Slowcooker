# Domain Alignment Report

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Generated**: 2026-10-26
**Source Concepts**: `domain-concepts.md` (14 entities, 12 concepts)
**Reference Models**: `orgModel/01 - Skill Development Process/domain-model.md`, `orgModel/01 - Skill Development Process/vocabulary.md`
**Alignment Confidence**: 0.80/1.0

## Executive Summary

**Total Alignments**: 14 entities reviewed, 12 concepts reviewed
**Direct Matches**: 0 | **Partial Matches**: 3 | **New Entities**: 11
**Conflicts Detected**: 1 | **Recommendations**: 4

This project's domain is genuinely novel relative to the existing organizational model: `orgModel/01 - Skill Development Process` covers skill-framework/learning-pathway concepts and the existing EDPS pipeline skills (requirements, change management, hierarchy, etc.) — none of which model UI/design artifacts. Accordingly, **no direct entity matches** were found; this is the expected and correct outcome for a genuinely new domain area, not a sign of poor alignment. The useful alignment work here is in the **patterns** (traceability, in-document versioning, gate/skill registration) that PRJ-06 should reuse rather than reinvent, plus one real naming conflict worth resolving before it propagates.

PRJ-06's own `orgModel/02 - UI Prototype Skill Development Process/domain-model.md` is currently an empty stub ("To be defined after requirements analysis") — this report's recommendations (below) are what should populate it next.

## Entity Alignments

### ✅ Direct Matches
None. No existing organizational entity represents a screen, mockup, UI model, or design document — this organization's prior domain model is entirely about skill/competency development and the EDPS pipeline's own process entities, not UI artifacts.

### ⚠️ Partial Matches

#### GateCheck → *(no named entity, but a strong structural pattern match)* *(ENT-612)*
**Confidence**: 0.70
**Source Model**: Implicit across `orgModel/01 - Skill Development Process/domain-model.md`'s many `*Skill` entities (e.g., `BoundaryValidator`, `HierarchyManagementSkill`) and the broader EDPS gate/orchestrator system (Iteration 3/4, not itself modeled in `domain-model.md` as an entity)
**Differences**: The existing model documents *skills* as entities (e.g., `BoundaryValidator` is modeled as a skill-component entity with its own attributes), but does not model the **gate check mechanism itself** as a domain entity anywhere — gates are referenced only procedurally in skill descriptions
**Action**: 🔄 PRJ-06's `GateCheck` entity is reasonable to keep project-local rather than push into the shared org model, since the shared model doesn't yet have a place for it either. Recommend **not** force-fitting this into the existing model; if a future iteration wants to formalize "Gate Check" as a shared organizational concept, that's a bigger change than this project should make unilaterally (see REC-003 below).

#### Changelog → Reference Management *(CON-passing-concept, partial conceptual overlap)* *(ENT-613)*
**Confidence**: 0.55
**Source Model**: `vocabulary.md`'s **Reference Management** term ("Automated maintenance of cross-references and dependencies... Ensures organizational model consistency during evolution")
**Differences**: Reference Management is about cross-*document* links staying valid; PRJ-06's `Changelog` is about a single document's own *version history* — related evolutionary-consistency goals, but not the same mechanism
**Action**: 🔄 Keep `Changelog`/`In-Document Changelog Versioning` as its own distinct concept (R-610); do not conflate with Reference Management. Worth noting the connection in PRJ-06's own vocabulary entry so a future reader understands the relationship rather than seeing two unrelated-looking terms.

#### UIModel/Aggregation → DomainModel *(partial structural analogy, not a naming conflict)* *(ENT-606, ENT-614)*
**Confidence**: 0.60
**Source Model**: `orgModel/01 - Skill Development Process/domain-model.md`'s own `DomainModel` entity (from `01 - Building Skills`'s domain-concepts.md, ENT-010: "Conceptual model capturing entities, relationships, and behaviors within a problem domain")
**Differences**: The existing `DomainModel` entity is the general EDPS concept of *a* domain model; PRJ-06's `UIModel` is a specific, novel kind of model (domain-to-UI aggregation) that is **not** a replacement or specialization of the general `DomainModel` concept — it's a new, adjacent model type that *consumes* a domain model as input
**Action**: 🔄 Recommend explicitly stating in PRJ-06's own domain-model.md that `UIModel` is **not** a type of `DomainModel`, but a distinct model that references one — avoids a future reader assuming an inheritance relationship that doesn't exist

### 🆕 New Entities
The remaining 11 entities (Screen, ScreenInventory, LayoutSpec, InteractiveMockup, InteractionFlow, UIModelEntry, DesignDocument, FeedbackItem, DesignSpecification, ComponentInventory) have no organizational counterparts — all are genuinely new domain concepts introduced by this project, consistent with it being the first UI-prototyping-focused project in this organization.

**Action for all 11**: ➕ Propose addition to PRJ-06's own `orgModel/02 - UI Prototype Skill Development Process/domain-model.md` (currently an empty stub) — these are not candidates for the shared `01 - Skill Development Process` model, since that model is scoped to skill/competency development, not UI artifacts. This is the expected outcome for entities belonging to a new, genuinely distinct process area, consistent with EDPS's own convention of one `domain-model.md` per process.

## Operation Alignments

### ✅ Method Matches
None directly — PRJ-06's operations (`generateLayoutSpec()`, `generateMockup()`, `regenerate()`, `syncWithDomainModel()`, `propagateChange()`) are all new, UI-specific behaviors with no existing organizational counterpart to align against.

### 🆕 New Operations
All operations listed in `domain-concepts.md`'s entity definitions are new:
- `Screen.generateLayoutSpec()`, `Screen.generateMockup()`, `Screen.regenerate(reason)`
- `UIModel.syncWithDomainModel()`, `UIModel.propagateChange()`

**Pattern worth reusing, not a direct match**: `HierarchyManagementSkill`'s decomposition/regeneration-adjacent behavior (from `orgModel/01 - Skill Development Process/domain-model.md`) and `documentation-automation`'s Content Guard pattern (from `vocabulary.md`: "Pre-check... that detects manually-authored content exceeding 10 lines... and prompts before overwrite") are structurally similar to what `Screen.regenerate()` needs to avoid clobbering manual edits — flagged as a reusable pattern in Recommendations below (REC-002), not an alignment match per se since the entities themselves don't correspond.

## Terminology Alignments

### ✅ Vocabulary Matches
None found directly — PRJ-06 introduces an entirely new terminology set (UI Model, Aggregation, Base/Derived Model, Strict Conformance, etc.) with no existing organizational vocabulary entries to match against.

### ⚠️ Conflicting Definitions

| Term | Extracted Definition (PRJ-06) | Org Definition (existing vocabulary.md) | Resolution |
|------|---------------------|----------------|------------|
| **Validation** (implicit, via "Flow/Mockup Consistency Check") | Automated comparison confirming a Mermaid flow diagram matches a mockup's actual clickable transitions (R-603a) | No direct "Validation" vocabulary entry exists, but **Hierarchy Validation** ("Structural integrity check of process hierarchies... auto-fixes safe... issues; structural errors require human review") and **Boundary Validator** establish a strong existing convention: *validation = structural/consistency checking with a pass/fail/warn report*, not a vague term | PRJ-06's `GateCheck`'s `flow_mockup_consistency` check type is **consistent** with this existing convention (good — no actual conflict), but PRJ-06's own documents (requirements.md, domain-concepts.md) never used the bare word "Validation" as a standalone glossary term, which is why this wasn't flagged as a direct conflict. **Recommend**: when PRJ-06's own vocabulary.md is populated, explicitly use "Validation" in a manner consistent with the existing Hierarchy Validation/Boundary Validator pattern (pass/fail/warn reporting), not a bespoke new meaning, to avoid future drift. |

### 🆕 New Terminology
All 12 business concepts from `domain-concepts.md` (ScreenGeneration, MockupGeneration, FlowModeling, DomainUIAlignment, CoEvolution, RegenerateOnChange, DesignRationale, InDocumentVersioning, MockupDrivenDiscussion, SoloModeRolePlay, StrictConformance, PartialImportGapDetection) are new terminology candidates with no existing organizational vocabulary counterpart.

## Relationship Patterns

### Existing Patterns Applied
- **Base/Derived-like structural precedent**: `Process Node` / `Hierarchy Index` (from `vocabulary.md`) establishes a precedent for a project-level artifact that aggregates/indexes multiple sub-items with parent/child links — structurally similar in spirit to PRJ-06's base/derived UIModel relationship (REL-603), though applied to a different kind of hierarchy (process decomposition vs. role-scoped model derivation). Worth reviewing `hierarchy-management`'s actual implementation approach for base/derived-style regeneration-on-change logic before designing PRJ-06's own from scratch.
- **Content Guard precedent for regeneration safety**: `documentation-automation`'s **Content Guard** pattern ("detects manually-authored content exceeding 10 lines... and prompts before overwrite... `--force` flag bypasses") is directly applicable to PRJ-06's `Screen.regenerate()` (R-629a) — this is an existing, proven mechanism for exactly the "don't clobber manual edits" risk flagged in `scope-analysis.md`'s Medium Priority Risks. **Strong recommendation to reuse this pattern rather than invent a new one** (see REC-002).
- **Traceability pattern**: PRJ-06's `requirement_refs`/`domain_entity_refs` fields (Screen, UIModelEntry) directly follow the existing `source_refs` convention used throughout `domain-concepts.md`'s own entity schema (e.g., `Requirement.requirement_id` format `R-XXX`, `source_refs` arrays on every entity) — already correctly applied, no action needed.
- **Gate/Severity pattern**: PRJ-06's `GateCheck.severity` (mode-resolved for `stakeholder_confirmation` type) correctly reuses the existing `stakeholder_confirmation` gate check type and `collaboration_mode` mechanism from Iteration 3/4, rather than reinventing approval semantics — already correctly applied per R-622, no action needed.

### New Patterns Identified
- **Co-Evolution between two independently-owned models** (UIModel ↔ domain-model.md, via `domain-alignentities`/`model-integration`): this is a genuinely new relationship pattern not previously present in the organizational model — prior EDPS skills generally produce artifacts that feed *forward* in the pipeline (Requirements → Goals → Domain → Diagrams → Plan), not artifacts that need *bidirectional* sync with an already-existing, independently-evolving model. This pattern deserves explicit documentation once implemented (see REC-004), since it may recur if future projects introduce other derived/aligned models.

## Recommendations

### REC-001 (Priority: High)
**Type**: Clarification
**Description**: Explicitly document in PRJ-06's own `domain-model.md` that `UIModel` is a distinct, new model type — not a subtype or replacement of the existing `DomainModel` concept — to prevent future confusion about their relationship.
**Impact**: Low effort, prevents a plausible future misunderstanding given the name similarity.
**Implementation**: Add a short "Relationship to Domain Model" note at the top of PRJ-06's `domain-model.md` once it's populated.

### REC-002 (Priority: High)
**Type**: Standardization
**Description**: Implement `Screen.regenerate()`/`R-629a`'s "don't clobber manual edits" safety using the existing **Content Guard** pattern from `documentation-automation` (detect substantial manually-authored content, prompt before overwrite, `--force` to bypass) rather than designing a new mechanism from scratch.
**Impact**: Saves design effort, and gives PRJ-06's regeneration behavior a proven, already-understood precedent other EDPS skill maintainers will recognize.
**Implementation**: When implementing the Phase 1/2 regeneration logic (per `scope-analysis.md`), reference `documentation-automation/SKILL.md`'s Content Guard section directly as the template.

### REC-003 (Priority: Medium)
**Type**: Extension (deferred)
**Description**: Do not attempt to formalize "Gate Check" as a shared organizational domain entity in this project. The existing model documents gates only procedurally (within each skill's own description), not as a first-class entity anywhere. Formalizing it would be a cross-cutting change affecting all 32+ existing skills, out of scope for PRJ-06.
**Impact**: Keeps PRJ-06 scoped to its own domain; avoids an unplanned, large refactor of the shared organizational model.
**Implementation**: None for this project. Flag as a possible future organizational-model improvement if a later project independently needs it.

### REC-004 (Priority: Medium)
**Type**: Documentation
**Description**: Once UI Model Co-Evolution (R-627a) is actually implemented (per `scope-analysis.md`'s Phase 2), document the bidirectional-sync pattern explicitly, since it's structurally new relative to every other EDPS skill's purely forward-feeding pipeline relationship.
**Impact**: Helps future projects recognize and reuse this pattern if they introduce their own derived/aligned models, rather than re-deriving the same design from scratch.
**Implementation**: Add a short pattern-description note to this project's `artifacts/Documentation/` once R-627a is built, not before (documenting a design before it's validated by implementation risks describing something that changes).

---
**Traceability**: Aligned against `orgModel/01 - Skill Development Process/domain-model.md` and `vocabulary.md`; extracted entities from `artifacts/Analysis/domain-concepts.md`
**Alignment Confidence**: 0.80/1.0 — high confidence in the "no direct match, genuinely new domain" conclusion (the organizational model clearly has no UI/design concepts to match against); medium confidence in the specific pattern-reuse recommendations (REC-002 in particular) since they're based on reading other skills' documented behavior, not yet validated against an actual implementation attempt
**Generated**: 2026-10-26

## Next Steps

1. **Populate PRJ-06's own `domain-model.md`** (currently an empty stub) using the 14 entities from `domain-concepts.md`, following the existing `01 - Skill Development Process/domain-model.md`'s format conventions (Domain Class Diagram, Actors, Core Entities, Key Relationships, Business Rules sections)
2. **Populate PRJ-06's own `vocabulary.md`** (currently just a bare heading) with the 12 business concepts and key terminology from `domain-concepts.md`, following the existing vocabulary.md's table format (Term | Definition | Synonyms | Notes)
3. Apply REC-001 and REC-002 when drafting the above
4. Proceed to `diagram-generatecollaboration` to visualize entity interactions, now that alignment confirms no conflicting organizational concepts need to be reconciled first
