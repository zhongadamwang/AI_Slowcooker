# EDPS Skills User Manual

This repository contains a set of AI-assisted skills for starting projects, analyzing requirements, modeling business processes, planning work, and maintaining EDPS documentation. Use them from GitHub Copilot in VS Code by describing what you want to do; you do not need to know the skill name or provide a complete specification.

## Quick Start

### Start a project

Start with a rough idea. You do not need to choose a project number, folder layout, or process name:

```text
@workspace Help me start a project. I want to make it easier for customers to use our portal on their phones.
```

The [project-document-management](.github/skills/project-document-management/SKILL.md) skill can ask a few focused questions, recommend a structure, show a short preview, and confirm before creating project files. You can also ask it to proceed with sensible defaults.

### Work with an existing project

Name the goal and, when known, the project folder or project number:

```text
@workspace In OrgDocument/projects/01 - Building Skills, turn these notes into traceable requirements and a goals summary.

[Paste notes or attach source files]
```

The [edps-skill-navigator](.github/skills/edps-skill-navigator/SKILL.md) can recommend a skill or workflow from a plain-language request. For a multi-step workflow with tracked progress, use [edps-workflow-orchestrator](.github/skills/edps-workflow-orchestrator/SKILL.md).

## How to Use the Skills

1. **Describe the outcome.** For example, "clean up this requirements document," "show what this process change affects," or "estimate these tasks."
2. **Provide the available context.** Attach source documents or point to the project folder. If details are missing, the skill should identify assumptions or ask focused questions; you do not need to invent technical identifiers.
3. **Review the proposed work and generated files.** Most skills produce Markdown for people and, where useful, JSON for downstream processing.
4. **Continue with the next useful step.** You can invoke a skill directly, ask the navigator what to do next, or use the orchestrator to manage a longer workflow.

Use a skill by name when you know what you want:

```text
@workspace Use requirements-ingest to turn the attached product brief into traceable, atomic requirements for OrgDocument/projects/01 - Building Skills.
```

For broad requests, describe the goal instead:

```text
@workspace Help me turn these requirements into a scoped, modeled, and documented project plan. Suggest the steps and pause for my review at important decisions.
```

## Find the Right Skill

Each skill name links to its detailed guide. Skills can be used individually; the suggested next steps below are common paths, not mandatory pipelines.

### Project setup and workflow guidance

| Skill | Use it to… |
|---|---|
| [project-document-management](.github/skills/project-document-management/SKILL.md) | Start or update a project structure, initialize process documentation, change a project archetype or collaboration mode, or validate project folders. |
| [edps-skill-navigator](.github/skills/edps-skill-navigator/SKILL.md) | Describe a goal in everyday language and get a recommended skill or sequence. |
| [edps-workflow-orchestrator](.github/skills/edps-workflow-orchestrator/SKILL.md) | Start, track, resume, or manage a multi-skill workflow with prerequisites and project state. |

### Requirements and early analysis

| Skill | Use it to… |
|---|---|
| [requirements-sanitize](.github/skills/requirements-sanitize/SKILL.md) | Separate business needs from implementation, infrastructure, or operational detail in a mixed source document. Use before ingestion when that noise would obscure the business requirements. |
| [requirements-ingest](.github/skills/requirements-ingest/SKILL.md) | Convert source documents, notes, or email into classified, traceable requirements. |
| [requirements-merge](.github/skills/requirements-merge/SKILL.md) | Combine multiple requirement sources, identify duplicates or conflicts, and preserve where requirements came from. |
| [goals-extract](.github/skills/goals-extract/SKILL.md) | Identify goals, success measures, constraints, assumptions, and open questions from requirements. |
| [process-w5h](.github/skills/process-w5h/SKILL.md) | Analyze requirements from Who, What, When, Where, Why, and How perspectives. |
| [process-scopemin](.github/skills/process-scopemin/SKILL.md) | Separate essential first-release scope from optional or later work. |

### Domain and process modeling

| Skill | Use it to… |
|---|---|
| [domain-extractconcepts](.github/skills/domain-extractconcepts/SKILL.md) | Find business entities, terminology, and relationships in requirements. |
| [domain-alignentities](.github/skills/domain-alignentities/SKILL.md) | Compare extracted concepts with existing organizational models and terminology. |
| [domain-proposenewconcepts](.github/skills/domain-proposenewconcepts/SKILL.md) | Identify domain-model gaps and propose concepts supported by the requirements. |
| [diagram-generatecollaboration](.github/skills/diagram-generatecollaboration/SKILL.md) | Create collaboration and related Mermaid diagrams with requirement traceability. |
| [process-merge](.github/skills/process-merge/SKILL.md) | Integrate a new process model with existing organizational processes while minimizing overlap and disruption. |
| [model-integration](.github/skills/model-integration/SKILL.md) | Integrate domain models and processes into the organizational model and resolve conflicts. |
| [process-findtopandupdate](.github/skills/process-findtopandupdate/SKILL.md) | Carry detailed analysis or process changes back to top-level requirements and documents. |
| [hierarchy-management](.github/skills/hierarchy-management/SKILL.md) | Decompose a control participant into a child process, navigate the process tree, or manage hierarchy metadata. |
| [documentation-automation](.github/skills/documentation-automation/SKILL.md) | Generate or regenerate process, collaboration, domain-model, and navigation documents from a process model. |
| [orgmodel-update](.github/skills/orgmodel-update/SKILL.md) | Update organizational model documents and folders based on requirements and domain analysis. |

### Planning, tracking, and change

| Skill | Use it to… |
|---|---|
| [plan-derivetasks](.github/skills/plan-derivetasks/SKILL.md) | Turn requirements and goals into tasks with deliverables, acceptance criteria, and dependencies. |
| [plan-estimateeffort](.github/skills/plan-estimateeffort/SKILL.md) | Estimate task effort with rationale and uncertainty. |
| [plan-buildschedule](.github/skills/plan-buildschedule/SKILL.md) | Build a schedule from tasks, estimates, dependencies, and constraints. |
| [project-planning-tracking](.github/skills/project-planning-tracking/SKILL.md) | Set up project phases, milestones, task tracking, and progress updates. |
| [project-status-reporting](.github/skills/project-status-reporting/SKILL.md) | Summarize project status for teams, stakeholders, or executives using project documentation. |
| [change-management](.github/skills/change-management/SKILL.md) | Record a requirement, process, or specification change and its rationale and traceability. |
| [change-impact-analysis](.github/skills/change-impact-analysis/SKILL.md) | Trace a proposed or completed change across hierarchy levels and identify affected artifacts; supports what-if analysis. |

### Migration, validation, and quality

| Skill | Use it to… |
|---|---|
| [migration-tools](.github/skills/migration-tools/SKILL.md) | Convert legacy flat collaboration diagrams to the hierarchical format while preserving traceability. |
| [hierarchy-validation](.github/skills/hierarchy-validation/SKILL.md) | Check structural consistency, participant types, naming, and links across a process hierarchy or branch. |
| [edps-compliance](.github/skills/edps-compliance/SKILL.md) | Check EDPS methodology, boundaries, requirements traceability, and evolution history; get findings and remediation guidance. |
| [integration-testing](.github/skills/integration-testing/SKILL.md) | Run the EDPS skill-suite integration and workflow validation process. |

### GitHub task synchronization and skill development

| Skill | Use it to… |
|---|---|
| [github-issue-create-update](.github/skills/github-issue-create-update/SKILL.md) | Create or update GitHub Issues from local Markdown task files and record issue references in those files. |
| [github-issue-sync-status](.github/skills/github-issue-sync-status/SKILL.md) | Check or synchronize local task status from linked GitHub Issues and report conflicts. |
| [skill-creator](.github/skills/skill-creator/SKILL.md) | Create, improve, or package a skill for a specialized workflow. |

## Common Workflows

### Requirements to analysis

```text
@workspace Help me analyze these source materials for OrgDocument/projects/01 - Building Skills.
If the documents mix business needs with technical or operational details, clean that up first.
Then create traceable requirements and identify goals, success measures, assumptions, and open questions.
```

Common sequence: `requirements-sanitize` when useful → `requirements-ingest` → optionally `requirements-merge` → `goals-extract` and/or `process-w5h` → `process-scopemin`.

### Requirements to domain model and process diagrams

```text
@workspace Use the requirements and goals in this project to identify domain concepts,
compare them with our existing orgModel, identify any gaps, and create traceable collaboration diagrams.
Show me important assumptions before updating existing models.
```

Common sequence: `domain-extractconcepts` → `domain-alignentities` → `domain-proposenewconcepts` as needed; use `diagram-generatecollaboration` to create diagrams. Use `process-merge` or `model-integration` when incorporating new work into an existing organizational model.

### Plan delivery

```text
@workspace Based on this project's requirements and goals, identify the first useful release,
derive tasks with acceptance criteria and dependencies, estimate the effort, and propose a schedule.
Call out unknowns instead of inventing dates or team capacity.
```

Common sequence: `process-scopemin` → `plan-derivetasks` → `plan-estimateeffort` → `plan-buildschedule`. Use `project-planning-tracking` to manage milestones and `project-status-reporting` to communicate progress.

### Create or update a process hierarchy

```text
@workspace Decompose the Order Service control participant into a child process.
Keep the hierarchy links consistent, generate the child process documentation, and validate the result.
```

Common sequence: `diagram-generatecollaboration` → `hierarchy-management` → `documentation-automation` → `hierarchy-validation` → `edps-compliance`. For changes to an existing hierarchy, use `change-impact-analysis` first to review the impact; use `change-management` to record the change.

### Track work with GitHub Issues

```text
@workspace Create or update GitHub Issues from the task files in this project.
Show me the proposed changes and report any task files that cannot be synchronized.
```

Use `github-issue-create-update` to publish local task files and `github-issue-sync-status` to bring issue status back into local files. GitHub access is required; provide repository access through the configured environment or approved authentication flow. Do not put access tokens in project files or commit them.

## Project and File Structure Convention

Project documentation in this repository lives under `OrgDocument/`. Project folders use a sequential two-digit number and a readable name; the registry is [OrgDocument/projects/projects.md](OrgDocument/projects/projects.md). Generated artifacts belong in the project tree, not in a generic `projects/[PROJECT-ID]/` directory.

### Project layout

```text
OrgDocument/
├── projects/
│   ├── projects.md                         # Project registry
│   └── [NN] - [Project Name]/
│       ├── main.md                          # Project overview and navigation
│       ├── README.md                        # Project summary
│       ├── project-plan.md                  # Phases, deliverables, and schedule
│       ├── project-metadata.json            # Project ID, archetype, mode, history
│       ├── artifacts/
│       │   ├── main.md
│       │   ├── Analysis/                    # Generated requirements, goals, and analysis outputs
│       │   │   ├── requirements.md/json     # Ingested, traceable requirements
│       │   │   ├── sanitized-requirements.md
│       │   │   └── sanitization-report.md
│       │   ├── Source Materials/            # Original requirements and other source documents
│       │   ├── Changes/                     # Change records and impact reports
│       │   ├── Sample Data/                 # Examples and sample inputs
│       │   ├── Testing/                     # Test plans and validation reports
│       │   └── Documentation/               # Supporting docs (standard/hierarchical only)
│       └── tasks/
│           ├── main.md
│           ├── README.md
│           ├── task-tracking.md
│           ├── task-template.md
│           └── T[NN]-[task-name].md         # Individual tasks, when used
└── orgModel/
    └── [NN] - [Process Name]/
        ├── main.md
        ├── process.md
        ├── collaboration.md
        ├── domain-model.md
        ├── vocabulary.md
        ├── test-case-list.md
        ├── test-cases/
        │   └── main.md
        ├── hierarchy-metadata.json          # Added when managing a hierarchy
        └── [NN]-[BoundaryName]Boundary/     # Hierarchical projects only
            ├── main.md
            ├── process.md
            ├── collaboration.md
            └── domain-model.md
```

The exact folders depend on the project archetype:

- **Flat**: project overview, `artifacts/` (without `Documentation/`), and `tasks/`; no linked `orgModel` process tree.
- **Standard**: full project artifacts and tasks, plus a process model in `OrgDocument/orgModel/` when applicable.
- **Hierarchical**: standard project structure plus boundary folders for nested process levels. Boundary documentation is generated from the collaboration model.

The former `artifacts/Requirements/` folder has been renamed to `artifacts/Source Materials/`. Keep original requirement documents and other inputs there unchanged. Put generated outputs—including `requirements.md`, `requirements.json`, `sanitized-requirements.md`, and `sanitization-report.md`—along with goals, analysis, and diagrams in `artifacts/Analysis/`. Every managed directory has a `main.md` index. When working within an EDPS project, ask skills to use these locations. Some skills document a standalone `outputs/projects/{project_id}/` default for use outside an EDPS project; the EDPS project tree takes precedence when one is specified.

## Choosing a Workflow Style

- Use a **single skill** for a focused task or when you want to control each step.
- Use the **navigator** when you know the outcome but not which skill fits.
- Use the **orchestrator** when you want a sequenced workflow with prerequisites and resumable progress. It supports standard, rapid, and compliance-focused workflows.
- Review and confirm proposed changes to existing requirements, process models, or project structures. A generated report or draft does not replace your approval.

For a new project, the project setup skill can recommend an archetype and collaboration mode. `solo` supports documented assumptions and self-attestation; `traditional` expects stakeholder confirmation. Projects predating the collaboration-mode field are treated as traditional unless explicitly changed.

## Tips

- Point to the project folder or attach the source material instead of copying large documents into a prompt.
- Ask the skill to state assumptions, unresolved questions, and files it changed.
- Keep original source files unchanged; review generated analysis before using it downstream.
- Do not invent stakeholder approvals, deadlines, estimates, or capacity when they have not been provided.
- Use the Markdown report for review and JSON outputs for downstream skills when both are generated.
- Follow each skill's guide linked above for detailed inputs, options, and output formats.
