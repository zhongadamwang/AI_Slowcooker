---
name: ui-generatemodel
description: Generate or revise a software-boundary UI Model (UIModel/UIModelEntry/Aggregation) from a boundary's domain, process, and use-case models, closing the existing manual-generation gap while preserving stable UME identities and the existing screen-pipeline contract. Produces UI Model content only for explicitly software-typed boundaries with actual UI requirements; records non-applicability explicitly elsewhere. Use when a software boundary's use-case model exists and a UI Model needs to be produced or refreshed from it.
license: MIT
metadata:
  version: 0.1.0
  last-updated: "2026-11-08"
---

# UI Generate Model

Generate a software-boundary's UI Model (the existing `UIModel`/`UIModelEntry`/`Aggregation` structure, D-02) automatically from its domain, process, and use-case models — closing the manual-authoring gap the orchestrator previously documented ("S33 uses S06 as an explicitly insufficient proxy prerequisite").

## Intent

Per PRJ-07's confirmed decisions (R-002, R-005, R-008, R-011): the UI model is a modeling artifact within the design workflow, not merely a prototype output, and it must stay aligned with the domain, process, and use-case models at the same boundary. This skill is the actual producer that closes the gap `ui-prototyping-conventions.md` left as "may be authored manually" — it does not introduce a new UI schema.

**This skill does not change what a UIModel/UIModelEntry/Aggregation *is***. Every field already defined in [`OrgDocument/orgModel/02 - UI Prototype Skill Development Process/domain-model.md`](../../../OrgDocument/orgModel/02%20-%20UI%20Prototype%20Skill%20Development%20Process/domain-model.md) (D-02) is produced exactly as-is. This skill only adds **how** that structure gets produced (automatically, from aligned inputs) and **two new optional fields** carrying boundary/use-case provenance (Section 2) — additive, never a breaking schema change, per T01 contract Section 6.

## Shared Contract

**Read in full before implementing against this skill**: [`../model-validatealignment/references/cross-model-alignment-contract.md`](../model-validatealignment/references/cross-model-alignment-contract.md) — Section 2 (boundary typing, UI applicability rule R-011), Section 6 (compatibility notes for this exact skill).

This skill produces content; it does **not** self-certify alignment. `model-validatealignment` validates this skill's output for cross-model consistency at end of round (contract Section 4) — this skill's own job is to never *knowingly* produce non-compliant output in the first place (contract Section 6: "ui-generatemodel is expected to only ever produce compliant entries in the first place, not rely on the validator to catch its own mistakes after the fact").

## Inputs

- **Primary**: the target boundary's `main.md`, specifically its `## System Boundary` section's declared `boundary_type`. **Required** before this skill may run — see Workflow Step 0.
- **Primary**: that boundary's `use-case-model.json` (from `usecase-generatemodel`, T02) — the main driver of what UI concepts might be needed. Development/testing of this skill may use T01's contract fixtures directly, ahead of a real T02 run, per this task's explicit note that T02 is a runtime input dependency, not an implementation-blocking prerequisite.
- **Secondary**: that boundary's `domain-model.md` and `process.md` — supply the actual entities a `UIModelEntry` aggregates and any process-activity context informing aggregation groupings.
- **Secondary**: the boundary's existing `ui-model.json`, if one already exists (for revision — see Step 4).

> **Pre-condition**: Exactly like `usecase-generatemodel`'s own Step 0, this skill must stop and surface a clarification question if the target boundary's `boundary_type` is `unknown` or undeclared — **never** infer software status from the mere presence of a use-case model, a UI-sounding use case name, or any other indirect signal. Domain-concepts completion is explicitly **not** UI readiness (per this task's own Detailed Requirements) — a fully-modeled domain and process layer at a boundary says nothing about whether that boundary is software-typed.

## Outputs

**Files Generated** (per D-02's existing storage convention, `orgModel/[NN] - [Process Name]/ui-model.md`/`.json` — this skill writes to the *boundary's own* process folder, which for a decomposed hierarchy is that boundary's specific sub-folder, not always the hierarchy root):
- `ui-model.md` — human-readable model (primary, exact existing D-02 Markdown shape)
- `ui-model.json` — structured model (primary for downstream consumption by `screen-generateinventory`)

**Non-applicability is recorded, not silently absent.** If a boundary is `non-software`, or is `software` but its use-case model yields zero screens worth generating, this skill still writes a minimal `ui-model.json` with `entries: []` and a `generation_note` field (Section 2) explaining why — never simply omits the file, which would be indistinguishable from "not yet run" to a downstream consumer or validator.

### JSON Structure (`ui-model.json`) — Existing D-02 Shape, Unchanged, Plus Two Additive Fields

```json
{
  "model_id": "string",
  "model_type": "base",
  "derives_from": null,
  "role_scope": null,
  "source_domain_model": "string (relative path)",
  "generation_note": "string | null — NEW, additive (see below)",
  "generated_at": "ISO-8601",
  "changelog": [{ "version": "string", "date": "string", "change": "string" }],
  "entries": [
    {
      "entry_id": "UME-001",
      "ui_concept_name": "string",
      "domain_entity_refs": ["string, ..."],
      "aggregation_description": "string",
      "boundary_ref": "string — NEW, additive (see below)",
      "source_use_case_refs": ["UC-xxx, ... — NEW, additive (see below)"]
    }
  ],
  "aggregations": [
    { "aggregation_id": "string", "member_entities": ["string, ..."], "resulting_ui_concept": "string" }
  ]
}
```

**New, additive fields** (never required by existing consumers, never removed from any entry the existing schema already had):
- `generation_note` (model-level, optional): present **only** when `entries` is empty or the model required an explainable decision — e.g., `"Boundary BND-BATCH-RECON is software-typed but its use-case model (UCM-BATCH-RECON) has no human-facing interactions; zero screens generated, consistent with R-011's 'software boundaries do not automatically require a screen.'"` Omit entirely when not needed (a populated, unremarkable model does not need a note).
- `boundary_ref` (per entry, required when this skill produced the entry): the `boundary_id` (contract Section 1.2) this entry's domain entities were aggregated from. This is what lets `model-validatealignment` check "does every `UIModelEntry`'s `domain_entity_refs` resolve to Scoped Entity References whose `scope` matches a software-typed boundary" (contract Section 6) without re-deriving it from scratch.
- `source_use_case_refs` (per entry, optional): the `use_case_id`(s) (e.g., `UC-001`) whose steps motivated this entry's existence. Optional because a manually-authored legacy `ui-model.json` (predating this skill, or predating `usecase-generatemodel` even existing) correctly has no such provenance — this field's absence is not an error.

A consumer (`screen-generateinventory`, any other existing tool) that only reads `entry_id`/`ui_concept_name`/`domain_entity_refs`/`aggregation_description` continues to work completely unchanged; these are additive annotations, never a replacement for or restructuring of the existing fields.

### Markdown Structure (`ui-model.md`)

Identical to D-02's existing shape (model_id, model_type, entries each with entry_id/ui_concept_name/domain_entity_refs/aggregation_description, changelog) — see T03 of PRJ-06's worked examples (`OrgDocument/projects/06 - Building UI Prototype skills/artifacts/UI Prototype/examples/*/`) for the established style this skill must match. The only addition is an optional inline boundary/use-case citation, following the same `*(Ref: ...)*` convention already used throughout the framework:

```markdown
### Order Summary *(UME-001)*
**Aggregates**: Order, Customer, LineItem
*(Boundary: BND-CHILD-SW; Ref: UC-001, UC-002)*
```

## Workflow

### Step 0 — Verify the boundary is ready (identical discipline to `usecase-generatemodel`'s Step 0)

1. The target boundary's `main.md` must have an explicit `## System Boundary` section with a declared `boundary_type`. If `unknown` or absent: **stop**, surface the contract's clarification question (Section 2.1), do not generate anything, do not default either direction.
2. If `boundary_type` is `non-software`: **stop** generation of a populated model. Per Section 4.2, still write a minimal `ui-model.json` with `entries: []` and a `generation_note` explaining the boundary is non-software (never produce a UI model with actual entries for a non-software boundary — this is R-011's hardest line, and this skill's single most important refusal).
3. If `boundary_type` is `software`: proceed to Step 1. (Note: reaching Step 1 does **not** guarantee any entries get produced — see Step 3.)

### Step 1 — Read the boundary's use-case model

Load `use-case-model.json` for this boundary. If it does not exist: **stop** and report a missing-applicable-model condition (contract Section 4.3's `INVALID_INPUT` semantics) — do **not** proceed to generate a UI model from the domain model alone, since without use cases this skill has no actor-goal evidence for what screens are actually needed (generating screens straight from domain entities, bypassing use-case evidence, is exactly the "UIModel is a modeling artifact, not merely a prototype output" anti-pattern R-002 exists to prevent).

### Step 2 — Identify UI-worthy use cases

Not every use case in a software boundary's model needs a screen. Per this task's Detailed Requirements and R-011's explicit note ("software boundaries do not automatically require a screen"), examine each use case's actor:
- **Human actors** interacting directly with this boundary (not a system-to-system or scheduled-trigger actor) are the primary signal that a use case is UI-worthy.
- **Internal-role/external-system actors** (e.g., the worked example's "Nightly Scheduler") are evidence the use case does **not** need a screen — their interactions are not rendered as UI.

A boundary may legitimately have zero UI-worthy use cases despite being software-typed (the `software-boundary-no-ui-required` fixture, reused from T01). This is not an error or incompleteness; record it via `generation_note` per the Outputs section, and stop with `entries: []`.

### Step 3 — Aggregate domain entities into UIModelEntries

For each UI-worthy use case (or a coherent group of related use cases sharing an actor/goal), identify which domain entities its steps actually touch (per the use case's script Main Flow, which already references domain entities by their existing IDs — this skill does not invent new entity references, it reads the ones the script already cites). Group these into one `UIModelEntry` per coherent UI concept, exactly as `screen-generateinventory`'s own existing Step 1 guidance describes screens aggregating from UI Model entries — this skill performs the analogous aggregation one level up, from domain entities into UI Model entries, using use-case evidence as the organizing signal instead of ad hoc judgment.

Preserve the existing single-base-model rule (D-02 Business Rule 2): exactly one `base` UIModel per boundary. (Derived/role-scoped UIModels remain a Phase 3 concern, unchanged by this skill, per D-02's own existing scope boundary.)

### Step 4 — Revision discipline: preserve stable `UME` identities

On a re-run against an existing `ui-model.json` for this boundary (e.g., because the use-case model or domain model changed), **preserve every existing `entry_id` for a `UIModelEntry` that still corresponds to the same UI concept** — do not renumber. This directly implements D-02's existing Business Rule 3 ("Regenerate, Don't Flag": when inputs change, dependent entries are regenerated with changelog entries, not merely flagged stale) and this task's own "stable-ID revision" validation requirement. A `UIModelEntry` whose backing use case or domain entity reference no longer resolves is flagged in the changelog with its reference left visibly marked unresolved (same `[UNRESOLVED — see changelog]` convention as `usecase-generatemodel`'s own Step 5) — never silently deleted or silently re-pointed at a guessed replacement.

### Step 5 — Write output, verify against the hard-constraints checklist

Write `ui-model.md`/`.json`. Before considering the task complete, verify:
- [ ] Every entry's `boundary_ref` names an explicitly `software`-typed boundary (never `non-software` or `unknown`)
- [ ] Every entry's `domain_entity_refs` actually appear in that boundary's `domain-model.md` (this skill resolves references against real content, same discipline as T01's manifest-source-disagreement fixture — it does not trust a use-case script's entity citation without checking)
- [ ] Changelog present (D-02 Business Rule / existing R-610 requirement, unchanged)
- [ ] No existing `screen-generateinventory`/`screen-*` consumer-facing field was removed or restructured

## Quality Checks

1. **Boundary readiness enforced**: this skill never produces a populated model for a `non-software` or `unknown`-typed boundary — verified by Step 0, not assumed.
2. **Use-case-evidenced aggregation**: every `UIModelEntry` traces to at least one use case via `source_use_case_refs` (when this skill itself produced the entry — a pre-existing manually-authored entry predating this skill's adoption is exempt, per the field's documented optionality).
3. **No forced UI generation**: a software boundary with zero UI-worthy use cases produces `entries: []` plus a `generation_note`, never a fabricated screen just to have *something* to show.
4. **Stable identity across revisions**: re-running against an existing model does not change any `entry_id` for an entry that still applies; unresolved references are flagged, not silently dropped or guessed.
5. **Existing screen pipeline compatibility**: `screen-generateinventory` (S33) can consume this skill's output with zero changes to its own logic — confirmed by the worked example (Section below) actually being readable by the existing field names it depends on (`entry_id`, `ui_concept_name`, `domain_entity_refs`).

## Fixtures and Worked Example

See [`examples/three-level-worked-example/`](examples/three-level-worked-example/) — reuses the exact same fixture boundaries as T01's `model-validatealignment` fixtures and T02's `usecase-generatemodel` worked example (`BND-ROOT` non-software, `BND-CHILD-SW` software, `BND-GRANDCHILD` software), for consistency across all of PRJ-07's deliverables:
- `BND-ROOT` (non-software): `ui-model.json` with `entries: []` and a `generation_note` citing non-software status — demonstrates Step 0.2's refusal.
- `BND-CHILD-SW` (software, human actors present): `ui-model.json` with 2 real `UIModelEntry` items, aggregated from the use cases T02 already produced for this same boundary — demonstrates Steps 1–3 end-to-end, consuming T02's actual output rather than a hypothetical one.
- `BND-GRANDCHILD` (software, but its one use case's only actor is a direct human performing a narrow logging action): included as a worked illustration of a borderline case, with explicit reasoning in its `generation_note` for why it *does* warrant one small UIModelEntry rather than being treated as non-UI-worthy like the `software-boundary-no-ui-required` fixture's Nightly Scheduler case — the distinguishing factor (direct human actor vs. internal-role/system actor) is called out explicitly, not left for a reader to infer.

## Migration Notes for Existing Model Consumers

- **`screen-generateinventory` (S33)**: no change required. Its existing pre-condition check ("a UI Model must already exist for the project... nothing to generate a screen inventory from until the UI Model is in place") is satisfied identically whether the `ui-model.json` it reads was authored manually or produced by this skill. The two new additive fields (`boundary_ref`, `source_use_case_refs` on entries; `generation_note` on the model) are not read by S33 and do not need to be.
- **Any manually-authored legacy `ui-model.json`** (e.g., PRJ-06's T03 toy-order-domain worked example, predating this skill): remains valid as-is. This skill's additive fields are optional; a legacy file's absence of `boundary_ref`/`source_use_case_refs`/`generation_note` is not a validation failure for that file — these fields only become expected going forward, for models this skill itself produces or revises.
- **`model-validatealignment`**: uses the new `boundary_ref` field (when present) as a direct signal for its own R-011 check (contract Section 2.2), rather than needing to re-derive which boundary a `UIModelEntry`'s entities came from by cross-referencing `domain_entity_refs` against every boundary's `domain-model.md` manually. When `boundary_ref` is absent (a legacy entry), the validator falls back to that manual cross-reference — this skill's new field is an optimization/clarity aid for validation, not a new requirement the validator depends on exclusively.

## Integration

**Upstream**: `usecase-generatemodel` (use-case model — primary driver), `domain-extractconcepts`/`domain-alignentities` (domain model), `documentation-automation` (process model, contextual), `hierarchy-management` (boundary `main.md`/`boundary_type`)

**Downstream**: `screen-generateinventory` (S33, consumes `ui-model.json` exactly as before), `model-validatealignment` (validates this skill's output for cross-model alignment at end of round)

**Typical pipeline** (per T01 contract's Workflow Integration):
```
Requirements + domain concepts
  -> collaboration/hierarchy and boundary identification (incl. boundary_type declaration)
  -> scoped domain/process documents
  -> usecase-generatemodel
  -> ui-generatemodel (software boundary with UI requirements only)   ← this skill
  -> model-validatealignment (end-of-round)
  -> screen inventory -> layout -> mockup -> verified flow -> handoff/feedback
```

## Example Prompt

```
Use the ui-generatemodel skill to generate the UI model for this software boundary.

Boundary: [boundary_id, boundary_type, hierarchy_path]
Use-case model: [paste use-case-model.json or reference its path]
Domain model: [paste domain-model.md or reference its path]

Produce a ui-model.md/.json using the existing UIModel/UIModelEntry/Aggregation
structure, with every entry's domain_entity_refs resolved against the real
domain model and every entry traced back to the use case(s) that motivated it.
If this boundary has no UI-worthy use cases, produce an empty-entries model
with a generation_note explaining why, not a fabricated screen.
```
