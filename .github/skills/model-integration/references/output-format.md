# Model Integration — Output Format

The complete templates for this skill's outputs. Values are illustrative. Status fields describe the plan; record a step as executed only after `orgmodel-update` has actually applied it, and ignore the rollback fields (the orgModel is under version control).

### JSON Structure (`model-integration.json`)
```json
{
  "project_id": "string",
  "integration_metadata": {
    "generated_at": "ISO8601",
    "source_alignment": "domain-alignment.json",
    "source_newconcepts": "domain-newconcepts.json",
    "target_models": ["orgModel/01-skill-dev/domain-model.md"],
    "integration_strategy": "additive|replacement|merge|hybrid",
    "edp_compliance": "boolean",
    "total_integrations": "number",
    "conflict_resolution_count": "number",
    "rollback_capability": "boolean"
  },
  "integration_plan": {
    "phases": [
      {
        "phase_id": "P1",
        "phase_name": "Entity Integration",
        "sequence": 1,
        "strategy": "additive",
        "estimated_impact": "low|medium|high",
        "rollback_points": ["after_entity_mapping", "after_validation"],
        "dependencies": ["terminology_alignment"]
      }
    ],
    "integration_points": [
      {
        "integration_id": "IP-001",
        "type": "entity_integration|process_integration|terminology_integration|relationship_integration",
        "source": {
          "entity": "User Authentication",
          "source_file": "domain-concepts.json",
          "requirements_trace": ["REQ-001", "REQ-005"]
        },
        "target": {
          "model": "orgModel/01-skill-dev/domain-model.md",
          "section": "Security.Authentication",
          "existing_entities": ["Team Member", "Access Control"]
        },
        "integration_strategy": {
          "approach": "merge_with_existing",
          "conflict_resolution": "rename_and_specialize",
          "minimal_disruption": "extend_existing_hierarchy",
          "validation_checkpoints": ["entity_consistency", "relationship_integrity"]
        }
      }
    ],
    "conflict_resolutions": [
      {
        "conflict_id": "CR-001",
        "type": "entity_naming|relationship_mismatch|process_overlap|terminology_conflict",
        "description": "User vs Team Member entity naming conflict",
        "source_entity": "User",
        "target_entity": "Team Member",
        "resolution_strategy": {
          "approach": "create_specialization",
          "new_hierarchy": "Team Member > Authenticated User > External User",
          "impact": "extends_existing_model",
          "validation": "backward_compatibility_maintained"
        },
        "stakeholder_impact": {
          "affected_processes": ["authentication", "user_management"],
          "communication_required": ["developers", "business_analysts"],
          "training_impact": "minimal"
        }
      }
    ]
  },
  "integration_results": {
    "successful_integrations": [
      {
        "integration_id": "IP-001",
        "target_file": "orgModel/01-skill-dev/domain-model.md",
        "changes_applied": {
          "entities_added": ["Authenticated User"],
          "relationships_modified": ["Team Member -> has -> Authentication Profile"],
          "sections_updated": ["Security.Authentication"]
        },
        "validation_status": "passed",
        "rollback_data": "backup_reference_id"
      }
    ],
    "failed_integrations": [
      {
        "integration_id": "IP-005",
        "failure_reason": "circular_dependency_detected",
        "error_details": "Process A requires Process B which depends on Process A",
        "recommended_action": "redesign_process_flow",
        "rollback_performed": "true"
      }
    ],
    "model_coherence_check": {
      "consistency_score": "0.0-1.0",
      "validation_results": [
        {
          "check_type": "entity_consistency",
          "status": "passed|warning|failed",
          "issues": ["duplicate_entity_definitions"],
          "recommendations": ["consolidate_duplicate_entities"]
        }
      ]
    }
  }
}
```

### Integration Report Structure (`model-integration.md`)
```markdown
# Model Integration Report

**Project**: [Project Name]  
**Generated**: [ISO8601 timestamp]  
**Integration Strategy**: [additive|replacement|merge|hybrid]  
**EDP Compliance**: [Yes|No]  
**Overall Status**: [Success|Partial|Failed]

## Executive Summary
[High-level summary of integration approach, results, and impact]

## Integration Strategy
- **Approach**: [Strategy explanation]
- **Minimal Disruption Principles**: [How EDP methodology applied]
- **Rollback Capability**: [Available rollback points]
- **Progressive Integration**: [Phased deployment approach]

## Integration Results

### Successful Integrations
| Integration ID | Type | Target Model | Changes Applied | Impact |
|----------------|------|--------------|-----------------|--------|
| IP-001 | Entity | orgModel/01-skill-dev/domain-model.md | Added Authenticated User | Low |

### Conflict Resolutions
| Conflict ID | Type | Resolution | Stakeholder Impact |
|-------------|------|------------|-------------------|
| CR-001 | Entity Naming | Create Specialization | Minimal - extends existing |

### Model Coherence Validation
- **Consistency Score**: [0.0-1.0]
- **Critical Issues**: [Number]
- **Warnings**: [Number]
- **Recommendations**: [Number]

## Stakeholder Impact Analysis
[Summary of impacts by stakeholder group with communication requirements]

## Next Steps
- [ ] Review integration results with stakeholders
- [ ] Validate updated models in target environment
- [ ] Schedule training for affected processes
- [ ] Plan next integration phase
```
