# Layout Specification — Price Item Management *(LS-104)*

**Screen**: Price Item Management *(SCR-104)*
**UI Model Entry**: UME-104
*(Ref: R-705, R-717, R-718, R-719, R-720, R-721, R-722, R-723, R-724)*

## Changelog

- **v1.0** (2026-10-27): Initial generation
- **v1.1** (2026-11-01): Recreated as a responsive, interactive prototype; added version metadata, control behavior, and verification criteria.
- **v1.2** (2026-11-01): Recorded browser interaction and responsive verification after prototype recreation.

## Purpose

Lets a user, after selecting a Price Book, Price Category, and Price Header (plus an optional Price Area filter), view, create, copy, edit, and delete the actual Price Item records — the leaf-level price data containing Price 1/Price 2 values and several business-flag attributes.

## Design Rationale

Three cascading filters plus one free-form filter (Price Area) are shown together, reflecting R-717's deepest cascading-dependency chain in the whole system (Book → Category → Header, plus Price Area as a non-hierarchical refinement). The Data tab is visibly the longest of all four screens' detail forms, which directly reflects Price Item being the most attribute-rich entity in the domain model (R-724) — rather than compress this into a shortened placeholder list, every field named in the source requirement is represented, including the two still-ambiguous flag fields, which are rendered with a visible `[REVIEW NEEDED]` label rather than a guessed name, consistent with `domain-concepts.md`'s own decision not to guess at them.

## Layout

### HTML

```html
<div class="screen screen--price-item">
  <header class="screen__header">
    <h1>Price Item Management</h1>
  </header>
  <section class="screen__filter">
    <label for="price-book-filter">Price Book</label>
    <select id="price-book-filter">
      <option selected>1001 — Standard Service Pricing</option>
    </select>
    <label for="category-filter">Category</label>
    <select id="category-filter">
      <option selected>2001 — Coiled Tubing Services</option>
    </select>
    <label for="header-filter">Price Header</label>
    <select id="header-filter">
      <option selected>3001 — Equipment Rental</option>
    </select>
    <label for="price-area-filter">Price Area</label>
    <input type="text" id="price-area-filter" placeholder="Filter by price area…">
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
          <th>Item Number</th>
          <th>Description</th>
          <th>Price 1</th>
          <th>Price 2</th>
          <th>Unit of Measure</th>
          <th>Book ID</th>
          <th>Category ID</th>
          <th>Header ID</th>
          <th>Price Area</th>
        </tr>
      </thead>
      <tbody>
        <tr class="record-list__row record-list__row--selected">
          <td>4001</td>
          <td>0</td>
          <td>CT-REEL-2378</td>
          <td>2-3/8" Coiled Tubing Reel, Daily Rate</td>
          <td>$1,250.00</td>
          <td>$1,100.00</td>
          <td>Day</td>
          <td>1001</td>
          <td>2001</td>
          <td>3001</td>
          <td>West Texas</td>
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
        <dt>ID</dt><dd><input type="text" value="4001" readonly class="field--readonly"></dd>
        <dt>Price Book</dt><dd><input type="text" value="1001 — Standard Service Pricing" readonly class="field--readonly"></dd>
        <dt>Category</dt><dd><input type="text" value="2001 — Coiled Tubing Services" readonly class="field--readonly"></dd>
        <dt>Price Header</dt><dd><input type="text" value="3001 — Equipment Rental" readonly class="field--readonly"></dd>
        <dt>Item Number</dt><dd><input type="text" value="CT-REEL-2378"></dd>
        <dt>Description</dt><dd><input type="text" value='2-3/8" Coiled Tubing Reel, Daily Rate'></dd>
        <dt>Account</dt><dd><input type="text" value="4000-EQUIP-RENTAL"></dd>
        <dt>Bundle Category</dt><dd><input type="text" value="Equipment"></dd>
        <dt>Price 1</dt><dd><input type="text" value="1250.00"></dd>
        <dt>Price 2</dt><dd><input type="text" value="1100.00"></dd>
        <dt>Unit of Measure</dt><dd><input type="text" value="Day"></dd>
        <dt>Price Area</dt><dd><input type="text" value="West Texas"></dd>
        <dt>Customer</dt><dd><input type="text" value="(blank — applies to all customers)"></dd>
        <dt>Is Discountable</dt><dd><input type="checkbox" checked></dd>
        <dt>Is Discontinued</dt><dd><input type="checkbox"></dd>
        <dt>Is Product</dt><dd><input type="checkbox"></dd>
        <dt>Is Internal</dt><dd><input type="checkbox"></dd>
        <dt class="field--review-needed">[REVIEW NEEDED] Field A <span class="review-badge">?</span></dt><dd><input type="checkbox" disabled></dd>
        <dt class="field--review-needed">[REVIEW NEEDED] Field B <span class="review-badge">?</span></dt><dd><input type="checkbox" disabled></dd>
        <dt>Service Line</dt>
        <dd>
          <select multiple class="multi-select" size="3">
            <option selected>Coiled Tubing</option>
            <option>CBM Coil Tubing</option>
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
.screen--price-item {
  font-family: system-ui, sans-serif;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.screen__filter {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #eee;
}
.screen__filter label { font-size: 0.85rem; color: #555; }
.screen__filter select, .screen__filter input {
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
.record-list { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.record-list th, .record-list td {
  text-align: left;
  padding: 0.4rem 0.6rem;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
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
  grid-template-columns: 180px 1fr;
  gap: 0.5rem 1rem;
  padding: 1rem 0;
  max-height: 420px;
  overflow-y: auto;
}
.detail-form dt { font-size: 0.8rem; color: #666; align-self: center; }
.field--readonly { background: #f3f4f6; color: #666; }
.field--review-needed { color: #b45309; }
.review-badge {
  display: inline-block;
  background: #fef3c7;
  color: #b45309;
  border-radius: 999px;
  padding: 0 0.4rem;
  font-size: 0.75rem;
  margin-left: 0.25rem;
}
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
| `filter-book`, `filter-category`, `filter-header` | Change ancestor selection | local-action | `record-rows` | Restricts records to the selected book/category/header combination | Native select keyboard |
| `filter-area` | Enter or clear a search term | local-action | `record-rows` | Case-insensitive substring filters by Price Area and exposes the empty state | Type, Enter, or clear |
| `header-link` | Activate link | navigation | SCR-103 | Returns to the selected header level | Enter |
| `select-record-[id]` | Activate record ID | local-action | `record-form` | Loads that item into the detail panel | Enter or Space |
| `add-record` | Activate Add | local-action | `record-form` | Assigns max ID + 1 and version 0; ancestor values follow the current filters | Enter or Space |
| `copy-record` | Activate Copy to Add | local-action | `record-form` | Copies the selection with a new ID and version 0 | Enter or Space |
| `edit-record` | Activate Edit | local-action | `record-form` | Enables editable fields; ID, Version, and ancestor references stay read-only | Enter or Space |
| `remove-record` | Activate Remove | dialog-open | `remove-dialog` | Opens a confirmation for the selected item | Enter or Space |
| `cancel-remove` | Activate Cancel or press Escape | dialog-close | `remove-dialog` | Closes without deleting; focus returns to Remove | Enter, Space, or Escape; backdrop does not dismiss |
| `confirm-remove` | Confirm removal | local-action | `record-rows` | Removes the sample record and exposes the empty state if needed | Enter or Space |
| `tab-data`, `tab-effective`, `tab-current`, `tab-original` | Activate tab | local-action | Corresponding tab panel | Shows data or the corresponding audit metadata | Enter/Space; Left/Right/Home/End |
| `update-record` | Submit valid details | local-action | `record-form` | Creates at version 0 or increments the edited record version; announces success | Enter |
| `close-record` | Activate Close | local-action | `record-form` | Discards unsaved edits and restores the selected record | Enter or Space |

## Open Issues

The two source flag names remain unresolved. They are visibly marked `[REVIEW NEEDED]` and disabled; no names or behavior are inferred. Record edits are in-memory prototype behavior only.

## Prototype Verification

| Check | Expected | Observed | Status | Evidence |
|---|---|---|---|---|
| Browser, filters, responsive, navigation, and local actions | Opens from `file://`; cascading and Price Area filters work; review fields stay disabled; fits 375px and 1440px; no external resources | Passed at 375x844 and 1440x900 with no page-level horizontal overflow. Book/category/header cascading, Price Area substring search and empty results, disabled review-needed fields, add, copy, edit, required-description validation, version updates, Close discard, remove confirmation, Cancel/Escape dismissal, focus restoration, tabs, and navigation worked. Browser run reported no runtime errors or external requests. | Pass | Browser interaction run on SCR-104/mockup.html, responsive screenshots, and interaction-flows.md verification log |

**Traces to**: UME-104, R-705, R-717, R-718, R-719, R-720, R-721, R-722, R-723, R-724
**Generated**: 2026-10-27T00:00:00Z
