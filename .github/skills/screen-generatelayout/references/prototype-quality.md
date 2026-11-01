# Prototype Quality Contract

Apply this contract when generating or revising layouts, mockups, flows, handoffs,
and feedback walkthroughs. It defines a professional UI-design starting point,
not a production application or a mandatory visual theme.

## Contents

- [Visual design](#visual-design)
- [Interaction specification](#interaction-specification)
- [Runtime behavior](#runtime-behavior)
- [Verification and handoff](#verification-and-handoff)

## Visual design

1. Honor supplied brand guidelines and existing UI conventions. Otherwise choose
   one restrained, domain-appropriate direction and record it as a design
   assumption. Do not force dashboards, sidebars, or decorative cards on every UI.
2. Define concrete CSS custom properties for colors, typography, spacing, radii,
   shadows, and focus rings in the first layout. Reuse the same values and shared
   component styling across all subsequent layouts, including batch and
   single-screen revisions. No external fonts or icon libraries: use a system
   font stack and, when useful, inline SVG with accessible labels.
3. Establish clear hierarchy: page title, supporting context, grouped sections,
   one dominant primary action per task, and quieter secondary actions. Use a
   consistent spacing scale (for example 4/8/12/16/24/32 px), readable line height,
   restrained borders/shadows, and realistic, consistent sample data.
4. Specify hover, active, disabled, validation, and `:focus-visible` states.
   Communicate status with text as well as color. Target WCAG AA contrast:
   4.5:1 for normal text, 3:1 for large text, and 3:1 for meaningful control
   boundaries/focus indicators. Verify the actual selected color pairs.
5. Provide responsive CSS, not just a fixed desktop canvas. At 375 px and
   1440 px widths, avoid page-level horizontal overflow, clipped content, or
   overlapping actions. Scroll wide tables inside labeled containers when
   necessary. Give controls at least 24 x 24 px targets, preferably 44 px.
6. Include purposeful empty, validation-error, and success presentations for
   interactions that can reach those states. Do not add fake loading indicators
   to purely synchronous local actions. Avoid lorem ipsum and decorative
   placeholder boxes that conceal missing design work.

## Interaction specification

Include `## Interaction Specification` in every layout spec:

| Control ID | Trigger | Kind | Target | Result / state change | Keyboard / dismissal |
|---|---|---|---|---|---|
| order-history | Activate link | navigation | SCR-002 | Opens customer order history | Enter |
| edit-contact | Activate button | dialog-open | contact-dialog | Opens prefilled contact form | Enter or Space |
| save-contact | Submit form | local-action | contact-dialog | Validates email, updates summary, shows success, closes dialog | Enter |
| cancel-contact | Activate button | dialog-close | contact-dialog | Discards unsaved changes | Enter, Space, or Escape |

- Cover every visible actionable control, including menu items, table-row
  actions, filters, tabs, accordion headers, dialog triggers, and dismissals.
  Use stable HTML IDs matching the table. Do not infer destinations from labels
  alone when a target can be specified explicitly.
- Keep pages as `SCR-[###]` inventory entries. Keep dialogs, popovers, drawers,
  and local states inside their owning screen unless requirements justify a
  separately navigable view. Use locally unique HTML IDs, not new screen IDs.
- Use real relative links for navigation:
  `<a id="order-history" href="../SCR-002/mockup.html"
  data-transition-target="SCR-002">Order history</a>`.
  Supply both `href` and matching metadata in the layout when the target is known.
  Use `aria-current="page"` for the current navigation item.
- Use buttons for actions. Annotate local controls with `data-ui-action`
  (`dialog-open`, `dialog-close`, `local-action`) and a `data-ui-target` naming
  the dialog or affected element when applicable. Native controls such as
  `<details>` may rely on their built-in behavior, with IDs documented in the table.
- Specify dialog markup, labels, sample values, validation rules, save/cancel
  behavior, and whether backdrop dismissal is allowed. Prefer a native
  `<dialog aria-labelledby="...">` opened with `showModal()`.
- If a target or requirement is unresolved, record it visibly in the spec's
  `## Open Issues` and in the rendered prototype. Disable the affected action
  with a nearby explanation. An HTML comment alone is not adequate feedback.
  Never ship `href="#"`, `javascript:` links, empty handlers, or enabled no-ops.

## Runtime behavior

- Embed all CSS and vanilla JS in each `mockup.html`. No fetch, module imports,
  CDNs, external fonts/assets, package manager, or server. Sibling page links
  are the intentional exception to file self-containment; distribute the
  whole screen-folder set for multi-page navigation.
- Wire every interaction in the spec. Search/filter affects visible content,
  tabs change panels, and save updates the displayed local sample state.
  Confirm destructive actions before mutating state. Do not substitute
  `alert()`/`confirm()` for designed application dialogs.
- For modal dialogs, place focus meaningfully, keep Tab/Shift+Tab inside the
  modal, support Escape and a visible cancel/close control, and restore focus
  to the opener after all dismissal paths. Do not allow background interaction.
  Decide backdrop dismissal explicitly; do not dismiss destructive confirmations
  or discard unsaved form input accidentally.
- Validate before committing. Show field-level errors with associated text and
  `aria-invalid`, focus the first invalid field, preserve entered values on
  error, and announce successful changes through an `aria-live` status region.
  Cancel must not commit changes.
- Use in-memory sample state by default. State resets on reload and is not shared
  across pages; browser history may restore previous page state. Say so in a
  quiet visible prototype note and handoff. Only add cross-page
  persistence if explicitly needed, and do not depend on `file://` storage
  behavior. Never imply that a prototype saved to a real backend.
- Render user-entered text using `textContent` or safe DOM construction, not
  interpolated `innerHTML`. Do not include personal data or credentials.

## Verification and handoff

Record `## Prototype Verification` in each layout spec after generating its
mockup. Use a table with **Check**, **Expected**, **Observed**, **Status**, and
**Evidence** (browser/viewport and control ID or source location).

1. Open each actual file with `file://` in a real browser. Confirm styling,
   no console/runtime errors, and no unexpected network/asset requests.
2. Follow every navigation link to the actual existing file, including return
   paths and browser Back/Forward. Compare targets with the inventory; matching
   a regex or finding the destination folder alone is not a resolution test.
3. Exercise every interaction-table row, including disabled-control explanations.
   For each dialog test open, keyboard focus containment, Escape, cancel, reopen,
   invalid submit, valid save, focus restoration, and allowed/disallowed backdrop
   dismissal. Test reachable empty/error/success states.
4. Review the rendered UI at 375 px and 1440 px, plus keyboard-only operation,
   zoom/readability, selected contrast pairs, and consistency across screens.
   Capture screenshots when available for visual review, but screenshots alone
   do not prove interactions work.
5. Use browser automation when available and log what actually ran. If browser
   access is unavailable, label browser checks **Not run / blocked**, give manual
   steps, and leave completion pending. Code inspection, launching a browser
   process, and solo-mode self-attestation are not substitutes for observed behavior.
6. Handoff summarizes the visual direction, links to the authoritative token and
   interaction specs, identifies the first screen to open and principal journey,
   and reports verified behavior, open issues, and simulation limitations.
   Keep Markdown and JSON summaries equivalent.

## Runnable reference

Open [the bundled starter](../../screen-generatemockup/assets/professional-starter/SCR-001/mockup.html)
directly in a browser and keep both screen folders together. It demonstrates
cross-page navigation, a responsive order workspace, filtering, and an editable
contact dialog with validation, cancellation, focus restoration, and local
sample-state updates. Adapt its patterns to the domain; do not copy its order
content or treat its styling as a required brand.

### Starter verification (2026-11-01)

This is reference-template validation, not a new end-to-end requirements/domain
pipeline run or a retroactive pass for the historical MVP artifacts.

| Check | Expected | Observed | Status | Evidence |
|---|---|---|---|---|
| Modal lifecycle | Open, trapped focus, cancel/Escape discard, reopen, error, save and focus restoration | 19 dialog/accordion/runtime assertions passed after adding explicit Escape handling for the integrated browser | Pass | Integrated browser, actual SCR-001 file URL, 1440 px, control IDs `edit-contact`, `email-input`, `cancel-contact`, `save-contact`, `toggle-delivery` |
| Navigation and local state | All links, Back/Forward, filtering/empty state and reload reset work | 23 assertions passed, including all 6 page links, no runtime errors and no external resource requests | Pass | Integrated browser, both actual file URLs, 375/1440 px, `view-history`, `order-search`, `status-filter`, `view-order` and navigation IDs |
| Responsive design | No page-level horizontal overflow, dialog fits and hierarchy remains clear | Both widths passed geometry checks; desktop detail/history and narrow dialog screenshots reviewed | Pass | 375/1440 px browser viewports |
| Static contract | Valid gates, source links, IDs, shared tokens and measured contrast | 7 regression tests passed | Pass | `python .github/skills/screen-generatemockup/scripts/test_prototype_contract.py -v` from repository root |
| Skill metadata | Six updated skills validate and package | All 6 passed the existing skill-creator packager | Pass | `skill-creator/scripts/package_skill.py` with UTF-8 mode and session-local PyYAML |

Re-run the static checks after template/contract changes and repeat the browser
matrix above after changing HTML/CSS/JS. Static tests do not certify runtime
behavior or replace visual review.
