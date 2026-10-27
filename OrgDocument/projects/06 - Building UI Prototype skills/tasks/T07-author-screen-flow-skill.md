# T07 — Author screen-generateflow Skill (Interaction Flow Diagrams)

**Task ID**: T07
**Phase**: Phase 2 - Generation Pipeline
**Priority**: P0-Critical
**Estimated Effort**: 1 day
**Status**: Completed ✅
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-27
**Completed**: 2026-10-27

## Description

Implements R-603 (Interaction Flow Modeling) — gives the screen set a connective narrative (e.g., "Login → Dashboard → Order Detail"), reusing `diagram-generatecollaboration`'s existing Mermaid conventions rather than inventing a new diagramming approach.

## Objectives

- Author the flow generation skill producing Mermaid interaction-flow diagrams across the screen set

## Detailed Requirements

### Functional Requirements
- **FR-07.1**: Flow diagram's edges correspond to the actual navigation implemented in T06's mockups
- **FR-07.2**: Diagram style/syntax is consistent with `diagram-generatecollaboration`'s existing patterns

### Technical Requirements
- **TR-07.1**: Consistency between flow diagram and mockup is manually verified in MVP (automated check is the Phase 2 Enhancement feature, R-603a) — make this an explicit, non-skippable verification step in this task, not an afterthought

## Acceptance Criteria

- [x] SKILL.md authored
- [x] Flow diagram generated for a test screen set
- [x] Manual verification performed confirming diagram edges match actual mockup transitions

## Dependencies

### Prerequisites
- **T04** — needs the screen set
- **T06** — needs actual mockup transitions to verify against

### Blocks
- T08 (design document summarizes flows)

---

## Completion Notes

**Completed**: 2026-10-27

### Changes Made

- **`.github/skills/screen-generateflow/SKILL.md`** (new, v1.0.0, skill_id S36): the pipeline's consistency-anchoring skill — its entire design centers on "the mockup is ground truth," not the diagram. Key design points:
  - **Edges extracted only from real `<a href>` links in generated mockups**, never from the screen inventory's purposes or the original requirements' implied flow — this is the literal mechanism satisfying FR-07.1, not just a stated intention
  - **`flowchart LR` chosen over `sequenceDiagram`**, a deliberate divergence from `diagram-generatecollaboration`'s primary style — justified because screen-to-screen navigation isn't a time-ordered message exchange between system components (actors/boundaries/controls/entities), it's a node-and-edge navigation graph, which flowchart models more naturally. Reuses `diagram-generatecollaboration`'s general Mermaid styling conventions while choosing the appropriate diagram *type* for this skill's actual content, rather than forcing sequence-diagram syntax onto content it doesn't fit.
  - **Output is consolidated at the project level** (`interaction-flows.md`), explicitly *not* per-screen — correctly distinguishing this from `layout-spec.md`/`mockup.html` (genuinely per-screen entities) since a flow inherently spans multiple screens
  - **Verification Log made mandatory and non-skippable** (Step 4), not just a nice-to-have — directly operationalizes TR-07.1's "make this an explicit, non-skippable verification step" instruction as a concrete table every edge must have a row in, rather than leaving "verify it" as unenforceable prose
  - **Step 5 explicitly handles divergence resolution**: if the mockup and an assumed/planned edge disagree, the mockup wins (fix the diagram) unless the mockup itself has a bug (fix the mockup) — either way, never publish a known-divergent diagram
  - Explicitly previews the **Phase 2 relationship to R-603a**: automating this skill's manual verification is exactly what R-603a should do, not a redesign from scratch — pointing future Phase 2 work at reusing this skill's own verification logic

- **`.github/skills/screen-generateflow/gate.json`** (new, skill_id S36, confirmed unique): 5 checks — 3 hard (`interaction_flows_exists`, `mermaid_diagram_present` checking for `flowchart` syntax specifically, `verification_log_present` enforcing TR-07.1's non-skippable step at the gate level too), 2 soft (`no_sequence_diagram_misuse`, `id_format_valid`)

- **`.github/skills/README.md`**: S11 section extended with `screen-generateflow`'s row
- **`.github/skills/INDEX.md`**: skill count 35→36, version 2.4.0→2.5.0, new changelog entry explaining the flowchart-vs-sequenceDiagram choice and the manual-verification-now/automated-later (R-603a) relationship

### Key Decisions

- **flowchart over sequenceDiagram**: the single most notable technical decision in this task — diverges from `diagram-generatecollaboration`'s dominant style specifically because this skill's content (screen navigation) doesn't fit that style's semantics (time-ordered inter-component messaging). Reusing conventions means reusing *principles* (clear labels, traceability, focused diagrams over monoliths) even when the specific diagram type differs.
- **Verification Log as mandatory gate-checked evidence**, not just a documented best practice — both the SKILL.md's own process (Step 4) and the gate.json's `verification_log_present` check enforce this at two layers, so the requirement can't quietly be skipped by an implementer in a hurry
- **No automated consistency checking in this task** — correctly left to R-603a (Phase 2 Enhancement, per `scope-analysis.md`); this task's job was to make manual verification rigorous and logged, not to prematurely build the automation

### Next Steps for Integration

- **T08** (`screen-assembledocument`): summarizes/references `interaction-flows.md` in the consolidated design document — should link to it, not duplicate its diagrams inline, consistent with the same "reference, don't duplicate" pattern already established for the screen inventory (D-6)
- **T09** (`screen-discussfeedback`): R-611a's mockup-driven walkthrough can use this flow diagram as a discussion map; observed stakeholder clicks during discussion may themselves surface a needed correction back to this diagram
- **T10**: must register `screen-generateflow` (S36) in the orchestrator's DAG with prerequisites on both `screen-generateinventory` and `screen-generatemockup`
- **Future Phase 2 work on R-603a**: should automate exactly this skill's Steps 4–5 verification logic (comparing diagram edges against mockup `<a href>` targets), not redesign the comparison approach from scratch
