# Top Requirements Update — Output Format

The complete templates for this skill's outputs. Values are illustrative. Status fields describe the plan; record a step as executed only after `orgmodel-update` has actually applied it, and ignore the rollback fields (the orgModel is under version control).

### JSON Structure (`top-requirements-update.json`)

```json
{
  "project_id": "string",
  "update_metadata": {
    "generated_at": "ISO8601",
    "source_requirements": "requirements.json",
    "source_analysis": ["domain-concepts.json", "process-merge.json", "w5h-analysis.json"],
    "hierarchy_analysis_method": "dependency_graph",
    "update_strategy": "insight_integration",
    "consistency_validation": "bidirectional",
    "total_requirements_analyzed": "number",
    "top_level_requirements_identified": "number",
    "requirements_updated": "number",
    "orgmodel_documents_affected": "number",
    "traceability_preservation": "complete",
    "validation_status": "passed|failed|partial"
  },
  "hierarchy_analysis": {
    "requirement_hierarchy": [
      {
        "hierarchy_level": 1,
        "requirement_id": "REQ-TOP-001",
        "requirement_type": "business_goal",
        "title": "Implement Evolutionary Development Capability",
        "current_statement": "Enable team to adapt development practices based on changing requirements",
        "dependency_type": "strategic",
        "child_requirements": ["REQ-002", "REQ-005", "REQ-012"],
        "affects_orgmodel": ["orgModel/01-skill-development/main.md"],
        "stakeholder_impact": "high",
        "update_priority": "critical"
      }
    ],
    "dependency_graph": {
      "nodes": [
        {
          "requirement_id": "REQ-TOP-001",
          "level": 1,
          "type": "strategic",
          "influences": ["REQ-002", "REQ-005"],
          "influenced_by": ["business_goals"]
        }
      ],
      "edges": [
        {
          "from": "REQ-TOP-001",
          "to": "REQ-002",
          "relationship": "decomposes_to",
          "weight": 0.8
        }
      ]
    }
  },
  "insight_integration": {
    "updates_applied": [
      {
        "update_id": "UPD-001",
        "target_requirement": "REQ-TOP-001",
        "update_type": "refinement",
        "source_insights": [
          {
            "source": "domain-concepts.json",
            "insight_type": "entity_identification",
            "specific_insight": "Skill entity identified as core domain concept",
            "integration_approach": "terminology_alignment"
          },
          {
            "source": "process-merge.json",
            "insight_type": "process_integration",
            "specific_insight": "Existing training process can be extended vs replaced",
            "integration_approach": "process_refinement"
          }
        ],
        "original_statement": "Enable team to adapt development practices based on changing requirements",
        "updated_statement": "Implement skill-based evolutionary development framework that extends existing training processes to enable adaptive development practices",
        "rationale": "Domain analysis revealed 'Skill' as central entity; process analysis showed extension opportunity rather than replacement",
        "impact_assessment": {
          "scope_change": "expanded",
          "complexity_change": "increased",
          "risk_change": "decreased",
          "stakeholder_alignment": "improved"
        }
      }
    ],
    "consistency_validations": [
      {
        "validation_id": "CV-001",
        "validation_type": "hierarchical_consistency",
        "parent_requirement": "REQ-TOP-001",
        "child_requirements": ["REQ-002", "REQ-005"],
        "consistency_check": "alignment_validation",
        "status": "consistent",
        "alignment_score": 0.92,
        "issues_identified": [],
        "resolution_actions": []
      }
    ]
  },
  "orgmodel_coordination": {
    "affected_documents": [
      {
        "document_path": "orgModel/01-skill-development/main.md",
        "update_type": "strategic_alignment",
        "update_priority": "high",
        "changes_required": [
          {
            "section": "Process Overview",
            "change_type": "enhancement",
            "current_content": "Team development through structured learning",
            "proposed_content": "Skill-based evolutionary development with adaptive learning pathways",
            "source_requirement": "REQ-TOP-001",
            "validation_required": true
          }
        ],
        "consistency_dependencies": ["orgModel/02-training/process.md"],
        "stakeholder_approval": "pending"
      }
    ],
    "cross_document_consistency": [
      {
        "consistency_id": "CDC-001",
        "documents": ["orgModel/01-skill-development/main.md", "orgModel/02-training/process.md"],
        "consistency_type": "terminology_alignment",
        "alignment_requirement": "Skill terminology must be consistent across documents",
        "current_status": "inconsistent",
        "resolution_plan": "Update training process terminology to align with skill framework",
        "estimated_effort": "0.5 days"
      }
    ]
  },
  "traceability_maintenance": {
    "requirement_lineage": [
      {
        "requirement_id": "REQ-TOP-001",
        "change_history": [
          {
            "change_id": "CHG-001",
            "timestamp": "ISO8601",
            "change_type": "insight_integration",
            "source_analysis": ["domain-concepts", "process-merge"],
            "previous_version": "Enable team to adapt development practices",
            "updated_version": "Implement skill-based evolutionary development framework",
            "change_rationale": "Domain analysis insights integrated",
            "approver": "system_analysis",
            "rollback_data": "stored"
          }
        ],
        "impact_trace": [
          {
            "affected_requirement": "REQ-002",
            "relationship": "child",
            "impact_type": "alignment_update",
            "status": "propagated"
          }
        ]
      }
    ],
    "validation_checkpoints": [
      {
        "checkpoint_id": "VC-001",
        "checkpoint_type": "consistency_validation",
        "scope": "hierarchy_alignment",
        "validation_criteria": "All child requirements align with updated parent",
        "status": "passed",
        "validation_timestamp": "ISO8601"
      }
    ]
  }
}
```
