---
name: goals-extract
description: Extract the business goal, success criteria, KPIs, constraints, assumptions, and open questions from a project's requirements, each traced to the requirement it came from, written as goals.md and goals.json. Use after requirements-ingest when the user asks what the project is trying to achieve, how success will be measured, or what is still undecided, and before scoping (process-scopemin) or planning (plan-derivetasks), which both read goals.json.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Goals Extract

Requirements say what must be built. This skill extracts why: the outcomes the business wants, how it will know they were achieved, and what limits or uncertainties surround them.

## Inputs

- **Primary**: `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/requirements.json` (from `requirements-ingest`)

If it does not exist, run `requirements-ingest` first; goals extracted straight from a raw document have no requirement IDs to trace to.

## Outputs

Written to `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- `goals.json` — structured data for downstream skills
- `goals.md` — human-readable report

### `goals.json`

```json
{
  "project_id": "PRJ-07",
  "goal_statement": "string",
  "success_criteria": [{ "id": "SC-001", "criteria": "string", "source_refs": ["R-001"] }],
  "kpis": [{ "kpi": "string", "source_refs": ["R-002"], "target_value": "string", "timeframe": "string" }],
  "constraints": [{ "constraint": "string", "source_refs": ["R-004"] }],
  "assumptions": [{ "assumption": "string", "source_refs": ["R-005"] }],
  "open_questions": [{ "question": "string", "source_refs": ["R-001"] }],
  "traceability": {
    "source_requirements": ["R-001", "R-002"],
    "extraction_timestamp": "ISO-8601",
    "confidence_scores": { "goal_statement": 0.9, "overall": 0.85 }
  }
}
```

All six content keys are always present; use an empty array when the requirements genuinely contain none of that kind. `source_refs` holds requirement IDs from `requirements.json`, optionally with a section (`R-001:2.1`). `id`, `target_value`, and `timeframe` are optional.

### `goals.md`

```markdown
# Goals Analysis

## Business Goal
[Goal statement]

## Success Criteria
- [Criterion] *(Ref: R-001)*

## Key Performance Indicators
- [KPI with target and timeframe] *(Ref: R-002)*

## Constraints
- [Constraint] *(Ref: R-004)*

## Assumptions
- [Assumption] *(Ref: R-005)*

## Open Questions
- [Question] *(Ref: R-001)*

---
**Traceability:** Extracted from requirements: R-001, R-002
**Generated:** [timestamp]
```

A complete worked example of both files is in [references/example-output.md](references/example-output.md).

## Workflow

### 1. Find the outcome statements

Read every requirement and mark the ones that express a desired outcome, not a system behaviour. Signals:

- **Outcome verbs**: increase, reduce, improve, decrease, optimize, ensure, enhance, streamline, grow, expand, maintain
- **Intent phrases**: "the objective is to", "the goal is to", "should aim to", "in order to", "so that"
- **Targets and deadlines**: a number, percentage, date, or "within [timeframe]"

"The system shall export reports" is a mandate, not a goal. "The system shall export reports so that month-end close takes one day instead of three" contains one: the faster close. Extract the outcome and leave the mandate behind.

### 2. Sort what you found

| Output | What belongs there |
|---|---|
| `goal_statement` | One or two sentences stating the overall outcome the project exists to achieve. Synthesize it from the outcome statements; do not copy a feature description |
| `success_criteria` | Conditions that, when true, show the goal was met. Each should be checkable |
| `kpis` | Quantities that will be measured, with target value and timeframe where the requirements give them |
| `constraints` | Limits the solution must respect (requirements tagged `constraint`, plus limits stated inside other requirements) |
| `assumptions` | Things taken as true that the goal depends on |
| `open_questions` | Anything the requirements leave undecided, contradict themselves on, or state too vaguely to act on |

### 3. Keep it honest

- **Do not invent targets.** If a requirement says "faster" with no number, the criterion is "faster than today" and the missing number is an open question. A made-up "25% faster" looks measured and is not.
- **Do not fill a section for the sake of it.** An empty `kpis` array with an open question "No measurable targets are stated; how will success be measured?" is the correct output for requirements that state none.
- **Every item cites at least one requirement.** An item you cannot trace is your inference; either find its source or move it to open questions.
- Confidence scores reflect how directly the requirements state the goal: high when a goal is stated outright, lower when it had to be synthesized from scattered hints.

### 4. Write both files

Write `goals.json` and `goals.md` with the same content, then check against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py goals-extract \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Quality checks

- The goal statement describes a business outcome, not a feature list.
- Success criteria are checkable; where the requirements give numbers, the criteria carry them (specific, measurable, time-bound).
- Every item traces to a requirement ID that exists in `requirements.json`.
- No target, deadline, or KPI appears that the requirements do not state.

## Integration

**Upstream**: `requirements-ingest`

**Downstream**: `process-scopemin` (business-value weighting), `plan-derivetasks`, `domain-extractconcepts` (optional context), `project-status-reporting`
