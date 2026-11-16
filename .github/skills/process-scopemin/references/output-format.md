# Scope Analysis — Output Format

The complete templates for `scope-analysis.md` and `scope-analysis.json`.

**Primary Format (Markdown)** - Scope Analysis Report:

```markdown
# Minimum Viable Scope Analysis

**Project**: PROJECT-001
**Source**: requirements.md
**Generated**: 2026-02-15T10:30:00Z
**Analysis Method**: Business Value + Dependency + Complexity Assessment

## Executive Summary

**MVP Definition**: [Brief description of the minimum viable product]
**Core Features Count**: X features identified as essential
**Enhancement Features**: Y features for post-MVP phases
**Optional Features**: Z features for future consideration
**Estimated MVP Effort**: [Time/resource estimate]

## Core Features (MVP Essential)

### Feature: [Feature Name]
- **Business Value**: [High/Medium/Low] - [Justification]
- **Technical Complexity**: [High/Medium/Low]
- **Dependencies**: [List of prerequisite features]
- **User Impact**: [Critical functionality description]
- **Risk of Exclusion**: [What happens if not included in MVP]

## Enhancement Features (Post-MVP Phase 1)

### Feature: [Feature Name]
- **Business Value**: [High/Medium/Low] - [Justification]
- **Technical Complexity**: [High/Medium/Low]
- **Dependencies**: [List of prerequisite features]
- **Enhancement Rationale**: [Why this builds on MVP]
- **Target Release**: [Suggested phase/timeline]

## Optional Features (Future Consideration)

### Feature: [Feature Name]
- **Business Value**: [High/Medium/Low] - [Justification]
- **Technical Complexity**: [High/Medium/Low]
- **Nice-to-Have Rationale**: [Why this is optional]
- **Potential ROI**: [Return on investment analysis]

## Feature Prioritization Matrix

| Feature | Business Value | Technical Complexity | Dependencies | MVP Category |
|---------|----------------|---------------------|--------------|--------------|
| [Name]  | [H/M/L]        | [H/M/L]            | [List/None]  | [Core/Enhance/Optional] |

## MVP Roadmap

### Phase 0 - Foundation
- [Core infrastructure features]
- [Essential service foundations]

### Phase 1 - MVP Launch
- [Minimum viable feature set]
- [Core user workflows]

### Phase 2 - Enhancement
- [First enhancement features]
- [User experience improvements]

### Phase 3 - Expansion
- [Advanced features consideration]
- [Platform scaling capabilities]

## Scope Boundaries

### In Scope (MVP)
- [Clearly defined included functionality]
- [Core user journeys supported]
- [Essential integrations]

### Out of Scope (MVP)
- [Explicitly excluded functionality]
- [Deferred advanced features]
- [Future integration considerations]

## Risk Assessment

### High Priority Risks
- [Risks that could impact MVP viability]
- [Mitigation strategies]

### Medium Priority Risks
- [Risks that could delay enhancement phases]
- [Monitoring approaches]

## Success Criteria

### MVP Launch Success
- [Measurable criteria for MVP success]
- [User adoption metrics]
- [Business value validation]

### Enhancement Phase Success
- [Criteria for proceeding to enhancement features]
- [Performance and usage thresholds]

## Recommendations

### Immediate Actions
1. [Priority development recommendations]
2. [Resource allocation suggestions]
3. [Risk mitigation priorities]

### Future Considerations
1. [Long-term strategic recommendations]
2. [Technology evolution planning]
3. [Market expansion opportunities]

---
**Traceability**: Requirements tracked to original specifications
**Review Date**: [Scheduled scope review date]
**Stakeholder Approval**: [Pending/Approved status]
```

**Secondary Format (JSON)** - Machine Processing:

```json
{
  "metadata": {
    "project_id": "PROJECT-001",
    "source_file": "requirements.md",
    "generated_timestamp": "2026-02-15T10:30:00Z",
    "analysis_method": "business_value_dependency_complexity",
    "skill_version": "1.0.0"
  },
  "mvp_summary": {
    "definition": "Brief MVP description",
    "core_features_count": 5,
    "enhancement_features_count": 8,
    "optional_features_count": 12,
    "estimated_effort": "3-4 months"
  },
  "features": [
    {
      "id": "FEAT-001",
      "name": "Feature Name",
      "category": "core|enhancement|optional",
      "business_value": {
        "score": "high|medium|low",
        "justification": "Value proposition explanation"
      },
      "technical_complexity": {
        "score": "high|medium|low",
        "implementation_notes": "Technical considerations"
      },
      "dependencies": [
        "FEAT-002", "FEAT-003"
      ],
      "user_impact": "Impact description",
      "priority_score": 85,
      "phase_assignment": "mvp|phase1|phase2|future"
    }
  ],
  "roadmap": {
    "phase0_foundation": ["FEAT-001", "FEAT-002"],
    "phase1_mvp": ["FEAT-003", "FEAT-004"],
    "phase2_enhancement": ["FEAT-005", "FEAT-006"],
    "phase3_expansion": ["FEAT-007", "FEAT-008"]
  },
  "scope_boundaries": {
    "in_scope": [
      "Core functionality description",
      "Essential user workflows"
    ],
    "out_of_scope": [
      "Advanced features deferred",
      "Future integrations"
    ]
  },
  "risks": [
    {
      "id": "RISK-001",
      "priority": "high|medium|low",
      "description": "Risk description",
      "impact": "Impact on scope",
      "mitigation": "Mitigation strategy"
    }
  ],
  "success_criteria": {
    "mvp_launch": [
      "User adoption target",
      "Business value metric"
    ],
    "enhancement_phase": [
      "Performance threshold",
      "Feature usage metric"
    ]
  },
  "traceability": [
    {
      "feature_id": "FEAT-001",
      "source_requirements": ["REQ-001", "REQ-003"],
      "justification": "Traceability explanation"
    }
  ]
}
```
