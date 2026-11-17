---
name: edps-skill-navigator
description: Recommend which EDPS skill or sequence of skills fits a request, and what to run next on a project, by matching the request against the skill catalogue and checking which artifacts the project already has - then run the chosen skill if the user agrees. Use when the user asks which skill to use, what to do next, how to get from what they have to what they want (for example "turn these notes into a schedule"), or describes a goal in general terms without naming a skill. For running and tracking a whole multi-skill workflow with saved state, use edps-workflow-orchestrator.
license: MIT
metadata:
  version: 3.0.0
  last-updated: "2026-11-17"
---

# EDPS Skill Navigator

Answer "which skill, in what order, starting from here?" for a single request. The answer comes from two sources only: the skill catalogue and the project's actual files.

- **The catalogue**: the Skill Catalogue in [`edps-workflow-orchestrator/SKILL.md`](../edps-workflow-orchestrator/SKILL.md) gives every skill's ID, category, and prerequisites. It is the single source for the order skills run in; do not keep a separate dependency list here.
- **What each skill does and when to use it**: each skill's own `description`, listed in [`../README.md`](../README.md).
- **Where the project stands**: the files that exist under `OrgDocument/projects/[NN] - [Project Name]/` and the relevant `OrgDocument/orgModel/` folders.

## Workflow

### 1. Identify the goal

Restate what the user wants as an outcome ("a schedule", "use cases for the dispatch boundary", "validated alignment"). If the request could mean two different outcomes, ask one short question with the options instead of guessing; for example "clean up requirements" could mean `requirements-sanitize` (remove technical noise) or `requirements-merge` (reconcile several sources).

### 2. Find the target skill

Pick the skill whose description matches the outcome. If several skills each produce part of it, the target is the last one in the chain.

### 3. Work back to what exists

Walk the target's prerequisites in the catalogue. For each, check whether its output already exists in the project (for example `artifacts/Analysis/requirements.json` for `requirements-ingest`). Stop at the first prerequisites whose outputs are present. The path is the skills between there and the target, in catalogue order.

Note conditions the catalogue states: `usecase-generatemodel` needs a declared `boundary_type`; `ui-generatemodel` and the `screen-*` skills apply only to software boundaries; `requirements-sanitize` applies only to mixed-perspective sources.

### 4. Recommend

Give:

- the target skill and why it fits;
- the path of skills to run, each with the file it will read and the file it will write;
- which steps can be skipped because their output already exists, and which existing outputs look stale or incomplete (check them with `run_gate.py`, below);
- anything the user must decide or supply first (a source document, a boundary type, a stakeholder answer).

Keep it short: a few lines per step. Then offer to run the first step. Run nothing that writes files until the user agrees.

### 5. Hand over larger work

If the path is long (more than about four skills), the user wants to follow a whole archetype (`standard`, `rapid`, `compliance`), or the work will span sessions, recommend `edps-workflow-orchestrator`, which tracks progress in `project-state.json`.

## Checking existing outputs

To tell whether an existing output is complete enough to build on, run that skill's completion gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py <skill-name> \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

A failed or incomplete gate means the step should be re-run or fixed before the steps after it.

## Example

> "We have meeting notes about a new returns process. I need a delivery schedule."

- Target: `plan-buildschedule`.
- Project has no `artifacts/Analysis/` outputs yet, and the notes mix business and IT detail.
- Path: `requirements-sanitize` → `requirements-ingest` → `goals-extract` → (`process-scopemin`, if an MVP cut is wanted) → `plan-derivetasks` → `plan-estimateeffort` → `plan-buildschedule`.
- Seven steps: suggest `edps-workflow-orchestrator` with the `standard` archetype, or start with `requirements-sanitize` on the notes.

## Integration

**Reads**: the orchestrator's Skill Catalogue, each skill's description, the project's files

**Hands over to**: the recommended skill, or `edps-workflow-orchestrator` for multi-step workflows
