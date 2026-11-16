# W5H Analysis — Output Format and Worked Example

The complete shape of `w5h-analysis.md` and `w5h-analysis.json`, shown as a worked example. Section headings and top-level JSON keys are fixed; the sub-structure inside each dimension follows the content of the requirements being analysed.

**Primary Format (Markdown)** - W5H Analysis Report:

```markdown
# W5H Requirements Analysis

**Project**: PROJECT-001
**Source**: requirements.md
**Generated**: 2026-02-08T14:30:00Z
**Analysis Framework**: Who, What, When, Where, Why, How

## WHO - Stakeholders and Roles

### Primary Stakeholders
- **End Users**: Software developers using evolutionary development practices
- **Project Team**: Internal development team members
- **Management**: Leadership overseeing development process improvement

### Secondary Stakeholders
- **Quality Assurance**: Testing teams validating new practices
- **Operations**: Teams responsible for deployment and maintenance

### Roles and Responsibilities
| Role | Responsibilities | Authority Level |
|------|-----------------|----------------|
| Development Team Lead | Oversee skill implementation | Decision maker |
| Team Members | Learn and apply new skills | Contributors |

## WHAT - Functional and Non-Functional Requirements

### Functional Requirements
- **F1**: Define core competencies for evolutionary development
- **F2**: Create learning pathways for skill development
- **F3**: Implement adaptive planning methodologies

### Non-Functional Requirements
- **NF1**: Process must integrate with existing tooling
- **NF2**: Training materials must be accessible to all team members
- **NF3**: Implementation timeline must be flexible

### System Boundaries
- **In Scope**: Internal team skill development, process adaptation
- **Out of Scope**: External vendor training, new tooling procurement

## WHEN - Timeline and Milestones

### Project Timeline
- **Phase 1**: Skill framework documentation (Weeks 1-2)
- **Phase 2**: Team capability assessment (Weeks 3-4)
- **Phase 3**: Learning plan creation (Weeks 5-6)
- **Phase 4**: Pilot implementation (Weeks 7-10)

### Critical Milestones
- **M1**: Framework completion - Week 2
- **M2**: Assessment completion - Week 4
- **M3**: Pilot launch - Week 7

### Dependencies and Constraints
- **Traditional mode**: Must complete stakeholder interviews before assessment
- **Solo mode**: The developer role-plays each identified stakeholder perspective (per `collaboration_mode` — see `collaboration-mode-reference.md`, Iteration 4 artifacts) and documents inline which role lens was used for each assumption, rather than scheduling a separate interview
- Pilot implementation depends on framework approval

## WHERE - Context and Environment

### Operational Environment
- **Development Environment**: VS Code with existing toolchain
- **Team Structure**: Cross-functional development teams
- **Geographic Distribution**: Primarily local team with some remote members

### System Integration Points
- **Version Control**: Integration with current Git workflows
- **CI/CD**: Compatibility with existing deployment pipelines
- **Documentation**: Alignment with current documentation standards

### Physical and Virtual Boundaries
- **Team Workspace**: Hybrid office/remote environment
- **Development Infrastructure**: Cloud-based development environment
- **Communication Channels**: Existing team communication tools

## WHY - Purpose and Business Rationale

### Business Drivers
- **Primary**: Improve development agility and responsiveness
- **Secondary**: Enhance team capabilities and job satisfaction
- **Strategic**: Position team for future evolutionary development challenges

### Success Metrics
- **Quantitative**: 25% reduction in feature delivery time
- **Qualitative**: Improved team confidence in handling changing requirements
- **Business**: Increased customer satisfaction with development responsiveness

### Value Proposition
- Enhanced ability to respond to changing market conditions
- Improved team resilience and adaptability
- Better alignment between development practices and business needs

## HOW - Implementation Approach and Methods

### Technical Approach
- **Methodology**: Incremental skill development with regular feedback
- **Framework**: Competency-based learning model
- **Assessment**: 360-degree skill evaluation process

### Implementation Strategy
1. **Discovery Phase**: Research best practices and assess current state
2. **Design Phase**: Create competency framework and learning paths
3. **Development Phase**: Build training materials and assessment tools
4. **Deployment Phase**: Roll out pilot program with selected team
5. **Evaluation Phase**: Measure results and refine approach

### Risk Mitigation
- **Risk**: Team resistance to change
  - **Mitigation**: Involve team in framework design, emphasize benefits
- **Risk**: Time constraints
  - **Mitigation**: Phase implementation, integrate with existing work

### Quality Assurance
- **Traditional mode**: Regular checkpoint reviews with stakeholders
- **Solo mode**: Regular self-review checkpoints from each relevant role's perspective, logged as self-attestations (see `stakeholder_confirmation` gate checks); genuinely ambiguous or high-stakes items are still escalated to a real stakeholder rather than self-attested — see [Mode-Conditional Stakeholder Engagement](#mode-conditional-stakeholder-engagement) below
- Continuous feedback collection from participants
- Measurable success criteria at each phase

## Summary

This W5H analysis provides a comprehensive view of the evolutionary development skill building project, ensuring all critical dimensions are considered in planning and implementation.
```

**Secondary Format (JSON)** - For Machine Processing:

```json
{
  "project_id": "PROJECT-001",
  "generated_at": "2026-02-08T14:30:00Z",
  "analysis_framework": "W5H",
  "who": {
    "primary_stakeholders": [
      {
        "role": "End Users",
        "description": "Software developers using evolutionary development practices",
        "influence": "high",
        "interest": "high"
      }
    ],
    "secondary_stakeholders": [
      {
        "role": "Quality Assurance", 
        "description": "Testing teams validating new practices",
        "influence": "medium",
        "interest": "medium"
      }
    ],
    "roles_responsibilities": [
      {
        "role": "Development Team Lead",
        "responsibilities": ["Oversee skill implementation"],
        "authority_level": "Decision maker"
      }
    ]
  },
  "what": {
    "functional_requirements": [
      {
        "id": "F1",
        "description": "Define core competencies for evolutionary development",
        "priority": "high",
        "category": "core_functionality"
      }
    ],
    "non_functional_requirements": [
      {
        "id": "NF1", 
        "description": "Process must integrate with existing tooling",
        "type": "integration_constraint",
        "priority": "high"
      }
    ],
    "scope": {
      "in_scope": ["Internal team skill development", "process adaptation"],
      "out_of_scope": ["External vendor training", "new tooling procurement"]
    }
  },
  "when": {
    "timeline": {
      "total_duration": "10 weeks",
      "phases": [
        {
          "name": "Phase 1",
          "description": "Skill framework documentation",
          "duration": "Weeks 1-2",
          "deliverables": ["Framework document"]
        }
      ]
    },
    "milestones": [
      {
        "id": "M1",
        "name": "Framework completion",
        "target_date": "Week 2",
        "dependencies": []
      }
    ]
  },
  "where": {
    "environment": {
      "development": "VS Code with existing toolchain",
      "team_structure": "Cross-functional development teams",
      "geographic": "Primarily local team with some remote members"
    },
    "integration_points": {
      "version_control": "Integration with current Git workflows",
      "cicd": "Compatibility with existing deployment pipelines",
      "documentation": "Alignment with current documentation standards"
    }
  },
  "why": {
    "business_drivers": {
      "primary": "Improve development agility and responsiveness",
      "secondary": "Enhance team capabilities and job satisfaction",
      "strategic": "Position team for future evolutionary development challenges"
    },
    "success_metrics": {
      "quantitative": "25% reduction in feature delivery time",
      "qualitative": "Improved team confidence in handling changing requirements",
      "business": "Increased customer satisfaction with development responsiveness"
    }
  },
  "how": {
    "technical_approach": {
      "methodology": "Incremental skill development with regular feedback",
      "framework": "Competency-based learning model",
      "assessment": "360-degree skill evaluation process"
    },
    "implementation_phases": [
      {
        "phase": "Discovery",
        "description": "Research best practices and assess current state",
        "activities": ["Stakeholder interviews", "Best practice research"]
      }
    ],
    "risks": [
      {
        "risk": "Team resistance to change",
        "probability": "medium",
        "impact": "high",
        "mitigation": "Involve team in framework design, emphasize benefits"
      }
    ]
  }
}
```
