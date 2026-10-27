# Layout Specification — Price Header Management *(LS-103)*

**Screen**: Price Header Management *(SCR-103)*
**UI Model Entry**: UME-103
*(Ref: R-704, R-714, R-715, R-716, R-719, R-720, R-721, R-722, R-723)*

## Changelog

- **v1.0** (2026-10-27): Initial generation

## Purpose

Lets a user, after selecting a Price Book and Price Category, view, create, copy, edit, and delete hierarchical Price Headers — each organized into a parent/child grouping structure with an explicit depth level.

## Design Rationale

Two cascading filter dropdowns (Price Book, then Category) are shown together above the list, directly reflecting R-714's two-level dependency (unlike SCR-102's single Price Book filter). The list's "Level" and "Parent Header ID" columns are shown explicitly rather than rendered as an indented tree, since the source requirement only specifies these as flat columns in a table (R-715/R-704) — a nested tree-view is a plausible future visual enhancement but not what this requirement actually describes, so the literal flat-column structure is what's generated here.

## Layout

### HTML

```html
<div class="screen screen--price-header">
  <header class="screen__header">
    <h1>Price Header Management</h1>
  </header>
  <section class="screen__filter">
    <label for="price-book-filter">Price Book</label>
    <select id="price-book-filter">
      <option selected>1001 — Standard Service Pricing</option>
      <option>1002 — Promotional Pricing Q4</option>
    </select>
    <label for="category-filter">Category</label>
    <select id="category-filter">
      <option selected>2001 — Coiled Tubing Services</option>
      <option>2002 — Primary Cementing Services</option>
    </select>
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
          <th>Category ID</th>
          <th>Parent Header ID</th>
          <th>Level</th>
        </tr>
      </thead>
      <tbody>
        <tr class="record-list__row record-list__row--selected">
          <td>3001</td>
          <td>0</td>
          <td>Equipment Rental</td>
          <td>1001</td>
          <td>2001</td>
          <td>—</td>
          <td>0</td>
        </tr>
        <tr class="record-list__row">
          <td>3002</td>
          <td>0</td>
          <td>Equipment Rental — Small Diameter</td>
          <td>1001</td>
          <td>2001</td>
          <td>3001</td>
          <td>1</td>
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
        <dt>ID</dt><dd><input type="text" value="3001" readonly class="field--readonly"></dd>
        <dt>Price Book</dt><dd><input type="text" value="1001 — Standard Service Pricing" readonly class="field--readonly"></dd>
        <dt>Category</dt><dd><input type="text" value="2001 — Coiled Tubing Services" readonly class="field--readonly"></dd>
        <dt>Description</dt><dd><input type="text" value="Equipment Rental"></dd>
        <dt>Parent Price Header</dt>
        <dd>
          <select>
            <option selected>(none — top level)</option>
            <option>3001 — Equipment Rental</option>
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
.screen--price-header {
  font-family: system-ui, sans-serif;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.screen__filter {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
**Traces to**: UME-103, R-704, R-714, R-715, R-716, R-719, R-720, R-721, R-722, R-723
**Generated**: 2026-10-27T00:00:00Z
