# Project Plan — 05 - Building Skills Iteration 4

**Project ID**: PRJ-05  
**Archetype**: standard  
**Start Date**: May 11, 2026  
**Target Completion**: [TBD]  
**Status**: Planning Phase — Awaiting Requirements  

## Executive Summary

This iteration introduces a `collaboration_mode` switch (`solo` | `traditional`) across the EDPS skill framework, derived from `artifacts/Source Materials/add-solo-mode.md`. Traditional mode preserves today's multi-stakeholder approval/sign-off behavior unchanged. Solo mode lets a single AI-aided developer, who represents every stakeholder role, replace formal confirmation gates with self-attested build-and-clarify loops — while still surfacing real external stakeholder check-ins when a role genuinely represents a separate person (e.g., a client/sponsor).

## Project Phases

### Phase 1: Foundation
**Duration**: 2-3 days  
**Deliverables**: `collaboration-mode-reference.md`, `collaboration_mode` field wired into `project-document-management` and `project-metadata.json`

**Tasks**: T01 (schema & switch definition), T02 (wire into project init)

### Phase 2: Orchestration
**Duration**: 5-7 days  
**Deliverables**: Mode-aware gate check type (`stakeholder_confirmation`), updated gate evaluator, mode-conditional guidance in stakeholder-facing skills and change/planning skills

**Tasks**: T03 (gate evaluation), T04 (stakeholder-facing skills), T05 (build-and-clarify loop for change mgmt/planning)

### Phase 3: Validation
**Duration**: 1-2 days  
**Deliverables**: `solo-mode-guide.md`, migration guidance for existing projects, end-to-end validation report

**Tasks**: T06 (documentation, migration notes, validation)

## Risk Management

- **Backward compatibility risk**: Existing projects must not silently lose approval gates. Mitigation: default to `traditional` when `collaboration_mode` is absent (T01/T02).
- **Role-confusion risk**: Solo mode could blur when a role is genuinely a separate external party. Mitigation: "real external stakeholder" flag (T05) keeps real check-ins from being skipped.
- **Scope creep risk**: Touches many existing skill files (gates + instructions). Mitigation: tasks scoped per skill group (T03 gates, T04/T05 instructions) to keep diffs reviewable.

## Dependencies

- Project 04 - Building Skills Iteration 3 (completed) — specifically T07 (orchestrator) and T08 (completion gates), which this feature extends
- `artifacts/Source Materials/add-solo-mode.md` — source material for this feature

## Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Project Initialization | May 11, 2026 | ✅ Complete |
| Collaboration Mode Tasks Defined | 2026-10-22 | ✅ Complete |
| Phase 1 Complete (T01-T02) | TBD | Not Started |
| Phase 2 Complete (T03-T05) | TBD | Not Started |
| Phase 3 Complete (T06) | TBD | Not Started |
| Project Complete | TBD | Not Started |

---

**Last Updated**: 2026-10-22
