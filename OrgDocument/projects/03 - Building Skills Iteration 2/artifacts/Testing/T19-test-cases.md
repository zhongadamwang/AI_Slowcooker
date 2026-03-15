# T19 Test Cases — Structural Validation Scope Segregation

**Task**: T19 — Resolve C-2  
**Created**: March 14, 2026  
**Executed**: March 14, 2026  
**Method**: Static specification verification against `.github/skills/edps-compliance/SKILL.md` and `.github/skills/hierarchy-validation/SKILL.md`  
**Result**: ✅ 7/7 PASS  
**Skill Under Test**: `edps-compliance` (pre-condition gate + reduced Group B) and `hierarchy-validation` (updated description)

---

## TC-T19-01 — Pre-Condition Satisfied via Report File (Happy Path)

**Category**: Pre-Condition Gate  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Setup
- Target scope: `orgModel/01 - Skill Development Process/`
- `hierarchy-validation-report.json` is provided in the input with:
  - `target_scope`: `orgModel/01 - Skill Development Process/`
  - `overall_status`: `VALID`

### Expected Behaviour
1. `edps-compliance` reads `hierarchy-validation-report.json`.
2. Validates that `target_scope` in the report matches the current run target — they match.
3. `overall_status` is `VALID` — pre-condition is satisfied.
4. Proceeds normally to Step 1 (Discover Scope) through Step 6 (Generate Reports).
5. Final `overall_status` is one of `COMPLIANT`, `MOSTLY_COMPLIANT`, `NEEDS_ATTENTION`, or `NON_COMPLIANT` (not `BLOCKED`).

### Pass Criteria
- [x] No `pre-condition-not-met` error is emitted. *(Pre-Conditions section lines 70–72: scope match + `VALID`/`MOSTLY_VALID` → proceed to workflow)*
- [x] Report is generated for Group B (HR-2, HR-6) and Group C (EP-1–EP-4) checks. *(Group B table contains only HR-2 and HR-6; Group C table unchanged with EP-1–EP-4)*
- [x] Group B `total_checks` counts only 2 rules (HR-2 and HR-6). *(HR-1/3/4/5 removed from the rule catalogue)*

---

## TC-T19-02 — Pre-Condition Not Met — BLOCKED Status

**Category**: Pre-Condition Gate  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Setup
- Target scope: `orgModel/01 - Skill Development Process/`
- No `hierarchy-validation-report.json` provided.
- No manual confirmation given.

### Expected Behaviour
1. `edps-compliance` detects no report and no manual confirmation.
2. Emits `pre-condition-not-met` error with the following fields:
   - `error`: `"pre-condition-not-met"`
   - `missing_pre_condition`: contains `hierarchy-validation`
   - `suggested_command`: references the target scope
   - `blocking_issues`: non-empty array
3. Halts — does not proceed to Step 1 or any compliance checks.
4. Output `overall_status` is `BLOCKED`.

### Pass Criteria
- [x] `overall_status` in output is `BLOCKED`. *(`BLOCKED` added as first-match case in scoring formula)*
- [x] All three required error fields (`missing_pre_condition`, `suggested_command`, `blocking_issues`) are present. *(Pre-condition error schema explicitly defines all three fields)*
- [x] No Group A, B, or C checks are performed. *(Pre-Conditions section: "must halt immediately and return a `pre-condition-not-met` error without executing any Group A, B, or C checks")*
- [x] No `edps-compliance-report.json` or `edps-compliance-report.md` is written (or if written, it records only the BLOCKED status with the error payload). *(Halt behaviour specified; only BLOCKED error payload emitted)*

---

## TC-T19-03 — Scope-Mismatch Guard Triggered

**Category**: Pre-Condition Gate — Scope Mismatch  
**Severity**: Should Have  
**Result**: ✅ PASS  

### Setup
- Target scope: `orgModel/01 - Skill Development Process/`
- `hierarchy-validation-report.json` is provided but contains:
  - `target_scope`: `orgModel/02 - Some Other Process/`
  - `overall_status`: `VALID`

### Expected Behaviour
1. `edps-compliance` reads `hierarchy-validation-report.json`.
2. Detects that `target_scope` in the report (`orgModel/02 - Some Other Process/`) does not match the current target (`orgModel/01 - Skill Development Process/`).
3. Issues a `scope-mismatch` warning in the console.
4. Falls back to requiring manual confirmation.
5. Without manual confirmation, emits `pre-condition-not-met` error and returns `BLOCKED`.

### Pass Criteria
- [x] `scope-mismatch` warning is logged/emitted. *(Pre-Conditions line 73: "issue a `scope-mismatch` warning")*
- [x] The mismatched report is **not** accepted as satisfying the pre-condition. *(Falls back to requiring manual confirmation)*
- [x] Skill does not silently proceed with wrong-scope data. *(Explicit `scope-mismatch` path prevents silent acceptance)*
- [x] Final status is `BLOCKED` (absent manual confirmation). *(Without manual confirmation — line 75 — `edps-compliance` emits pre-condition error and halts → `BLOCKED`)*

---

## TC-T19-04 — HR-2 Check Still Executes (Retained Rule)

**Category**: Group B Rule Retention  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Setup
- Pre-condition satisfied (valid report provided).
- Target: a folder where a sub-process folder `01-PaymentBoundary/` exists but the parent `collaboration.md` has no `control`-type participant named `Payment`.

### Expected Behaviour
1. Step 3 executes HR-2 check only (HR-1/3/4/5 are not checked).
2. HR-2 FAIL: sub-folder `01-PaymentBoundary/` cannot be matched to any `control`-type participant in the parent.
3. Report records HR-2 as FAIL with appropriate violation detail.

### Pass Criteria
- [x] HR-2 violation is reported. *(HR-2 Check algorithm block is intact in Step 3)*
- [x] No HR-1, HR-3, HR-4, or HR-5 check results appear in the report. *(HR-1/3/4/5 algorithm blocks fully removed; only delegation note remains)*
- [x] `total_checks` does not include HR-1/3/4/5. *(Group B catalogue has exactly 2 rules: HR-2 and HR-6)*

---

## TC-T19-05 — HR-6 Check Still Executes (Retained Rule)

**Category**: Group B Rule Retention  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Setup
- Pre-condition satisfied.
- Target: a folder with a `hierarchy-metadata.json` whose `last_updated` is 7 days older than the most recent `collaboration.md` modification time.

### Expected Behaviour
1. Step 3 executes HR-6 check.
2. HR-6 WARNING: `last_updated` is stale.
3. Report records HR-6 as FAIL (WARNING severity).

### Pass Criteria
- [x] HR-6 warning is recorded. *(HR-6 Check algorithm block is intact in Step 3)*
- [x] `compliance_score` is reduced by the HR-6 failure contribution. *(Scoring formula counts all FAIL results regardless of severity; HR-6 FAIL contributes to passed_checks denominator)*

---

## TC-T19-06 — Reduced Rule Count in Compliance Score

**Category**: Scoring Formula  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Setup
- Pre-condition satisfied.
- Target with 2 `collaboration.md` files.
- All VR rules PASS (4 checks × 2 files = 8).
- HR-2 PASS, HR-6 PASS (2 checks).
- All EP rules PASS (4 checks × 2 files = 8).
- No skipped checks.

### Expected Behaviour
- `total_checks` = 18 (8 VR + 2 HR + 8 EP). HR-1/3/4/5 do NOT contribute.
- `passed_checks` = 18.
- `compliance_score` = 100%.

### Pass Criteria
- [x] `total_checks` is 18, not 22 (which would include the removed HR-1/3/4/5). *(Group B table has 2 rules; 4 VR × 2 files + 2 HR + 4 EP × 2 files = 18 total checks)*
- [x] `compliance_score` = 100.0. *(18/18 × 100 = 100.0)*
- [x] `overall_status` = `COMPLIANT`. *(Scoring: errors=0 AND score≥90 → COMPLIANT)*

---

## TC-T19-07 — hierarchy-validation Description Contains Authoritative Scope Statement

**Category**: Specification Verification  
**Severity**: Must Have  
**Result**: ✅ PASS  

### Verification
- Open `hierarchy-validation/SKILL.md`.
- Read the `description` field in the YAML frontmatter.

### Pass Criteria
- [x] The description explicitly states that `hierarchy-validation` is the authoritative structural integrity checker for the EDPS skill suite. *(Frontmatter line 4: "**Authoritative structural integrity checker for the EDPS skill suite.**")*
- [x] The description notes that other skills delegate structural checks to `hierarchy-validation` rather than re-implementing them. *(Frontmatter line 4: "other skills (e.g., edps-compliance) delegate these checks to hierarchy-validation via a mandatory pre-condition gate rather than re-implementing them")*

---

## Test Results Summary

**Executed**: March 14, 2026  
**Method**: Static specification verification — each pass criterion traced directly to the corresponding line(s) in the updated skill files  
**Executed by**: GitHub Copilot (automated spec review)

| Test Case | Category | Severity | Result |
|-----------|----------|----------|--------|
| TC-T19-01 | Pre-Condition Gate — Happy Path | Must Have | ✅ PASS |
| TC-T19-02 | Pre-Condition Gate — BLOCKED | Must Have | ✅ PASS |
| TC-T19-03 | Pre-Condition Gate — Scope Mismatch | Should Have | ✅ PASS |
| TC-T19-04 | Group B Rule Retention — HR-2 | Must Have | ✅ PASS |
| TC-T19-05 | Group B Rule Retention — HR-6 | Must Have | ✅ PASS |
| TC-T19-06 | Scoring Formula — Reduced Rule Count | Must Have | ✅ PASS |
| TC-T19-07 | Specification Verification — hierarchy-validation | Must Have | ✅ PASS |
| **Total** | | | **7/7 PASS** |

**No gaps or defects found.** All Must Have and Should Have acceptance criteria satisfied.
