---
name: screen-generateflow
description: Generate Mermaid interaction-flow diagrams across a project's screen set, reusing diagram-generatecollaboration's existing conventions, and manually verify the diagram's edges match the actual navigation implemented in generated mockups. Fourth skill in the UI Prototyping pipeline (Project 06); gives the screen set a connective narrative for stakeholder discussion.
license: MIT
version: 1.0.0
last-updated: 2026-10-27
---

# Screen Generate Flow

Generate Mermaid interaction-flow diagrams showing navigation between a project's screens, verified against the actual clickable mockups.

## Intent

Produce the **Interaction Flow** (`InteractionFlow`, R-603) for a project's screen set: a Mermaid diagram showing navigation/interaction between screens (e.g., "Login → Dashboard → Order Detail"), reusing `diagram-generatecollaboration`'s existing sequence-diagram conventions rather than inventing a new diagramming notation. Without this skill, a generated screen set is a disconnected pile of individually-clickable mockups with no narrative tying them together — this skill is what lets a stakeholder (or the developer, in solo mode) see and discuss the *journey* through the screens, not just each screen in isolation.

Critically, this skill's diagram is **not generated in a vacuum** — FR-07.1 requires its edges to correspond to the actual navigation already implemented in `screen-generatemockup`'s output (T06). The mockup is the ground truth; the flow diagram documents what the mockup actually does, not what was originally planned or intended. If the two diverge, the mockup wins and the diagram must be corrected (or, if the divergence reveals a mockup bug, the mockup is fixed and the diagram then documents the corrected behavior) — either way, this skill does not get to publish a diagram it hasn't verified against the real artifact.

## Inputs

- **Primary**: `artifacts/UI Prototype/screen-inventory.json` (from `screen-generateinventory`) — the full screen set and their names/purposes
- **Secondary**: `artifacts/UI Prototype/SCR-[###]/mockup.html` for every screen (from `screen-generatemockup`) — specifically, each mockup's actual `<a href="../SCR-[###]/mockup.html">` navigation links, which are this skill's ground truth for what edges to draw
- **Format**: The screen list plus the real navigation links embedded in each mockup file

> **Pre-condition**: Both `screen-generateinventory` and `screen-generatemockup` must have already run for the screens being diagrammed. This skill does not invent navigation — it documents navigation that already exists in the mockups.

## Outputs

**Files Generated** (project-level, not per-screen, per T02's file layout convention):
- `artifacts/UI Prototype/interaction-flows.md` — a single Markdown document containing one or more Mermaid flow diagrams for the project, consolidated rather than split per-screen (since a flow, by nature, spans multiple screens — splitting it per-screen would fragment a single coherent diagram across files for no benefit)

### Markdown Structure (`interaction-flows.md`)

```markdown
# Interaction Flows

**Project**: [project_id]
**Generated**: [timestamp]
**Source**: screen-inventory.json, SCR-[###]/mockup.html (all screens)

## Primary Navigation Flow *(IF-001)*
**Screens Involved**: SCR-001 (Order Summary), SCR-002 (Customer Order History)
**Verified Against**: SCR-001/mockup.html, SCR-002/mockup.html *(see Verification Log below)*

\`\`\`mermaid
flowchart LR
    SCR001["Order Summary (SCR-001)"] -->|"View Customer Order History"| SCR002["Customer Order History (SCR-002)"]
    SCR002 -->|"Back to Order"| SCR001
\`\`\`

## [Additional Flows...]

## Verification Log

| Flow | Edge | Mockup Source | Status |
|---|---|---|---|
| IF-001 | SCR-001 → SCR-002 | SCR-001/mockup.html, line [N]: `<a href="../SCR-002/mockup.html">` | ✅ Verified |
| IF-001 | SCR-002 → SCR-001 | SCR-002/mockup.html, line [N]: `<a href="../SCR-001/mockup.html">` | ✅ Verified |

---
**Traceability**: Diagram edges verified against actual mockup navigation per FR-07.1 (manual in MVP; see screen-generateflow's own Quality Checks)
**Generated**: [timestamp]
```

## Core Function

**Input**: Screen inventory + all screens' mockup.html navigation links
**Output**: A single consolidated flow-diagram document for the project
**Output Destination**: `artifacts/UI Prototype/interaction-flows.md`

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing screen-inventory.json and
the full set of generated mockup.html files.
Copilot will produce a verified Mermaid flow diagram.

Example prompt:
"Use screen-generateflow to diagram navigation across these screens,
verifying every edge against the actual <a href> links in their mockup.html
files — do not include an edge unless you can point to its source link."
```

## Flow Generation Process

### Step 1 — Extract actual navigation edges from the mockups

For every screen's `mockup.html`, scan for `<a href="../SCR-[###]/mockup.html">` links (the real navigation, per `screen-generatemockup`'s Step 2 convention). Record each one as a directed edge: source screen → target screen, with the link's visible text/label as the edge's description.

**Do not** derive edges from the screen inventory's purposes/descriptions alone, and do not derive them from what the requirements *implied* the flow should be — only from links that actually exist in the generated mockups. This is the mechanism that satisfies FR-07.1.

### Step 2 — Group edges into coherent named flows

Where the screen set has multiple distinct user journeys (e.g., an "order review" flow vs. a "customer management" flow), group edges into separate named Mermaid diagrams (`IF-001`, `IF-002`, ...) rather than one giant diagram mixing unrelated journeys — consistent with `diagram-generatecollaboration`'s practice of multiple focused diagrams over one monolithic one. A small screen set may only need one flow; don't force an artificial split.

### Step 3 — Render using `diagram-generatecollaboration`'s Mermaid conventions

Use `flowchart LR` (left-to-right) for screen-to-screen navigation flows — distinct from `diagram-generatecollaboration`'s `sequenceDiagram` style, which models message exchanges between system participants (actors/boundaries/controls/entities), not screen-to-screen UI navigation. Screen navigation is more naturally a flowchart (nodes = screens, edges = navigation actions) than a sequence diagram (which implies time-ordered messages between distinct system components). Reuse `diagram-generatecollaboration`'s general Mermaid styling conventions (clear node labels including the screen's ID, descriptive edge labels) while choosing the diagram *type* appropriate to this skill's actual content.

### Step 4 — Build the Verification Log (FR-07.1's non-skippable step)

Per TR-07.1, this step is **mandatory and non-skippable in MVP** — do not publish `interaction-flows.md` without it. For every edge in every diagram, record in the Verification Log table: which mockup file and (approximately) which line contains the actual `<a href>` that justifies this edge's existence. If an edge cannot be matched to a real link, **do not include it in the diagram** — go back to Step 1 and re-check, or flag the discrepancy explicitly rather than drawing an aspirational edge that doesn't exist yet.

### Step 5 — Reconcile mockup/flow divergence, if found

If Step 4 reveals a mockup has a navigation link the diagram hadn't captured, or the diagram had assumed an edge that the mockup doesn't actually implement, resolve the divergence before finalizing: either add the missing edge (if the mockup's link is correct and intentional) or flag the mockup for correction (if the link exists but shouldn't, or is missing but should exist per the screen's purpose) — do not silently publish a diagram known to diverge from the real mockups.

## Quality Checks

1. **Every edge traces to a real `<a href>`**: no edge in any diagram lacks a corresponding Verification Log entry pointing to an actual mockup link.
2. **No orphaned diagrams**: every screen that has at least one navigation link in its mockup should appear in at least one flow diagram — a screen with real navigation that's absent from every diagram is a gap, not an acceptable omission.
3. **Consolidated, not fragmented**: output is one project-level `interaction-flows.md`, never split per-screen (contrast with `layout-spec.md`/`mockup.html`, which are correctly per-screen since those entities genuinely are per-screen; a flow is not).
4. **Manual verification actually performed**: per TR-07.1, this is a required, logged step in MVP (the Verification Log *is* the evidence this happened) — not an automated gate check yet (that's R-603a, Phase 2 Enhancement, deferred per `scope-analysis.md`).
5. **Mermaid syntax verified**: render every fenced Mermaid block with the target renderer before publishing; fix any parse or render errors.
6. **No statement-separator text in labels**: avoid literal semicolons (`;`) in Mermaid labels or diagram text, where they can be parsed as statement separators. Use commas, conjunctions, or separate statements instead.

## Integration

**Upstream**: `screen-generateinventory` (screen set), `screen-generatemockup` (ground-truth navigation links)

**Downstream**: `screen-assembledocument` (T08, summarizes/references `interaction-flows.md` in the consolidated design document), `screen-discussfeedback` (T09, R-611a's mockup-driven walkthrough can use this flow diagram as a map of the discussion, and observed stakeholder clicks during discussion may themselves surface a needed correction to this diagram — see R-611a)

**Typical pipeline**:
```
screen-inventory.json + all SCR-[###]/mockup.html (navigation links)
        → screen-generateflow → interaction-flows.md (verified against real mockup links)
                                        ↓
                              screen-assembledocument (T08)
                              screen-discussfeedback (T09)
```

**Relationship to R-603a (Phase 2, not this task)**: this skill's Step 4/5 verification process is explicitly manual in MVP. The Phase 2 Enhancement feature (R-603a) will eventually automate this same check as a gate (`flow_mockup_consistency` check type, already reserved in `domain-concepts.md`'s `GateCheck` entity) — when that's built, it should automate exactly what Steps 4–5 already do manually, not redesign the verification logic from scratch.

## Example Prompt

```
Use the screen-generateflow skill to diagram navigation for this project.

Screen Inventory (from screen-inventory.json): [paste or reference]
Mockups (from SCR-*/mockup.html): [paste or reference all generated mockup files]

Produce interaction-flows.md with Mermaid flowchart diagrams, grouped into
coherent named flows. Include a Verification Log confirming every edge traces
to a real <a href> link in the mockups — do not include any edge you cannot
verify against an actual link.
```
