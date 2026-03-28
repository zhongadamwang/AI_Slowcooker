<!-- Identifier: V-01 -->

# Skill Development Process Vocabulary

## Canonical Terms and Definitions

### Core Concepts

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Skill** | A measurable capability required for effective job performance | Competency, Ability | Must be observable and assessable |
| **AI Agent Skill** | AI-enabled capability that automates or enhances development tasks | AI Skill, Automation Capability | Specialization of Skill with AI-specific attributes |
| **Skill Framework** | Structured competency model organizing related skills | Competency Framework, Skill Model | Organizes multiple related skills into coherent structure |
| **Skill Profile** | Documented record of individual's current and target skills | Competency Profile, Skill Matrix | Updated regularly through assessments |
| **Learning Path** | Structured sequence of activities to develop a specific skill | Development Plan, Learning Journey | Customized to individual needs and roles |
| **Skill Gap** | Difference between current and required skill levels | Development Need, Capability Gap | Basis for prioritizing learning efforts |
| **Proficiency Level** | Degree of skill mastery demonstrated by individual | Skill Level, Competency Level | Standardized across organization |

### Process Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Skills Assessment** | Systematic evaluation of current skill levels | Competency Evaluation, Skill Audit | Uses standardized criteria and methods |
| **Skill Validation** | Verification that skill has been successfully acquired | Competency Verification, Skill Certification | Requires demonstration in practice |
| **Knowledge Transfer** | Process of sharing expertise between individuals | Knowledge Sharing, Skill Transfer | Critical for organizational learning |
| **Mentoring** | One-on-one guidance relationship for skill development | Coaching, Skill Guidance | Pairs experienced with developing practitioners |
| **Learning Activity** | Specific action taken to develop skills | Training Activity, Development Exercise | Can be formal or informal |
| **Requirements Ingest** | Process of normalizing requirements from various formats into consistent, chunked representation with traceability | Requirements Processing, Requirements Import | Project-specific process for requirements management |
| **Requirements Merge** | Process of combining multiple requirement documents into a single coherent specification with conflict resolution | Requirements Consolidation, Spec Merge | `requirements-merge` skill; maintains source traceability across all merged requirements |
| **Change Management** | Systematic approach to tracking, documenting, and managing changes to requirements and project scope | Change Control, Change Tracking | Standard industry practice for project governance |
| **W5H Analysis** | Framework examining Who, What, When, Where, Why, and How aspects of requirements | Five W and H Analysis, Requirements Analysis Framework | Valuable analysis framework for comprehensive understanding |

### Roles and Responsibilities

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Skill Manager** | Person responsible for organizational skill development coordination | Learning Coordinator, Competency Manager | Central role in skill development ecosystem |
| **Project Owner** | Primary decision maker and change approver for the project | Project Manager, Product Owner | Has broader authority scope than Team Lead |
| **Subject Matter Expert (SME)** | Individual with deep expertise in specific domain | Domain Expert, Technical Lead | Resource for advanced skill development |
| **Learning Facilitator** | Person who guides group learning activities | Trainer, Instructor | Focuses on knowledge transfer and group dynamics |

### Evolutionary Development Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Evolutionary Development** | Adaptive development methodology that evolves requirements and solutions iteratively based on feedback | Iterative Development, Adaptive Methodology | Encompasses Adaptive Planning plus other iterative practices |
| **Adaptive Planning** | Planning approach that adjusts based on learning and feedback | Iterative Planning, Responsive Planning | Key skill for evolutionary development |
| **Continuous Integration** | Practice of regularly integrating and testing code changes | CI, Automated Integration | Technical skill for evolutionary development |
| **Feedback Loop** | System for collecting and incorporating stakeholder input | Response Cycle, Learning Loop | Process skill for evolutionary development |
| **Refactoring** | Restructuring code without changing external behavior | Code Improvement, Restructuring | Technical skill for maintaining evolving systems |

### AI Skills and Automation Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Skill Navigator** | Intelligent orchestration system that coordinates multiple AI skills | Workflow Orchestrator, Skill Coordinator | Meta-skill for managing skill ecosystem |
| **Natural Language Orchestration** | Capability to invoke and coordinate skills using conversational input | NL Workflow Control, Conversational Automation | Core feature of EDPS Skill Navigator |
| **Skill Registry** | Catalog of available AI skills with capabilities and metadata | Skill Catalog, Capability Index | Maintained by SkillNavigator for intelligent recommendations |
| **Workflow Template** | Predefined sequence of skills for common development patterns | Skill Chain, Process Template | Reusable patterns for efficient workflow execution |
| **Context Awareness** | System ability to consider project state and user history in recommendations | Situational Intelligence, Adaptive Guidance | Key capability for intelligent skill orchestration |
| **GitHub Issue Sync** | Bidirectional synchronization between local task markdown files and GitHub Issues | Issue Sync, Task-Issue Bridge | Enabled by `github-issue-create-update` and `github-issue-sync-status` skills |
| **Participant Stereotype** | Classification of diagram participants into exactly one of four roles: actor, boundary, control, or entity | UML Stereotype, Participant Type | Drives decomposition eligibility and message routing validation in hierarchical diagrams |
| **Box Boundary** | Mermaid `box ... end` syntax block grouping related participants under a named system boundary | Boundary Group, System Box | Actors must be declared outside all boxes; boundary participants must be listed first inside a box |
| **Boundary Validator** | Component enforcing four EDPS hierarchy rules run as a pre-render check after box syntax generation: VR-1 Single External Interface (error), VR-2 Boundary-First Reception (error), VR-3 Control-Only Decomposition (error), VR-4 Cohesive Responsibility (warning) | Hierarchy Validator, Stereotype Enforcer | Outputs machine-readable `boundary_validation_report` JSON and markdown summary table; supports strict (blocks on errors) and advisory (annotates inline) modes |
| **Skill Creator** | Framework for building and validating new EDPS skills following a standardized SKILL.md schema | Skill Scaffold, Skill Framework | `skill-creator` skill; ensures consistency across all skills in the ecosystem |

### Change Management Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|--------|
| **Change Classification** | Systematic categorization of changes by type, scope, and impact | Change Typing, Modification Classification | Enables proper workflow routing and approval processes |
| **Impact Assessment** | Analysis of change effects on stakeholders, processes, and systems | Change Impact Analysis, Effect Evaluation | Required for all significant organizational changes |
| **Reference Management** | Automated maintenance of cross-references and dependencies | Link Management, Dependency Tracking | Ensures organizational model consistency during evolution |
| **Incremental Requirement Updates** | Process for integrating new requirements without disrupting existing analysis | Progressive Requirements Integration, Delta Updates | Supports continuous evolution while maintaining traceability |

### Project Management Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|-------|
| **Project Document Management** | Skill for initializing and maintaining consistent project documentation folder structures | Doc Structure, Project Scaffold | `project-document-management` skill; creates hierarchical trees with requirements, artifacts, and org modeling docs |
| **Project Planning Tracking** | Skill for planning project phases, tracking milestones, and managing tasks using structured templates | Milestone Tracking, Phase Management | `project-planning-tracking` skill; integrates with document tree organization |
| **Project Status Reporting** | Skill for generating executive dashboards, status summaries, and stakeholder communications | Status Dashboard, Progress Report | `project-status-reporting` skill; auto-aggregates data from project documentation structure |

### Hierarchical Process Management Terms

| Term | Definition | Synonyms | Notes |
|------|------------|----------|-------|
| **Hierarchy Management** | Skill for decomposing control-type process participants into Level N+1 sub-process folders with stubs, cross-references, and metadata tracking | Process Decomposition, Sub-Process Management | `hierarchy-management` skill; enforces VR-3 control-only decomposition rule |
| **Process Node** | A single node in a hierarchical process tree representing one decomposed sub-process, with associated level, folder path, parent/child links, and complexity metrics | Hierarchy Node, Sub-Process Node | Stored in `hierarchy-metadata.json`; linked via breadcrumb trail and Sub-Processes table |
| **Process Decomposition** | The act of breaking a control-type participant in a collaboration diagram into a child sub-process diagram at Level N+1 | Decomposition, Sub-Process Creation | Requires control stereotype; produces stub documents and metadata node |
| **Breadcrumb Navigation** | Relative path chain from a Level N document back to all ancestor `main.md` files, enabling navigation up the hierarchy tree | Breadcrumb Trail, Ancestor Links | Injected into child `main.md`; rebuilt by hierarchy-management on every decomposition and link-integrity check |
| **Hierarchy Index** | Root-level `hierarchy-index.md` file with a flat breadth-first table and Mermaid `flowchart TD` of all process nodes in the hierarchy | Hierarchy Map, Process Tree Index | Auto-regenerated after every decomposition and rollback by `hierarchy-management` |
| **Complexity Metrics** | Per-node measurements — `interaction_count`, `participant_count`, `nesting_depth` — used to evaluate diagram complexity and trigger decomposition recommendations | Complexity Scores, Scale Metrics | Stored in `hierarchy-metadata.json` per ProcessNode; advisory warning at 80% of threshold, critical at threshold |
| **Decomposition Candidate** | A control-type participant whose `interaction_count` exceeds the configured `decomposition_candidate_min_interactions` threshold, flagged for decomposition | Decomposition Suggestion, High-Complexity Control | Identified during scale analysis after each decomposition; listed in `scale_management` aggregates |
| **EDPS Compliance** | Scored conformance assessment of a process hierarchy against 11 rules across three groups (Group A boundary rules, Group B hierarchy structural rules, Group C evolutionary principles) | Compliance Score, EDPS Conformance | `edps-compliance` skill; outputs score 0–100 with status COMPLIANT / MOSTLY_COMPLIANT / NEEDS_IMPROVEMENT / NON_COMPLIANT |
| **Compliance Group** | A categorized set of rules within EDPS compliance: Group A (boundary diagram rules, delegated), Group B (hierarchy structural rules, partially delegated), Group C (evolutionary principle rules, native) | Rule Group, Compliance Category | Group A delegated to `diagram-generatecollaboration`; Group B structural rules delegated to `hierarchy-validation` |
| **Hierarchy Validation** | Structural integrity check of process hierarchies across 14 rules: cross-level type consistency (HV), cross-reference integrity (HX), naming and structure compliance (HN) | Structure Validation, Hierarchy Check | `hierarchy-validation` skill; auto-fixes safe path/metadata issues; structural errors require human review |
| **Documentation Automation** | Skill for auto-generating level-calibrated `main.md`, `process.md`, `collaboration.md`, and `domain-model.md` documents from hierarchy metadata and parent diagram context | Doc Generation, Auto-Docs | `documentation-automation` skill; Level Content Guide calibrates scope by Level 0–3+; content guard prevents silent overwrites |
| **Level Content Guide** | Reference table in `documentation-automation` calibrating documentation scope, overview tone, and process detail depth for each hierarchy level (Level 0–3+) | Level Calibration, Depth Guide | Level 0 = system overview; Level 1 = subsystem detail; Level 2 = component flow; Level 3+ = operation-level detail |
| **Content Guard** | Pre-check in `documentation-automation` that detects manually-authored content exceeding 10 lines in a stub file and prompts before overwrite | Overwrite Guard, Stub Integrity Check | `--force` flag bypasses for confirmed intentional overwrite; prevents accidental loss of manually-authored content |
| **Migration Tools** | Non-destructive skill for upgrading flat collaboration diagrams to hierarchy-aware format with stereotypes and box boundaries | Legacy Migration, Diagram Upgrade | `migration-tools` skill; `--mode preview` shows changes; `--mode apply` writes enhanced output; originals never modified |
| **Change Impact Analysis** | Dependency-aware impact tracing for process hierarchy changes with 5-level risk classification and compatibility with `change-management` skill output format | Impact Tracing, Dependency Analysis | `change-impact-analysis` skill; `what-if` mode (default) previews; `apply` mode auto-repairs navigational artifacts |
| **Risk Level** | Five-level severity classification for change impact: NONE, LOW, MEDIUM, HIGH, CRITICAL; accompanied by `normalized_risk_level` (HIGH/MEDIUM/LOW) and `critical_flag` for `change-management` compatibility | Severity Level, Impact Severity | Output of `change-impact-analysis` skill; `critical_count` in summary enables quick filtering of highest-priority impacts |

## Naming Standards

### File Naming
- Process documents: Use lowercase with hyphens (e.g., `skill-assessment.md`)
- Test cases: Use format `tc-[identifier]-[sequence].md` (e.g., `tc-assess-001.md`)

### ID Formats
- Skill IDs: `SKILL-[Category]-[Number]` (e.g., `SKILL-TECH-001`)
- Learning Path IDs: `LP-[Skill]-[Version]` (e.g., `LP-ADAPT-v1.0`)
- Assessment IDs: `ASSESS-[Type]-[Date]-[ID]` (e.g., `ASSESS-INITIAL-20260207-001`)

## Abbreviations

| Abbreviation | Full Term | Usage Context |
|-------------|-----------|---------------|
| **SME** | Subject Matter Expert | Role identification |
| **LP** | Learning Path | Document references |
| **KT** | Knowledge Transfer | Activity planning |
| **CI/CD** | Continuous Integration/Continuous Deployment | Technical skills context |