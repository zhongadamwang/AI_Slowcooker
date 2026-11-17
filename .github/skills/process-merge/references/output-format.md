# Process Merge — Output Format

The complete templates for this skill's outputs. Values are illustrative. Status fields describe the plan; record a step as executed only after `orgmodel-update` has actually applied it, and ignore the rollback fields (the orgModel is under version control).

### JSON Structure (`process-merge.json`)
```json
{
  "project_id": "string",
  "merge_metadata": {
    "generated_at": "ISO8601",
    "source_domain_concepts": "domain-concepts.json",
    "source_alignment": "domain-alignment.json",
    "target_orgmodels": ["orgModel/01-skill-dev/process.md"],
    "overlap_analysis_method": "entity_matching",
    "integration_strategy": "minimal_disruption",
    "edp_compliance": "boolean",
    "total_processes_analyzed": "number",
    "minimum_overlap_identified": "number",
    "integration_complexity": "low|medium|high",
    "stakeholder_validation_required": "boolean",
    "rollback_capability": "boolean"
  },
  "overlap_analysis": {
    "process_mappings": [
      {
        "mapping_id": "PM-001",
        "new_process": {
          "name": "User Authentication Process",
          "source_requirements": ["REQ-001", "REQ-003"],
          "entities": ["User", "Authentication Service", "Security Token"],
          "activities": ["Login Request", "Credential Validation", "Token Generation"],
          "decision_points": ["Credential Valid?", "Multi-factor Required?"],
          "estimated_integration_impact": "low|medium|high"
        },
        "existing_processes": [
          {
            "orgmodel": "orgModel/02-security-management/process.md",
            "process_name": "Access Control Process",
            "overlap_percentage": 85,
            "shared_entities": ["User", "Security Token"],
            "shared_activities": ["Credential Validation"],
            "integration_points": ["post_authentication", "token_management"],
            "disruption_assessment": "minimal"
          }
        ],
        "overlap_type": "significant|partial|minimal|none",
        "integration_strategy": {
          "approach": "extend_existing|merge_processes|create_specialized|create_new",
          "minimal_disruption_plan": {
            "preserve_existing": ["authentication_flow", "token_structure"],
            "extend_with": ["multi_factor_support", "enhanced_logging"],
            "stakeholder_checkpoints": ["after_entity_mapping", "before_deployment"]
          }
        }
      }
    ],
    "overlap_summary": {
      "total_new_processes": "number",
      "processes_with_significant_overlap": "number",
      "processes_requiring_new_creation": "number",
      "processes_for_extension": "number",
      "minimum_integration_scope": {
        "entities_to_integrate": "number",
        "activities_to_merge": "number",
        "decision_points_to_align": "number"  
      }
    }
  },
  "integration_plan": {
    "phases": [
      {
        "phase_id": "P1",
        "phase_name": "Entity Alignment",
        "sequence": 1,
        "strategy": "minimal_disruption",
        "activities": [
          "Map new entities to existing entity hierarchy",
          "Identify terminology conflicts and resolutions",
          "Validate entity relationship consistency"
        ],
        "deliverables": ["entity_mapping_validation.md"],
        "stakeholder_checkpoints": ["entity_review_meeting"],
        "rollback_points": ["before_entity_integration"],
        "estimated_effort": "0.5 days",
        "risk_assessment": "low"
      },
      {
        "phase_id": "P2",
        "phase_name": "Process Flow Integration",
        "sequence": 2,
        "strategy": "extend_existing_flows",
        "activities": [
          "Integrate new activities into existing process flows",
          "Align decision points and branching logic",
          "Update process documentation and diagrams"
        ],
        "deliverables": ["updated_process_flows.md", "integration_validation.json"],
        "stakeholder_checkpoints": ["process_flow_review"],
        "rollback_points": ["before_process_update", "after_validation"],
        "estimated_effort": "1.5 days",
        "risk_assessment": "medium"
      }
    ],
    "stakeholder_validation": {
      "required_approvals": [
        {
          "approval_id": "SV-001",
          "stakeholder_role": "Process Owner",
          "scope": "process_flow_changes",
          "validation_criteria": ["business_logic_preservation", "performance_maintenance"],
          "approval_deadline": "ISO8601",
          "escalation_path": "department_head > executive_sponsor"
        }
      ],
      "validation_checkpoints": [
        {
          "checkpoint_id": "CP-001",
          "name": "Entity Integration Validation",
          "criteria": ["terminology_consistency", "relationship_integrity"],
          "validation_method": "stakeholder_review",
          "required_participants": ["domain_expert", "process_owner"],
          "success_criteria": "unanimous_approval"
        }
      ]
    },
    "rollback_strategy": {
      "rollback_points": [
        {
          "point_id": "RP-001",
          "name": "Pre-Integration State",
          "captured_state": "complete_orgmodel_snapshot",
          "rollback_triggers": ["validation_failure", "stakeholder_rejection"],
          "recovery_time": "< 1 hour",
          "data_integrity": "guaranteed"
        }
      ],
      "rollback_procedures": [
        "Restore orgModel files from snapshot",
        "Reset domain model alignments",
        "Notify stakeholders of rollback completion"
      ]
    }
  },
  "integration_results": {
    "successful_integrations": [
      {
        "integration_id": "SI-001",
        "process_name": "Enhanced Authentication Process",
        "target_orgmodel": "orgModel/02-security-management/",
        "integration_type": "extension",
        "changes_applied": [
          "Added multi-factor authentication activities",
          "Extended user entity with authentication attributes",  
          "Updated decision points for security levels"
        ],
        "validation_status": "passed",
        "stakeholder_approval": "approved",
        "rollback_status": "not_required"
      }
    ],
    "failed_integrations": [
      {
        "integration_id": "FI-001", 
        "process_name": "Complex Workflow Process",
        "failure_reason": "irreconcilable_entity_conflicts",
        "rollback_executed": "true",
        "alternative_approach": "create_separate_process_model",
        "stakeholder_notification": "completed"
      }
    ],
    "integration_metrics": {
      "total_processes_integrated": "number",
      "average_overlap_percentage": "number",
      "minimal_disruption_achieved": "boolean",
      "stakeholder_satisfaction": "high|medium|low",
      "rollback_incidents": "number",
      "integration_completion_time": "hours"
    }
  }
}
```
