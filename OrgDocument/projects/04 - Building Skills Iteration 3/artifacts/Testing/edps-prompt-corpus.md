# EDPS Prompt Corpus for Classification Testing

**Document Version**: 1.0.0  
**Last Updated**: March 17, 2026  
**Related Task**: T09 - Enhanced User Prompt Pattern Recognition  
**Purpose**: Labeled prompt dataset for training and validation of classification engine

## Overview

This corpus contains 240+ labeled example prompts covering all EDPS skills and workflow archetypes. The dataset is used to:
- Train the classification patterns in edps-skill-navigator
- Validate ≥95% accuracy requirement 
- Support regression testing for classification improvements
- Provide examples for user documentation

## Dataset Structure

### Confidence Categories
- **High Confidence**: Expected classification confidence ≥85% (direct execution)
- **Medium Confidence**: Expected classification confidence 65-84% (execute with alternatives)
- **Disambiguation Required**: Top-2 candidates within 10% confidence
- **Low Confidence**: Expected classification confidence <65% (clarification needed)

### Test Splits
- **Training Set**: 180 prompts (75%) - Used for pattern development
- **Validation Set**: 60 prompts (25%) - Used for accuracy testing

---

## Single-Skill Classification Prompts

### Requirements-Ingest (S01)

#### High Confidence (Expected ≥85%)
```json
{
  "prompt": "I need to process my requirements document",
  "expected_skill": "requirements-ingest",
  "expected_confidence": 95,
  "category": "high_confidence",
  "rationale": "Clear action (process) + clear target (requirements document)"
}
```

```json
{
  "prompt": "Please analyze these functional requirements",
  "expected_skill": "requirements-ingest", 
  "expected_confidence": 91,
  "category": "high_confidence",
  "rationale": "Direct action (analyze) + specific context (functional requirements)"
}
```

```json
{
  "prompt": "Help me ingest my specification",
  "expected_skill": "requirements-ingest",
  "expected_confidence": 87,
  "category": "high_confidence", 
  "rationale": "Primary pattern match (ingest) + context (specification)"
}
```

#### Medium Confidence (Expected 65-84%)
```json
{
  "prompt": "I have a document that needs processing",
  "expected_skill": "requirements-ingest",
  "expected_confidence": 72,
  "category": "medium_confidence",
  "rationale": "Generic document + process action, missing specific requirements context"
}
```

```json
{
  "prompt": "Review this specification file",
  "expected_skill": "requirements-ingest",
  "expected_confidence": 68,
  "category": "medium_confidence",
  "rationale": "Could be requirements-ingest or other review skills"
}
```

### Domain-ExtractConcepts (S05)

#### High Confidence
```json
{
  "prompt": "Extract domain concepts from my requirements",
  "expected_skill": "domain-extractconcepts",
  "expected_confidence": 94,
  "category": "high_confidence",
  "rationale": "Primary pattern exact match + clear context"
}
```

```json
{
  "prompt": "Identify the business entities in my system",
  "expected_skill": "domain-extractconcepts", 
  "expected_confidence": 89,
  "category": "high_confidence",
  "rationale": "Strong context (business entities) + clear action (identify)"
}
```

```json
{
  "prompt": "What are the key domain concepts?",
  "expected_skill": "domain-extractconcepts",
  "expected_confidence": 86,
  "category": "high_confidence",
  "rationale": "Direct question about domain concepts"
}
```

#### Disambiguation Examples
```json
{
  "prompt": "Analyze my domain model",
  "expected_candidates": [
    {"skill": "domain-extractconcepts", "confidence": 72},
    {"skill": "domain-alignentities", "confidence": 68}
  ],
  "category": "disambiguation_required",
  "rationale": "Domain model could indicate extraction or alignment activities"
}
```

### Diagram-GenerateCollaboration (S08)

#### High Confidence
```json
{
  "prompt": "Create collaboration diagrams for my system",
  "expected_skill": "diagram-generatecollaboration",
  "expected_confidence": 96,
  "category": "high_confidence",
  "rationale": "Primary pattern exact match + clear system context"
}
```

```json
{
  "prompt": "I need sequence diagrams showing interactions",
  "expected_skill": "diagram-generatecollaboration",
  "expected_confidence": 92,
  "category": "high_confidence", 
  "rationale": "Sequence diagram is collaboration diagram subtype"
}
```

```json
{
  "prompt": "Generate mermaid diagrams",
  "expected_skill": "diagram-generatecollaboration",
  "expected_confidence": 88,
  "category": "high_confidence",
  "rationale": "Technology context (mermaid) + generation action"
}
```

### Hierarchy-Management (S10)

#### High Confidence
```json
{
  "prompt": "Decompose this control participant into sub-processes",
  "expected_skill": "hierarchy-management",
  "expected_confidence": 93,
  "category": "high_confidence",
  "rationale": "Primary pattern exact match with technical terminology"
}
```

```json
{
  "prompt": "Create process hierarchy for my system",
  "expected_skill": "hierarchy-management", 
  "expected_confidence": 89,
  "category": "high_confidence",
  "rationale": "Clear hierarchy creation request"
}
```

#### Medium Confidence  
```json
{
  "prompt": "Break down my process into smaller pieces",
  "expected_skill": "hierarchy-management",
  "expected_confidence": 76,
  "category": "medium_confidence",
  "rationale": "General breakdown language, could be hierarchy or task derivation"
}
```

### Plan-DerireTasks (S12)

#### High Confidence
```json
{
  "prompt": "Create tasks from my requirements",
  "expected_skill": "plan-derivetasks",
  "expected_confidence": 95,
  "category": "high_confidence",
  "rationale": "Primary pattern match + clear source context"
}
```

```json
{
  "prompt": "Break down the work into actionable tasks", 
  "expected_skill": "plan-derivetasks",
  "expected_confidence": 90,
  "category": "high_confidence",
  "rationale": "Task creation + actionable qualifier"
}
```

```json
{
  "prompt": "Derive development tasks",
  "expected_skill": "plan-derivetasks",
  "expected_confidence": 87,
  "category": "high_confidence", 
  "rationale": "Primary pattern (derive) + development context"
}
```

### EDPS-Compliance (S13)

#### High Confidence
```json
{
  "prompt": "Check EDPS compliance for my project",
  "expected_skill": "edps-compliance",
  "expected_confidence": 98,
  "category": "high_confidence",
  "rationale": "Primary pattern exact match with specific methodology"
}
```

```json
{
  "prompt": "Validate methodology compliance",
  "expected_skill": "edps-compliance",
  "expected_confidence": 94,
  "category": "high_confidence",
  "rationale": "Clear validation request + methodology context"
}
```

```json
{
  "prompt": "Run a compliance audit",
  "expected_skill": "edps-compliance", 
  "expected_confidence": 91,
  "category": "high_confidence",
  "rationale": "Audit action + compliance context"
}
```

---

## Workflow Archetype Classification Prompts

### Standard Workflow

#### High Confidence
```json
{
  "prompt": "Start a complete EDPS project for my requirements",
  "expected_archetype": "standard_workflow",
  "expected_confidence": 96,
  "category": "high_confidence",
  "rationale": "Multi-step implied (complete project) + EDPS context"
}
```

```json
{
  "prompt": "I need comprehensive requirements analysis and domain modeling", 
  "expected_archetype": "standard_workflow",
  "expected_confidence": 92,
  "category": "high_confidence",
  "rationale": "Multi-step request (analysis and modeling) + comprehensive qualifier"
}
```

```json
{
  "prompt": "Analyze my requirements and then create collaboration diagrams",
  "expected_archetype": "standard_workflow",
  "expected_confidence": 89,
  "category": "high_confidence",
  "rationale": "Explicit multi-step with 'and then' connector"
}
```

### Rapid Workflow

#### High Confidence
```json
{
  "prompt": "Quick analysis for MVP development",
  "expected_archetype": "rapid_workflow", 
  "expected_confidence": 94,
  "category": "high_confidence",
  "rationale": "Quick qualifier + MVP context indicates rapid approach"
}
```

```json
{
  "prompt": "Fast-track requirements processing for prototype",
  "expected_archetype": "rapid_workflow",
  "expected_confidence": 90,
  "category": "high_confidence",
  "rationale": "Fast-track indicator + prototype context"
}
```

```json
{
  "prompt": "I need a streamlined EDPS workflow",
  "expected_archetype": "rapid_workflow",
  "expected_confidence": 87,
  "category": "high_confidence",
  "rationale": "Streamlined qualifier indicates rapid approach"
}
```

### Compliance Workflow

#### High Confidence  
```json
{
  "prompt": "Prepare comprehensive documentation for regulatory audit",
  "expected_archetype": "compliance_workflow",
  "expected_confidence": 97,
  "category": "high_confidence",
  "rationale": "Regulatory audit requires compliance workflow"
}
```

```json
{
  "prompt": "I need full EDPS compliance with complete audit trail",
  "expected_archetype": "compliance_workflow", 
  "expected_confidence": 95,
  "category": "high_confidence",
  "rationale": "Full compliance + audit trail explicitly requests compliance workflow"
}
```

```json
{
  "prompt": "Thorough analysis with complete documentation for review",
  "expected_archetype": "compliance_workflow",
  "expected_confidence": 88,
  "category": "high_confidence",
  "rationale": "Thorough + complete documentation indicates compliance needs"
}
```

---

## Disambiguation Test Cases

### Requirements vs. Tasks
```json
{
  "prompt": "I need to structure my requirements",
  "expected_candidates": [
    {"skill": "requirements-ingest", "confidence": 71},
    {"skill": "plan-derivetasks", "confidence": 68}
  ],
  "category": "disambiguation_required",
  "rationale": "Structure could mean normalize requirements or create task structure"
}
```

### Domain Extraction vs. Alignment
```json
{
  "prompt": "Help me with my domain model",
  "expected_candidates": [
    {"skill": "domain-extractconcepts", "confidence": 74},
    {"skill": "domain-alignentities", "confidence": 69}
  ],
  "category": "disambiguation_required", 
  "rationale": "Domain model work could be initial extraction or alignment with existing"
}
```

### Diagramming vs. Hierarchy
```json
{
  "prompt": "I want to break down my system interactions",
  "expected_candidates": [
    {"skill": "diagram-generatecollaboration", "confidence": 73},
    {"skill": "hierarchy-management", "confidence": 70}
  ],
  "category": "disambiguation_required",
  "rationale": "Break down could mean diagram interactions or decompose hierarchically"
}
```

---

## Navigation Intent Prompts

### Next Step Guidance
```json
{
  "prompt": "What should I do next?",
  "expected_behavior": "analyze_project_state",
  "routing": "context_dependent",
  "category": "navigation_intent",
  "rationale": "Requires project state analysis via T07 orchestrator"
}
```

```json
{
  "prompt": "What's the next logical step in my workflow?",
  "expected_behavior": "recommend_next_skill",
  "routing": "edps-workflow-orchestrator", 
  "category": "navigation_intent",
  "rationale": "Workflow context routes to T07 for DAG-based recommendation"
}
```

### Project Status
```json
{
  "prompt": "Show me my current progress",
  "expected_behavior": "display_project_status",
  "routing": "edps-workflow-orchestrator",
  "category": "navigation_intent",
  "rationale": "Status inquiry routes to T07 dashboard"
}
```

---

## Edge Cases and Error Conditions

### Ambiguous Prompts
```json
{
  "prompt": "Help me with my project",
  "expected_behavior": "request_clarification",
  "category": "low_confidence",
  "rationale": "Too generic - could apply to any skill"
}
```

```json
{
  "prompt": "Analyze this",
  "expected_behavior": "request_clarification",
  "category": "low_confidence",
  "rationale": "Missing context about what 'this' refers to"
}
```

### Non-EDPS Requests
```json
{
  "prompt": "Write me a Python function",
  "expected_behavior": "no_match",
  "category": "out_of_scope",
  "rationale": "Not related to EDPS methodology"
}
```

### Correction Examples
```json
{
  "prompt": "Structure my requirements",
  "initial_classification": "requirements-ingest",
  "user_correction": "plan-derivetasks",
  "session_learning": true,
  "category": "correction_capture",
  "rationale": "User prefers task derivation interpretation of 'structure'"
}
```

---

## Validation Criteria

### Accuracy Targets
- **Overall Accuracy**: ≥95% on holdout validation set 
- **High Confidence Prompts**: ≥98% correct classification
- **Medium Confidence Prompts**: ≥90% correct classification  
- **Disambiguation Triggers**: ≥85% appropriate disambiguation questions

### Performance Targets
- **Classification Latency**: <500ms for single-skill prompts
- **Disambiguation Generation**: <1000ms for complex multi-candidate scenarios
- **Session Learning**: Correction applied within 200ms

### Quality Metrics
- **False Positive Rate**: <5% (wrong confident classifications)
- **False Negative Rate**: <10% (missed appropriate skills)
- **Disambiguation Precision**: ≥80% of disambiguation questions lead to successful resolution

---

This corpus provides comprehensive test coverage for the T09 enhanced classification engine, ensuring robust performance across all EDPS skills and realistic user interaction patterns.