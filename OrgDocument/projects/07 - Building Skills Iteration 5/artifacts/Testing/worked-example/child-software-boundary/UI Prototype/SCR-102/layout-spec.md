# Layout Specification — Job Status Update *(LS-102)*

**Screen**: Job Status Update *(SCR-102)*
**UI Model Entry**: UME-002
*(Ref: UC-002)*

## Changelog
- **v1.0** (2026-11-08): Initial generation

## Purpose

Lets a Technician update a single ServiceRequest's status as field work progresses, with a confirmation dialog before committing the change — demonstrating real local-dialog interaction (open, cancel, validate, save) for T07's browser-verification requirement.

## Layout

### HTML

```html
<div class="screen screen--job-status">
  <header class="screen__header"><h1>Job Status Update</h1></header>
  <a class="btn" id="to-dispatch-link" href="../SCR-101/mockup.html" data-transition-target="SCR-101">← Back to Dispatch Queue</a>
  <section class="screen__detail-section">
    <dl class="detail-form">
      <dt>Request</dt><dd>Equipment Rental — 2378</dd>
      <dt>Current Status</dt><dd id="current-status">En Route</dd>
      <dt>New Status</dt>
      <dd>
        <select id="new-status-select">
          <option value="">(choose a status)</option>
          <option value="on-site">On-Site</option>
          <option value="in-progress">In Progress</option>
          <option value="complete">Complete</option>
        </select>
      </dd>
    </dl>
    <button class="btn btn--primary" id="update-status-btn" data-action="open-confirm-dialog">Update Status</button>
  </section>

  <div class="dialog-overlay" id="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="confirm-dialog-title" hidden>
    <div class="dialog">
      <h2 id="confirm-dialog-title">Confirm Status Change</h2>
      <p id="confirm-dialog-message">Change status to <strong id="confirm-dialog-value"></strong>?</p>
      <div class="dialog__actions">
        <button class="btn" id="confirm-cancel-btn" data-action="cancel">Cancel</button>
        <button class="btn btn--primary" id="confirm-save-btn" data-action="save">Confirm</button>
      </div>
    </div>
  </div>
</div>
```

### CSS

```css
.screen--job-status { font-family: system-ui, sans-serif; padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; max-width: 480px; }
.detail-form { display: grid; grid-template-columns: 140px 1fr; gap: 0.5rem 1rem; padding: 1rem 0; }
.btn { padding: 0.4rem 0.9rem; border: 1px solid #ccc; background: #f8f8f8; border-radius: 4px; cursor: pointer; font-size: 0.85rem; text-decoration: none; color: #333; display: inline-block; align-self: flex-start; }
.btn--primary { background: #2563eb; color: white; border-color: #2563eb; }
.dialog-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; }
.dialog-overlay[hidden] { display: none; }
.dialog { background: white; border-radius: 8px; padding: 1.5rem; min-width: 300px; }
.dialog__actions { display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem; }
```

## Interaction Specification

- `#update-status-btn` is disabled until `#new-status-select` has a non-empty value (validation)
- `#update-status-btn` click → opens `#confirm-dialog` (local state, not navigation), populating `#confirm-dialog-value` with the chosen status label
- `#confirm-cancel-btn` click → closes the dialog, no change applied, focus returns to `#update-status-btn`
- `#confirm-save-btn` click → applies the change (`#current-status` text updates to the new value), closes the dialog
- `#to-dispatch-link` → real page navigation to SCR-101

## Open Issues

None — this is a minimal worked example, not a production screen; further fields (e.g., notes, photo attachment) are plausible future additions but out of scope for T07's demonstration purpose.

---
**Traces to**: UME-002, UC-002
**Generated**: 2026-11-08
