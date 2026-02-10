# Project Glossary - 01 Building Skills

**Generated**: 2026-02-10T00:00:00Z  
**Source**: Requirements analysis of 11 project documents  
**Usage**: Domain terminology for AI Agent Skills development

## Technical Infrastructure Terms

### AI Agent Skills
Modular AI capabilities that can be invoked through VS Code/Claude Code to automate software development processes from requirements to delivery.

### VS Code
Visual Studio Code - The primary development environment where AI skills are integrated and executed.

### Claude Code  
AI coding assistant integration within VS Code that provides the runtime environment for AI skills.

### Markdown Processing
The standardized approach where all skill inputs and outputs are in Markdown format for compatibility and human readability.

### GitHub Agent Skills Standard
Framework providing integration patterns for AI skills in GitHub-based development workflows.

### skill-creator
Existing skills framework used as the foundation instead of developing a custom framework.

## Requirements Engineering Terms

### Requirements Ingest
The process of normalizing requirements from various formats into consistent, chunked representation with traceability.

### Atomic Requirements
Requirements broken down into single, verifiable units typically under 400 tokens for optimal LLM processing.

### Confidence Score
Numerical rating (0.0-1.0) indicating the certainty level of requirement extraction and classification.

### Schema Validation
Process ensuring requirements conform to defined data structures and formatting standards.

### Requirements Engineering
Systematic approach to gathering, analyzing, documenting, and managing requirements throughout development.

## Domain Modeling Terms

### Domain Model
Conceptual model capturing the key entities, relationships, and behaviors within a specific problem domain.

### Business Entities
Core objects in the business domain that have identity, attributes, and behaviors (e.g., User, Order, Product).

### W5H Framework
Analysis methodology examining Who, What, When, Where, Why, and How aspects of requirements.

### OrgModel
Organizational model documenting processes, roles, and structures within the development organization.

## Process and Workflow Terms

### Evolutionary Development
Development approach that adapts and evolves requirements and solutions iteratively based on learned feedback.

### Change Management
Systematic approach to tracking, documenting, and managing changes to requirements and project scope.

### Traceability
Ability to track relationships between requirements, design elements, code, and test cases throughout the development lifecycle.

### Audit Trail
Historical record of all changes, decisions, and evolution in project requirements and scope.

### Stakeholder Engagement
Process of identifying, communicating with, and managing expectations of all parties affected by the project.

## Diagramming and Visualization Terms

### Collaboration Diagram
Visual representation showing how actors and systems interact to accomplish business goals.

### Sequence Diagram
Time-ordered diagram showing message exchanges between participants in a process or use case.

### Mermaid
Markdown-compatible diagramming language for creating flowcharts, sequence diagrams, and other visualizations.

### PlantUML
Text-based diagramming tool for creating UML diagrams from simple textual descriptions.

## Project Planning Terms

### PERT
Program Evaluation and Review Technique - Project management method using optimistic, most likely, and pessimistic time estimates.

### DAG (Directed Acyclic Graph)
Mathematical structure representing task dependencies where tasks flow in one direction without circular dependencies.

### Critical Path
The longest sequence of dependent tasks that determines the minimum project duration.

### Task Planning
Process of breaking down project work into manageable tasks with dependencies, estimates, and schedules.

### Project Estimation
Process of predicting the effort, duration, and resources required to complete project tasks.

## Development Process Terms

### Continuous Integration
Development practice where code changes are automatically built, tested, and integrated frequently.

### Version Control
System for tracking and managing changes to code and documents throughout the development process.

### Scope Management
Process of defining, controlling, and managing what is included and excluded from the project.

### Template System
Standardized document structures that ensure consistency in project documentation and change management.

### Reference Management  
System for maintaining links and relationships between documents, requirements, and project artifacts.

## Change Management Specific Terms

### Change Tracking
Process of documenting and monitoring modifications to requirements, scope, or project plans.

### Change Types
Categories of modifications including requirement changes (REQ-CHG), additions (REQ-ADD), removals (REQ-REM), scope changes (SCOPE-CHG), and process changes (PROC-CHG).

### Change Template
Standardized format for documenting change requests with impact analysis, approval workflow, and implementation tracking.

### Impact Analysis
Assessment of how proposed changes affect existing requirements, tasks, schedules, and project components.

### Change Workflow
Defined process for proposing, reviewing, approving, and implementing changes to project requirements.

## Process Mining Terms

### Process Mining
Technique for discovering, monitoring, and improving real processes by extracting knowledge from event logs.

### Process Catalog
Repository of organizational business processes including workflows, procedures, and process models.

### Sub-process Nesting
Hierarchical organization of processes where high-level processes contain more detailed sub-processes.

### Process Depth
Measure of how many levels deep a process hierarchy extends from top-level to atomic activities.

---

## Usage Guidelines

### Terminology Consistency
- Use singular forms for entity names (User, not Users)
- Apply PascalCase for entity names (OrderItem, not order_item)  
- Use lower_snake_case for attributes (created_date, not CreatedDate)

### Acronym Handling
- Define acronyms on first use (PERT - Program Evaluation and Review Technique)
- Use consistently throughout project documentation
- Maintain acronym list for reference

### Term Evolution
- Update glossary when new terms emerge during development
- Flag deprecated terms when processes or tools change
- Maintain version history of term definitions

### Cross-Reference Integration
- Link glossary terms in requirements documents
- Reference terms in change management documentation  
- Ensure consistent usage across all project artifacts