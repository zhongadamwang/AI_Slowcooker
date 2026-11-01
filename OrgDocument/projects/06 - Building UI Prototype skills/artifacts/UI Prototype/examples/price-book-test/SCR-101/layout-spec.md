# Layout Specification — Price Book Management *(LS-101)*

**Screen**: Price Book Management *(SCR-101)*
**UI Model Entry**: UME-101
*(Ref: R-706, R-707, R-708, R-709, R-710, R-719, R-720, R-721, R-723)*

## Changelog

- **v1.0** (2026-10-27): Initial generation
- **v1.1** (2026-11-01): Recreated as a responsive, interactive prototype; added version metadata, control behavior, and verification criteria.
- **v1.2** (2026-11-01): Recorded browser interaction and responsive verification after prototype recreation.

## Purpose

Lets a user view, create, copy, edit, and delete Price Book records — the top-level price configuration entity — including version history metadata, following the common list+tabbed-detail pattern shared across all four price-configuration screens.

## Design Rationale

Used the shared "list on top, tabbed detail below" layout described identically across all four source screens (Price Book, Category, Header, Item) in the original requirements — reusing one consistent structural pattern across all four screens, rather than inventing a different layout per screen, directly honors the source document's own repeated description of this exact structure for every entity.

## Layout

### HTML

```html
<div class="screen screen--price-book">
  <header class="screen__header">
    <h1>Price Book Management</h1>
  </header>
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
          <th>Version Number</th>
          <th>Company</th>
        </tr>
      </thead>
      <tbody>
        <tr class="record-list__row record-list__row--selected">
          <td>1001</td>
          <td>2</td>
          <td>Standard Service Pricing</td>
          <td>2</td>
          <td>Sanjel</td>
        </tr>
        <tr class="record-list__row">
          <td>1002</td>
          <td>0</td>
          <td>Promotional Pricing Q4</td>
          <td>0</td>
          <td>Sanjel</td>
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
        <dt>ID</dt><dd><input type="text" value="1001" readonly class="field--readonly"></dd>
        <dt>Description</dt><dd><input type="text" value="Standard Service Pricing"></dd>
        <dt>Version Number</dt><dd><input type="text" value="2" readonly class="field--readonly"></dd>
        <dt>Business Unit</dt><dd><input type="text" value="North America Services"></dd>
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
.screen--price-book {
  font-family: system-ui, sans-serif;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.list-toolbar {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
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
.record-list {
  width: 100%;
  border-collapse: collapse;
}
.record-list th, .record-list td {
  text-align: left;
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid #eee;
}
.record-list__row--selected { background: #eff6ff; }
.detail-tabs {
  display: flex;
  gap: 0.25rem;
  border-bottom: 1px solid #ddd;
}
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
.detail-form dt { font-size: 0.8rem; color: #666; align-self: center; }
.field--readonly { background: #f3f4f6; color: #666; }
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
| `category-link` | Activate link | navigation | SCR-102 | Opens categories for this book | Enter |
| `select-record-[id]` | Activate record ID | local-action | `record-form` | Loads that record into the detail panel | Enter or Space |
| `add-record` | Activate Add | local-action | `record-form` | Assigns max ID + 1 and version 0; enables required fields | Enter or Space |
| `copy-record` | Activate Copy to Add | local-action | `record-form` | Copies the selection with a new ID and version 0 | Enter or Space |
| `edit-record` | Activate Edit | local-action | `record-form` | Enables editable fields; ID and Version stay read-only | Enter or Space |
| `remove-record` | Activate Remove | dialog-open | `remove-dialog` | Opens a confirmation for the selected book | Enter or Space |
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
| Browser, responsive, navigation, and local actions | Opens from `file://`; fits 375px and 1440px; links and controls work without external resources | Passed at 375x844 and 1440x900 with no page-level horizontal overflow. Add, copy, edit, required-description validation, version updates, Close discard, remove confirmation, Cancel/Escape dismissal, focus restoration, tabs, and navigation to SCR-102 worked. Browser run reported no runtime errors or external requests. | Pass | Browser interaction run on SCR-101/mockup.html, responsive screenshots, and interaction-flows.md verification log |

**Traces to**: UME-101, R-706, R-707, R-708, R-709, R-710, R-719, R-720, R-721, R-723
**Generated**: 2026-10-27T00:00:00Z
