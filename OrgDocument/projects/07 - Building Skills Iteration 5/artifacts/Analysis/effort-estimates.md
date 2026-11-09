# Provisional Effort Estimates

**Project**: PRJ-07  
**Date**: 2026-11-07  
**Source**: [Task breakdown](task-breakdown.md)  
**Structured data**: [effort-estimates.json](effort-estimates.json)

| Task | Optimistic | Most likely | Pessimistic | PERT expected | Risk rationale |
|------|------------|-------------|-------------|---------------|----------------|
| T01 | 1 | 2 | 3 | 2.00 | Shared scoped identity and applicability contract |
| T02 | 2 | 3 | 5 | 3.17 | Multi-level use-case scripts and stable revisions |
| T03 | 1 | 2 | 3 | 2.00 | Extend current UI schema without consumer breakage |
| T04 | 2 | 3 | 6 | 3.33 | Actual-source checks, contradictions, stale reports |
| T05 | 1 | 2 | 4 | 2.17 | Multiple existing producers/consumers and gates |
| T06 | 2 | 3 | 6 | 3.33 | Resume/round state and mode/archetype bypass prevention |
| T07 | 2 | 3 | 5 | 3.17 | Integrated examples, observed behavior, documentation |
| **Total person-days** | **11** | **18** | **32** | **19.17** | Uncalibrated planning estimate |

PERT: expected effort `(O + 4M + P) / 6`; variance `((P - O) / 6)^2`. Qualitative complexity/risk informed the triples; no unsupported velocity/story-point conversion or historical actuals are claimed. Risks are included in pessimistic estimates, not multiplied again.

One implementer at full capacity gives approximately 19.17 working days before contingency. Add 3 working days, then round up to approximately 23 working days. Parallel implementation after T01 can reduce elapsed time, not total effort; unlimited-resource critical path is approximately 14.00 days.

Illustrative independent-risk PERT intervals are 17.42-20.92 person-days (80%) and 16.49-21.84 (95%). These are not calibrated delivery guarantees; shared contract/integration risks are correlated. See [confidence notes](estimation-confidence.md).
