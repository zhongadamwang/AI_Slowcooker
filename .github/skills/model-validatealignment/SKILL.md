---
name: model-validatealignment
description: Validate that a boundary's domain, use-case, and UI models agree on the entities and system boundaries they reference, at the end of every modeling round. Runs a deterministic validator over the real boundary folders and reports PASS, NEEDS_CLARIFICATION, or INVALID_INPUT with item-level findings and clarification questions. Owns the shared cross-model alignment contract. Use after usecase-generatemodel or ui-generatemodel has run, after any model in a boundary was edited, when resuming a project to check whether an earlier PASS is stale, or when asked whether the models are aligned. Does not generate models itself.
license: MIT
metadata:
  version: 1.0.0
  last-updated: "2026-11-15"
---

# Model Validate Alignment

Checks that the models of one or more boundaries are consistent with each other, by running a validator script over the boundary folders. A modeling round is only aligned when that script reports `PASS`; reading the models and concluding they look consistent is not a validation.

This skill owns the shared contract the modeling skills implement against: [`references/cross-model-alignment-contract.md`](references/cross-model-alignment-contract.md). Read it when you need the reference shapes, the boundary-typing rule, or the round lifecycle in full.

## Inputs

- The boundary folders in the round's scope. A boundary folder holds `main.md` (with a `## System Boundary` section) and, alongside it, `domain-model.md`, `use-case-model.json` with its `use-case-scripts/`, and where applicable `ui-model.json`.
- A round ID that has not been used before in this project (for example `ROUND-003`).
- The project's `artifacts/Analysis/` folder, where reports are written.

## Workflow

Run every command from the repository root.

### 1. Validate the round

```bash
python3 .github/skills/model-validatealignment/scripts/validate_alignment.py \
    --round-id ROUND-003 \
    --root "OrgDocument/orgModel/[NN] - [Process Name]" \
    --output-dir "OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis"
```

`--root` validates every boundary at or below that folder. To validate specific boundaries only, pass `--scope <boundary folder>` once per boundary instead.

The script writes, in the output folder:
- `alignment-report-[round-id].md` and `.json` — the round report. Reports are never overwritten; the script refuses to reuse a round ID for a different result.
- `alignment-status.json` — the latest round's status and the model versions it validated. The S39 completion gate reads this file.

### 2. Act on the status

| Status | Exit code | Meaning | What to do |
|---|---|---|---|
| `PASS` | 0 | Every check held | The round is aligned. Report it and continue |
| `NEEDS_CLARIFICATION` | 1 | Something is genuinely undecided: an undeclared `boundary_type`, or a reference a generator marked `[UNRESOLVED` | Put the report's clarification questions to the user (in solo mode, answer them explicitly in the stated role). Record the answer in the owning document, then validate again under a new round ID |
| `INVALID_INPUT` | 2 | A model is missing, unreadable, or contradicts another | Fix or regenerate the model each finding names, using the owning skill, then validate again under a new round ID |

Never report a round as aligned on any status other than `PASS`, and never resolve a finding by editing the report. A round cannot move from `NEEDS_CLARIFICATION` to `PASS` without a new validator run against the updated files. This holds in every collaboration mode and workflow archetype: solo self-attestation and the `rapid` archetype do not apply to alignment.

### 3. Check an earlier PASS before relying on it

A `PASS` describes the files as they were when the round ran. Before treating an earlier round as still valid (on resume, or before starting the screen pipeline), run:

```bash
python3 .github/skills/model-validatealignment/scripts/validate_alignment.py \
    --check-stale "OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/alignment-report-ROUND-003.json"
```

Exit code 0 means the report still holds. Exit code 3 means it is stale: either it was not `PASS`, or a model in its scope changed since. A stale round needs a fresh validation under a new round ID.

## What the validator checks

For each boundary in scope:

| Check | Result when it fails |
|---|---|
| `main.md` declares `boundary_type` as `software` or `non-software` (an absent or `unknown` type is never defaulted) | `NEEDS_CLARIFICATION` |
| `domain-model.md` and `use-case-model.json` exist and can be read | `INVALID_INPUT` |
| The use-case model's own `boundary_ref` agrees with `main.md` | `INVALID_INPUT` |
| Each use case's primary actor is defined in that model, its `boundary_ref` is this boundary, and its script file exists | `INVALID_INPUT` |
| Every entity ID a script or use case cites (`E-###`) is defined in this boundary's `domain-model.md` | `INVALID_INPUT` |
| No script in a non-software boundary has a `## UI References` section | `INVALID_INPUT` |
| A non-software boundary's UI model has no entries | `INVALID_INPUT` |
| Each UI model entry's `boundary_ref` is this boundary, its `domain_entity_refs` resolve in this boundary's domain model (by ID or name), and its `source_use_case_refs` resolve in this boundary's use-case model | `INVALID_INPUT` |
| No reference carries an `[UNRESOLVED` marker | `NEEDS_CLARIFICATION` |

Entity identity is `(boundary, entity_id)`. Two boundaries may both define `E-002`; that is not a conflict, and a reference is always resolved against the domain model of the boundary it appears in.

A software boundary with an empty UI model, or with no `ui-model.json` yet, is not a finding: software boundaries do not automatically need screens, and whether `ui-generatemodel` has run is its own gate's concern.

### What it does not check

- **The process model.** `process.md` is versioned for staleness, but its content is not parsed; scripts' references to process activities are not resolved.
- **Hierarchy structure, file and link integrity** (HV/HX/HN rules): owned by `hierarchy-validation`.
- **Diagram boundary rules** (VR-1 to VR-4): owned by `diagram-generatecollaboration`. A participant's `boundary` stereotype and this skill's `boundary_type` are independent.
- **Screens.** Whether each screen traces to a UI model entry is checked by the `screen-*` skills' gates.

State these limits when reporting a `PASS`, if the user asks what was verified.

## Outputs

- `artifacts/Analysis/alignment-report-[round-id].md` / `.json` — schema in contract Section 4.2
- `artifacts/Analysis/alignment-status.json` — latest round pointer
- A short summary to the user: status, boundaries covered, each finding, and each clarification question

## Tests and fixtures

`fixtures/` holds five boundary trees as real files, each with a `scenario.md` and an `expected-report.json`: `three-level-valid`, `unknown-boundary-type`, `missing-applicable-model`, `manifest-source-disagreement`, `software-boundary-no-ui-required`.

```bash
cd .github/skills/model-validatealignment/scripts
python3 -m unittest test_alignment_contract test_alignment_report test_alignment_loader
python3 run_fixtures.py     # validates each fixture from disk and compares with its expected report
```

Run both after changing any script here.

## Integration

**Upstream**: `hierarchy-management` (boundary folders and the `## System Boundary` section), `domain-extractconcepts` / `domain-alignentities` (domain model), `usecase-generatemodel`, `ui-generatemodel`

**Downstream**: `edps-workflow-orchestrator` (records each round in `modeling_rounds` and checks staleness on resume), `screen-generateinventory` and the rest of the screen pipeline (should start from a UI model whose round is `PASS` and not stale)
