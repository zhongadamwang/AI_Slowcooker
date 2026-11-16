---
name: requirements-ingest
description: Turn requirements documents in any format (Markdown, PDF, Word, email, pasted text, meeting notes) into a numbered list of atomic requirements with classification tags, source traceability, and confidence, written as requirements.md and requirements.json. Use when starting analysis on a new project, when the user supplies a requirements or specification document to process, when new source material must be added to an existing requirements set, or before any skill that needs requirements.json (goals-extract, process-w5h, domain-extractconcepts, plan-derivetasks).
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-15"
---

# Requirements Ingest

Read the source documents and produce one atomic, traceable requirement per item. Every downstream analysis skill reads the result, so the IDs assigned here are the traceability anchor for the whole project.

## Inputs

- **Source documents**: one or more files or pasted text. Originals belong in the project's `artifacts/Source Materials/`.
- **Project**: the project folder, `OrgDocument/projects/[NN] - [Project Name]/`.

If a source mixes business needs with IT infrastructure, implementation choices, or operational procedure (a transcript, a change request, a runbook, a technical spec), run `requirements-sanitize` first and ingest its `sanitized-requirements.md` instead. Ingesting such a source directly produces "requirements" that are really one team's past implementation decisions.

## Outputs

Written to `OrgDocument/projects/[NN] - [Project Name]/artifacts/Analysis/`:

- `requirements.md` — the human-readable report
- `requirements.json` — the same content for downstream skills

### `requirements.json`

```json
{
  "project_id": "PRJ-07",
  "generated_at": "2026-02-08T14:30:00Z",
  "total_requirements": 2,
  "requirements": [
    {
      "id": "R-001",
      "source_file": "requirements.pdf",
      "location_hint": "page 3, para 2",
      "text": "The system shall authenticate users within 3 seconds.",
      "tags": ["functional", "nonfunctional"],
      "confidence": 0.95
    }
  ],
  "glossary_suspects": ["OAuth2", "PCI DSS"]
}
```

| Field | Rule |
|---|---|
| `id` | `R-` plus a zero-padded three-digit number, assigned in document order. IDs are permanent (see Re-ingesting) |
| `source_file` | File name of the source the requirement came from |
| `location_hint` | Where in that source: section heading, page and paragraph, or line. Specific enough to find the original text |
| `text` | One verifiable statement, in the source's meaning. Reword only as far as needed to make it stand alone |
| `tags` | One or more of `functional`, `nonfunctional`, `constraint`, `assumption`, `out-of-scope` |
| `confidence` | 0.0–1.0: how clearly the source states this requirement (see Step 4) |
| `glossary_suspects` | Domain terms, acronyms, and product names a newcomer would need defined |

Additional fields are allowed when the source supports them (for example `section`, `priority`, `acceptance_criteria`). Do not rename or drop the fields above; downstream skills read them.

### `requirements.md`

```markdown
# Requirements Analysis Report

**Project**: PRJ-07
**Source**: requirements.pdf
**Generated**: 2026-02-08T14:30:00Z
**Total Requirements**: 2

## Requirements

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-001 | Authentication | The system shall authenticate users within 3 seconds. | functional, nonfunctional | high |
| R-002 | Performance | API response times shall not exceed 200 ms. | nonfunctional | high |

## Glossary Suspects
- OAuth2
- PCI DSS
```

The `## Requirements` table and `## Glossary Suspects` are required. Add further sections when the source calls for them (for example open questions, or decisions the source records as already made).

## Workflow

### 1. Read every source in full

Read the whole of each document before extracting anything, including tables, appendices, and footnotes. For a PDF or Word file, read it with whatever document-reading capability is available; if a file cannot be read, stop and say so instead of working from its name or a partial extract.

### 2. Split into atomic requirements

One requirement states one thing that could be checked on its own.

- Split compound sentences: "The system shall export reports and email them to managers" is two requirements.
- Keep a condition with the behaviour it governs: "Orders above $10,000 require dual approval" is one.
- Keep each self-contained. Replace "it" and "this feature" with what they refer to.
- Atomicity matters more than length, but a requirement running past a short paragraph usually hides several.
- Do not invent requirements the source does not state. Background, rationale, and examples are context, not requirements, unless they state a need.

### 3. Classify

| Tag | Use for |
|---|---|
| `functional` | What the system or process does: features, actions, behaviours |
| `nonfunctional` | How well: performance, security, usability, availability, compliance qualities |
| `constraint` | A limit imposed from outside: budget, deadline, mandated technology, regulation |
| `assumption` | Something taken as true that the requirements depend on |
| `out-of-scope` | Something the source explicitly excludes |

A requirement may carry more than one tag.

### 4. Score confidence

| Range | Meaning |
|---|---|
| 0.8–1.0 | Stated explicitly and unambiguously |
| 0.5–0.79 | Stated, but vague, incomplete, or missing a measurable target |
| below 0.5 | Inferred from context, or the source contradicts itself |

In `requirements.md`, show `high`, `medium`, or `low` for those three ranges. A low score flags something for a human to clarify; it is not a reason to drop the requirement.

### 5. Assign IDs and write both files

Number in document order starting at `R-001`. Write `requirements.json` and `requirements.md` with identical content, and set `total_requirements` to the actual count.

### Re-ingesting

When `requirements.json` already exists and sources are added or revised:

- Keep every existing ID attached to the same requirement. Other artifacts cite these IDs.
- Give new requirements the next unused numbers. Never reuse the number of a removed requirement.
- When a requirement's text changes, keep its ID and update the text.
- When an existing requirement must be split, keep its ID for the first part and give the others a letter suffix (`R-309a`), so existing citations still resolve.
- Do not silently delete a requirement that later artifacts reference. Record the change through `change-management`.

For combining several independently written requirement sets that overlap or conflict, use `requirements-merge`.

## Quality checks

- Every requirement is atomic, self-contained, and traceable to a findable place in a source.
- Every statement of need in the sources appears in the output; nothing was skipped because it was awkward to classify.
- No requirement was invented, and none had its meaning changed by rewording.
- `total_requirements` equals the number of entries, IDs are unique and sequential, and the two files agree.

Check the result against the gate:

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py requirements-ingest \
    --project "OrgDocument/projects/[NN] - [Project Name]"
```

## Integration

**Upstream**: `project-document-management` (project folder), `requirements-sanitize` (optional clean-up of mixed-perspective sources)

**Downstream**: `goals-extract`, `process-w5h`, `process-scopemin`, `domain-extractconcepts`, `requirements-merge`, `plan-derivetasks`, `change-management`
