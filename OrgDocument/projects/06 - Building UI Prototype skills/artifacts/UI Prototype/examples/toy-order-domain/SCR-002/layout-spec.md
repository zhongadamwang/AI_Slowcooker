# Layout Specification — Customer Order History *(LS-002)*

**Screen**: Customer Order History *(SCR-002)*
**UI Model Entry**: UME-003
*(Ref: R-614)*

## Changelog

- **v1.0** (2026-10-27): Initial generation

## Purpose

Lets a customer or support agent review the list of all orders placed by a given customer, at a summary level (date, status, no line-item detail), and navigate into any one of them for full detail.

## Design Rationale

Used a simple list/table layout rather than cards, since the content is primarily tabular (date, status) and a support agent scanning many orders benefits more from a dense table than visually spaced cards. Each row links directly to that order's detail screen — chosen deliberately as real `<a href>` navigation (not a JS click handler) specifically because it's simpler for `screen-generateflow` to detect and verify later, per `screen-generatemockup`'s own stated preference.

## Layout

### HTML

```html
<div class="screen screen--customer-order-history">
  <header class="screen__header">
    <h1>Order History — Jordan Ellis</h1>
    <nav class="screen__nav">
      <a href="../SCR-001/mockup.html" class="screen__nav-link" data-transition-target="SCR-001">Back to Order Summary</a>
    </nav>
  </header>
  <section class="screen__content">
    <table class="order-history__table">
      <thead>
        <tr>
          <th>Order</th>
          <th>Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><a href="../SCR-001/mockup.html" class="order-link" data-transition-target="SCR-001">Order #10234</a></td>
          <td>2026-10-15</td>
          <td><span class="status-badge status-badge--shipped">Shipped</span></td>
        </tr>
        <tr>
          <td><a href="../SCR-001/mockup.html" class="order-link" data-transition-target="SCR-001">Order #10198</a></td>
          <td>2026-09-02</td>
          <td><span class="status-badge status-badge--delivered">Delivered</span></td>
        </tr>
      </tbody>
    </table>
  </section>
</div>
```

### CSS

```css
.screen--customer-order-history {
  font-family: system-ui, sans-serif;
  padding: 1.5rem;
}
.screen__header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
}
.screen__nav-link {
  color: #2563eb;
  text-decoration: none;
  font-size: 0.9rem;
}
.order-history__table {
  width: 100%;
  border-collapse: collapse;
}
.order-history__table th,
.order-history__table td {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}
.order-link {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
}
.order-link:hover {
  text-decoration: underline;
}
.status-badge {
  display: inline-block;
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  font-size: 0.8rem;
}
.status-badge--shipped {
  background: #dcfce7;
  color: #166534;
}
.status-badge--delivered {
  background: #dbeafe;
  color: #1e40af;
}
```

---
**Traces to**: UME-003, R-614
**Generated**: 2026-10-27T00:00:00Z
