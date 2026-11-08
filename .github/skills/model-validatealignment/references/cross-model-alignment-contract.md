# Cross-Model Alignment Contract

**Owning skill**: `model-validatealignment` (new, S39 — see Skill ID Ledger below)
**Consumed by**: `usecase-generatemodel` (new, S32), `ui-generatemodel` (new, S40), the six existing `screen-*` skills (S33–S38), `domain-alignentities`, `model-integration`, `orgmodel-update`, `hierarchy-management`, `hierarchy-validation`, `diagram-generatecollaboration`, `edps-workflow-orchestrator`
**Status**: Draft — T01 of PRJ-07 (Building Skills Iteration 5)
**Version**: 1.0.0
**Created**: 2026-11-08

## Purpose and Scope

This is the single shared contract referenced by every skill that participates in cross-model alignment across the **UI model**, **use-case model**, **domain model**, and **process model**. It exists so that T02 (`usecase-generatemodel`), T03 (`ui-generatemodel`), and T04 (`model-validatealignment`'s own validator) implement against one agreed schema rather than three incompatible ad-hoc ones.

This document **extends** existing conventions; it does not replace or compete with them:
- It **reuses** `UIModel`/`UIModelEntry`/`Aggregation` exactly as defined in `OrgDocument/orgModel/02 - UI Prototype Skill Development Process/domain-model.md` (D-02). No competing UI schema is introduced here.
- It **reuses** `hierarchy-management`'s hierarchy metadata and folder-decomposition structure, and **delegates** all file/link integrity and cross-level participant-type checks (HV/HX/HN rules) to `hierarchy-validation`, per that skill's own exclusive-ownership statement.
- It **reuses** `diagram-generatecollaboration`'s VR-1–VR-4 boundary-validation rules (participant stereotype classification, boundary-first reception) as the authority on diagram-level boundary correctness. This contract's "system boundary" concept is a **superset concern**: every `boundary`-stereotype participant corresponds to a system boundary in this contract's sense, but not every system boundary identified here need be a decomposed `control`-type participant with its own sub-folder — see Section 2.1 for the precise distinction.
- It **preserves** every screen's singular `ui_model_ref` (never a direct domain-entity reference) and the existing `SCR-[###]`/`UME-[###]`/`LS-[###]`/`IM-[###]`/`IF-[###]`/`DD-[###]`/`FB-[###]` ID formats from `ui-prototyping-conventions.md`.
- It does **not** redefine `documentation-automation` (S11) or renumber `screen-generateinventory` through `screen-discussfeedback` (S33–S38).

## Skill ID Ledger (this task's allocation)

Per the orchestrator's Skill Catalogue (`edps-workflow-orchestrator/SKILL.md`), the full currently-used ID range is S00–S38 with exactly one gap: **S32**. This task allocates:

| Skill | Skill ID | Rationale |
|---|---|---|
| `usecase-generatemodel` | **S32** | Fills the one existing gap in the S00–S38 range rather than extending past S38, where a gap already existed unused |
| `model-validatealignment` | **S39** | New sequential ID, first allocated past the existing S38 ceiling |
| `ui-generatemodel` | **S40** | New sequential ID, second allocated past S38 |

No existing skill ID is renumbered. `documentation-automation` keeps **S11**; `screen-generateinventory` through `screen-discussfeedback` keep **S33–S38** exactly as registered in T10 (PRJ-06). This satisfies the acceptance criterion "new responsibility-based names and unused skill IDs are selected without renumbering S11 or S33-S38."

## 1. Shared Reference Types

All four models (domain, process, use-case, UI) that need to agree on "what entity/boundary are we both talking about" use these shared reference shapes. A reference is a *pointer*, never a duplicate definition — the authoritative definition always lives in exactly one owning document (see Section 1.4).

### 1.1 Scoped Entity Reference

```json
{
  "entity_id": "string",
  "entity_name": "string",
  "scope": "string",
  "defined_in": "string (relative path to the owning domain-model.md or process folder)"
}
```

- **`entity_id`**: the domain entity's existing identifier as it appears in that boundary's `domain-model.md`. Not globally unique across boundaries — see `scope`.
- **`entity_name`**: display name, for human-readable diagnostics only; **never** used to infer identity (per the Implementation Analysis's "never infer *** from display name alone" risk mitigation).
- **`scope`**: the identifying boundary path this entity ID is local to (see 1.2). Two entities with the same `entity_id` but different `scope` are **different entities** — this is how the "scoped entity-name collision" fixture (Acceptance Criterion 2) is resolved: collision is permitted and harmless because identity is `(scope, entity_id)`, not `entity_id` alone.
- **`defined_in`**: resolves to the actual `domain-model.md` (or `process.md`, for process-step-scoped entities) that is the authoritative source. A validator must be able to open this path and confirm the entity actually appears there — a reference that cannot be resolved to its `defined_in` document is a validation failure, not a silent pass (closing the "validator checks only a detached manifest" risk).

### 1.2 System Boundary Reference

```json
{
  "boundary_id": "string",
  "boundary_name": "string",
  "boundary_type": "software | non-software | unknown",
  "hierarchy_level": "integer (0 = root)",
  "hierarchy_path": "string (relative path to the boundary's process folder)",
  "parent_boundary_id": "string | null",
  "corresponds_to_participant": "string | null (collaboration.md participant alias, if this boundary is also a decomposed control-type participant)"
}
```

- **`boundary_type`** is the field this entire contract exists to make explicit and non-inferred. Valid values are exactly `software`, `non-software`, or `unknown`. **`unknown` is an explicit, first-class, unresolved classification — never silently treated as `non-software`, and never used to justify creating a UI screen.** This directly implements R-011 and the Implementation Analysis's explicit instruction not to infer software status from folder name, participant stereotype, `control` eligibility, or screen presence.
- **`hierarchy_level`/`hierarchy_path`**: anchors this boundary to its actual position in the process hierarchy tree that `hierarchy-management`/`hierarchy-validation` already maintain. This contract does not introduce a second hierarchy; it annotates the existing one.
- **`corresponds_to_participant`**: **optional, and frequently absent.** This is the field that prevents conflating boundary type with participant stereotype (an explicit requirement from T01's own description — Do not conflate boundary type with participant stereotype). A system boundary in this contract's sense (e.g., "the physical warehouse," "the customer's own home," "a third-party courier company") may have **no** corresponding `control`/`boundary`-stereotype participant in any `collaboration.md` at all — it's a real-world system boundary with actors and use cases, but not a software/decomposition artifact. Conversely, every `control`-type participant that *is* decomposed per HV-1 **does** have a corresponding boundary reference here, with this field populated. **Boundary stereotype (a collaboration-diagram annotation) and this contract's `boundary_type` (software/non-software/unknown) are independent axes** — a `boundary`-stereotype participant inside a diagram says nothing by itself about whether the real-world system boundary it represents is software-typed; that judgment is made explicitly, per Section 2.1.

### 1.3 Actor Reference (relative to a boundary)

```json
{
  "actor_id": "string",
  "actor_name": "string",
  "boundary_id": "string (the boundary this actor interacts with, per Section 1.2)",
  "actor_kind": "human | organization | external-system | internal-role"
}
```

Actors are always defined **relative to a specific boundary** (per the confirmed decision: "Actors are relative to the boundary under analysis, not restricted to human actors or software-level users"). The same real-world person or organization may be a distinct `Actor Reference` at each boundary level they interact with — this is intentional, not a modeling error, because "actor" here means "role relative to this boundary," not a single global identity record.

### 1.4 Ownership Rule (single source of truth per reference)

| Reference kind | Authoritative owning document | Who may define new ones |
|---|---|---|
| Scoped Entity Reference | that boundary's `domain-model.md` | `domain-extractconcepts`, `domain-alignentities`, `domain-proposenewconcepts` (unchanged) |
| System Boundary Reference | that boundary's `main.md` (new `## System Boundary` section — see Section 5) | `hierarchy-management` (initial creation), this contract's validator (classification only, never creation) |
| Actor Reference | that boundary's `use-case-model.md` (new, Section 3) | `usecase-generatemodel` only |
| UIModelEntry | `ui-model.md`/`.json` (existing, D-02) | `ui-generatemodel` (new) — the existing manual-authoring gap this task closes |

No reference is ever *redefined* by a consuming skill — a skill that needs to reference an entity, boundary, or actor includes a **reference** (the shapes above), and a validator resolves that reference back to its one authoritative definition. This is what makes alignment checkable: disagreement means two references pointing at incompatible `defined_in` targets, or a reference that fails to resolve at all, not a vague semantic judgment call.

## 2. Boundary Typing

### 2.1 Explicit Declaration, Never Inferred

Every System Boundary Reference (Section 1.2) must have its `boundary_type` **explicitly declared** at the time the boundary is first identified (typically during `hierarchy-management` decomposition or `usecase-generatemodel`'s own boundary discovery for non-decomposed real-world boundaries). The declaration is recorded in that boundary's `main.md` (Section 5) as a plain, human-readable statement with its rationale — not inferred by any downstream skill from:
- the folder name (a folder named `...Boundary` is a structural/decomposition artifact per HN-1, not evidence of software type)
- the `boundary`/`control`/`actor`/`entity` participant stereotype (an orthogonal diagram-annotation axis, per Section 1.2)
- `control`-type decomposition eligibility (HV-1 eligibility is about diagram structure, not real-world software status)
- the presence or absence of a Screen/UIModelEntry (that would be circular: UI applicability is *downstream* of boundary type, per Section 2.2, not evidence for it)

If a boundary's type has not yet been explicitly declared, every skill in this contract's scope must report it as `unknown` and treat that as an **unresolved classification requiring clarification** (Section 4.3) — never as a default of `non-software`, and never as silent permission to proceed with UI generation.

### 2.2 UI Applicability Rule (R-011)

- UI screens (Screens/UIModelEntries, per D-02) may exist **only** within boundaries whose `boundary_type` is explicitly `software`.
- This is **not** a requirement that every `software`-typed boundary have a screen, nor that every use case or process activity within a software boundary have one. `ui-generatemodel` (Section 6) decides screen-worthiness per its own aggregation logic, same as the existing `screen-generateinventory`'s "orphaned entries should be a deliberate, noted decision" convention — this contract only gates *where* UI may exist, not *how much* of it must exist there.
- A boundary with `boundary_type: "non-software"` or `"unknown"` must have **zero** UIModelEntries referencing it. A validator finding a UIModelEntry whose aggregated domain entities trace back to a non-software or unknown-typed boundary reports a hard alignment failure (Section 4), not a warning.

## 3. Use-Case Model and Script Extensions

This contract defines the **shape** that `usecase-generatemodel` (T02) must produce; T02's own `SKILL.md` defines the generation *process*. Both must conform to this shape.

### 3.1 Use-Case Model (`use-case-model.md`/`.json`)

Stored per-boundary, alongside that boundary's existing `domain-model.md`/`process.md`/`collaboration.md` (not consolidated into one project-wide file — mirroring how `domain-model.md` is already per-boundary in a decomposed hierarchy).

```json
{
  "model_id": "string",
  "boundary_ref": "System Boundary Reference (Section 1.2)",
  "actors": ["Actor Reference (Section 1.3), ..."],
  "use_cases": [
    {
      "use_case_id": "string (UC-[###], scoped per boundary — see 3.3)",
      "name": "string",
      "goal": "string",
      "primary_actor_ref": "Actor Reference",
      "boundary_ref": "System Boundary Reference (always the same as the model's own boundary_ref)",
      "requirement_refs": ["string, ..."],
      "script_ref": "string (relative path to this use case's script file)"
    }
  ],
  "generated_at": "ISO-8601",
  "changelog": [{ "version": "string", "date": "string", "change": "string" }]
}
```

### 3.2 Use-Case Script (one file per use case, in `use-case-scripts/`)

Per the Implementation Analysis's Use-Case Script Contract, each script records:

```markdown
# Use Case Script — [Name] (UC-[###])

**Actor**: [Actor Reference]
**Goal**: [string]
**System Boundary**: [System Boundary Reference]
**Hierarchy Level**: [integer]
**Requirement References**: [R-xxx, ...]

## Changelog
- v1.0 ([date]): Initial generation

## Trigger
[What starts this use case]

## Preconditions
- [condition, ...]

## Main Flow
1. [Actor/system step, referencing process activities/domain entities where applicable]
2. ...

## Alternative / Exception Paths
*(Omit this section entirely if none apply — do not generate an empty placeholder.)*
- **[Condition]**: [what happens instead, from which main-flow step]

## Postconditions
- [condition, ...]

## UI References
*(Only present if this use case's boundary_type is `software` AND at least one step has an actual Screen/UIModelEntry mapping. Omit entirely otherwise — never a placeholder "N/A" section.)*
- Step [N] → [Screen SCR-xxx / UIModelEntry UME-xxx]
```

### 3.3 Use-Case ID Scoping

`UC-[###]` is scoped per boundary (same pattern as `UME-[###]`'s per-model scoping, per `ui-prototyping-conventions.md` Section 1) — not globally unique across the whole project. A use case at a parent boundary and one at a child boundary may both be `UC-001`; they are disambiguated by their differing `boundary_ref`, exactly as `UME-[###]` is disambiguated by which model (base/derived) it belongs to.

## 4. Alignment Validation and the Modeling Round

### 4.1 Round Definition

A **modeling round** is a bounded creation or revision of the applicable models (domain, process, use-case, and — where applicable — UI) for one identified boundary and any affected parent/child boundaries. A round is **not** a cyclic DAG node; it is a bounded, versioned unit of work layered on top of the existing linear DAG (`usecase-generatemodel` → `ui-generatemodel` → screen pipeline), per the Implementation Analysis's explicit instruction to preserve the existing DAG rather than encode a refinement cycle as one.

### 4.2 Round Report

Every round, on completion, produces an **Alignment Report**, written to that project's `artifacts/Analysis/alignment-report-[round-id].md` (prior rounds' reports are preserved, never overwritten — same convention as `change-management`'s append-only change history).

```json
{
  "round_id": "string",
  "boundary_scope": ["System Boundary Reference, ..."],
  "source_model_versions": {
    "domain_model": "string (version or commit-like reference)",
    "process_model": "string",
    "use_case_model": "string",
    "ui_model": "string | null (null if not applicable to any boundary in scope)"
  },
  "status": "PASS | NEEDS_CLARIFICATION | INVALID_INPUT",
  "findings": [
    {
      "finding_id": "string",
      "severity": "error | clarification-needed",
      "reference_a": "the reference (Section 1) found in one model",
      "reference_b": "the conflicting or unresolved reference found in another model, or null if reference_a simply fails to resolve",
      "description": "string",
      "affected_models": ["domain | process | use-case | ui, ..."]
    }
  ],
  "clarification_questions": ["string, ... (only present when status is NEEDS_CLARIFICATION)"],
  "generated_at": "ISO-8601"
}
```

### 4.3 Status Semantics

- **`PASS`**: every entity and system-boundary reference across the applicable model set for this round's scope resolves consistently — same `(scope, entity_id)` pairs mean the same thing everywhere they're referenced, every `boundary_type` in scope is explicitly declared (never `unknown` left unresolved), and no UIModelEntry references a non-software or unknown boundary.
- **`NEEDS_CLARIFICATION`**: at least one finding exists that is genuinely ambiguous (e.g., an entity-name collision across boundaries without an established scoping relationship, a boundary with `unknown` type that a use case or UI model depends on). The round **cannot** be reported as aligned. Clarification questions are specific and reference the actual conflicting items (same discipline already used by `screen-discussfeedback`'s `[REVIEW NEEDED]` convention and the price-book-test pipeline run's handling of genuinely ambiguous fields — do not invent a plausible-sounding resolution).
- **`INVALID_INPUT`**: a reference fails to resolve to its `defined_in` target at all (e.g., points to a `domain-model.md` that doesn't contain that entity), or a required model is missing entirely for a boundary in scope. This is reported, not silently treated as "not applicable" (per the Implementation Analysis's explicit instruction: "Missing applicable models are reported rather than silently marked not applicable").

### 4.4 Non-Bypassable Alignment Completion

- A round's success (`PASS`) can **only** be set by `model-validatealignment`'s own validator actually running against the current model artifacts. No other skill, gate, or workflow archetype may mark a round as aligned.
- **Solo-mode self-attestation does not apply to this check.** The existing `stakeholder_confirmation` gate-check type's solo/traditional severity resolution (`resolveCheckSeverity()` in `edps-workflow-orchestrator`) is explicitly **not reused here** — model inconsistency is a factual, checkable property of the artifacts themselves, not a stakeholder confirmation of satisfaction. A `rapid` archetype's generally more lenient gate severities, and a solo developer's self-attestation privilege elsewhere in the framework, **cannot convert an inconsistency into a successful alignment report.** This directly implements the Implementation Analysis's risk mitigation: "Keep model inconsistency checks mandatory and distinct from stakeholder-confirmation severity."
- **Revision invalidates prior rounds.** If any model document within a round's `boundary_scope` is edited after that round's report was written, the prior round's `PASS` status is stale for that scope. A `resume` (orchestrator-level or manual) must check `source_model_versions` against the current artifacts before treating a prior round's `PASS` as still valid. A stale `PASS` is reported as stale, not silently trusted.
- **Clarification and revalidation.** When a round is `NEEDS_CLARIFICATION`, the workflow is: surface the clarification question(s) → record the human/self-attested (in solo mode, with the same role-play discipline as `requirements-sanitize`/`process-w5h`) answer → update the affected model document(s) → re-run validation → only then may the round transition to `PASS`. A round cannot skip directly from `NEEDS_CLARIFICATION` to `PASS` without an intervening re-validation against updated artifacts.

## 5. File and Folder Layout (Additive to Existing Conventions)

```
[boundary folder, e.g. OrgDocument/orgModel/[NN] - [Process Name]/ or a decomposed sub-boundary folder]/
├── main.md                         ← existing; gains a new "## System Boundary" section (Section 1.2 fields, human-readable)
├── domain-model.md                 ← existing, unowned by this contract
├── process.md                      ← existing, unowned by this contract
├── collaboration.md                ← existing, unowned by this contract
├── use-case-model.md               ← NEW (T02), Section 3.1
├── use-case-model.json             ← NEW (T02)
├── use-case-scripts/                ← NEW (T02)
│   ├── main.md                     ← index of scripts in this folder
│   └── UC-001-[slug].md            ← Section 3.2, one file per use case
├── ui-model.md                     ← existing per D-02 (T03, PRJ-06); NOW machine-generated by ui-generatemodel (T03 of PRJ-07) where boundary_type is software, instead of manually authored
└── ui-model.json                   ← existing per D-02

[project folder]/artifacts/Analysis/
└── alignment-report-[round-id].md  ← NEW, Section 4.2, one per round, never overwritten
```

No new project-level artifact category is introduced; `alignment-report-*.md` lives in the existing `Analysis` category (same as `requirements.md`, `domain-concepts.md`, etc. — an analysis output, not source material, not a change record).

## 6. Compatibility Notes for `ui-generatemodel` (T03)

`ui-generatemodel` produces the **same** `UIModel`/`UIModelEntry`/`Aggregation` JSON shape already defined in D-02 — this contract does not add new fields to that shape. Its only new behavior relative to the current manual process is: given a `software`-typed boundary's domain model, use-case model, and process model as inputs, it produces `ui-model.md`/`.json` automatically, closing the orchestrator's previously-documented "S33 uses S06 as an explicitly insufficient proxy prerequisite" gap. `screen-generateinventory` (S33)'s own precondition check continues to apply unchanged: it still verifies a UI Model actually exists and is non-empty before proceeding, regardless of whether that UI Model was produced manually or by `ui-generatemodel`.

A `UIModelEntry`'s `domain_entity_refs` (existing field, D-02) must, under this contract, resolve to Scoped Entity References (Section 1.1) whose `scope` matches a `software`-typed boundary. `model-validatealignment` is what actually checks this; `ui-generatemodel` is expected to only ever produce compliant entries in the first place, not rely on the validator to catch its own mistakes after the fact.

## 7. Compatibility Notes for the Six Existing Screen Skills (S33–S38)

No schema change to any of `screen-generateinventory`, `screen-generatelayout`, `screen-generatemockup`, `screen-generateflow`, `screen-assembledocument`, or `screen-discussfeedback` is required or proposed by this contract. Their existing gates, ID formats, portability requirements, and file layouts (per `ui-prototyping-conventions.md`) are unchanged. The only new integration point is **upstream**: `ui-generatemodel`'s output is consumed by `screen-generateinventory` exactly as a manually-authored `ui-model.json` would be — the screen pipeline cannot and does not need to distinguish how its input UIModel was produced.

## 8. Fixtures (Positive and Negative) — See `fixtures/`

Per Acceptance Criteria 2–3, this contract ships with worked fixtures validating the rules above, not just prose claims about them:

- `fixtures/three-level-valid/` — a three-level hierarchy (non-software parent boundary → software child boundary → further nested boundary) with a deliberate scoped entity-name collision across two of the levels, demonstrating `PASS` because `(scope, entity_id)` disambiguates the collision correctly.
- `fixtures/unknown-boundary-type/` — a boundary with no declared `boundary_type`, with a use case and a UIModelEntry attempted against it, demonstrating `NEEDS_CLARIFICATION` with a specific clarification question, and demonstrating the UIModelEntry attempt itself is rejected rather than silently created.
- `fixtures/missing-applicable-model/` — a boundary where the use-case model is absent entirely, demonstrating `INVALID_INPUT` (missing model reported, not silently treated as not-applicable).
- `fixtures/manifest-source-disagreement/` — a round report whose manifest claims an entity exists in a `domain-model.md` that does not actually contain it, demonstrating the validator actually opens and checks the referenced document rather than trusting the manifest at face value.
- `fixtures/software-boundary-no-ui-required/` — a `software`-typed boundary with use cases and process activities but deliberately zero UIModelEntries, demonstrating R-011's "software boundaries do not automatically require a screen" is respected, not silently flagged as incomplete.

Each fixture folder contains the full set of model documents for its scenario plus an `expected-report.json` the validator (T04) must reproduce exactly (`status` and `finding_id`s, at minimum) when implemented.

## 9. Glossary Additions (extends `vocabulary.md`, does not redefine it)

- **System boundary** (this contract's sense): a real-world or architectural boundary around a coherent set of actors and interactions, independent of whether it corresponds to a diagram `boundary`-stereotype participant or a decomposed `control`-type folder. See Section 1.2/2.1.
- **Modeling round**: a bounded, versioned unit of cross-model creation/revision for one or more boundaries, concluding in an Alignment Report. See Section 4.1.
- **Alignment Report**: the structured, round-scoped record of validation findings and status. See Section 4.2.
- **Use case** (confirmed terminology, per `requirements.md`'s Confirmed Decisions): a named actor–boundary interaction with a goal, documented via a linked script. See Section 3.
