---
name: usecase-generatemodel
description: Generate or revise boundary-scoped use-case models and detailed use-case scripts from requirements, domain/process/collaboration documents, and the shared cross-model alignment contract. Describes actor interactions with an identified system boundary at every applicable hierarchy level, including non-software boundaries. Use when modeling actor-boundary interactions, documenting detailed use-case scripts, or extending an existing use-case model across a new boundary level.
license: MIT
metadata:
  version: 0.1.0
  last-updated: "2026-11-08"
---

# Use Case Generate Model

Generate a boundary-scoped use-case model and its linked detailed scripts, from requirements and the scoped process/domain/collaboration documents already present at that boundary.

## Intent

Per PRJ-07's confirmed decisions (R-003, R-004, R-007, R-008): produce a use-case model whose actors and use cases are always defined **relative to a specific system boundary** (never a human-only, software-only, or leaf-level restriction), with every use case backed by a linked, detailed script covering trigger, preconditions, ordered steps, applicable alternatives/exceptions, and postconditions.

This skill is scoped **per boundary**, not per project — the same project's hierarchy may have a use-case model at its root boundary, another at a software child boundary, and another at a further-nested grandchild boundary, each independently generated/revised, each tracing its own actors and use cases back to that boundary alone.

## Shared Contract

**Read in full before implementing against this skill**: [`../model-validatealignment/references/cross-model-alignment-contract.md`](../model-validatealignment/references/cross-model-alignment-contract.md) — Section 1 (reference shapes), Section 3 (use-case model/script schema this skill must produce), Section 3.3 (ID scoping).

This skill produces content; it does **not** self-certify alignment. `model-validatealignment` is the sole owner of end-of-round validation (contract Section 4.4) — this skill's output is an *input* to that validation, not a substitute for it.

## Inputs

- **Primary**: the target boundary's existing `domain-model.md`, `process.md`, and `collaboration.md` (already present per `hierarchy-management`/`documentation-automation`'s existing process-folder conventions)
- **Primary**: that boundary's `main.md`, specifically its `## System Boundary` section (contract Section 1.2/5) — **required** before this skill may run. If `boundary_type` is not yet explicitly declared there, this skill must stop and surface the same clarification question `model-validatealignment` would raise (contract Section 2.1), not guess a type or proceed as if it were declared.
- **Secondary**: `artifacts/Analysis/requirements.json` (from `requirements-ingest`), scoped to the requirements relevant to this boundary
- **Secondary**: for a child boundary, its parent boundary's use-case model (if one exists) — used only for consistency checking of parent/child actor naming (contract HV-3-adjacent, informational), never to constrain which use cases the child boundary may have

> **Pre-condition**: A target boundary must already exist in the process hierarchy (a folder with `main.md`, produced by `hierarchy-management`), and that boundary's `main.md` must have an explicit `## System Boundary` section with a declared `boundary_type`. If either is missing, this skill cannot proceed to generate use cases for that boundary — see Workflow Step 0.

## Outputs

**Files Generated** (per contract Section 5, written alongside the boundary's existing `domain-model.md`/`process.md`/`collaboration.md`):
- `use-case-model.md` — human-readable model (primary)
- `use-case-model.json` — structured model for downstream consumption (`model-validatealignment`, `ui-generatemodel`)
- `use-case-scripts/main.md` — index of this boundary's scripts
- `use-case-scripts/UC-[###]-[slug].md` — one detailed script per modeled use case

### JSON Structure (`use-case-model.json`)

```json
{
  "model_id": "UCM-[boundary-slug]",
  "boundary_ref": {
    "boundary_id": "string",
    "boundary_name": "string",
    "boundary_type": "software | non-software | unknown",
    "hierarchy_level": 0,
    "hierarchy_path": "string",
    "parent_boundary_id": "string | null"
  },
  "actors": [
    { "actor_id": "A-001", "actor_name": "string", "boundary_id": "string", "actor_kind": "human | organization | external-system | internal-role" }
  ],
  "use_cases": [
    {
      "use_case_id": "UC-001",
      "name": "string",
      "goal": "string",
      "primary_actor_ref": "A-001",
      "boundary_ref": "same boundary_id as the model's own boundary_ref",
      "requirement_refs": ["R-xxx"],
      "script_ref": "use-case-scripts/UC-001-[slug].md"
    }
  ],
  "generated_at": "ISO-8601",
  "changelog": [{ "version": "1.0", "date": "ISO-8601", "change": "Initial generation" }]
}
```

Field conventions (per contract Section 3.1/3.3):
- `use_case_id`: `UC-[###]`, zero-padded 3-digit, **scoped per boundary** — not globally unique across the project. Scan this boundary's own existing `use-case-model.json` for the highest number, increment, verify uniqueness (same algorithm as `screen-generateinventory`'s `SCR-[###]` and `change-management`'s `generate_change_id()`).
- `primary_actor_ref`: singular — a use case has exactly one primary actor (secondary/supporting actors, if any, are documented in the script's Main Flow narrative, not modeled as additional structured references in v1).
- `boundary_ref` (on each use case): always identical to the model's own `boundary_ref.boundary_id` — a use case never references a different boundary than the model it belongs to. (A use case's *script* may reference process activities or entities from the same boundary; it does not reach into a different boundary's use-case model.)

### Markdown Structure (`use-case-model.md`)

```markdown
# Use-Case Model — [Boundary Name]

**Boundary ID**: [boundary_id]
**Boundary Type**: [software | non-software | unknown]
**Hierarchy Level**: [N]
**Generated**: [timestamp]

## Changelog
- v1.0 ([date]): Initial generation

## Actors
### [Actor Name] *(A-001)*
**Kind**: [human | organization | external-system | internal-role]

## Use Cases

### [Use Case Name] *(UC-001)*
**Goal**: [string]
**Primary Actor**: [Actor Name] (A-001)
**Script**: [use-case-scripts/UC-001-[slug].md](use-case-scripts/UC-001-[slug].md)
*(Ref: R-xxx)*

---
**Traceability**: Every use case traces to its boundary, a primary actor, and one or more requirements
**Generated**: [timestamp]
```

### Use-Case Script Structure (`use-case-scripts/UC-[###]-[slug].md`)

Exactly the shape in contract Section 3.2 — reproduced here for convenience, contract is authoritative:

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

## Alternative / Exception Paths
*(Omit entirely if none apply.)*
- **[Condition]**: [what happens instead, from which main-flow step]

## Postconditions
- [condition, ...]

## UI References
*(Only present if boundary_type is `software` AND at least one step has an actual Screen/UIModelEntry mapping. Omit entirely otherwise.)*
- Step [N] → [Screen SCR-xxx / UIModelEntry UME-xxx]
```

## Workflow

### Step 0 — Verify the boundary is ready

Before generating anything, confirm:
1. The target boundary's folder and `main.md` exist (if not: stop, this is a `hierarchy-management` precondition, not something this skill creates).
2. `main.md`'s `## System Boundary` section has an explicit `boundary_type`. If it reads `unknown` or is absent entirely, **stop** and surface the clarification question from the contract (Section 2.1) rather than guessing or defaulting. Do not generate a partial use-case model "pending" classification — either the boundary type is known, or generation does not proceed.

This mirrors `screen-generateinventory`'s own pre-condition discipline (stopping cleanly when its required input, a UI Model, doesn't exist yet) rather than inventing a fallback.

### Step 1 — Identify actors relative to this boundary

Read the boundary's `domain-model.md` and `collaboration.md` for candidate actors. An actor here is **whoever/whatever interacts with this boundary from outside it** — per the confirmed decision, this is explicitly **not** restricted to human users: an external system, another organization, a scheduled trigger, or an internal role performing work *within* a non-software boundary are all valid actors (see the `software-boundary-no-ui-required` fixture's "Nightly Scheduler" for a worked internal-role/non-human example).

Do not reuse a parent boundary's actor list wholesale — a parent's "Customer" actor and this (child) boundary's "Customer" actor are, per contract Section 1.3, **different Actor References** even if they're the same real-world person, because actor identity here is relative to the boundary. Define this boundary's own actors from scratch, informed by (not copied from) the parent.

### Step 2 — Identify use cases and their requirement backing

For each distinct actor goal at this boundary evidenced by the requirements and process documents, create one use case. A use case with no supporting `requirement_refs` is a signal to reconsider whether it's actually needed — same discipline as `screen-generateinventory`'s "a screen with no supporting requirement should be reconsidered, not silently generated."

**Non-software boundaries get full use-case treatment.** Do not skip, abbreviate, or treat a non-software boundary's use cases as lesser just because no UI will ever exist there — the `three-level-valid` fixture's root (non-software) boundary has its own legitimate `ServiceRequest`-handling activity; a validator or downstream consumer must never find this skill produced thinner output for non-software boundaries.

### Step 3 — Write the detailed script per use case

For every use case, write its linked script per the structure above. The Main Flow's steps should reference actual process activities and domain entities already defined at this boundary (per their own IDs in `process.md`/`domain-model.md`) wherever a step corresponds to one — do not invent new process/domain content here; this skill consumes those models, it does not extend them. If a step has no corresponding existing process activity, write it directly in prose instead of forcing a fabricated reference.

**UI References section**: only ever include this section if (a) `boundary_type` is `software`, and (b) a concrete Screen/UIModelEntry mapping actually exists for that step (e.g., because `ui-generatemodel`/`screen-generateinventory` already ran). This skill never fabricates a UI reference to a screen that doesn't exist, and never includes an empty/placeholder UI References section for a step that doesn't have one — per the contract's "Omit entirely if none apply" discipline already established for Alternative/Exception Paths.

### Step 4 — Assign IDs and write output

Assign `UC-[###]` per the scoped-per-boundary algorithm (contract Section 3.3), then write `use-case-model.md`/`.json` and each script file, plus `use-case-scripts/main.md` as a meaningful index (not a stub) listing every script with its use case name and a one-line summary.

### Step 5 — Revision discipline

On a re-run against an existing `use-case-model.json` (e.g., after the boundary's domain/process model changed), **preserve existing `use_case_id` and `actor_id` values and existing script content** for use cases that still apply — do not renumber or regenerate from scratch. For a use case whose backing requirement or process activity reference no longer resolves (e.g., the requirement was removed, or the process activity it referenced was deleted), **do not silently delete the use case or silently guess a replacement reference** — flag it explicitly in the model's changelog entry and leave the unresolved reference visible (e.g., `requirement_refs: ["R-204 [UNRESOLVED — see changelog]"]`) so a human/self-attesting developer notices and resolves it deliberately, mirroring `screen-discussfeedback`'s `[REVIEW NEEDED]` convention for genuinely ambiguous content.

## Quality Checks

1. **Boundary readiness enforced**: this skill never runs against a boundary with an undeclared `boundary_type` — verified by Step 0, not assumed.
2. **No actor reuse across boundaries**: every actor is locally defined to this boundary's `use-case-model.json`; a shared name with a parent/child boundary's actor is not treated as the same `actor_id`.
3. **Script completeness**: every `use_case_id` listed in `use-case-model.json` has a corresponding script file at its `script_ref` path, and that script has at minimum Trigger, Preconditions, Main Flow, and Postconditions sections (Alternative/Exception Paths and UI References are conditionally omitted, never required).
4. **No invented UI content**: a non-software or software-but-not-yet-screened use case's script has no UI References section — confirmed by absence, not an empty section.
5. **Revision preserves identity**: re-running against an existing model does not change any `use_case_id`/`actor_id` for use cases that still apply, and unresolved references are flagged, not silently dropped or guessed.

## Integration

**Upstream**: `hierarchy-management` (boundary folder/`main.md` existence, `boundary_type` declaration), `domain-extractconcepts`/`domain-alignentities` (domain model), `documentation-automation`/process-modeling skills (process model), `diagram-generatecollaboration` (collaboration model, actor/boundary evidence), `requirements-ingest`

**Downstream**: `ui-generatemodel` (consumes a software boundary's use-case model as one input), `model-validatealignment` (validates this skill's output for cross-model alignment at end of round — this skill does not self-certify), `screen-generateinventory` indirectly (via `ui-generatemodel`'s output)

**Typical pipeline** (per T01 contract's Workflow Integration):
```
Requirements + domain concepts
  -> collaboration/hierarchy and boundary identification (incl. boundary_type declaration)
  -> scoped domain/process documents
  -> usecase-generatemodel   ← this skill
  -> ui-generatemodel (software boundary with UI requirements only)
  -> model-validatealignment (end-of-round)
  -> screen inventory -> layout -> mockup -> verified flow -> handoff/feedback
```

## Example Prompt

```
Use the usecase-generatemodel skill to generate a use-case model for this boundary.

Boundary: [boundary_id, boundary_type, hierarchy_path]
Domain model: [paste domain-model.md or reference its path]
Process model: [paste process.md or reference its path]
Requirements: [paste requirements.json, scoped to this boundary, or reference its path]

Produce a use-case model and one detailed script per use case, with actors and
use cases defined relative to this boundary alone.
```
