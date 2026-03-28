# T20: Resolve C-3 — File Generation Ownership Contract

**Task ID**: T20  
**Phase**: Phase 3.5 - Conflict Resolution  
**Priority**: Medium  
**Estimated Effort**: 1 day  
**Status**: Completed (Tested — 5/5 PASS)  
**Assigned**: [Team Member]  
**Created**: March 14, 2026  
**Last Updated**: March 15, 2026

## Description

During architectural review, `hierarchy-management` and `documentation-automation` were found to write the same four files (`main.md`, `process.md`, `collaboration.md`, `domain-model.md`) for every sub-process folder. No contract exists specifying which skill's output takes precedence. When a practitioner runs `hierarchy-management` to decompose a participant and then invokes `documentation-automation` to generate rich content, files silently overwrite each other with no warning.

This task establishes a clear ownership contract: `hierarchy-management` generates minimal-content stub files on initial folder creation, and `documentation-automation` is the authoritative full-content generator.

## Objectives

- Redefine `hierarchy-management` file generation as stub-only (skeleton content, clearly marked as placeholders)
- Define a stub specification so both skills have a shared understanding of the initial file state
- Add an explicit delegation note to `hierarchy-management` directing users to invoke `documentation-automation` for complete content
- Ensure `documentation-automation` does not overwrite files that already contain full content without explicit user confirmation

## Detailed Requirements

### Functional Requirements

- **FR-T20.1**: Define a **Stub File Specification** in `hierarchy-management/SKILL.md` describing exactly what each stub file contains:
  - `main.md` stub: front-matter block (Level, Parent Process link, Status: `Draft`), section headers with `[TO BE GENERATED - invoke documentation-automation]` placeholders, Sub-Processes table empty placeholder.
  - `process.md` stub: title, level marker, single-line `[TO BE GENERATED - invoke documentation-automation]` placeholder.
  - `collaboration.md` stub: title, level marker, empty `sequenceDiagram` code block with a `%% TO BE GENERATED` comment, and a `**Source Requirements**: [TBD]` line.
  - `domain-model.md` stub: title, level marker, empty `classDiagram` code block with a `%% TO BE GENERATED` comment.
- **FR-T20.2**: Update `hierarchy-management/SKILL.md` Steps 3 and 4 to specify that the generated `collaboration.md`, `main.md`, `process.md`, and `domain-model.md` are stubs conforming to FR-T20.1. Remove or replace any language implying these are production-ready documents.
- **FR-T20.3**: Add a **Post-Creation Reminder** block at the end of `hierarchy-management/SKILL.md` Workflow: _"After folder creation completes, invoke `documentation-automation` with this folder as the target to generate content-complete documents. The stub files created here will be replaced."_
- **FR-T20.4**: Add a **Content Guard** to `documentation-automation/SKILL.md`: before overwriting any of the four files, check whether the file already contains non-stub content (heuristic: presence of content beyond placeholder lines). If non-stub content is detected, prompt the user: _"[filename] already contains generated content. Overwrite? (y/N)"_ rather than silently replacing.
- **FR-T20.5**: Define the Content Guard heuristic threshold: a file is considered non-stub if it contains more than 10 non-placeholder, non-header lines of substantive text or diagram code.

### Technical Requirements

- **TR-T20.1**: Stub files must pass `hierarchy-validation` rule HN-2 (Required Files Present) — stubs must exist and be syntactically valid Markdown and Mermaid code blocks.
- **TR-T20.2**: The `[TO BE GENERATED]` placeholder string must be machine-detectable (exact substring match) so the Content Guard in `documentation-automation` can reliably identify stub vs. generated files.

### Business Requirements

- **BR-T20.1**: A practitioner running `hierarchy-management` followed by `documentation-automation` must receive the expected full-content documents with no data loss and no silent overwrite.
- **BR-T20.2**: The stub state must be immediately valid for downstream `hierarchy-validation` and `edps-compliance` pre-condition checks (i.e., required files present, minimal required fields populated).

## Acceptance Criteria

### Must Have
- [x] `hierarchy-management/SKILL.md` defines a Stub File Specification (FR-T20.1) for all four files
- [x] `hierarchy-management/SKILL.md` Steps 3/4 updated to describe stub-only output
- [x] `hierarchy-management/SKILL.md` includes Post-Creation Reminder (FR-T20.3)
- [x] `documentation-automation/SKILL.md` includes Content Guard check (FR-T20.4) with the threshold and overwrite prompt

### Should Have
- [x] Stub file templates shown as literal examples in `hierarchy-management/SKILL.md`
- [x] Content Guard heuristic threshold documented (FR-T20.5)

### Could Have
- [x] A `--force` flag documented for `documentation-automation` to skip Content Guard (for CI/automated use)

## Implementation Approach

### Phase 1: Analysis
1. Read `hierarchy-management/SKILL.md` Steps 3 and 4 to identify all file generation language
2. Read `documentation-automation/SKILL.md` to find the four file generation steps and identify where to insert Content Guard

### Phase 2: Implementation
1. Edit `hierarchy-management/SKILL.md` — add Stub File Specification section
2. Edit `hierarchy-management/SKILL.md` — update Steps 3/4 to reference stub spec
3. Edit `hierarchy-management/SKILL.md` — add Post-Creation Reminder
4. Edit `documentation-automation/SKILL.md` — add Content Guard pre-check to Workflow Step 1

### Phase 3: Validation
1. Verify stub files meet HN-2 (required files present, valid syntax)
2. Create 3 test cases: (a) stub detected → full generation proceeds; (b) non-stub content detected → prompt shown; (c) `--force` bypasses guard

## Dependencies

### Prerequisites
- **Task Dependencies**: T5 (hierarchy-management created), T12 (documentation-automation created)
- **Artifact Dependencies**: `hierarchy-management/SKILL.md`, `documentation-automation/SKILL.md`

### Blocking/Blocked By
- **Blocks**: T13 (Migration Tools) — migration scripts must understand stub vs. generated state
- **Blocked By**: None (can proceed in parallel with T18/T19)

## Deliverables

- Updated `hierarchy-management/SKILL.md` (stub spec, post-creation reminder)
- Updated `documentation-automation/SKILL.md` (content guard)
- Test cases in `artifacts/Testing/T20-test-cases.md`
- Test results in `artifacts/Testing/T20-test-results.md` — 5/5 PASS; 1 defect found and fixed (D-T20-1)

## Notes

- The stub definition also benefits T13 (migration): existing Project 1 orgModel files will likely be classified as non-stub, directing the migration tool to preserve rather than overwrite them.
- **D-T20-1 (fixed)**: `collaboration.md` and `domain-model.md` stub templates originally lacked the exact machine-detectable marker `[TO BE GENERATED - invoke documentation-automation]` outside the Mermaid code block. Fixed by adding `**Diagram Status**: [TO BE GENERATED - invoke documentation-automation]` front-matter field to both stub templates.
