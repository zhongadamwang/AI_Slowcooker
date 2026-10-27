---
name: screen-generatemockup
description: Render a screen's layout specification (Markdown + embedded HTML/CSS) into a standalone, genuinely clickable HTML/JS mockup file that opens directly via file:// with zero build step. Third skill in the UI Prototyping pipeline (Project 06); its output is the primary stakeholder-discussion artifact and the basis for screen-generateflow's consistency checking.
license: MIT
version: 1.0.0
last-updated: 2026-10-27
---

# Screen Generate Mockup

Render a screen's layout specification into a standalone, clickable HTML/JS mockup — the literal interactive artifact a stakeholder can open in a browser and click through.

## Intent

Produce the **Interactive Mockup** (`InteractiveMockup`, R-602a) for each screen: a real, standalone HTML/JS file — not a specification of what interactivity *would* look like, but the actual clickable thing. This is the second of the two artifacts explicitly requested in the project's founding vision (`ui-prototyping-vision.md`): "a literal interactive HTML/JS mockup... clickable, not just specified." It is the artifact used for mockup-driven stakeholder discussion (R-611, R-611a — see `screen-discussfeedback`, T09) and the reference point `screen-generateflow` (T07) checks its interaction-flow diagrams against for consistency.

Unlike `screen-generatelayout`'s output, this skill's output must satisfy **R-626's portability constraint**: every generated mockup must open directly via `file://`, with zero build step, zero package manager, and zero local server — tested on a real browser, not assumed.

## Inputs

- **Primary**: `artifacts/UI Prototype/SCR-[###]/layout-spec.md` (from `screen-generatelayout`) — specifically its embedded HTML and CSS fenced code blocks
- **Secondary**: `artifacts/UI Prototype/screen-inventory.json` — the full screen set, needed to know which other `SCR-[###]` folders exist for generating real cross-screen navigation links (a single screen's layout spec alone doesn't reveal what other screens exist to link to)
- **Format**: One screen's layout spec HTML/CSS, plus the project's full screen list for link targets

> **Pre-condition**: `screen-generatelayout` must have already produced a `layout-spec.md` for the screen being rendered. This skill renders what T05 describes; it does not invent new layout content.

## Outputs

**Files Generated** (per screen, per T02's file layout convention):
- `artifacts/UI Prototype/SCR-[###]/mockup.html` — a single, standalone HTML file with embedded `<style>` (from the LayoutSpec's CSS) and embedded `<script>` (vanilla JS only, for click handling/navigation)

**No separate CSS/JS files.** Unlike a typical web project, this mockup embeds its CSS and JS directly inline in the single `mockup.html` file via `<style>`/`<script>` tags — this is a deliberate choice to guarantee R-626's portability: a single self-contained file has no relative-path dependencies that could break when opened via `file://` from an unpredictable working directory, and no risk of a stakeholder receiving `mockup.html` without its companion `style.css`/`script.js` if files are copied individually.

### HTML Structure (`mockup.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>[Screen Name] — Mockup (SCR-[###])</title>
<style>
/* Embedded verbatim from layout-spec.md's CSS block */
</style>
</head>
<body>
<!-- Embedded verbatim from layout-spec.md's HTML block, with navigation elements made clickable (see Step 2) -->
<div class="screen screen--order-summary">
  <header class="screen__header">
    <h1>Order Summary</h1>
    <nav class="screen__nav">
      <a href="../SCR-002/mockup.html" class="screen__nav-link" data-transition-target="SCR-002">View Customer Order History</a>
    </nav>
  </header>
  <section class="screen__content">
    <!-- ... -->
  </section>
</div>
<script>
  // Vanilla JS only. Used for any interactivity beyond plain <a href> navigation
  // (e.g., toggling a details panel) — kept minimal; real navigation between
  // screens should prefer plain <a href="../SCR-[###]/mockup.html"> links over
  // JS-driven navigation wherever a plain link suffices, since plain links are
  // simpler for screen-generateflow (T07) to detect and verify.
</script>
</body>
</html>
```

## Core Function

**Input**: One screen's `layout-spec.md` (HTML/CSS) + the project's screen-inventory for link targets
**Output**: One standalone `mockup.html` per screen
**Output Destination**: `artifacts/UI Prototype/SCR-[###]/mockup.html`

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing a screen's layout-spec.md
and the project's screen-inventory.json.
Copilot will render a standalone, clickable mockup.html.

Example prompt:
"Use screen-generatemockup to render SCR-001's layout-spec.md into a
clickable mockup.html, linking to the other screens in screen-inventory.json
where the layout's navigation elements call for it."
```

## Mockup Generation Process

### Step 1 — Embed the layout spec's HTML/CSS verbatim

Copy the HTML structure and CSS rules from `layout-spec.md` into the `mockup.html` template above. Do not alter the semantic structure or styling decided in T05 — this skill's job is to make the existing layout **clickable and standalone**, not to redesign it.

### Step 2 — Identify and wire up navigation elements

Scan the embedded HTML for elements that represent navigation to another screen (e.g., a link styled as "View Customer Order History", a button labeled "Back to Dashboard") — these are usually already present as placeholder-ish elements in the layout spec's HTML (e.g., `<a class="screen__nav-link">` with no `href`, or a `<button>` with a comment indicating its destination). For each one:
1. Determine the target screen by matching its intent against `screen-inventory.json`'s screen names/purposes
2. Convert it to a real `<a href="../SCR-[###]/mockup.html">` link (relative path, matching T02's per-screen sub-folder layout) if it isn't already
3. If no clear navigation target exists in the inventory for an element that implies one, **flag it rather than inventing a destination** — leave a clear inline comment (`<!-- screen-generatemockup: no matching screen found for this navigation element -->`) so the gap is visible, consistent with the EDPS principle of surfacing ambiguity rather than silently guessing.

### Step 3 — Add minimal vanilla JS only where a plain link is insufficient

Most navigation should be plain `<a href>` — no JS required. Only add `<script>` content for interactivity that genuinely cannot be expressed as a link (e.g., toggling a collapsible section within the same screen). Keep this to vanilla JS with no external dependencies, no framework runtime, no build step.

### Step 4 — Confirm standalone self-containment

Verify the generated `mockup.html` has **no external file references** of any kind — no `<link rel="stylesheet" href="...">`, no `<script src="...">` pointing to a separate file, no image `<img src="...">` pointing outside the file (if an image is genuinely needed, either omit it with a labeled placeholder box describing what would go there, or use an inline `data:` URI — never a path assuming a bundler or server will resolve it).

### Step 5 — Test portability (not assumed)

Per TR-06.2, actually open the generated `mockup.html` file via `file://` in a real browser — do not merely assert it should work. Confirm:
- The page renders without errors
- Styling is applied (the embedded `<style>` block is in effect)
- At least one navigation link, if present, successfully opens the target screen's mockup

## Quality Checks

1. **Zero external file dependencies**: scan for any `href`/`src` attribute pointing outside the mockup's own embedded content or a sibling `SCR-[###]/mockup.html` path — anything else (CDN links, relative paths to separate `.css`/`.js` files) is a portability violation.
2. **No target-framework leakage**: no React/Vue/Angular runtime script tags, JSX-like syntax, or framework-specific attributes — same constraint as T05, re-verified here since this skill also touches markup directly.
3. **Navigation correctness**: every `<a href="../SCR-[###]/...">` link's target `SCR-[###]` actually exists in `screen-inventory.json` — no links to screens that don't exist.
4. **Genuine clickability, not static rendering**: confirm the generated file is not merely a styled, non-interactive rendering of the layout — at least the navigation elements identified in Step 2 must be real, working links.
5. **Tested, not assumed, portability**: Step 5's real-browser `file://` test must actually have been performed for this screen's mockup before considering the task complete for it.

## Integration

**Upstream**: `screen-generatelayout` (provides the HTML/CSS to render), `screen-generateinventory`'s `screen-inventory.json` (provides valid navigation link targets)

**Downstream**: `screen-generateflow` (T07, checks its Mermaid flow diagram's edges against this mockup's actual `<a href>` navigation — this skill's output is the *ground truth* that flow diagrams are checked against, not the reverse), `screen-discussfeedback` (T09, presents this mockup as the discussion surface), `screen-assembledocument` (T08, references this mockup in the consolidated design document)

**Typical pipeline**:
```
SCR-[###]/layout-spec.md (HTML/CSS) + screen-inventory.json (link targets)
        → screen-generatemockup → SCR-[###]/mockup.html (standalone, clickable)
                                        ↓
                              screen-generateflow (checks consistency against this)
                              screen-discussfeedback (presents this for discussion)
```

## Example Prompt

```
Use the screen-generatemockup skill to render a clickable mockup.

Layout Spec (from SCR-001/layout-spec.md): [paste its HTML/CSS content]
Screen Inventory (from screen-inventory.json): [paste or reference, for link targets]

Produce a standalone mockup.html with embedded <style>/<script> only — no
external file references. Wire up any navigation elements to real sibling
screen mockups where the inventory confirms a matching target screen exists.
```
