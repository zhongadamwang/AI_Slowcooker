# T10: Hierarchy Validation — Test Cases

**Task ID**: T10  
**Test Case Author**: GitHub Copilot  
**Test Date**: March 14, 2026  
**Status**: All 34 test cases executed and passed (March 14, 2026) — 1 defect found and fixed during execution  
**References**: [T10 Task](../../tasks/T10-hierarchy-validation.md), [SKILL.md — hierarchy-validation](../../../../../.github/skills/hierarchy-validation/SKILL.md), [T10 Test Results](T10-test-results.md)

---

## Category 1: HV-1 — Decomposed-Participant Is Control

### TC-T10-001: Valid — sub-folder matches a control-type participant in parent
**Rule**: HV-1  
**Given**: Parent `collaboration.md` declares `OrderProcessor@{ "type": "control" }`; sub-folder `01-OrderProcessorBoundary/` exists  
**When**: HV-1 check runs  
**Then**: Rule passes — normalized name `OrderProcessor` matches participant name

**Pass Criteria:**
- [x] `rule_results[HV-1].status` is `"PASS"`
- [x] `violations` array is empty for HV-1
- [x] Normalization confirmed: ordinal prefix `01-` and suffix `Boundary` stripped; comparison is case-insensitive

---

### TC-T10-002: Invalid — sub-folder has no matching control-type participant in parent
**Rule**: HV-1  
**Given**: Sub-folder `02-PaymentGatewayBoundary/` exists; parent `collaboration.md` has `PaymentGateway@{ "type": "entity" }` (not `control`)  
**When**: HV-1 check runs  
**Then**: HV-1 FAIL: violation identifies `02-PaymentGatewayBoundary` and states no `control`-type participant named `PaymentGateway` was found

**Pass Criteria:**
- [x] `rule_results[HV-1].status` is `"FAIL"`
- [x] Violation `folder` references `02-PaymentGatewayBoundary`
- [x] Violation `detail` states no matching `control`-type participant found
- [x] `remediation` instructs adding a `control`-type participant or removing the sub-folder

---

## Category 2: HV-2 — Parent Actor Appearance

### TC-T10-003: Valid — decomposed participant appears as actor outside all boxes in child
**Rule**: HV-2  
**Given**: Parent diagram decomposes `OrderProcessor@{ "type": "control" }`; child `01-OrderProcessorBoundary/collaboration.md` declares `OrderProcessor@{ "type": "actor" }` outside all `box … end` blocks  
**When**: HV-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HV-2].status` is `"PASS"`
- [x] `violations` array empty
- [x] Actor is confirmed to be declared outside all `box … end` blocks

---

### TC-T10-004: Invalid — parent participant absent from child diagram as actor
**Rule**: HV-2  
**Given**: Child `01-OrderProcessorBoundary/collaboration.md` contains no `actor`-type participant representing the parent's `OrderProcessor`; it jumps directly to internal boundary participants  
**When**: HV-2 check runs  
**Then**: HV-2 FAIL: violation identifies missing external actor in child diagram

**Pass Criteria:**
- [x] `rule_results[HV-2].status` is `"FAIL"`
- [x] Violation `detail` states no `actor`-type participant matching `OrderProcessor` found outside box blocks
- [x] `remediation` instructs adding `OrderProcessor@{ "type": "actor" }` outside all `box` blocks in the child diagram

---

## Category 3: HV-3 — Actor Label Consistency

### TC-T10-005: Valid — actor label closely matches decomposed participant label
**Rule**: HV-3  
**Given**: Parent has `OrderProc@{ "type": "control", "label": "Order Processor" }`; child external actor is `OrderProc@{ "type": "actor", "label": "Order Processor Service" }` — character overlap well above 50 %  
**When**: HV-3 check runs  
**Then**: Rule passes — overlap sufficient

**Pass Criteria:**
- [x] `rule_results[HV-3].status` is `"PASS"`
- [x] No HV-3 violations

---

### TC-T10-006: Warning — actor label in child has low character overlap with parent label
**Rule**: HV-3  
**Given**: Parent label is `"Inventory Manager"`; child actor label is `"SupplyChainOrchestrator"` — below 50 % character overlap after ignoring common suffix words  
**When**: HV-3 check runs  
**Then**: HV-3 WARNING: the low-overlap label pairing is flagged

**Pass Criteria:**
- [x] `rule_results[HV-3].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` identifies the mismatched parent label and child actor label
- [x] `remediation` instructs aligning the child actor label to match the decomposed participant's label

---

## Category 4: HV-4 — Entry-Point Type Integrity

### TC-T10-007: Valid — first message recipient inside box is boundary-type
**Rule**: HV-4  
**Given**: Child `collaboration.md` has external actor `OrderProcessor` sending first message to `OrderAPI@{ "type": "boundary" }` inside the box  
**When**: HV-4 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HV-4].status` is `"PASS"`
- [x] No HV-4 violations

---

### TC-T10-008: Invalid — first message recipient inside box is control-type (bypasses boundary)
**Rule**: HV-4  
**Given**: Child diagram external actor `OrderProcessor` sends first message directly to `ValidationEngine@{ "type": "control" }` inside the box, skipping any boundary participant  
**When**: HV-4 check runs  
**Then**: HV-4 FAIL: entry-point violation identifies `ValidationEngine` as first recipient with wrong type

**Pass Criteria:**
- [x] `rule_results[HV-4].status` is `"FAIL"`
- [x] Violation `detail` names `ValidationEngine` and its type `control` as the incorrect first recipient
- [x] `remediation` instructs reordering so the first inbound message targets a `boundary`-type participant

---

## Category 5: HV-5 — No Internal Leakage

### TC-T10-009: Valid — no child-internal participants appear in parent diagram
**Rule**: HV-5  
**Given**: Parent has `OrderProcessor@{ "type": "control" }` only; child `01-OrderProcessorBoundary/` has internal participants `ValidationEngine` and `PricingEngine`; neither appears in the parent diagram  
**When**: HV-5 check runs  
**Then**: Rule passes — the decomposed control participant in the parent is expected; child internals are not leaking

**Pass Criteria:**
- [x] `rule_results[HV-5].status` is `"PASS"`
- [x] `OrderProcessor` presence in both parent and child is NOT flagged (expected decomposition)
- [x] No violations

---

### TC-T10-010: Invalid — child internal participant declared in parent diagram
**Rule**: HV-5  
**Given**: Parent `collaboration.md` declares BOTH `OrderProcessor@{ "type": "control" }` AND `ValidationEngine@{ "type": "control" }` where `ValidationEngine` is an internal participant inside `01-OrderProcessorBoundary/collaboration.md`  
**When**: HV-5 check runs  
**Then**: HV-5 FAIL: `ValidationEngine` is flagged as child-level leakage into the parent

**Pass Criteria:**
- [x] `rule_results[HV-5].status` is `"FAIL"`
- [x] Violation `detail` identifies `ValidationEngine` as an internal child participant appearing in the parent
- [x] The exempt boundary entry-point (`OrderAPI@{ "type": "boundary" }`) is NOT flagged even if it matches something
- [x] `remediation` instructs removing `ValidationEngine` from the parent diagram

---

## Category 6: HX-1 — Parent Link Resolves

### TC-T10-011: Valid — sub-process main.md has correct parent link
**Rule**: HX-1  
**Given**: `01-OrderProcessorBoundary/main.md` contains `**Parent Process**: [Order Management](../main.md)` and `../main.md` exists  
**When**: HX-1 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HX-1].status` is `"PASS"`
- [x] No violations

---

### TC-T10-012: Invalid — sub-process main.md has a broken parent link
**Rule**: HX-1  
**Given**: `01-OrderProcessorBoundary/main.md` contains `**Parent Process**: [Order Management](../../main.md)` (one extra `../` — path does not resolve)  
**When**: HX-1 check runs  
**Then**: HX-1 FAIL: violation identifies the file and the unresolvable relative path

**Pass Criteria:**
- [x] `rule_results[HX-1].status` is `"FAIL"`
- [x] Violation `file` references `01-OrderProcessorBoundary/main.md`
- [x] Violation `detail` includes the broken path `../../main.md`
- [x] `remediation` matches the HX-1 entry in the Remediation Reference table

---

## Category 7: HX-2 — Child Links Resolve

### TC-T10-013: Valid — all Sub-Processes entries in parent main.md resolve
**Rule**: HX-2  
**Given**: Parent `main.md` Sub-Processes table has two rows linking to `01-OrderProcessorBoundary/main.md` and `02-PaymentServiceBoundary/main.md`; both files exist  
**When**: HX-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HX-2].status` is `"PASS"`
- [x] No violations

---

### TC-T10-014: Invalid — parent main.md Sub-Processes link targets a non-existent file
**Rule**: HX-2  
**Given**: Parent `main.md` Sub-Processes table lists `01-OrderProcessorBoundary/main.md` (exists) and `03-DiscountEngineBoundary/main.md` (folder does not exist)  
**When**: HX-2 check runs  
**Then**: HX-2 FAIL: violation identifies the stale link to `03-DiscountEngineBoundary/main.md`

**Pass Criteria:**
- [x] `rule_results[HX-2].status` is `"FAIL"`
- [x] Violation `detail` names the unresolvable path `03-DiscountEngineBoundary/main.md`
- [x] `remediation` instructs correcting the path in the parent Sub-Processes table

---

## Category 8: HX-3 — Breadcrumb Path Integrity

### TC-T10-015: Valid — all breadcrumb links resolve correctly
**Rule**: HX-3  
**Given**: A Level 2 `main.md` breadcrumb reads `[Root](../../main.md) › [Level 1](../main.md) › Current`; both `../../main.md` and `../main.md` exist  
**When**: HX-3 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HX-3].status` is `"PASS"`
- [x] No HX-3 violations

---

### TC-T10-016: Warning — one breadcrumb link is broken
**Rule**: HX-3  
**Given**: Same Level 2 `main.md` breadcrumb, but `../../main.md` does not exist (root was reorganized)  
**When**: HX-3 check runs  
**Then**: HX-3 WARNING: the broken breadcrumb link is reported

**Pass Criteria:**
- [x] `rule_results[HX-3].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` references the specific broken relative path `../../main.md`
- [x] `remediation` refers to rebuilding the breadcrumb or running `--fix`

---

## Category 9: HX-4 — Decomposition Comment Matches Folder

### TC-T10-017: Valid — decomposition comment references an existing sub-folder
**Rule**: HX-4  
**Given**: `collaboration.md` contains `%% decomposed: OrderProcessor → 01-OrderProcessorBoundary/collaboration.md`; the folder `01-OrderProcessorBoundary/` exists  
**When**: HX-4 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HX-4].status` is `"PASS"`
- [x] No HX-4 violations

---

### TC-T10-018: Warning — decomposition comment references a deleted sub-folder
**Rule**: HX-4  
**Given**: `collaboration.md` contains `%% Decomposition: OrderProcessor → 01-OrderProcessorBoundary/collaboration.md` but `01-OrderProcessorBoundary/` was deleted (does not exist)  
**When**: HX-4 check runs  
**Then**: HX-4 WARNING: stale decomposition comment flagged

**Pass Criteria:**
- [x] Both `%% decomposed:` and `%% Decomposition:` comment variants matched by the check
- [x] `rule_results[HX-4].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` names the stale comment and the non-existent path
- [x] `remediation` instructs updating the path or removing the stale comment

---

## Category 10: HX-5 — Hierarchy Index Currency

### TC-T10-019: Valid — hierarchy-index.md lists all sub-process folders
**Rule**: HX-5  
**Given**: Root `hierarchy-index.md` Full Hierarchy Tree table lists Level 0 root, `01-OrderProcessorBoundary` at Level 1, and `01-ValidationEngineBoundary` at Level 2; all three correspond to actual folders  
**When**: HX-5 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HX-5].status` is `"PASS"`
- [x] No HX-5 violations

---

### TC-T10-020: Warning — hierarchy-index.md missing a recently added sub-folder
**Rule**: HX-5  
**Given**: Root `hierarchy-index.md` lists only `01-OrderProcessorBoundary`; a new `02-PaymentServiceBoundary/` folder also exists on the filesystem but is not listed in the index  
**When**: HX-5 check runs  
**Then**: HX-5 WARNING: `02-PaymentServiceBoundary` flagged as absent from index

**Pass Criteria:**
- [x] `rule_results[HX-5].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` names the missing folder
- [x] `remediation` instructs running `hierarchy-management` to regenerate the index or running `--fix`

---

## Category 11: HN-1 — Folder Name Convention

### TC-T10-021: Valid — folder name matches required pattern
**Rule**: HN-1  
**Given**: Sub-folder named `01-OrderProcessorBoundary`  
**When**: HN-1 check runs  
**Then**: Folder name matches `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`; rule passes

**Pass Criteria:**
- [x] `rule_results[HN-1].status` is `"PASS"`
- [x] No violations

---

### TC-T10-022: Invalid — folder name does not match convention
**Rule**: HN-1  
**Given**: Sub-folder named `orderprocessor-boundary` (lowercase, no ordinal prefix, hyphen before `boundary`)  
**When**: HN-1 check runs  
**Then**: HN-1 FAIL: violation identifies the non-conforming name and the required pattern

**Pass Criteria:**
- [x] `rule_results[HN-1].status` is `"FAIL"`
- [x] Violation `detail` references regex `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`
- [x] `remediation` instructs renaming the folder and updating all references

---

## Category 12: HN-2 — Required Files Present

### TC-T10-023: Valid — sub-folder contains both required files
**Rule**: HN-2  
**Given**: `01-OrderProcessorBoundary/` contains both `collaboration.md` and `main.md` (plus optional `process.md` and `domain-model.md`)  
**When**: HN-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HN-2].status` is `"PASS"`
- [x] `process.md` and `domain-model.md` absence does NOT trigger a failure (they are optional)

---

### TC-T10-024: Invalid — sub-folder is missing collaboration.md
**Rule**: HN-2  
**Given**: `02-PaymentServiceBoundary/` contains only `main.md`; `collaboration.md` is absent  
**When**: HN-2 check runs  
**Then**: HN-2 FAIL: violation identifies the missing `collaboration.md` in the specified folder

**Pass Criteria:**
- [x] `rule_results[HN-2].status` is `"FAIL"`
- [x] Violation `detail` specifies `collaboration.md` as the missing file
- [x] `remediation` instructs creating the missing file using `hierarchy-management` templates

---

## Category 13: HN-3 — Ordinal Uniqueness

### TC-T10-025: Valid — all sibling folders have unique ordinal prefixes
**Rule**: HN-3  
**Given**: Parent folder contains `01-OrderProcessorBoundary/`, `02-PaymentServiceBoundary/`, `03-NotificationServiceBoundary/` — ordinals `01`, `02`, `03` are all unique  
**When**: HN-3 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HN-3].status` is `"PASS"`
- [x] No violations

---

### TC-T10-026: Invalid — two sibling folders share the same ordinal prefix
**Rule**: HN-3  
**Given**: Parent folder contains `01-OrderProcessorBoundary/` and `01-PaymentServiceBoundary/` — both have ordinal prefix `01`  
**When**: HN-3 check runs  
**Then**: HN-3 FAIL: violation identifies both folders with the duplicated ordinal `01`

**Pass Criteria:**
- [x] `rule_results[HN-3].status` is `"FAIL"`
- [x] Violation `detail` names both conflicting folders and the duplicate ordinal
- [x] `remediation` instructs renumbering sub-folders to eliminate the conflict

---

## Category 14: HN-4 — Level Number Consistency

### TC-T10-027: Valid — Level field matches actual folder depth
**Rule**: HN-4  
**Given**: `01-OrderProcessorBoundary/main.md` has `**Level**: 1` and the folder is one level below the root process folder (actual depth = 1)  
**When**: HN-4 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HN-4].status` is `"PASS"`
- [x] No violations

---

### TC-T10-028: Warning — Level field in main.md is incorrect
**Rule**: HN-4  
**Given**: `01-OrderProcessorBoundary/01-ValidationEngineBoundary/main.md` has `**Level**: 1` but the correct depth is 2  
**When**: HN-4 check runs  
**Then**: HN-4 WARNING: mismatch between stated level (1) and computed depth (2)

**Pass Criteria:**
- [x] `rule_results[HN-4].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` states stated level `1` vs. computed depth `2`
- [x] `remediation` instructs updating `**Level**: [N]` to the correct value or running `--fix`

---

## Category 15: Validation Scoring and Overall Status

### TC-T10-029: VALID — all 14 rules pass
**Requirement**: Scoring formula  
**Given**: A well-formed hierarchy where all 14 applicable rules pass; 0 errors; 0 warnings  
**When**: Validation score is calculated  
**Then**: `validation_score = 100`, `overall_status = "VALID"`

**Pass Criteria:**
- [x] `summary.validation_score` equals `100.0`
- [x] `summary.overall_status` equals `"VALID"`
- [x] `summary.failed_errors` equals `0`
- [x] `summary.failed_warnings` equals `0`

---

### TC-T10-030: NEEDS_ATTENTION — 2 error violations
**Requirement**: Scoring formula  
**Given**: 14 checks; 2 FAIL on ERROR-severity rules (HV-1 and HX-1); all others pass  
**When**: Score is calculated  
**Then**: `validation_score ≈ 85.7`, `overall_status = "NEEDS_ATTENTION"` (errors > 0, errors ≤ 3)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `2`
- [x] `summary.overall_status` equals `"NEEDS_ATTENTION"`
- [x] `summary.validation_score` equals approximately `85.7` (12/14)

---

### TC-T10-031: INVALID — more than 3 error violations
**Requirement**: Scoring formula  
**Given**: 14 checks; 5 FAIL on ERROR-severity rules  
**When**: Score is calculated  
**Then**: `overall_status = "INVALID"` (errors > 3)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `5`
- [x] `summary.overall_status` equals `"INVALID"`

---

### TC-T10-032: MOSTLY_VALID — 0 errors, 3 warnings, score ≥ 70 %
**Requirement**: Scoring formula  
**Given**: 14 checks; 0 errors; 3 FAIL on WARNING-severity rules (HV-3, HX-3, HN-4); 11 pass  
**When**: Score is calculated  
**Then**: `validation_score ≈ 78.6`, `overall_status = "MOSTLY_VALID"` (errors = 0, score ≥ 70)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `0`
- [x] `summary.failed_warnings` equals `3`
- [x] `summary.overall_status` equals `"MOSTLY_VALID"`
- [x] `summary.validation_score` equals approximately `78.6` (11/14)

---

## Category 16: Incremental Validation Mode

### TC-T10-033: Incremental mode validates only the specified branch and its immediate parent
**Requirement**: Incremental Validation section  
**Given**: Full hierarchy has Level 0 root with two children: `01-OrderProcessorBoundary/` and `02-PaymentServiceBoundary/`; user runs validation with `--mode incremental` targeting `01-OrderProcessorBoundary/`  
**When**: Incremental validation runs  
**Then**: Only `01-OrderProcessorBoundary/` and its descendants are fully checked; root is only checked for HV-1, HV-2, HX-2 (registration checks); `02-PaymentServiceBoundary/` is not scanned at all

**Pass Criteria:**
- [x] Report scope reads `[01-OrderProcessorBoundary path] (incremental)`
- [x] `summary.folders_scanned` reflects only the targeted branch plus root-level partial check
- [x] Violations in `02-PaymentServiceBoundary/` are not reported
- [x] Root-level HV-1, HV-2, HX-2 checks ARE run to confirm the branch is registered correctly

---

## Category 17: Auto-Fix Behaviour

### TC-T10-034: Auto-fix corrects HN-4 (Level field) and HX-3 (breadcrumb) without touching ERROR rules
**Requirement**: Auto-Fix Pass section; `--fix` flag  
**Given**: Hierarchy with (a) `main.md` stating `**Level**: 1` but actual depth is 2 (HN-4 violation); (b) broken breadcrumb link (HX-3 violation); (c) missing `control`-type participant for a sub-folder (HV-1 ERROR violation)  
**When**: Validation runs with `--fix`  
**Then**: HN-4 and HX-3 are auto-corrected; HV-1 is reported but NOT auto-fixed

**Pass Criteria:**
- [x] `auto_fixes_applied` list contains entries for HN-4 and HX-3
- [x] Updated `main.md` now contains `**Level**: 2`
- [x] Updated breadcrumb contains a corrected relative path
- [x] HV-1 violation remains in `rule_results` with status `"FAIL"` and is NOT in `auto_fixes_applied`
- [x] `summary.auto_fixed` equals `2`

---
