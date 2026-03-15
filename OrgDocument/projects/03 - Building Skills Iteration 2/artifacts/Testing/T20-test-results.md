# T20 Test Results — File Generation Ownership Contract

**Task**: T20 — Resolve C-3 File Generation Ownership Contract  
**Executed**: March 15, 2026  
**Method**: Static specification analysis against `hierarchy-management/SKILL.md` and `documentation-automation/SKILL.md`  
**Executed By**: GitHub Copilot

---

## Summary

| Test Case | Result | Notes |
|-----------|--------|-------|
| TC-T20-1: Stub Detected → Full Generation Proceeds | ⚠ FAIL → FIXED | Defect D-T20-1: `collaboration.md` and `domain-model.md` stubs missing exact machine-detectable marker |
| TC-T20-2: Non-Stub Content → Overwrite Prompt | ✓ PASS | Minor gap: "skipped" confirmation message not explicitly defined |
| TC-T20-3: `--force` Bypasses Content Guard | ✓ PASS | Minor gap: `--force` mode log format not defined |
| TC-T20-4: Stub Files Pass HN-2 Validation | ✓ PASS | All four stubs are syntactically valid Markdown/Mermaid |
| TC-T20-5: End-to-End Pipeline — No Data Loss | ⚠ FAIL → FIXED | Same defect D-T20-1 |

**Final result after fix**: 5/5 PASS

---

## Defect Report

### D-T20-1 — Missing Exact Stub Marker in `collaboration.md` and `domain-model.md` Stubs

**Severity**: High  
**Status**: Fixed (March 15, 2026)  
**Affects**: TC-T20-1, TC-T20-5  
**Violated requirement**: TR-T20.2 — "The `[TO BE GENERATED]` placeholder string must be machine-detectable (exact substring match)"

**Root cause**: The `collaboration.md` and `domain-model.md` stub templates in `hierarchy-management/SKILL.md` only contained the Mermaid-internal comment `%% TO BE GENERATED — invoke documentation-automation to populate this diagram` inside the `sequenceDiagram`/`classDiagram` code blocks. This comment:
  - Uses `%%` prefix (Mermaid comment syntax), not `[` brackets
  - Uses an em dash `—` instead of a hyphen `-`
  - Has the suffix "to populate this diagram" not in the canonical marker

The Content Guard in `documentation-automation/SKILL.md` performs **exact substring match** for `[TO BE GENERATED - invoke documentation-automation]`. This match would **not fire** for the Mermaid comment variant, causing both files to fall through to the line-count path instead.

**Impact without fix**: The `collaboration.md` and `domain-model.md` stubs would be processed via the line-count path (≤ 10 lines → proceed), so generation would still proceed correctly in the most common scenario. However:
  - TC-T20-2 scenario: if a `collaboration.md` genuinely had > 10 content lines and no `[TO BE GENERATED]` marker, the prompt would still fire — correct behavior, wrong code path
  - TR-T20.2 (machine-detectability) would be formally violated

**Fix applied to `hierarchy-management/SKILL.md`**: Added `**Diagram Status**: [TO BE GENERATED - invoke documentation-automation]` as a front-matter field to both the `collaboration.md` stub and `domain-model.md` stub templates. This:
  - Injects the exact canonical marker into the non-Mermaid part of the file
  - Remains meaningful as a human-readable status field
  - Preserves the existing Mermaid `%% TO BE GENERATED` comment (useful for developers viewing the diagram)

---

## Detailed Findings by Test Case

### TC-T20-1: Stub Detected → Full Generation Proceeds

**Pre-fix result**: FAIL  
**Post-fix result**: PASS  

**Evidence before fix**:
- `main.md` stub: contains `[TO BE GENERATED - invoke documentation-automation]` at lines for Breadcrumb, Sub-Processes, and Overview — marker present ✓
- `process.md` stub: contains `[TO BE GENERATED - invoke documentation-automation]` in body — marker present ✓
- `collaboration.md` stub: only contained `%% TO BE GENERATED — invoke documentation-automation to populate this diagram` inside Mermaid block — exact marker **absent** ✗
- `domain-model.md` stub: same issue — exact marker **absent** ✗
- Content Guard decision matrix: "File exists and is a stub (contains `[TO BE GENERATED - invoke documentation-automation]`) → Proceed with generation" — would NOT fire for the two Mermaid-heavy stubs
- Fallthrough to line-count path (both stubs have ≤ 10 non-header lines) → generation would proceed, but through wrong path

**Evidence after fix**:
- Both `collaboration.md` and `domain-model.md` now contain `**Diagram Status**: [TO BE GENERATED - invoke documentation-automation]` in front-matter — exact marker present ✓
- Content Guard stub detection fires for all four files ✓

**Remaining gap**: No log format for "stub detected — proceeding" is defined in `documentation-automation/SKILL.md`. The skill specifies behavior (proceed) but not a console message confirming the detection path taken. This is an output-format omission, not a functional defect.

---

### TC-T20-2: Non-Stub Content Detected → Overwrite Prompt Shown

**Result**: PASS  

**Evidence**:
- `documentation-automation/SKILL.md` §2b decision matrix row: "File exists and non-stub line count > 10 → Prompt user: `[filename] already contains generated content. Overwrite? (y/N)`" — exact prompt text matches expected ✓
- "If the user responds `N` or provides no input → skip that file and preserve its content" — data preservation on N ✓
- Three stub files at this point still fall via stub detection or line-count path → generation proceeds without prompt ✓

**Remaining gap**: The skill states the file is skipped and preserved, but does not define an explicit "main.md was skipped" confirmation message. Functionally correct; output formatting unspecified. Low severity.

---

### TC-T20-3: `--force` Flag Bypasses Content Guard

**Result**: PASS  

**Evidence**:
- `documentation-automation/SKILL.md` §2b: "`--force` flag: When `documentation-automation` is invoked with `--force`, skip all Content Guard prompts and overwrite all files unconditionally." ✓
- "Use this flag in CI/automated pipelines where interactive prompts are unavailable." — CI use case documented ✓

**Remaining gap**: No log/output format indicating `--force` mode was active is specified. Not a functional defect — CI pipelines typically don't require explicit mode confirmation.

---

### TC-T20-4: Stub Files Pass HN-2 Validation

**Result**: PASS  

**Evidence**:
- `main.md` stub: valid Markdown heading (`# [ParticipantName] Boundary`), front-matter key-value fields, section headers (`## Navigation`, `## Overview`, etc.) ✓
- `process.md` stub: `<!-- Identifier: P-[NN] -->` HTML comment, valid Markdown heading, front-matter field ✓
- `collaboration.md` stub: valid Markdown heading, well-formed Mermaid `sequenceDiagram` block (empty body except comment is valid Mermaid syntax) ✓
- `domain-model.md` stub: valid Markdown heading, well-formed Mermaid `classDiagram` block (same reasoning) ✓
- `hierarchy-management/SKILL.md` §Stub File Specification explicitly states: "Stub files pass `hierarchy-validation` rule HN-2 (Required Files Present) immediately after creation." ✓
- `edps-compliance` pre-condition check: HN-2 passes because all required files exist; BR-T20.2 satisfied ✓

---

### TC-T20-5: End-to-End Pipeline — No Data Loss

**Pre-fix result**: FAIL  
**Post-fix result**: PASS  

**Evidence**: Same resolution as TC-T20-1. After fix:
- Step 1: `hierarchy-management` creates four stubs — all four now contain the exact marker ✓
- Step 2: Content Guard detects stubs for all four via marker → overwrites with full content — no silent overwrite since stubs → full generation is the intended path ✓
- Step 3: Practitioner edits `main.md` → file no longer contains `[TO BE GENERATED]` marker; non-stub line count > 10 ✓
- Step 4–5: Content Guard fires non-stub prompt for `main.md` ✓
- Step 6: User responds N → `main.md` preserved; other three files (if stubs, or if regeneration requested) proceed ✓
- BR-T20.1 satisfied: no data loss, no silent overwrite ✓

---

## Gap Register (Non-Blocking)

| ID | Description | Severity | Action |
|----|-------------|----------|--------|
| G-T20-1 | No log format defined for "stub detected — proceeding" console output | Low | Optional enhancement to `documentation-automation/SKILL.md` |
| G-T20-2 | No explicit "file skipped" confirmation message when user responds N | Low | Optional enhancement to `documentation-automation/SKILL.md` |
| G-T20-3 | No log format for `--force` mode activation | Low | Optional enhancement to `documentation-automation/SKILL.md` |

---

## Pass/Fail Matrix

| Requirement | Covered By | Result |
|-------------|------------|--------|
| FR-T20.1 (Stub File Specification) | TC-T20-1, TC-T20-4 | ✓ PASS |
| FR-T20.2 (Steps 3/4 stub-only) | TC-T20-1 (stub creation path) | ✓ PASS |
| FR-T20.3 (Post-Creation Reminder) | Verified in SKILL.md | ✓ PASS |
| FR-T20.4 (Content Guard + prompt) | TC-T20-1, TC-T20-2, TC-T20-3 | ✓ PASS |
| FR-T20.5 (10-line threshold) | TC-T20-2 | ✓ PASS |
| TR-T20.1 (HN-2 compliance) | TC-T20-4 | ✓ PASS |
| TR-T20.2 (machine-detectable marker) | TC-T20-1 | ✓ PASS (after fix) |
| BR-T20.1 (no data loss, no silent overwrite) | TC-T20-2, TC-T20-5 | ✓ PASS |
| BR-T20.2 (stubs valid for downstream checks) | TC-T20-4 | ✓ PASS |
| --force flag (Could Have) | TC-T20-3 | ✓ PASS |
