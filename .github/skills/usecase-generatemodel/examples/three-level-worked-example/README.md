# Three-Level Worked Example — usecase-generatemodel

This example demonstrates `usecase-generatemodel` producing independent, boundary-scoped use-case models at three nested hierarchy levels, reusing the same fixture boundaries T01's `model-validatealignment` contract already established (`BND-ROOT` non-software, `BND-CHILD-SW` software, `BND-GRANDCHILD` software) for consistency across PRJ-07's deliverables.

## What This Demonstrates

1. **Non-software boundaries get full use-case treatment** — `root-boundary/`'s two use cases (Request Field Service, Accept Service Request) are fully developed with scripts, exactly as rigorous as the software boundaries' use cases. Neither script has a UI References section, correctly omitted (not a placeholder) since no software exists at this boundary.
2. **Actors are relative to a boundary, never shared across levels** — "Field Operations Coordinator" exists as `A-002` at the root boundary and as a *separate* `A-001` at the child software boundary; "Technician" exists as `A-002` at the child boundary and as a *separate* `A-001` at the grandchild boundary. Each is independently defined, per contract Section 1.3 — this is called out explicitly in each boundary's `use-case-model.md`, not left implicit.
3. **Use-case IDs are scoped per boundary, not globally unique** — all three boundaries independently use `UC-001`, `UC-002`... starting from 1, exactly mirroring `UME-[###]`'s existing per-model scoping convention. This is intentional, not a collision.
4. **UI References appear only where applicable, and only illustratively here** — the child software boundary's `UC-001-schedule-technician.md` script includes a UI References section, but it is explicitly marked as **illustrative-only** in this worked example (showing what it *would* look like once `ui-generatemodel`/`screen-generateinventory` have actually run) — a true first-pass output from this skill alone, with no UI model yet existing, would correctly omit that section entirely.
5. **Cross-boundary handoffs are documented in prose, not as structured cross-boundary references** — UC-002's (root boundary) Main Flow step 3 describes handing off to the child boundary's dispatch system, but does not reach into or reference the child boundary's own `use-case-model.json` — each boundary's model remains self-contained per the contract's single-ownership rule (Section 1.4).

## Folder Layout

```
root-boundary/
├── use-case-model.md / .json          ← BND-ROOT, non-software, 2 use cases
├── use-case-scripts/
│   ├── main.md
│   ├── UC-001-request-field-service.md
│   └── UC-002-accept-service-request.md
└── child-software-boundary/
    ├── use-case-model.md / .json       ← BND-CHILD-SW, software, 2 use cases
    ├── use-case-scripts/
    │   ├── main.md
    │   ├── UC-001-schedule-technician.md
    │   └── UC-002-update-job-status.md
    └── grandchild-boundary/
        ├── use-case-model.md / .json   ← BND-GRANDCHILD, software, 1 use case
        └── use-case-scripts/
            ├── main.md
            └── UC-001-log-time-entry.md
```

Note: this example folder does not include the `domain-model.md`/`main.md`/`collaboration.md` files that would normally sit alongside these use-case models in a real project — those already exist as T01's fixtures under `../../model-validatealignment/fixtures/three-level-valid/`, and are not duplicated here. This folder is scoped to exactly this skill's own output.
