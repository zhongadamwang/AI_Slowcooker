---
name: edps-workflow-orchestrator
description: Run an EDPS workflow end to end across sessions - choose the standard, rapid, or compliance archetype, resolve which skills are available or blocked from the skill catalogue's prerequisites, run each skill's completion gate before marking it complete, track modeling rounds and their alignment status, and keep progress in project-state.json so work resumes where it stopped. Holds the Skill Catalogue (skill IDs S00-S41 and prerequisites). Use when the user wants to start, continue, or resume a full EDPS project workflow, asks for progress or the next step across a project, wants a skill skipped or marked complete, or needs the prerequisite order of skills.
license: MIT
metadata:
  version: 2.0.0
  last-updated: "2026-11-17"
---

# EDPS Workflow Orchestrator

The central coordination hub for end-to-end EDPS methodology execution. Sits above `edps-skill-navigator` to provide workflow lifecycle management, prerequisite enforcement, and persistent project state across every EDPS skill in the catalogue below (skill IDs S00–S41).

## Intent

Run a multi-skill EDPS workflow to completion across sessions:
1. Select the **workflow archetype** for the project goal
2. Resolve which skills are **available**, **blocked**, or done from the prerequisite graph (the Skill Catalogue below)
3. Keep a **project state file** (`project-state.json`) so work can resume in a later session
4. Run each skill's **completion gate** with `scripts/run_gate.py` before marking it complete
5. Report **progress** with completed / available / blocked status

For a one-off "which skill should I use?" question, `edps-skill-navigator` answers from the same catalogue without keeping state.

## Inputs

- **Workflow command**: One of `start`, `status`, `next`, `resume`, `reset`, or `skip` (see [Quick Commands](#quick-commands))
- **Archetype** *(for `start` only)*: `standard` | `rapid` | `compliance` (default: `standard`)
- **Project state** *(for `resume` only)*: Serialized JSON string from a prior session's `project-state.json`
- **Project context** *(optional)*: Current project folder path for auto-detection of completed artifacts
- **Skip justification** *(for `skip` only)*: Required free-text justification logged to project state
- **project-metadata.json** *(implicit, read automatically)*: The orchestrator reads `collaboration_mode` from the current project's `project-metadata.json` before every gate evaluation (see [Skill Completion Gates](#skill-completion-gates)). Absence of the field is treated as `traditional`, never inferred as `solo` (see T01/T02).

## Outputs

- **project-state.json** in the project root: skill states, skip audit, confirmations, modeling rounds, and a history of what happened (updated after every step)
- **Workflow plan**: ordered skill sequence for the archetype
- **Progress dashboard**: see [Progress Visualization](#progress-visualization)
- **Next step**: the next available skill(s), with the prompt to run each

---

## Skill Catalogue

Every EDPS skill is registered below with its skill ID, category, and prerequisite skill IDs. This catalogue is the source of truth for skill IDs (each skill's `gate.json` `skill_id` must match it) and for DAG construction. `S`-numbers always mean skill IDs; skill categories are referred to by name only.

| ID | Skill Name | Category | Prerequisite Skill IDs |
|----|-----------|----------|-----------------------|
| S00 | `requirements-sanitize` | Requirements | *(none — optional pre-step before S01)* |
| S01 | `requirements-ingest` | Requirements | *(none; use S00 output when source is mixed-perspective)* |
| S02 | `requirements-merge` | Requirements | S01 |
| S03 | `goals-extract` | Requirements | S01 |
| S04 | `process-w5h` | Requirements | S01 |
| S05 | `process-scopemin` | Planning | S03 |
| S06 | `domain-extractconcepts` | Domain | S01 |
| S07 | `domain-alignentities` | Domain | S06 |
| S08 | `domain-proposenewconcepts` | Domain | S07 |
| S09 | `diagram-generatecollaboration` | Visualization | S06 |
| S10 | `hierarchy-management` | Hierarchy | S09 |
| S11 | `documentation-automation` | Documentation | S10 |
| S12 | `hierarchy-validation` | Compliance | S10 |
| S13 | `edps-compliance` | Compliance | S12 |
| S14 | `migration-tools` | Hierarchy | S09 |
| S15 | `plan-derivetasks` | Planning | S03, S05 |
| S16 | `plan-estimateeffort` | Planning | S15 |
| S17 | `plan-buildschedule` | Planning | S15, S16 |
| S18 | `project-document-management` | Documentation | *(none)* |
| S19 | `project-planning-tracking` | Planning | S17 |
| S20 | `project-status-reporting` | Planning | S19 |
| S21 | `change-management` | Change | S01 |
| S22 | `change-impact-analysis` | Change | S21, S10 |
| S23 | `process-merge` | Integration | S04, S09 |
| S24 | `process-findtopandupdate` | Integration | S23 |
| S25 | `model-integration` | Integration | S24 |
| S26 | `orgmodel-update` | Integration | S11, S25 |
| S27 | `integration-testing` | Validation | S26 |
| S28 | `github-issue-create-update` | GitHub | S15 |
| S29 | `github-issue-sync-status` | GitHub | S28 |
| S30 | `edps-skill-navigator` | Meta | *(none — invokes others)* |
| S31 | `edps-workflow-orchestrator` | Meta | *(none — this skill; not a DAG node)* |
| S32 | `usecase-generatemodel` | Design & Visualization | S09, S10 *(boundary_type declared)* |
| S33 | `screen-generateinventory` | Design & Visualization | S40 *(UI Model)*, S01 |
| S34 | `screen-generatelayout` | Design & Visualization | S33 |
| S35 | `screen-generatemockup` | Design & Visualization | S34 |
| S36 | `screen-generateflow` | Design & Visualization | S33, S35 |
| S37 | `screen-assembledocument` | Design & Visualization | S34, S35, S36 |
| S38 | `screen-discussfeedback` | Design & Visualization | S35 |
| S39 | `model-validatealignment` | Design & Visualization | S32 *(round-scoped; validates whichever of S32/S40 are in round scope)* |
| S40 | `ui-generatemodel` | Design & Visualization | S32 *(software boundary only)* |
| S41 | `skill-creator` | Meta | *(none — create-only; not a DAG node)* |

> **Note**: `skill-creator` (S41, meta, create-only) and `migration-tools` (deprecated, use `hierarchy-management --op migrate`) are catalogued but excluded from archetype workflows by default. Include them explicitly with the `--include-deprecated` flag. `requirements-sanitize` (S00) is an optional pre-step; it is included automatically when the orchestrator detects that the source document is not already a clean business requirements document.
>
> **Category labels are names, not numbers.** `.github/skills/README.md` previously numbered its categories S1–S10 (and briefly "S11 — UI Prototyping"), which collided with skill IDs. Those labels are retired: where older project documents say "S5", read **Design & Visualization**; S33–S38 belong to that category alongside S32/S39/S40. No skill ID was renumbered by that change.
>
> **UI Prototyping skills (S32–S40) and Design & Visualization membership (PRJ-07, T06)**: `usecase-generatemodel` (S32) and `model-validatealignment` (S39) apply to *every* boundary identified during S09/S10, software or not — they are unconditionally part of the Design & Visualization phase, exactly like `diagram-generatecollaboration`/`hierarchy-management`. `ui-generatemodel` (S40) and the six `screen-*` skills (S33–S38) only ever produce output for a boundary whose `main.md` `## System Boundary` section declares `boundary_type: software` (see `hierarchy-management`'s stub template, T05) — a project with no software boundary completes S32/S39 against its non-software boundaries and simply never reaches S40/S33–S38, rather than being forced through an irrelevant UI phase. **The former S06-only UI-Model-readiness proxy is removed**: `screen-generateinventory` (S33) now has a real, auto-verifiable prerequisite on **S40** (`ui-generatemodel`), closing the gap this catalogue previously documented as "UI Model generation has no dedicated orchestrated skill of its own." See the [Modeling Rounds](#modeling-rounds-s32s39s40-lifecycle) section below for round/report lifecycle and non-bypassable alignment semantics.

---

## Workflow Archetypes

Three canonical archetypes cover the most common EDPS project goals. Each is a named DAG subset of the full catalogue.

### Archetype 1: `standard` — Full EDPS Lifecycle
**Use when**: Starting a new project end-to-end, or continuing an interrupted full-lifecycle project.  
**Duration estimate**: 3–5 days for a well-scoped project.

**Ordered phases and skills**:

```
Phase 0 — Project Initialization
  [S18] project-document-management        (parallel start point)

Phase 1 — Requirements Analysis
  [S00] requirements-sanitize              (optional; recommended when source is a conversation, IT spec, or operational doc)
  [S01] requirements-ingest                (requires: S18 OR project folder exists; input from S00 if executed)
  [S02] requirements-merge                 (optional; requires: S01 + multiple sources)
  [S03] goals-extract                      (requires: S01)
  [S04] process-w5h                        (requires: S01)
  [S05] process-scopemin                   (requires: S03)

Phase 2 — Domain Modeling
  [S06] domain-extractconcepts             (requires: S01)
  [S07] domain-alignentities               (requires: S06)
  [S08] domain-proposenewconcepts          (requires: S07)   [optional]

Phase 3 — Visualization & Hierarchy
  [S09] diagram-generatecollaboration      (requires: S06)
  [S10] hierarchy-management               (requires: S09)
  [S11] documentation-automation           (requires: S10)

Phase 4 — Compliance Validation
  [S12] hierarchy-validation               (requires: S10)
  [S13] edps-compliance                    (requires: S12)

Phase 5 — Planning
  [S15] plan-derivetasks                   (requires: S03, S05)
  [S16] plan-estimateeffort                (requires: S15)
  [S17] plan-buildschedule                 (requires: S15, S16)
  [S19] project-planning-tracking          (requires: S17)

Phase 6 — Integration
  [S23] process-merge                      (requires: S04, S09)
  [S24] process-findtopandupdate           (requires: S23)
  [S25] model-integration                  (requires: S24)
  [S26] orgmodel-update                    (requires: S11, S25)

Phase 7 — Final Validation
  [S27] integration-testing               (requires: S26)
  [S20] project-status-reporting          (requires: S19)
```

**Parallel execution opportunities** (skills safe to run simultaneously within a phase):
- Phase 1: S03 ∥ S04 ∥ S06 (all only require S01)
- Phase 3: S11 can begin as soon as first boundary folder from S10 is created
- Phase 5: S15 → S16 ∥ S17 (S16 and S17 can run as soon as S15 is done; S17 also needs S16)
- Phase 6: S23 and S15 are independent and can run in parallel

---

### Archetype 2: `rapid` — Quick Analysis Sprint
**Use when**: Existing project with requirements already ingested; need domain + diagram + plan in the shortest path.  
**Duration estimate**: 4–8 hours for a focused sprint.

```
[S03] goals-extract                        (requires: S01 already done)
[S05] process-scopemin                     (requires: S03)
[S06] domain-extractconcepts               (requires: S01 already done)
[S09] diagram-generatecollaboration        (requires: S06)
[S15] plan-derivetasks                     (requires: S03, S05)
[S16] plan-estimateeffort                  (requires: S15)
[S12] hierarchy-validation                 (requires: S09 via S10 implied)
[S13] edps-compliance                      (requires: S12)
```

**Parallel execution**: S06 ∥ S03 (after S01 verified complete); S15 ∥ S09 (after S03/S05 and S06 respectively).

**Prerequisites**: S01 (`requirements-ingest`) must already be complete in project state. If not, orchestrator inserts S01 before the sprint.

---

### Archetype 3: `compliance` — Compliance & Validation Focus
**Use when**: Existing Project 1–3 artifacts need compliance verification and hierarchy enforcement.  
**Duration estimate**: 2–4 hours.

```
[S10] hierarchy-management (--op validate)  (requires: S09 already done)
[S12] hierarchy-validation                  (requires: S10)
[S13] edps-compliance                       (requires: S12)
[S22] change-impact-analysis                (requires: S21 or skip if no changes)
[S11] documentation-automation              (requires: S10)
[S26] orgmodel-update                       (requires: S11)
[S27] integration-testing                   (requires: S26)
[S20] project-status-reporting              (requires: S19 or standalone)
```

**Prerequisites**: S09 (`diagram-generatecollaboration`) output must exist. If `hierarchy-metadata.json` is absent, S10 must run in full decomposition mode first.

---

### Design & Visualization Phase — Including Modeling Rounds (PRJ-07, T06)

**Use when**: A project's requirements call for domain/process modeling, use-case modeling, and (for software boundaries) UI prototyping — screen inventories, layout specs, clickable mockups, interaction flows, and a consolidated design document for stakeholder discussion.

**Duration estimate**: 2–3 days for a small-to-medium boundary/screen set, consistent with Project 06's `scope-analysis.md` MVP estimate.

```
Design & Visualization — Unconditional (every boundary, software or not)
  [S09] diagram-generatecollaboration        (requires: S06)
  [S10] hierarchy-management                  (requires: S09; declares boundary_type per boundary)
  [S11] documentation-automation               (requires: S10)
  [S32] usecase-generatemodel                  (requires: S09, S10 with boundary_type declared — not 'unknown')
  [S39] model-validatealignment                (requires: S32; end-of-round, see Modeling Rounds below)

Design & Visualization — Conditional on boundary_type: software (per boundary)
  [S40] ui-generatemodel                       (requires: S32, boundary_type == software)
  [S33] screen-generateinventory               (requires: S40, S01)
  [S34] screen-generatelayout                  (requires: S33)
  [S35] screen-generatemockup                  (requires: S34)
  [S36] screen-generateflow                    (requires: S33, S35)
  [S37] screen-assembledocument                (requires: S34, S35, S36)
  [S38] screen-discussfeedback                 (requires: S35)
```

**Parallel execution opportunities**: S36 and S37 both only require S34/S35 (plus S33 for S36) and can run in either order or in parallel once their shared prerequisites are satisfied; S38 can begin as soon as S35 produces at least one screen's mockup, independent of whether S36/S37 have run yet. S32/S39 can run per-boundary in parallel across independent, non-overlapping boundaries.

**S32/S39 are unconditional Design & Visualization members; S40/S33–S38 remain conditional on boundary_type.** Every EDPS project that reaches this phase runs `usecase-generatemodel` and `model-validatealignment` against every identified boundary — these are not an optional extension, unlike the removed "UI Prototyping Extension" framing. What remains genuinely conditional is **UI execution**: `ui-generatemodel` (S40) and the six `screen-*` skills only ever engage for a boundary whose `main.md` declares `boundary_type: software`. A project with zero software boundaries completes S32/S39 for all its boundaries and simply never reaches S40/S33–S38 — this is the correct, documented outcome (R-011), not an incomplete workflow.

**The former S06-only UI-Model-readiness proxy is removed.** `screen-generateinventory` (S33) now has a real, orchestrator-verifiable prerequisite on **S40** (`ui-generatemodel`'s completion), not merely "S06 has run" as a necessary-but-insufficient stand-in. The orchestrator can now mark S33 `available` only once S40 has actually produced a non-empty `ui-model.json` for at least one software boundary — closing the gap this catalogue previously had to document as a manual pre-condition workaround.

#### Modeling Rounds (S32/S39/S40 lifecycle)

A **modeling round** (full definition: [cross-model-alignment-contract.md](../model-validatealignment/references/cross-model-alignment-contract.md) Section 4) is a bounded creation/revision of the domain/process/use-case/UI models for one or more boundaries, concluding in an **Alignment Report** (`PASS` / `NEEDS_CLARIFICATION` / `INVALID_INPUT`). This is layered on top of the existing linear DAG above — it is **not** a cyclic DAG node; refinement is represented as a **new round**, not a new graph edge back to an earlier skill.

**Project state additions** (see [Project State Schema](#project-state-schema) below for the full `modeling_rounds` field): each round records its `round_id`, `boundary_scope`, `source_model_versions` (as they stood when the round ran), and its `status`. `S39`'s own `completed` state in the `skills` map means "at least one round has reached a terminal status" — it does **not** by itself mean every round is `PASS`; the orchestrator must inspect `modeling_rounds` for the actual per-boundary status, exactly as `model-validatealignment`'s own `resolve_round_for_resume()` does (see its `scripts/alignment_report.py`).

**Running a round's validation.** Run `python3 .github/skills/model-validatealignment/scripts/validate_alignment.py --round-id <id> --root <process or boundary folder> --output-dir "<project>/artifacts/Analysis"` from the repository root. It writes the round report and `alignment-status.json` (the latest round's status and model versions), which is what the S39 completion gate reads. Copy that file's `status` and `source_model_versions` into `modeling_rounds` for each boundary in scope.

**Non-bypassable alignment, across every mode and archetype.** A round's `PASS` status can only be set by `model-validatealignment`'s own validator actually running against current artifacts (contract Section 4.4). This is explicitly **not** subject to:
- `collaboration_mode` (`solo` vs. `traditional`) — unlike `stakeholder_confirmation` gate checks, whose severity depends on collaboration mode (see Skill Completion Gates below), alignment-round status has no severity-resolution step at all. There is no code path, solo or traditional, that converts a `NEEDS_CLARIFICATION`/`INVALID_INPUT` round into `PASS` without an actual revalidation.
- Workflow archetype (`standard`/`rapid`/`compliance`) — `rapid`'s generally more lenient gate severities (see each skill's `gate.json` `workflow_archetypes` field) do not apply to round status; `model-validatealignment`'s own `gate.json` keeps `workflow_archetypes.rapid: "hard"` specifically so a rapid-archetype project cannot soften this check the way other skills' soft checks are allowed to relax.
- `orchestrate skip` — skipping `S39` is logged to `skip_audit` exactly like skipping any other skill, but a skipped `S39` means the round was never validated, not that it passed. The orchestrator must never report a boundary as "aligned" on the strength of a skipped validation.

**Revision invalidates prior rounds.** If `orchestrate resume` finds that any model document within a prior round's `boundary_scope` has a newer version than that round's recorded `source_model_versions`, the prior round's `PASS` (if it was `PASS`) is **stale** — the orchestrator must not report that boundary as currently aligned; it must surface "revalidation required" and treat `S39` as `available` again for that boundary, not `completed`. This mirrors `resolve_round_for_resume()`'s `'stale'` return value exactly.

---

## DAG Prerequisite Engine

### How it works

The orchestrator maintains a directed acyclic graph where each node is a skill and each directed edge `A → B` means "A must complete before B can start".

**At every step, for each skill node, compute its state:**

| State | Condition |
|-------|-----------|
| `available` | All prerequisite skills are in `completed` state |
| `blocked` | One or more prerequisites are not yet `completed` |
| `completed` | Skill has been executed and its completion gate allowed progression |
| `skipped` | Explicitly bypassed with recorded justification |
| `optional` | Marked optional in archetype; not on critical path |

**Resolution algorithm**:
```
function get_available_skills(project_state, archetype_dag):
  available = []
  for skill in archetype_dag.skills:
    if skill.state in [completed, skipped]:
      continue
    if all(prereq.state in [completed, skipped] for prereq in skill.prerequisites):
      available.append(skill)
  return sort_by_critical_path_impact(available)
```

**Critical path priority**: Skills on the longest dependency chain to the final node are surfaced first.

### Blocked skill reporting

When a user attempts to invoke a blocked skill, the orchestrator returns:

```json
{
  "event": "skill_blocked",
  "skill": "hierarchy-validation",
  "skill_id": "S12",
  "reason": "Prerequisites not satisfied",
  "blocking_prerequisites": [
    {
      "skill": "hierarchy-management",
      "skill_id": "S10",
      "state": "not_started",
      "resolution": "Run hierarchy-management to decompose control-type participants before running hierarchy-validation."
    }
  ],
  "suggested_action": "Invoke hierarchy-management first, then return to hierarchy-validation."
}
```

---

## Project State Schema

The project state object is the single source of truth for where a project stands in its workflow. It is serialized to `project-state.json` in the project root after every skill execution.

```json
{
  "$schema": "https://edps.dev/schemas/project-state/v1.0.0",
  "project_id": "PRJ-NN",
  "project_name": "string",
  "archetype": "standard | rapid | compliance",
  "workflow_version": "1.0.0",
  "created": "ISO-8601",
  "last_updated": "ISO-8601",
  "session_id": "string — identifies the working session that last updated the state",
  "overall_progress": {
    "total_skills": 0,
    "completed": 0,
    "skipped": 0,
    "available": 0,
    "blocked": 0,
    "percent_complete": 0
  },
  "skills": {
    "S01": {
      "skill_name": "requirements-ingest",
      "state": "not_started | available | in_progress | completed | skipped",
      "started_at": "ISO-8601 or null",
      "completed_at": "ISO-8601 or null",
      "output_artifacts": ["artifacts/Analysis/requirements.md"],
      "gate_result": null,
      "skip_justification": null
    }
  },
  "skip_audit": [
    {
      "skill_id": "S08",
      "skill_name": "domain-proposenewconcepts",
      "skipped_at": "ISO-8601",
      "justification": "string — required",
      "session_id": "uuid"
    }
  ],
  "history": [
    {
      "timestamp": "ISO-8601",
      "event": "skill_completed | skill_skipped | skill_failed | gate_failed | round_validated | workflow_started | workflow_complete",
      "skill_id": "S01",
      "gate_status": "passed | passed_with_warnings | failed | incomplete | bypassed | null",
      "outputs": ["artifacts/Analysis/requirements.md"],
      "note": "string"
    }
  ],
  "confirmations": [
    {
      "role": "Primary Stakeholder",
      "confirmation_statement": "string — from the gate check",
      "confirmed_by": "self-attestation | <real stakeholder name>",
      "collaboration_mode": "solo | traditional",
      "timestamp": "ISO-8601"
    }
  ],
  "workflow_metadata": {
    "parallel_groups_executed": [],
    "critical_path_remaining": ["S09", "S10", "S12", "S13"],
    "estimated_remaining_hours": 0
  },
  "modeling_rounds": {
    "_comment": "PRJ-07, T06. Keyed by boundary_id; one entry per boundary that has had at least one S32/S39 round. Absence of a boundary_id here means no round has ever run for it -- distinct from a round existing with a non-PASS status.",
    "BND-[###]": {
      "latest_round_id": "string",
      "status": "PASS | NEEDS_CLARIFICATION | INVALID_INPUT | stale",
      "source_model_versions": {
        "domain_model": "string",
        "process_model": "string",
        "use_case_model": "string",
        "ui_model": "string | null"
      },
      "report_refs": ["artifacts/Analysis/alignment-report-[round-id].md"],
      "last_validated_at": "ISO-8601"
    }
  }
}
```

**`modeling_rounds` and `resume` staleness checking**: on `orchestrate resume`, for every boundary present in `modeling_rounds`, the orchestrator re-reads that boundary's actual current `domain-model.md`/`process.md`/`use-case-model.json`/`ui-model.json` and compares against the recorded `source_model_versions` by running `python3 .github/skills/model-validatealignment/scripts/validate_alignment.py --check-stale <round report .json>` (exit code 0 = still valid, 3 = stale). If stale, the orchestrator sets that boundary's `status` to `"stale"` in the resumption summary (not silently left as the old `"PASS"`) and marks `S39` `available` again for that boundary, regardless of whether `S39`'s overall `skills` map entry still shows `completed` from an earlier, now-superseded round.

### Serialization and Resumption

**Saving state**: After every skill execution (or skip), write updated `project-state.json` to the project root.

**Resuming across sessions**: When the user invokes `orchestrate resume`, the orchestrator:
1. Reads `project-state.json` from the project root
2. Validates the schema version; if mismatched, runs migration
3. Rebuilds the DAG from the current `skills` states
4. Surfaces the `available` skills as the next steps
5. Generates a resumption summary: "Session resumed. 5/12 skills complete. Next available: hierarchy-management, goals-extract (parallel)."

---

## History Log

Record what happens in the `history` array of `project-state.json`, one entry per event, so the state file is also the project's audit trail:

```json
{ "timestamp": "2026-03-16T10:30:00Z", "event": "skill_completed", "skill_id": "S01",
  "gate_status": "passed_with_warnings", "outputs": ["artifacts/Analysis/requirements.md"], "note": "" }
```

Events: `workflow_started`, `skill_completed`, `skill_skipped`, `skill_failed`, `gate_failed`, `round_validated`, `workflow_complete`.

---

## Progress Visualization

### Compact dashboard (shown after every `orchestrate status` or `orchestrate next`)

```
╔══════════════════════════════════════════════════════════════╗
║  EDPS Workflow Orchestrator — PRJ-04 (standard archetype)   ║
╠══════════════════════════════════════════════════════════════╣
║  Overall:  ████████████░░░░░░░░  8/20 skills  40%          ║
╠══════════════════════════╦═══════════════════════════════════╣
║  Phase 0 — Init          ║  ✅ 1/1                          ║
║  Phase 1 — Requirements  ║  ✅ 4/5  (S02 skipped ⊘)        ║
║  Phase 2 — Domain        ║  🔄 1/3  (S06 ✅  S07 ▶  S08 ⬜) ║
║  Phase 3 — Hierarchy     ║  ⬜ 0/3                          ║
║  Phase 4 — Compliance    ║  ⬜ 0/2                          ║
║  Phase 5 — Planning      ║  ⬜ 0/4                          ║
║  Phase 6 — Integration   ║  ⬜ 0/4                          ║
║  Phase 7 — Validation    ║  ⬜ 0/2                          ║
╠══════════════════════════╩═══════════════════════════════════╣
║  ▶ AVAILABLE NOW (2):                                       ║
║    1. domain-alignentities    [S07]  ~30 min  ← NEXT       ║
║    2. plan-derivetasks        [S15]  ~45 min  (parallel ✓) ║
╠══════════════════════════════════════════════════════════════╣
║  🔒 BLOCKED (waiting on S07):  diagram-generatecollaboration║
╚══════════════════════════════════════════════════════════════╝
```

**Legend**: ✅ completed | 🔄 in progress | ▶ available | ⬜ blocked | ⊘ skipped

### Full dependency tree (shown with `orchestrate status --verbose`)

```
requirements-ingest [S01] ✅
├── goals-extract [S03] ✅
│   └── process-scopemin [S05] ✅
│       └── plan-derivetasks [S15] ▶  ← available
│           ├── plan-estimateeffort [S16] ⬜
│           └── plan-buildschedule [S17] ⬜
├── process-w5h [S04] ✅
├── domain-extractconcepts [S06] ✅
│   └── domain-alignentities [S07] ▶  ← available
│       ├── domain-proposenewconcepts [S08] ⬜ (optional)
│       └── diagram-generatecollaboration [S09] ⬜
│           └── hierarchy-management [S10] ⬜
│               ├── documentation-automation [S11] ⬜
│               │   └── orgmodel-update [S26] ⬜
│               └── hierarchy-validation [S12] ⬜
│                   └── edps-compliance [S13] ⬜
└── requirements-merge [S02] ⊘ (skipped — single source)
```

---

## Skill Completion Gates

The orchestrator integrates with skill completion gates to validate output quality before marking skills as completed and advancing the workflow. This ensures EDPS methodology standards are met at each step.

### Gate evaluation process

When `orchestrate complete [skill]` is invoked, run the skill's gate with the gate runner and act on its result. Do not judge a gate by reading `gate.json` and the artifacts yourself; the runner's result is the gate result.

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py <skill-name> \
    --project "OrgDocument/projects/[NN] - [Project Name]" \
    [--process <orgModel process folder>] [--boundary <boundary folder>] \
    [--archetype standard|rapid|compliance] [--json]
```

Pass `--process` for skills that write into an orgModel process folder (S09, S10, S11) and `--boundary` for skills that work on one boundary (S32, S40); run those gates once per folder. The collaboration mode is read from `project-metadata.json`.

| Runner status | Exit code | What the orchestrator does |
|---|---|---|
| `passed` | 0 | Mark the skill `completed` |
| `passed_with_warnings` | 0 | Show the failed checks and their remediation, then mark `completed` unless the user chooses to remediate first |
| `bypassed` | 0 | Mark `completed`; record that the archetype bypasses this gate |
| `failed` | 1 | Do not mark `completed`; show each failed hard check's remediation |
| `incomplete` | 2 | Re-run with the scope folder the skipped checks name |
| `no_gate` | 0 | Mark `completed` |

How severity resolves (full detail in [references/gate-schema.md](references/gate-schema.md)):

- A check is `hard` or `soft` as declared. The only exception is `stakeholder_confirmation`, which is hard in `traditional` mode and soft (self-attested) in `solo` mode. No other check type is affected by collaboration mode.
- Each gate states, per archetype, whether its hard failures block (`hard`), only warn (`soft`), or whether the gate is skipped (`bypass`). `model-validatealignment` (S39) is `hard` in every archetype, and none of its checks is a stakeholder confirmation, so neither archetype nor collaboration mode can soften it.
- In the `compliance` archetype a quality score below 0.80 also blocks.

When a `stakeholder_confirmation` check passes by solo self-attestation, append the confirmation record (shape in the gate schema reference) to `project-state.json`.

The gate check types, path scopes, `applies_when` conditions, and the quality score are defined in [references/gate-schema.md](references/gate-schema.md). After editing any `gate.json`, run `run_gate.py --lint`.

### Gate evaluation output

`run_gate.py --json` prints the result the orchestrator records with the `skill_completed` event:

```json
{
  "skill": "requirements-ingest",
  "skill_id": "S01",
  "archetype": "standard",
  "collaboration_mode": "solo",
  "archetype_level": "hard",
  "status": "passed_with_warnings",
  "allowed": true,
  "quality_score": 0.75,
  "quality_below_threshold": true,
  "checks": [
    { "id": "artifacts_exist", "type": "artifact_existence", "severity": "hard", "status": "passed", "detail": "all artifacts exist" },
    { "id": "requirement_count", "type": "threshold", "severity": "soft", "status": "failed", "detail": "...", "remediation": "..." }
  ]
}
```

---

## Quick Commands

Commands are requests to this skill in the conversation (for example "orchestrate status").

### `orchestrate start [archetype]`
**Purpose**: Begin a new workflow for the current project.  
**Flow**:
1. If `project-state.json` already exists → warn user, offer to reset or resume
2. Ask for/confirm archetype (`standard`, `rapid`, or `compliance`)
3. Auto-detect completed artifacts in the current project folder to pre-populate skill states
4. Write initial `project-state.json`
5. Display compact dashboard with available first steps
6. Emit `workflow_started` event

### `orchestrate status`
**Purpose**: Display the current workflow progress dashboard.  
**Flags**: `--verbose` shows full dependency tree

### `orchestrate next`
**Purpose**: Show the next recommended skill(s) with ready-to-use prompts.  
**Output**: Lists all currently `available` skills, sorted by critical-path impact. For the top skill, provides a complete copy-paste prompt.

### `orchestrate resume`
**Purpose**: Restore a previous session from `project-state.json`.  
**Flow**:
1. Read and validate `project-state.json`
2. Rebuild DAG state
3. Display resumption summary + compact dashboard

### `orchestrate complete [skill-id-or-name]`
**Purpose**: Mark a skill as completed after running gate validation checks.  
**Flow**:
1. Validate the skill was `available` (not blocked by prerequisites)
2. **Run gate evaluation** with `scripts/run_gate.py` (see [Gate evaluation process](#gate-evaluation-process))
3. **Gate decision logic**:
   - If gate fails with hard errors → block completion, display remediation steps
   - If gate passes → continue to step 4
   - If gate has soft failures → warn user, offer to continue or remediate
4. Update skill state to `completed` in `project-state.json`
5. Emit `skill_completed` event with gate results
6. Recompute available skills based on updated DAG
7. Display updated dashboard + next available skills

**Gate integration example**:
```bash
> orchestrate complete requirements-ingest

⏳ Evaluating skill completion gates...

✅ Gate evaluation passed (quality score: 92%)
   • Artifact exists: artifacts/Analysis/requirements.md ✅
   • Content structure: Basic sections present ✅  
   • Traceability links: Missing REQ-IDs ⚠️ (soft failure)

❗ Remediation available: Add requirement IDs for full traceability

Continue with completion? (Y/n) y

🎯 requirements-ingest marked complete
📊 Dashboard: 1/12 skills complete (8% progress)
🔄 Next available: goals-extract, process-w5h (can run in parallel)
```

### `orchestrate skip [skill-id-or-name] --justification "..."`
**Purpose**: Skip an optional or non-critical skill with a recorded justification.  
**Rules**:
- Hard-gated skills (on critical path) cannot be skipped without `--force`
- Justification text is mandatory; empty string → error
- Skip is recorded in `skip_audit` in project state

### `orchestrate reset`
**Purpose**: Clear project state and restart the workflow.  
**Confirmation required**: "Are you sure? This will clear all workflow progress. (y/N)"

### `orchestrate add-skill [skill-name] --after [skill-id]`
**Purpose**: Insert an ad-hoc skill execution into the current workflow at a specified position.  
**Use case**: Adding `change-management` mid-workflow after a requirements change.

---

## Integration with edps-skill-navigator

Both skills read the same Skill Catalogue. The navigator answers single requests ("which skill turns notes into a schedule?") and hands a long or multi-session path to this skill; this skill runs and tracks the whole workflow.

---

## Error Handling and Recovery

| Scenario | Orchestrator Behaviour |
|----------|------------------------|
| Skill execution fails mid-workflow | Mark skill `failed`; surface error; keep preceding skills `completed`; offer retry or skip |
| `project-state.json` is corrupt or missing | Offer to auto-detect state from existing project artifacts (scan for outputs); or restart |
| Schema version mismatch on resume | Run forward migration; log migration steps to `project-state.json` |
| Circular dependency detected in custom workflow | Report cycle, refuse to execute, suggest resolution |
| Session timeout mid-skill | Mark skill as `interrupted`; prompt user to re-invoke or manually complete |

---

## Best Practices

1. **Always start with `orchestrate start`** — even if you plan to do only one skill. The state object enables resumption and compliance reporting.
2. **Use `orchestrate next`** instead of guessing — it accounts for the current state and surfaces critical-path skills first.
3. **Never skip hard-gated skills without a justification** — gate bypasses without justification violate EDPS compliance requirements.
4. **Commit `project-state.json`** to version control — it acts as a project audit trail alongside the artifacts.
5. **For parallel skills**, run them in either order; the state tracks each independently.
6. **Use `compliance` archetype for existing projects** — it runs only the validation and compliance slice of the workflow, avoiding re-execution of analysis already done.

---

**Version History**:
- **2.0.0** (2026-11-17): Removed descriptions of components that do not exist (a separate `skill-completion-gates` consumer of emitted events, an NLP engine, latency targets); events are a history log in `project-state.json`; gate evaluation is by `scripts/run_gate.py`.
- **1.4.0** (2026-11-15): Gate evaluation is now executable — `scripts/run_gate.py` evaluates any skill's `gate.json` against real files and `--lint` validates the gate definitions; the JavaScript pseudo-code that previously stood in for it is removed and the gate schema is documented in `references/gate-schema.md`. Round validation and staleness checks now name `model-validatealignment`'s `validate_alignment.py`.
- **1.3.1** (2026-11-15): Review fixes — removed the code fence that wrapped this file (its frontmatter did not parse); moved `version`/`last-updated` under `metadata`; added catalogue rows for `edps-workflow-orchestrator` (S31) and `skill-creator` (S41) and aligned every `gate.json` `skill_id` with this catalogue; retired the numbered category labels (S1–S10) in favour of category names; removed hard-coded skill counts.
- **1.3.0** (2026-11-08): PRJ-07/T06 — Removed the standalone "S11 — UI Prototyping" category; S33–S38 are now catalogued as members of **S5 — Design & Visualization**, no skill IDs renumbered. Registered `usecase-generatemodel` (S32, filling the one existing catalogue gap), `model-validatealignment` (S39), and `ui-generatemodel` (S40). Replaced the former S06-only UI-Model-readiness proxy with a real prerequisite: S33 now requires S40's completion. Added the `modeling_rounds` project-state field and round/revision staleness-checking on `orchestrate resume`. Documented that alignment-round (S39) completion is non-bypassable across `collaboration_mode` and workflow archetype — its gate checks are never `stakeholder_confirmation` type, so `resolveCheckSeverity()` cannot soften them.
- **1.2.0** (2026-10-27): Registered UI Prototyping extension skills S33–S38 (`screen-generateinventory`, `screen-generatelayout`, `screen-generatemockup`, `screen-generateflow`, `screen-assembledocument`, `screen-discussfeedback`) per Project 06 T10. Added as an optional extension, not folded into the three named archetypes, since not every project has a UI component. Documented the UI Model dependency gap (no dedicated orchestrated skill yet for UI Model generation itself).
- **1.1.0** (2026-10-22): Prior update (see git history for details).
- **1.0.0** (2026-03-16): Initial release.
