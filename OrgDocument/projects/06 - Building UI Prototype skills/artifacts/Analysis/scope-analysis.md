# Minimum Viable Scope Analysis

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Source**: requirements.md (v1.3), goals.md, domain-concepts.md
**Generated**: 2026-10-26
**Analysis Method**: Business Value + Dependency + Complexity Assessment

## Executive Summary

**MVP Definition**: Generate a traceable screen inventory, per-screen Markdown+HTML/CSS layout specs, and standalone clickable HTML/JS mockups directly from requirements and a newly introduced UI Model — discussable with a stakeholder (or role-played in solo mode) and feeding corrections back through the existing `change-management` skill — fully registered with the EDPS orchestrator and gates. Import of an existing design spec, derived role-based UI Models, and automated consistency/co-evolution tooling are explicitly **not** required for v1; they are the natural Phase 2/3 of this same feature set.

**Core Features Count**: 15 features identified as essential
**Enhancement Features**: 7 features for Phase 2
**Optional Features**: 2 features for future consideration
**Estimated MVP Effort**: 2–3 weeks solo-developer effort (skill authoring + gate/orchestrator integration + one real end-to-end dry run), consistent with this project's own W5H timeline estimate

## Core Features (MVP Essential)

### Feature: Screen Inventory & UI Prototype Artifact Category
*(R-601, R-601a)*
- **Business Value**: High — this is the entry point artifact; nothing else in the skill set can be discussed or generated without first knowing what screens exist
- **Technical Complexity**: Medium — requires extending `project-document-management`'s folder-scaffolding templates with a new `UI Prototype` category (a dependency on an existing skill, not purely new logic)
- **Dependencies**: None upstream within this skill set; depends on `project-document-management` accepting the new artifact category
- **User Impact**: Without it, there is no standalone place to put generation outputs — would force everything into the consolidated design document, contradicting D-6
- **Risk of Exclusion**: Critical — this was explicitly resolved (D-6) as a standalone artifact specifically to avoid full-document regeneration on small changes; skipping it reintroduces that problem from day one

### Feature: Layout Specification Generation
*(R-602)*
- **Business Value**: High — the literal, implementation-guiding Markdown+HTML/CSS document is one of the two things the user explicitly asked for ("generate a set of UI design documents that can be used for future development")
- **Technical Complexity**: Medium — generating literal HTML/CSS from requirements/UI Model input is the core "hard problem" of this skill set
- **Dependencies**: UI Model Generation (needs something to reference per R-606)
- **User Impact**: Direct implementation guide for a future developer
- **Risk of Exclusion**: Critical — without it, there's no design document at all, defeating the project's primary goal

### Feature: Interactive Mockup Generation
*(R-602a, R-626)*
- **Business Value**: High — the second explicit user ask ("a literal interactive HTML/JS mockup... clickable, not just specified")
- **Technical Complexity**: Medium — standalone, zero-build-step HTML/JS generation; complexity is in keeping it genuinely clickable and portable, not in the generation itself
- **Dependencies**: Layout Specification Generation (the mockup renders what the layout spec describes)
- **User Impact**: This is literally the artifact the user wants to "discuss requirements, ideas, designs with stakeholders" against
- **Risk of Exclusion**: Critical — explicitly named as a core capability by the user; cannot be deferred

### Feature: Interaction Flow Diagramming
*(R-603)*
- **Business Value**: High — without flows, individual screens have no connective narrative; a stakeholder discussion needs to show how screens relate
- **Technical Complexity**: Low-Medium — reuses `diagram-generatecollaboration`'s existing Mermaid conventions (ASM-4), not a new diagramming system
- **Dependencies**: Screen Inventory, Interactive Mockup Generation (flows must correspond to actual mockup transitions per R-603)
- **User Impact**: Enables the "navigate Login → Dashboard → Order Detail" style discussion the vision doc implies
- **Risk of Exclusion**: High — a set of disconnected screens is a weak discussion tool compared to a navigable flow

### Feature: Lightweight, Evolving Component Inventory
*(R-604)*
- **Business Value**: Medium — reduces inconsistent re-description of the same UI pattern, but the user explicitly said "not rigorous" (D-3), so this is deliberately low-effort by design
- **Technical Complexity**: Low — informal tracking, no enforcement logic required for v1
- **Dependencies**: Layout Specification Generation (components are observed within layout specs)
- **User Impact**: Mild consistency improvement across screens
- **Risk of Exclusion**: Medium — could be deferred without breaking core value, but it's cheap enough that deferring it saves little effort while losing some quality; kept in MVP mainly because of its low cost, not high necessity

### Feature: Requirement Traceability
*(R-605)*
- **Business Value**: High — traceability is a foundational EDPS principle (R-306 pattern from prior iterations), not unique to this project
- **Technical Complexity**: Low — mechanically attaching requirement IDs to generated artifacts
- **Dependencies**: None beyond requirements.json being available
- **User Impact**: Lets a future developer or reviewer verify *why* a screen exists
- **Risk of Exclusion**: High — without it, this skill set breaks EDPS's core evolutionary/traceable methodology, undermining the entire framework's value proposition

### Feature: UI Model Generation, Base Model & Core Traceability
*(R-606, R-627, R-628, R-629, R-630)*
- **Business Value**: High — this is the user-initiated architectural improvement ("introduce a UI Model... to make better alignment among the models"); it's the mechanism that keeps screens from needing individual regeneration on every domain tweak
- **Technical Complexity**: High — the single most architecturally significant piece of new modeling work in this project; defining what "aggregation" means concretely and how it's represented is non-trivial
- **Dependencies**: Domain model must already exist (`domain-extractconcepts`/`domain-alignentities` outputs)
- **User Impact**: Without it, screens would reference domain entities directly, which the user explicitly rejected as the traceability model
- **Risk of Exclusion**: Critical — this is a named, deliberate architectural decision, not an optional nicety; excluding it would contradict a direct user requirement

### Feature: Design Document Output (Consolidated + JSON)
*(R-607, R-608)*
- **Business Value**: High — the consolidated document is the artifact "suitable for handing to a future developer without requiring the original AI session" — a core stated goal
- **Technical Complexity**: Medium — mostly an assembly/summarization layer over already-generated screens/flows/components (per domain-concepts.md's REL-610), not new generation logic
- **Dependencies**: Screen Inventory, Layout Specification Generation, Interaction Flow Diagramming
- **User Impact**: The durable, standalone deliverable the user asked for
- **Risk of Exclusion**: Critical — explicitly requested output format

### Feature: In-Document Changelog Versioning
*(R-610)*
- **Business Value**: Medium-High — the user explicitly chose this over relying on git history (D-4); cheap to implement, meaningfully improves design-evolution visibility
- **Technical Complexity**: Low — appending structured changelog entries is simple bookkeeping
- **Dependencies**: Design Document Output, Layout Specification Generation (each needs its own changelog section)
- **User Impact**: A future developer can see design evolution without needing to reconstruct it from git log
- **Risk of Exclusion**: High relative to its low cost — explicitly requested, inexpensive to deliver, no good reason to defer

### Feature: Discussion Surface & Feedback Capture (incl. Solo-Mode Role-Play)
*(R-611, R-612, R-614)*
- **Business Value**: High — this is the third pillar of the user's original ask ("discuss requirements, ideas, designs with stakeholders")
- **Technical Complexity**: Medium — presenting the mockup as a discussion surface is straightforward; capturing feedback in a form that routes cleanly into `change-management` needs careful schema alignment (ASM-5)
- **Dependencies**: Interactive Mockup Generation; `change-management` skill (existing, consumed not modified)
- **User Impact**: Enables the core conversational use case, including functioning in solo mode with no second real person available
- **Risk of Exclusion**: Critical — without this, the mockup is just a static artifact, not the "discuss with stakeholders" tool the user asked for

### Feature: EDPS Pipeline Integration (Position, Change Loop, Gate/Orchestrator, Collaboration-Mode)
*(R-619, R-620, R-621, R-622)*
- **Business Value**: High — not optional "nice integration," but the difference between a disconnected side-tool and a genuine EDPS skill set member
- **Technical Complexity**: Medium — follows well-established patterns from 32 existing skills; the work is mechanical application of an existing pattern, not invention
- **Dependencies**: All generation features above must exist first (there must be outputs to gate-check)
- **User Impact**: Indirect but structurally essential — ensures this skill set doesn't become a maintenance orphan outside the orchestrator's DAG
- **Risk of Exclusion**: Critical — explicitly required by R-621/R-622; every other EDPS skill does this, and this project's own goals.md (CON-6) forbids inventing a separate approval mechanism

### Feature: Format & Tooling Constraints (Text-Based, No Design Tool, No Tech Stack, Portability)
*(R-623, R-624, R-625, R-626)*
- **Business Value**: High — these aren't "features" to build so much as guardrails that shape every other feature's implementation; getting them wrong would undermine the whole MVP (e.g., if mockups secretly needed a build step)
- **Technical Complexity**: Low as a standalone concern, but pervasive — must be respected by every generation feature, not implemented once
- **Dependencies**: None — these are constraints, not sequenced features
- **User Impact**: Guarantees zero-setup viewing/editing for both the developer and any stakeholder
- **Risk of Exclusion**: Critical — these are hard constraints (D-5, R-623–R-626), not aspirational goals; violating any of them breaks an explicit requirement

## Enhancement Features (Post-MVP Phase 1)

### Feature: Automated Flow/Mockup Consistency Gate
*(R-603a)*
- **Business Value**: Medium-High — catches a real class of drift (documented flow diverging from actual clickable behavior) automatically
- **Technical Complexity**: High — requires parsing both Mermaid edges and actual `<a href>`/JS navigation calls in generated HTML/JS and diffing them; genuinely nontrivial to get reliable
- **Dependencies**: Interaction Flow Diagramming, Interactive Mockup Generation (both must exist and be stable first)
- **Enhancement Rationale**: The MVP can rely on manual review of flow/mockup consistency (same as every other current EDPS skill without automated cross-artifact checks); automating this is valuable but not blocking for an initial usable version
- **Target Release**: Phase 1, shortly after MVP — this directly implements a user-stated decision (D-7: "automatically"), so it shouldn't be deferred indefinitely, just sequenced after the generation pipeline it depends on is proven

### Feature: UI Model Co-Evolution Automation
*(R-627a)*
- **Business Value**: Medium — prevents silent divergence between the UI Model and domain model over time
- **Technical Complexity**: High — requires either modifying `domain-alignentities`/`model-integration` or building a reliable change-detection hook into them; genuine cross-skill integration work, more involved than most other requirements here
- **Dependencies**: UI Model Generation (R-627) must exist and be stable; coordination with two existing skills' maintainers (practically: the same developer, but still requires understanding their internals deeply)
- **Enhancement Rationale**: MVP can start with **manual** co-evolution (developer re-runs UI Model generation by hand after a domain change) — functionally correct, just not automatic. Automating the trigger is valuable polish, not core function
- **Target Release**: Phase 1 — directly resolves D-10, should follow soon after MVP proves the UI Model concept works at all

### Feature: Regenerate-on-Change Automation
*(R-629a)*
- **Business Value**: Medium-High — directly implements the user's explicit preference (D-11: "regenerate... may be more effective") over a flag-and-wait approach
- **Technical Complexity**: Medium-High — needs reliable change detection on UI Model entries and safe regeneration that doesn't clobber manual edits (a real risk noted in goals.md's OQ-G6 discussion)
- **Dependencies**: UI Model Co-Evolution Automation (needs to know *when* the UI Model changed, which is this feature's prerequisite)
- **Enhancement Rationale**: In MVP, regeneration can be a manually triggered command rather than automatic; the user's decision is about *behavior* (regenerate vs. flag) not *automation timing*, so a manual-trigger MVP still honors D-11's spirit while deferring the harder "detect change automatically" part
- **Target Release**: Phase 1, same wave as Co-Evolution Automation since they're technically coupled

### Feature: Design Rationale Capture
*(R-609)*
- **Business Value**: Medium — valuable for future-developer context, but not blocking for a usable prototype
- **Technical Complexity**: Low-Medium — mostly a matter of prompting for and recording rationale alongside each design decision
- **Dependencies**: Layout Specification Generation
- **Enhancement Rationale**: A design document without captured rationale is still useful (the "what" is there); rationale enriches the "why" but its absence doesn't block implementation
- **Target Release**: Phase 1

### Feature: Mockup-Driven Walkthrough & Clarifying Question Generation
*(R-611a, R-613)*
- **Business Value**: Medium — meaningfully improves discussion quality (following actual clicks, surfacing ambiguity proactively) but the discussion capability itself (core feature above) works without these refinements
- **Technical Complexity**: Medium — requires tracking actual navigation during a live discussion session and pattern-matching ambiguous requirement-to-UI mappings
- **Dependencies**: Discussion Surface & Feedback Capture (core feature)
- **Enhancement Rationale**: Basic discussion (show mockup, capture typed/spoken feedback) delivers most of the value; these two features are refinements to *how* that discussion is conducted
- **Target Release**: Phase 1

### Feature: Design Specification Import & Strict Conformance
*(R-615, R-616)*
- **Business Value**: Medium-High — explicitly requested by the user ("if I have a UI design specification, I can import it"), but it's the *second* of the two original capabilities (generate vs. import), and generation must work first for import to have anything to conform *to*
- **Technical Complexity**: High — parsing an arbitrary externally authored Markdown+HTML/CSS document into the same internal representation used for generated output, then enforcing strict reuse of its conventions, is a substantial parsing/matching problem
- **Dependencies**: The entire Generation pipeline (Screen Inventory through Component Inventory) must exist first, since import populates the same internal model that generation does
- **Enhancement Rationale**: Generation-only (no import) is a complete, independently useful v1 — many users will start greenfield with no existing spec to import. Import is additive value for the subset of users who already have one
- **Target Release**: Phase 1 — important enough not to push to "optional," but sequenced after generation is proven solid

## Optional Features (Future Consideration)

### Feature: Derived Role-Based UI Models
*(R-631, R-632)*
- **Business Value**: Low-Medium for v1 — valuable once a project has genuinely divergent role-based views (e.g., Admin vs. Customer), but many smaller projects may never need more than the base model
- **Technical Complexity**: High — requires a working base UI Model first, plus a filter/adaptation mechanism and its own sync/regeneration logic (compounding R-629a's complexity)
- **Nice-to-Have Rationale**: The user confirmed this is "potentially" needed (D-12's own wording), not definitely — a soft signal this can wait until a real project surfaces the actual need
- **Potential ROI**: High for multi-role products, zero for single-role/internal-tool projects — ROI is highly situational, better evaluated against a real use case than built speculatively

### Feature: Partial Import Gap Detection & Import Source Traceability
*(R-617, R-618)*
- **Business Value**: Low-Medium — useful polish once import (enhancement feature above) is in regular use, but doesn't block import from working at all for a complete spec
- **Technical Complexity**: Medium — gap detection requires comparing imported coverage against the full required screen set; source traceability requires tagging provenance per screen
- **Nice-to-Have Rationale**: A complete, well-formed imported spec doesn't need gap detection; this feature mainly protects against partial/incomplete imports, a secondary concern
- **Potential ROI**: Moderate — protects against a specific failure mode (incomplete import silently leaving gaps) that may or may not occur often in practice

## Feature Prioritization Matrix

| Feature | Business Value | Technical Complexity | Dependencies | MVP Category |
|---------|----------------|---------------------|--------------|--------------|
| Screen Inventory & UI Prototype Category | High | Medium | project-document-management | Core |
| Layout Specification Generation | High | Medium | UI Model | Core |
| Interactive Mockup Generation | High | Medium | Layout Spec | Core |
| Interaction Flow Diagramming | High | Low-Medium | Screen Inventory, Mockup | Core |
| Lightweight Component Inventory | Medium | Low | Layout Spec | Core |
| Requirement Traceability | High | Low | requirements.json | Core |
| UI Model Generation, Base Model & Traceability | High | High | Domain model | Core |
| Design Document Output (+ JSON) | High | Medium | Screens, Flows | Core |
| In-Document Changelog | Medium-High | Low | Design Document | Core |
| Discussion Surface & Feedback Capture | High | Medium | Mockup, change-management | Core |
| EDPS Pipeline Integration | High | Medium | All generation features | Core |
| Format & Tooling Constraints | High | Low (pervasive) | None | Core |
| Automated Flow/Mockup Consistency Gate | Medium-High | High | Flow, Mockup | Enhancement |
| UI Model Co-Evolution Automation | Medium | High | UI Model | Enhancement |
| Regenerate-on-Change Automation | Medium-High | Medium-High | Co-Evolution Automation | Enhancement |
| Design Rationale Capture | Medium | Low-Medium | Layout Spec | Enhancement |
| Mockup-Driven Walkthrough & Clarifying Questions | Medium | Medium | Discussion Surface | Enhancement |
| Design Specification Import & Conformance | Medium-High | High | Full generation pipeline | Enhancement |
| Derived Role-Based UI Models | Low-Medium | High | Base UI Model | Optional |
| Partial Import Gap Detection & Source Traceability | Low-Medium | Medium | Import | Optional |

## MVP Roadmap

### Phase 0 — Foundation
- Format & Tooling Constraints established as design principles across all generation code (not a separate build step, but a checklist applied throughout)
- `project-document-management` extended with the `UI Prototype` artifact category
- Requirement Traceability conventions established (ID-linking pattern, consistent with existing EDPS skills)

### Phase 1 — MVP Launch
- UI Model Generation, Base Model & Traceability
- Screen Inventory (standalone artifact)
- Layout Specification Generation
- Interactive Mockup Generation
- Interaction Flow Diagramming
- Lightweight Component Inventory
- Design Document Output (consolidated + JSON)
- In-Document Changelog Versioning
- Discussion Surface & Feedback Capture (including solo-mode role-play)
- EDPS Pipeline Integration (orchestrator registration, gates, collaboration-mode)

### Phase 2 — Enhancement
- Automated Flow/Mockup Consistency Gate
- UI Model Co-Evolution Automation (upgrading from MVP's manual re-run)
- Regenerate-on-Change Automation (upgrading from MVP's manual trigger)
- Design Rationale Capture
- Mockup-Driven Walkthrough & Clarifying Question Generation
- Design Specification Import & Strict Conformance

### Phase 3 — Expansion
- Derived Role-Based UI Models
- Partial Import Gap Detection & Import Source Traceability

## Scope Boundaries

### In Scope (MVP)
- Generating screens, layout specs, mockups, flows, and a design document from requirements + a newly generated base UI Model
- Discussing the mockup with a stakeholder (or role-playing in solo mode) and capturing feedback into `change-management`
- Full traceability from screens back to requirements and the UI Model
- Orchestrator/gate registration consistent with all existing EDPS skills
- Manual (not automated) UI Model regeneration when the domain model changes

### Out of Scope (MVP)
- Automated detection of domain-model changes and automatic UI Model regeneration (Phase 2)
- Automated flow/mockup consistency checking — rely on manual review for now (Phase 2)
- Importing an existing design specification (Phase 2) — MVP is generation-only
- Multiple/derived role-based UI Models (Phase 3)
- Any code scaffolding toward a specific application framework (explicitly out of scope per R-625/D-5 for the entire project, not just MVP)

## Risk Assessment

### High Priority Risks
- **UI Model concept may prove harder to generalize than expected** (affects: UI Model Generation, Core feature) — "aggregation" is a genuinely new concept for this framework; mitigation: validate with one concrete example (e.g., this very project's own eventual UI, or a simple toy domain) before committing to a final schema
- **Mockup-to-flow consistency drift, even without the automated gate** (affects: MVP quality) — since the automated check is deferred to Phase 2, MVP relies on manual diligence; mitigation: make manual review an explicit step in the skill's own Quality Checks section, not an afterthought
- **`project-document-management` dependency** (affects: Screen Inventory & UI Prototype Category) — this skill set cannot unilaterally add a new artifact category; mitigation: treat this as a small, explicit cross-skill change request, not a silent assumption

### Medium Priority Risks
- **Feedback-to-change-management schema mismatch** (affects: Discussion Surface) — UI-specific feedback (e.g., "change field Y from optional to required on Screen X") may not map cleanly onto `change-management`'s existing change-type taxonomy; mitigation: do a small schema-compatibility check early in Phase 1, not after the feature is fully built
- **Manual regeneration triggers being forgotten** (affects: MVP's manual co-evolution approach) — without automation, a developer might simply forget to regenerate after a domain change; mitigation: document this explicitly as a known MVP limitation in the design document/guide, so it's a conscious tradeoff, not a silent gap

## Success Criteria

### MVP Launch Success
- A real end-to-end dry run (per w5h-analysis.md's Phase 4) produces at least one working screen, layout spec, mockup, and design document from a real (even if small) domain/requirements input
- All MVP features pass their own `gate.json` validation once authored
- The generated mockup opens via `file://` with zero setup, confirmed on at least one real browser

### Enhancement Phase Success
- Automated flow/mockup consistency gate catches at least one real, previously-unnoticed divergence in a test run
- Import of a hand-authored sample design spec produces screens that visibly reuse its conventions rather than diverging

## Recommendations

### Immediate Actions
1. Treat **UI Model Generation** as the first thing to prototype concretely (even informally) — it's the highest-complexity, highest-business-value Core feature, and several other Core features depend on its shape being settled
2. Confirm the `project-document-management` extension (new `UI Prototype` category) as a small, explicit task before starting generation-feature work, so screen inventory output has somewhere real to go
3. Do the `change-management` feedback-schema compatibility check early (flagged as a Medium risk above) rather than discovering a mismatch late in Discussion Surface development

### Future Considerations
1. Once Phase 1 ships, revisit whether automated co-evolution (Phase 2) is worth the integration complexity, or whether manual regeneration remains "good enough" in practice — don't assume Phase 2 is automatically worth building without evidence of real friction
2. Derived Role-Based UI Models (Phase 3) should wait for a genuine multi-role project to motivate its design, rather than being speculatively architected now
3. Consider whether Import (Phase 2) should be resequenced earlier if an actual existing design spec becomes available sooner than expected — this scope plan assumes greenfield-first, but real usage may reveal import is needed sooner

---
**Traceability**: Requirements tracked to R-601–R-632 (`artifacts/Analysis/requirements.md` v1.3)
**Review Date**: Recommend revisiting this scope after the Phase 1 end-to-end dry run, before committing to Phase 2 sequencing
**Stakeholder Approval**: Solo mode — self-reviewed by the developer; no real external stakeholder review required at this stage per `collaboration_mode: solo`
