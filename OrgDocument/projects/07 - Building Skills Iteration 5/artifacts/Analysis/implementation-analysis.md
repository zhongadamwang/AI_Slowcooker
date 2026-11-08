# Implementation Analysis

**Project**: PRJ-07  
**Date**: 2026-11-07  
**Status**: Proposed implementation design; no skills implemented  
**Inputs**: [Requirements](requirements.md), [confirmed decisions](../Source%20Materials/s5-modeling-decisions.md)

## Findings From the Existing Framework

| Evidence | Finding | Implementation consequence |
|----------|---------|----------------------------|
| [Skills catalog](../../../../../.github/skills/README.md) | S5 and S11 are separate documentation categories. | Move all six screen skills into S5; remove the active S11 category, not historical project records. |
| [Orchestrator catalog and UI extension](../../../../../.github/skills/edps-workflow-orchestrator/SKILL.md) | UI Model generation is manual; S33 uses S06 as an explicitly insufficient proxy prerequisite. | Register a real UI-model producer and check artifact readiness, not just domain-skill completion. |
| [Inventory skill](../../../../../.github/skills/screen-generateinventory/SKILL.md) and [gate](../../../../../.github/skills/screen-generateinventory/gate.json) | A screen references exactly one UI Model entry, not a domain entity directly. | Preserve this chain and the standalone inventory; add boundary checks through the referenced entry. |
| [UI domain model](../../../../orgModel/02%20-%20UI%20Prototype%20Skill%20Development%20Process/domain-model.md) | UIModelEntry already carries domain entity references and aggregation semantics. | Extend the existing contract, not replace it with a competing UI schema. |
| [Diagram skill](../../../../../.github/skills/diagram-generatecollaboration/SKILL.md) and [hierarchy validation](../../../../../.github/skills/hierarchy-validation/SKILL.md) | Participant stereotype and hierarchy structure already have authoritative validators. | A software system boundary is not the same thing as a `boundary` participant stereotype. Reuse VR/HR validation; do not duplicate or alter decomposition eligibility. |
| [Documentation gate](../../../../../.github/skills/documentation-automation/gate.json) | `documentation-automation` has skill ID S11. | Preserve that ID: the removed S11 category is not this skill ID. Preserve S33-S38 too. |
| [Orchestrator gate integration](../../../../../.github/skills/edps-workflow-orchestrator/SKILL.md) | Coordination and gate evaluation are documented procedures/reference code. No standalone completion-gates implementation is present in the inspected skill tree. | Integrate into the actual skill instructions, gate files, state contract, and executable validator; do not assume a deployed gate service exists or build a general-purpose one. |
| [Prototype regression suite](../../../../../.github/skills/screen-generatemockup/scripts/test_prototype_contract.py) | Python standard-library static checks exist, but explicitly do not prove browser behavior. | Reuse these checks and add targeted alignment tests; verify actual navigation/dialog behavior on the worked example. |

## Recommended Responsibility Split

Names are proposed from responsibilities, as authorized by the user.

1. **`usecase-generatemodel`**: produce a boundary-scoped use-case model and linked detailed scripts at every applicable hierarchy level.
2. **`ui-generatemodel`**: produce the existing UIModel/UIModelEntry structure from aligned domain/process/use-case inputs for software boundaries. This closes the known manual-generation gap.
3. **`model-validatealignment`**: own the single cross-model entity/system-boundary validation contract, report results, and request clarification. Include a small deterministic Python validator and tests, not a new workflow platform.

Existing skills remain owners of collaboration, domain/process documents, hierarchy decomposition, and prototype artifacts. The six `screen-*` skill names and their interactive pipeline remain unchanged.

## Proposed Artifacts and Shared Contract

Resolve the process folder from project metadata/hierarchy metadata. Do not hardcode a project-local `orgModel/` layout: this repository's process trees live under `OrgDocument/orgModel/`.

- **Per identified system-boundary level**: keep `domain-model.md`, `process.md`, and `collaboration.md`; add `use-case-model.md/json` and a `use-case-scripts/` directory with one linked script per use case and a meaningful `main.md`.
- **For software boundaries with UI requirements**: add `ui-model.md/json` using existing `model_id`, `entries`, `entry_id`, `domain_entity_refs`, and aggregation semantics. Preserve each screen's singular `ui_model_ref`.
- **Per modeling round**: write an alignment report in project `artifacts/Analysis/`, preserving prior round reports and model versions. Its manifest references the actual model documents and their entity/boundary definitions, so a JSON projection cannot silently disagree with Markdown.
- **Shared references**: boundary identity, explicit boundary type, hierarchy level/parent, scoped entity identity, actor identity, requirement references, and source/version references. Choose exact schema fields in T01. Retain existing IDs; scope them by model/boundary when local IDs collide.
- **Boundary typing**: record software status explicitly. Do not infer it from a folder name, participant stereotype, `control` eligibility, or the presence of a screen. Unknown type is an explicit unresolved classification, never permission to create a UI screen.
- **Alignment does not mean identical models**: different levels can expose different entities and details. Validate justified mappings, scope, and boundary membership; do not require every entity or process step to appear in every model.

### Use-Case Script Contract

Each use case identifies its actor, goal, system boundary, hierarchy level, and requirements. Its script records trigger, preconditions, ordered actor/system interactions, alternative/exception paths where applicable, and postconditions. Step references point to applicable process activities and domain entities; UI references are conditional on software-boundary UI applicability. Actors are relative to the boundary under analysis, not restricted to human actors or software-level users.

### Modeling-Round Contract

A round is a bounded creation or revision of the applicable models for an identified boundary and its affected parent/child boundaries. Intermediate edits may be incomplete; the round cannot be declared aligned without a current validation result.

1. Identify scope, source model versions, and affected boundaries.
2. Build/revise domain, process, and use-case models; build/revise UI models only where applicable.
3. Validate entities and system boundaries across the applicable model set.
4. Report `PASS`, `NEEDS_CLARIFICATION`, or `INVALID_INPUT` with item-level evidence and affected references. These are proposed report statuses, not arbitrary new orchestrator skill states.
5. For unresolved inconsistency, show focused clarification questions; record the answer, update the affected models, and revalidate.
6. A later edit invalidates the prior round's success for the affected model set; resume must check versions. A skip, rapid archetype, or solo self-attestation cannot convert inconsistency into successful alignment.

Non-software boundaries still have use cases and alignment validation. UI is explicitly not applicable there, rather than a fabricated empty screen. Software boundaries without UI requirements likewise do not force a prototype. Missing applicable models are reported rather than silently marked not applicable.

## Workflow Integration

Preserve the existing DAG for prerequisites; do not encode a refinement cycle as a cyclic DAG.

```text
Requirements + domain concepts
  -> collaboration/hierarchy and boundary identification
  -> scoped domain/process documents
  -> usecase-generatemodel
  -> ui-generatemodel (software boundary with UI requirements only)
  -> end-of-round model-validatealignment
  -> screen inventory -> layout -> mockup -> verified flow -> handoff/feedback
  -> any model-affecting feedback starts a new round and revalidation
```

For standalone modeling-skill invocations, document the same end-of-round validation obligation. Full workflows persist round/report references in project state and refuse to report alignment completion against stale artifacts. Prototype feedback continues through existing change-management, impact analysis, and orgModel update paths.

S5 membership is unconditional categorization; UI execution remains conditional on applicability. Do not force UI generation in every standard/rapid/compliance project.

## Impact Surfaces

- New skills: their `SKILL.md`, shared contract reference, gate files, executable validator, fixtures, and examples.
- Modeling producers: `diagram-generatecollaboration`, `hierarchy-management`, `documentation-automation`, `domain-alignentities`, `model-integration`, and `orgmodel-update`; entity/boundary references and validation hooks.
- UI consumers: all six screen skills and gates; preserve schemas/IDs, portability, standalone inventory, and actual control behavior.
- Coordination: orchestrator catalog/archetypes/state/completion events, navigator instructions and [workflow templates](../../../../../.github/skills/edps-skill-navigator/assets/workflow-templates.json), and affected prompt routing.
- Project lifecycle: `project-document-management` initialization/evolution rules and process-folder indexes.
- Change lifecycle: change-management and hierarchy impact reporting must include affected use-case/UI models and invalidate only applicable validation results.
- Validation/docs: hierarchy/compliance delegation, integration-testing, active skills catalog, maintained framework overview, shared process documentation, and Project 07 handoff.

Inventory exact references during implementation; the navigator's `.json` templates file contains Markdown with fenced JSON, so do not treat the whole file as plain JSON.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Category/skill ID collision | Assert the S11 category disappears while `documentation-automation` retains S11 and screen IDs retain S33-S38. |
| Entity names collide across hierarchy levels | Use scoped identities and explicit cross-level mappings; never infer identity from display name alone. |
| Validator checks only a detached manifest | Trace every definition to actual versioned model artifacts; test mismatches between source and projection. |
| Old models lack boundary typing | Report missing classification and request clarification before UI use; avoid global migration of historical projects. |
| Prototype changes accidentally bypass modeling | Map feedback to affected models and require a fresh round report where the contract changes. |
| Solo/rapid bypass weakens consistency | Keep model inconsistency checks mandatory and distinct from stakeholder-confirmation severity. |
| Concurrent rounds modify shared process models | Preserve source versions, detect stale reports, and serialize conflicting updates; parallelize independent task implementation only. |

## Release Acceptance

Demonstrate at least three levels including a non-software parent and software child, plus a software boundary without UI. Validate fresh/revised/resumed rounds, entity conflicts, boundary conflicts, unknown typing, unresolved clarification, and stale reports. Prove all 11 requirements have passing evidence and preserve the current UI interaction contract.

No new framework, external API, broad historical migration, or production application is required.
