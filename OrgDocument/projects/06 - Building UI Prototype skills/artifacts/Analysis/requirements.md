# Requirements Analysis Report

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Source**: `artifacts/Source Materials/ui-prototyping-vision.md`
**Generated**: 2026-10-26
**Status**: Draft v1.3 — UI Model open questions resolved (integration ownership, regeneration behavior, multi-model support)
**Total Requirements**: 35

## Changelog

- **v1.3** (2026-10-26): Resolved OQ-G5–OQ-G7 (UI Model follow-up questions). Revised R-627, R-629. Added R-627a (shared ownership with existing modeling skills), R-629a (regenerate-on-change behavior), R-630/R-631/R-632 (base + derived role-based UI Models). Total requirements 31 → 35.
- **v1.2** (2026-10-26): Resolved OQ-G1–OQ-G4 (from goals.md analysis). Revised R-601, R-604, R-606, R-616. Added R-601a (new artifact category), R-603a (automated consistency gate), R-627/R-628/R-629 (new UI Model — Domain Alignment section). Total requirements 26 → 31.
- **v1.1** (2026-10-26): Resolved OQ-1 through OQ-5. Revised R-602, R-604, R-607, R-610, R-615; added R-602a, R-611a, R-625, R-626; removed Open Questions section (converted to Resolved Decisions log).
- **v1.0** (2026-10-26): Initial draft, 24 requirements, 5 open questions flagged.

## Summary

This project extends the EDPS skill framework with a new **UI Prototyping** skill category that sits alongside the existing analysis skills (requirements, goals, W5H, domain modeling, diagrams, planning). The goal is to let a solo developer use an AI-generated UI prototype as a living artifact for discussing requirements, ideas, and designs with stakeholders — producing durable design documents for future development, and optionally starting from an existing design specification rather than from scratch.

**Core format decision (v1.1)**: the primary deliverable is a **Markdown document with embedded HTML/CSS code** — readable as a design document, and literal enough to directly guide UI implementation. Where interactivity needs to be demonstrated, the skill set also generates a **literal interactive HTML/JS mockup** (clickable, not just specified) that a stakeholder can click through. Both the design document and the mockup are plain text, version-controllable, and require no special tooling to view.

**Model alignment decision (v1.2)**: a new **UI Model** artifact (`ui-model.md`/`ui-model.json`) is introduced as an intermediate alignment layer between the existing domain model and generated screens. It captures how domain entities aggregate into UI-facing concepts (e.g., a single "Order Summary" screen combining `Order` + `Customer` + `LineItem` entities), so screens reference stable UI Model entries rather than domain entities directly — insulating the UI layer from needing a full regeneration every time the domain model shifts slightly.

**Model governance decision (v1.3)**: UI Model generation lives in this new skill set, but is **co-evolved with the existing modeling skills** (`domain-alignentities`, `model-integration`) rather than owned unilaterally — when the domain model changes through those skills, the UI Model must be kept in step, and vice versa. When the UI Model changes, dependent screens are **regenerated**, not merely flagged stale. The UI Model itself is not always singular: a project may have one **base UI Model** plus multiple **derived role-based UI Models** (e.g., an Admin view vs. a Customer view of the same underlying domain), each tracing back to the base.

Three capabilities anchor the scope:
1. **Generate** — produce UI prototype artifacts (standalone screen inventory, UI Model, Markdown+HTML/CSS layout specs, interaction flows, a literal clickable HTML/JS mockup) from requirements, domain model, and UI Model inputs, traceable back to source requirements.
2. **Discuss** — use the generated prototype (including the clickable mockup) as a conversation surface with stakeholders to refine requirements/ideas/designs, capturing feedback as structured change input back into the EDPS pipeline.
3. **Import** — accept an existing UI design specification in the same Markdown+HTML/CSS format as a constraint/seed; when present, new generation must strictly reuse its observed conventions rather than inventing divergent ones.

**Scope boundary (v1.1, resolved)**: scope stops at design-level artifacts. The literal HTML/CSS/JS mockup *is* a design document in this project's model — it's in scope. General-purpose code scaffolding in a specific application framework is **out of scope** until a target tech stack is determined by a future project.

---

## Resolved Decisions (from Open Questions)

| # | Question | Decision |
|---|---|---|
| **D-1** (was OQ-1) | Import format for existing design specs | **Markdown with embedded HTML/CSS code**, the same format used for generated output (symmetric import/export). |
| **D-2** (was OQ-2) | Literal mockup vs. structured spec of interactivity | **Literal interactive HTML/JS mockup.** Stakeholders must be able to actually click through it. |
| **D-3** (was OQ-3) | Component inventory rigor | **Not rigorous by default — evolves with the model.** See D-8 for the refinement that this applies specifically to the no-import case. |
| **D-4** (was OQ-4) | Versioning mechanism for design iterations | **In-document changelog**, not reliance on git history alone. |
| **D-5** (was OQ-5) | Scope boundary re: code scaffolding | **Scope stops at design documents.** The HTML/CSS mockup counts as a design document; broader code scaffolding is deferred until a tech stack is determined. |
| **D-6** (was OQ-G1) | Screen inventory: standalone vs. embedded | **Standalone artifact**, output to `artifacts/UI Prototype/` in the consuming project (see R-601, R-601a) — not just a section inside the consolidated design document. Keeps small UI changes from requiring a full-document regeneration. |
| **D-7** (was OQ-G2) | Flow/mockup consistency checking | **Automatic.** Implemented as a gate check (see R-603a) rather than a manual review step. |
| **D-8** (was OQ-G3 + OQ-G4, combined) | Import conformance behavior and style extraction rigor | **Branches on whether an import exists:** if a design spec **is** imported, generation must **strictly follow** its observed conventions ("conformance" = reuse what's literally observed in the import — no formal schema validator, no invention of new styles). If **no** import exists, the system builds an MVP first and **evolves** components/style organically as the model grows (this is the scope of D-3's "non-rigorous" default). |
| **D-9** (new, user-initiated) | Introduce a UI Model reflecting the domain model and its aggregations | Confirmed — see **UI Model — Domain Alignment** section (R-627–R-632) and revised R-606. |
| **D-10** (was OQ-G5) | Who owns/generates the UI Model — this skill set, or existing modeling skills (`domain-alignentities`/`model-integration`)? | **This skill set generates it, but co-evolves it with the existing modeling skills** — neither a silent takeover of `domain-alignentities`'s territory, nor a fully isolated parallel model. See R-627a. |
| **D-11** (was OQ-G6) | When the UI Model changes due to a domain-model change, do affected screens auto-regenerate or just get flagged stale? | **Regenerate.** Judged more effective than a flag-and-wait approach — avoids screens silently drifting out of sync while waiting on manual review. See R-629a; in-document changelogs (R-610) retain the history so regeneration isn't destructive to traceability. |
| **D-12** (was OQ-G7) | Is one UI Model per project sufficient, or can there be multiple? | **Potentially multiple: a base model plus derived role-based models** (e.g., Admin vs. Customer views of the same domain). See R-630–R-632. |

**New concept introduced (v1.2, user-initiated, not from a prior open question)**: A **UI Model** should be introduced to improve alignment across models — it reflects the domain model and its aggregations, sitting between `domain-model.md` and generated screens. See the new **UI Model — Domain Alignment** section below (R-627–R-629) and revised R-606.

*Architectural placement note*: this draft places `ui-model.md`/`.json` alongside `domain-model.md` in the consuming project's `orgModel/[NN] - [Process Name]/` folder (a durable, evolving model artifact, not a one-off generation output), while screen inventories/mockups/layout specs live in that project's `artifacts/UI Prototype/` folder (iteration-specific generation outputs that reference the UI Model). This is a recommendation for your review, not a locked decision — flag if you'd place it differently.

---

## Requirements

### Generation — Screen & Flow Modeling

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-601 | Screen Inventory Generation (Standalone Artifact) | The system must generate a screen inventory as its **own standalone artifact** (`screen-inventory.md`/`.json`) — not embedded inside the consolidated design document — stored in the consuming project's `artifacts/UI Prototype/` folder. It lists each distinct screen/view, its purpose, and the primary entities/actions it exposes | functional, generation, core | high |
| R-601a | New Standard Artifact Category: "UI Prototype" | The EDPS standard project artifact categories (`Analysis`, `Changes`, `Documentation`, `Sample Data`, `Source Materials`, `Testing` — owned by `project-document-management`) must be extended with a new **`UI Prototype`** category to host this skill set's generation outputs (screen inventory, layout specs, mockups). This is a dependency on `project-document-management`'s folder-scaffolding templates, not something this skill set can introduce unilaterally | functional, generation, integration, core | high |
| R-602 | Layout Specification with Embedded Implementation Code | For each identified screen, the system must produce a layout specification as a **Markdown document with embedded HTML/CSS code** — literal enough to directly guide UI implementation, not just descriptive placeholders | functional, generation, core | high |
| R-602a | Literal Interactive Mockup | The system must also generate a **literal interactive HTML/JS mockup** per screen or flow — an actual file a stakeholder can open in a browser and click through, not merely a specification of what interactivity would look like | functional, generation, core | high |
| R-603 | Interaction Flow Modeling | The system must model navigation and interaction flows between screens (e.g., "Login → Dashboard → Order Detail"), expressed as a diagram (Mermaid, consistent with `diagram-generatecollaboration`'s existing conventions), and these flows must correspond to the actual clickable links/transitions implemented in the HTML/JS mockup (R-602a) | functional, generation, core | high |
| R-603a | Automated Flow/Mockup Consistency Check | The system must **automatically** verify that the Mermaid interaction-flow diagram (R-603) matches the mockup's actual clickable transitions (e.g., comparing documented edges against `<a href>`/JS navigation calls in the mockup), implemented as a gate check rather than a manual review step | functional, generation, validation, core | high |
| R-604 | Lightweight, Evolving Component Inventory (No-Import Case) | When no design specification has been imported (see R-615), the system must track a component inventory (buttons, forms, cards, navigation patterns) kept **informal and non-rigorous** — an MVP set built first and evolved organically as the model grows, not enforced as a formal design system. When an import **is** present, component conventions instead follow R-616's strict-conformance rule | functional, generation, low-rigor | medium |
| R-605 | Traceability to Requirements | Every generated screen, component, and flow must carry a traceability link back to the source requirement ID(s) that justify its existence | functional, traceability, core | high |
| R-606 | Traceability to UI Model (Revised — supersedes direct domain-entity reference) | Screens must reference entries in the **base or derived UI Model** (R-627, R-630, R-631) — not domain entities directly — so that a domain-model change requires updating the UI Model once rather than touching every affected screen individually. The UI Model itself traces to the domain entities it aggregates | functional, traceability, core | high |

### UI Model — Domain Alignment *(new in v1.2, extended in v1.3)*

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-627 | UI Model Generation | The system must generate a **UI Model** (`ui-model.md`/`.json`) for the consuming project, stored alongside `domain-model.md` in that project's `orgModel/[NN] - [Process Name]/` folder. It maps domain entities and their **aggregations** into UI-facing concepts (e.g., a screen-level "view" combining multiple domain entities into one coherent unit a user interacts with) | functional, generation, core | high |
| R-627a | Co-Evolution with Existing Modeling Skills | UI Model generation/maintenance is **owned by this skill set**, but must **co-evolve** with `domain-alignentities` and `model-integration` rather than operating as an isolated parallel model: when those skills update the domain model, this skill set must be invoked (or invoke itself) to keep the UI Model in step, and conversely a UI Model change that implies a domain insight should be surfaced back to those skills rather than silently diverging | functional, integration, core | high |
| R-628 | Screens Reference UI Model, Not Domain Directly | Generated screens (R-601, R-602) must reference UI Model entries as their primary traceability target (see revised R-606); the UI Model is the single place where domain-to-UI aggregation logic lives, rather than each screen re-deriving its own aggregation of domain entities | functional, traceability, core | high |
| R-629 | UI Model Evolution | The UI Model must evolve alongside `domain-model.md` as the project's domain understanding changes, following the same evolutionary/incremental-refinement principles EDPS already applies to other `orgModel` artifacts — not a one-time snapshot | nonfunctional, evolution, core | high |
| R-629a | Regenerate-on-Change | When the UI Model changes as a result of a domain-model update (R-629), all screens/mockups whose UI Model entry changed must be **regenerated**, not merely flagged as stale — judged more effective at keeping the prototype trustworthy than a flag-and-wait approach. Each regeneration must append an entry to the affected document's in-document changelog (R-610) so the regeneration itself is traceable and not silently destructive | functional, evolution, core | high |
| R-630 | Base UI Model | Every project must have exactly one **base UI Model** representing the full, role-agnostic aggregation of the domain model into UI-facing concepts — the default source of truth other UI Models derive from | functional, generation, core | high |
| R-631 | Derived Role-Based UI Models | The system must support generating one or more **derived UI Models**, each scoped to a specific user role or context (e.g., an Admin-facing model vs. a Customer-facing model of the same underlying domain), each one a filtered/adapted view of the base UI Model (R-630) rather than an independently authored model | functional, generation, medium | medium |
| R-632 | Derived Model Traceability and Sync | Each derived UI Model must trace back to the base UI Model entries it derives from, and must be regenerated (R-629a) when its corresponding base entries change — consistent with how screens regenerate from UI Model changes | functional, traceability, evolution, medium | medium |

### Generation — Design Document Output

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-607 | UI Design Document Output | The system must produce a consolidated **Markdown design document with embedded HTML/CSS code** summarizing screens, flows, components, and design rationale — literal enough to directly guide UI implementation, and suitable for handing to a future developer without requiring the original AI session | functional, output, core | high |
| R-608 | Machine-Readable Companion Output | Alongside the human-readable document, the system must produce a structured JSON representation of the same screens/flows/components, for downstream tooling | functional, output, core | high |
| R-609 | Design Rationale Capture | Each significant design decision must be captured with its rationale, not just the resulting artifact | functional, traceability, medium | medium |
| R-610 | In-Document Changelog Versioning | Each design document must carry its **own in-document changelog section** recording successive versions as stakeholder discussion refines it — not relying on git history alone to reconstruct design evolution | functional, evolution, core | high |

### Conversational / Discussion Mode

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-611 | Prototype as Discussion Surface | The system must support presenting the current prototype state — including the literal clickable HTML/JS mockup (R-602a) — as the basis for a structured discussion with a stakeholder, not just as a terminal artifact | functional, discussion, core | high |
| R-611a | Mockup-Driven Walkthrough | Because the mockup is literal and clickable (D-2), the discussion should be able to follow the stakeholder's actual navigation through it — observed clicks/paths can themselves surface where the flow diagram (R-603) needs correction | functional, discussion, medium | medium |
| R-612 | Feedback Capture | Stakeholder feedback given during a prototype discussion must be capturable in a structured form and routed into the existing `change-management` skill rather than being lost in conversation | functional, discussion, integration, core | high |
| R-613 | Clarifying Question Generation | When a requirement maps ambiguously to UI, the system should surface a specific clarifying question for the stakeholder rather than silently guessing | functional, discussion, medium | medium |
| R-614 | Solo-Mode Role-Play Alignment | Per the project's `collaboration_mode` (currently Solo), when no real stakeholder is available, the developer may role-play the relevant stakeholder perspective during discussion, with assumptions documented inline | functional, discussion, mode-aware, medium | medium |

### Import — Existing Design Specification

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-615 | Design Specification Import | The system must accept an existing UI design specification in the **same Markdown-with-embedded-HTML/CSS format** used for generated output (D-1), and parse it into the same internal screen/component/flow representation used for generated prototypes | functional, import, core | high |
| R-616 | Strict Conformance to Imported Spec | When a design specification **has been** imported, subsequent generation (new screens, flow extensions) must **strictly reuse** the imported spec's observed HTML/CSS conventions, component terminology, and visual/structural style — "conformance" means reusing what is literally observed in the import, not validating against a formal schema, and no new/divergent styling may be introduced for equivalent elements (D-8) | functional, import, core | high |
| R-617 | Partial Import / Gap Detection | When an imported spec covers only part of the required screens, the system must identify which required screens/flows are *not* covered by the import and flag them for generation or stakeholder clarification | functional, import, medium | medium |
| R-618 | Import Source Traceability | Screens/components originating from an imported spec must be distinguishable from newly generated ones in the output document, so a future developer knows which parts are externally authoritative vs. AI-proposed | functional, import, traceability, medium | medium |

### Integration with Existing EDPS Skills

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-619 | Pipeline Position | The UI prototyping skill set must consume outputs from existing analysis skills (`requirements-ingest`, `domain-extractconcepts`, `goals-extract`, optionally `diagram-generatecollaboration`) as primary inputs, following the same `artifacts/Analysis/` input/output convention used by all other EDPS skills | functional, integration, core | high |
| R-620 | Change Loop Back to Analysis Skills | Feedback captured during prototype discussion (R-612) that implies a requirements change must flow through `change-management`'s existing structured change-document workflow, not a separate ad-hoc mechanism | functional, integration, core | high |
| R-621 | Gate & Workflow Orchestrator Integration | New UI prototyping skills must register in `edps-workflow-orchestrator`'s skill catalogue (DAG prerequisites) and ship a `gate.json`, consistent with how all other EDPS skills integrate with the orchestrator | functional, integration, compliance | high |
| R-622 | Collaboration-Mode Awareness | Any stakeholder-confirmation points introduced by this skill set must use the existing `stakeholder_confirmation` gate check type and respect `collaboration_mode` — not a new, separate approval mechanism | functional, integration, mode-aware, high | high |

### Non-Functional / Constraints

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-623 | Text-Based, Version-Controllable Artifacts | All generated artifacts — Markdown, embedded HTML/CSS, JS mockup files, JSON, Mermaid — must be plain text so they can be diffed, versioned, and reviewed in git | nonfunctional, constraint, core | high |
| R-624 | No Assumed Design Tool Access | The skill set must not assume the developer has access to a specific commercial design tool to *produce* output | nonfunctional, constraint, core | high |
| R-625 | No Target Tech Stack Assumption | The skill set must not assume or target a specific application framework. The mockup is a standalone design artifact, not scaffolding for a particular framework; broader code-scaffolding capability is explicitly deferred (D-5) | nonfunctional, constraint, scope-boundary | high |
| R-626 | Mockup Portability | The generated HTML/JS mockup must run standalone (`file://`) without requiring a build step, package manager, or local server | nonfunctional, constraint, core | high |

---

## Glossary Suspects

- UI Prototype / Prototype State
- Screen Inventory (standalone artifact)
- **UI Model** (new — domain-to-UI aggregation layer; may be base or role-derived)
- **Base UI Model** (role-agnostic, singular per project)
- **Derived UI Model** (role/context-scoped, traces to base)
- **Aggregation** (domain entities combined into one UI-facing concept)
- **Co-Evolution** (UI Model kept in step with domain-model changes via existing modeling skills)
- **Regenerate-on-Change** (screens/derived models regenerate, rather than merely flag stale, when their source changes)
- Layout Specification (Markdown + embedded HTML/CSS)
- Literal Interactive Mockup (HTML/JS, clickable)
- Interaction Flow
- Flow/Mockup Consistency Check (automated)
- Component Inventory (informal/evolving when no import; strict reuse when import present)
- Design Specification (import source)
- Design Rationale
- In-Document Changelog
- Strict Conformance (to an imported spec)
- Clarifying Question (discussion mode)

## Traceability Note

This document is a **Draft** requirements analysis, manually authored and iteratively refined through direct conversation rather than run through the `requirements-ingest` skill mechanically. Recommend running it through `requirements-ingest` (or treating it as the `requirements.md` baseline as-is) before proceeding to `domain-extractconcepts`/`process-scopemin`, per the standard EDPS pipeline order.
