# Layout Specification — Price Book Management *(LS-101)*

**Screen**: Price Book Management *(SCR-101)*
**UI Model Entry**: UME-101
*(Ref: R-706, R-707, R-708, R-709, R-710, R-719, R-720, R-721, R-723)*

## Changelog

- **v1.0** (2026-10-27): Initial generation

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
**Traces to**: UME-101, R-706, R-707, R-708, R-709, R-710, R-719, R-720, R-721, R-723
**Generated**: 2026-10-27T00:00:00Z
