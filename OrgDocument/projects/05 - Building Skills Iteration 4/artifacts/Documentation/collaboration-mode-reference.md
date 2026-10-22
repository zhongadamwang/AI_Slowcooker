# Collaboration Mode Reference

This reference defines `collaboration_mode`, a project-level setting that determines how stakeholder confirmation and approval work across the EDPS skill framework. It is orthogonal to **workflow archetype** (`standard` / `rapid` / `compliance`) — any archetype can run in either mode.

**Source material**: `artifacts/Source Materials/add-solo-mode.md`

## Why This Exists

Traditional projects have many team members performing distinct roles. Because different people hold different perspectives and considerations, the project needs explicit confirmation and approval from each person to assure responsibilities are fulfilled and requirements are confirmed — this also waives the project team's liability for misunderstood intent.

AI-aided projects typically have a single developer working with EDPS skills. That developer presents *all* roles in the target business process. Information is still fed in **by role**, not by person's name — so the framework continues to reason about role-based collaboration — but there is no second person available to confirm or approve. The accountability mechanism has to change: formal sign-off becomes a documented self-review, and the discipline shifts into a **build-and-clarify loop**, where the developer is responsible for reaching out to real stakeholders for feedback when genuine ambiguity exists.

`collaboration_mode` makes this an explicit, auditable project setting instead of an implicit assumption.

## The Two Modes

### `traditional`

- Multiple real people occupy different roles in the process.
- Role-based confirmations must be backed by an actual, distinct person's sign-off.
- Formal approval/confirmation steps are **hard requirements** — skills and gates that call for stakeholder confirmation block progress until a real confirmation record exists.
- This is the existing EDPS behavior (Iterations 1–3), unchanged by this feature. It is also the **safe default** for any project that predates this setting (see [Backward Compatibility](#backward-compatibility)).

### `solo`

- One developer represents every role in the process.
- Role-based outputs (e.g., "Primary Stakeholders: End Users") are still captured **by role**, never by a person's name — this does not change between modes.
- The developer self-attests on behalf of each role instead of obtaining a separate person's sign-off. A self-attestation is a short, explicit note identifying which role lens was used and what was confirmed (see [Self-Attestation vs. Sign-Off](#self-attestation-vs-sign-off)).
- Formal confirmation/approval steps become **soft** — they are satisfied by a logged self-attestation rather than blocking on an external party.
- The loop driving quality is no longer "wait for approval" but **build-and-clarify**: produce the artifact, self-review it from the relevant role's perspective, and iterate.
- Solo mode does **not** eliminate real stakeholder involvement. When a role genuinely represents a separate external party (e.g., an actual client or sponsor, not a role the developer can credibly self-represent), the developer is still responsible for reaching out for real feedback and clarification. This distinction is formalized as the **real external stakeholder flag**, defined fully in `T05` and applied in `change-management` / `project-planning-tracking`.

## Self-Attestation vs. Sign-Off

| | Sign-Off (traditional) | Self-Attestation (solo) |
|---|---|---|
| **Who provides it** | A distinct person occupying the role | The developer, explicitly naming which role lens they used |
| **What it represents** | Independent confirmation that the role's concerns are satisfied | A documented self-review from that role's perspective |
| **Blocking behavior** | Hard — blocks workflow progression until provided | Soft — logged, does not block |
| **Audit trail** | Confirmation record: role, person, statement, timestamp | Self-attestation record: role, statement, timestamp (same shape, no separate-person field required) |
| **Can be skipped silently?** | No | No — still logged every time, just non-blocking |

Both forms produce the same kind of audit record so a project's history reads consistently regardless of mode; only the identity behind the record and its blocking severity differ.

## Scope of This Setting (v1)

- `collaboration_mode` is a **project-level** setting — one value per project, not configurable per skill or per task in this phase. Keeping v1 simple avoids a combinatorial mode matrix before real usage data exists.
- It governs only **stakeholder confirmation/approval mechanics** (gates of type `stakeholder_confirmation`, introduced in T03) and the **instructional guidance** inside stakeholder-facing skills (T04, T05). It does not change artifact structure, archetype selection, or any other gate check type.

## Default Mode

**New projects default to `solo`.** This framework is built for AI-aided single-developer use; requiring an explicit opt-in to the common case would add friction for no safety benefit.

## Backward Compatibility

**Existing projects without a `collaboration_mode` field are treated as `traditional`.** This is a deliberate asymmetry from the new-project default above: a project that predates this feature was built under the old implicit assumption that approvals matter, and absence of the field must never be read as silent permission to relax that expectation. A project can only become `solo` through an explicit, logged action (see [Changing Mode](#changing-mode)) — never by omission.

## Where It Lives

`collaboration_mode` is stored in `project-metadata.json` at the project root:

```json
{
  "project_id": "PRJ-NN",
  "collaboration_mode": "solo | traditional",
  "...": "..."
}
```

Implementation of the field itself (schema wiring into `project-document-management` and the init flow) is covered by **T02**.

## Changing Mode

Mode is set at project initialization and may be changed later via an explicit command (e.g., `orchestrate set-mode solo`). Every mode change is recorded as an entry in `project-metadata.json`'s `evolution_history`, including the timestamp and the reason for the change. A mode change is **not retroactive**: gate evaluations and self-attestations already recorded under the old mode remain valid as-is; only evaluations performed after the switch follow the new mode's rules. Full implementation is covered by **T02**.

## Real External Stakeholder Flag

Solo mode's self-attestation mechanism assumes the developer can credibly represent a role themselves. That assumption breaks down when a role is actually backed by a separate real person whose agreement genuinely matters — self-attesting on their behalf would misrepresent their actual position, not just streamline process overhead. The **real external stakeholder flag** marks which roles fall into that category.

**Definition**: A role is flagged **real external** when it is tied to an actual, separate party outside the developer's own judgment — someone whose buy-in, interpretation, or authority cannot be substituted by the developer role-playing that perspective. A role is **developer-played** when the developer can credibly perform that function themselves in a solo project, even though the role is still tracked and reasoned about separately.

This flag governs the build-and-clarify loop introduced in **T05**: in `solo` mode, developer-played roles are satisfied by a logged self-perspective note (no external contact needed); real external roles still require an actual check-in, exactly as in `traditional` mode. The flag has no effect in `traditional` mode, where every role already requires real-person confirmation regardless.

| Role | Flag | Rationale |
|---|---|---|
| Client / Sponsor | **Real external** | An actual paying party or budget holder; their agreement to scope/schedule impact cannot be self-attested |
| Regulator / Compliance Officer | **Real external** | Regulatory interpretation requires real authority the developer cannot substitute for |
| QA | Developer-played | In a solo project, the developer performs the QA function directly; no separate QA person exists to notify |
| DevOps / Ops | Developer-played | Same reasoning — the developer is also the ops function in a solo project |

**Default rule**: When a role's status is unclear, default to **real external**. Treating a developer-played role as external only costs an unnecessary check-in; treating a real external stakeholder as developer-played risks silently proceeding without the one person whose agreement actually matters.

Applied in `change-management/SKILL.md` (Mode-Conditional Stakeholder Communication) and `project-planning-tracking/SKILL.md` (Estimation Update Process, Step 4 Implementation Planning).

## Downstream Impact (What This Schema Feeds)

This definition is the foundation other T0x tasks build on:

| Task | What it adds |
|---|---|
| **T02** | Implements the `collaboration_mode` field in `project-document-management`, `project-metadata.json`, and the `set-mode` command |
| **T03** | Adds a new gate check type, `stakeholder_confirmation`, whose severity is mode-dependent (hard in `traditional`, soft/self-attested in `solo`); updates the orchestrator's gate evaluator to branch on mode before archetype |
| **T04** | Updates stakeholder-facing skill *instructions* (`process-w5h`, `requirements-sanitize`, `requirements-ingest`) with mode-conditional guidance, replacing assumptions of a mandatory live stakeholder interview |
| **T05** | Updates `change-management` and `project-planning-tracking` with a build-and-clarify loop and introduces the **real external stakeholder flag** so solo mode never silently skips a check-in that should involve an actual separate person |
| **T06** | Publishes a user-facing `solo-mode-guide.md`, migration notes for existing projects, and an end-to-end validation report |

## Worked Example

A solo developer initializes a new project. `collaboration_mode` defaults to `solo`. They run `process-w5h`, which identifies "Primary Stakeholders: End Users, Business Owner." Rather than interviewing a separate Business Owner, the developer role-plays that perspective, documents the assumption inline, and logs a self-attestation: *"Confirmed as Business Owner: success criteria reflect actual business priority, not just technical feasibility."* The gate for this step is satisfied (soft, non-blocking) and the project moves forward. Later, a genuine scope question arises that only the real client can answer — per the "real external stakeholder" flag (T05), the developer reaches out directly rather than self-attesting on the client's behalf.
