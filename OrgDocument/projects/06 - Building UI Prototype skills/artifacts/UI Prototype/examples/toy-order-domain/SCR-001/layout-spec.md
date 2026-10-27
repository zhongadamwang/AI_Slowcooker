# Layout Specification — Order Summary *(LS-001)*

**Screen**: Order Summary *(SCR-001)*
**UI Model Entry**: UME-001
*(Ref: R-614)*

## Changelog

- **v1.0** (2026-10-27): Initial generation

## Purpose

Lets a customer or support agent review a single order's full detail — the placing customer, order metadata, and every line item — in one coherent view, rather than needing to cross-reference separate Customer/Order/LineItem records.

## Design Rationale

Used a two-column layout: a narrower left column for order/customer metadata (static, glanceable) and a wider right column for the line-items table (the part most likely to need scrolling for orders with many items). This split was chosen because the UI Model entry (UME-001) aggregates three distinct domain entities (Order, Customer, LineItem) that read better separated into "about this order" vs. "what's in this order" rather than stacked into one long vertical list.

## Layout

### HTML

```html
<div class="screen screen--order-summary">
  <header class="screen__header">
    <h1>Order #10234</h1>
    <nav class="screen__nav">
      <a href="../SCR-002/mockup.html" class="screen__nav-link" data-transition-target="SCR-002">View Customer Order History</a>
    </nav>
  </header>
  <section class="screen__content">
    <aside class="order-meta">
      <h2>Order Details</h2>
      <dl>
        <dt>Order Date</dt>
        <dd>2026-10-15</dd>
        <dt>Status</dt>
        <dd><span class="status-badge status-badge--shipped">Shipped</span></dd>
      </dl>
      <h2>Customer</h2>
      <dl>
        <dt>Name</dt>
        <dd>Jordan Ellis</dd>
        <dt>Email</dt>
        <dd>jordan.ellis@example.com</dd>
      </dl>
    </aside>
    <div class="line-items">
      <h2>Line Items</h2>
      <table class="line-items__table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Quantity</th>
            <th>Unit Price</th>
            <th>Subtotal</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Wireless Mouse</td>
            <td>2</td>
            <td>$24.99</td>
            <td>$49.98</td>
          </tr>
          <tr>
            <td>USB-C Hub</td>
            <td>1</td>
            <td>$39.99</td>
            <td>$39.99</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</div>
```

### CSS

```css
.screen--order-summary {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 1.5rem;
  padding: 1.5rem;
  font-family: system-ui, sans-serif;
}
.screen__header {
  grid-column: 1 / -1;
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.75rem;
}
.screen__nav-link {
  color: #2563eb;
  text-decoration: none;
  font-size: 0.9rem;
}
.order-meta dl {
  margin: 0 0 1rem;
}
.order-meta dt {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.5rem;
}
.order-meta dd {
  margin: 0;
  font-weight: 500;
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
.line-items__table {
  width: 100%;
  border-collapse: collapse;
}
.line-items__table th,
.line-items__table td {
  text-align: left;
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}
```

---
**Traces to**: UME-001, R-614
**Generated**: 2026-10-27T00:00:00Z
