# EDPS Iteration 3 — User Guide: Phase 3 Capabilities

**Document**: T12-user-guide.md  
**Version**: 3.0.0  
**Date**: March 18, 2026  
**Audience**: EDPS practitioners, process analysts, project owners  

---

## What's New in Iteration 3

Iteration 3 adds three capabilities that make the EDPS skill ecosystem significantly easier to use:

| Capability | Benefit |
|-----------|---------|
| **Intelligent Workflow Orchestration** | Describe what you want in plain English — the system selects and runs the right sequence of skills automatically |
| **Quality Gates** | Validation checkpoints are automatically enforced at each workflow stage with plain-English failure explanations |
| **Enhanced Natural Language Understanding** | 94% intent accuracy — the system correctly interprets ambiguous or complex requests and recommends the right skills |

---

## Quick Start: Using the New Capabilities

### The Simplest Way — Just Describe Your Goal

You no longer need to know which skills to invoke. Just describe your goal:

```
"I need to analyze this requirements document and generate a collaboration diagram"
```

The system will:
1. Classify your intent (creation — diagram)
2. Recommend `requirements-ingest → domain-extractconcepts → diagram-generatecollaboration`
3. Execute the workflow with quality gates enforced automatically
4. Return validated outputs or plain-English guidance if a gate fails

### Quality Level Hints

Modify how thorough the execution is by adding quality language:

| Your language | What it activates |
|--------------|-------------------|
| "quick", "fast", "brief" | Expedited profile — minimal gates, fastest path |
| (nothing / default) | Standard profile — balanced quality and speed |
| "thorough", "comprehensive", "full" | High profile — all available quality gates |

**Examples**:
```
"Quick review of the requirements"              → expedited (1 gate, 3 skills)
"Analyze the requirements"                      → standard  (2 gates, 4–6 skills)
"Comprehensive end-to-end organizational model" → high      (4 gates, 10+ skills)
```

---

## Using the Workflow Orchestrator (T07)

### Available Workflow Patterns

| Pattern | When to use | Typical duration |
|---------|-------------|----------------|
| Fast-Track Analysis | Quick read of requirements or diagram | < 20 s |
| Requirements to Diagram | Create collaboration diagram from requirements | 30–60 s |
| Domain Modeling Workflow | Full org model from stakeholder requirements | 45–90 s |
| Validation Focus | Validate EDPS compliance of existing artifacts | 25–45 s |
| Process Integration | Integrate a new process into existing org model | 30–60 s |
| Change Management | Apply a change request to the org model | 20–40 s |
| End-to-End | Complete requirements through fully documented hierarchy | 90–300 s |

### Triggering a Specific Workflow

Simply describe the workflow by name or by what it produces:

```
"Run a validation-focus workflow on the collaboration diagram"
"Do an end-to-end analysis from requirements through documentation"
"Use the fast-track analysis workflow"
```

### Describing a Custom Workflow

You can also specify the exact steps you want as a numbered list:

```
"I need:
1. Ingest the requirements
2. Extract domain concepts
3. Align with existing organizational entities
4. Generate the collaboration diagram
5. Validate EDPS compliance"
```

The system parses each step, maps it to the correct skill, and executes in sequence (with safety gates inserted automatically).

### Modifying a Running Workflow

After a workflow has been selected, you can modify it in the same session:

```
"Add a hierarchy validation step before the documentation phase"
"Remove the domain alignment step"
"Make it more comprehensive"
"Move the compliance check to run before the diagram generation"
```

---

## Understanding Quality Gates (T08)

### What Quality Gates Do

Quality gates are validation checkpoints inserted automatically at key points in the workflow. They prevent bad data from propagating to later steps.

### Gate Results

At each gate, you will see one of three outcomes:

| Outcome | Meaning | Workflow continues? |
|---------|---------|-------------------|
| ✅ PASSED | Output meets quality threshold | Yes |
| ⚠️ WARNING | Minor issue detected, not blocking | Yes (with note) |
| ❌ FAILED | Required quality criteria not met | No — remediation provided |

### Reading a Gate Failure

When a gate fails, the output explains:
- **What failed**: plain English description of the problem
- **Why it matters**: how the failure affects downstream steps
- **How to fix it**: the specific skill(s) to invoke to resolve the issue

**Example gate failure output**:
```
Quality Gate: edps_vr_validation — FAILED

What failed: The collaboration diagram has two external actors (Customer and Admin)
both accessing the Order Processing boundary directly.

Why it matters: EDPS Boundary Rule VR-1 requires that exactly one external actor
interfaces with each boundary. Having two direct actors creates ambiguity in the
process model and will cause hierarchy validation to fail downstream.

How to fix it: Run the diagram-generatecollaboration skill again and ensure the
Admin actor is mediated through the boundary's control participant, not as a direct
external actor.

Skill to invoke: diagram-generatecollaboration
```

### Gate Profiles by Quality Level

| Profile | Gates included |
|---------|---------------|
| Light (expedited) | Output quality check only |
| Standard (default) | Output quality + Traceability completeness |
| Comprehensive (high) | Standard + EDPS VR validation + Hierarchy integrity |

---

## Using Enhanced NLP (T09)

### How the System Understands Your Requests

The NLP engine analyses your prompt across three dimensions simultaneously:

1. **Intent** — What do you want to do? (analysis, creation, validation, integration, planning, troubleshooting, documentation)
2. **Entities** — What are you working with? (boundary names, diagram levels, skill references, quality constraints)
3. **Context** — What's your project situation? (phase, quality level, urgency)

### Skill Recommendations

After analysing your prompt, the system recommends up to 5 skills ranked by relevance. Recommendations are shown with:
- **Skill name**
- **Why recommended** — which part of your request triggered this recommendation
- **Confidence score** — how confident the system is this is the right skill

### Session Context Memory

The NLP engine remembers context established earlier in your conversation:

```
Turn 1: "We're in the design phase working on a high-quality EDPS model"
         → System notes: phase=design, quality=high

Turn 2: "Now validate the hierarchy"
         → System applies high-quality gate profile automatically
         → No need to repeat "high quality" on every request
```

Context is retained for 30 minutes of inactivity, then reset.

### When the System Asks for Clarification

If your request is ambiguous (confidence < 70%), the system will ask at most 2 clarifying questions before proceeding with its best interpretation. For urgent requests, it will proceed on best interpretation without asking.

**Example**:
```
You: "Review everything"

System: "I can help with that. To give you the most relevant assistance:
1. What would you like me to review — requirements, a collaboration diagram, or the full hierarchy?
2. Should this be a quick check or a comprehensive review?"
```

---

## Common Use Case Prompts

### Requirements Analysis
```
"Analyze this requirements document for domain concepts and goals"
"Quick review of the requirements for EDPS compliance"
"What are the key goals in this stakeholder requirements document?"
```

### Creating EDPS Artifacts
```
"Create a collaboration diagram from these requirements"
"Generate a full EDPS organizational model for the payment processing system"
"Set up the project documentation hierarchy for Level 1 and Level 2"
```

### Validation
```
"Validate this hierarchy for EDPS compliance"
"Check VR-1 through VR-4 boundary rules in the collaboration diagram"
"Verify that traceability links are intact throughout the model"
```

### Integration & Change Management
```
"Integrate the new billing process into the existing organizational model"
"Apply change request CR-042: rename the Payment boundary"
"Merge the requirements from both source documents"
```

### Planning
```
"Derive tasks from the analyzed requirements"
"Estimate the effort for implementing this organizational model"
"Build a project schedule for the remaining work"
```

### Troubleshooting
```
"Why is the hierarchy validation failing?"
"Fix the VR-2 boundary violation in the collaboration diagram"
"Resolve the conflict detected in the requirements merge"
```

---

## Migration from Iteration 2

### What Changes for Existing Users

**Nothing breaks.** All 30 existing skills work exactly as before. The Iteration 3 enhancements are additive:

| If you used to... | You can now... |
|------------------|---------------|
| Invoke skills one by one | Let the orchestrator chain them automatically |
| Manually check outputs for quality | Let quality gates flag issues automatically |
| Specify exact skill names | Just describe your goal in plain English |

### Existing Prompt Patterns Still Work

All existing skill-based prompts from Iterations 1 and 2 continue to work unchanged. Iteration 3 simply adds the ability to use natural language instead.

```
// Iteration 1/2 style — still works
"Use the requirements-ingest skill to process this document"

// Iteration 3 style — also works
"Ingest and analyze this requirements document"
```

---

## Frequently Asked Questions

**Q: How do I know which workflow was selected?**  
A: The system displays the selected workflow pattern name and step list before execution begins.

**Q: Can I skip a quality gate?**  
A: Quality gates can be bypassed by specifying expedited quality level ("quick" / "fast"). This selects the light gate profile which has only one gate.

**Q: What if the system classifies my intent incorrectly?**  
A: If the wrong skills are recommended, simply clarify: "No, I meant to validate, not create." The learning system records the correction and improves future recommendations.

**Q: How do I provide feedback on recommendations?**  
A: Accepting or rejecting a recommended skill feeds back to the learning system automatically through the conversation interface.

**Q: Is my session context shared across conversations?**  
A: No. Session context resets between separate conversations (or after 30 minutes of inactivity).

**Q: Which skills are NOT invocable through the orchestrator?**  
A: `skill-creator` is not invocable as a workflow step — it is a meta-skill used to create new skills and must be invoked directly.
