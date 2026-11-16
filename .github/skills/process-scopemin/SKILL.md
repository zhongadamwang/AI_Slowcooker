---
name: process-scopemin
description: Find the minimum viable scope in a requirements set by grouping requirements into features and classifying each as core, enhancement, or optional from its business value, dependencies, and complexity, then laying out a phased roadmap, written as scope-analysis.md and scope-analysis.json. Use when the user asks what the MVP is, what can be deferred or cut, how to phase delivery, or how to fit a requirements set to limited time or budget; and before plan-derivetasks, which reads the scope decision.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Process Scope Minimization

Decide what is the least that must be built for the product to be worth having, and put everything else in a later phase with a reason.

## Inputs

- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (from `requirements-ingest`)
- **Recommended**: `goals.json` (from `goals-extract`). Business value is judged against the stated goal; without it, say that value was judged from the requirements alone
- **Optional**: `w5h-analysis.json` (stakeholders and constraints); any time, budget, or team limits the user states

## Outputs

Written to `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- `scope-analysis.md` — the report and recommendation
- `scope-analysis.json` — the same classification for downstream skills

### `scope-analysis.json` (top level)

| Key | Content |
|---|---|
| `metadata` | `project_id`, `source_file`, `generated_timestamp`, `analysis_method` |
| `mvp_summary` | `definition`, counts of core / enhancement / optional features, `estimated_effort` |
| `features` | One per feature: `id` (`FEAT-001`), `name`, `category` (`core`, `enhancement`, or `optional`), `business_value` (`score`, `justification`), `technical_complexity` (`score`, `implementation_notes`), `dependencies`, `user_impact`, `phase_assignment` |
| `roadmap` | Feature IDs per phase: `phase0_foundation`, `phase1_mvp`, `phase2_enhancement`, `phase3_expansion` |
| `scope_boundaries` | `in_scope`, `out_of_scope` |
| `risks` | `id`, `priority`, `description`, `impact`, `mitigation` |
| `success_criteria` | `mvp_launch`, `enhancement_phase` |
| `traceability` | Per feature: `feature_id`, `source_requirements` (requirement IDs), `justification` |

### `scope-analysis.md` (sections)

`## Executive Summary`, `## Core Features (MVP Essential)`, `## Enhancement Features (Post-MVP Phase 1)`, `## Optional Features (Future Consideration)`, `## Feature Prioritization Matrix`, `## MVP Roadmap`, `## Scope Boundaries`, `## Risk Assessment`, `## Success Criteria`, `## Recommendations`.

The complete templates for both files are in [references/output-format.md](references/output-format.md).

## Workflow

### 1. Group requirements into features

A feature is a capability a user or the business would recognise ("order tracking"), usually backed by several requirements. Give each a `FEAT-###` ID and record which requirement IDs it covers. Every functional requirement belongs to some feature; note any that fit none.

### 2. Assess each feature

Score each `high`, `medium`, or `low`, with a one-line justification.

| Dimension | High | Medium | Low |
|---|---|---|---|
| **Business value** | Directly serves the stated goal; a critical user workflow; what makes the product worth having | Improves efficiency or satisfaction; strengthens the offering | Convenience; an advanced or rare case; preparation for the future |
| **Complexity** | New technology, difficult integration, significant unknowns | Standard implementation with known patterns | Well understood, little integration, low risk |

Then map dependencies: which features need which others to exist first. Include business dependencies (a regulatory requirement, a partner integration) as well as technical ones.

### 3. Classify

- **Core**: the product does not solve its problem without it, or other core features depend on it.
- **Enhancement**: clearly valuable and builds on the core, but the MVP is usable without it.
- **Optional**: nice to have; low immediate value or speculative.

Dependencies override value scores: a low-value feature that a core feature depends on is core. A high-value feature with heavy dependencies and high complexity is a candidate for the first enhancement phase, with the reason stated.

### 4. Test the MVP boundary

The core set is a valid MVP only if all of these hold. If one fails, move features until it does.

- A user can complete at least one whole workflow from start to finish.
- The product solves a complete problem, not a fragment of one.
- It delivers enough value to validate the business goal.
- It is a foundation the enhancement features can be added to without rework.

Also check from the other side: is anything in core that could be removed without breaking those four? The point of the exercise is the smallest set that passes.

### 5. Lay out the roadmap

- **Phase 0 — Foundation**: infrastructure and groundwork the core features need
- **Phase 1 — MVP**: the core features
- **Phase 2 — Enhancement**: the first enhancement features
- **Phase 3 — Expansion**: remaining enhancement and optional features

State what is in and out of scope for the MVP explicitly. An out-of-scope list is as useful to stakeholders as the in-scope one.

### 6. Write both files

Write `scope-analysis.json` and `scope-analysis.md` with the same classification, then check against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py process-scopemin \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- Every feature has a category, a value justification, a complexity assessment, and its source requirement IDs.
- No core feature depends on a feature in a later phase.
- The MVP passes the four boundary tests, and the report says how.
- Effort estimates are given only as rough ranges and labelled as such; detailed estimation is `plan-estimateeffort`'s job.
- The scope decision is a recommendation. In `traditional` collaboration mode it needs stakeholder approval before planning treats it as settled; record the approval status truthfully ("Pending" until someone has actually approved).

## Integration

**Upstream**: `requirements-ingest`, `goals-extract`, optionally `process-w5h`

**Downstream**: `plan-derivetasks` (tasks for the MVP scope), `project-planning-tracking`, `diagram-generatecollaboration` (which features to model first), `change-management` (later scope changes)
