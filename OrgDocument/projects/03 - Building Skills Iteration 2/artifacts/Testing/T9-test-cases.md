# T9: EDPS Compliance Checking — Test Cases

**Task ID**: T9  
**Test Case Author**: GitHub Copilot  
**Test Date**: March 14, 2026  
**Status**: All 33 test cases executed and passed (March 14, 2026) — 3 defects found and fixed during execution  
**References**: [T9 Task](../../tasks/T9-edps-compliance.md), [SKILL.md — edps-compliance](../../../../../.github/skills/edps-compliance/SKILL.md), [T9 Test Results](T9-test-results.md)

---

## Category 1: VR-1 — Single External Interface (Group A)

### TC-T9-001: Valid — single external actor per boundary
**Rule**: VR-1  
**Given**: A `collaboration.md` with one `box` boundary containing a `boundary`-type entry point; only `Customer` (actor) sends messages directly into the box  
**When**: VR-1 check runs  
**Then**: Rule passes; no violations reported

**Input snippet:**
```
participant Customer@{ "type": "actor" }
box Order Platform
  participant OrderAPI@{ "type": "boundary" }
  participant OrderProcessor@{ "type": "control" }
end
Customer ->> OrderAPI: Place Order
```

**Pass Criteria:**
- [x] `rule_results[VR-1].status` is `"PASS"`
- [x] `violations` array is empty for VR-1
- [x] `compliance_score` not reduced by VR-1

---

### TC-T9-002: Invalid — two external actors accessing the same boundary directly
**Rule**: VR-1  
**Given**: `Customer` and `Admin` both send messages directly to participants inside the same `box`  
**When**: VR-1 check runs  
**Then**: VR-1 FAIL: violation reports both actors and the affected boundary name

**Pass Criteria:**
- [x] `rule_results[VR-1].status` is `"FAIL"`
- [x] Violation `detail` mentions both `Customer` and `Admin`
- [x] Violation references the correct boundary name
- [x] `remediation` suggests introducing a gateway control participant
- [x] In relaxed mode: report generated; in strict mode: execution stops with error summary

---

### TC-T9-003: Valid — multiple boundaries each with one actor
**Rule**: VR-1  
**Given**: Two separate `box` blocks; `BoxA` accessed only by `UserPortal`; `BoxB` accessed only by `AdminConsole`  
**When**: VR-1 check runs  
**Then**: Both boundaries PASS; no violations

**Pass Criteria:**
- [x] `rule_results[VR-1].status` is `"PASS"`
- [x] `violations` array empty
- [x] Both boundaries listed in `checked_files` or equivalent per-file result

---

## Category 2: VR-2 — Boundary-First Reception (Group A)

### TC-T9-004: Valid — first message targets boundary-type participant
**Rule**: VR-2  
**Given**: Actor `Customer` sends first message to `OrderAPI@{ "type": "boundary" }` inside the box  
**When**: VR-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[VR-2].status` is `"PASS"`
- [x] No violations for VR-2

---

### TC-T9-005: Invalid — actor bypasses boundary and sends to control directly
**Rule**: VR-2  
**Given**: Actor `Admin` sends first message to `OrderProcessor@{ "type": "control" }` inside the box (skipping the boundary participant)  
**When**: VR-2 check runs  
**Then**: VR-2 FAIL: violation identifies the bypassed boundary and the direct target

**Pass Criteria:**
- [x] `rule_results[VR-2].status` is `"FAIL"`
- [x] Violation `detail` names `Admin` as the actor and `OrderProcessor` as the direct non-boundary target
- [x] `remediation` instructs rerouting the first message to the `boundary`-type entry point

---

### TC-T9-006: Valid — actor outside all boxes sends normally; no box involved
**Rule**: VR-2  
**Given**: A `collaboration.md` with no `box` blocks — all participants are top-level  
**When**: VR-2 check runs  
**Then**: Rule is SKIPPED (no boxes to evaluate); status `"SKIPPED"`

**Pass Criteria:**
- [x] `rule_results[VR-2].status` is `"SKIPPED"`
- [x] SKIPPED result does not count against `total_checks` denominator for scoring

---

## Category 3: VR-3 — Control-Only Decomposition (Group A)

### TC-T9-007: Valid — only control-type participant has a sub-folder
**Rule**: VR-3  
**Given**: `OrderProcessor@{ "type": "control" }` has a corresponding `01-OrderProcessorBoundary/` sub-folder; no other types have sub-folders  
**When**: VR-3 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[VR-3].status` is `"PASS"`
- [x] No violations

---

### TC-T9-008: Invalid — entity-type participant has a sub-folder
**Rule**: VR-3  
**Given**: `OrderRepository@{ "type": "entity" }` has a corresponding `02-OrderRepositoryBoundary/` sub-folder  
**When**: VR-3 check runs  
**Then**: VR-3 FAIL: violation names `OrderRepository` and its type `entity`

**Pass Criteria:**
- [x] `rule_results[VR-3].status` is `"FAIL"`
- [x] Violation `detail` includes participant name `OrderRepository` and type `entity`
- [x] `remediation` suggests removing the sub-folder or reclassifying the participant as `control`

---

### TC-T9-009: Invalid — actor-type participant has a sub-folder
**Rule**: VR-3  
**Given**: `Customer@{ "type": "actor" }` has a corresponding sub-folder  
**When**: VR-3 check runs  
**Then**: VR-3 FAIL identical to TC-T9-008 but type is `actor`

**Pass Criteria:**
- [x] `rule_results[VR-3].status` is `"FAIL"`
- [x] Violation `detail` includes type `actor`

---

## Category 4: VR-4 — Cohesive Responsibility (Group A)

### TC-T9-010: Warning — boundary participants span unrelated functional domains
**Rule**: VR-4  
**Given**: A box named "Processing Boundary" contains `UserAuthService@{ "type": "control" }` and `InventoryCache@{ "type": "entity" }` — authentication and inventory are unrelated domains; top-cluster coverage < 60 %  
**When**: VR-4 check runs  
**Then**: VR-4 WARNING: low cohesion flagged for the boundary

**Pass Criteria:**
- [x] `rule_results[VR-4].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` identifies "Processing Boundary" as low-cohesion
- [x] `remediation` suggests splitting into separate boundaries

---

### TC-T9-011: Valid — participants share a cohesive domain
**Rule**: VR-4  
**Given**: A box contains `OrderValidator@{ "type": "control" }`, `OrderRepository@{ "type": "entity" }`, `OrderAPI@{ "type": "boundary" }` — all order-domain  
**When**: VR-4 check runs  
**Then**: Rule PASS; top-cluster coverage ≥ 60 %

**Pass Criteria:**
- [x] `rule_results[VR-4].status` is `"PASS"`
- [x] No VR-4 violations

---

## Category 5: HR-1 — Parent-Child Link Integrity (Group B)

### TC-T9-012: Valid — sub-process main.md has working parent link
**Rule**: HR-1  
**Given**: `01-OrderProcessorBoundary/main.md` contains `**Parent Process**: [Order Management](../main.md)` and `../main.md` exists  
**When**: HR-1 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HR-1].status` is `"PASS"`
- [x] No violations

---

### TC-T9-013: Invalid — sub-process main.md has a broken parent link
**Rule**: HR-1  
**Given**: `01-OrderProcessorBoundary/main.md` contains `**Parent Process**: [Order Management](../main.md)` but `../main.md` does not exist  
**When**: HR-1 check runs  
**Then**: HR-1 FAIL: violation identifies the sub-folder and the broken relative path

**Pass Criteria:**
- [x] `rule_results[HR-1].status` is `"FAIL"`
- [x] Violation `file` references `01-OrderProcessorBoundary/main.md`
- [x] Violation `detail` includes the broken path `../main.md`
- [x] `remediation` matches the HR-1 entry in the Remediation Suggestions Reference table

---

## Category 6: HR-2 — Decomposed Participant Exists (Group B)

### TC-T9-014: Valid — sub-folder maps to a control-type participant in parent diagram
**Rule**: HR-2  
**Given**: Sub-folder `01-OrderProcessorBoundary/` exists; parent `collaboration.md` contains `OrderProcessor@{ "type": "control" }` (normalized name matches)  
**When**: HR-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[HR-2].status` is `"PASS"`
- [x] Normalization applied: ordinal prefix and `Boundary` suffix stripped; PascalCase compared case-insensitively

---

### TC-T9-015: Invalid — orphan sub-folder has no matching control participant in parent
**Rule**: HR-2  
**Given**: Sub-folder `02-PaymentGatewayBoundary/` exists but parent `collaboration.md` contains no participant named `PaymentGateway`  
**When**: HR-2 check runs  
**Then**: HR-2 FAIL: violation identifies orphan folder `02-PaymentGatewayBoundary`

**Pass Criteria:**
- [x] `rule_results[HR-2].status` is `"FAIL"`
- [x] Violation `detail` names the orphaned folder and states no matching `control`-type participant was found
- [x] `remediation` suggests removing or renaming the folder, or adding the participant to the parent diagram

---

## Category 7: HR-3, HR-4, HR-5, HR-6 — Structural Detail Rules (Group B)

### TC-T9-016: HR-3 Warning — broken relative link in breadcrumb
**Rule**: HR-3  
**Given**: `main.md` breadcrumb contains `[Root](../../main.md)` but `../../main.md` does not exist (extra `../` level)  
**When**: HR-3 check runs  
**Then**: HR-3 WARNING: violation identifies the file and broken link

**Pass Criteria:**
- [x] `rule_results[HR-3].status` is `"FAIL"` severity `WARNING`
- [x] Violation references the specific broken path

---

### TC-T9-017: HR-4 Warning — sub-folder missing from parent Sub-Processes section
**Rule**: HR-4  
**Given**: Parent `main.md` Sub-Processes section lists only `01-OrderProcessorBoundary`; `02-PaymentServiceBoundary/` folder also exists but is not listed  
**When**: HR-4 check runs  
**Then**: HR-4 WARNING: `02-PaymentServiceBoundary` omission flagged

**Pass Criteria:**
- [x] `rule_results[HR-4].status` is `"FAIL"` severity `WARNING`
- [x] Violation `detail` names the missing sub-folder
- [x] `remediation` refers to running `hierarchy-management` Sub-Processes table update

---

### TC-T9-018: HR-5 Error — non-conforming folder name
**Rule**: HR-5  
**Given**: A sub-folder named `orderprocessor/` (lowercase, no ordinal prefix, no `Boundary` suffix)  
**When**: HR-5 check runs  
**Then**: HR-5 FAIL: violation identifies the non-conforming folder name and the expected pattern

**Pass Criteria:**
- [x] `rule_results[HR-5].status` is `"FAIL"`
- [x] Violation `detail` references the regex `^\d{2}-[A-Za-z][A-Za-z0-9]*Boundary$`
- [x] `remediation` instructs renaming the folder to conform

---

### TC-T9-019: HR-6 Warning — hierarchy-metadata.json absent
**Rule**: HR-6  
**Given**: Target scope folder contains multiple sub-folders but no `hierarchy-metadata.json` file  
**When**: HR-6 check runs  
**Then**: HR-6 WARNING: absence flagged

**Pass Criteria:**
- [x] `rule_results[HR-6].status` is `"FAIL"` severity `WARNING`
- [x] In relaxed mode: WARNING (not ERROR)
- [x] In strict mode: treated as ERROR and reduces `overall_status` eligibility for `COMPLIANT`

---

## Category 8: EP-1 — Traceability Presence (Group C)

### TC-T9-020: Valid — collaboration.md contains inline R-citation
**Rule**: EP-1  
**Given**: `collaboration.md` contains the text `[R-306]` somewhere in the file  
**When**: EP-1 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[EP-1].status` is `"PASS"`
- [x] Single citation sufficient to pass

---

### TC-T9-021: Valid — collaboration.md has Source Requirements frontmatter block
**Rule**: EP-1  
**Given**: `collaboration.md` header contains `**Source Requirements**: [R-101], [R-102]`  
**When**: EP-1 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[EP-1].status` is `"PASS"`
- [x] Both citation forms (inline `[R-NNN]` and `**Source Requirements**:` block) accepted

---

### TC-T9-022: Invalid — collaboration.md has no traceability reference
**Rule**: EP-1  
**Given**: A valid Mermaid `sequenceDiagram` in `collaboration.md` with no `[R-` patterns and no `**Source Requirements**:` line  
**When**: EP-1 check runs  
**Then**: EP-1 FAIL: violation identifies the file and states no traceability reference found

**Pass Criteria:**
- [x] `rule_results[EP-1].status` is `"FAIL"`
- [x] Violation `file` references the offending `collaboration.md`
- [x] `remediation` matches EP-1 entry in remediation table

---

## Category 9: EP-2 — Abstraction Level Separation (Group C)

### TC-T9-023: Valid — no child-internal participants leak into parent diagram
**Rule**: EP-2  
**Given**: Parent `collaboration.md` lists `OrderProcessor@{ "type": "control" }` (this is the decomposed participant); child `01-OrderProcessorBoundary/collaboration.md` lists internal participants `ValidationEngine` and `PricingEngine`; parent does NOT list `ValidationEngine` or `PricingEngine`  
**When**: EP-2 check runs  
**Then**: Rule passes

**Pass Criteria:**
- [x] `rule_results[EP-2].status` is `"PASS"`
- [x] The decomposed control participant appearing in both parent and as a folder name is NOT flagged (expected relationship)

---

### TC-T9-024: Invalid — child-internal participant appears in parent diagram
**Rule**: EP-2  
**Given**: Parent `collaboration.md` lists BOTH `OrderProcessor@{ "type": "control" }` AND `ValidationEngine@{ "type": "control" }` — where `ValidationEngine` is an internal participant of child `01-OrderProcessorBoundary/collaboration.md` and does not exist as a standalone sub-folder in the parent scope  
**When**: EP-2 check runs  
**Then**: EP-2 FAIL: violation flags `ValidationEngine` as a child-level participant appearing in the parent

**Pass Criteria:**
- [x] `rule_results[EP-2].status` is `"FAIL"`
- [x] Violation `detail` identifies `ValidationEngine` as appearing in parent scope but belonging to child scope
- [x] `remediation` instructs removing the child participant from the parent and referencing the sub-process boundary as a single unit

---

## Category 10: EP-3 and EP-4 — Metadata and Annotation (Group C)

### TC-T9-025: EP-3 Warning — main.md missing Status and Last Updated
**Rule**: EP-3  
**Given**: A `main.md` that has no `**Status**:` field and no `<!-- Last Updated:` comment  
**When**: EP-3 check runs  
**Then**: EP-3 WARNING in relaxed mode; EP-3 ERROR in strict mode

**Pass Criteria:**
- [x] Relaxed: `rule_results[EP-3].status` is `"FAIL"` severity `WARNING`
- [x] Strict: `rule_results[EP-3].status` is `"FAIL"` severity `ERROR`
- [x] `remediation` matches EP-3 entry in remediation table

---

### TC-T9-026: EP-4 Warning — decomposed participant lacks annotation comment
**Rule**: EP-4  
**Given**: `collaboration.md` contains `OrderProcessor@{ "type": "control" }` with a corresponding `01-OrderProcessorBoundary/` sub-folder but no `%% decomposed:` comment on or near the participant declaration  
**When**: EP-4 check runs  
**Then**: EP-4 WARNING in relaxed mode

**Pass Criteria:**
- [x] Relaxed: `rule_results[EP-4].status` is `"FAIL"` severity `WARNING`
- [x] `remediation` instructs adding `%% decomposed: OrderProcessor → 01-OrderProcessorBoundary/collaboration.md` after the participant declaration
- [x] Strict: treated as `ERROR` per the strict vs. relaxed mode table

---

### TC-T9-027: EP-3 and EP-4 Pass — fully annotated main.md and collaboration.md
**Rules**: EP-3, EP-4  
**Given**: `main.md` contains `**Status**: Active` and `<!-- Last Updated: 2026-03-14 -->`; `collaboration.md` contains `%% decomposed: OrderProcessor → 01-OrderProcessorBoundary/collaboration.md`  
**When**: EP-3 and EP-4 checks run  
**Then**: Both pass

**Pass Criteria:**
- [x] `rule_results[EP-3].status` is `"PASS"`
- [x] `rule_results[EP-4].status` is `"PASS"`

---

## Category 11: Compliance Scoring and Overall Status

### TC-T9-028: COMPLIANT — all rules pass
**Requirement**: Scoring formula  
**Given**: A well-formed hierarchy where all 11 applicable rules pass; 0 errors; 0 warnings  
**When**: Score is calculated  
**Then**: `compliance_score = 100`, `overall_status = "COMPLIANT"`

**Pass Criteria:**
- [x] `summary.compliance_score` equals `100.0`
- [x] `summary.overall_status` equals `"COMPLIANT"`
- [x] `summary.failed_errors` equals `0`
- [x] `summary.failed_warnings` equals `0`

---

### TC-T9-029: NEEDS_ATTENTION — 2 error violations
**Requirement**: Scoring formula  
**Given**: 11 checks run; 2 FAIL on ERROR-severity rules (VR-1 and HR-1); all others pass  
**When**: Score is calculated  
**Then**: `compliance_score ≈ 81.8`, `overall_status = "NEEDS_ATTENTION"` (errors > 0, errors ≤ 3)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `2`
- [x] `summary.overall_status` equals `"NEEDS_ATTENTION"` (not `"NON_COMPLIANT"` since errors ≤ 3)
- [x] `summary.compliance_score` equals approximately `81.8`

---

### TC-T9-030: NON_COMPLIANT — more than 3 error violations
**Requirement**: Scoring formula  
**Given**: 11 checks run; 5 FAIL on ERROR-severity rules  
**When**: Score is calculated  
**Then**: `overall_status = "NON_COMPLIANT"` (errors > 3)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `5`
- [x] `summary.overall_status` equals `"NON_COMPLIANT"`

---

### TC-T9-031: SKIPPED rules excluded from scoring denominator
**Requirement**: Scoring formula  
**Given**: Scope is a single-file scan; VR-2, HR-1, HR-2, HR-3, HR-4, HR-6 are SKIPPED (no boxes, no sub-folders); 5 rules evaluated; all 5 pass  
**When**: Score is calculated  
**Then**: `total_checks = 5`; `compliance_score = 100`; SKIPPED rules do not appear in denominator

**Pass Criteria:**
- [x] `summary.total_checks` equals `5` (not `11`)
- [x] `summary.compliance_score` equals `100.0`
- [x] SKIPPED rule entries present in `rule_results` with `status = "SKIPPED"` but excluded from score

---

## Category 12: Strict vs. Relaxed Mode

### TC-T9-032: Relaxed mode (default) — WARNING violations do not block COMPLIANT status
**Requirement**: Strict vs. Relaxed Mode table  
**Given**: 11 checks; 0 errors; 2 warnings (EP-3 and EP-4 missing annotations); score = 81.8%  
**When**: Score and status calculated in relaxed mode  
**Then**: `overall_status = "MOSTLY_COMPLIANT"` (errors = 0, score < 90)

**Pass Criteria:**
- [x] `summary.failed_errors` equals `0`
- [x] `summary.overall_status` equals `"MOSTLY_COMPLIANT"` (not `"NON_COMPLIANT"`)
- [x] In relaxed mode: WARNING violations do not count as errors; they reduce score but not error count

---

### TC-T9-033: Strict mode — VR-4 cohesion threshold raised to 70%
**Requirement**: Strict vs. Relaxed Mode table  
**Given**: A boundary with top-cluster coverage of 65% (passes relaxed 60% threshold, fails strict 70% threshold)  
**When**: VR-4 check runs in strict mode  
**Then**: VR-4 FAIL WARNING in strict mode; VR-4 PASS in relaxed mode

**Pass Criteria:**
- [x] Strict: `rule_results[VR-4].status` is `"FAIL"` severity `WARNING`
- [x] Relaxed: `rule_results[VR-4].status` is `"PASS"`
- [x] Mode recorded in `report_metadata.mode`

---
