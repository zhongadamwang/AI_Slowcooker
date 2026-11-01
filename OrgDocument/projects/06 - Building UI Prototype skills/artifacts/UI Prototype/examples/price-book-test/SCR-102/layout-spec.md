# Layout Specification — Price Category Management *(LS-102)*

**Screen**: Price Category Management *(SCR-102)*
**UI Model Entry**: UME-102
*(Ref: R-703, R-711, R-712, R-713, R-719, R-720, R-721, R-723)*

## Changelog

- **v1.0** (2026-10-27): Initial generation
- **v1.1** (2026-11-01): Recreated as a responsive, interactive prototype; added version metadata, control behavior, and verification criteria.
- **v1.2** (2026-11-01): Recorded browser interaction and responsive verification after prototype recreation.

## Purpose

Lets a user, after selecting a Price Book, view, create, copy, edit, and delete Price Categories — each organized by one or more Service Lines.

## Design Rationale

Added a Price Book filter dropdown with a Clear button above the list, directly reflecting the source requirement's cascading-dependency rule (R-711/R-722): a Price Category only makes sense in the context of a selected Price Book, so the filter is placed prominently above the list rather than buried in the detail tabs. The Service Line field is rendered as a multi-select list (not a single dropdown) since R-713 states a category may have more than one Service Line.

## Layout

### HTML

```html
<div class="screen screen--price-category">
  <header class="screen__header">
    <h1>Price Category Management</h1>
  </header>
  <section class="screen__filter">
    <label for="price-book-filter">Price Book</label>
    <select id="price-book-filter">
      <option selected>1001 — Standard Service Pricing</option>
      <option>1002 — Promotional Pricing Q4</option>
    </select>
    <button class="btn" data-action="clear-filter">Clear</button>
  </section>
  <section class="screen__list-section">
    <div class="list-toolbar">
      <button class="btn btn--primary" data-action="add">Add</button>
      <button class="btn" data-action="copy-to-add">Copy to Add</button>
      <button class="btn" data-action="edit">Edit</button>
      <button class="btn btn--danger" data-action="remove">Remove</button>
    </div>
    <table class="record-list">
      <thead>
        <tr>
          <th>ID</th>
          <th>Version</th>
          <th>Description</th>
          <th>Book ID</th>
        </tr>
      </thead>
      <tbody>
        <tr class="record-list__row record-list__row--selected">
          <td>2001</td>
          <td>1</td>
          <td>Coiled Tubing Services</td>
          <td>1001</td>
        </tr>
        <tr class="record-list__row">
          <td>2002</td>
          <td>0</td>
          <td>Primary Cementing Services</td>
          <td>1001</td>
        </tr>
      </tbody>
    </table>
  </section>
  <section class="screen__detail-section">
    <nav class="detail-tabs" role="tablist">
      <button class="detail-tabs__tab detail-tabs__tab--active" role="tab">Data</button>
      <button class="detail-tabs__tab" role="tab">Effective Info</button>
      <button class="detail-tabs__tab" role="tab">Currently Version Info</button>
      <button class="detail-tabs__tab" role="tab">Original Version Info</button>
    </nav>
    <div class="detail-tabs__panel" role="tabpanel">
      <dl class="detail-form">
        <dt>ID</dt><dd><input type="text" value="2001" readonly class="field--readonly"></dd>
        <dt>Price Book</dt><dd><input type="text" value="1001 — Standard Service Pricing" readonly class="field--readonly"></dd>
        <dt>Description</dt><dd><input type="text" value="Coiled Tubing Services"></dd>
        <dt>Service Line</dt>
        <dd>
          <select multiple class="multi-select" size="4">
            <option selected>Coiled Tubing</option>
            <option>CBM Coil Tubing</option>
            <option>Nitrogen Coil</option>
            <option>Operations</option>
          </select>
        </dd>
      </dl>
    </div>
  </section>
  <footer class="screen__footer">
    <button class="btn btn--primary" data-action="update">Update</button>
    <button class="btn" data-action="close">Close</button>
  </footer>
</div>
```

### CSS

```css
.screen--price-category {
  font-family: system-ui, sans-serif;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.screen__filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eee;
}
.screen__filter label { font-size: 0.85rem; color: #555; }
.screen__filter select {
  padding: 0.3rem 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.list-toolbar { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
.btn {
  padding: 0.4rem 0.9rem;
  border: 1px solid #ccc;
  background: #f8f8f8;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}
.btn--primary { background: #2563eb; color: white; border-color: #2563eb; }
.btn--danger { background: #fff; color: #dc2626; border-color: #dc2626; }
.record-list { width: 100%; border-collapse: collapse; }
.record-list th, .record-list td {
  text-align: left;
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid #eee;
}
.record-list__row--selected { background: #eff6ff; }
.detail-tabs { display: flex; gap: 0.25rem; border-bottom: 1px solid #ddd; }
.detail-tabs__tab {
  padding: 0.5rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.85rem;
  color: #666;
}
.detail-tabs__tab--active {
  border-bottom: 2px solid #2563eb;
  color: #2563eb;
  font-weight: 600;
}
.detail-form {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 0.5rem 1rem;
  padding: 1rem 0;
}
.detail-form dt { font-size: 0.8rem; color: #666; align-self: start; padding-top: 0.3rem; }
.field--readonly { background: #f3f4f6; color: #666; }
.multi-select { width: 100%; }
.screen__footer {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  padding-top: 0.75rem;
  border-top: 1px solid #eee;
}
```

---
## Visual Design

Use the shared Northstar Pricing direction across SCR-101–SCR-104: calm blue navigation and primary actions, white work surfaces, a pale slate canvas, restrained borders, and system sans-serif typography. Shared tokens are `--ink: #182538`, `--muted: #526176`, `--brand: #2454a6`, `--brand-dark: #173d79`, `--surface: #ffffff`, `--canvas: #f3f5f8`, `--line: #d9e0ea`, `--focus: #b45309`, `--danger: #a83232`, and `--good: #176b4a`, with a 14px card radius and low-contrast surface shadow. Keep controls at least 42px high, show a 3px visible focus ring, use a constrained 1280px content width, and horizontally scroll wide tables inside their own labeled container. At 375px, navigation wraps and detail fields become one column; at 1440px, the record list and details remain aligned without page-level overflow.

## Interaction Specification

| Control ID | Trigger | Kind | Target | Result / state change | Keyboard / dismissal |
|---|---|---|---|---|---|
| `filter-book` | Change book | local-action | `record-rows` | Filters categories to the selected book; an empty selection shows the empty state | Native select keyboard |
| `clear-filter` | Activate Clear | local-action | `price-book-filter` | Restores all books and refreshes the list | Enter or Space |
| `price-book-link`, `header-link` | Activate link | navigation | SCR-101 / SCR-103 | Moves one step up or down the setup hierarchy | Enter |
| `select-record-[id]` | Activate record ID | local-action | `record-form` | Loads that category into the detail panel | Enter or Space |
| `add-record` | Activate Add | local-action | `record-form` | Assigns max ID + 1 and version 0; parent book follows the selected filter | Enter or Space |
| `copy-record` | Activate Copy to Add | local-action | `record-form` | Copies the selection with a new ID and version 0 | Enter or Space |
| `edit-record` | Activate Edit | local-action | `record-form` | Enables editable fields; ID and Version stay read-only | Enter or Space |
| `remove-record` | Activate Remove | dialog-open | `remove-dialog` | Opens a confirmation for the selected category | Enter or Space |
| `cancel-remove` | Activate Cancel or press Escape | dialog-close | `remove-dialog` | Closes without deleting; focus returns to Remove | Enter, Space, or Escape; backdrop does not dismiss |
| `confirm-remove` | Confirm removal | local-action | `record-rows` | Removes the sample record and selects the next available row | Enter or Space |
| `tab-data`, `tab-effective`, `tab-current`, `tab-original` | Activate tab | local-action | Corresponding tab panel | Shows data or the corresponding audit metadata | Enter/Space; Left/Right/Home/End |
| `update-record` | Submit valid details | local-action | `record-form` | Creates at version 0 or increments the edited record version; announces success | Enter |
| `close-record` | Activate Close | local-action | `record-form` | Discards unsaved edits and restores the selected record | Enter or Space |

## Open Issues

None for this screen. Record edits are in-memory prototype behavior only.

## Prototype Verification

| Check | Expected | Observed | Status | Evidence |
|---|---|---|---|---|
| Browser, filters, responsive, navigation, and local actions | Opens from `file://`; filters and empty state work; fits 375px and 1440px; no external resources | Passed at 375x844 and 1440x900 with no page-level horizontal overflow. Price Book filtering, Clear, empty state, add, copy, edit, required-description validation, version updates, Close discard, remove confirmation, Cancel/Escape dismissal, focus restoration, tabs, and both navigation links worked. Browser run reported no runtime errors or external requests. | Pass | Browser interaction run on SCR-102/mockup.html, responsive screenshots, and interaction-flows.md verification log |

**Traces to**: UME-102, R-703, R-711, R-712, R-713, R-719, R-720, R-721, R-723
**Generated**: 2026-10-27T00:00:00Z
