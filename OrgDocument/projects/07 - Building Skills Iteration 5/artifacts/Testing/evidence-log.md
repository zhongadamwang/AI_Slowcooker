# Evidence Log — T07 Release Verification

**Project**: PRJ-07 — Building Skills Iteration 5
**Generated**: 2026-11-08

Every test suite/check referenced by [requirement-coverage-matrix.md](requirement-coverage-matrix.md) and [negative-examples/README.md](worked-example/negative-examples/README.md) was re-run during T07 itself, not assumed to still hold from earlier tasks. Full transcripts below.

## 1. `model-validatealignment` Combined Test Suite (T01 + T04)

```
$ python3 -m unittest test_alignment_contract test_alignment_report -v
...
----------------------------------------------------------------------
Ran 18 tests in 0.004s

OK
```

## 2. End-to-End Fixture Runner (T04)

```
$ python3 run_fixtures.py
[OK] three-level-valid: generated status='PASS', expected status='PASS'
[OK] unknown-boundary-type: generated status='NEEDS_CLARIFICATION', expected status='NEEDS_CLARIFICATION'
[OK] missing-applicable-model: generated status='INVALID_INPUT', expected status='INVALID_INPUT'
[OK] manifest-source-disagreement: generated status='INVALID_INPUT', expected status='INVALID_INPUT'
[OK] software-boundary-no-ui-required: generated status='PASS', expected status='PASS'

All 5 fixtures: generated status matches expected-report.json status.
```

## 3. Pre-Existing Prototype Contract Regression Suite (unmodified by PRJ-07)

```
$ python3 .github/skills/screen-generatemockup/scripts/test_prototype_contract.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.006s

OK
```

This suite pre-dates PRJ-07 entirely (from PRJ-06's own development). Its continued, unmodified pass after all of T01–T06's integration edits is direct evidence that none of the six existing `screen-*` skills' schemas, IDs, or interactive-prototype contract were disturbed.

## 4. T07 Worked-Example Real DOM Interaction Verification (new, this task)

```
$ node verify_interactions.js
PASS: SCR-102: Update Status button starts disabled
PASS: SCR-102: Update Status button enabled after selecting a status
PASS: SCR-102: confirm dialog starts hidden
PASS: SCR-102: dialog opens on Update Status click
PASS: SCR-102: dialog shows the chosen status value
PASS: SCR-102: dialog closes on Cancel
PASS: SCR-102: Cancel does NOT apply the status change
PASS: SCR-102: dialog re-opens for second attempt
PASS: SCR-102: dialog closes on Confirm (save)
PASS: SCR-102: Confirm DOES apply the status change
PASS: SCR-101: Assign button starts disabled
PASS: SCR-101: Assign button still disabled with only technician chosen
PASS: SCR-101: Assign button enabled once both technician and time slot are set
PASS: SCR-101: assigned technician cell updates on Assign
PASS: SCR-101: confirmation message shown after Assign

ALL 15 CHECKS PASSED
```

See [browser-verification-report.md](worked-example/child-software-boundary/UI%20Prototype/browser-verification-report.md) for the full honest scoping of what this does and does not confirm (real DOM/JS execution: yes; visual rendering in an actual browser window: not achievable in this sandbox, explicitly flagged as a residual follow-up).

## 5. Stale-Report Scenario (new, this task)

```
$ python3 stale_report_demo.py
is_stale(): True
resolve_round_for_resume(): stale

--- counterfactual: no edit happened ---
is_stale(): False
resolve_round_for_resume(): valid
```

## 6. Non-Bypassability Structural Proof (T04, re-confirmed as part of the combined suite above)

`test_alignment_report.py::RevisionInvalidationTests::test_a_skip_or_self_attestation_cannot_fabricate_a_valid_resume` is included in the 18-test combined suite run (#1 above) and passed. It asserts, via `inspect.signature(resolve_round_for_resume)`, that the function's parameter set is exactly `{"prior_round", "current_model_versions"}` — no `collaboration_mode`/`severity`/`archetype` parameter exists for any caller to exploit.

---
**All six evidence items above were executed in this task, with their literal console output reproduced rather than paraphrased.**
