# Requirements Analysis Report

**Project**: PRJ-06 — 06 - Building UI Prototype skills
**Source**: `artifacts/Source Materials/ui-prototyping-vision.md`
**Generated**: 2026-10-26
**Status**: Draft v1.1 — open questions resolved, ready for `goals-extract` / `process-w5h`
**Total Requirements**: 26

## Changelog

*(Applying R-610's in-document changelog pattern to this document itself, as its first real instance.)*

- **v1.1** (2026-10-26): Resolved OQ-1 through OQ-5 (see decisions below). Revised R-602, R-604, R-607, R-610, R-615; added R-602a, R-611a, R-625, R-626; removed Open Questions section (converted to Resolved Decisions log).
- **v1.0** (2026-10-26): Initial draft, 24 requirements, 5 open questions flagged.

## Summary

This project extends the EDPS skill framework with a new **UI Prototyping** skill category that sits alongside the existing analysis skills (requirements, goals, W5H, domain modeling, diagrams, planning). The goal is to let a solo developer use an AI-generated UI prototype as a living artifact for discussing requirements, ideas, and designs with stakeholders — producing durable design documents for future development, and optionally starting from an existing design specification rather than from scratch.

**Core format decision (v1.1)**: the primary deliverable is a **Markdown document with embedded HTML/CSS code** — readable as a design document, and literal enough to directly guide UI implementation. Where interactivity needs to be demonstrated, the skill set also generates a **literal interactive HTML/JS mockup** (clickable, not just specified) that a stakeholder can click through. Both the design document and the mockup are plain text, version-controllable, and require no special tooling to view (a browser is enough for the mockup; any editor for the Markdown).

Three capabilities anchor the scope:
1. **Generate** — produce UI prototype artifacts (screen inventory, Markdown+HTML/CSS layout specs, interaction flows, a literal clickable HTML/JS mockup) from requirements and domain model inputs, traceable back to source requirements.
2. **Discuss** — use the generated prototype (including the clickable mockup) as a conversation surface with stakeholders to refine requirements/ideas/designs, capturing feedback as structured change input back into the EDPS pipeline.
3. **Import** — accept an existing UI design specification in the same Markdown+HTML/CSS format as a constraint/seed, so new generation conforms to it rather than inventing a new design language.

**Scope boundary (v1.1, resolved)**: scope stops at design-level artifacts. The literal HTML/CSS/JS mockup *is* a design document in this project's model — it's in scope. General-purpose code scaffolding (e.g., generating component stubs in a specific application framework like React/Vue/etc.) is **out of scope** until a target tech stack is determined by a future project; this skill set does not assume or target one.

---

## Resolved Decisions (from Open Questions, 2026-10-26)

| # | Question | Decision |
|---|---|---|
| **D-1** (was OQ-1) | Import format for existing design specs | **Markdown with embedded HTML/CSS code**, the same format used for generated output (symmetric import/export). The embedded code must be literal enough to guide implementation, not just descriptive prose. |
| **D-2** (was OQ-2) | Literal mockup vs. structured spec of interactivity | **Literal interactive HTML/JS mockup.** Stakeholders must be able to actually click through it, not just read a description of flows. |
| **D-3** (was OQ-3) | Component inventory rigor | **Not rigorous — evolves with the model.** No formal design-system enforcement in v1; the component inventory grows organically as screens are generated, tracked loosely rather than governed strictly. |
| **D-4** (was OQ-4) | Versioning mechanism for design iterations | **In-document changelog**, not reliance on git history alone. Each design document/screen carries its own changelog section (see this document's own Changelog above as the working example). |
| **D-5** (was OQ-5) | Scope boundary re: code scaffolding | **Scope stops at design documents.** The literal HTML/CSS mockup counts as a design document and is in scope. Broader code scaffolding in a specific target framework/tech stack is explicitly deferred until that tech stack is determined in a future project. |

---

## Requirements

### Generation — Screen & Flow Modeling

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-601 | Screen Inventory Generation | The system must generate a screen inventory from requirements and domain model inputs, listing each distinct screen/view, its purpose, and the primary entities/actions it exposes | functional, generation, core | high |
| R-602 | Layout Specification with Embedded Implementation Code | For each identified screen, the system must produce a layout specification as a **Markdown document with embedded HTML/CSS code** — literal enough to directly guide UI implementation, not just descriptive placeholders | functional, generation, core | high |
| R-602a | Literal Interactive Mockup | The system must also generate a **literal interactive HTML/JS mockup** per screen or flow — an actual file a stakeholder can open in a browser and click through, not merely a specification of what interactivity would look like | functional, generation, core | high |
| R-603 | Interaction Flow Modeling | The system must model navigation and interaction flows between screens (e.g., "Login → Dashboard → Order Detail"), expressed as a diagram (Mermaid, consistent with `diagram-generatecollaboration`'s existing conventions), and these flows must correspond to the actual clickable links/transitions implemented in the HTML/JS mockup (R-602a) | functional, generation, core | high |
| R-604 | Lightweight, Evolving Component Inventory | The system must track a component inventory (buttons, forms, cards, navigation patterns) referenced across screens, kept **informal and non-rigorous** — it evolves organically as the model grows rather than being enforced as a formal design system in v1 | functional, generation, low-rigor | medium |
| R-605 | Traceability to Requirements | Every generated screen, component, and flow must carry a traceability link back to the source requirement ID(s) and/or domain entities that justify its existence | functional, traceability, core | high |
| R-606 | Traceability to Domain Model | Screens must reference the domain entities (from `domain-extractconcepts`/`domain-model.md`) they display or manipulate, so UI and domain model stay in sync as either evolves | functional, traceability, core | high |

### Generation — Design Document Output

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-607 | UI Design Document Output | The system must produce a consolidated **Markdown design document with embedded HTML/CSS code** summarizing screens, flows, components, and design rationale — literal enough to directly guide UI implementation, and suitable for handing to a future developer without requiring the original AI session | functional, output, core | high |
| R-608 | Machine-Readable Companion Output | Alongside the human-readable document, the system must produce a structured JSON representation of the same screens/flows/components, for downstream tooling | functional, output, core | high |
| R-609 | Design Rationale Capture | Each significant design decision (e.g., "chose a wizard flow over a single form because requirement R-0XX specifies a multi-step approval") must be captured with its rationale, not just the resulting artifact | functional, traceability, medium | medium |
| R-610 | In-Document Changelog Versioning | Each design document must carry its **own in-document changelog section** recording successive versions as stakeholder discussion refines it — not relying on git history alone to reconstruct design evolution (see this requirements document's own Changelog section as the working pattern) | functional, evolution, core | high |

### Conversational / Discussion Mode

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-611 | Prototype as Discussion Surface | The system must support presenting the current prototype state — including the literal clickable HTML/JS mockup (R-602a) — as the basis for a structured discussion with a stakeholder, not just as a terminal artifact | functional, discussion, core | high |
| R-611a | Mockup-Driven Walkthrough | Because the mockup is literal and clickable (D-2), the discussion should be able to follow the stakeholder's actual navigation through it — observed clicks/paths can themselves surface where the flow diagram (R-603) needs correction | functional, discussion, medium | medium |
| R-612 | Feedback Capture | Stakeholder feedback given during a prototype discussion must be capturable in a structured form (e.g., "on Screen X, change field Y from optional to required") and routed into the existing `change-management` skill rather than being lost in conversation | functional, discussion, integration, core | high |
| R-613 | Clarifying Question Generation | When a requirement maps ambiguously to UI (e.g., unclear who can edit a field, unclear multi-step vs. single-step flow), the system should surface a specific clarifying question for the stakeholder rather than silently guessing | functional, discussion, medium | medium |
| R-614 | Solo-Mode Role-Play Alignment | Per the project's `collaboration_mode` (currently Solo — see Iteration 4's `collaboration-mode-reference.md`), when no real stakeholder is available, the developer may role-play the relevant stakeholder perspective during discussion, with assumptions documented inline, consistent with the existing solo-mode pattern used in `process-w5h` | functional, discussion, mode-aware, medium | medium |

### Import — Existing Design Specification

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-615 | Design Specification Import | The system must accept an existing UI design specification in the **same Markdown-with-embedded-HTML/CSS format** used for generated output (D-1), and parse it into the same internal screen/component/flow representation used for generated prototypes | functional, import, core | high |
| R-616 | Conformance to Imported Spec | Once a design specification has been imported, subsequent generation (new screens, flow extensions) must conform to the imported spec's HTML/CSS conventions, component terminology, and visual/structural style rather than introducing a divergent style | functional, import, core | high |
| R-617 | Partial Import / Gap Detection | When an imported spec covers only part of the required screens, the system must identify which required screens/flows are *not* covered by the import and flag them for generation or stakeholder clarification | functional, import, medium | medium |
| R-618 | Import Source Traceability | Screens/components originating from an imported spec must be distinguishable from newly generated ones in the output document, so a future developer knows which parts are externally authoritative vs. AI-proposed | functional, import, traceability, medium | medium |

### Integration with Existing EDPS Skills

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-619 | Pipeline Position | The UI prototyping skill set must consume outputs from existing analysis skills (`requirements-ingest`, `domain-extractconcepts`, `goals-extract`, optionally `diagram-generatecollaboration`) as primary inputs, following the same `artifacts/Analysis/` input/output convention used by all other EDPS skills | functional, integration, core | high |
| R-620 | Change Loop Back to Analysis Skills | Feedback captured during prototype discussion (R-612) that implies a requirements change must flow through `change-management`'s existing structured change-document workflow, not a separate ad-hoc mechanism | functional, integration, core | high |
| R-621 | Gate & Workflow Orchestrator Integration | New UI prototyping skills must register in `edps-workflow-orchestrator`'s skill catalogue (DAG prerequisites) and ship a `gate.json`, consistent with how all other EDPS skills integrate with the orchestrator introduced in Iteration 3 | functional, integration, compliance | high |
| R-622 | Collaboration-Mode Awareness | Any stakeholder-confirmation points introduced by this skill set (e.g., "stakeholder approved this screen design") must use the existing `stakeholder_confirmation` gate check type and respect `collaboration_mode`, consistent with Iteration 4's solo/traditional feature — not a new, separate approval mechanism | functional, integration, mode-aware, high | high |

### Non-Functional / Constraints

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|------------|
| R-623 | Text-Based, Version-Controllable Artifacts | All generated artifacts — Markdown, embedded HTML/CSS, JS mockup files, JSON, Mermaid — must be plain text so they can be diffed, versioned, and reviewed in git; no binary design-tool output for the primary deliverable | nonfunctional, constraint, core | high |
| R-624 | No Assumed Design Tool Access | The skill set must not assume the developer has access to a specific commercial design tool (e.g., Figma) to *produce* output — the core workflow (including the clickable mockup) must function with only EDPS skills, a markdown-capable editor, and a web browser | nonfunctional, constraint, core | high |
| R-625 | No Target Tech Stack Assumption | The skill set must not assume or target a specific application framework (React, Vue, etc.). The HTML/CSS/JS mockup is a standalone design artifact, not scaffolding for a particular framework; broader code-scaffolding capability is explicitly deferred (D-5) | nonfunctional, constraint, scope-boundary | high |
| R-626 | Mockup Portability | The generated HTML/JS mockup must run standalone (open directly in a browser, e.g., via `file://`) without requiring a build step, package manager, or local server, so a stakeholder can view it with zero setup | nonfunctional, constraint, core | high |

---

## Glossary Suspects

- UI Prototype / Prototype State
- Screen Inventory
- Layout Specification (Markdown + embedded HTML/CSS)
- Literal Interactive Mockup (HTML/JS, clickable)
- Interaction Flow
- Component Inventory (informal, evolving)
- Design Specification (import source — same Markdown+HTML/CSS format)
- Design Rationale
- In-Document Changelog
- Conformance (to an imported spec)
- Clarifying Question (discussion mode)

## Traceability Note

This document is a **Draft** requirements analysis, manually authored and iteratively refined through direct conversation (`ui-prototyping-vision.md` + resolved open questions above) rather than run through the `requirements-ingest` skill mechanically. Recommend running it through `requirements-ingest` (or reviewing it as-is and treating it as the `requirements.md` baseline) before proceeding to `goals-extract` and `process-w5h`, per the standard EDPS pipeline order.
