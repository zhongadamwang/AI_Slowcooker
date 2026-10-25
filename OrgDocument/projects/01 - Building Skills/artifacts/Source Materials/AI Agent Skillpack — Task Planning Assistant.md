# AI Agent Skillpack — Task Planning Assistant

A modular set of AI "skills" for VS Code/Claude Code that automates your end‑to‑end approach to requirement analysis, system design, scoping, task derivation, and planning. These skills integrate with your development workflow through the VS Code environment.

## 0) High‑Level Architecture

Skills are designed for VS Code/Claude Code integration → process markdown documents → produce markdown artifacts → support developer workflow.

Core components

- Skills Framework: Individual AI skills that can be invoked through VS Code/Claude Code
- Markdown Processing: All inputs and outputs in markdown format
- Workspace Integration: Skills work within existing VS Code project structure
- Memory: Project-level context maintained through markdown artifacts

## 1) Skill Catalog (aligned to your outline)

Each skill includes: Intent • Inputs • Outputs (typed JSON) • Tools • Prompt stub • Steps • Quality checks.

### 1.1 Requirements.Ingest

Intent: Normalize markdown requirements into a consistent, chunked representation.

Inputs

- `markdown_content`: Markdown text content
- `source_file_path`: File path for traceability
- `project_id`: string

Outputs (Markdown)

```markdown
## Requirements Analysis Report

### Project: {project_id}
### Source: {source_file_path}

| ID | Section | Text | Tags | Confidence |
|----|---------|------|------|-----------|
| R-001 | ## Goals | System shall validate orders | functional, validation | high |
| R-002 | ## Constraints | Response time < 2s | performance, constraint | high |

### Glossary Suspects
- term1
- term2
```

Tools: Markdown parser, text chunking, classification.

Prompt stub (used only for classification/tagging if needed):



> Classify each requirement chunk into {assumption|constraint|functional|nonfunctional|out-of-scope}. Return JSON per schema.



Steps

1. Convert to text; retain location hints.
2. Split into atomic requirement chunks.
3. Tag chunk type; collect glossary suspects.

Quality: Ensure chunk granularity < 200 tokens; preserve traceability (`source_file`, `location_hint`).

### 1.2 Goals.Extract

Intent: Derive the business goal, success criteria, constraints, and KPIs.

Inputs: Requirements analysis markdown from 1.1.

Outputs (Markdown)

```markdown
## Goals & Objectives

### Goal Statement
{goal_statement}

### Success Criteria
- {success_criteria_1}
- {success_criteria_2}

### KPIs
- {kpi_1}
- {kpi_2}

### Constraints
- {constraint_1}
- {constraint_2}

### Assumptions
- {assumption_1}
- {assumption_2}

### Open Questions
- {question_1}
- {question_2}
```

Tools: LLM analysis, markdown generation.

Prompt stub:



> Summarize the business goal in one sentence. List success criteria, KPIs, constraints, assumptions, and open questions as bullet arrays.



Quality: Enforce SMART wording on KPIs where possible (target, unit, timeframe).

### 1.3 Process.W5H

Intent: Build the Who/What/When/Where/How map.

Inputs: `requirements[]`, `goal_statement`.

Outputs



```en-us
{
  "who": ["ActorA", "RoleB"],
  "what": ["CapabilityX", "EventY"],
  "when": ["TriggerZ", "SLA..."],
  "where": ["System1", "Channel2"],
  "how": ["BusinessRule1", "Algorithm2"],
  "rationale": "string"
}
```



Tools: LLM extraction, rules for de-duplication.

Prompt stub:



> Extract W5H with concise items; remove duplicates; return arrays only.



Quality: No synonyms across lists; ensure each `who` appears in `how` or `what` relations later.

### 1.4 Domain.ExtractConcepts

Intent: Identify Actors, Systems, Business Entities (with key attributes & verbs).

Inputs: `requirements[]`, W5H.

Outputs



```en-us
{
  "actors": [{"name":"string","description":"string"}],
  "systems": [{"name":"string","type":"internal|external","description":"string"}],
  "entities": [{
    "name":"string",
    "attributes":["string"],
    "verbs":["create|read|update|delete|transition"],
    "notes":"string"
  }]
}
```



Tools: NER, noun phrase mining, verb/object mining.

Quality: All entity names are singular, PascalCase; attributes are lower_snake_case.

### 1.5 Domain.AlignEntities

Intent: Map extracted concepts to the existing domain model; rename to canonical.

Inputs: Concepts from 1.4; existing ontology/domain model.

Outputs



```en-us
{
  "mappings": [
    {"from":"PurchaseOrder","to":"PO","match_score":0.92,"rationale":"string"}
  ],
  "unmapped": ["NewConcept1", "NewConcept2"],
  "conflicts": ["Order vs SalesOrder"]
}
```



Tools: Vector search over ontology; synonym dictionary; fuzzy matching.

Quality: No auto-merge if `match_score < 0.85`; flag for review.

### 1.6 Domain.ProposeNewConcepts

Intent: Define new concepts to avoid conflicts; propose names & definitions.

Inputs: `unmapped[]`, conflicts, context.

Outputs



```en-us
{
  "proposals": [
    {"name":"FulfillmentBatch","definition":"string","related":["Shipment"],"reasons":["string"]}
  ]
}
```



Quality: Check uniqueness vs ontology; names in PascalCase; definition ≤ 40 words.

### 1.7 Diagram.GenerateCollaboration

Intent: Produce a collaboration/sequence diagram from process flow & requirements.

Inputs: W5H, mapped actors/systems/entities, requirement references.

Outputs: Mermaid or PlantUML diagram text.

Rules

- New message ⇒ potential sub‑process; if no detail in requirements, do not decompose further.
- Every message must cite `R-ids` that justify it.

Mermaid template

sequenceDiagram

 autonumber

 participant A as {Actor/System}

 participant B as {Actor/System}

 Note over A,B: Goal: {{goal}}

 A->>B: {{Message}} [R-001,R-014]

Quality: Lint for orphan participants and cycles.

### 1.8 Process.ScopeMin

Intent: Define the minimum viable process scope and whether a master data model is needed.

Inputs: Collaboration diagram, domain mapping.

Outputs



```en-us
{
  "scope_statement":"string",
  "in_scope":["string"],
  "out_of_scope":["string"],
  "requires_master_data_model": true,
  "process_domain_model_stub": {"entities":["string"],"relations":["A->B"]}
}
```



Quality: Ensure scope items trace to requirement IDs.

### 1.9 Process.Merge

Intent: Merge new process with existing process catalog; detect sub-process nesting and depth.

Inputs: New process graph; existing BPMN/graph repo.

Outputs



```en-us
{
  "merged_graph":"graph_json_or_bpmn",
  "subprocesses_detected":[{"name":"X","depth":2}],
  "changes":[{"node":"Approve","action":"modified|added|removed","reason":"string"}]
}
```



Tools: Graph diff; similarity matching.

Quality: If step semantics match ≥ 0.9, prefer reuse over create.

### 1.10 Process.FindTopAndUpdate

Intent: Find the top node in merged graph; update process, collaboration, and domain-model diagrams.

Inputs: Merged graph; previous diagrams; domain model.

Outputs: Updated diagrams (Mermaid/PlantUML), traversal report.

Quality: No node with in-degree=0 except the true root; re‑render until invariant holds.

### 1.11 Plan.DeriveTasks

Intent: Identify tasks to modify/create processes and models; order by dependencies (bottom→top).

Inputs: Updated diagrams, diff report, scope.

Outputs



```en-us
{
  "tasks": [
    {
      "id":"T-001",
      "title":"Create API contract for SubmitOrder",
      "type":"process|data|system|test|infra",
      "depends_on":["T-000"],
      "artifacts":["/workspace/.../sequence.mmd"],
      "acceptance_criteria":["string"],
      "trace_to_requirements":["R-001","R-014"]
    }
  ],
  "dag": {"nodes":["T-001"],"edges":[["T-000","T-001"]]}
}
```



Quality: Every task must trace back to at least one requirement or diff item.

### 1.12 Plan.EstimateEffort

Intent: Estimate tasks using three‑point (PERT) and confidence.

Inputs: Tasks; historicals (optional velocity, cycle time).

Outputs



```en-us
{
  "estimates": [
    {
      "task_id":"T-001",
      "optimistic": 4,
      "most_likely": 8,
      "pessimistic": 14,
      "expected": 9.67,
      "std_dev": 1.67,
      "confidence":"medium",
      "assumptions":["string"],
      "risks":["string"]
    }
  ],
  "throughput_hint":"string"
}
```



Formulae

- `expected = (O + 4*M + P) / 6`
- `std_dev = (P - O) / 6`

Quality: Flag tasks with `std_dev/expected > 0.3` as risky.

### 1.13 Plan.BuildSchedule

Intent: Build a schedule (markdown format) using estimates + DAG.

Inputs: Estimates; DAG; resource constraints (optional); sprint length.

Outputs (Markdown)

```markdown
## Project Schedule

### Critical Path Analysis
- **Total Duration**: 45 days
- **Critical Path**: T-001 → T-003 → T-007 → T-012

### Task Schedule
| Task ID | Title | Start | Duration | Dependencies |
|---------|-------|-------|----------|-------------|
| T-001 | API Design | Day 1 | 3 days | - |
| T-002 | Database Schema | Day 1 | 2 days | - |

### Milestones
- [ ] Week 2: Core APIs complete
- [ ] Week 4: Integration testing
- [ ] Week 6: Production deployment
```

Quality: Respect dependencies; compute critical path; highlight resource conflicts.

## 2) Skill Usage Flow

1. `Requirements.Ingest` → 2) `Goals.Extract` → 3) `Process.W5H` → 4) `Domain.ExtractConcepts` → 5) `Domain.AlignEntities` → 6) `Domain.ProposeNewConcepts` (if needed) → 7) `Diagram.GenerateCollaboration` → 8) `Process.ScopeMin` → 9) `Process.Merge` → 10) `Process.FindTopAndUpdate` → 11) `Plan.DeriveTasks` → 12) `Plan.EstimateEffort` → 13) `Plan.BuildSchedule`.

Usage: Skills are invoked individually through VS Code/Claude Code interface. Each skill takes markdown input and produces markdown output. Developer can run skills sequentially or selectively based on needs.

## 3) Data Schemas (YAML)

### 3.1 Normalized Requirement



```en-us
- id: R-001
  source_file: SRS_v3.pdf
  location_hint: "p.3 para.2"
  text: "System shall validate order within 2s."
  tags: [functional, performance]
```



### 3.2 W5H



```en-us
who: [Customer, CSR, PaymentGateway]
what: [PlaceOrder, ValidatePayment]
when: [OnSubmit, OnTimeout2s]
where: [WebApp, MobileApp]
how: [Ruleset_ValidationV1, Retry3x]
```



### 3.3 Domain Mapping



```en-us
mappings:
  - from: PlaceOrder
    to: OrderSubmission
    match_score: 0.91
unmapped: [QuoteRevision]
conflicts: [Order vs SalesOrder]
```



### 3.4 Tasks DAG



```en-us
tasks:
  - id: T-001
    title: Create API contract for SubmitOrder
    type: process
    depends_on: []
    acceptance_criteria:
      - Contract published in repo
      - Approved by domain architect
    trace_to_requirements: [R-001, R-003]
dag:
  nodes: [T-001]
  edges: []
```



## 4) Prompt Templates (concise)

Domain.AlignEntities



```en-us
You are a domain librarian. Map the extracted concepts to the canonical domain model.
- Return JSON with fields: mappings[], unmapped[], conflicts[].
- Do not merge when match_score < 0.85. Provide rationale for each mapping.
```



Diagram.GenerateCollaboration



```en-us
Create a Mermaid sequence diagram from W5H and mapped actors/systems.
Rules:
- New message implies a potential sub-process; do not expand if no details in requirements.
- Each message annotates requirement IDs in square brackets.
Output only valid Mermaid code.
```



Plan.DeriveTasks



```en-us
From diffs and updated diagrams, list tasks required to implement changes.
- Include acceptance criteria and trace_to_requirements.
- Produce a DAG where edges point from prerequisite to dependent.
```



Plan.EstimateEffort



```en-us
Estimate using PERT (O, M, P). Return expected and std_dev. Flag high risk if std_dev/expected > 0.3. List assumptions and risks.
```



## 5) Implementation — VS Code Skills

> Skills will be implemented as Claude Code / VS Code compatible functions that process markdown input and produce markdown output.

### Skill Structure
Each skill follows this pattern:
- **Input**: Markdown content + context
- **Processing**: LLM analysis with specific prompts
- **Output**: Structured markdown document  
- **Integration**: Works within VS Code workspace

### Example Skill Implementation

```markdown
<!-- Skill: Requirements.Ingest -->
<!-- Input: Raw requirements markdown -->
<!-- Output: Structured requirements analysis -->

## Requirements Analysis Report

### Project: {project_id}
### Source: {source_file_path}

[Structured table with requirement IDs, text, tags, confidence]
```

### Skill Invocation
Skills are invoked through VS Code interface:
- Input: Current markdown document or selection
- Context: Project workspace and domain knowledge 
- Output: New markdown document or updated content



## 6) Skills & Artifacts

- Markdown Documents: All inputs and outputs in markdown format for easy editing and version control
- Mermaid Diagrams: Embedded in markdown for sequence and flow diagrams  
- Traceability: Requirement IDs maintained throughout all artifacts
- VS Code Integration: Skills work within existing project structure

## 7) Governance, Quality & Safety

- Traceability: Every diagram edge and task cites requirement IDs.
- Naming: Canonicalize via ontology; prohibit duplicates.
- Confidence: Thresholds to trigger human‑in‑the‑loop.
- PII/Secrets: Redact before indexing; store embeddings securely.
- Versioning: Keep `vN` for diagrams and JSON artifacts per run.

## 8) What I need from you to tailor the build

1. VS Code skill implementation approach: Claude Code integration method
2. Domain model location: markdown files, YAML, or JSON format
3. Existing process catalog: markdown documentation location
4. Sample requirement markdown: 1–2 files to test the skills
5. Workspace structure: preferred folder organization for artifacts

## 9) Next step

Share the above items (even rough stubs are fine). I'll create the skill definitions and templates that:

- Process your sample markdown requirements
- Produce W5H analysis + collaboration diagram (Mermaid)
- Derive a task list with dependency mapping
- Generate PERT estimates and basic schedule in markdown

We can then refine each skill's prompts and outputs until they match your exact workflow and integrate seamlessly with VS Code.