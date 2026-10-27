---
name: project-document-management
description: Initialize and manage project documentation structures following hierarchical folder guidelines. Creates consistent project trees with requirements, artifacts, and organizational modeling documents. Supports flat (Project 1) and EDPS-hierarchical (Project 3) archetypes, an opt-in UI Prototype artifact category for UI prototyping skills, integrates with documentation-automation for stub generation, tracks project evolution metadata, and supports a solo vs. traditional collaboration mode orthogonal to archetype.
license: MIT
version: 2.3.0
last-updated: 2026-10-27
---

# Project Document Management

Creates and manages standardized EDPS project documentation structures. Supports three project archetypes, integrates with `documentation-automation` for auto-generated docs, and records project evolution metadata for compliance and change tracking.

## Intent

Bootstrap and maintain a standardised EDPS project documentation tree — creating folder hierarchies, stub template files, cross-reference structures, and `project-metadata.json` evolution records that all downstream skills depend on. Selects the correct folder layout and file templates based on the chosen **archetype**.

## Inputs

- **Project idea**: A name, a rough description, or simply what the user wants to accomplish. Ask for missing essentials in plain language; users do not need to know EDPS terminology or provide a complete specification.
- **Project number**: Determine the next unused two-digit number from `projects.md`; do not ask the user to calculate it.
- **Archetype** *(optional, default: `standard`)*: Recommend `flat`, `standard`, or `hierarchical` based on the described work and explain the difference without jargon. See [Project Archetypes](#project-archetypes).
- **Collaboration mode** *(optional, default: `solo`)*: Explain that `solo` means the user can proceed with documented assumptions, while `traditional` expects stakeholder confirmation. Recommend one based on the described project and let the user accept or change it. This is orthogonal to archetype. Existing projects whose `project-metadata.json` predates this field are read as `traditional` — never silently inferred as `solo`.
- **Initial source materials** *(optional)*: Original project documents or notes to pre-populate `artifacts/Source Materials/`
- **orgModel process name** *(optional)*: For standard or hierarchical projects, suggest a process name based on the project idea and confirm it as part of the preview; the user may accept the suggestion or provide another name. Flat projects do not need a process name.

## Outputs

- `OrgDocument/projects/[NN] - [Project Name]/` — Full project folder tree per archetype
- `main.md` in every directory created or managed by the initialization workflow
- `README.md`, `project-plan.md`, task files, and process documentation appropriate to the selected archetype
- `project-metadata.json` — Machine-readable project metadata and evolution history
- *(standard and hierarchical archetypes)* `orgModel/[NN] - [Process Name]/` tree; hierarchical boundary folders receive `documentation-automation` stubs

## `main.md` Directory Documentation Rules

Git does not track empty directories. Therefore, every directory created or managed by this skill must contain a `main.md` that describes the directory and its contents. This applies to the project root, `artifacts/` and its category folders, `tasks/`, each process folder, `test-cases/`, and every hierarchy boundary folder.

Each `main.md` must:

1. Use a heading that identifies the directory or process.
2. State the directory's purpose and the kind of material it contains in a brief overview.
3. List its immediate child directories and important files, with a short description and relative Markdown links where useful. Do not recursively duplicate their inventories.
4. Say that no content has been added yet when the directory is intentionally empty; never leave `main.md` blank or as a generation-only placeholder.
5. Keep links relative to the `main.md` file and verify that each target exists. Do not invent expected documents as though they already exist.
6. Be updated when the directory's purpose, immediate contents, or child-folder structure changes.

Use the project-root and process-root templates below for those folders; use this concise template for other directories:

```markdown
# [Directory Name]

## Purpose
[Why this directory exists and what belongs here.]

## Contents
- `[child-folder/](child-folder/main.md)` — [brief description]
- `[important-file.md](important-file.md)` — [brief description]

No content has been added yet.
```

Remove the final empty-directory sentence once content is added. Omit unavailable links and the empty-directory sentence as appropriate. For boundary folders, the initial `main.md` must be a concise, meaningful directory summary; `documentation-automation` may replace it with the full process-level overview.

## Project Archetypes

Archetypes control which folders and files are created at initialization. Specify the archetype when invoking this skill.

### `flat` — Project 1 Style
Minimal project structure: `artifacts/` with standard subfolders, `tasks/`, and core markdown files. No `orgModel` integration. Use for quick analysis projects or GitHub integration projects.

```
[NN] - [Project Name]/
├── artifacts/
│   ├── main.md
│   ├── Analysis/
│   │   └── main.md
│   ├── Source Materials/   # Original project documents and references
│   │   └── main.md
│   ├── Changes/
│   │   └── main.md
│   ├── Sample Data/
│   │   └── main.md
│   └── Testing/
│       └── main.md
├── tasks/
│   ├── main.md
│   ├── README.md
│   ├── task-tracking.md
│   └── task-template.md
├── main.md
├── project-plan.md
└── README.md
```

### `standard` — Default EDPS Style (Projects 2–3)
Full project artifacts + `orgModel` process folder with standard modeling files. Use for most EDPS skill development or requirements analysis projects.

```
[NN] - [Project Name]/
├── artifacts/
│   ├── main.md
│   ├── Analysis/
│   │   └── main.md
│   ├── Source Materials/   # Original project documents and references
│   │   └── main.md
│   ├── Changes/
│   │   └── main.md
│   ├── Documentation/
│   │   └── main.md
│   ├── Sample Data/
│   │   └── main.md
│   ├── Testing/
│   │   └── main.md
│   └── UI Prototype/       # Only when the project uses UI prototyping skills (see T01, Project 06)
│       └── main.md
├── tasks/
│   ├── main.md
│   ├── README.md
│   ├── task-tracking.md
│   └── task-template.md
├── main.md
├── project-plan.md
└── README.md

orgModel/[NN] - [Process Name]/
├── main.md
├── process.md
├── collaboration.md
├── domain-model.md
├── vocabulary.md
├── test-case-list.md
└── test-cases/
    └── main.md
```

### `hierarchical` — EDPS Boundary-First Style (Project 3+)
All `standard` content plus `orgModel` folders using the `[NN]-[Name]Boundary/` hierarchy pattern. Each boundary sub-folder receives a meaningful `main.md` summary and `documentation-automation` stubs for its remaining process documents. Use when designing multi-level EDPS process hierarchies.

```
orgModel/[NN] - [Process Name]/
├── main.md
├── process.md
├── collaboration.md               ← defines boundary sub-folders
├── domain-model.md
├── vocabulary.md
├── test-case-list.md
├── test-cases/
│   └── main.md
├── hierarchy-metadata.json        ← created by hierarchy-management
└── [NN]-[BoundaryName]Boundary/   ← one per control-type participant
    ├── main.md                    ← concise directory summary, then expanded by documentation-automation
    ├── process.md                 ← [TO BE GENERATED - invoke documentation-automation]
    ├── collaboration.md           ← [TO BE GENERATED - invoke documentation-automation]
    └── domain-model.md            ← [TO BE GENERATED - invoke documentation-automation]
```

**Important**: Boundary sub-folder files are initialised as stubs. After creating each boundary folder, invoke `documentation-automation` to replace stubs with generated content based on `collaboration.md`.

## Usage Scenarios

1. **New Project Initialization**: Create complete folder structure for a greenfield project (specify archetype)
2. **orgModel Process Initialization**: Set up a new top-level or sub-process folder within an existing project
3. **Project Migration**: Restructure an existing flat project to standard or hierarchical layout
4. **Structure Validation**: Verify a project follows documentation guidelines and flag missing elements
5. **Iterative Update**: Add folders or update stubs in an existing project following EDPS evolutionary principles
6. **Template Refresh**: Regenerate template files to the current version without overwriting substantive content

## Project Initialization Workflow

### Guided, Interactive Intake

Do not present initialization as a form the user must already know how to fill out. Start from whatever they provided, including an incomplete idea, and guide them through only the decisions needed to create a useful first version. When the `ask_user` tool is available, use it for focused clarification and confirmation questions; phrase them in everyday language and include a recommended answer where helpful. Otherwise, ask naturally in chat.

1. Read `projects.md` and inspect the existing project folders before proposing a project number or name. Choose the next unused two-digit number yourself; if there is a numbering conflict, resolve it before writing.
2. If the project idea or goal is unclear, ask one short, plain-language question about what they want to achieve. If a useful name is missing, offer a concise name based on their answer and let them change it. Do not ask them for a project ID, folder path, metadata, or template details.
3. Recommend an archetype in everyday language:
   - `flat`: a lightweight project that needs analysis and task folders, but no organizational process model.
   - `standard`: the recommended starting point when the work benefits from a process model and full EDPS documentation.
   - `hierarchical`: use when the user already knows the work needs multiple nested process levels and boundaries.
   Explain the recommendation briefly and allow the user to accept it or choose another. If the user is unsure, use `standard`.
4. Explain collaboration mode briefly: `solo` allows documented assumptions and self-attestation; `traditional` is for work requiring stakeholder confirmation. Recommend `solo` for a new project unless the user describes a team or approval process that calls for `traditional`. The creation-time default is `solo`; never apply this default when reading legacy metadata.
5. For standard or hierarchical projects, suggest a clear process name from the project idea. Explain that it can be refined later; do not make the user invent EDPS naming conventions. Flat projects do not need an orgModel process.
6. Reuse any requirements, notes, or attached materials already available. Ask about source materials only if their absence blocks the requested setup; do not make a complete requirements document a prerequisite.
7. Before creating files, show a compact preview in familiar terms (project name, purpose, recommended structure, collaboration mode, and process model if applicable) and ask for confirmation. If a key choice remains unresolved, ask a focused question and update the preview. Do not require answers to optional planning fields such as stakeholders, dates, success measures, or detailed requirements; record these as to-be-defined and help the user fill them in after initialization.
8. Once confirmed, continue through the initialization steps below without asking the user to supply internal identifiers or repeat information already provided. If the user explicitly asks to proceed without a preview, honor that and use the stated defaults.

When the user has already provided enough information and a clear confirmation to create the project, avoid redundant questions: infer the project number and description, apply the defaults, and proceed.

### Step 1 — Confirm Choices and Determine Parameters

1. Use the confirmed project name and description; derive a concise description from the user's idea if needed.
2. Use the next unused project number from `projects.md`, then verify it is not already in use.
3. Use the confirmed archetype and collaboration mode, or their documented recommendations/defaults if the user is unsure.
4. For standard or hierarchical projects, use the confirmed process name or a suggested name the user accepted.

### Step 2 — Create Project Folder Tree

Create the folder structure for the selected archetype (see [Project Archetypes](#project-archetypes)). Always create the following core folders; include `Documentation/` under `artifacts/` only for standard and hierarchical projects; include `UI Prototype/` under `artifacts/` only when the project will use the UI Prototyping skill set (see Integration Points — `screen-generateinventory` and related skills):

```
OrgDocument/projects/[NN] - [Project Name]/
├── artifacts/
│   ├── main.md
│   ├── Analysis/main.md
│   ├── Source Materials/main.md
│   ├── Changes/main.md
│   ├── Documentation/main.md       ← standard + hierarchical only
│   ├── Sample Data/main.md
│   ├── Testing/main.md
│   └── UI Prototype/main.md        ← only when UI prototyping skills are in use
├── tasks/
│   ├── main.md
│   ├── README.md
│   ├── task-tracking.md
│   └── task-template.md
├── main.md
├── project-plan.md
├── README.md
└── project-metadata.json
```

### Step 3 — Write project-metadata.json

Create `project-metadata.json` in the project root:

```json
{
  "project_id": "PRJ-[NN]",
  "project_name": "[Project Name]",
  "project_number": "[NN]",
  "archetype": "[flat|standard|hierarchical]",
  "collaboration_mode": "[solo|traditional]",
  "created": "[ISO-8601 date]",
  "last_updated": "[ISO-8601 date]",
  "status": "Initialized",
  "version": "1.0.0",
  "evolution_history": [
    {
      "version": "1.0.0",
      "date": "[ISO-8601 date]",
      "change": "Initial project structure created",
      "archetype": "[archetype]",
      "collaboration_mode": "[solo|traditional]",
      "changed_by": "project-document-management"
    }
  ],
  "linked_orgmodel": "[OrgDocument/orgModel/NN - Process Name]  or null",
  "skills_used": []
}
```

If `collaboration_mode` is not specified by the caller, default to `"solo"` for a brand-new project (see T01's default-mode rule). This default applies only at **creation time** — it is never inferred for an existing project that is missing the field; see [Reading Legacy Metadata](#reading-legacy-metadata-collaboration_mode) below.

Update `evolution_history` with a new entry every time the project structure is modified by this skill.

### Reading Legacy Metadata (`collaboration_mode`)

When this skill (or any downstream skill) reads `project-metadata.json` and the `collaboration_mode` field is absent, treat the project as `"traditional"` for all purposes — do not write the field in automatically and do not treat its absence as `"solo"`. This preserves the safe-default rule from `collaboration-mode-reference.md`: a project that predates this feature keeps its original (stricter) stakeholder-confirmation behavior until someone explicitly runs **Change Collaboration Mode** below.

### Step 4 — Update Project Registry

Add row to `OrgDocument/projects/projects.md`:

```markdown
| [NN] | [Project Name] | [Brief description] | Initialized | [Date] |
```

### Step 5 — Initialize orgModel Process Tree (standard and hierarchical archetypes)

If `orgModel process name` was provided or archetype requires it:

```
OrgDocument/orgModel/[NN] - [Process Name]/
├── main.md
├── process.md
├── collaboration.md
├── domain-model.md
├── vocabulary.md
├── test-case-list.md
└── test-cases/
    ├── main.md
    └── tc-[identifier]-[3-digit-sequence].md
```

**File initialization rules**:
- `main.md`, `process.md`, `collaboration.md`, `domain-model.md` → write with the standard EDPS templates (see below); `main.md` must also summarize the process folder's purpose and contents
- `vocabulary.md`, `test-case-list.md` → write empty stubs with heading only; `orgmodel-update` owns their content
- `test-cases/main.md` → describe the folder's purpose and explain that individual test cases belong there

### Step 6 — Initialize Boundary Sub-folders (hierarchical archetype only)

For each `control`-type participant identified in the top-level `collaboration.md`, create a boundary sub-folder:

```
orgModel/[NN] - [Process Name]/
└── [NN]-[BoundaryName]Boundary/
    ├── main.md          ← create a meaningful directory summary; documentation-automation expands it
    ├── process.md       ← insert stub: [TO BE GENERATED - invoke documentation-automation]
    ├── collaboration.md ← insert stub: [TO BE GENERATED - invoke documentation-automation]
    └── domain-model.md  ← insert stub: [TO BE GENERATED - invoke documentation-automation]
```

After creating each boundary folder, **invoke `documentation-automation`** to replace the process-document stubs and expand `main.md` into the generated process overview. This skill does not generate the detailed process documentation itself.

**Invocation pattern**:
```
[After creating boundary folder] → invoke documentation-automation for [process-folder]/[NN]-[Name]Boundary/
```

## Iterative Update Workflow

Use this workflow when evolving an **existing** project structure to add EDPS methodology support or upgrade an archetype.

### Detect Current State
1. Read `project-metadata.json` to determine current `archetype` and `version`.
2. If `project-metadata.json` is missing → treat as legacy project, infer archetype from folder structure.

### Upgrade Archetype
| From → To | Actions |
|-----------|---------|
| `flat` → `standard` | Add `Documentation/` to artifacts; create `orgModel/[NN] - [Process Name]/` tree if process name provided |
| `flat` → `hierarchical` | All standard actions plus boundary sub-folder stubs |
| `standard` → `hierarchical` | Add boundary sub-folder stubs for `control`-type participants in existing `collaboration.md` |

### Add Missing Files
For every directory in the managed project/process tree, create a `main.md` if it is absent and summarize the directory based on its actual contents. Do **not** overwrite files that already contain substantive content (line count > 10 non-placeholder lines). Create other expected files as stubs when absent.

### Record Evolution
After every update, append a new entry to `evolution_history` in `project-metadata.json` and increment the `version` field (patch increment for file additions, minor for archetype upgrades).

## Standard File Templates

### Non-root Directory `main.md` Template
Use the directory documentation rules above for every generated folder that does not use the project-root or process-root template. Keep the contents list limited to immediate children and important files.

### Project main.md Template
```markdown
<!-- Identifier: PRJ-[NN] -->

# [NN] - [Project Name]

## Overview
[Brief project description and objectives]

**Archetype**: [flat|standard|hierarchical]  
**Collaboration Mode**: [Solo | Traditional]  
**Status**: Initialized — Awaiting Requirements  
**Created**: [Date]  

## Structure
- [`artifacts/main.md`](artifacts/main.md) — Index of supporting materials and analysis outputs
- [`tasks/main.md`](tasks/main.md) — Index of individual task files and tracking documents

## Key Documents
- [`project-plan.md`](project-plan.md) — Detailed project planning and timeline
- [`README.md`](README.md) — Project summary and quick reference
- [`tasks/README.md`](tasks/README.md) — Task overview and tracking
- [`artifacts/Source Materials/main.md`](artifacts/Source%20Materials/main.md) — Original project documents, transcripts, references, and drafts
- [`../../orgModel/[NN] - [Process Name]/main.md`](../../orgModel/[NN]%20-%20[Process%20Name]/main.md) — Linked organizational process model

## Dependencies
- [List of project dependencies]

## Success Criteria
[To be defined based on requirements]

## Timeline
[To be defined in project-plan.md]

---
**Project Status**: Initialized — Awaiting Requirements  
**Last Updated**: [Date]  
**Next Steps**: Provide requirements input and conduct initial analysis
```

When generating this template, resolve `[Solo | Traditional]` from the project's actual `collaboration_mode` (default `Solo` for a new project). See `collaboration-mode-reference.md` (published under Iteration 4's `artifacts/Documentation/`) for the full definitions of each mode; do not hardcode a link to it here since its path is specific to one project, not a shared location.

### Process main.md Template (standard / hierarchical archetypes)
```markdown
# [NN] - [Process Name]

**Level**: [0 | 1 | 2 | …]  
**Parent Process**: [Parent process name or Root]  
**Archetype**: [standard|hierarchical]  
**Last Updated**: [Date]  

## Business Model Overview
[Description of the business model at this process level]

## Requirements Source
[Overview of requirements driving this process level]

## Process Scope
[Specific scope and boundaries for this process granularity]

## Business Context
[Business context and rationale for this process level]

## Key Stakeholders
[Primary stakeholders involved at this process level]

## Process Flow
See [process.md](process.md) for detailed activity diagram.

## Collaborations
See [collaboration.md](collaboration.md) for entity interactions.

## Domain Model
See [domain-model.md](domain-model.md) for actors and entities.

## Sub-Processes
[List of boundary sub-folder links — e.g., [01-OrderServiceBoundary](01-OrderServiceBoundary/main.md)]

## Test Coverage
See [test-case-list.md](test-case-list.md) for verification test cases.

## Folder Contents
- [`test-cases/main.md`](test-cases/main.md) — Purpose and contents of the individual test-case folder.
```

### Boundary Sub-folder Stub Template (hierarchical archetype)
Use the standard directory `main.md` template for `main.md` so the folder is searchable immediately. The following placeholder is inserted into the other generated files in a new boundary sub-folder. `documentation-automation` replaces these stubs with real content.

```markdown
[TO BE GENERATED - invoke documentation-automation]
```

### project-plan.md Template
```markdown
# Project Plan — [NN] - [Project Name]

**Project ID**: PRJ-[NN]  
**Archetype**: [flat|standard|hierarchical]  
**Start Date**: [Date]  
**Target Completion**: [Date]  
**Status**: Planning Phase — Awaiting Requirements  

## Executive Summary
[To be defined]

## Project Phases

### Phase 0: Requirements Analysis and Planning
**Duration**: [TBD]  
**Deliverables**: Requirements doc, Technical analysis, Task breakdown

### Phase 1: [To be defined]
**Deliverables**: [TBD]

### Phase 4: Integration and Testing
**Deliverables**: Integration testing, Documentation updates, Deployment

## Risk Management
[To be updated as risks are identified]
```

## Quick Commands

### Initialize New Project
**Parameters**: Project idea or name (required); derive `project_number` from `projects.md`; `description`, `archetype` (default: `standard`), `collaboration_mode` (default: `solo`), and `orgmodel_process_name` (suggest one for standard/hierarchical projects) may be inferred or confirmed interactively.
**Actions**:
1. Read `projects.md` and propose the next unused project number; do not require the user to supply it
2. Guide the user through the project name/goal and explain any archetype or collaboration-mode choices in plain language; recommend sensible defaults for unknowns
3. Preview the proposed setup and get confirmation before creating files, unless the user has already clearly confirmed or asked to proceed directly
4. Create project folder with archetype-appropriate subfolder structure
5. Write `project-metadata.json` (version `1.0.0`), including `collaboration_mode`
6. Generate the project-root `main.md`, `README.md`, and `project-plan.md` from templates, stating the active collaboration mode plainly in `main.md`
7. Create `main.md` indexes in `artifacts/`, each artifact category, and `tasks/`
8. Create `tasks/` with `README.md`, `task-tracking.md`, and `task-template.md`
9. Update `projects.md` registry
10. *(standard/hierarchical)* Create `orgModel/[NN] - [Process Name]/` tree and `test-cases/main.md`
11. *(hierarchical)* Create boundary-folder summaries and process-document stubs; invoke `documentation-automation` per boundary folder

### Initialize Process Model
**Parameters**: `process_number`, `process_name`, `scope_description`, `archetype` (default: `standard`)  
**Actions**:
1. Create `orgModel/[NN] - [Process Name]/` folder
2. Generate `main.md`, `process.md`, `collaboration.md`, `domain-model.md` from templates
3. Create `vocabulary.md`, `test-case-list.md` stubs (content owned by `orgmodel-update`)
4. Create `test-cases/` folder with a descriptive `main.md`
5. *(hierarchical)* Create boundary sub-folder stubs and invoke `documentation-automation`
6. Update parent `main.md` sub-process list

### Upgrade Archetype
**Parameters**: `project_number`, `target_archetype`  
**Actions**:
1. Read `project-metadata.json` to determine current archetype
2. Apply incremental changes per upgrade path table
3. Increment version in `project-metadata.json` (minor bump for archetype upgrade)
4. Append entry to `evolution_history`

### Change Collaboration Mode
**Parameters**: `project_number`, `target_mode` (`solo` | `traditional`), `reason` (required free-text justification)  
**Actions**:
1. Read `project-metadata.json`; if `collaboration_mode` is absent, treat current mode as `traditional` for the purposes of recording the "from" state
2. Validate `target_mode` is one of `solo` or `traditional`; reject otherwise
3. Set `collaboration_mode` to `target_mode`
4. Append an `evolution_history` entry recording `from_mode`, `to_mode`, `reason`, and timestamp (patch version bump — this is a metadata-only change, not a structural one)
5. State plainly in the response that the mode change is **not retroactive**: gate evaluations and self-attestations already recorded under the prior mode remain valid as-is; only evaluations performed after this change follow the new mode's rules (per `collaboration-mode-reference.md`)
6. If the project's `main.md`/`README.md` state the active mode (see Step 3 and templates below), update that text too so it never goes stale

This operation never touches folder structure, archetype, or any other metadata field.

### Structure Validation
**Actions**:
1. Verify folder naming conventions (`[NN] - [Name]` for projects; `[NN]-[Name]Boundary` for hierarchy nodes)
2. Check that every directory in the managed tree contains a non-empty `main.md` with a purpose and an accurate immediate-contents summary
3. Check expected archetype-specific files and folders
4. Validate `project-metadata.json` presence and schema
5. Validate cross-reference links in every `main.md` resolve to existing files or directories
6. Detect stub files not yet replaced by `documentation-automation`
7. Report: ✅ valid | ⚠️ missing files | ❌ broken links | 🔲 ungenerated stubs

## Naming Conventions

### Folders
- Projects: `[NN] - [Project Name]` (e.g., "01 - Customer Portal")
- Processes: `[NN] - [Process Name]` (e.g., "02 - User Authentication")
- Artifacts: Descriptive names without numbering (e.g., "Analysis", "UI Mockups")

### Files  
- Main documentation: `main.md`
- Process diagrams: `process.md`  
- Collaboration diagrams: `collaboration.md`
- Domain models: `domain-model.md`
- Vocabulary: `vocabulary.md`
- Test case lists: `test-case-list.md`
- Individual test cases: `tc-[identifier]-[3-digit-sequence].md`

## Naming Conventions

### Folders
- Projects: `[NN] - [Project Name]` (e.g., `03 - Building Skills Iteration 2`)
- Standard process nodes: `[NN] - [Process Name]` (e.g., `01 - Skill Development Process`)
- Hierarchical boundary nodes: `[NN]-[NamePascalCase]Boundary` (e.g., `01-OrderServiceBoundary`)
- Artifacts: Descriptive names without numbering (e.g., `Analysis`, `Testing`)

### Files
- Main documentation: `main.md`
- Process diagrams: `process.md`
- Collaboration diagrams: `collaboration.md`
- Domain models: `domain-model.md`
- Vocabulary: `vocabulary.md`
- Test case lists: `test-case-list.md`
- Individual test cases: `tc-[identifier]-[3-digit-sequence].md`
- Hierarchy metadata: `hierarchy-metadata.json` *(created by `hierarchy-management`)*
- Project metadata: `project-metadata.json` *(created by this skill)*

## Integration Points

### `documentation-automation` *(primary downstream)*
- **Trigger**: After this skill creates any boundary sub-folder (hierarchical archetype)
- **Input it provides**: Stub files containing `[TO BE GENERATED - invoke documentation-automation]`
- **Output it receives**: Fully generated `main.md`, `process.md`, `collaboration.md`, `domain-model.md`
- **Ordering rule**: This skill creates the folder structure → `documentation-automation` fills the content

### `hierarchy-management`
- **Coordination**: `hierarchy-management` creates `hierarchy-metadata.json` and boundary sub-folders when decomposing control-type participants. This skill creates the initial top-level process tree; `hierarchy-management` extends it downward.
- **Conflict avoidance**: Do not create `[NN]-[Name]Boundary/` folders if `hierarchy-management` will do so based on `collaboration.md` decomposition.

### `orgmodel-update`
- **Files owned by `orgmodel-update`**: `vocabulary.md`, `test-case-list.md` — initialize as empty stubs only; never overwrite content in these files.
- **Files owned by this skill**: project and artifact-directory `main.md` files, `project-plan.md`, `README.md`, `project-metadata.json`. Process-folder `main.md` is authored from the process template; hierarchy boundary `main.md` is expanded by `documentation-automation`.

### `requirements-ingest`
- Read original requirement sources from `artifacts/Source Materials/` and write generated `requirements.md` and `requirements.json` to `artifacts/Analysis/`.
- Keep original source files unchanged in `artifacts/Source Materials/`; generated and transformed analysis outputs belong in `artifacts/Analysis/`.

### UI Prototyping skill set *(`screen-generateinventory` and related skills, planned — Project 06)*
- **Trigger**: When a project's requirements/goals call for generating UI prototypes (screen inventories, layout specs, interactive mockups) discussable with stakeholders
- **Folder dependency**: These skills write to `artifacts/UI Prototype/`, a category this skill introduces but does not populate — create the empty `main.md`-only folder at init time (Step 2) or via the Iterative Update Workflow's "Add Missing Files" path for existing projects; the UI Prototyping skills themselves own everything written inside it
- **Ordering rule**: This skill creates the folder → UI Prototyping skills fill the content, the same ordering convention used for `documentation-automation` and `orgmodel-update` below
- **Non-standard categories are opt-in**: Unlike `Documentation/` (tied to archetype), `UI Prototype/` is tied to whether the project actually uses these skills, not to archetype alone — do not create it by default for every standard/hierarchical project

### `goals-extract`
- Output can seed the `## Success Criteria` section of `main.md` after project initialization.

### `edps-workflow-orchestrator` *(planned — T07)*
- `project-metadata.json` `skills_used` array is updated by the orchestrator to track which skills have been invoked against this project.

## Best Practices

1. **Make first-time setup approachable**: Start from the user's rough idea, explain recommendations plainly, and leave optional details to be refined later.
2. **Consistent numbering**: Use sequential NN for projects and process nodes; do not reuse numbers.
3. **project-metadata.json is the source of truth**: Always read it before modifying a project structure.
4. **Never leave a folder undocumented**: Create a useful `main.md` in every managed directory, even when the directory has no other content.
5. **Registry updates are mandatory**: Always update `projects.md` when creating a new project folder.
6. **Never skip documentation-automation**: After creating boundary sub-folders (hierarchical archetype), immediately invoke `documentation-automation` to convert stubs.
7. **Record every structural change**: Append to `evolution_history` in `project-metadata.json` for every modification — required for EDPS compliance.
8. **Never infer `collaboration_mode`**: If `project-metadata.json` lacks the field, treat the project as `traditional`. Only an explicit **Change Collaboration Mode** action may change it — never a side effect of another operation.