# T04 — Update Stakeholder-Facing Skills for Role-Based Solo Input

**Task ID**: T04
**Phase**: Phase 2 - Orchestration
**Priority**: P1-High
**Estimated Effort**: 2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22

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
- [ ] `process-w5h/SKILL.md` updated with mode-conditional stakeholder interview guidance
- [ ] `requirements-sanitize/SKILL.md` Definition-of-Done checklist updated with mode-conditional validation
- [ ] `requirements-ingest/SKILL.md` reviewed and updated if it contains similar assumptions
- [ ] "break out of solo mode" guidance present in all three

## Dependencies

### Prerequisites
- **T01** — mode definitions to reference

### Blocks
- None (parallel-safe with T03, T05)
