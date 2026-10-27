# W5H Requirements Analysis

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Source**: requirements.md (v1.1), goals.md
**Generated**: 2026-10-26T22:00:00Z
**Analysis Framework**: Who, What, When, Where, Why, How
**Collaboration Mode**: Solo — stakeholder roles below are role-played by the developer with assumptions documented inline, per `process-w5h`'s Mode-Conditional Stakeholder Engagement pattern. No items required breaking out to a real stakeholder for this pass (see note at end of WHO section).

## WHO — Stakeholders and Roles

### Primary Stakeholders

- **Solo Developer** (the primary user of this skill set): builds requirements/domain models with existing EDPS skills, then uses UI prototyping skills to generate and iterate on prototypes. *(Ref: R-619)*
- **Future Developer** (not necessarily the same person — could be future-you or a collaborator onboarding later): consumes the design document to implement the actual UI, without access to the original AI session. *(Ref: R-607)*
- **Business/Product Stakeholder** (role played by the developer in solo mode, or a real person if the project later moves to traditional mode): reviews the clickable mockup, gives feedback on screens/flows, and implicitly approves design direction. *(Ref: R-611, R-612, R-614)*

  *Assumed as Business/Product Stakeholder (solo mode): the primary interest is confirming the prototype reflects actual intended behavior before implementation begins — not aesthetic polish. Based on R-611/R-612's framing of discussion mode as a requirements/ideas/design refinement tool rather than a visual-design approval gate.*

### Secondary Stakeholders

- **Design-Spec Author** (external, pre-existing — e.g., a prior designer or a past version of the developer): the origin of any imported design specification; not actively involved in this project, but their prior work constrains R-615/R-616. *(Ref: R-615, R-616)*
- **EDPS Framework Maintainer** (the developer wearing a different hat): ensures new skills integrate cleanly with `edps-workflow-orchestrator`, gates, and the broader skill catalogue rather than existing as a bolt-on. *(Ref: R-621, R-622)*

### Roles and Responsibilities

| Role | Responsibilities | Authority Level |
|------|-----------------|----------------|
| Solo Developer | Runs requirements → domain model → UI prototyping pipeline; makes final design calls in solo mode | Decision maker |
| Business/Product Stakeholder (role-played or real) | Reviews mockup, gives feedback, confirms direction | Confirms/approves (self-attested in solo mode per R-614) |
| Future Developer | Implements from the design document; may flag gaps back via change-management | Consumer, feedback source |
| Design-Spec Author | Provides the imported spec's conventions as a constraint | Passive (historical authority over style only) |
| EDPS Framework Maintainer | Ensures orchestrator/gate compliance | Gatekeeper for integration quality |

**Note on solo-mode break-out**: none of the WHO items above triggered the "break out of solo mode" criteria (genuine ambiguity, real external authority, high-stakes irreversibility) — all roles here are ones the developer can credibly self-represent for this requirements pass. This may change once real screens are reviewed with an actual business stakeholder, if one exists outside the developer.

## WHAT — Functional and Non-Functional Requirements

### Functional Requirements
- **F1**: Generate screen inventory, Markdown+HTML/CSS layout specs, and literal clickable HTML/JS mockups from requirements/domain model input *(Ref: R-601, R-602, R-602a)*
- **F2**: Model and diagram interaction flows between screens, kept consistent with the mockup's actual clickable transitions *(Ref: R-603, R-611a)*
- **F3**: Maintain a lightweight, evolving component inventory without formal design-system enforcement *(Ref: R-604)*
- **F4**: Trace every screen/component/flow back to source requirements and domain entities *(Ref: R-605, R-606)*
- **F5**: Produce a consolidated human-readable design document plus a machine-readable JSON companion *(Ref: R-607, R-608)*
- **F6**: Capture design rationale alongside design decisions, not just the resulting artifact *(Ref: R-609)*
- **F7**: Maintain an in-document changelog per design document as it evolves *(Ref: R-610)*
- **F8**: Support stakeholder discussion against the live mockup, including capturing feedback and routing it into `change-management` *(Ref: R-611, R-612)*
- **F9**: Surface clarifying questions when a requirement maps ambiguously to UI *(Ref: R-613)*
- **F10**: Support solo-mode role-play for discussion when no real stakeholder is available *(Ref: R-614)*
- **F11**: Import an existing design spec (same Markdown+HTML/CSS format) and conform subsequent generation to it, including partial-coverage gap detection and import-source traceability *(Ref: R-615–R-618)*
- **F12**: Integrate with the existing EDPS pipeline — consume analysis-skill outputs, register with the orchestrator, ship a gate.json, and reuse `stakeholder_confirmation`/`collaboration_mode` rather than inventing new mechanisms *(Ref: R-619, R-620, R-621, R-622)*

### Non-Functional Requirements
- **NF1**: All artifacts are plain text — diffable and version-controllable, no binary design-tool output *(Ref: R-623)*
- **NF2**: No assumed access to a commercial design tool for producing output *(Ref: R-624)*
- **NF3**: No assumed or targeted application framework — explicitly excludes general code scaffolding until a tech stack is chosen *(Ref: R-625)*
- **NF4**: Mockups run standalone via `file://`, zero build step, zero server *(Ref: R-626)*

### System Boundaries
- **In Scope**: Design-level artifacts — screen inventories, Markdown+HTML/CSS layout specs, literal clickable HTML/JS mockups, interaction-flow diagrams, design rationale, import/conformance handling, EDPS pipeline integration
- **Out of Scope**: Framework-specific code scaffolding (React/Vue/etc. component stubs), any functionality requiring a determined target tech stack, formal design-system governance/enforcement, real backend/data integration in the mockup (mockups are static/simulated, not wired to live data)

## WHEN — Timeline and Milestones

*(Solo-mode note: no externally imposed deadline exists yet; timeline below is a reasonable self-estimated sequencing, not a committed schedule. Would need real-stakeholder input per "When to Break Out of Solo Mode" if a hard external deadline were ever imposed.)*

### Project Timeline
- **Phase 1 — Requirements & Goals** (this phase): requirements.md, goals.md, w5h-analysis (current) — essentially complete pending final review
- **Phase 2 — Domain & Scope**: `domain-extractconcepts` against this requirements set; `process-scopemin` to define a minimal first version of the skill set (not every requirement needs a v1 skill)
- **Phase 3 — Skill Design**: author the actual new EDPS skill(s) — SKILL.md files, gate.json, orchestrator catalogue registration
- **Phase 4 — Validation**: a real end-to-end dry run — take a small existing project's requirements/domain model and generate an actual screen + mockup, confirming the pipeline works as designed

### Critical Milestones
- **M1**: Requirements/goals/W5H baseline agreed (this document + goals.md + requirements.md all reviewed)
- **M2**: Minimal viable scope defined (which of R-601–R-626 are v1 vs. deferred)
- **M3**: First working skill produces a real screen + mockup from a real input
- **M4**: Orchestrator/gate integration verified end-to-end

### Dependencies and Constraints
- Domain modeling (`domain-extractconcepts`) should run before detailed skill design, since R-606 ties screens to domain entities
- Orchestrator/gate integration (R-621) depends on the final skill names/IDs being settled — can't register in the DAG before the skill(s) exist

## WHERE — Context and Environment

### Operational Environment
- **Development Environment**: Local filesystem + git repo (`AI_Slowcooker`), markdown-capable editor, modern web browser for mockup viewing — no cloud/server dependency assumed *(Ref: R-624, R-626, NF2, NF4)*
- **Team Structure**: Solo developer, `collaboration_mode: solo` *(Ref: CON-7)*
- **Target Audience Location**: Wherever the stakeholder/future-developer happens to be — the zero-setup mockup portability requirement (R-626) is specifically there to remove environment friction

### System Integration Points
- **Upstream**: `requirements-ingest`, `domain-extractconcepts`, `goals-extract`, optionally `diagram-generatecollaboration` *(Ref: R-619)*
- **Downstream/Lateral**: `change-management` (feedback loop), `edps-workflow-orchestrator` (DAG + gates), `collaboration-mode-reference.md`'s `stakeholder_confirmation` mechanism *(Ref: R-620, R-621, R-622)*
- **Output Consumers**: a future developer implementing the real UI from the design document; potentially a future, not-yet-scoped code-scaffolding skill set once a tech stack is chosen *(Ref: R-607, R-625)*

### Physical and Virtual Boundaries
- **Artifact Location**: `OrgDocument/projects/06 - Building UI Prototype skills/artifacts/` following the standard EDPS `Analysis/`/`Documentation/` convention
- **Mockup Boundary**: standalone HTML/JS files, self-contained, no network calls to real backends (simulated data only, per System Boundaries above)

## WHY — Purpose and Business Rationale

### Business Drivers
- **Primary**: Let a solo developer discuss requirements/designs with stakeholders using something concrete to look at and click through, rather than abstract requirements text alone — reduces miscommunication risk before real implementation starts
- **Secondary**: Produce a design document durable enough that implementation doesn't require re-deriving intent from scratch or re-involving the original AI session
- **Strategic**: Extend the EDPS methodology's evolutionary, traceable approach into the UI/design layer, which prior iterations (1–4) didn't cover — closing a real gap in the existing skill set

### Problem Statement
Currently, EDPS skills take a project from raw requirements through domain modeling, diagrams, and planning — but stop short of anything a stakeholder can actually *look at*. Requirements and domain models are precise but abstract; a non-technical stakeholder reviewing a `domain-model.md` or `requirements.json` can't easily validate "is this what I meant" the way they could by clicking through a mockup.

### Success Metrics
- See `goals.md`'s Success Criteria (SC-1 through SC-8) and KPIs (KPI-1 through KPI-6) for the quantified version of this section.

### Value Proposition
- Faster, more concrete requirements validation loop (mockup-driven walkthroughs, R-611a)
- Design documents that directly double as implementation guides (embedded HTML/CSS, R-602/R-607) — less translation loss between "design" and "build"
- Reuses existing EDPS infrastructure (change-management, orchestrator, collaboration-mode gates) instead of creating a parallel, disconnected workflow

## HOW — Implementation Approach and Methods

### Technical Approach
- **Methodology**: Standard EDPS skill-authoring pattern — a new `.github/skills/<skill-name>/SKILL.md` + `gate.json` per new skill, following the conventions established across all 32 existing skills (see `skill-creator` for the meta-process)
- **Framework**: Plain Markdown + embedded HTML/CSS/JS as the artifact format (no new tooling dependency); Mermaid for flow diagrams, consistent with `diagram-generatecollaboration`
- **Integration Pattern**: New skill(s) consume `artifacts/Analysis/*.json` outputs from upstream skills and write their own outputs to `artifacts/Analysis/` and/or a new `artifacts/UI Prototype/` category, following existing conventions

### Implementation Strategy
1. **Scope Definition Phase**: Run `process-scopemin` against this requirements/goals baseline to decide v1 vs. deferred scope (e.g., is import/conformance in v1, or added later?)
2. **Domain Alignment Phase**: Run `domain-extractconcepts`/`domain-alignentities` so screens have real domain entities to reference (R-606)
3. **Skill Design Phase**: Draft SKILL.md(s) for the new skill(s) — likely candidates: a screen/mockup generation skill, an import/conformance skill, possibly split further depending on `process-scopemin`'s output
4. **Gate & Orchestrator Phase**: Write gate.json per new skill, register in the orchestrator's DAG (prerequisites likely: domain-extractconcepts, goals-extract)
5. **Validation Phase**: Dry-run the new skill(s) against a real small example (candidate: this very project's own domain, or a simple toy example) to confirm the pipeline actually produces a working mockup

### Risk Mitigation
- **Risk**: Scope too broad for a first version (generation + discussion + import all at once)
  - **Mitigation**: `process-scopemin` explicitly exists for this; don't skip it even though it feels like "just more planning"
- **Risk**: New skills don't integrate cleanly with the orchestrator/gates, becoming a disconnected side-feature
  - **Mitigation**: R-621/R-622 made integration an explicit requirement, not an afterthought; validate against `edps-workflow-orchestrator`'s actual DAG schema early
- **Risk**: "Literal interactive mockup" scope creeps toward full app development
  - **Mitigation**: R-625/CON-4 draws the line explicitly at no-target-framework; revisit only when a real tech-stack decision is made elsewhere

### Quality Assurance
- **Solo mode**: self-review checkpoints at each phase above, logged as self-attestations where a `stakeholder_confirmation` gate applies; break out to a real stakeholder if a design decision turns out to be genuinely ambiguous or high-stakes (per `process-w5h`'s own break-out criteria)
- Traceability (R-605/R-606) itself acts as a quality check — if a screen can't be traced to a requirement or domain entity, that's a signal scope has drifted

## Summary

This W5H analysis confirms the UI Prototyping skill set (PRJ-06) is a well-scoped extension of the existing EDPS framework: it has a clear single primary user (the solo developer, wearing multiple hats), a concrete problem statement (requirements/domain models are too abstract for stakeholder validation), and deliberately reuses existing EDPS infrastructure (change-management, orchestrator, collaboration-mode) rather than growing a parallel system. The main open implementation question is **scope sizing for v1** — recommend running `process-scopemin` next to decide what ships first versus what's deferred, before moving into actual skill design.
