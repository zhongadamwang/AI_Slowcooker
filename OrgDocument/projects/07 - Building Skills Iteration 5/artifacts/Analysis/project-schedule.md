# Implementation Schedule

**Project**: PRJ-07  
**Start/end dates**: Uncommitted  
**Assumption**: One implementer at full working-day capacity  
**Baseline**: 19.17 working days + 3 contingency days = 22.17, approximately 23 whole working days  
**Data**: [project-schedule.json](project-schedule.json)

Working-day offsets use half-open intervals; offset zero means implementation begins, not the project's creation date.

| Task | Start offset | Finish offset | Milestone |
|------|--------------|---------------|-----------|
| T01 | 0.00 | 2.00 | M1: Contract ready |
| T02 | 2.00 | 5.17 | |
| T03 | 5.17 | 7.17 | |
| T04 | 7.17 | 10.50 | M2: Producers and validator ready |
| T05 | 10.50 | 12.67 | |
| T06 | 12.67 | 16.00 | M3: Integrated S5 rounds ready |
| T07 | 16.00 | 19.17 | M4: Release evidence ready |
| Contingency | 19.17 | 22.17 | Rework, clarification, integration uncertainty |

Approximate resource-leveled Gantt (one character ~= one working day):

```text
Task   0    5    10   15   20
T01    ##
T02      ###
T03         ##
T04           ###
T05              ##
T06                ###
T07                   ###
Buffer                   ###
```

This serial order is a capacity choice, not additional task prerequisites. T02/T03/T04 can run independently after T01 using shared fixtures. With three implementers on that phase, the prerequisite critical path is approximately 14 working days before buffer; no staffing increase is assumed in the baseline.

At five full working days per week, the rounded solo envelope is approximately five weeks. Availability, holidays, and start date remain unknown. Re-estimate at M1 and M2 rather than converting this into a committed calendar deadline.

See [critical path](critical-path-analysis.md), [milestones](milestone-plan.md), and [confidence notes](estimation-confidence.md).
