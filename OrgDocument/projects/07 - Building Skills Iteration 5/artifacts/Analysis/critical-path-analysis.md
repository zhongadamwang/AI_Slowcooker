# Critical Path Analysis

**Project**: PRJ-07  
**Basis**: Rounded PERT expected durations and prerequisite DAG; unlimited resources

| Task | Earliest start | Earliest finish | Total slack |
|------|----------------|-----------------|-------------|
| T01 | 0.00 | 2.00 | 0.00 |
| T02 | 2.00 | 5.17 | 0.16 |
| T03 | 2.00 | 4.00 | 1.33 |
| T04 | 2.00 | 5.33 | 0.00 |
| T05 | 5.33 | 7.50 | 0.00 |
| T06 | 7.50 | 10.83 | 0.00 |
| T07 | 10.83 | 14.00 | 0.00 |

Critical path: **T01 -> T04 -> T05 -> T06 -> T07**, approximately 14.00 working days. T02 is near-critical: a delay of more than 0.16 day makes its branch controlling. These are planning approximations, not minute-level commitments.

Resource leveling for one implementer yields 19.17 working days before contingency. All work consumes that implementer's capacity even if the prerequisite DAG permits parallelism. Do not report the 14-day lower bound as the solo delivery timeline.

Prioritize contract quality and early source-backed validator fixtures to reduce rework. Independent implementation can use frozen shared fixtures, but concurrent modifications of one boundary's real models require version checking/serialization.

See [schedule](project-schedule.md) and [task dependencies](task-breakdown.md).
