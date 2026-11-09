# PRJ-07 Release Guide — Modeling with S5's Use-Case, UI, and Alignment Skills

**Project**: PRJ-07 — Building Skills Iteration 5
**Status**: Release — all 7 tasks complete
**Audience**: Developers using `usecase-generatemodel` (S32), `ui-generatemodel` (S40), and `model-validatealignment` (S39), and anyone resuming or auditing a project that uses them

## What Changed

S5 — Design & Visualization now includes three new skills alongside the existing `diagram-generatecollaboration`/`hierarchy-management`/`documentation-automation`/`migration-tools` and the six `screen-*` skills (formerly their own "S11" category, now folded into S5):

- **`usecase-generatemodel` (S32)** — generates a boundary-scoped use-case model and linked detailed scripts
- **`ui-generatemodel` (S40)** — generates a software boundary's UI Model from its use-case model, closing the previous manual-authoring gap
- **`model-validatealignment` (S39)** — validates cross-model (domain/process/use-case/UI) entity and boundary alignment at the end of every modeling round

All three skills share one contract: [`cross-model-alignment-contract.md`](../../../../.github/skills/model-validatealignment/references/cross-model-alignment-contract.md). Read that document for the authoritative schema; this guide explains **how to actually use these skills day-to-day**.

## Applicability — What Runs Where

| Boundary's `boundary_type` | `usecase-generatemodel` (S32) | `ui-generatemodel` (S40) | Six `screen-*` skills (S33–S38) |
|---|---|---|---|
| `software` | Runs | Runs — produces real `UIModelEntry`s if the use-case model has human-facing interactions, or an empty model + `generation_note` if not | Run, if `ui-generatemodel` produced any entries |
| `non-software` | Runs (full treatment, same rigor as software boundaries) | **Refuses** — writes an empty model with a `generation_note` citing non-software status | Never run (nothing to generate screens from) |
| `unknown` (undeclared) | **Refuses** — surfaces a clarification question | **Refuses** — same reason | Never run |

**The single most important rule**: `boundary_type` must be **explicitly declared** in a boundary's `main.md` (`hierarchy-management` writes it as `unknown` with a visible `[ACTION REQUIRED]` prompt when a boundary is first created — see its `SKILL.md`). Never infer it from folder name, participant stereotype, or the presence/absence of a screen. If you see a boundary still showing `unknown`, that's your cue to classify it before running S32/S40 against it.

## Direct Invocation (Outside a Full Orchestrated Workflow)

You don't need to run a full `orchestrate start` workflow to use these skills standalone:

1. Confirm the target boundary's `main.md` has a declared `boundary_type` (not `unknown`). If it's still `unknown`, classify it first — ask yourself: "does this boundary have its own software system with a UI, or is it a real-world/organizational boundary (a physical location, another company, a manual process)?"
2. Run `usecase-generatemodel` against that boundary's `domain-model.md`/`process.md`/`collaboration.md`. It produces `use-case-model.md`/`.json` and `use-case-scripts/`.
3. **Only if `boundary_type` is `software`**: run `ui-generatemodel` against the use-case model just produced. It produces `ui-model.md`/`.json`.
4. Run `model-validatealignment` to check the result (see Clarification and Round Revision below).
5. **Only if the UI model has entries**: proceed into the existing screen pipeline (`screen-generateinventory` → ... → `screen-discussfeedback`), completely unchanged from how it worked before PRJ-07.

Standalone invocation still produces an end-of-round validation obligation — per the contract, document that a round occurred even outside a full orchestrated workflow, so a later resume (orchestrated or not) can check for staleness.

## Handling Clarification

When `model-validatealignment` reports `NEEDS_CLARIFICATION`:

1. Read the `clarification_questions` array in the round's report — these are specific, referencing the actual conflicting items (e.g., "Is boundary X a software system with its own UI, or a non-software real-world boundary?"), never generic.
2. Answer the question — in solo mode, this is a self-attested, documented assumption (same build-and-clarify discipline as `requirements-sanitize`); in traditional mode, this may require a real stakeholder check-in if the ambiguity concerns something only they can resolve.
3. Update the affected model document(s) to reflect the answer (e.g., add the missing `boundary_type` declaration to `main.md`).
4. **Re-run `model-validatealignment`**. A round cannot skip directly from `NEEDS_CLARIFICATION` to `PASS` — there is no shortcut, and none of this validator's checks are the `stakeholder_confirmation` type that solo-mode self-attestation can soften (see the contract's Section 4.4 and T06's orchestrator integration for why this is structurally true, not just documented).

Never treat a `NEEDS_CLARIFICATION` or `INVALID_INPUT` round as if it were `PASS`. If you're unsure whether a prior round is still trustworthy, see Round Revision and Resume below.

## Round Revision and Resume

A **modeling round** is a bounded unit of work for one or more boundaries, ending in an Alignment Report. Key behaviors:

- **Fresh round**: first time a boundary's models are validated. Standard flow above.
- **Revised round**: you've edited a boundary's domain/process/use-case/UI model after a prior round's report was written. The prior round's status (even if it was `PASS`) is **stale** the moment any model within its `boundary_scope` changes — re-run `model-validatealignment` to get a current report. Don't assume last week's `PASS` still holds.
- **Resumed round** (across a session break, or via `orchestrate resume`): the orchestrator (or you, manually) compares each boundary's `modeling_rounds` entry's recorded `source_model_versions` against the actual current file versions. If they differ, that boundary's status is reported as `stale`, not silently trusted as the old `PASS`. This is exactly what `model-validatealignment/scripts/alignment_report.py`'s `resolve_round_for_resume()` function does — see [negative-examples/stale_report_demo.py](Testing/worked-example/negative-examples/stale_report_demo.py) for a concrete, executed example of this detection working correctly (and *not* over-firing when nothing actually changed).

## Legacy-Model Classification

If you're working in a project whose boundaries were decomposed **before** PRJ-07 (i.e., before `hierarchy-management`'s `main.md` stub gained its `## System Boundary` section), those boundaries have no `boundary_type` declared at all. Treat this exactly like an `unknown` declaration:

- `usecase-generatemodel`/`ui-generatemodel` will refuse to run until you add a `## System Boundary` section with an explicit `boundary_type` to that boundary's `main.md`.
- This is a one-time, per-boundary classification task — it does not require rewriting any other content in that boundary's existing `domain-model.md`/`process.md`/`collaboration.md`.
- There is **no bulk/automatic migration** for existing projects — per the Implementation Analysis's explicit scope boundary ("No new framework, external API, broad historical migration... is required"), classify boundaries as you actually need to model them, not all at once preemptively.

## Where to Look for Working Examples

- **Three-level worked example** (non-software root → software child → software grandchild), reused consistently across T01–T05: [`model-validatealignment/fixtures/three-level-valid/`](../../../../.github/skills/model-validatealignment/fixtures/three-level-valid/), [`usecase-generatemodel/examples/three-level-worked-example/`](../../../../.github/skills/usecase-generatemodel/examples/three-level-worked-example/), [`ui-generatemodel/examples/three-level-worked-example/`](../../../../.github/skills/ui-generatemodel/examples/three-level-worked-example/)
- **Full screen pipeline run** against a real generated UI model (T07, this release): [`Testing/worked-example/child-software-boundary/UI Prototype/`](Testing/worked-example/child-software-boundary/UI%20Prototype/)
- **Negative examples** (all six required failure/clarification categories): [`Testing/worked-example/negative-examples/`](Testing/worked-example/negative-examples/)
- **Requirement coverage**: [`Testing/requirement-coverage-matrix.md`](Testing/requirement-coverage-matrix.md)

## No Production Deployment Required

Per the Implementation Analysis's Release Acceptance: this release is complete as a skill-framework capability. No production application, external API, or broad historical project migration is in scope or required to consider PRJ-07 released.
