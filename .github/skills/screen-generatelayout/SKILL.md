---
name: screen-generatelayout
description: Generate a literal, implementation-ready Markdown + embedded HTML/CSS layout specification per screen, from a project's screen inventory. Second skill in the UI Prototyping pipeline (Project 06); its output is rendered into a clickable mockup by screen-generatemockup.
license: MIT
version: 1.0.0
last-updated: 2026-10-27
---

# Screen Generate Layout

Generate a literal, implementation-ready layout specification — Markdown with embedded HTML/CSS — for each screen in a project's screen inventory.

## Intent

Produce the **Layout Specification** (`LayoutSpec`, R-602) for each screen identified by `screen-generateinventory`: a Markdown document containing literal, usable HTML/CSS — not descriptive placeholders like "a header goes here" — specific enough to directly guide implementation. This is the core "hard problem" of the UI Prototyping skill set: everything upstream (requirements, UI Model, screen inventory) is abstract; this skill is the first point where the pipeline commits to a concrete, renderable design.

Each `LayoutSpec` carries forward the traceability already established by `screen-generateinventory` (`requirement_refs`, `ui_model_ref`) and adds its own in-document changelog (R-610) and captured design rationale (R-609, *best-effort in MVP — see Quality Checks*).

## Inputs

- **Primary**: `artifacts/UI Prototype/screen-inventory.json` (from `screen-generateinventory`)
- **Secondary**: `orgModel/[NN] - [Process Name]/ui-model.json` — specifically, the `UIModelEntry` each screen references, for its `domain_entity_refs` and `aggregation_description`, which inform what content/fields the layout should actually present
- **Format**: One or more `screens[]` entries from the inventory; this skill may run once per screen or in a batch across the whole inventory

> **Pre-condition**: `screen-generateinventory` must have already produced a `screen-inventory.json` with at least one screen. This skill has nothing to generate a layout *for* otherwise.

## Outputs

**Files Generated** (per screen, per T02's file layout convention):
- `artifacts/UI Prototype/SCR-[###]/layout-spec.md` — the Markdown document with embedded HTML/CSS (primary; this *is* the LayoutSpec, not a separate JSON companion — R-602 calls for a Markdown artifact directly, and HTML/CSS is naturally embedded as fenced code blocks, so no separate JSON representation is needed for this particular entity unlike ScreenInventory/UIModel)

### Markdown Structure (`layout-spec.md`)

```markdown
# Layout Specification — [Screen Name] *(LS-[###])*

**Screen**: [Screen Name] *(SCR-[###])*
**UI Model Entry**: UME-[###]
*(Ref: R-[###])*

## Changelog

- **v1.0** ([date]): Initial generation

## Purpose

[One or two sentences restating the screen's purpose from screen-inventory.json —
not duplicating data, but giving a human reader context before the markup below]

## Design Rationale

[Notable design decisions and why they were made — e.g., "Used a two-column layout
because the UI Model entry aggregates both Order and Customer data, and these read
better side-by-side than stacked." Best-effort in MVP — see Quality Checks.]

## Layout

### HTML

\`\`\`html
<!-- Literal, implementation-ready markup for this screen -->
<div class="screen screen--order-summary">
  <header class="screen__header">
    <h1>Order Summary</h1>
  </header>
  <section class="screen__content">
    <!-- ... -->
  </section>
</div>
\`\`\`

### CSS

\`\`\`css
/* Literal, implementation-ready styling for this screen */
.screen--order-summary {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
}
/* ... */
\`\`\`

---
**Traces to**: UME-[###], R-[###]
**Generated**: [timestamp]
```

## Core Function

**Input**: One screen-inventory entry (+ its referenced UIModelEntry for content guidance)
**Output**: One `layout-spec.md` per screen, containing literal HTML/CSS
**Output Destination**: `artifacts/UI Prototype/SCR-[###]/layout-spec.md`

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing a screen-inventory.json entry
(and, if available, its referenced UI Model entry).
Copilot will generate a literal Markdown+HTML/CSS layout specification.

Example prompt:
"Use screen-generatelayout to produce the layout specification for SCR-001
('Order Summary') from this screen-inventory.json and ui-model.json."
```

## Layout Generation Process

### Step 1 — Read the screen's context

From the screen-inventory entry: `screen_id`, `name`, `purpose`, `ui_model_ref`, `requirement_refs`. From the referenced `UIModelEntry` (via `ui_model_ref`): `domain_entity_refs` and `aggregation_description` — these tell you *what content* the screen needs to present (e.g., a screen tracing to a `UIModelEntry` aggregating `Order`+`Customer`+`LineItem` needs sections for each, not just a generic placeholder).

### Step 2 — Draft the HTML structure

Produce semantic, literal HTML reflecting the screen's actual content needs — real element structure (headers, sections, lists, forms as appropriate to the screen's purpose), not lorem-ipsum or `<!-- content here -->` placeholders. Field names and labels should be derived from the aggregated domain entities' actual attributes where known (e.g., from `domain-model.md`), not invented generically.

### Step 3 — Draft the CSS

Produce literal, workable CSS for the HTML structure from Step 2 — enough to convey actual layout (grid/flex structure, spacing, basic visual hierarchy), not necessarily polished visual design. The goal is a layout a stakeholder can read and understand, and a developer can build from directly — not a final visual-design pass.

### Step 4 — Capture design rationale (best-effort)

Where a non-obvious layout decision was made (e.g., choosing a two-column layout, choosing a list vs. card presentation), note it briefly in the Design Rationale section. Per R-609's scope-analysis.md classification (Enhancement, not Core/MVP), this is **best-effort** in MVP — a LayoutSpec without rich rationale is still valid output; this step should not block generation if there's nothing non-obvious to note.

### Step 5 — Write the changelog

Every `layout-spec.md` must include a Changelog section (R-610), even on first generation — write "v1.0 ([date]): Initial generation" rather than omitting the section until a second iteration exists. This matches T02 Section 3's checklist requirement and keeps the section's presence unconditional rather than something added only on revision.

### Step 6 — Verify against the hard-constraints checklist

Before considering this skill's output complete for a given screen, verify against `ui-prototyping-conventions.md` Section 3:
- [ ] Text-only output (Markdown + embedded HTML/CSS only)
- [ ] No design-tool dependency to produce this output
- [ ] No target-framework assumption (plain HTML/CSS only — no React/Vue/Angular markup, imports, or conventions)
- [ ] Changelog present (even if only one entry)
- [ ] No direct domain-entity reference in traceability (confirm the LayoutSpec cites `UME-[###]`, inherited from its Screen, not a domain entity directly)

(Mockup portability does not apply to this skill's own output — `layout-spec.md` is not itself a `file://`-opened artifact; that constraint applies to `screen-generatemockup`'s output in T06.)

## Quality Checks

1. **Literalness**: scan generated HTML/CSS for placeholder language ("TODO", "content here", "Lorem ipsum", "[insert...]") — none should appear in final output. If content is genuinely unknown (e.g., real field values), use realistic representative values instead of placeholders (e.g., "Order #10234" rather than "[Order ID]").
2. **Traceability preserved**: `requirement_refs` and `ui_model_ref` from the Screen's inventory entry are both present in the LayoutSpec's front matter, unchanged.
3. **Changelog unconditional**: present even on first generation, not only added later.
4. **No framework leakage**: no JSX, Vue single-file-component syntax, Angular directives, or framework-specific imports anywhere in the HTML/CSS blocks.

## Integration

**Upstream**: `screen-generateinventory` (provides the screen to lay out), the project's UI Model (provides content-guiding `UIModelEntry` detail)

**Downstream**: `screen-generatemockup` (T06, renders this LayoutSpec's HTML/CSS into a clickable, standalone mockup file), `screen-assembledocument` (T08, summarizes/references this LayoutSpec in the consolidated design document)

**Typical pipeline**:
```
screen-inventory.json (per screen) + ui-model.json (referenced entry)
        → screen-generatelayout → SCR-[###]/layout-spec.md
                                        ↓
                              screen-generatemockup → SCR-[###]/mockup.html
```

## Example Prompt

```
Use the screen-generatelayout skill to produce a layout specification.

Screen (from screen-inventory.json): SCR-001, "Order Summary"
UI Model Entry (from ui-model.json): UME-001, aggregates Order + Customer + LineItem

Produce a literal, implementation-ready Markdown document with embedded HTML/CSS —
not a descriptive wireframe. Include the changelog section and traceability fields.
```
