# T01 — Define Collaboration Mode Schema & Switch

**Task ID**: T01
**Phase**: Phase 1 - Foundation
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-22
**Last Updated**: 2026-10-22

## Description

Introduce a first-class `collaboration_mode` concept (`traditional` | `solo`) that cuts across the whole EDPS skill framework, independent of workflow archetype (`standard`/`rapid`/`compliance`). This task defines the schema, vocabulary, and decision rules; later tasks wire it into individual skills.

Source: `artifacts/Source Materials/add-solo-mode.md` — traditional projects require multi-stakeholder confirmation/approval to assure accountability; solo AI-aided projects have one developer representing all roles, so approvals collapse into a build-and-clarify loop.

## Objectives

- Define `collaboration_mode` as an orthogonal axis to `archetype` (a solo *and* standard/rapid/compliance project is valid)
- Specify the semantic difference precisely: in `traditional`, role-based confirmations are mapped to a *real distinct person* who must sign off; in `solo`, the developer self-attests on behalf of every role, and formal sign-off steps are replaced by a documented self-review
- Define the default mode (recommend: `solo`, since this is an AI-aided single-developer framework) and how/where it's set

## Detailed Requirements

### Functional Requirements
- **FR-01.1**: `collaboration_mode` is a project-level setting, stored in `project-metadata.json`, set at project initialization and changeable later via explicit command
- **FR-01.2**: Mode applies globally to a project; no per-skill override in this phase (keep v1 simple)
- **FR-01.3**: Document the rule: role outputs (e.g., "Primary Stakeholders: End Users") are always captured by role name; in `solo` mode no individual person-name mapping is required or expected

### Technical Requirements
- **TR-01.1**: Schema addition is backward-compatible — existing projects without `collaboration_mode` default to `traditional` (safest default; do not silently relax existing approval expectations for prior projects)
- **TR-01.2**: Document in a new `collaboration-mode-reference.md` artifact (shared reference, not tied to one skill)

## Acceptance Criteria

### Definition of Done
- [ ] `collaboration-mode-reference.md` published defining the two modes, defaults, and the self-attestation vs sign-off distinction
- [ ] `project-metadata.json` schema documented with the new field (see T02 for implementation)
- [ ] Clear statement of which downstream skills/gates are affected (feeds T03–T05)

## Dependencies

### Prerequisites
- None — this is the foundational definition task

### Blocks
- T02, T03, T04, T05 all depend on this schema being settled first
