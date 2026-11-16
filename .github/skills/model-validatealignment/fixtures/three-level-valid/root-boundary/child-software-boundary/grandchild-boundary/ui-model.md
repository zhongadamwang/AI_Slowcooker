# UI Model — Grandchild Boundary

**Model ID**: UIM-GRANDCHILD
**Model Type**: base
**Boundary**: BND-GRANDCHILD (software)
**Generated**: 2026-11-08T00:00:00Z

## Changelog
- v1.0 (2026-11-08): Initial generation from use-case-model.json (UCM-GRANDCHILD)

## Generation Note

Boundary BND-GRANDCHILD's one use case (UC-001, Log Time Entry) has a **direct human actor** (Technician) performing the logging action themselves — unlike the `software-boundary-no-ui-required` fixture's "Nightly Scheduler" (an internal-role/scheduled-trigger actor with no human-facing interaction), this is a human directly entering data. One small UIModelEntry is therefore warranted here, not a forced absence — this is the deciding factor between this boundary and a boundary with only non-human actors.

## Entries

### Time Entry Log *(UME-001)*
**Aggregates**: TimeEntry (E-004)
*(Boundary: BND-GRANDCHILD; Ref: UC-001)*

A single-entity view of TimeEntry allowing a Technician to log a start/end time block directly, supporting the Log Time Entry use case.

---
**Traceability**: Every entry traces to its boundary and the use case(s) that motivated it
**Generated**: 2026-11-08T00:00:00Z
