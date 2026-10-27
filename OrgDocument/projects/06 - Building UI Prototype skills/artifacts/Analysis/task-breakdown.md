# Task Breakdown — 06 - Building UI Prototype skills

**Project**: PRJ-06
**Generated**: 2026-10-26
**Source**: requirements.md (v1.3), goals.md, w5h-analysis.md, domain-concepts.md, scope-analysis.md, domain-alignment.md, collaboration-diagrams.md

## Summary

This breakdown converts `scope-analysis.md`'s MVP scope (12 Core features) into **11 actionable tasks** across **4 phases**, sequenced per the dependency chain confirmed in `collaboration-diagrams.md` (D-602/D-603/D-604). Enhancement (Phase 2) and Optional (Phase 3) features from scope-analysis.md are captured as a lightweight backlog at the end, not broken into detailed tasks yet — consistent with the scope analysis's own recommendation not to over-plan deferred work.

**Total Tasks**: 11 (T01–T11)
**Total Phases**: 4
**Estimated Total Effort**: 13–18 days (~2.5–3.5 weeks solo), consistent with scope-analysis.md's 2–3 week estimate plus validation buffer

## Phase Overview

| Phase | Name | Tasks | Focus |
|---|---|---|---|
| 1 | Foundation | T01–T03 | Prerequisites: artifact category, traceability conventions, UI Model schema proof |
| 2 | Generation Pipeline | T04–T07 | The core "generate" capability: screens, layouts, mockups, flows |
| 3 | Discussion & Integration | T08–T09 | The "discuss" capability plus EDPS pipeline registration |
| 4 | Validation | T10–T11 | End-to-end dry run, skill documentation polish |

## Task List

| Task | Title | Phase | Priority | Depends On | Est. Effort |
|---|---|---|---|---|---|
| T01 | Extend project-document-management with UI Prototype Artifact Category | 1 - Foundation | P0 | — | 0.5–1 day |
| T02 | Establish Traceability & Format Conventions | 1 - Foundation | P0 | — | 0.5 day |
| T03 | Prototype UI Model Schema (Base Model + Aggregation) | 1 - Foundation | P0 | T02 | 2–3 days |
| T04 | Author screen-generateinventory Skill | 2 - Generation | P0 | T01, T03 | 1–2 days |
| T05 | Author screen-generatelayout Skill (Markdown + HTML/CSS) | 2 - Generation | P0 | T04 | 2–3 days |
| T06 | Author screen-generatemockup Skill (Clickable HTML/JS) | 2 - Generation | P0 | T05 | 2–3 days |
| T07 | Author screen-generateflow Skill (Interaction Flow Diagrams) | 2 - Generation | P0 | T04, T06 | 1 day |
| T08 | Author screen-assembledocument Skill (Consolidated Design Doc) | 3 - Discussion & Integration | P0 | T05, T06, T07 | 1–2 days |
| T09 | Author screen-discussfeedback Skill (Discussion + change-management Routing) | 3 - Discussion & Integration | P0 | T06 | 1–2 days |
| T10 | Gate & Orchestrator Registration (All New Skills) | 3 - Discussion & Integration | P0 | T04–T09 | 1–2 days |
| T11 | End-to-End MVP Validation (Real Dry Run) | 4 - Validation | P0 | T10 | 1–2 days |

## Dependency Chain (visual)

```
T01 (artifact category) ──┐
T02 (conventions) ──┬──────┤
                     T03 (UI Model) ──► T04 (inventory) ──► T05 (layout) ──► T06 (mockup) ──┬──► T07 (flow)
                                                                                              ├──► T08 (design doc)
                                                                                              └──► T09 (discussion)
                                                                          T04,T05,T06,T07,T08,T09 ──► T10 (gates/orchestrator)
                                                                                                        └──► T11 (validation)
```

## Naming Note

Skill names below (`screen-generateinventory`, etc.) follow this framework's existing `verb-objectNoun`/`domain-action` naming convention (e.g., `goals-extract`, `process-w5h`, `diagram-generatecollaboration`). These are proposed names for T04–T09's deliverables — confirm or rename during T04's actual authoring, since the final name affects the orchestrator catalogue entry in T10.

---

## Phase 1 — Foundation

### T01: Extend project-document-management with UI Prototype Artifact Category
**Maps to**: Scope-analysis.md Core feature "Screen Inventory & UI Prototype Artifact Category" (R-601, R-601a)
**Why first**: Every generation output needs somewhere to go; this is a small, explicit cross-skill change rather than something this project can assume into existence
**Deliverable**: `.github/skills/project-document-management/SKILL.md` updated — new `UI Prototype` artifact category added alongside existing ones (`Analysis`, `Changes`, `Documentation`, `Sample Data`, `Source Materials`, `Testing`), including the folder-scaffolding template and `main.md` generation rule for the new folder
**Acceptance Criteria**:
- [ ] New projects initialized via `project-document-management` get an `artifacts/UI Prototype/main.md` folder when the UI Prototyping skill set is in use
- [ ] Existing projects without this category are unaffected (additive change only)
- [ ] `gate.json` for `project-document-management` optionally extended with a soft check for the new category's presence (consistent with how Iteration 4 added `collaboration_mode_present` as a soft check)

### T02: Establish Traceability & Format Conventions
**Maps to**: R-605, R-606, R-623–R-626 (cross-cutting, not a single feature in scope-analysis.md but called out there as "pervasive... must be respected by every generation feature")
**Why first**: These are hard constraints that shape every subsequent task's implementation; documenting them once now avoids re-deriving them ad-hoc in T04–T09
**Deliverable**: A short internal conventions note (can live in `artifacts/Documentation/ui-prototyping-conventions.md`) covering:
  - ID format: `SCR-[###]` for screens, `UME-[###]` for UI Model entries (per `vocabulary.md`'s proposed prefixes)
  - Traceability tag format: how `requirement_refs`/`ui_model_ref` are embedded in generated Markdown/JSON
  - File/folder layout confirmed for `artifacts/UI Prototype/`
  - The hard constraints checklist (text-based, no design tool, no tech stack, `file://` portability) as a literal pre-ship checklist every later task must satisfy
**Acceptance Criteria**:
- [ ] Conventions document published and cross-referenced from T04–T09's eventual SKILL.md files
- [ ] ID formats finalized (not just "recommended, not yet enforced" as left open in `vocabulary.md`)

### T03: Prototype UI Model Schema (Base Model + Aggregation)
**Maps to**: Scope-analysis.md Core feature "UI Model Generation, Base Model & Traceability" (R-606, R-627, R-628, R-629, R-630) — explicitly flagged as the **top recommendation** in scope-analysis.md ("treat as the first thing to prototype concretely... several other Core features depend on its shape being settled")
**Why first**: Highest-complexity, highest-business-value Core feature; `domain-concepts.md` flagged this as only medium-confidence pending a real example
**Deliverable**: A concrete worked example of `ui-model.md`/`.json` against a small real or toy domain (candidate: a simplified slice of this very project's own domain, or a small external example) — validating that "aggregation" is representable without needing a new modeling notation (per `goals.md`'s ASM-8)
**Note**: This task deliberately produces a **worked example**, not yet the actual generation skill (`screen-generateinventory` in T04 is where the skill itself gets authored) — the goal here is validating the schema design risk flagged in `domain-concepts.md` and `scope-analysis.md` before committing to it in code/instructions
**Acceptance Criteria**:
- [ ] At least one concrete `ui-model.md` example exists showing a base model with 2+ `UIModelEntry` aggregations, each aggregating 2+ domain entities
- [ ] Schema confirmed workable using only Markdown+JSON (no new notation needed) — or, if a new notation genuinely is needed, that gap is explicitly documented before T04 proceeds
- [ ] Derived-model placeholder structure sketched (even if Phase 3 defers full implementation) so T03's schema doesn't need breaking changes later for R-630/R-631's base/derived relationship

---

## Phase 2 — Generation Pipeline

### T04: Author screen-generateinventory Skill
**Maps to**: R-601 (Screen Inventory, standalone artifact)
**Deliverable**: New `.github/skills/screen-generateinventory/SKILL.md` (or confirmed final name per the Naming Note above) — generates `screen-inventory.md`/`.json` in `artifacts/UI Prototype/` from requirements + the UI Model (T03) input
**Acceptance Criteria**:
- [ ] Given a requirements.json + ui-model.json input, produces a screen inventory listing each screen's purpose, UI Model reference, and requirement traceability
- [ ] Output is a standalone artifact, never embedded in a larger document (per D-6)
- [ ] Follows T02's established ID/traceability conventions

### T05: Author screen-generatelayout Skill (Markdown + HTML/CSS)
**Maps to**: R-602 (Layout Specification with Embedded Implementation Code)
**Deliverable**: New SKILL.md generating one `LayoutSpec` (Markdown + embedded HTML/CSS) per screen in the inventory
**Acceptance Criteria**:
- [ ] Generated HTML/CSS is literal and usable, not placeholder/descriptive text (core distinguishing requirement from a traditional wireframe)
- [ ] Each LayoutSpec includes an in-document changelog section stub (R-610), ready for future iteration entries
- [ ] Each LayoutSpec traces to its Screen's `requirement_refs` and `ui_model_ref`

### T06: Author screen-generatemockup Skill (Clickable HTML/JS)
**Maps to**: R-602a (Literal Interactive Mockup), R-626 (Mockup Portability)
**Deliverable**: New SKILL.md generating a standalone, `file://`-openable HTML/JS mockup per screen, rendering what the LayoutSpec (T05) describes
**Acceptance Criteria**:
- [ ] Generated mockup opens directly via `file://` with zero build step, package manager, or server (R-626) — test on at least one real browser, not just assumed
- [ ] Mockup is genuinely clickable (real navigation between generated screens' mockup files), not merely a static render
- [ ] No references to a specific target framework (React/Vue/etc.) anywhere in generated output (R-625)

### T07: Author screen-generateflow Skill (Interaction Flow Diagrams)
**Maps to**: R-603 (Interaction Flow Modeling)
**Deliverable**: New SKILL.md generating Mermaid interaction-flow diagrams across the screen set, reusing `diagram-generatecollaboration`'s existing conventions (ASM-4) rather than inventing new diagram syntax
**Acceptance Criteria**:
- [ ] Flow diagram's edges correspond to the actual navigation implemented in T06's mockups (manually verified in MVP — automated check is the Phase 2 Enhancement feature, R-603a)
- [ ] Diagram style/syntax is consistent with `diagram-generatecollaboration`'s existing sequence/flowchart patterns

---

## Phase 3 — Discussion & Integration

### T08: Author screen-assembledocument Skill (Consolidated Design Doc)
**Maps to**: R-607 (UI Design Document Output), R-608 (JSON Companion), R-610 (In-Document Changelog)
**Deliverable**: New SKILL.md that assembles the consolidated `DesignDocument` (Markdown + JSON) summarizing all screens/flows/components generated in T04–T07, with its own top-level changelog
**Acceptance Criteria**:
- [ ] Consolidated document summarizes without duplicating full storage (screen inventory remains the standalone source of truth per D-6 — this document references it, doesn't replace it)
- [ ] JSON companion output is well-formed and mirrors the Markdown content
- [ ] Document is "suitable for handing to a future developer without requiring the original AI session" (R-607's literal acceptance bar) — sanity-check by having someone unfamiliar with the session read it, or self-review from that lens in solo mode

### T09: Author screen-discussfeedback Skill (Discussion + change-management Routing)
**Maps to**: R-611 (Discussion Surface), R-612 (Feedback Capture), R-614 (Solo-Mode Role-Play), R-620 (Change Loop)
**Deliverable**: New SKILL.md (or an instruction-level addition to an existing skill — decide during authoring) that presents the mockup set as a discussion surface, captures `FeedbackItem`s, and produces structured input compatible with `change-management`'s existing change-document schema
**Acceptance Criteria**:
- [ ] At least one real or simulated feedback item successfully produces a valid `change-management`-compatible structured change document, with no manual re-transcription step (KPI-4 from goals.md)
- [ ] Solo-mode role-play guidance present, following `process-w5h`'s existing pattern (R-614), including its own "when to break out of solo mode" note
- [ ] **Risk check (flagged in scope-analysis.md as Medium priority)**: confirm early in this task — not after full implementation — that `change-management`'s schema can represent UI-specific feedback (e.g., "change field Y from optional to required on Screen X") without needing a new change type

### T10: Gate & Orchestrator Registration (All New Skills)
**Maps to**: R-621 (Gate & Workflow Orchestrator Integration), R-622 (Collaboration-Mode Awareness)
**Deliverable**: `gate.json` for each new skill from T04–T09; registration of all new skill IDs in `edps-workflow-orchestrator/SKILL.md`'s skill catalogue (DAG prerequisites matching the dependency chain above)
**Acceptance Criteria**:
- [ ] Each new skill has a working `gate.json` (reusing `stakeholder_confirmation` check type where relevant, per R-622 — not inventing a new approval mechanism)
- [ ] Orchestrator catalogue updated with correct prerequisite IDs reflecting T04→T05→T06→(T07,T08,T09) dependency order
- [ ] `orchestrate status`/`orchestrate next` correctly surface the new skills in a test run

---

## Phase 4 — Validation

### T11: End-to-End MVP Validation (Real Dry Run)
**Maps to**: Scope-analysis.md Success Criteria "MVP Launch Success" — a real dry run producing at least one working screen, layout spec, mockup, and design document
**Deliverable**: A validation report (`artifacts/Testing/ui-prototyping-mvp-validation-report.md`) documenting an actual run of T04–T10's skills against a real (even if small) requirements/domain input, following the validation-report pattern established in Iteration 4's T06
**Acceptance Criteria**:
- [ ] At least one real screen generated end-to-end (inventory → layout → mockup → flow → design document)
- [ ] Generated mockup confirmed to open via `file://` on a real browser with zero setup
- [ ] At least one feedback item successfully routed through to a `change-management` structured change document
- [ ] Gate evaluations pass (or documented known-soft-failures) for all new skills
- [ ] Report explicitly notes what worked, what didn't, and whether T03's UI Model schema held up under a real (not just toy) example

---

## Deferred Backlog (Not Broken Into Tasks Yet)

Per `scope-analysis.md`'s own Phase 2/3 roadmap — these remain tracked at the feature level in `scope-analysis.md`, not decomposed into tasks here, consistent with its recommendation not to speculatively over-plan deferred work:

**Phase 2 — Enhancement** (revisit after T11 validates the MVP):
- Automated Flow/Mockup Consistency Gate (R-603a)
- UI Model Co-Evolution Automation (R-627a) — upgrading T03's manual approach
- Regenerate-on-Change Automation (R-629a) — upgrading manual trigger to automatic
- Design Rationale Capture (R-609)
- Mockup-Driven Walkthrough & Clarifying Question Generation (R-611a, R-613)
- Design Specification Import & Strict Conformance (R-615, R-616)

**Phase 3 — Expansion** (revisit only if a real need surfaces):
- Derived Role-Based UI Models (R-630, R-631, R-632)
- Partial Import Gap Detection & Import Source Traceability (R-617, R-618)

---

## Risk Carryover from scope-analysis.md

These risks were already identified; repeated here so task execution doesn't lose them:
- **UI Model concept may prove harder to generalize than expected** → directly addressed by T03's worked-example-first approach
- **Manual mockup-to-flow consistency drift without the automated gate** → mitigated by making manual review an explicit T07 acceptance criterion, not an afterthought
- **`project-document-management` dependency** → T01 treats this as its own explicit task rather than an assumption
- **Feedback-to-change-management schema mismatch** → T09 explicitly front-loads this check rather than discovering it late

---
**Traceability**: Tasks map to `scope-analysis.md`'s 12 Core features and requirements R-601–R-632 as annotated per task
**Next Step**: Populate `tasks/task-tracking.md` and individual `tasks/T01-*.md`...`T11-*.md` files from this breakdown
