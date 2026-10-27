# Goals Analysis

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Source**: requirements.md (v1.3)
**Generated**: 2026-10-26 (updated)

## Business Goal

Extend the EDPS skill framework with a UI Prototyping skill set that lets a solo, AI-aided developer turn requirements and domain models directly into literal, clickable HTML/CSS/JS prototypes — usable both as a stakeholder discussion surface and as an implementation-ready design document — while supporting import of an existing design spec so new work conforms to it rather than reinventing a style. *(Ref: R-601, R-602, R-602a, R-611, R-615)*

## Success Criteria

- **SC-1**: Generate a complete, standalone screen inventory artifact and Markdown+HTML/CSS layout spec for every screen identified from requirements/domain model input *(Ref: R-601, R-601a, R-602)*
- **SC-2**: Every generated screen has a corresponding literal, clickable HTML/JS mockup that opens directly in a browser with zero build step *(Ref: R-602a, R-626)*
- **SC-3**: Interaction flows (Mermaid diagrams) match the actual clickable transitions implemented in the mockup, **verified automatically via a gate check** — no divergence between the documented flow and the clickable experience *(Ref: R-603, R-603a)*
- **SC-4**: Every screen, component, and flow traces back to at least one source requirement ID and a **UI Model** entry (which itself traces to domain entities) *(Ref: R-605, R-606, R-627, R-628)*
- **SC-5**: Stakeholder feedback given while reviewing the mockup is captured in structured form and successfully routed into `change-management` without being lost *(Ref: R-612, R-620)*
- **SC-6**: An existing design specification (same Markdown+HTML/CSS format) can be imported and subsequent generation **strictly reuses** its observed components/terminology/style, with no divergent styling introduced *(Ref: R-615, R-616)*
- **SC-7**: New UI prototyping skills are fully registered in `edps-workflow-orchestrator`'s DAG with working `gate.json` files, consistent with all existing EDPS skills *(Ref: R-621)*
- **SC-8**: Every design document produced carries its own in-document changelog reflecting at least one real iteration cycle *(Ref: R-610)*
- **SC-9**: A UI Model artifact exists alongside `domain-model.md`, correctly reflecting domain entities and their aggregations into UI-facing concepts, and evolves as the domain model changes *(Ref: R-627, R-629)*

## Key Performance Indicators

- **KPI-1**: Mockup portability — 100% of generated mockups open successfully via `file://` with no server/build step across at least two major browsers *(Ref: R-626)*
- **KPI-2**: Traceability coverage — 100% of generated screens/components carry a resolvable link to a source requirement and a UI Model entry *(Ref: R-605, R-606, R-628)*
- **KPI-3**: Flow/mockup consistency — 0 discrepancies between the Mermaid interaction-flow diagram and the mockup's actual clickable transitions, **checked automatically by a gate** on every generation/regeneration *(Ref: R-603, R-603a, R-611a)*
- **KPI-4**: Feedback-to-change latency — stakeholder feedback captured during a discussion session is expressible as a `change-management` structured change document within the same session, with no manual re-transcription step *(Ref: R-612)*
- **KPI-5**: Import conformance — when a design spec is imported, 100% of newly generated screens reuse its existing component terminology/style with **zero** newly invented, divergent naming for equivalent elements *(Ref: R-616)*
- **KPI-6**: Orchestrator integration completeness — all new skills in this set appear in the orchestrator's skill catalogue and pass their own `gate.json` validation *(Ref: R-621)*
- **KPI-7**: UI Model freshness — UI Model is regenerated/updated within the same session as any domain-model change that affects an aggregation it defines *(Ref: R-629)*

## Constraints

- **CON-1**: Primary deliverable format is fixed as Markdown with embedded HTML/CSS — no alternate primary format (e.g., Figma-native, binary) *(Ref: R-602, R-607, R-623)*
- **CON-2**: Mockups must be standalone HTML/JS with no build step, package manager, or local server dependency *(Ref: R-626)*
- **CON-3**: Must not assume access to a specific commercial design tool (e.g., Figma) to produce output *(Ref: R-624)*
- **CON-4**: Must not assume or target a specific application framework (React, Vue, etc.) — code scaffolding beyond the standalone mockup is explicitly out of scope until a tech stack is chosen *(Ref: R-625, D-5)*
- **CON-5**: Component inventory stays informal/evolving **only when no design spec has been imported**; when a spec **is** imported, conformance is strict (reuse exactly what's observed, no invention) *(Ref: R-604, R-616, D-3, D-8)*
- **CON-6**: Any stakeholder-confirmation mechanism must reuse the existing `stakeholder_confirmation` gate check type and respect `collaboration_mode` rather than introducing a new, separate approval path *(Ref: R-622)*
- **CON-7**: Collaboration mode for this project is currently **Solo** — discussion-mode requirements (R-611 family) must function even with no second real person available, via role-play per `process-w5h`'s existing pattern *(Ref: R-614)*
- **CON-8**: Screens must not reference domain entities directly — all traceability routes through the UI Model (base or derived), which is the single owner of domain-to-UI aggregation logic *(Ref: R-606, R-628)*
- **CON-9**: The UI Model is not independently authored per role — derived (role-based) UI Models must be filtered/adapted views of the single base UI Model, not separately maintained models *(Ref: R-630, R-631)*
- **CON-10**: UI Model changes must not silently diverge from the domain model — co-evolution with `domain-alignentities`/`model-integration` is required, not optional *(Ref: R-627a)*

## Assumptions

- **ASM-1**: The existing analysis-skill outputs this project depends on (`requirements.json`/`requirements.md`, `domain-concepts.json`, `goals.json`) are available and well-formed before UI prototyping skills run *(Ref: R-619)*
- **ASM-2**: A single developer (solo mode) can meaningfully role-play all relevant stakeholder perspectives for v1 discussion-mode usage; a real multi-person review is deferred until a genuine need arises *(Ref: R-614, CON-7)*
- **ASM-3**: Modern web browsers (recent Chrome/Firefox/Safari) are available in the developer's and stakeholders' environments to view generated mockups — no requirement to support legacy browsers *(Ref: R-626)*
- **ASM-4**: `diagram-generatecollaboration`'s existing Mermaid conventions are suitable for representing UI interaction flows without modification *(Ref: R-603)*
- **ASM-5**: The `change-management` skill's existing structured change-document schema can represent UI-specific feedback without needing a new change type *(Ref: R-612, R-620)*
- **ASM-6**: No target tech stack will be determined within this project's timeframe; code-scaffolding scope (R-625) remains deferred for the full duration of this effort *(Ref: D-5)*
- **ASM-7**: `project-document-management` can be extended with a new `UI Prototype` artifact category without breaking existing project archetypes (flat/standard/hierarchical) *(Ref: R-601a)*
- **ASM-8**: A UI Model can meaningfully represent "aggregation" (multiple domain entities combining into one UI-facing concept) using the same Markdown+JSON conventions as `domain-model.md`, without needing a new modeling notation *(Ref: R-627)*
- **ASM-9**: Regenerating screens on every UI Model change (R-629a) remains tractable in practice — i.e., regeneration doesn't become so frequent/expensive that it discourages iterative domain refinement. Revisit if this assumption proves false once real usage begins *(Ref: R-629a)*
- **ASM-10**: `domain-alignentities`/`model-integration` can be invoked or coordinated with from this new skill set without requiring breaking changes to their existing interfaces *(Ref: R-627a)*

## Resolved Decisions (carried from requirements.md)

| # | Decision |
|---|---|
| **D-6** (was OQ-G1) | Screen inventory is a **standalone artifact** in `artifacts/UI Prototype/`, not embedded in the consolidated design document |
| **D-7** (was OQ-G2) | Flow/mockup consistency is checked **automatically** via a gate (R-603a), not manually |
| **D-8** (was OQ-G3 + OQ-G4) | **If an import exists**: strict conformance — reuse exactly what's observed, no new styling invented. **If no import exists**: build MVP first, evolve informally (non-rigorous) |
| **D-9** (new, user-initiated) | Introduce a **UI Model** reflecting the domain model and its aggregations, as an alignment layer between domain model and generated screens (R-627–R-629) |
| **D-10** (was OQ-G5) | UI Model is **generated by this skill set**, but **co-evolved** with `domain-alignentities`/`model-integration` rather than owned in isolation (R-627a) |
| **D-11** (was OQ-G6) | When the UI Model changes, affected screens are **regenerated** (not just flagged stale) — judged more effective at keeping the prototype trustworthy (R-629a) |
| **D-12** (was OQ-G7) | UI Models can be **multiple**: one **base** model plus **derived role-based** models (e.g., Admin vs. Customer), each tracing back to the base (R-630–R-632) |

## Open Questions

*(All goals-phase open questions OQ-G1–OQ-G7 are now resolved — see Resolved Decisions above. None outstanding at this stage; next open questions, if any, are expected to surface during `domain-extractconcepts`/`process-scopemin`.)*

---
**Traceability:** Extracted from requirements: R-601–R-632, D-1–D-12 (`artifacts/Analysis/requirements.md`, v1.3)
**Generated:** 2026-10-26 (updated)
