---
name: hierarchy-management
description: Manage hierarchical process decomposition in EDPS collaboration diagrams. Decomposes control-type participants into Level N+1 sub-processes with their own collaboration diagrams, tracks parent-child relationships across unlimited hierarchy depth, manages the folder structure, and maintains hierarchy metadata. Use when a user wants to decompose a participant into a sub-process, navigate a process hierarchy, roll back a decomposition, view hierarchy statistics, or generate a hierarchy tree visualization.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-16"
---

# Hierarchy Management

Decompose control-type participants into sub-process diagrams and manage the full hierarchy tree across EDPS collaboration models.

## Intent

Decompose `control`-type participants into Level N+1 sub-process diagrams, manage the full EDPS hierarchy tree across unlimited decomposition depth, create and maintain folder structures, generate stub documentation files, update parent navigation links, and track hierarchy metadata. Also exposes a `--op migrate` mode that non-destructively upgrades pre-Project 3 flat diagrams to boundary-annotated format (absorbing the `migration-tools` skill).

## Inputs

- **Parent diagram**: `[process-folder]/collaboration.md` — the diagram containing the participant to decompose
- **Target participant**: name of the control-type participant to decompose
- **Optional**: `[process-folder]/hierarchy-metadata.json` — existing hierarchy metadata

## Outputs

- `[process-folder]/[NN]-[ParticipantName]Boundary/collaboration.md` — new Level N+1 diagram
- `[process-folder]/[NN]-[ParticipantName]Boundary/main.md` — sub-process overview with parent/child navigation links, now including a `## System Boundary` section (see below)
- `[process-folder]/[NN]-[ParticipantName]Boundary/process.md` — activity/workflow diagram for the sub-process
- `[process-folder]/[NN]-[ParticipantName]Boundary/domain-model.md` — class diagram with entities and relationships
- `[process-folder]/hierarchy-metadata.json` — updated hierarchy metadata (created if absent)
- `[process-folder]/folder-creation.log` — audit log appended with each sub-folder created
- Updated navigation links in parent `main.md` and `collaboration.md`

### System Boundary Declaration

Every boundary folder this skill creates corresponds to a [System Boundary Reference](../model-validatealignment/references/cross-model-alignment-contract.md#12-system-boundary-reference) in the shared cross-model alignment contract. This skill is responsible for the **structural** fields of that reference (`boundary_id`, `hierarchy_level`, `hierarchy_path`, `parent_boundary_id`, `corresponds_to_participant`) — all derivable from the decomposition itself and written automatically into the new `main.md`'s `## System Boundary` section.

**`boundary_type` is explicitly NOT auto-populated by this skill.** Per the contract's Section 2.1, `boundary_type` (`software`/`non-software`/`unknown`) must be an explicit, human-confirmed classification — never inferred from the fact that a participant was `control`-type and decomposable (HV-1 eligibility is a diagram-structure concern, orthogonal to real-world software status). This skill writes the `## System Boundary` section with `boundary_type` left as `unknown` and a visible prompt for the user/developer to confirm it, mirroring the existing stub-file discipline (`[TO BE GENERATED - invoke documentation-automation]`) for a different, non-bypassable reason: this field cannot be safely auto-filled by any downstream skill either. `usecase-generatemodel`/`ui-generatemodel` (PRJ-07) will refuse to run against a boundary whose `main.md` still shows `unknown` here — see their own Step 0.

The section's exact text is part of the `main.md` stub in [references/stub-files.md](references/stub-files.md).

This section is additive to the existing stub specification below — it does not replace or change any other stub content, and it is **not** gated behind the `[TO BE GENERATED - invoke documentation-automation]` Content Guard marker, since `boundary_type` confirmation is a decision for the user/developer, not generated content `documentation-automation` can produce from the collaboration diagram.

## Workflow

### 1. Validate Decomposition Eligibility

Before creating anything:

1. Read the parent `collaboration.md`
2. Identify the target participant's stereotype from the `%% Stereotypes:` comment
3. **If type ≠ `control`** → stop and return:

```json
{
  "error": "control-only-decomposition",
  "participant": "[Name]",
  "type": "[actual-type]",
  "message": "Only control-type participants can be decomposed into sub-processes.",
  "suggestion": "If this participant requires internal detail, consider reclassifying it as 'control', or model its internals as a separate diagram rather than a process decomposition."
}
```

4. Check whether a sub-folder for this participant already exists (decomposition already performed) → warn the user and offer to update instead

### 2. Determine Level and Folder Name

- Detect the current level by inspecting `hierarchy-metadata.json` at the parent level (or counting parent folder depth)
- Assign a two-digit ordinal prefix: count existing sub-folders in the parent directory and increment (e.g., `01`, `02`, `03`)
- Folder name pattern: `[NN]-[ParticipantNamePascalCase]Boundary`

Example: decomposing `OrderService` at Level 1 → `01-OrderServiceBoundary/`

#### 2a. Special Character Sanitization

Before building the folder name, sanitize the participant name:

| Rule | Input Example | Sanitized Output |
|------|--------------|-----------------|
| Remove spaces (PascalCase join) | `Order Service` | `OrderService` |
| Remove or replace `/` `\` `:` `*` `?` `"` `<` `>` `\|` | `Order/Service` | `OrderService` |
| Remove leading/trailing hyphens and dots | `.OrderService.` | `OrderService` |
| Collapse consecutive non-alphanumeric sequences to single hyphen | `Order--Service` | `OrderService` |
| Preserve existing PascalCase casing | `OrderServiceBoundary` | `OrderServiceBoundary` |

The final folder name must match the regex `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`.

#### 2b. Naming Collision Resolution

Before creating the folder, check whether `[NN]-[ParticipantName]Boundary/` already exists **in the same parent directory**:

1. **Exact match exists** (same ordinal + same name): the decomposition was already performed.
   - Stop and ask the user: "Sub-folder `[NN]-[ParticipantName]Boundary/` already exists. Do you want to (a) skip creation and reuse the existing folder, (b) overwrite its generated files, or (c) cancel?"
2. **Name match but different ordinal** (e.g., user renamed the folder): treat as a new decomposition — assign the next available ordinal.
3. **Ordinal conflict only** (different name, same number): increment the proposed ordinal until a free slot is found.

### 3. Write the Four Stub Files

Create `main.md`, `process.md`, `collaboration.md`, and `domain-model.md` in the new folder, each exactly as given in [references/stub-files.md](references/stub-files.md).

- These are **stubs only**: syntactically valid Markdown and Mermaid with no process content. Do not populate participants, messages, flowchart steps, or classes here. `documentation-automation` generates the content and replaces the stubs.
- Every stub contains the exact marker `[TO BE GENERATED - invoke documentation-automation]`, which is how `documentation-automation` tells a stub from a generated file.
- In `main.md`, fill in the structural fields of the `## System Boundary` section and leave `Boundary Type` as `unknown` with its action-required note.
- Stubs satisfy `hierarchy-validation` rule HN-2 (required files present) as soon as they are written.

### 4. Append the Folder Creation Audit Log

After all files are written, **append** a log entry to `[process-folder]/folder-creation.log` (create if absent):

```
[ISO-8601 timestamp] CREATED  [NN]-[ParticipantName]Boundary/
  Level:      [N+1]
  Parent:     [ParentProcessName] ([process-folder]/)
  Files:      collaboration.md, main.md, process.md, domain-model.md
  Decomposed: [ParticipantName] (type: control)
  Ordinal:    [NN] (sibling count before: [count])
```

If a collision was resolved (see §2b), also append:
```
  Collision:  resolved — [description of resolution]
```

> **Post-Creation Reminder**: After folder creation completes, invoke `documentation-automation` with this folder as the target to generate content-complete documents. The stub files created in Step 3 will be replaced with fully populated `collaboration.md`, `main.md`, `process.md`, and `domain-model.md`.

### 5. Update Parent Navigation

Add a **Sub-Processes** section (or entry) to:

1. Parent `main.md` — add a link to the new sub-folder's `main.md` (including process and domain-model links):

```markdown
## Sub-Processes

| Sub-Process | Collaboration | Process Flow | Domain Model |
|-------------|--------------|--------------|-------------|
| [[NN]-[ParticipantName]Boundary]([NN]-[ParticipantName]Boundary/main.md) | [diagram]([NN]-[ParticipantName]Boundary/collaboration.md) | [flow]([NN]-[ParticipantName]Boundary/process.md) | [model]([NN]-[ParticipantName]Boundary/domain-model.md) |
```

2. Parent `collaboration.md` — add a `decomposition` comment after the participant declaration:

```
%% Decomposition: [ParticipantName] → [NN]-[ParticipantName]Boundary/collaboration.md
```

### 6. Update `hierarchy-metadata.json`

Read existing metadata (create if absent) and add an entry for the new sub-process.  
See [references/hierarchy-metadata-schema.md](references/hierarchy-metadata-schema.md) for schema details.

Key fields to set/update:
- `nodes.[id].status` of the parent participant → `"decomposed"`
- Add a new node entry for the new sub-process
- Update `hierarchy_statistics` (depth, breadth, leaf count, boundary count)
- Run **Process Level Tracking and Scale Management** analysis on the newly created `collaboration.md` and populate `complexity_metrics` for all control-type nodes in the new diagram; recompute `hierarchy_statistics.scale_management`

### 7. Cross-Reference Navigation Maintenance

After writing the files and updating the parent, make a pass over the navigation links:

- **7a. Parent to child**: the parent `main.md` has one `## Sub-Processes` table row per sub-folder, sorted by ordinal, with relative paths.
- **7b. Child to parent**: each child `main.md` has a resolving **Parent Process** link, a breadcrumb matching its real folder depth, and the correct level number.
- **7c. Link integrity**: every link in `## Navigation` and `## Sub-Processes` across the tree resolves; report broken links and offer to repair those caused by a rename or move, logging each repair in `folder-creation.log`.
- **7d. After a rollback**: the parent's table row for the removed sub-process is gone.

The full procedures, the breadcrumb construction rules, rebuilding navigation for an existing tree, the root-level `hierarchy-index.md`, and the hierarchy tree visualization are in [references/navigation.md](references/navigation.md).

## Decomposition Rollback

When the user requests a rollback of a decomposition:

1. Remove the sub-folder and its contents (`collaboration.md`, `main.md`, `process.md`, `domain-model.md`, `hierarchy-metadata.json`) (ask for confirmation first)
2. Revert parent participant's `status` in `hierarchy-metadata.json` to `"available"`
3. Remove the `%% Decomposition:` comment from parent `collaboration.md`
4. Remove the sub-process navigation link row from parent `main.md`'s Sub-Processes table
5. Remove the node from `hierarchy-metadata.json`
6. Append a `REMOVED` entry to `folder-creation.log`:
   ```
   [ISO-8601 timestamp] REMOVED  [NN]-[ParticipantName]Boundary/
     Reason:   user-requested rollback
     Restored: [ParticipantName] status → available
   ```
7. Report: participant name, folder removed, parent updated

## Process Level Tracking and Scale Management

After every decomposition, and on request, measure each diagram's complexity (participant, message, and control counts against configurable thresholds), raise warnings for diagrams that have grown too large, identify which control participants are decomposition candidates, and keep `hierarchy_statistics` (depth, breadth, leaf and boundary counts) current in `hierarchy-metadata.json`.

Thresholds, the metric calculations, warning levels, the candidate-identification rules, and the statistics report are in [references/scale-management.md](references/scale-management.md).

## Multi-Level Deep Decomposition

When decomposing a participant that is already at Level 2 or deeper, apply the same workflow — there is no maximum depth. Each level's folder nests inside the parent folder:

```
[ProcessRoot]/
├── main.md
├── collaboration.md
├── process.md
├── domain-model.md
├── hierarchy-metadata.json
├── folder-creation.log
└── 01-ServiceABoundary/
    ├── main.md
    ├── collaboration.md
    ├── process.md
    ├── domain-model.md
    ├── hierarchy-metadata.json
    └── 01-LogicEngineBoundary/
        ├── main.md
        ├── collaboration.md
        ├── process.md
        ├── domain-model.md
        └── hierarchy-metadata.json
```

Each folder maintains its **own** `hierarchy-metadata.json` scoped to that sub-tree, while the root's metadata covers the full tree.

---

## Migrate Operation Mode (`--op migrate`)

This operation mode absorbs the functionality of the `migration-tools` skill (retained for backward compatibility). Use `--op migrate` to non-destructively upgrade pre-Project 3 flat (Project 1 style) `collaboration-diagrams.md` / `collaboration-diagrams.json` files to the boundary-annotated (Project 3 style) format.

### Invocation

```
hierarchy-management --op migrate
  [--scope batch|diagram=<diagram-id>]
  [--mode preview|apply]
  [project-folder]/artifacts/Analysis/collaboration-diagrams.md
```

| Flag | Default | Description |
|------|---------|-------------|
| `--scope batch` | `batch` | Migrate all diagrams in the file |
| `--scope diagram=<id>` | — | Migrate a single diagram by ID |
| `--mode preview` | `preview` | Show proposed changes without writing files |
| `--mode apply` | — | Write enhanced counterpart files |

### What it Does

1. **Load** `collaboration-diagrams.md` and/or `collaboration-diagrams.json`.
2. **Classify** each participant using stereotype-classification rules from `diagram-generatecollaboration` (actor / boundary / control / entity heuristics).
3. **Detect** logical boundary groups from message patterns and participant names.
4. **Emit enhanced variants** with box annotations following Project 3 syntax:
   - `box [BoundaryName]` … `end` wrapping
   - `@{ "type": "[stereotype]", "label": "..." }` participant annotations
5. **Write** output to `*-enhanced.md` / `*-enhanced.json` counterparts (originals **never modified**).
6. **Write** `migration-log.md` summarising per-diagram changes, boundary inferences, and any warnings.

### Non-Destructive Guarantee

Original `collaboration-diagrams.md` and `collaboration-diagrams.json` are **never modified**. All changes are written to the `*-enhanced.*` counterparts.

### After Migration

Once migration is complete, run `diagram-generatecollaboration` boundary validation on the enhanced files, then proceed with `hierarchy-management --op decompose` to start creating Level N+1 sub-processes from the upgraded diagrams.

## References

- **[Hierarchy Metadata Schema](references/hierarchy-metadata-schema.md)** — JSON schema for `hierarchy-metadata.json`, field definitions, and example document
- **[Decomposition Patterns](references/decomposition-patterns.md)** — Participant inference heuristics, multi-boundary patterns, and worked examples at each hierarchy level
- [references/stub-files.md](references/stub-files.md) — the four stub file templates
- [references/navigation.md](references/navigation.md) — breadcrumbs, link maintenance, hierarchy index, tree visualization
- [references/scale-management.md](references/scale-management.md) — complexity metrics, thresholds, statistics

## Completion Gate

```bash
python3 .github/skills/edps-workflow-orchestrator/scripts/run_gate.py hierarchy-management \
    --project "OrgDocument/projects/[NN] - [Project Name]" \
    --process "OrgDocument/orgModel/[NN] - [Process Name]"
```
