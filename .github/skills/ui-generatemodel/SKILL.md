---
name: ui-generatemodel
description: Generate or revise the UI Model (UIModel, UIModelEntry, Aggregation) of a software-typed boundary from its use-case and domain models, deciding which use cases need screens and which domain entities each screen concept aggregates, written as ui-model.md and ui-model.json beside the boundary's other models. Keeps existing UME IDs stable on revision and records an explained empty model where no UI applies. Use after usecase-generatemodel for a boundary declared software, when the user asks for a UI model or which screens a boundary needs, or when a boundary's use-case or domain model changed; and before screen-generateinventory, which reads ui-model.json.
license: MIT
metadata:
  version: 0.2.0
  last-updated: "2026-11-17"
---

# UI Generate Model

Produce a boundary's UI Model from evidence: its use cases say which actors need to see or enter something, and its domain model says which entities that involves. The UI Model is a modeling artifact that must stay aligned with the domain and use-case models, not a sketch of screens.

The structure (`UIModel`, `UIModelEntry`, `Aggregation`) is defined in [`OrgDocument/orgModel/02 - UI Prototype Skill Development Process/domain-model.md`](../../../OrgDocument/orgModel/02%20-%20UI%20Prototype%20Skill%20Development%20Process/domain-model.md). This skill fills that structure; it adds three optional fields and changes nothing else.

The shared rules for boundaries and references are in [`../model-validatealignment/references/cross-model-alignment-contract.md`](../model-validatealignment/references/cross-model-alignment-contract.md) (Section 2 for boundary typing and where UI may exist, Section 6 for this skill). `model-validatealignment` checks the result at the end of the modeling round, but produce only compliant entries; do not rely on the validator to catch them.

## Inputs

- **Required**: the boundary's `main.md`, for the `boundary_type` in its `## System Boundary` section
- **Required**: the boundary's `use-case-model.json` and its `use-case-scripts/` (from `usecase-generatemodel`)
- **Required**: the boundary's `domain-model.md`; `process.md` for context on grouping
- **On revision**: the boundary's existing `ui-model.json`

## Outputs

Written into the boundary's own folder (for a decomposed hierarchy, its sub-folder, not the hierarchy root):

- `ui-model.json` — read by `screen-generateinventory`
- `ui-model.md` — the same model for people

Always write both files, even when the model has no entries: an absent file is indistinguishable from "not run yet".

### `ui-model.json`

```json
{
  "model_id": "UIM-CHILD-SW",
  "model_type": "base",
  "derives_from": null,
  "role_scope": null,
  "source_domain_model": "domain-model.md",
  "generation_note": "string — only when entries is empty or a decision needs explaining",
  "generated_at": "ISO-8601",
  "changelog": [{ "version": "1.0", "date": "2026-11-08", "change": "Initial generation from use-case-model.json (UCM-CHILD-SW)" }],
  "entries": [
    {
      "entry_id": "UME-001",
      "ui_concept_name": "Dispatch Queue",
      "domain_entity_refs": ["E-002", "E-003"],
      "aggregation_description": "What the entry brings together and which use case it supports",
      "boundary_ref": "BND-CHILD-SW",
      "source_use_case_refs": ["UC-001"]
    }
  ],
  "aggregations": [
    { "aggregation_id": "AGG-001", "member_entities": ["E-002", "E-003"], "resulting_ui_concept": "UME-001" }
  ]
}
```

The three fields this skill adds, which no existing consumer reads:

| Field | Where | Rule |
|---|---|---|
| `generation_note` | model | Present when `entries` is empty or a decision needs explaining (why no screens, why a borderline use case got one). Omit otherwise |
| `boundary_ref` | each entry | The `boundary_id` of this boundary. Required on every entry this skill writes |
| `source_use_case_refs` | each entry | The use case IDs that motivated the entry. Write it on every entry you generate; it may be absent on a hand-written legacy entry |

### `ui-model.md`

Same content in the established Markdown style (see the worked example), with each entry's boundary and use cases cited inline:

```markdown
### Dispatch Queue *(UME-001)*
**Aggregates**: ServiceRequest (E-002), Technician (E-003)
*(Boundary: BND-CHILD-SW; Ref: UC-001)*
```

It must have a `## Changelog` section.

## Workflow

### 0. Check the boundary type

Read `boundary_type` from `main.md`'s `## System Boundary` section.

- **Absent or `unknown`**: stop. Ask the user whether the boundary is software (a system with its own interface) or non-software (an organization, place, or manual process), and record the answer in `main.md`. Never infer it from the folder name, a participant stereotype, the existence of a use-case model, or a UI-sounding use case name.
- **`non-software`**: UI may not exist here. The orchestrator does not schedule this skill for such boundaries; if invoked anyway, write a model with `entries: []` and a `generation_note` saying the boundary is non-software, and stop. Never write entries for a non-software boundary.
- **`software`**: continue. Reaching step 1 does not mean any screens will be generated.

### 1. Load the use-case model

If `use-case-model.json` does not exist, stop and say so: run `usecase-generatemodel` first. Do not derive screens from the domain model alone; without use cases there is no evidence of what any actor needs to see.

### 2. Decide which use cases need UI

A software boundary does not automatically need screens. For each use case, look at its primary actor's `interaction` field:

- **`direct`**: a person performs the steps themselves, whatever their `actor_kind` (a customer, or an `internal-role` such as a coordinator or technician). This use case is UI-worthy.
- **`automated`**: no person is present (another system, a scheduled trigger). It does not need a screen.

Decide on `interaction`, never on `actor_kind` alone: an `internal-role` actor is usually a person using the system. If an actor has no `interaction` value (a model written before the field existed), read the script to see whether a person performs the steps, and record your conclusion in the changelog.

If no use case is UI-worthy, write `entries: []` with a `generation_note` explaining why. That is a correct, complete result, not a failure.

### 3. Aggregate entities into entries

For each UI-worthy use case, or a group of use cases that share an actor and goal, take the domain entities its script's Main Flow cites and group them into one `UIModelEntry` per coherent UI concept. Record each grouping as an `Aggregation`.

- Use only entity IDs the scripts already cite, and confirm each one is defined in this boundary's `domain-model.md`. Do not add entities the use cases never touch, and never cite an entity from another boundary.
- Keep exactly one `base` UIModel per boundary. Derived and role-scoped models are out of scope.

### 4. Preserve identity on revision

When `ui-model.json` already exists:

- Keep every existing `entry_id` attached to the same UI concept. Never renumber; give new entries the next unused number.
- Regenerate an entry whose inputs changed, and say what changed in the changelog.
- If an entry's use case or entity no longer exists, do not delete it silently or re-point it at a guess. Leave the reference visibly marked, for example `"E-007 [UNRESOLVED — see changelog]"`, and explain in the changelog. `model-validatealignment` reports these markers as needing clarification.

### 5. Write and check

Write both files, then check:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py ui-generatemodel \
    --project "OrgDocument/projects/[NN] - [Project Name]" --boundary <boundary folder>
```

Then, at the end of the modeling round, run `model-validatealignment`.

## Quality checks

- No entries in a non-software or undeclared boundary.
- Every entry carries `boundary_ref` and `source_use_case_refs`, and every `domain_entity_refs` value is defined in this boundary's domain model.
- An empty model always has a `generation_note`; no screen was invented just to have something.
- Existing `entry_id`s are unchanged for entries that still apply.
- The D-02 fields (`entry_id`, `ui_concept_name`, `domain_entity_refs`, `aggregation_description`) are all present, so `screen-generateinventory` reads the model unchanged.

## Worked example

[`examples/three-level-worked-example/`](examples/three-level-worked-example/) uses the same three boundaries as `usecase-generatemodel`'s example and `model-validatealignment`'s `three-level-valid` fixture:

- `BND-ROOT` (non-software): empty model with a `generation_note`, showing step 0.
- `BND-CHILD-SW` (software): two entries built from that boundary's use cases.
- `BND-GRANDCHILD` (software): one small entry for a technician logging time directly, with a `generation_note` explaining why this borderline case gets a screen.

## Compatibility

- **`screen-generateinventory`** reads `entry_id`, `ui_concept_name`, and `domain_entity_refs`, and works unchanged whether the model was written by hand or by this skill.
- **Hand-written legacy models** (such as Project 06's toy order domain example) remain valid without the three added fields.

## Integration

**Upstream**: `usecase-generatemodel` (use cases and actor interaction), `domain-extractconcepts` / `domain-alignentities` (domain model), `hierarchy-management` (boundary folder and `boundary_type`)

**Downstream**: `screen-generateinventory`, `model-validatealignment`
