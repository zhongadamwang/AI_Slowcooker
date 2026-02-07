---
name: goals-extract
description: Extract business goals, success criteria, constraints, KPIs, assumptions, and open questions from requirements input.
license: MIT
---

# Goals Extract Skill

## Intent
Derive the business goal, success criteria, constraints, and KPIs from requirements input.

## Inputs
- requirements[] (from requirements folder)

## Outputs
```json
{
  "goal_statement": "string",
  "success_criteria": ["string"],
  "kpis": ["string"],
  "constraints": ["string"],
  "assumptions": ["string"],
  "open_questions": ["string"]
}
```

## Tools
- LLM with goal extraction prompt
- Glossary lookup to normalize terms

## Prompt Stub
Summarize the business goal in one sentence. List success criteria, KPIs, constraints, assumptions, and open questions as bullet arrays.

## Quality
- Enforce SMART wording on KPIs where possible (target, unit, timeframe)

## Example Output
```json
{
  "goal_statement": "Enable efficient and accurate ingestion of requirements into the AI Slowcooker system to support downstream automation and analysis.",
  "success_criteria": [
    "All requirements are ingested without loss or misinterpretation.",
    "Ingestion process is completed within the defined time window.",
    "System supports traceability from ingested requirements to business objectives."
  ],
  "kpis": [
    "100% of requirements ingested per batch (unit: percent, timeframe: per ingestion cycle)",
    "Ingestion latency less than 5 minutes per batch (unit: minutes, timeframe: per batch)",
    "Zero critical errors in requirement mapping (unit: count, timeframe: monthly review)"
  ],
  "constraints": [
    "Input requirements must conform to the specified format.",
    "System must operate within existing infrastructure and security policies.",
    "No manual intervention allowed during ingestion."
  ],
  "assumptions": [
    "Requirements provided are complete and up-to-date.",
    "Glossary terms are available for normalization.",
    "Downstream systems are ready to consume ingested data."
  ],
  "open_questions": [
    "What is the process for handling ambiguous or conflicting requirements?",
    "How will updates to requirements be managed post-ingestion?",
    "Are there scalability limits for batch size or frequency?"
  ]
}
```
