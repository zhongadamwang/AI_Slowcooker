# Tasks - Building Skills Iteration 4

This folder contains individual task files for implementing the Project 5 objectives. Each task follows GitHub issue format for team collaboration and tracking.

## Task Overview

This iteration's first feature — a **solo vs. traditional collaboration mode** switch across the EDPS framework (source: `../artifacts/Source Materials/add-solo-mode.md`) — is **complete** as of 2026-10-22. Traditional mode keeps today's multi-stakeholder approval/sign-off behavior; solo mode replaces it with developer self-attestation across roles, collapsing into a build-and-clarify loop, while still prompting real external check-ins when a role represents an actual separate stakeholder. See `../artifacts/Documentation/solo-mode-guide.md` for the how-to guide and `../artifacts/Testing/solo-mode-validation-report.md` for end-to-end validation results.

| Task | Title | Phase |
|---|---|---|
| [T01](T01-define-collaboration-mode-schema.md) | Define Collaboration Mode Schema & Switch | 1 - Foundation |
| [T02](T02-wire-mode-into-project-init.md) | Wire Mode into Project Initialization | 1 - Foundation |
| [T03](T03-mode-aware-gate-evaluation.md) | Mode-Aware Gate Evaluation (Approval Checks) | 2 - Orchestration |
| [T04](T04-update-stakeholder-facing-skills.md) | Update Stakeholder-Facing Skills for Solo Input | 2 - Orchestration |
| [T05](T05-build-and-clarify-loop.md) | Build-and-Clarify Loop (Change Mgmt & Planning) | 2 - Orchestration |
| [T06](T06-documentation-and-validation.md) | Documentation, Migration Notes & Validation | 3 - Validation |

## Task Status Summary

| Phase | Total Tasks | Not Started | In Progress | Completed | Progress % |
|-------|-------------|-------------|-------------|-----------|------------|
| **1 - Foundation** | 2 | 0 | 0 | 2 | 100% |
| **2 - Orchestration** | 3 | 0 | 0 | 3 | 100% |
| **3 - Validation** | 1 | 0 | 0 | 1 | 100% |
| **Total** | **6** | **0** | **0** | **6** | **100%** |

## Getting Started

1. Review original project materials in [`../artifacts/Source Materials/`](../artifacts/Source%20Materials/)
2. Check project overview in [`../main.md`](../main.md)
3. Refer to [`task-template.md`](task-template.md) for creating new tasks
4. Track progress in [`task-tracking.md`](task-tracking.md)
5. **This feature is complete** — see [`../artifacts/Documentation/solo-mode-guide.md`](../artifacts/Documentation/solo-mode-guide.md) to start using solo mode, or [`../artifacts/Testing/solo-mode-validation-report.md`](../artifacts/Testing/solo-mode-validation-report.md) for validation details
