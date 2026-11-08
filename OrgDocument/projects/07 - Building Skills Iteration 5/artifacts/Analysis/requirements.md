# Requirements Analysis Report

**Project**: PRJ-07 - Building Skills Iteration 5  
**Source**: [Original request](../Source%20Materials/s5-modeling-integration.md)  
**Decision source**: [User responses](../Source%20Materials/s5-modeling-decisions.md)  
**Generated**: 2026-11-07  
**Total Requirements**: 11  
**Status**: Decisions incorporated - Implementation not started

## Goal

Make S5 - Design & Visualization a coherent modeling workflow that includes UI prototyping and use-case modeling alongside domain and process models.

## Requirements

| ID | Source section | Requirement | Tags | Confidence |
|----|----------------|-------------|------|------------|
| R-001 | Original Request, sentence 1 | Integrate the existing UI Prototype skills into S5 - Design & Visualization. | functional | high |
| R-002 | Original Request, sentence 2 | Treat the UI model as a modeling artifact within the design workflow, not merely as a prototype output. | constraint | high |
| R-003 | Original Request, sentence 3 | Create a use-case skill that builds a use-case model. | functional | high |
| R-004 | Original Request, sentence 3 | The use-case skill shall produce use-case scripts describing the detailed process for each modeled use case. | functional | high |
| R-005 | Original Request, sentence 4 | Keep the UI model, use-case model, domain model, and process model aligned. | constraint | high |
| R-006 | Original Responses, bullet 3 | Replace S11 - UI Prototyping as a separate category with membership in S5 - Design & Visualization. | constraint | high |
| R-007 | Original Responses, bullet 4 | Use cases shall describe actor interactions with an identified system boundary at every hierarchy level where such a boundary exists. | functional | high |
| R-008 | Original Responses, bullet 5, sentence 1 | Use entities and system boundaries as the alignment contract across UI, use-case, domain, and process models. | constraint | high |
| R-009 | Original Responses, bullet 5, sentence 2 | Perform model-alignment validation at the end of every modeling round. | functional | high |
| R-010 | Original Responses, bullet 5, sentence 3 | Request clarification for unresolved model inconsistencies rather than treating them as aligned. | functional | high |
| R-011 | Original Responses, bullet 6 | UI screens shall exist only within software-type boundaries. | constraint | high |

## Proposed Acceptance Checks

These checks operationalize the confirmed requirements for later planning. Detailed schemas and validation mechanics remain implementation design work; the decisions below are confirmed.

| Requirement | Proposed verification |
|-------------|-----------------------|
| R-001 | S5 documentation and workflow routing include all six existing UI Prototype skills, preserving their inventory, layout, mockup, flow, handoff, and feedback pipeline. |
| R-002 | The workflow identifies the UI model's inputs, outputs, and relationships to the other models; prototype artifacts reference the UI model they realize. |
| R-003 | A new skill generates a use-case model with identifiable actors, goals, use cases, system boundaries, and links to source requirements. |
| R-004 | Each modeled use case has a linked script covering its trigger, preconditions, actor/system steps, alternative or exception paths where applicable, and postconditions. |
| R-005 | A representative example demonstrates agreement across the four models on entities and system boundaries, with traceability to applicable use-case interactions, process activities, and UI interactions. |
| R-006 | Active skill catalogs and workflow category mappings place all six UI Prototype skills in S5 and no longer retain S11 as a separate category. Historical records need not be rewritten. |
| R-007 | A multi-level example models actor interactions at each level with an identified system boundary, including a non-software boundary; scope is not restricted to software or leaf-level boundaries. |
| R-008 | Validation checks entity references and system-boundary definitions across the applicable models, exposing contradictory identity, scope, or boundary membership. |
| R-009 | Each modeling round ends with an alignment-validation result, including rounds that revise existing models. |
| R-010 | An example with unresolved entity or boundary disagreement produces an explicit clarification request and remains unresolved until clarification and revalidation; it does not report successful alignment. |
| R-011 | A mixed-boundary example assigns every UI screen to a software-type boundary and creates no UI screens for non-software boundaries. Software boundaries do not automatically require a screen. |

## Existing Framework Context

The [skills catalog](../../../../../.github/skills/README.md) currently lists UI Prototyping separately under S11. Its six skills are:

1. `screen-generateinventory`
2. `screen-generatelayout`
3. `screen-generatemockup`
4. `screen-generateflow`
5. `screen-assembledocument`
6. `screen-discussfeedback`

S5 currently lists `diagram-generatecollaboration`, `hierarchy-management`, `documentation-automation`, and `migration-tools`. This report records the desired integration; it does not modify those skills or the catalog.

## Confirmed Decisions

- **Terminology**: "Use case" is the confirmed wording. Original source wording is preserved.
- **Skill naming**: Generate final skill names from their responsibilities; there are no fixed naming rules imposed by this request.
- **Category membership**: Replace S11 with S5 membership, rather than keeping a second UI Prototyping category.
- **Use-case scope**: Describe actor interactions with an identified system boundary at all applicable hierarchy levels, including non-software boundaries.
- **Alignment contract**: Entities and system boundaries are the shared contract across the four models.
- **Validation cadence**: Validate alignment at the end of every modeling round. Unresolved inconsistencies require clarification; they are not successful alignment.
- **UI applicability**: UI screens exist only within software-type boundaries. This does not require every software boundary, activity, or use case to have a screen.

## Remaining Implementation Design

- Generate responsibility-based skill names and select artifact formats and locations.
- Define how entity and boundary references are represented and compared, and which skill owns end-of-round validation and clarification handling.
- These implementation details do not reopen the confirmed scope decisions above.

## Scope Boundary

This step captures requirements only. Skill implementation, workflow/gate changes, generated models, task derivation, and updates to the shared organizational process model are deferred.

## Glossary Suspects

- **UI model**: Model of user-facing interactions and screens; distinct from rendered prototypes.
- **Use-case model**: Model of actors and their interactions with identified system boundaries at applicable hierarchy levels.
- **Use-case script**: Detailed scenario describing how a use case proceeds.
- **Model alignment**: Agreement on entities and system boundaries across UI, use-case, domain, and process models, validated after each modeling round.
- **Software-type boundary**: A system boundary typed as software; the only boundary type within which UI screens may exist.
