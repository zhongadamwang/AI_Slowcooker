# Three-Level Worked Example — ui-generatemodel

This example demonstrates `ui-generatemodel` producing boundary-scoped UI Models at the same three nested hierarchy levels used by T01's `model-validatealignment` fixtures and T02's `usecase-generatemodel` worked example (`BND-ROOT` non-software, `BND-CHILD-SW` software, `BND-GRANDCHILD` software), consuming T02's actual generated use-case models as real input rather than a hypothetical one.

## What This Demonstrates

1. **Non-software boundaries get zero entries, explicitly explained** — `root-boundary/ui-model.json` has `"entries": []` plus a `generation_note` citing BND-ROOT's non-software status. This is Step 0.2's refusal in action: the file exists (never silently omitted) but is deliberately empty, distinguishable from an incomplete run.
2. **Software boundaries get use-case-evidenced aggregation, not ad hoc screens** — `child-software-boundary/ui-model.json`'s two entries (`Dispatch Queue`, `Job Status Update`) are each traced via `source_use_case_refs` back to the exact use case (`UC-001`/`UC-002`) from T02's own `use-case-model.json` for this same boundary — not invented independently.
3. **A software boundary can still legitimately warrant very little UI** — `grandchild-boundary/ui-model.json` has exactly one small entry, with its `generation_note` explicitly reasoning through *why* this boundary gets an entry (a direct human actor) while the `software-boundary-no-ui-required` fixture's boundary (an internal-role/scheduled-trigger actor) correctly gets none. The distinguishing factor is called out, not left for a reader to infer.
4. **Existing D-02 schema fields are completely unchanged** — every entry still has exactly `entry_id`, `ui_concept_name`, `domain_entity_refs`, `aggregation_description`. The new `boundary_ref`/`source_use_case_refs`/`generation_note` fields are strictly additive; a consumer reading only the original four fields sees exactly what it would have seen from a manually-authored `ui-model.json`.
5. **`domain_entity_refs` are drawn from real domain-model.md content** — e.g., `E-002`/`E-003` in the child-software-boundary model are the actual entity IDs defined in that boundary's `domain-model.md` (T01's fixture), not invented IDs.

## Folder Layout

```
root-boundary/
├── ui-model.md / .json                 ← BND-ROOT, non-software, 0 entries + generation_note
└── child-software-boundary/
    ├── ui-model.md / .json              ← BND-CHILD-SW, software, 2 entries
    └── grandchild-boundary/
        └── ui-model.md / .json          ← BND-GRANDCHILD, software, 1 entry + generation_note explaining why
```

Note: this example folder does not duplicate the `domain-model.md`/`main.md`/`collaboration.md` files from T01's fixtures, nor the `use-case-model.json`/scripts from T02's worked example — both already exist at `../../model-validatealignment/fixtures/three-level-valid/` and `../../usecase-generatemodel/examples/three-level-worked-example/` respectively, and this folder's `source_domain_model`/implicit use-case inputs reference them by relative path rather than copying their content. This folder is scoped to exactly this skill's own output.
