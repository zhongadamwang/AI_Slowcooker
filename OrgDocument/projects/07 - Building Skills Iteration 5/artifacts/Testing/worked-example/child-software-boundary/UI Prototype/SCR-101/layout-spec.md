# Layout Specification — Dispatch Queue *(LS-101)*

**Screen**: Dispatch Queue *(SCR-101)*
**UI Model Entry**: UME-001
*(Ref: UC-001)*

## Changelog
- **v1.0** (2026-11-08): Initial generation

## Purpose

Lets a Field Operations Coordinator see unscheduled ServiceRequests alongside available Technicians, and assign a Technician + time slot to a request — the list+detail pattern used throughout this worked example's screens.

## Layout

### HTML

```html
<div class="screen screen--dispatch-queue">
  <header class="screen__header"><h1>Dispatch Queue</h1></header>
  <section class="screen__list-section">
    <table class="record-list">
      <thead><tr><th>Request</th><th>Status</th><th>Assigned Technician</th></tr></thead>
      <tbody>
        <tr class="record-list__row record-list__row--selected">
          <td>Equipment Rental — 2378</td><td>Unscheduled</td><td>—</td>
        </tr>
      </tbody>
    </table>
  </section>
  <section class="screen__detail-section">
    <dl class="detail-form">
      <dt>Technician</dt>
      <dd>
        <select id="technician-select">
          <option selected>(choose a technician)</option>
          <option>J. Alvarez — available</option>
        </select>
      </dd>
      <dt>Time Slot</dt>
      <dd><input type="text" id="time-slot-input" placeholder="e.g. Tomorrow 9am-12pm"></dd>
    </dl>
  </section>
  <footer class="screen__footer">
    <button class="btn btn--primary" id="assign-btn" data-action="assign">Assign</button>
    <a class="btn" id="to-job-status-link" href="../SCR-102/mockup.html" data-transition-target="SCR-102">Open Job Status Update →</a>
  </footer>
</div>
```

### CSS

```css
.screen--dispatch-queue { font-family: system-ui, sans-serif; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.record-list { width: 100%; border-collapse: collapse; }
.record-list th, .record-list td { text-align: left; padding: 0.4rem 0.6rem; border-bottom: 1px solid #eee; }
.record-list__row--selected { background: #eff6ff; }
.detail-form { display: grid; grid-template-columns: 160px 1fr; gap: 0.5rem 1rem; padding: 1rem 0; }
.btn { padding: 0.4rem 0.9rem; border: 1px solid #ccc; background: #f8f8f8; border-radius: 4px; cursor: pointer; font-size: 0.85rem; text-decoration: none; color: #333; display: inline-block; }
.btn--primary { background: #2563eb; color: white; border-color: #2563eb; }
.screen__footer { display: flex; gap: 0.5rem; padding-top: 0.75rem; border-top: 1px solid #eee; }
```

## Interaction Specification

- `#technician-select` + `#time-slot-input` must both have values before `#assign-btn` is enabled (validated in mockup JS)
- `#assign-btn` click → shows a confirmation message inline (no page change, no dialog — this is the screen's own "save" outcome)
- `#to-job-status-link` → real page navigation to SCR-102

---
**Traces to**: UME-001, UC-001
**Generated**: 2026-11-08
