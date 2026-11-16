---
name: requirements-merge
description: Combine two or more overlapping requirement sources into one coherent specification, detecting duplicates and conflicts, resolving only the safe ones automatically, logging the rest for stakeholder decision, and keeping every unified requirement traceable to its sources. Produces unified-requirements.md, merge-analysis.json, and merge-conflicts.md. Use when requirements arrive from several documents, teams, or versions that overlap or contradict each other, when stakeholder feedback must be reconciled with an existing specification, or when asked to consolidate, de-duplicate, or reconcile requirements.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Requirements Merge

Merge several requirement sources into one specification without losing anything, hiding any disagreement, or deciding on a stakeholder's behalf.

Use `requirements-ingest` when sources simply add up (new material for the same requirements set). Use this skill when they overlap or disagree.

## Inputs

- **Sources**: two or more requirement documents, or `requirements.json` files produced by `requirements-ingest`
- **Project**: the project folder, `OrgDocument/projects/[NN] - [Project Name]/`
- **Merge strategy** *(optional)*: `conservative` (every conflict goes to stakeholder review) or `comprehensive` (safe conflicts are auto-resolved; the default)

## Outputs

Written to `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- `unified-requirements.md` — the merged specification
- `merge-analysis.json` — the merge trace: every unified requirement with its sources, every conflict, every consolidation
- `merge-conflicts.md` — the conflicts, for stakeholder review

### `merge-analysis.json` (top level)

| Key | Content |
|---|---|
| `metadata` | `project_id`, `merge_timestamp`, `sources` (file name, requirement count, format), `merge_strategy` |
| `merge_summary` | Input and output requirement counts; conflicts identified, auto-resolved, and pending |
| `unified_requirements` | One per requirement: `id`, `text`, `category`, `merge_type`, `confidence_level`, `stakeholder_status`, `source_traceability` (source file, original ID, original text, contribution) |
| `conflicts` | `id` (`CR-001`), `description`, `status`, `business_impact`, `technical_impact`, `sources_involved` (source, position, rationale), `proposed_resolution`, `escalation_level` |
| `redundancy_analysis` | `eliminated_redundancies`, `preserved_variations` |

### `unified-requirements.md` (sections)

`## Executive Summary`, `## Requirements by Category` (consensus requirements, requirements with resolved conflicts, requirements added from a single source), `## Conflict Resolution Log`, `## Redundancy Analysis`, `## Traceability Matrix`.

### `merge-conflicts.md`

Conflicts grouped by priority. For each: what the sources say, the impact, the options, a recommendation, and who needs to decide.

The complete layout of all three files, as a worked example, is in [references/output-format.md](references/output-format.md).

## Workflow

### 1. Normalize every source

Bring each source to atomic requirements with stable IDs. For a raw document, apply `requirements-ingest`'s extraction rules, keeping each source's own IDs (or assigning per-source ones such as `SF-012`) so that the original statement can always be found.

### 2. Match requirements across sources

Compare by meaning, not wording. Each requirement falls into one of:

| Relationship | Meaning | Action |
|---|---|---|
| **Duplicate** | Same need, same constraints | Consolidate into one; cite all sources |
| **Complementary** | Same need, each adds detail | Combine into one fuller requirement; cite all sources |
| **Variation** | Same need, legitimately different by platform, region, role, or phase | Keep the variations distinct and say why |
| **Conflict** | Cannot all be true | Go to step 3 |
| **Unique** | Appears in one source only | Carry over as it is |

### 3. Classify and prioritize conflicts

Types: direct contradiction, priority mismatch, different scope for the same requirement, different approach to the same goal, incompatible quality targets, incompatible timelines.

| Priority | Typical subject |
|---|---|
| High | Architecture, regulation, security fundamentals, anything with large cost or schedule impact |
| Medium | Feature behaviour, performance targets, integration approach |
| Low | Implementation detail, tooling, conventions |

### 4. Resolve only what is safe to resolve

Under the `comprehensive` strategy, auto-resolve a conflict only when all of these hold: the resolution does not change business logic, has no significant cost or schedule impact, is technically feasible, and is one every affected stakeholder would reasonably accept. Typical safe resolutions:

- Two compliance or security requirements: apply the stricter.
- Two quality or test-coverage standards: apply the higher, if feasible.
- The same requirement stated at two levels of detail: keep the more specific.

Log every automatic resolution with its rationale so it can be challenged. Under `conservative`, auto-resolve nothing.

Everything else is **pending**. For each pending conflict, set out the positions, the impact of each option, and a recommendation, and name the level that should decide (team, architecture review, business stakeholders, executive). In the unified specification, mark the affected requirement as unresolved and state the interim assumption, if one is needed to continue.

**Never record a decision, approval, or sign-off that has not actually been given.** `stakeholder_status` is `pending` until a real person decides (in `solo` collaboration mode, until the developer explicitly decides in the relevant role and says so). The worked example's approvals and dates are illustrations, not defaults.

### 5. Write the unified specification

- Organize by business area, then by requirement. Use one consistent vocabulary; where sources used different terms for one thing, pick one and note the synonym.
- Assign unified IDs (`R-001`, ...) and record, for each, every source requirement it came from and how (`consensus`, `enhancement`, `aggregation`, `conflict_resolution`, `addition`).
- Report honest statistics: counts come from the actual merge. Do not include satisfaction rates, approval percentages, or other figures nobody measured.

### 6. Check coverage, then write the files

Go through every requirement of every source and confirm it is represented in the unified set, consolidated into something that is, or listed in a conflict. Nothing may simply disappear. Then write the three files and check against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py requirements-merge \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- Every source requirement is accounted for, and every unified requirement traces to at least one source.
- Every conflict is listed, with its sources' actual positions; none was settled quietly by choosing a side.
- Automatic resolutions meet all the safety conditions and are logged.
- Legitimate variations were kept apart, not flattened into one requirement.
- No approval, decision, date, or metric in the output is invented.

## Integration

**Upstream**: `requirements-ingest` (normalized sources), optionally `goals-extract` and `process-w5h` (priorities and who decides)

**Downstream**: `goals-extract`, `process-scopemin`, `domain-extractconcepts` (run on the unified set), `change-management` (resolutions that change agreed requirements)

To make the unified set the project's `requirements.json`, run `requirements-ingest` on `unified-requirements.md`, or keep both and state in the project which one downstream skills should read.
