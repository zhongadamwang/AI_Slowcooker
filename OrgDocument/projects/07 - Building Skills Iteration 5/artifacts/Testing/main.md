# Testing

## Purpose
Test artifacts, validation reports, and integration test results.

## Contents
- `requirement-coverage-matrix.md` — all 11 requirements (R-001–R-011) with linked, actually-executed passing evidence
- `evidence-log.md` — full re-run transcript of every test suite/script the coverage matrix and negative-examples catalog reference
- `worked-example/` — the three-level worked example's screen-pipeline run and negative-examples catalog
  - `child-software-boundary/UI Prototype/` — a real S33–S36 screen-pipeline run (2 screens) against T03's actual `ui-model.json`, including a Node.js/jsdom real-DOM interaction verification script and its honest browser-verification report
  - `negative-examples/` — all six required negative/clarification scenarios, each with an executed proof
