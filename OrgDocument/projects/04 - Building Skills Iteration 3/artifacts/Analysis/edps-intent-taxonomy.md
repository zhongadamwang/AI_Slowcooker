# EDPS Intent Taxonomy and Classification Patterns

**Document Version**: 1.0.0  
**Last Updated**: March 17, 2026  
**Related Task**: T09 - Enhanced User Prompt Pattern Recognition  
**Classification Accuracy Target**: ≥95%

## Overview

This document defines the comprehensive mapping between natural language user prompts and EDPS skills or workflow archetypes. It serves as the authoritative reference for the enhanced classification engine in the edps-skill-navigator.

## Classification Architecture

### Intent Categories

1. **Single-Skill Intent**: User wants to execute one specific EDPS skill
2. **Workflow Archetype Intent**: User wants to execute a complete EDPS workflow
3. **Multi-Step Intent**: User describes a sequence that maps to workflow archetype
4. **Navigation Intent**: User wants guidance on what to do next
5. **Clarification Intent**: User is responding to disambiguation questions

### Confidence Thresholds

| Confidence Range | Action | User Experience |
|-----------------|--------|-----------------|
| ≥95% | Direct execution with explanation | "🎯 Executing: [skill]" |
| 85-94% | Execute with confidence note | "🎯 Executing: [skill] (89% confidence)" |
| 65-84% | Execute with alternatives | "🎯 Executing: [skill]. Did you mean: [alt]?" |
| 50-64% | Disambiguation required | "❓ I found several matches: [options]" |
| <50% | Clarification request | "❓ Could you rephrase? Try: [suggestions]" |

### Disambiguation Logic

```
If top_confidence >= 85%:
    execute_directly()
Elif top_candidate_confidence - second_candidate_confidence <= 10%:
    request_disambiguation(top_3_candidates)
Elif top_confidence >= 65%:
    execute_with_warning(top_candidate, alternatives=next_2)
Else:
    request_clarification(all_candidates_above_30%)
```

## Single-Skill Intent Patterns

### Requirements Processing Skills

#### requirements-ingest
**Purpose**: Normalize and structure requirements documents  
**Primary Patterns**:
- "analyze requirements", "process requirements", "ingest requirements"
- "normalize requirements", "structure requirements", "parse requirements"  
- "review requirements", "organize requirements"

**Context Indicators**:
- "requirements document", "user stories", "specification"
- "functional requirements", "business requirements", "non-functional"
- "requirement", "spec", "specification"

**Action Words**: process, analyze, ingest, normalize, structure, parse, review, organize

**Example Prompts** (High Confidence):
- "I need to process my requirements document" (97%)
- "Help me analyze these requirements" (93%) 
- "Can you ingest my specification?" (89%)

**Example Prompts** (Medium Confidence):
- "Review this document" (72% - could be requirements-ingest or other)
- "Process this file" (68% - needs context)

---

#### goals-extract  
**Purpose**: Extract business goals and success criteria  
**Primary Patterns**:
- "extract goals", "identify objectives", "find success criteria"
- "business goals", "success metrics", "objectives"
- "extract objectives", "identify goals"

**Context Indicators**:
- "goals", "objectives", "success criteria", "KPIs"
- "business objectives", "success metrics", "outcomes"
- "targets", "measures"

**Action Words**: extract, identify, find, discover, determine

**Example Prompts** (High Confidence):
- "Extract the business goals from my requirements" (96%)
- "What are the success criteria?" (91%)
- "Identify project objectives" (88%)

---

### Domain Analysis Skills

#### domain-extractconcepts
**Purpose**: Identify key business entities and domain concepts  
**Primary Patterns**:
- "extract domain concepts", "identify entities", "find domain model"
- "business entities", "domain analysis", "conceptual model"
- "domain concepts", "business concepts"

**Context Indicators**:
- "domain", "entities", "business concepts", "terminology"
- "vocabulary", "concepts", "model elements", "business model"
- "conceptual", "entity relationship"

**Action Words**: extract, identify, find, discover, analyze, model

**Example Prompts** (High Confidence):
- "Extract domain concepts from my requirements" (94%)
- "Identify the business entities" (92%)
- "What are the key domain concepts?" (89%)

**Disambiguation Examples**:
- "Analyze my domain" → Could be domain-extractconcepts (72%) or domain-alignentities (68%)

---

### Visualization Skills

#### diagram-generatecollaboration
**Purpose**: Create Mermaid collaboration diagrams with boundary support  
**Primary Patterns**:
- "create diagrams", "generate collaboration", "sequence diagram"
- "interaction diagram", "collaboration diagram", "system diagram"
- "visualize interactions", "create mermaid diagram"

**Context Indicators**: 
- "diagram", "visualization", "interaction", "collaboration"
- "sequence", "participants", "boundaries", "mermaid"
- "visual", "chart", "flow"

**Action Words**: create, generate, draw, visualize, diagram, show

**Example Prompts** (High Confidence):
- "Create collaboration diagrams" (96%)
- "Generate interaction diagrams" (93%)
- "I need a sequence diagram" (90%)

**Multi-Step Detection**:
- "Create diagrams and then decompose them" → standard_workflow (87%)

---

### Planning Skills

#### plan-derivetasks
**Purpose**: Convert requirements into actionable development tasks  
**Primary Patterns**:
- "create tasks", "derive tasks", "task planning", "break down work"
- "create task list", "plan tasks", "identify activities"
- "task breakdown", "work breakdown"

**Context Indicators**:
- "tasks", "work items", "activities", "deliverables"
- "action items", "task breakdown", "work packages"
- "to-do", "checklist"

**Action Words**: create, derive, plan, break down, identify, define

**Example Prompts** (High Confidence):
- "Create tasks from my requirements" (95%)
- "Break down the work into tasks" (92%)
- "Derive actionable tasks" (89%)

---

#### plan-estimateeffort
**Purpose**: Provide effort estimates for development tasks  
**Primary Patterns**:
- "estimate effort", "estimate time", "calculate effort"
- "time estimation", "effort analysis", "estimate duration"
- "sizing", "estimation"

**Context Indicators**:
- "effort", "time", "duration", "estimate", "hours", "days"
- "resources", "capacity", "workload"
- "estimation", "sizing", "planning"

**Action Words**: estimate, calculate, assess, analyze, size

**Example Prompts** (High Confidence):
- "Estimate effort for my tasks" (93%)
- "How long will this take?" (88%)
- "Calculate time estimates" (86%)

---

### Hierarchy Management Skills

#### hierarchy-management
**Purpose**: Decompose control-type participants into hierarchical sub-processes  
**Primary Patterns**:
- "decompose participant", "create hierarchy", "manage hierarchy"
- "sub-process", "decomposition", "hierarchical structure"
- "break down process", "nested processes"

**Context Indicators**:
- "hierarchy", "decompose", "sub-process", "levels"
- "parent-child", "control participant", "nested"
- "breakdown", "structure", "levels"

**Action Words**: decompose, create, manage, structure, organize, break down

**Example Prompts** (High Confidence):
- "Decompose this control participant" (91%)
- "Create process hierarchy" (88%)
- "Break down into sub-processes" (85%)

---

### Compliance Skills

#### edps-compliance
**Purpose**: Validate EDPS methodology compliance  
**Primary Patterns**:
- "check compliance", "validate EDPS", "compliance check"
- "methodology validation", "EDPS validation", "compliance audit"
- "validate methodology", "check standards"

**Context Indicators**:
- "compliance", "validation", "EDPS", "methodology"
- "rules", "standards", "requirements", "audit"
- "validate", "check", "verify"

**Action Words**: check, validate, verify, ensure, audit, assess

**Example Prompts** (High Confidence):
- "Check EDPS compliance" (98%)
- "Validate my methodology" (94%)
- "Run compliance check" (92%)

## Workflow Archetype Intent Patterns

### Standard Workflow
**Use Case**: Balanced quality and efficiency for typical EDPS projects  
**Primary Patterns**:
- "start EDPS project", "complete analysis", "full workflow"
- "comprehensive analysis", "standard process", "complete project"
- "analyze requirements and create diagrams", "full EDPS workflow"

**Multi-Step Indicators**:
- "and then", "followed by", "complete", "comprehensive"
- "full", "entire", "through", "end-to-end"

**Example Prompts** (High Confidence):
- "Start a complete EDPS project" (96%)
- "I need comprehensive requirements analysis" (92%)
- "Analyze requirements and create domain model" (89%)

### Rapid Workflow  
**Use Case**: Streamlined execution optimized for MVP and fast iteration  
**Primary Patterns**:
- "quick analysis", "fast track", "rapid development"  
- "MVP analysis", "quick start", "minimum viable"
- "streamlined process", "fast iteration"

**Context Indicators**:
- "quick", "fast", "rapid", "MVP", "minimum"
- "prototype", "fast track", "streamlined"
- "agile", "sprint", "iteration"

**Example Prompts** (High Confidence):
- "Quick analysis for MVP" (94%)
- "Fast track my requirements" (90%)
- "Rapid prototype analysis" (87%)

### Compliance Workflow
**Use Case**: Comprehensive analysis with full audit trail  
**Primary Patterns**:
- "full compliance", "audit ready", "complete documentation"
- "regulatory compliance", "audit preparation", "compliance review"
- "thorough analysis", "comprehensive audit"

**Context Indicators**:
- "compliance", "audit", "regulatory", "documentation"
- "full", "complete", "thorough", "comprehensive"
- "review", "validation", "verification"

**Example Prompts** (High Confidence):
- "Prepare for compliance audit" (97%)
- "Full documentation for regulatory review" (94%)
- "Comprehensive EDPS compliance check" (92%)

## Navigation Intent Patterns

### Project Guidance
**User wants to know what to do next**

**Primary Patterns**:
- "what should I do next", "what's the next step", "recommend next action"
- "what do you suggest", "guide me", "what now"

**Context Awareness Required**: Current project state, completed skills, available next steps

**Response Pattern**:
1. Analyze project state via T07 orchestrator
2. Identify available skills based on DAG prerequisites  
3. Recommend highest-value next step with rationale
4. Offer to execute recommended action

### Status Inquiry
**User wants to understand current progress**

**Primary Patterns**:
- "show progress", "project status", "where am I"
- "what's been completed", "current state"

**Integration**: Routes to T07 orchestrator status dashboard

## Session Learning Patterns

### Correction Capture
When user corrects a classification:

```
User: "Create requirements structure"
Navigator: requirements-ingest (87% confidence)
User: "No, I meant create tasks"
Navigator: "Thanks! Learning: 'create requirements structure' → plan-derivetasks"
```

### Pattern Adaptation
- Store correction in session memory: `session_corrections[original_prompt] = corrected_choice`
- Adjust confidence weights: boost corrected choice, reduce incorrect choice
- Apply learning to subsequent similar prompts within session

### Confidence Calibration
- Track disambiguation success rate
- Adjust thresholds based on user feedback patterns
- Optimize for minimal interruption while maintaining accuracy

## Quality Integration (T08)

### Gate-Informed Recommendations
```javascript
function getNextRecommendation(projectState, gateResults) {
  // Consider completed skills with quality scores
  const completedQuality = gateResults.average_quality_score;
  
  if (completedQuality < 0.80) {
    return {
      type: 'quality_improvement',
      message: 'Quality scores suggest reviewing recent outputs before proceeding',
      suggested_reviews: identifyLowQualitySkills(gateResults)
    };
  }
  
  // Standard next-step recommendation
  return getStandardRecommendation(projectState);
}
```

### Risk Detection
- Identify skills with consistently low gate scores
- Warn before recommending dependent skills
- Suggest quality improvement actions

---

This taxonomy serves as the foundation for ≥95% classification accuracy in the enhanced edps-skill-navigator T09 implementation.