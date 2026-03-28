# W5H Requirements Analysis

**Project**: 03-Building-Skills-Iteration-2  
**Source**: requirements.json, goals.json  
**Generated**: 2026-03-14T10:00:00Z  
**Analysis Framework**: Who, What, When, Where, Why, How

## WHO — Stakeholders and Roles

### Primary Stakeholders
- **AI Agent Developers**: Build and maintain skills that generate hierarchical collaboration diagrams with boundary concepts
- **Process Modelers**: Use enhanced skills to decompose complex organizational processes into hierarchical boundaries
- **EDPS Methodology Practitioners**: Ensure generated artifacts comply with evolutionary development principles

### Secondary Stakeholders
- **Project 1 Skill Users**: Existing users whose workflows must remain unbroken (backward compatibility)
- **OrgModel Maintainers**: Responsible for evolving organizational models with new hierarchical concepts
- **Quality Assurance**: Validate boundary detection accuracy, decomposition rule enforcement, and EDPS compliance

### Roles and Responsibilities

| Role | Responsibilities | Authority Level |
|------|-----------------|----------------|
| Skill Developer | Implement boundary detection, hierarchy management, and participant stereotyping | Developer |
| Process Architect | Define boundary patterns, validate decomposition rules, approve hierarchy structures | Decision Maker |
| OrgModel Owner | Approve organizational model updates with hierarchical boundary concepts | Approver |
| QA Engineer | Validate boundary accuracy, hierarchy depth, backward compatibility | Validator |
| End User (Developer) | Use enhanced skills to model processes hierarchically | Consumer |

## WHAT — Functional and Non-Functional Requirements

### Core Capabilities to Build

1. **Boundary-Enhanced Collaboration Diagrams** *(R-302, R-303, R-310)*
   - Extend `diagram-generatecollaboration` skill with Mermaid `box` syntax
   - Implement participant stereotype classification (actor, boundary, control, entity)
   - Enforce decomposition rules: only control-type participants decompose
   - Ensure boundary-type participants receive actor messages first

2. **Hierarchical Process Decomposition** *(R-301, R-304)*
   - Enable any control-type interaction to become a Level N+1 sub-process
   - Generate sub-folder structures with standard files (main.md, collaboration.md, process.md, domain-model.md)
   - Provide cross-reference navigation between hierarchy levels
   - Support unlimited depth (tested to 5+ levels)

3. **Scale and Complexity Management** *(R-305)*
   - Level 0: 3-7 main interactions per diagram
   - Level N: 5-12 steps maximum per sub-process
   - Automatic complexity detection and decomposition suggestions
   - Warnings for overly complex single-level diagrams

4. **EDPS Compliance Validation** *(R-306)*
   - Validate evolutionary development principles in all artifacts
   - Change impact analysis across hierarchy levels
   - Requirements traceability to process levels
   - Incremental model refinement support

5. **OrgModel Enhancement** *(R-308, R-309a)*
   - Update organizational process documents with boundary concepts
   - Enhance organizational collaboration diagrams with box syntax
   - Integrate boundary patterns into domain models
   - Create organizational templates for hierarchical modeling

6. **Backward Compatibility & Migration** *(R-309b)*
   - Import Project 1 diagrams without modification
   - Migration tools to convert flat diagrams to hierarchical format
   - Preserve all existing requirement links and metadata
   - Zero breaking changes to existing skill interfaces

### Non-Functional Requirements
- **Performance**: ≤30 second diagram generation time *(TC-301)*
- **Integration**: Seamless VS Code and GitHub Copilot integration *(TC-302)*
- **Usability**: Developer adoption >90%, productive within 2 hours of training
- **Quality**: >95% test coverage for new functionality

## WHEN — Timeline and Sequencing

### Phase Schedule

| Phase | Timeline | Duration | Key Deliverables |
|-------|----------|----------|-----------------|
| Phase 1: Foundation Enhancement | Weeks 2-4 (March 2026) | 2-3 weeks | Boundary-enhanced collaboration skill, participant stereotypes |
| Phase 2: Hierarchy Management | Weeks 5-7 (April 2026) | 2-3 weeks | Hierarchy management skill, sub-folder generation, cross-references |
| Phase 3: EDPS Compliance | Weeks 8-9 (April-May 2026) | 2 weeks | Compliance checking, validation tools, change impact analysis |
| Phase 4: Migration & Integration | Weeks 10-12 (May 2026) | 1-2 weeks | Migration tools, OrgModel update, performance testing, documentation |

### Critical Dependencies (Sequencing)
1. Phase 1 must complete before Phase 2 (boundary support needed for hierarchy)
2. Phases 2-3 can partially overlap (compliance checking can begin while hierarchy completes)
3. Phase 4 depends on all prior phases (migration requires complete feature set)
4. OrgModel update (T15) depends on all skill implementations (T1-T14)

### Milestones
- **M1** (End Week 4): Boundary-enhanced diagrams generating correctly with participant stereotypes
- **M2** (End Week 7): Full hierarchy management with sub-folder generation and navigation
- **M3** (End Week 9): EDPS compliance validation passing all test cases
- **M4** (End Week 12): Project 1 migration complete, OrgModel updated, documentation delivered

## WHERE — Implementation Context

### Technical Environment
- **Primary Platform**: VS Code with GitHub Copilot integration
- **Diagram Rendering**: Mermaid sequence diagrams with `box` syntax
- **Document Format**: Markdown files with embedded Mermaid and JSON metadata
- **File System**: Hierarchical folder structures within OrgDocument project tree

### Artifact Locations

| Artifact Type | Location Pattern |
|--------------|-----------------|
| Skill definitions | `.github/skills/{skill-name}/SKILL.md` |
| Process diagrams | `OrgDocument/orgModel/{process}/collaboration.md` |
| Domain models | `OrgDocument/orgModel/{process}/domain-model.md` |
| Project artifacts | `OrgDocument/projects/03 - Building Skills Iteration 2/artifacts/` |
| Task files | `OrgDocument/projects/03 - Building Skills Iteration 2/tasks/` |
| Generated hierarchies | `OrgDocument/orgModel/{process}/{sub-process}/` |

### Skill Enhancement Targets

| Skill | Enhancement | Impact |
|-------|------------|--------|
| `diagram-generatecollaboration` | Add boundary detection, box syntax, participant stereotypes | Primary — 40% effort |
| New: `hierarchy-management` | Process decomposition, folder generation, cross-references | New skill — 20% effort |
| New: `boundary-validation` | EDPS compliance checking, boundary rule validation | New skill — 15% effort |
| `orgmodel-update` | Enhance with hierarchical boundary support | Enhancement — 15% effort |
| New: `migration-tools` | Project 1 diagram conversion utilities | New skill — 10% effort |

## WHY — Business Justification

### Problem Being Solved
Project 1 skills produce single-level, flat collaboration diagrams that cannot represent complex multi-component systems. This forces modelers to create oversized, unreadable diagrams or lose important detail. The lack of hierarchy violates EDPS methodology which requires evolutionary process decomposition.

### Business Value

1. **Complexity Management**: Break large systems into navigable process hierarchies *(R-301)*
2. **EDPS Methodology Alignment**: Fulfill organizational commitment to evolutionary development *(R-306)*
3. **Scalable Modeling**: Handle unlimited system complexity through progressive decomposition *(R-305)*
4. **Knowledge Organization**: Structured folder hierarchies make process knowledge discoverable *(R-304)*
5. **Change Impact Analysis**: Understand how changes propagate across process levels *(R-306)*
6. **Organizational Evolution**: OrgModel reflects actual methodology capabilities *(R-308)*

### Risk of Not Implementing
- Inability to model complex organizational processes effectively
- EDPS methodology compliance gap
- Limited scalability of AI-assisted process modeling
- Inconsistency between organizational methodology and tool capabilities

## HOW — Implementation Approach

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│           Enhanced diagram-generatecollaboration         │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │  Boundary     │ │ Participant  │ │ Mermaid Box     │ │
│  │  Detection    │ │ Stereotype   │ │ Syntax Gen      │ │
│  │  Engine       │ │ Classifier   │ │                 │ │
│  └──────────────┘ └──────────────┘ └─────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              hierarchy-management (NEW)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │  Process      │ │ Sub-Folder   │ │ Cross-Reference │ │
│  │  Decomposer   │ │ Generator    │ │ Navigator       │ │
│  └──────────────┘ └──────────────┘ └─────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              boundary-validation (NEW)                    │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│  │  EDPS         │ │ Hierarchy    │ │ Change Impact   │ │
│  │  Compliance   │ │ Validator    │ │ Analyzer        │ │
│  └──────────────┘ └──────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Implementation Strategy

1. **Extend, Don't Replace**: Enhance existing `diagram-generatecollaboration` skill by adding boundary capabilities while preserving all existing features
2. **New Skills for New Concepts**: Create dedicated skills for hierarchy management and boundary validation
3. **Participant-Type-Driven Design**: Use participant stereotypes as the central organizing principle for all decomposition decisions
4. **Folder-as-Hierarchy**: Map process hierarchy directly to folder structure for intuitive navigation
5. **Incremental Migration**: Provide optional migration path — Project 1 diagrams continue to work without modification

### Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Boundary syntax | Mermaid `box` | Only viable option for grouping in Mermaid sequence diagrams |
| Participant types | `@{ "type" : "..." }` annotations | Mermaid-native participant metadata syntax |
| Decomposition trigger | Control-type only | EDPS methodology alignment; prevents over-decomposition |
| Folder naming | `NN-BoundaryName/` format | Consistent with existing OrgModel conventions |
| Migration approach | Opt-in enhancement | Preserves backward compatibility while enabling gradual adoption |
