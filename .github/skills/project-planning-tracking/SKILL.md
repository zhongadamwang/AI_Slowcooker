---
name: project-planning-tracking
description: Plan project phases, track milestones, manage tasks, and monitor progress using structured templates and tracking mechanisms compatible with document tree organization.
license: MIT
---

# Project Planning and Tracking

Provides structured approach to project planning, milestone tracking, and progress monitoring using templates that integrate with the established document tree structure.

## Core Function

**Input**: Project requirements, timeline constraints, resource information
**Output**: Project plans, milestone tracking, progress reports, task management structures

## Planning Framework

### 1. Project Planning Workflow

```markdown
## Phase 1: Project Initiation
- [ ] Project charter creation
- [ ] Stakeholder identification  
- [ ] Initial requirements gathering
- [ ] Success criteria definition
- [ ] Resource assessment

## Phase 2: Planning
- [ ] Work breakdown structure (WBS)
- [ ] Timeline development
- [ ] Risk assessment
- [ ] Resource allocation
- [ ] Communication plan

## Phase 3: Execution & Monitoring
- [ ] Progress tracking
- [ ] Milestone reviews
- [ ] Risk mitigation
- [ ] Change management
- [ ] Quality assurance

## Phase 4: Closure
- [ ] Deliverable verification
- [ ] Lessons learned
- [ ] Documentation finalization
- [ ] Project closure report
```

### 2. Milestone Template

Store as `project-milestones.md` in project root:

```markdown
# [Project Name] - Milestones

| ID | Milestone | Target Date | Status | Dependencies | Notes |
|----|-----------|-------------|---------|--------------|-------|
| M01 | Requirements Complete | YYYY-MM-DD | Not Started | - | Initial req gathering |
| M02 | Analysis Phase Done | YYYY-MM-DD | Not Started | M01 | Analysis artifacts |
| M03 | Design Approval | YYYY-MM-DD | Not Started | M02 | Stakeholder sign-off |
| M04 | Development Complete | YYYY-MM-DD | Not Started | M03 | All features implemented |
| M05 | Testing Complete | YYYY-MM-DD | Not Started | M04 | QA validation |
| M06 | Production Deployment | YYYY-MM-DD | Not Started | M05 | Go-live |

## Status Legend
- **Not Started**: Planning or waiting for dependencies
- **In Progress**: Active work ongoing
- **At Risk**: Behind schedule or blocked
- **Complete**: Milestone achieved
- **Cancelled**: No longer applicable
```

### 3. Task Tracking Template

Store as `project-tasks.md` in project root:

```markdown
# [Project Name] - Task Tracking

## Active Sprint/Iteration
**Period**: [Start Date] - [End Date]

### High Priority
- [ ] [Task Description] (Assigned: [Name], Due: [Date])
- [ ] [Task Description] (Assigned: [Name], Due: [Date])

### Medium Priority  
- [ ] [Task Description] (Assigned: [Name], Due: [Date])
- [ ] [Task Description] (Assigned: [Name], Due: [Date])

### Low Priority
- [ ] [Task Description] (Assigned: [Name], Due: [Date])
- [ ] [Task Description] (Assigned: [Name], Due: [Date])

## Completed Tasks
- [x] [Completed Task] (Completed: [Date])

## Blocked/Waiting
- [ ] [Blocked Task] - Blocked by: [Reason/Dependency]

## Next Sprint Candidates
- [ ] [Future Task] (Estimated Effort: [Size])
```

## Progress Tracking

### Weekly Status Report Template

```markdown
# Weekly Status Report - [Project Name]
**Week of**: [Date Range]
**Prepared by**: [Name]
**Next Update**: [Date]

## Executive Summary
[High-level status - Green/Yellow/Red with brief explanation]

## Progress This Week
### Completed
- [Accomplishment 1]
- [Accomplishment 2]

### In Progress
- [Current Work Item 1] - [% Complete]
- [Current Work Item 2] - [% Complete]

## Upcoming (Next Week)
- [Planned Task 1]
- [Planned Task 2]

## Issues & Risks
| Issue | Impact | Mitigation | Owner | Target Resolution |
|-------|--------|------------|-------|-------------------|
| [Issue] | [High/Med/Low] | [Action] | [Person] | [Date] |

## Milestone Status
- **Next Milestone**: [Name] - [Target Date] - [On Track/At Risk/Behind]
- **Key Dependency**: [What needs to happen]

## Resource Status
- **Team Availability**: [Any capacity issues]
- **Budget Utilization**: [% used / remaining]
- **Critical Needs**: [Resources needed]

## Metrics
- **Requirements**: [# Complete] / [# Total] ([% Complete])
- **Test Cases**: [# Passed] / [# Total] ([% Coverage])
- **Key Deliverables**: [# Complete] / [# Planned]
```

### Project Health Dashboard

Store as `project-health.md`:

```markdown
# [Project Name] - Health Dashboard

## Overall Health: [🟢 Green | 🟡 Yellow | 🔴 Red]

### Key Performance Indicators

| Metric | Current | Target | Status | Trend |
|--------|---------|---------|---------|-------|
| Schedule Adherence | [%] | 90% | [🟢🟡🔴] | [↗↗↘] |
| Budget Utilization | [%] | <80% | [🟢🟡🔴] | [↗↗↘] |
| Requirements Completeness | [%] | 100% | [🟢🟡🔴] | [↗↗↘] |
| Defect Rate | [#] | <5 | [🟢🟡🔴] | [↗↗↘] |
| Stakeholder Satisfaction | [rating] | >4/5 | [🟢🟡🔴] | [↗↗↘] |

### Risk Register
| Risk | Probability | Impact | Mitigation | Owner | Status |
|------|-------------|---------|-------------|-------|---------|
| [Risk Description] | [H/M/L] | [H/M/L] | [Action] | [Name] | [Active/Resolved] |

### Change Log
| Date | Change | Impact | Approved By |
|------|--------|---------|-------------|
| [Date] | [Description] | [Schedule/Budget/Scope] | [Stakeholder] |
```

## Integration with Document Tree

### Project Structure Enhancement

Adds planning artifacts to existing project structure:

```
orgDocument/projects/[NN] - [project name]/
├── requirements/
├── artifacts/
├── main.md
├── project-milestones.md      # Milestone tracking
├── project-tasks.md           # Task management  
├── project-health.md          # Health dashboard
├── status-reports/            # Weekly/monthly reports
│   ├── YYYY-MM-DD-weekly.md
│   └── YYYY-MM-DD-monthly.md
└── planning/                  # Planning artifacts  
    ├── project-charter.md
    ├── work-breakdown.md
    ├── risk-register.md
    └── resource-plan.md
```

## Quick Commands

### Initialize Project Planning
1. Create planning folder structure
2. Generate milestone template
3. Create task tracking template  
4. Initialize health dashboard
5. Set up status reporting schedule

### Update Project Status
1. Review milestone progress
2. Update task completion status
3. Assess risks and issues
4. Generate status report
5. Update health metrics

### Milestone Review
1. Evaluate milestone criteria completion
2. Update milestone status
3. Identify next period priorities
4. Document lessons learned
5. Plan celebration/communication

## Planning Best Practices

1. **Regular Updates**: Weekly task updates, bi-weekly milestone reviews
2. **Clear Ownership**: Assign specific owners to tasks and milestones
3. **Realistic Estimates**: Use historical data and buffer time
4. **Early Warning**: Flag risks and issues promptly
5. **Stakeholder Communication**: Regular, consistent status updates
6. **Continuous Improvement**: Capture and apply lessons learned

## Metrics and KPIs

### Schedule Metrics
- Milestone completion rate
- Task completion velocity  
- Schedule variance percentage
- Critical path adherence

### Quality Metrics
- Requirements traceability
- Test case pass rate
- Defect discovery rate
- Stakeholder satisfaction scores

### Resource Metrics
- Budget utilization
- Team capacity utilization
- Resource allocation efficiency
- Change request impact

## Reporting Cadence

- **Daily**: Task updates (via comments/status)
- **Weekly**: Status reports and team meetings
- **Bi-weekly**: Milestone reviews and planning  
- **Monthly**: Health dashboard updates and stakeholder reports
- **Quarterly**: Project retrospectives and process improvements