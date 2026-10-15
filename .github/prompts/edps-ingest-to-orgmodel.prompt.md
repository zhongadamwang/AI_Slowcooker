---
description: "Run the full EDPS ingest-to-orgModel workflow: sanitize, ingest, goals, W5H, domain analysis, collaboration diagram, orgModel update."
name: edps-ingest-to-orgmodel
argument-hint: "Requirements file path or project folder, e.g. 'OrgDocument/projects/05 - Building Skills Iteration 4'"
agent: edps-ba
---
Run the ingest-to-orgModel workflow for: ${input:source:Requirements file or project folder}

Read each skill's `SKILL.md` in `.github/skills/` before applying it. Track the steps with a todo list and save intermediate outputs under the project's `artifacts/` subfolders.

1. `requirements-sanitize` (skip if the source is already business-only; say which).
2. `requirements-ingest`.
3. `goals-extract`.
4. `process-w5h`.
5. `process-scopemin` to separate core from optional requirements.
6. `domain-extractconcepts`, then `domain-alignentities` against `OrgDocument/orgModel/`, then `domain-proposenewconcepts` for gaps.
7. `diagram-generatecollaboration` for the affected process level.
8. `process-merge` and `model-integration` if the new process overlaps the existing orgModel; otherwise `orgmodel-update`.
9. `process-findtopandupdate` to keep top-level requirements consistent.

Stop and ask me before step 8 if any alignment conflict or requirement contradiction is unresolved.

End with a summary: files changed (as links), open questions, and a suggestion to use the "Validate hierarchy and compliance" handoff.
