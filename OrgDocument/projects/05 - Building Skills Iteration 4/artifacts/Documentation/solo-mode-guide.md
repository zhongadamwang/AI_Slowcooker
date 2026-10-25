# Solo Mode Guide

**Project**: 05 - Building Skills Iteration 4
**Version**: 1.0
**Created**: 2026-10-22
**Audience**: A developer starting or running an AI-aided EDPS project alone

---

## Overview

This guide walks through starting and running a project in **solo collaboration mode** — the default mode for new projects in this framework. For the full conceptual definitions of `solo` vs. `traditional` mode, see [`collaboration-mode-reference.md`](collaboration-mode-reference.md). This guide is the how-to companion to that reference.

If you are picking up an **existing** project created before this feature shipped, see [Migrating an Existing Project](#migrating-an-existing-project) in `migration-guide.md` instead — existing projects default to `traditional`, not `solo`.

---

## Why Solo Mode Exists

You're a single developer using EDPS skills to build something. There's no separate Business Owner, QA lead, or Compliance Officer sitting next to you waiting to sign off on each step. Traditional EDPS behavior — which assumes those people exist and must confirm each step — would just block you on approvals nobody is there to give.

Solo mode replaces that with a **build-and-clarify loop**: you produce the artifact, review it from the relevant role's perspective yourself, log that self-review, and move on. The framework still reasons about roles (Business Owner, End User, QA, etc.) exactly as before — only *who confirms* and *how blocking that confirmation is* changes.

---

## Step 1 — Initialize Your Project in Solo Mode

Solo is the default for new projects, so you usually don't need to do anything special:

```
@workspace Use the project-document-management skill to initialize a new project:

Project Name: My New Project
Project Number: 06
Description: [one sentence]
Archetype: standard
```

`collaboration_mode` will be set to `"solo"` in the generated `project-metadata.json` automatically. If you want to be explicit (or you're initializing a project that should actually run `traditional` — e.g., you do have real teammates), say so:

```
Collaboration Mode: traditional
```

You can confirm it took effect by checking `project-metadata.json`:

```json
{
  "project_id": "PRJ-06",
  "collaboration_mode": "solo",
  "...": "..."
}
```

---

## Step 2 — Run Requirements and Analysis Skills Normally

Nothing changes about *what* you run. Continue through the normal EDPS pipeline — `requirements-sanitize` (if needed) → `requirements-ingest` → `goals-extract` / `process-w5h` / `domain-extractconcepts`, etc.

What changes is what happens when a skill's instructions or gate call for stakeholder input.

### Example: `process-w5h`

When `process-w5h` identifies stakeholders in its WHO analysis — say, "Primary Stakeholders: End Users, Business Owner" — in solo mode you don't go find a Business Owner to interview. Instead:

1. Mentally (or literally) put on the Business Owner's hat.
2. Answer the analysis questions from that perspective.
3. Document the assumption inline, naming the role lens you used:

   > *"Assumed as Business Owner: success criteria reflect actual business priority, based on requirement R-014, not just technical feasibility."*

This is a **self-attestation**. It's logged the same way a real Business Owner's sign-off would be logged in `traditional` mode — just without a separate person behind it.

See `process-w5h/SKILL.md`'s **Mode-Conditional Stakeholder Engagement** section for the full pattern, and its **When to Break Out of Solo Mode** subsection for when you should stop self-attesting and go find a real person.

### Example: `requirements-sanitize`

Its Definition-of-Done asks that every retained statement be "understandable by a non-technical business stakeholder." In solo mode, you self-validate using that lens directly — and flag anything you're genuinely unsure you're representing accurately, rather than guessing silently. See its own **When to Break Out of Solo Mode** subsection for the specific triggers.

---

## Step 3 — Understand What Gates Do Differently

Some skills have a `gate.json` with a `stakeholder_confirmation` check (introduced in T03; `process-w5h`'s gate is the worked example). In `traditional` mode, this check is **hard** — it blocks you from completing the skill until a real confirmation record exists. In `solo` mode, it's **soft**:

- If you haven't recorded a confirmation, the gate **auto-passes** and generates a self-attestation record for you automatically, satisfied by the fact that you (the developer) are the one running the skill.
- You can still write your own self-attestation explicitly if you want more detail captured than the auto-generated note provides.
- Either way, nothing blocks you.

This is intentional — solo mode is supposed to be frictionless day-to-day, while still leaving a complete audit trail.

---

## Step 4 — Handle Change Requests

When something changes mid-project and you run `change-management`, the "notify stakeholders" step becomes role-aware:

- **If every role affected by the change is one you play yourself** (e.g., "this affects the QA testing approach") → log a short self-perspective note in the change document. No external contact needed.
- **If a role affected is flagged as a "real external stakeholder"** (see the table in `collaboration-mode-reference.md`'s **Real External Stakeholder Flag** section — e.g., Client/Sponsor, Regulator) → you still need to actually reach out to that real person. Solo mode never lets you self-attest on behalf of someone whose real agreement matters.

The same logic applies in `project-planning-tracking` when a schedule/estimate change triggers its own "Communicate Changes" step.

**Rule of thumb**: if you're unsure whether a role is developer-played or real-external, treat it as real-external. An unnecessary check-in costs you a few minutes; a skipped real check-in can cost you the whole relationship with that stakeholder.

---

## Step 5 — Know When to Break Out of Solo Mode Entirely

Solo mode doesn't mean you never talk to anyone. Per the source material behind this feature: *"the developer is responsible to reach out with stakeholders for feedback and clarification."* Concretely, reach out for real input when:

- A role's priorities are genuinely unclear from available information, and guessing wrong would meaningfully change scope, requirements, or the WHY of the project
- The decision has real financial, legal, or compliance consequences you can't verify yourself
- The affected role is flagged **real external** (see Step 4)
- The decision is high-stakes — irreversible, costly to redo, or tied to a committed deadline

This isn't a failure of solo mode — it's the "clarify" half of the build-and-clarify loop working as designed.

---

## Switching Modes Mid-Project

If your solo project unexpectedly gains a real second contributor (or vice versa), switch modes explicitly:

```
@workspace Use project-document-management's Change Collaboration Mode operation:

Project Number: 06
Target Mode: traditional
Reason: Added a second developer to the team
```

This logs the switch in `evolution_history` with a timestamp and reason. **It is not retroactive** — self-attestations and gate evaluations already recorded under the old mode stay valid as-is; only work done *after* the switch follows the new mode's rules.

---

## Quick Reference

| Situation | Traditional Mode | Solo Mode |
|---|---|---|
| Stakeholder role identified in analysis | Interview a real person | Role-play the perspective, document assumptions inline |
| `stakeholder_confirmation` gate check | Hard — blocks until confirmed | Soft — auto-passes with a self-attestation record |
| Change affects a developer-played role | Formal notification | Logged self-perspective note |
| Change affects a real external stakeholder | Formal notification | Still a real check-in — unchanged |
| Deployment-phase change | Requires stakeholder approval | Still requires a real check-in — unchanged, regardless of role flag |
| Genuinely ambiguous or high-stakes decision | Resolved via stakeholder input | Still resolved via real stakeholder input — solo mode doesn't remove this |

---

## See Also

- [`collaboration-mode-reference.md`](collaboration-mode-reference.md) — Full conceptual definitions, defaults, backward compatibility, and the Real External Stakeholder Flag
- [`migration-guide.md`](migration-guide.md) — If you're picking up an existing (pre-feature) project
- `.github/skills/process-w5h/SKILL.md` — Mode-Conditional Stakeholder Engagement
- `.github/skills/requirements-sanitize/SKILL.md` — Mode-conditional validation in Quality Checks
- `.github/skills/change-management/SKILL.md` — Mode-Conditional Stakeholder Communication, Real External Stakeholder Flag
- `.github/skills/project-planning-tracking/SKILL.md` — Mode-conditional re-baselining communication
- `.github/skills/edps-workflow-orchestrator/SKILL.md` — `stakeholder_confirmation` gate check evaluation logic
