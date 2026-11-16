# Goals Extract — Worked Example

A complete `goals.json` and `goals.md` for a small requirements set. The optional per-item fields (`extraction_method`, `outcome_verb`, `target_value`, `timeframe`) are shown here.

### JSON Format
```json
{
  "goal_statement": "Reduce requirements processing time by 75% within 6 months while maintaining 99% accuracy.",
  "success_criteria": [
    {
      "criteria": "Achieve 75% reduction in processing time compared to current baseline.",
      "source_refs": ["REQ-001:2.1"],
      "extraction_method": "pattern_match",
      "outcome_verb": "reduce"
    },
    {
      "criteria": "Maintain 99% accuracy rate for all processed requirements.",
      "source_refs": ["REQ-002:3.1"],
      "extraction_method": "pattern_match", 
      "outcome_verb": "maintain"
    },
    {
      "criteria": "Complete implementation within 6 months of project start.",
      "source_refs": ["REQ-001:4.2"],
      "extraction_method": "temporal_pattern",
      "outcome_verb": "complete"
    }
  ],
  "kpis": [
    {
      "kpi": "Processing time: < 2.5 minutes per batch (75% reduction from 10 minutes baseline)",
      "source_refs": ["REQ-002:2.3"],
      "extraction_method": "pattern_match",
      "outcome_verb": "reduce",
      "target_value": "75%",
      "timeframe": "per batch"
    },
    {
      "kpi": "Accuracy rate: ≥ 99% (unit: percent, timeframe: daily)",
      "source_refs": ["REQ-002:3.1"],
      "extraction_method": "pattern_match",
      "outcome_verb": "maintain",
      "target_value": "99%",
      "timeframe": "daily"
    }
  ],
  "constraints": [
    {
      "constraint": "Input requirements must conform to the specified format.",
      "source_refs": ["REQ-001:1.1"]
    },
    {
      "constraint": "System must operate within existing infrastructure and security policies.",
      "source_refs": ["REQ-004:1.1"]
    },
    {
      "constraint": "No manual intervention allowed during ingestion.",
      "source_refs": ["REQ-002:2.5"]
    }
  ],
  "assumptions": [
    {
      "assumption": "Requirements provided are complete and up-to-date.",
      "source_refs": ["REQ-001:assumptions"]
    },
    {
      "assumption": "Glossary terms are available for normalization.",
      "source_refs": ["REQ-003:2.1"]
    },
    {
      "assumption": "Downstream systems are ready to consume ingested data.",
      "source_refs": ["REQ-004:3.2"]
    }
  ],
  "open_questions": [
    {
      "question": "What is the process for handling ambiguous or conflicting requirements?",
      "source_refs": ["REQ-001:notes"]
    },
    {
      "question": "How will updates to requirements be managed post-ingestion?",
      "source_refs": ["REQ-002:future_considerations"]
    },
    {
      "question": "Are there scalability limits for batch size or frequency?",
      "source_refs": ["REQ-002:performance"]
    }
  ],
  "traceability": {
    "source_requirements": ["REQ-001", "REQ-002", "REQ-003", "REQ-004"],
    "extraction_timestamp": "2026-02-08T10:30:00Z",
    "confidence_scores": {
      "goal_statement": "0.95",
      "overall": "0.87",
      "pattern_precision": "0.92",
      "outcome_focus_score": "0.89"
    }
  }
}
```

### Markdown Format
```markdown
# Goals Analysis

## Business Goal
Reduce requirements processing time by 75% within 6 months while maintaining 99% accuracy.

## Success Criteria
- Achieve 75% reduction in processing time compared to current baseline. *(Ref: REQ-001:2.1) [reduce]*
- Maintain 99% accuracy rate for all processed requirements. *(Ref: REQ-002:3.1) [maintain]*
- Complete implementation within 6 months of project start. *(Ref: REQ-001:4.2) [complete]*

## Key Performance Indicators
- Processing time: < 2.5 minutes per batch (75% reduction from 10 minutes baseline) *(Ref: REQ-002:2.3) [reduce]*
- Accuracy rate: ≥ 99% (unit: percent, timeframe: daily) *(Ref: REQ-002:3.1) [maintain]*

## Constraints
- Input requirements must conform to the specified format. *(Ref: REQ-001:1.1)*
- System must operate within existing infrastructure and security policies. *(Ref: REQ-004:1.1)*
- No manual intervention allowed during ingestion. *(Ref: REQ-002:2.5)*

## Assumptions
- Requirements provided are complete and up-to-date. *(Ref: REQ-001:assumptions)*
- Glossary terms are available for normalization. *(Ref: REQ-003:2.1)*
- Downstream systems are ready to consume ingested data. *(Ref: REQ-004:3.2)*

## Open Questions
- What is the process for handling ambiguous or conflicting requirements? *(Ref: REQ-001:notes)*
- How will updates to requirements be managed post-ingestion? *(Ref: REQ-002:future_considerations)*
- Are there scalability limits for batch size or frequency? *(Ref: REQ-002:performance)*

---
**Traceability:** Extracted from requirements: REQ-001, REQ-002, REQ-003, REQ-004  
**Generated:** 2026-02-08T10:30:00Z  
**Extraction Method:** Rule-based patterns + LLM validation  
**Pattern Precision:** 0.92 | **Outcome Focus:** 0.89 | **Overall Confidence:** 0.87
```
