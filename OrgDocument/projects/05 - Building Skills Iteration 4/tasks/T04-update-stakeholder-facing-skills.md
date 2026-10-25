# T04 — Update Stakeholder-Facing Skills for Role-Based Solo Input

**Task ID**: T04
**Phase**: Phase 2 - Orchestration
**Priority**: P1-High
**Estimated Effort**: 2 days
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22
**Completed**: 2026-10-22

## Description

Several skills assume a live stakeholder interview or sign-off loop baked into their instructions, not just their gates: `process-w5h` ("Must complete stakeholder interviews before assessment"), `requirements-sanitize` (Definition-of-Done requires validation "by a business stakeholder"), and `requirements-ingest`. Update these skills' own SKILL.md instructions (not just gates) so solo-mode guidance reflects role-based self-input instead of implying a mandatory external interview.

## Objectives

- Update `process-w5h`, `requirements-sanitize`, `requirements-ingest` SKILL.md files to add mode-aware guidance in their "Usage"/"Intent" sections
- Ensure stakeholder role outputs (primary/secondary stakeholders, etc.) are always captured as roles — this doesn't change between modes, only the *confirmation mechanism* changes
- Clarify that in `solo` mode, the developer plays each role in turn when producing analysis, and explicitly notes which role lens was used per statement where ambiguity could matter

## Detailed Requirements

### Functional Requirements
- **FR-04.1**: `process-w5h` — rewrite "Must complete stakeholder interviews before assessment" as a mode-conditional: traditional → interview required; solo → developer role-plays each identified stakeholder role and documents assumptions inline
- **FR-04.2**: `requirements-sanitize` — Definition-of-Done item "validated by a business stakeholder" becomes: traditional → external validation; solo → developer self-validates using the business-stakeholder lens, flags any statement they're not confident role-playing correctly for later real-stakeholder check-in
- **FR-04.3**: Add a "when to break out of solo mode" guidance note to all three skills — i.e., even in solo mode, genuinely ambiguous or high-stakes business decisions should still prompt the developer to reach out to a real stakeholder (per the source material's "developer is responsible to reach out... for feedback and clarification")

### Technical Requirements
- **TR-04.1**: No new gate check types here (that's T03) — this task is skill *instruction* text only
- **TR-04.2**: Keep changes additive/backward compatible — traditional-mode guidance stays exactly as-is

## Acceptance Criteria

### Definition of Done
- [x] `process-w5h/SKILL.md` updated with mode-conditional stakeholder interview guidance
- [x] `requirements-sanitize/SKILL.md` Definition-of-Done checklist updated with mode-conditional validation
- [x] `requirements-ingest/SKILL.md` reviewed and updated if it contains similar assumptions
- [x] "break out of solo mode" guidance present in all three

## Dependencies

### Prerequisites
- **T01** — mode definitions to reference

### Blocks
- None (parallel-safe with T03, T05)

---

## Completion Notes

**Completed**: 2026-10-22

### Changes Made

- **`.github/skills/process-w5h/SKILL.md`**:
  - "Dependencies and Constraints" — "Must complete stakeholder interviews before assessment" rewritten as mode-conditional: traditional keeps the interview requirement; solo has the developer role-play each stakeholder perspective and document the role lens used per assumption inline
  - "Quality Assurance" — "Regular checkpoint reviews with stakeholders" made mode-conditional, cross-referencing the `stakeholder_confirmation` gate check from T03
  - New **Mode-Conditional Stakeholder Engagement** section (after the WHO Analysis Prompt): clarifies stakeholders are always identified by role in both modes (unchanged), and describes the solo-mode role-play + inline assumption documentation pattern, with a worked example
  - New **When to Break Out of Solo Mode** subsection: three concrete triggers (genuine ambiguity, real external authority, high-stakes/irreversible decisions) plus how to document an escalation when it happens

- **`.github/skills/requirements-sanitize/SKILL.md`**:
  - Step 5 (sanitization report) — "Recommended follow-up actions" example made mode-conditional: solo mode has the developer self-validate directly and log it as a self-attestation; only genuinely uncertain items still get recommended for real-stakeholder follow-up
  - Quality Checks Definition-of-Done — the "validated by a business stakeholder" item and the `FLAG` resolution item both made mode-conditional (FR-04.2)
  - New **When to Break Out of Solo Mode** subsection: three triggers specific to this skill's context (genuinely ambiguous `FLAG` items, statements with real financial/legal/compliance consequences, and sanitization-report follow-ups that already call for stakeholder validation)

- **`.github/skills/requirements-ingest/SKILL.md`**:
  - Reviewed per FR-04.3/DoD item 3 — **no changes made**. Grepped for stakeholder/interview/approval/confirm language; none found. This skill's inputs/outputs are purely about document normalization and traceability, with no stakeholder-confirmation assumption baked into its instructions. Noted here rather than silently skipped so the "reviewed and updated if needed" criterion is traceable.

### Key Decisions

- Kept all mode-conditional text **additive** (TR-04.2) — traditional-mode guidance reads exactly as it did before in every edited section; solo-mode guidance is inserted alongside it, not replacing it
- Used a consistent **"When to Break Out of Solo Mode"** subsection pattern across both edited skills so the triggers are easy to find and compare, even though the specific triggers differ per skill's content (W5H stakeholder analysis vs. requirements sanitization)
- Did not touch gate.json files in this task (TR-04.1) — that mechanism-level work is T03's scope; this task is instruction text only, as scoped
- `requirements-ingest/SKILL.md` was confirmed clean via `grep -n -i "stakeholder\|interview\|sign.off\|approval\|confirm"` with zero matches, rather than assumed clean

### Next Steps for Integration

- **T05**: Introduce the "real external stakeholder" flag referenced here (in process-w5h's break-out guidance) as a formal concept, and apply the same mode-conditional pattern to `change-management` and `project-planning-tracking`
- **T06**: The end-to-end validation walkthrough should exercise both `process-w5h` and `requirements-sanitize` in solo mode to confirm the self-attestation/self-validation guidance reads naturally in practice
