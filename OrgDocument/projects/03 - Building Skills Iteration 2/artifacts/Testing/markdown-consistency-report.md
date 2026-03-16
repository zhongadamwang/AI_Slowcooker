# Markdown & Format Consistency Report

**Date**: March 15, 2026  
**Scope**: All 31 SKILL.md files  
**Overall Result**: ⚠️ WARNING — 5 format violations found (4 HIGH, 1 MEDIUM)

---

## Summary

| Check | Result | Details |
|-------|--------|---------|
| Code fence format | ⚠️ WARNING | 4 skills use 4-backtick fence instead of standard 3-backtick |
| Frontmatter presence | ✅ PASS | 31/31 have `name:` and `description:` in frontmatter |
| Section headings | ⚠️ WARNING | 1 skill uses non-standard section names |
| JSON schema compliance | ✅ PASS | All output JSON structures validated |
| File naming conventions | ✅ PASS | All files follow kebab-case convention |
| Cross-skill references | ✅ PASS | All skill-to-skill references resolve correctly |
| Traceability format | ✅ PASS | Requirement IDs consistent (R-xxx, G-xxx, T-xxx) |

---

## Code Fence Format

**Standard**: SKILL.md files should begin with ` ```skill` (3 backticks) and end with ` ``` `.

### Violations (HIGH)

| Skill | Opening Fence | Expected | Impact |
|-------|--------------|---------|--------|
| hierarchy-management | `````skill` (4 backticks) | ` ```skill` | VS Code Copilot may fail to parse as skill definition |
| hierarchy-validation | `````skill` (4 backticks) | ` ```skill` | VS Code Copilot may fail to parse as skill definition |
| documentation-automation | `````skill` (4 backticks) | ` ```skill` | VS Code Copilot may fail to parse as skill definition |
| change-impact-analysis | `````skill` (4 backticks) | ` ```skill` | VS Code Copilot may fail to parse as skill definition |

**Correct examples** (3-backtick format — 27 skills):
```
```skill
---
name: diagram-generatecollaboration
...
---
```
```

**Root cause**: These 4 skills were created during Project 3 development (Tasks T5, T10, T11, T12). It is likely the skill-creator SKILL.md template was inadvertently using 4-backtick fencing at the time, or the files were created with code fences nested inside a markdown document.

**Remediation**: In each affected SKILL.md, change line 1 from `````skill to ` ```skill` and update the matching closing fence at the end of file.

---

## Section Heading Consistency

**Standard headings used by 30/31 skills**:
- `## Intent`
- `## Inputs`
- `## Outputs`
- `## Usage Examples` (or `## Usage`)

### Violations (MEDIUM)

| Skill | Non-standard headings | Standard equivalent |
|-------|----------------------|-------------------|
| requirements-ingest | `## Core Function`, `## Usage` | `## Intent`, `## Inputs`, `## Outputs` |

Note: `requirements-ingest` pre-dates the EDPS standard section naming convention and was created with a Python-script-oriented documentation style. It is functionally complete.

---

## Frontmatter Completeness

All 31 SKILL.md files contain required frontmatter fields:

| Field | Present | Count |
|-------|---------|-------|
| `name:` | ✅ | 31/31 |
| `description:` | ✅ | 31/31 |
| `license:` | ✅ (most) | ~29/31 |

---

## JSON Output Schema Compliance

All skills producing JSON output were validated against their declared schemas. No violations found.

Checked schemas for:
- requirements-ingest (requirements.json)
- goals-extract (goals.json)
- domain-extractconcepts (concepts.json)
- plan-derivetasks (task-breakdown.json)
- diagram-generatecollaboration (boundary-validation-report.json)
- hierarchy-management (hierarchy-metadata.json)
- hierarchy-validation (hierarchy-validation-report.json)
- edps-compliance (edps-compliance-report.json)
- change-impact-analysis (change-impact-report.json with `normalized_risk_level`)
- migration-tools (migration-output.json)

---

## File Naming Conventions

All SKILL.md files follow kebab-case naming. All output files declared in SKILL.md specifications follow the naming patterns:
- `[concept]-[type].[ext]` (e.g., `hierarchy-validation-report.json`)
- `[project]-[artifact].[ext]` (e.g., `integration-test-report.md`)

No violations found.

---

## Cross-Skill Reference Validation

All inter-skill references audited:

| Reference | From skill | To skill | Resolution |
|-----------|-----------|---------|-----------|
| VR-1–VR-4 delegation | edps-compliance | diagram-generatecollaboration | ✅ Resolves (T18) |
| HR-1/3/4/5 delegation | edps-compliance | hierarchy-validation | ✅ Resolves (T19) |
| Stub file contract | hierarchy-management | documentation-automation | ✅ Resolves (T20) |
| normalized_risk_level | change-impact-analysis | change-management | ✅ Resolves (T21) |
| Hierarchy guard | orgmodel-update | documentation-automation | ✅ Resolves (T22) |
| Skills catalog | edps-skill-navigator | All 31 skills | ✅ All registered (T14) |

---

## Terminology Consistency

Cross-skill terminology audit against `OrgDocument/orgModel/01 - Skill Development Process/vocabulary.md`:

| Term | Consistent | Notes |
|------|-----------|-------|
| "boundary" | ✅ | Used uniformly as folder/participant grouping concept |
| "control" (participant type) | ✅ | Used uniformly as decomposable participant stereotype |
| "actor", "entity" (participant types) | ✅ | Consistent across diagram-generatecollaboration, hierarchy-management, hierarchy-validation |
| "traceability" vs "trace" | ✅ | "traceability" used consistently |
| "requirement ID" format (R-xxx) | ✅ | Consistent across all requirements-related skills |
| "normalized_risk_level" | ✅ | New term; defined in change-impact-analysis, consumed by change-management |

16 new hierarchical terms added to vocabulary.md in T15 (e.g., "decomposition eligibility", "hierarchy metadata", "stub file"). All 16 now used consistently.

---

## Recommendations

1. **Fix 4-backtick code fences** in 4 skills (see Code Fence Format section above). Priority: HIGH.

2. **Normalise requirements-ingest headers** — add standard `## Intent`, `## Inputs`, `## Outputs`. Priority: MEDIUM.

3. **Update skill-creator SKILL.md** — explicitly document the 3-backtick ` ```skill` as a **required** format rule, not just a recommendation. This prevents future deviations when creating new skills.

4. **Add format lint check to integration-testing Phase 1** — automatically detect: (a) non-3-backtick opening, (b) missing standard section headings. This would have caught the 4-backtick issue earlier in the development cycle.

---

*Generated by integration-testing skill v2.0 — March 15, 2026*
