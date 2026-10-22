# Migration Guide Addendum: Collaboration Mode for Existing Projects

**Project**: 05 - Building Skills Iteration 4
**Version**: 1.0
**Created**: 2026-10-22
**Audience**: Teams with projects created before the `collaboration_mode` feature shipped

---

## Overview

This addendum covers migrating **existing projects** to the `collaboration_mode` feature introduced in Iteration 4 (see [`collaboration-mode-reference.md`](collaboration-mode-reference.md) and [`solo-mode-guide.md`](solo-mode-guide.md)). It does not duplicate the general diagram-migration guidance above this section — that content covers a different, earlier migration (Project 1 → Project 3 diagram style) and remains valid and unrelated to this one.

---

## What Changed

Projects initialized before this feature shipped have a `project-metadata.json` with no `collaboration_mode` field at all. Projects initialized after it ships have the field set explicitly (`solo` by default, or `traditional` if chosen).

## The Safe Default Rule

**Absence of the field is read as `traditional`, never as `solo`.** This is deliberate and asymmetric from the new-project default:

- A **new** project defaults to `solo` because that's the common case this framework is built for.
- An **existing** project predates this feature and was built under the old implicit assumption that stakeholder approvals matter at every gate. Silently treating its missing field as `solo` would retroactively relax approval expectations nobody agreed to relax. That's not a safe migration — it's a silent behavior change.

So: if you do nothing, your existing project keeps behaving exactly as it always has. `stakeholder_confirmation` gate checks (where they exist) stay hard-blocking, and skill instructions default to their traditional-mode guidance.

## When You Should Explicitly Switch to Solo

If your existing project is actually being run by a single developer — which, realistically, describes most projects in this framework — you're currently paying the overhead of `traditional` mode's confirmation requirements for no benefit. Switch explicitly:

```
@workspace Use project-document-management's Change Collaboration Mode operation:

Project Number: [NN]
Target Mode: solo
Reason: Single-developer project; traditional-mode approval overhead doesn't reflect how this project is actually run
```

This:
1. Sets `collaboration_mode: "solo"` in `project-metadata.json`
2. Appends an `evolution_history` entry recording `from_mode: "traditional"` (or absent, read as traditional), `to_mode: "solo"`, your reason, and a timestamp
3. Updates the project's `main.md` mode line if present

## What a Mode Switch Does *Not* Do

- **It is not retroactive.** Any gate evaluations or confirmations already recorded under the old (implicit `traditional`) behavior remain valid as-is. You do not need to re-run completed skills.
- **It does not change folder structure, archetype, or any other metadata field.** This is a metadata-only change (patch version bump), scoped entirely to collaboration mode.
- **It does not retroactively invalidate anything** — only gate evaluations performed *after* the switch follow the new mode's rules.

## When to Stay on `traditional`

Keep (or explicitly set) `traditional` mode if your project genuinely has multiple real people in different roles — e.g., an actual Business Owner, a separate QA reviewer, a client who needs real sign-off. Solo mode's self-attestation mechanism assumes the developer can credibly represent every role; if that assumption doesn't hold for your project, `traditional` mode's formal confirmation requirements are doing real work, not just adding overhead.

## Migration Checklist

- [ ] Read `project-metadata.json` — confirm whether `collaboration_mode` is present
- [ ] Decide: is this genuinely a solo project, or does it have real separate stakeholders?
- [ ] If solo: run the Change Collaboration Mode operation with an explicit reason
- [ ] If traditional should remain the explicit choice (rather than just the implicit default): run the same operation with `Target Mode: traditional` so the setting is explicit and auditable rather than relying on field-absence
- [ ] Confirm the `evolution_history` entry was appended correctly
- [ ] Spot-check one in-progress skill to confirm gate behavior now matches the new mode (see [`solo-mode-validation-report.md`](../Testing/solo-mode-validation-report.md) for what passing behavior looks like)

## See Also

- [`collaboration-mode-reference.md`](collaboration-mode-reference.md) — Full definitions, defaults, and the Real External Stakeholder Flag
- [`solo-mode-guide.md`](solo-mode-guide.md) — How-to guide for running a project in solo mode day-to-day
- [`../Testing/solo-mode-validation-report.md`](../Testing/solo-mode-validation-report.md) — End-to-end validation confirming the gate and skill-instruction behavior described above
