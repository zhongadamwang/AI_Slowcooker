# T08 — Author screen-assembledocument Skill (Consolidated Design Doc)

**Task ID**: T08
**Phase**: Phase 3 - Discussion & Integration
**Priority**: P0-Critical
**Estimated Effort**: 1-2 days
**Status**: Not Started
**Assigned**: [Unassigned]
**Created**: 2026-10-26
**Last Updated**: 2026-10-26

## Description

Implements R-607 (UI Design Document Output), R-608 (JSON Companion), and R-610 (In-Document Changelog) at the consolidated-document level. This is the durable deliverable "suitable for handing to a future developer without requiring the original AI session" — one of the project's core stated goals.

## Objectives

- Author a skill that assembles the consolidated `DesignDocument` (Markdown + JSON) summarizing all screens/flows/components from T04–T07
- Include a top-level in-document changelog

## Detailed Requirements

### Functional Requirements
- **FR-08.1**: Consolidated document summarizes screens/flows/components without duplicating full storage — screen inventory (T04) remains the standalone source of truth; this document references it
- **FR-08.2**: JSON companion output mirrors the Markdown content

### Technical Requirements
- **TR-08.1**: Document must pass a "handoff" sanity check — readable and actionable by someone unfamiliar with the generating session (or self-reviewed from that lens in solo mode)

## Acceptance Criteria

- [ ] SKILL.md authored
- [ ] Consolidated design document generated from a test screen/flow/component set
- [ ] JSON companion well-formed and consistent with Markdown content
- [ ] Handoff sanity check performed and passed

## Dependencies

### Prerequisites
- **T05, T06, T07** — needs layout specs, mockups, and flows to summarize

### Blocks
- T10 (gate registration needs a stable output to validate against)
- T11 (validation dry run exercises this skill)
