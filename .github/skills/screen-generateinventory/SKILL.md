---
name: screen-generateinventory
description: Generate a standalone screen inventory for UI prototyping from requirements and a UI Model, listing each distinct screen, its purpose, UI Model reference, and requirement traceability. First skill in the UI Prototyping pipeline (Project 06); produces the entry-point artifact all subsequent generation skills (screen-generatelayout, screen-generatemockup, screen-generateflow) depend on.
license: MIT
version: 1.0.0
last-updated: 2026-10-27
---

# Screen Generate Inventory

Generate a standalone, traceable inventory of UI screens from requirements and a UI Model — the entry-point artifact for the UI Prototyping skill set.

## Intent

Identify the distinct screens/views a project's UI needs, based on its requirements and UI Model entries, and record them as a standalone inventory artifact — never embedded inside a larger design document (per D-6, `requirements.md` v1.3). Each screen traces to the requirement(s) that justify it and to exactly one UI Model entry (never a domain entity directly), establishing the first link in the traceability chain `Requirement → Aggregation → UIModelEntry → Screen` that every downstream UI Prototyping skill relies on.

## Inputs

- **Primary**: `projects/[project-name]/orgModel/[NN] - [Process Name]/ui-model.json` (from the project's UI Model — see `domain-model.md` under `orgModel/02 - UI Prototype Skill Development Process/` for the schema, and T03's worked example for a validated instance)
- **Secondary**: `projects/[project-name]/artifacts/Analysis/requirements.json` (from `requirements-ingest`)
- **Format**: Structured UI Model entries (`entry_id`, `ui_concept_name`, `domain_entity_refs`) and structured requirements (`req_id`, `text`, `tags`)

> **Pre-condition**: A UI Model must already exist for the project. If it doesn't, this skill cannot proceed — a screen must trace to a UI Model entry (R-606/R-628), not directly to a domain entity, so there is nothing to generate a screen inventory from until the UI Model is in place.

## Outputs

**Files Generated:**
- `artifacts/UI Prototype/screen-inventory.md` — Human-readable screen inventory (primary)
- `artifacts/UI Prototype/screen-inventory.json` — Structured screen inventory for downstream skills (machine processing)

Both files are written to the `UI Prototype` artifact category introduced in T01 (`project-document-management` v2.3.0). This category must already exist in the project before this skill runs; if it doesn't, run `project-document-management`'s Iterative Update Workflow to add it first.

**This output is always standalone** — per D-6, it is never embedded as a section inside `screen-assembledocument`'s consolidated design document (T08). The design document *summarizes and references* this inventory; it does not replace it.

### JSON Structure (`screen-inventory.json`)

```json
{
  "inventory_id": "SCRINV-001",
  "project_id": "string",
  "generated_at": "ISO8601",
  "source_files": ["ui-model.json", "requirements.json"],
  "screens": [
    {
      "screen_id": "SCR-001",
      "name": "Order Summary",
      "purpose": "Let a customer or support agent review a single order's full detail",
      "ui_model_ref": "UME-001",
      "requirement_refs": ["R-614"],
      "import_origin": "generated"
    }
  ]
}
```

Field conventions (per `ui-prototyping-conventions.md`, T02):
- `screen_id`: `SCR-[###]`, zero-padded 3-digit, sequential — scan existing `screen-inventory.json` for the highest number in use, increment, verify uniqueness before writing (same algorithm as `change-management`'s `generate_change_id()`)
- `ui_model_ref`: **singular** string — a Screen traces to exactly one UI Model entry, never an array (contrast with `requirement_refs`)
- `requirement_refs`: array — a Screen may be justified by one or more requirements
- `import_origin`: `"generated"` for all screens produced by this skill. (`"imported"` is reserved for the Phase 2 `screen-importspec`/design-specification-import capability — not produced here.)

### Markdown Structure (`screen-inventory.md`)

```markdown
# Screen Inventory

**Project**: [project_id]
**Generated**: [timestamp]
**Source**: ui-model.json, requirements.json
**Total Screens**: [count]

## Screens

### Order Summary *(SCR-001)*
**Purpose**: Let a customer or support agent review a single order's full detail
**UI Model Entry**: UME-001
*(Ref: R-614)*

### [Additional Screens...]

---
**Traceability**: Every screen traces to exactly one UI Model entry and one or more requirements
**Generated**: [timestamp]
```

## Core Function

**Input**: UI Model (`ui-model.json`) + requirements (`requirements.json`)
**Primary Output**: Markdown screen inventory (human review, discussion)
**Secondary Output**: JSON screen inventory (consumed by `screen-generatelayout`, `screen-generatemockup`, `screen-generateflow`)
**Output Destination**: `artifacts/UI Prototype/screen-inventory.md` and `.json`

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing the project's ui-model.json and requirements.json.
Copilot will identify distinct screens needed and produce a traceable inventory.

Example prompt:
"Use screen-generateinventory to identify the screens needed for this UI Model and requirements set, with full traceability to UI Model entries and source requirements."
```

**Command Line (reference pattern, consistent with other EDPS skills):**
```bash
python screen_generateinventory.py PROJECT-001 ui-model.json requirements.json
# Saves to: artifacts/UI Prototype/
#   📄 screen-inventory.md (Markdown - primary)
#   📋 screen-inventory.json (JSON - machine processing)
```

## Screen Identification Process

### Step 1 — Walk the UI Model's entries

For each `UIModelEntry` in the base UI Model (and, if present, any derived UI Models — though derived-model screen generation is a Phase 3 concern per `scope-analysis.md`; MVP operates against the base model only), consider whether it corresponds to one distinct screen or whether multiple screens are needed to present it fully (e.g., a list-style entry like "Customer Order History" might justify both a list screen and a detail screen — but splitting a single entry into multiple screens should only happen when the requirements actually call for more than one view, not by default).

### Step 2 — Attach requirement traceability

For each candidate screen, identify which requirement(s) justify its existence (R-605). A screen with no supporting requirement is a signal to reconsider whether it's actually needed — per `collaboration-mode-reference.md`'s solo-mode build-and-clarify pattern, flag this rather than silently generating an unjustified screen.

### Step 3 — Assign IDs and write output

Assign `SCR-[###]` per the ID generation algorithm in `ui-prototyping-conventions.md` Section 1, then write both the Markdown and JSON outputs.

### Step 4 — Verify against the hard-constraints checklist

Before considering this skill's output complete, verify against `ui-prototyping-conventions.md` Section 3's checklist items relevant to this skill:
- [ ] Text-only output (Markdown + JSON only — no binary files)
- [ ] No direct domain-entity reference (`ui_model_ref` points to a `UME-[###]`, never a domain entity ID)

(The remaining checklist items — mockup portability, no design-tool dependency, no target-framework assumption, changelog presence — apply to later skills in the pipeline, not to this one, since this skill produces no HTML/CSS/JS and no single-document changelog target. `screen-inventory.md`/`.json` themselves are not required to carry an in-document changelog, unlike `LayoutSpec`/`DesignDocument`/`UIModel` — they are generated fresh each run from the current UI Model and requirements state, consistent with their role as a derived index rather than an authored document.)

## Quality Checks

1. **Traceability completeness**: every screen has a non-empty `ui_model_ref` and at least one `requirement_refs` entry
2. **ID uniqueness**: no duplicate `screen_id` values; new IDs correctly continue the existing sequence rather than colliding with previously-generated screens
3. **Standalone artifact rule**: confirm output is never embedded inside another document — screen inventory is always its own file
4. **No orphaned UI Model entries without rationale**: if a `UIModelEntry` exists but no screen was generated from it, this should be a deliberate, noted decision (e.g., it's purely a data-aggregation concept with no dedicated screen), not a silent omission

## Integration

**Upstream**: UI Model generation (T03's schema; a future `ui-model-generate` skill is not yet built — in the interim, the UI Model may be authored manually following the schema in `orgModel/02 - UI Prototype Skill Development Process/domain-model.md`), `requirements-ingest`

**Downstream**: `screen-generatelayout` (consumes each screen entry to produce its `LayoutSpec`), `screen-generatemockup` (consumes the layout spec), `screen-generateflow` (consumes the full screen set to model navigation), `screen-assembledocument` (summarizes the inventory into the consolidated design document — references it, does not replace it)

**Typical pipeline**:
```
[ui-model.json] + [requirements.json] → screen-generateinventory → screen-inventory.md / .json
                                                                  ↓
                                                        screen-generatelayout → ...
```

## Example Prompt

```
Use the screen-generateinventory skill to identify screens for this project.

UI Model: [paste ui-model.json or reference its path]
Requirements: [paste requirements.json or reference its path]

Project ID: ORDER-MGMT-001

Produce a traceable screen inventory — each screen must reference exactly one
UI Model entry and at least one source requirement.
```
