---
name: screen-generatemockup
description: Generate or improve professional, genuinely interactive HTML/JS prototypes with working cross-page navigation, accessible popup dialogs, forms, filters, and local state. Use when rendering layout specs into file://-portable mockups, wiring prototype controls, or improving click-through behavior. Third skill in the UI Prototyping pipeline.
license: MIT
metadata:
  version: 1.1.0
  last-updated: "2026-11-01"
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

**No separate CSS/JS files.** Embed CSS and JS in each file. A screen renders independently, but cross-page navigation intentionally requires sibling screen folders; distribute the whole set without changing their relative paths.

**Verification evidence**: Append/update `## Prototype Verification` in the owning
`layout-spec.md` with observed browser results per the shared quality contract.
Do not claim completion while required checks are blocked or failing.

### HTML Structure (`mockup.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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

## Workflow

Read [Prototype Quality Contract](../screen-generatelayout/references/prototype-quality.md)
before rendering or revising a mockup. Use the two-page
[professional starter](assets/professional-starter/SCR-001/mockup.html) as a
runnable reference for styling and dialog behavior, not a mandatory screen design.

### Step 1 — Embed the layout spec's HTML/CSS verbatim

Copy the HTML structure and CSS rules from `layout-spec.md` into the `mockup.html` template above. Preserve the approved layout, styling, and traceability. For legacy specs missing professional styling or interaction/dialog definitions, improve the layout spec first with `screen-generatelayout`; do not silently redesign only the mockup. Add runtime behavior and accessibility attributes as needed and synchronize structural changes back to the spec.

### Step 2 — Identify and wire up navigation elements

Read the layout's Interaction Specification and wire every navigation control:
1. Use its explicit target ID and validate it against the full inventory. For legacy specs, resolve clear targets from context; flag ambiguity rather than guessing.
2. Use real `<a href="../SCR-[###]/mockup.html" data-transition-target="SCR-[###]">` links and current-page navigation state. Verify the destination file exists, not just its inventory entry.
3. Generate all screens needed for the selected journey before testing. If a target is unresolved or not generated, show a disabled action with a visible explanation and record it in Open Issues. Missing required journey links block completion; inline comments are not sufficient.

### Step 3 — Implement all specified local interactions and popup dialogs

Keep navigation as plain links and implement the Interaction Specification's
local behaviors with dependency-free vanilla JS. Every enabled control must
work: dialogs/popovers open and dismiss, filters alter results, forms validate
and update local sample state, and cancel discards edits. Follow the contract's
modal focus, keyboard, validation, and safe DOM rules. Prefer native `<dialog>`
and `showModal()` over custom overlays; do not use browser alert/confirm boxes
as a substitute. Mark simulated saves and state-reset limitations visibly.

### Step 4 — Confirm standalone self-containment

Verify there are no external resource dependencies: styles, scripts, fonts,
images, fetch calls, or framework runtimes. Use inline SVG/data URIs for needed
imagery, not placeholder boxes. Sibling mockup navigation links are allowed.

### Step 5 — Test portability (not assumed)

Per TR-06.2, open every generated file via `file://` in a real browser. Execute
the contract's full verification matrix: every link and return path, every
control, dialog lifecycle and validation, keyboard operation, responsive visual
review at 375/1440 px, and runtime errors/resource requests. Record actual
expected/observed results in Prototype Verification. If browser tooling is
unavailable, record Not run / blocked with manual steps; do not claim a pass
from code inspection or from merely launching a browser.

## Quality Checks

1. **Zero external resource dependencies**: no external CSS/JS/fonts/assets or fetch calls. Actual same-page anchors and relative mockup navigation are allowed; verify their targets rather than treating all `href` values as resource loads.
2. **No target-framework leakage**: no React/Vue/Angular runtime script tags, JSX-like syntax, or framework-specific attributes — same constraint as T05, re-verified here since this skill also touches markup directly.
3. **Navigation correctness**: every `<a href="../SCR-[###]/...">` link's target `SCR-[###]` actually exists in `screen-inventory.json` — no links to screens that don't exist.
4. **Genuine interaction**: exercise every specified control and reachable dialog/error/empty/success state, not merely one navigation link.
5. **Tested, not assumed, portability**: Step 5's real-browser `file://` test must actually have been performed for this screen's mockup before considering the task complete for it.
6. **Visual quality preserved**: review actual renders at both contract viewports, with shared styling, readable content, visible focus, and no page-level overflow.

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
