# T11 — Change Impact Analysis: Test Cases

**Skill**: `change-impact-analysis`
**Created**: March 14, 2026
**Last Updated**: March 14, 2026
**Total Test Cases**: 28

---

## Test Organisation

| Category | Tests | Rules Covered |
|----------|-------|--------------|
| CI-1: Parent Reference Impact | TC-01 – TC-04 | CI-1 |
| CI-2: Child Navigation Impact | TC-05 – TC-08 | CI-2 |
| CI-3: Participant Propagation Impact | TC-09 – TC-11 | CI-3 |
| CI-4: Hierarchy Index Impact | TC-12 – TC-13 | CI-4 |
| CI-5: Side-Document Impact | TC-14 – TC-15 | CI-5 |
| CR-1: Requirement-to-Artifact Mapping | TC-16 – TC-18 | CR-1 |
| CR-2: Requirement Boundary Impact | TC-19 – TC-21 | CR-2 |
| CR-3: Downstream Requirement Propagation | TC-22 – TC-24 | CR-3 |
| Scoring & Risk Classification | TC-25 – TC-26 | Aggregation |
| What-If vs Apply Mode | TC-27 – TC-28 | Mode behaviour |

---

## Group CI — Artifact-Level Impact Rules

### CI-1: Parent Reference Impact

---

**TC-01**: Boundary folder rename detected in parent Sub-Processes table

| Field | Value |
|-------|-------|
| **Category** | CI-1 |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | Parent `main.md` has a `## Sub-Processes` table row: `[Order Boundary](01-OrderBoundary/main.md)`. The folder has been renamed to `01-NewOrderBoundary`. |
| **Expected** | Impact record for parent `main.md` with `rule_id: CI-1`, `severity: HIGH`, `auto_fixable: true`. Remediation states update the link from `01-OrderBoundary/main.md` to `01-NewOrderBoundary/main.md`. |
| **Expected Risk** | HIGH |

---

**TC-02**: Boundary folder deletion detected in parent Sub-Processes table

| Field | Value |
|-------|-------|
| **Category** | CI-1 |
| **Priority** | High |
| **Input** | `change_type: boundary-restructure`, `target: orgModel/P1/02-PaymentBoundary/`, `root: orgModel/P1/` |
| **Setup** | Parent `main.md` references `02-PaymentBoundary/main.md` in the Sub-Processes table. The folder no longer exists. |
| **Expected** | Impact record for parent `main.md` with `rule_id: CI-1`, `severity: HIGH`, remediation states remove the dangling row. |
| **Expected Risk** | HIGH |

---

**TC-03**: Decomposition comment in parent collaboration.md references changed folder

| Field | Value |
|-------|-------|
| **Category** | CI-1 |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | Parent `collaboration.md` contains `%% decomposed: OrderService → 01-OrderBoundary`. Folder renamed to `01-NewOrderBoundary`. |
| **Expected** | Impact record for parent `collaboration.md` with `rule_id: CI-1`, `severity: HIGH`, `auto_fixable: false` (comment update requires human review of diagram semantics). |
| **Expected Risk** | HIGH |

---

**TC-04**: No parent reference impact when change point is root level

| Field | Value |
|-------|-------|
| **Category** | CI-1 |
| **Priority** | Medium |
| **Input** | `change_type: participant-change`, `target: RootService`, `root: orgModel/P1/` |
| **Setup** | Change occurs at Level 0 (root). No parent folder exists. |
| **Expected** | No CI-1 impact records generated. CI-2 records may still be generated for children. |
| **Expected Risk** | MEDIUM or lower |

---

### CI-2: Child Navigation Impact

---

**TC-05**: Child Parent Process link broken by boundary rename

| Field | Value |
|-------|-------|
| **Category** | CI-2 |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | `01-OrderBoundary/01-FulfillmentBoundary/main.md` contains `**Parent Process**: [Order Boundary](../main.md)`. The grandchild breadcrumb also traverses the renamed folder. |
| **Expected** | Impact records for `01-FulfillmentBoundary/main.md`: `CI-2` HIGH for `**Parent Process**` link, `CI-2` HIGH for breadcrumb segment. `auto_fixable: true` for both. |
| **Expected Risk** | HIGH |

---

**TC-06**: Multi-level breadcrumb cascade — all descendants affected

| Field | Value |
|-------|-------|
| **Category** | CI-2 |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | Hierarchy: `P1/` → `01-OrderBoundary/` → `01-FulfillmentBoundary/` → `01-PackagingBoundary/`. All three descendants have breadcrumbs traversing `01-OrderBoundary`. |
| **Expected** | Three CI-2 HIGH impact records (one per descendant). All `auto_fixable: true`. Report's `total_affected_files` ≥ 3. |
| **Expected Risk** | HIGH |

---

**TC-07**: Depth limit restricts downward traversal

| Field | Value |
|-------|-------|
| **Category** | CI-2 |
| **Priority** | Medium |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/`, `--depth 1` |
| **Setup** | Same hierarchy as TC-06 (3 descendant levels). |
| **Expected** | Only 1 CI-2 impact record generated (direct child only). Grandchild and great-grandchild are not scanned. Report notes depth limit was applied. |
| **Expected Risk** | HIGH (at least one HIGH impact found) |

---

**TC-08**: No child navigation impact when boundary has no sub-folders

| Field | Value |
|-------|-------|
| **Category** | CI-2 |
| **Priority** | Low |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/03-NotificationBoundary/`, `root: orgModel/P1/` |
| **Setup** | `03-NotificationBoundary` is a leaf node with no child sub-folders. |
| **Expected** | No CI-2 impact records. CI-1 impact record generated for parent. Overall risk remains HIGH (due to CI-1). |
| **Expected Risk** | HIGH |

---

### CI-3: Participant Propagation Impact

---

**TC-09**: Control participant rename triggers child actor label impact

| Field | Value |
|-------|-------|
| **Category** | CI-3 |
| **Priority** | Medium |
| **Input** | `change_type: participant-change`, `target: OrderService`, `root: orgModel/P1/` |
| **Setup** | `OrderService` is a `control`-type participant at Level 0. Level 1 `collaboration.md` contains external `actor` named `OrderService` outside all boxes. |
| **Expected** | CI-3 MEDIUM impact record for Level 1 `collaboration.md`: actor label must be updated. If sub-folder name is `01-OrderServiceBoundary`, additional HIGH CI-3 record noting folder rename required. |
| **Expected Risk** | HIGH (if folder rename required) or MEDIUM |

---

**TC-10**: Non-control participant rename does not trigger sub-folder impact

| Field | Value |
|-------|-------|
| **Category** | CI-3 |
| **Priority** | Medium |
| **Input** | `change_type: participant-change`, `target: CustomerPortal`, `root: orgModel/P1/` |
| **Setup** | `CustomerPortal` is an `actor`-type participant at Level 0. No sub-folder named `CustomerPortalBoundary` exists. |
| **Expected** | No CI-3 impact records referencing a sub-folder rename. CI-5 LOW impact may exist if `process.md` references the participant. |
| **Expected Risk** | LOW or NONE |

---

**TC-11**: Participant rename propagation stops when no matching child actor found

| Field | Value |
|-------|-------|
| **Category** | CI-3 |
| **Priority** | Low |
| **Input** | `change_type: participant-change`, `target: LogisticsService`, `root: orgModel/P1/` |
| **Setup** | `LogisticsService` is a `control`-type participant at Level 0 but its sub-process folder `01-LogisticsBoundary` does not contain a matching external actor in `collaboration.md`. |
| **Expected** | CI-3 MEDIUM impact record flagging the missing actor alignment as an inconsistency. Remediation recommends adding the external actor or verifying whether the sub-folder relationship is intentional. |
| **Expected Risk** | MEDIUM |

---

### CI-4: Hierarchy Index Impact

---

**TC-12**: Boundary rename invalidates hierarchy-index.md rows

| Field | Value |
|-------|-------|
| **Category** | CI-4 |
| **Priority** | Medium |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | `hierarchy-index.md` at root lists `01-OrderBoundary` in three table rows (one per level where it appears as a path segment). |
| **Expected** | CI-4 MEDIUM impact record for `hierarchy-index.md`, noting 3 affected rows. `auto_fixable: true` (full regeneration). |
| **Expected Risk** | HIGH (elevated by CI-1/CI-2 records too) |

---

**TC-13**: No hierarchy index impact when hierarchy-index.md absent

| Field | Value |
|-------|-------|
| **Category** | CI-4 |
| **Priority** | Low |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P2/01-ProcurementBoundary/`, `root: orgModel/P2/` |
| **Setup** | `orgModel/P2/hierarchy-index.md` does not exist. |
| **Expected** | No CI-4 impact record generated. Overall impact still reflects CI-1/CI-2 findings. |
| **Expected Risk** | HIGH (from other rules) |

---

### CI-5: Side-Document Impact

---

**TC-14**: Process.md references changed boundary name

| Field | Value |
|-------|-------|
| **Category** | CI-5 |
| **Priority** | Low |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/` |
| **Setup** | `01-OrderBoundary/process.md` contains a link and a heading that reference `OrderBoundary`. |
| **Expected** | CI-5 LOW impact record for `process.md` noting 2 occurrences of the changed name. `auto_fixable: false`. |
| **Expected Risk** | HIGH (from CI-1/CI-2; CI-5 adds LOW count) |

---

**TC-15**: Domain-model.md reference to renamed participant

| Field | Value |
|-------|-------|
| **Category** | CI-5 |
| **Priority** | Low |
| **Input** | `change_type: participant-change`, `target: OrderService`, `root: orgModel/P1/` |
| **Setup** | `01-OrderBoundary/domain-model.md` contains a class named `OrderService`. |
| **Expected** | CI-5 LOW impact record for `domain-model.md`. Remediation notes the class name may need manual update. |
| **Expected Risk** | MEDIUM or HIGH |

---

## Group CR — Requirement Change Tracing Rules

### CR-1: Requirement-to-Artifact Mapping

---

**TC-16**: Requirement ID found in collaboration.md annotations

| Field | Value |
|-------|-------|
| **Category** | CR-1 |
| **Priority** | High |
| **Input** | `change_type: requirement-change`, `target: R-302`, `root: orgModel/P1/` |
| **Setup** | Three `collaboration.md` files across three levels contain `[R-302]` inline annotations. One `main.md` also references `[R-302]` in a requirements section. |
| **Expected** | Four CR-1 HIGH impact records (one per file), each with file path and matching line numbers. |
| **Expected Risk** | HIGH |

---

**TC-17**: Requirement ID found only in main.md narrative

| Field | Value |
|-------|-------|
| **Category** | CR-1 |
| **Priority** | High |
| **Input** | `change_type: requirement-change`, `target: R-410`, `root: orgModel/P1/` |
| **Setup** | Requirement `R-410` appears only in two `main.md` files in their description paragraphs (not `collaboration.md`). |
| **Expected** | Two CR-1 HIGH impact records for the `main.md` files. No collaboration diagram records. |
| **Expected Risk** | HIGH |

---

**TC-18**: Requirement ID not found in any artifact

| Field | Value |
|-------|-------|
| **Category** | CR-1 |
| **Priority** | Medium |
| **Input** | `change_type: requirement-change`, `target: R-999`, `root: orgModel/P1/` |
| **Setup** | No file in the hierarchy references `R-999`. |
| **Expected** | No CR-1 impact records. Console and report output: "No affected artifacts found — change appears isolated." Risk = NONE. |
| **Expected Risk** | NONE |

---

### CR-2: Requirement Boundary Impact

---

**TC-19**: Boundary-type participant annotated with requirement ID

| Field | Value |
|-------|-------|
| **Category** | CR-2 |
| **Priority** | High |
| **Input** | `change_type: requirement-change`, `target: R-302`, `root: orgModel/P1/` |
| **Setup** | In `01-OrderBoundary/collaboration.md`, the `boundary`-type participant `OrderEntry` has `@{ "note": "Implements R-302 single-actor rule" }`. |
| **Expected** | CR-2 HIGH impact record identifying `OrderEntry` as implementing R-302 with constraint `single-actor rule`. Remediation notes the boundary constraint may change. |
| **Expected Risk** | HIGH |

---

**TC-20**: Multiple boundary participants across levels implement same requirement

| Field | Value |
|-------|-------|
| **Category** | CR-2 |
| **Priority** | High |
| **Input** | `change_type: requirement-change`, `target: R-302`, `root: orgModel/P1/` |
| **Setup** | Two boundary participants at Level 1 and one at Level 2 all have annotations referencing `R-302`. |
| **Expected** | Three CR-2 HIGH impact records. Each record identifies the participant name, hierarchy level, and constraint type. |
| **Expected Risk** | HIGH |

---

**TC-21**: Requirement referenced in comment only — no annotation found

| Field | Value |
|-------|-------|
| **Category** | CR-2 |
| **Priority** | Medium |
| **Input** | `change_type: requirement-change`, `target: R-305`, `root: orgModel/P1/` |
| **Setup** | `R-305` appears in a `%% Requirement: R-305 — boundary-first reception` comment in a `collaboration.md` but is not in any `@{ ... }` participant annotation. |
| **Expected** | CR-2 MEDIUM impact record for the file, noting the requirement is referenced in a diagram comment but no participant-level annotation was found. Remediation recommends manual review. |
| **Expected Risk** | MEDIUM |

---

### CR-3: Downstream Requirement Propagation

---

**TC-22**: Downstream levels reference same root requirement

| Field | Value |
|-------|-------|
| **Category** | CR-3 |
| **Priority** | Medium |
| **Input** | `change_type: requirement-change`, `target: R-302`, `root: orgModel/P1/` |
| **Setup** | Hierarchy: Level 0 references `[R-302]`; Level 1 sub-process references `[R-302a]` (derived); Level 2 sub-process references `[R-302b]` (derived). |
| **Expected** | CR-3 MEDIUM impact records for Level 1 (`R-302a`) and Level 2 (`R-302b`) files, propagating from the root requirement. |
| **Expected Risk** | HIGH (due to CR-1 and CR-2 HIGH records at Level 0) |

---

**TC-23**: Downstream propagation stops at level without matching reference

| Field | Value |
|-------|-------|
| **Category** | CR-3 |
| **Priority** | Medium |
| **Input** | `change_type: requirement-change`, `target: R-304`, `root: orgModel/P1/` |
| **Setup** | Level 0 references `[R-304]`. Level 1 has no reference to `R-304` or any `R-304x` variant. Level 2 does reference `[R-304]` directly. |
| **Expected** | CR-3 MEDIUM impact record for Level 2 (direct match). No record for Level 1 (no match). Note in report that propagation chain has a gap at Level 1. |
| **Expected Risk** | HIGH |

---

**TC-24**: Derived sub-requirement pattern matching (R-[root][letter])

| Field | Value |
|-------|-------|
| **Category** | CR-3 |
| **Priority** | Medium |
| **Input** | `change_type: requirement-change`, `target: R-307`, `root: orgModel/P1/` |
| **Setup** | Files reference `R-307`, `R-307a`, `R-307b`, and `R-307c` across four hierarchy levels. |
| **Expected** | CR-3 MEDIUM impact records for each file referencing `R-307a`, `R-307b`, `R-307c`. The root `R-307` file also has a CR-1 HIGH record. Total: 4 impact records. |
| **Expected Risk** | HIGH |

---

## Scoring and Risk Classification

---

**TC-25**: Risk classification — CRITICAL threshold

| Field | Value |
|-------|-------|
| **Category** | Aggregation |
| **Priority** | High |
| **Input** | `change_type: boundary-restructure`, `target: orgModel/P1/01-CoreBoundary/`, `root: orgModel/P1/` |
| **Setup** | Change to a central boundary with 5 children and 2 parent layers. Produces ≥ 5 HIGH impact records and ≥ 10 total affected files. |
| **Expected** | `overall_risk: CRITICAL`. Console displays `🚨` indicator. `total_affected_files` ≥ 10. |
| **Expected Risk** | CRITICAL |

---

**TC-26**: Risk classification — NONE when change is truly isolated

| Field | Value |
|-------|-------|
| **Category** | Aggregation |
| **Priority** | Medium |
| **Input** | `change_type: participant-change`, `target: InternalHelper`, `root: orgModel/P1/` |
| **Setup** | `InternalHelper` is an `entity`-type participant inside a box in a leaf `collaboration.md`. No other files reference it. No sub-folder exists for it. `process.md` and `domain-model.md` do not mention it. |
| **Expected** | No impact records. `overall_risk: NONE`. Console displays `✅`. |
| **Expected Risk** | NONE |

---

## What-If vs Apply Mode

---

**TC-27**: What-if mode does not modify any files

| Field | Value |
|-------|-------|
| **Category** | Mode |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/`, `root: orgModel/P1/`, `--mode what-if` (default) |
| **Setup** | Multiple HIGH impacts detected (CI-1, CI-2, CI-4). All have `auto_fixable: true`. |
| **Expected** | Report files (`change-impact-report.md`, `change-impact-report.json`) are created. No `main.md`, `collaboration.md`, or `hierarchy-index.md` files are modified. `auto_fixed: 0` in summary. |
| **Mode** | what-if |

---

**TC-28**: Apply mode repairs navigational artifacts but not structural ones

| Field | Value |
|-------|-------|
| **Category** | Mode |
| **Priority** | High |
| **Input** | `change_type: boundary-rename`, `target: orgModel/P1/01-OrderBoundary/ → 01-NewOrderBoundary/`, `root: orgModel/P1/`, `--mode apply` |
| **Setup** | CI-1 (parent Sub-Processes link), CI-2 (two child `**Parent Process**` links), CI-4 (hierarchy-index.md). CI-5 `process.md` reference also flagged. |
| **Expected** | CI-1 fix applied: parent `main.md` Sub-Processes link updated. CI-2 fixes applied: both child `main.md` parent links updated. CI-4 fix applied: `hierarchy-index.md` regenerated. CI-5 NOT auto-fixed (not in allowlist). `auto_fixed: 4` in summary. Report produced. |
| **Mode** | apply |

---

*End of T11 test cases — 28 total.*
