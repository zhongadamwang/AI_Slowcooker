# T20 Test Cases — File Generation Ownership Contract

**Task**: T20 — Resolve C-3 File Generation Ownership Contract  
**Created**: March 15, 2026  
**Skill Under Test**: `hierarchy-management`, `documentation-automation`

---

## TC-T20-1: Stub Detected → Full Generation Proceeds

### Scenario
A practitioner runs `hierarchy-management` to decompose participant `OrderService` into `01-OrderServiceBoundary/`. Immediately after, they invoke `documentation-automation` targeting the new folder.

### Pre-conditions
- `01-OrderServiceBoundary/` was just created by `hierarchy-management`
- All four files (`main.md`, `process.md`, `collaboration.md`, `domain-model.md`) exist and are stubs (each contains `[TO BE GENERATED - invoke documentation-automation]`)

### Steps
1. Invoke `documentation-automation` targeting `01-OrderServiceBoundary/`
2. Content Guard pre-check runs for each of the four files
3. Each file is detected as a stub (contains `[TO BE GENERATED - invoke documentation-automation]`)
4. Generation proceeds without any prompts

### Expected Result
- All four files are overwritten with full content-complete documents
- No overwrite prompt is shown to the user
- Content Guard pre-check log shows: `[filename]: stub detected — proceeding` for all four files
- The resulting files do **not** contain `[TO BE GENERATED - invoke documentation-automation]`

### Acceptance Criteria Covered
- FR-T20.4 (Content Guard detects stubs and proceeds)
- TR-T20.2 (machine-detectable stub marker)

---

## TC-T20-2: Non-Stub Content Detected → Overwrite Prompt Shown

### Scenario
A practitioner manually edited `main.md` in `01-OrderServiceBoundary/` after running `documentation-automation`, adding 15 lines of custom overview text. They then re-invoke `documentation-automation` on the same folder.

### Pre-conditions
- `01-OrderServiceBoundary/main.md` contains more than 10 non-placeholder, non-header lines of substantive text
- `process.md`, `collaboration.md`, `domain-model.md` are still stubs (for contrast)

### Steps
1. Invoke `documentation-automation` targeting `01-OrderServiceBoundary/`
2. Content Guard pre-check runs for each of the four files
3. `main.md` is detected as non-stub (> 10 non-placeholder lines)
4. `documentation-automation` prompts: `"main.md already contains generated content. Overwrite? (y/N)"`
5. User responds `N`

### Expected Result
- `main.md` is **not** overwritten; its custom content is preserved
- The three stub files (`process.md`, `collaboration.md`, `domain-model.md`) **are** generated without prompt
- User sees confirmation that `main.md` was skipped

### Acceptance Criteria Covered
- FR-T20.4 (Content Guard prompts on non-stub content)
- FR-T20.5 (10-line threshold)
- BR-T20.1 (no data loss, no silent overwrite)

---

## TC-T20-3: `--force` Flag Bypasses Content Guard

### Scenario
A CI pipeline invokes `documentation-automation --force` on a folder where `main.md` already contains non-stub content (generated in a previous run).

### Pre-conditions
- `01-OrderServiceBoundary/main.md` contains more than 10 non-placeholder lines
- All four files have been previously generated (none are stubs)
- Invocation includes the `--force` flag

### Steps
1. CI pipeline invokes `documentation-automation --force` targeting `01-OrderServiceBoundary/`
2. Content Guard pre-check detects non-stub content in all four files
3. Due to `--force`, no interactive prompts are issued
4. All four files are overwritten

### Expected Result
- All four files are overwritten unconditionally
- No user prompts are issued
- Log/output indicates `--force` mode was active

### Acceptance Criteria Covered
- Conditional (Could Have): `--force` flag for CI/automated use (FR-T20.4, Could Have item)

---

## TC-T20-4: Stub Files Pass HN-2 Validation

### Scenario
Immediately after `hierarchy-management` creates `01-OrderServiceBoundary/`, `hierarchy-validation` is run to verify the required files are present and syntactically valid.

### Pre-conditions
- `hierarchy-management` has created `01-OrderServiceBoundary/` with all four stub files
- `documentation-automation` has **not** been run yet

### Steps
1. Run `hierarchy-validation` on `01-OrderServiceBoundary/`
2. Validator checks HN-2: required files present (`main.md`, `process.md`, `collaboration.md`, `domain-model.md`)
3. Validator checks that Markdown headings are present in each file
4. Validator checks that Mermaid code blocks in `collaboration.md` and `domain-model.md` are syntactically valid (empty but well-formed)

### Expected Result
- HN-2 passes: all four files are present
- Mermaid stub blocks (empty `sequenceDiagram` and `classDiagram` with `%% TO BE GENERATED` comment) are valid syntax — no parse errors
- `edps-compliance` pre-condition check succeeds (required files present, minimal required fields populated)

### Acceptance Criteria Covered
- TR-T20.1 (stub files pass HN-2)
- BR-T20.2 (stubs immediately valid for downstream checks)

---

## TC-T20-5: End-to-End Pipeline — No Data Loss

### Scenario
Full practitioner workflow: decompose → document → verify.

### Steps
1. `hierarchy-management` decomposes `PaymentGateway` → creates `02-PaymentGatewayBoundary/` with four stub files
2. `documentation-automation` runs on `02-PaymentGatewayBoundary/` → Content Guard finds stubs → overwrites all four with full content
3. Practitioner edits `main.md` to add domain-specific notes (15 lines)
4. `documentation-automation` is re-invoked without `--force`
5. Content Guard detects non-stub content in `main.md` → prompts user
6. User responds `N` to preserve custom content
7. `documentation-automation` regenerates `process.md`, `collaboration.md`, `domain-model.md` only

### Expected Result
- Step 2: All stubs replaced with full content; no silent overwrites
- Step 6–7: Custom `main.md` content preserved; other three files regenerated
- No data loss at any step

### Acceptance Criteria Covered
- BR-T20.1 (full pipeline, no data loss, no silent overwrite)
- FR-T20.4 (Content Guard in action)
