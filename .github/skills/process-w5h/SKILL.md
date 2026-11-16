---
name: process-w5h
description: Analyse a project's requirements along six dimensions (Who, What, When, Where, Why, How) to surface stakeholders and their roles, functional scope, timing, operating context, business rationale, and implementation approach, written as w5h-analysis.md and w5h-analysis.json. Use after requirements-ingest when the user asks who is involved or affected, wants a stakeholder analysis, wants the requirements examined from several perspectives, or needs gaps in the requirements exposed before domain modeling or planning.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Process W5H Analysis

Read the requirements six times, each time asking a different question. The value is as much in what a dimension cannot answer as in what it can: a requirements set that says nothing about *when* or *who decides* has a gap worth reporting.

## Inputs

- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (from `requirements-ingest`)
- **Optional**: `goals.json` (from `goals-extract`), which informs Why
- **Read automatically**: `collaboration_mode` in the project's `project-metadata.json` (`solo` or `traditional`; absent means `traditional`)

## Outputs

Written to `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- `w5h-analysis.md` — the report
- `w5h-analysis.json` — the same content for downstream skills

### `w5h-analysis.json`

The six dimension keys are fixed. The structure inside each follows what the requirements contain; the sub-keys below are the usual ones.

```json
{
  "project_id": "PRJ-07",
  "generated_at": "ISO-8601",
  "analysis_framework": "W5H",
  "who":   { "primary_stakeholders": [], "secondary_stakeholders": [], "roles_responsibilities": [] },
  "what":  { "functional_requirements": [], "non_functional_requirements": [], "scope": { "in_scope": [], "out_of_scope": [] } },
  "when":  { "timeline": {}, "milestones": [] },
  "where": { "environment": {}, "integration_points": {} },
  "why":   { "business_drivers": {}, "success_metrics": {} },
  "how":   { "technical_approach": {}, "implementation_phases": [], "risks": [] }
}
```

### `w5h-analysis.md`

```markdown
# W5H Requirements Analysis

**Project**: PRJ-07
**Source**: requirements.json
**Generated**: [timestamp]

## WHO — Stakeholders and Roles
## WHAT — Functional and Non-Functional Requirements
## WHEN — Timeline and Milestones
## WHERE — Context and Environment
## WHY — Purpose and Business Rationale
## HOW — Implementation Approach and Methods
## Summary
```

Each of the six dimension sections is required, with its heading starting `## WHO`, `## WHAT`, and so on. The full layout of both files, with a worked example, is in [references/output-format.md](references/output-format.md).

## Workflow

### 1. Analyse each dimension

Cite requirement IDs (`R-xxx`) for what you record.

| Dimension | Question | Look for |
|---|---|---|
| **Who** | Who is involved, and in what capacity? | Primary stakeholders (users, customers, decision makers); secondary stakeholders (support, operations, regulators, partners); each role's responsibilities and authority; influence and interest |
| **What** | What must exist or happen? | Functional and non-functional requirements; business rules; explicit in-scope and out-of-scope statements |
| **When** | What are the timing facts? | Deadlines, phases, milestones, sequencing dependencies, triggers and frequencies |
| **Where** | In what context does this operate? | Organizational setting, systems it must integrate with, operating environment, physical or geographic boundaries |
| **Why** | What justifies the work? | The problem being solved, business drivers, success measures, value to each stakeholder |
| **How** | How will it be approached? | Method and approach stated or implied by the requirements, phases, risks with mitigations |

### 2. Identify stakeholders by role

Name roles ("Finance Approver"), never individuals. Record influence and interest as `high`, `medium`, or `low` where the requirements support a judgement.

### 3. Report gaps, do not fill them

When the requirements say nothing about a dimension, say so in that section ("The requirements state no deadline or sequencing constraint") and list it as an open item. Do not supply a plausible-looking timeline, stakeholder, budget, or risk that the requirements do not support. For How in particular, record the approach the requirements point to and mark your own suggestions as suggestions.

### 4. Confirm the stakeholder analysis

How the Who analysis gets confirmed depends on `collaboration_mode`; the output format is the same in both.

- **`traditional`**: each identified role is confirmed by a real person in that role before the analysis is treated as settled. Record who confirmed what.
- **`solo`**: take each role's perspective in turn and note inline, beside each stakeholder entry, which role lens you used and what you assumed on its behalf, for example: *"Assumed as End User: primary motivation is reducing manual data entry (R-014)."*

Even in solo mode, go to a real stakeholder when:

- a role's priorities are unclear from the requirements and guessing would change the Why or What analysis;
- the role is a real external party whose authority you cannot stand in for (a compliance officer's reading of a regulation, a paying client's budget ceiling);
- the decision is high-stakes: irreversible, costly to redo, or affecting a committed deadline.

Record which items were escalated and why. The gate's `stakeholder_roles_confirmed` check looks for this confirmation in the project state (see `edps-workflow-orchestrator/references/gate-schema.md`). The collaboration modes are described in `OrgDocument/projects/05 - Building Skills Iteration 4/artifacts/Documentation/collaboration-mode-reference.md`.

### 5. Write both files

Write `w5h-analysis.json` and `w5h-analysis.md` with the same content, then check against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py process-w5h \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- All six dimensions are present, each either answered from the requirements or reported as a gap.
- Statements cite the requirements they rest on.
- Stakeholders are roles, not named people.
- Nothing in the analysis (dates, durations, metrics, stakeholders) was invented to make a dimension look complete.

## Integration

**Upstream**: `requirements-ingest`, optionally `goals-extract`

**Downstream**: `process-scopemin` (stakeholder context), `process-merge`, `plan-derivetasks`, `diagram-generatecollaboration` (actors)
