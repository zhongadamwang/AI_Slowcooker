# EDPS Skill Completion Gates - Authoring Guide

This guide covers creating and maintaining `gate.json` files that define completion validation for EDPS skills.

## Purpose

Skill completion gates provide automated quality validation to ensure EDPS methodology standards are met before workflows advance to the next step. Gates check artifact existence, content patterns, and quality thresholds appropriate for each workflow archetype.

## Gate File Location

Every EDPS skill should have a `gate.json` file in its skill directory:
```
.github/skills/[skill-name]/
├── SKILL.md
└── gate.json       ← Completion validation definition
```

## Schema Reference

### Basic Structure

```json
{
  "$schema": "https://edps.dev/schemas/gate/v1.0.0",
  "skill_id": "S01",
  "skill_name": "requirements-ingest", 
  "version": "1.0.0",
  "gate_type": "completion",
  "severity": "hard | soft",
  "description": "Brief description of what this gate validates",
  "checks": [ /* array of validation checks */ ],
  "quality_score_weight": 0.05,
  "bypass_allowed": true,
  "workflow_archetypes": {
    "standard": "hard | soft | bypass",
    "rapid": "hard | soft | bypass", 
    "compliance": "hard | soft | bypass"
  }
}
```

### Required Fields

- **skill_id**: Unique identifier (S01-S31 for core skills)
- **skill_name**: Exact name matching the skill directory
- **version**: Semantic version for gate evolution
- **severity**: Default severity level (`hard` blocks workflow, `soft` warns)
- **checks**: Array of validation checks to run

### Check Types

#### 1. Artifact Existence
Verifies required output files exist in the expected locations.

```json
{
  "id": "requirements_file_exists",
  "type": "artifact_existence", 
  "severity": "hard",
  "description": "Requirements document must be created",
  "artifacts": [
    "artifacts/Requirements/requirements.md",
    "artifacts/Analysis/requirements-analysis.json"
  ],
  "remediation": "Run requirements-ingest to create requirements documentation"
}
```

#### 2. Content Pattern Validation
Checks file content for required text, patterns, or structure.

```json
{
  "id": "content_structure_check",
  "type": "content_pattern",
  "severity": "soft",
  "description": "Should include standard requirement sections",
  "file": "artifacts/Requirements/requirements.md", 
  "must_contain": ["## Functional Requirements", "## Non-Functional Requirements"],
  "must_not_contain": ["TODO", "PLACEHOLDER"],
  "must_contain_pattern": "REQ-\\d{3}:",
  "min_matches": 3,
  "remediation": "Add structured requirement sections with proper IDs"  
}
```

#### 3. JSON Schema Validation
Validates JSON artifacts against defined schemas.

```json
{
  "id": "json_structure_valid",
  "type": "json_schema",
  "severity": "hard", 
  "description": "JSON output must conform to schema",
  "file": "artifacts/Analysis/domain-model.json",
  "schema": {
    "type": "object",
    "required": ["entities", "relationships"],
    "properties": {
      "entities": {
        "type": "array",
        "minItems": 1
      }
    }
  },
  "remediation": "Ensure JSON follows required domain model structure"
}
```

### Workflow Archetype Behavior

Gates can behave differently based on workflow archetype:

| Archetype | Purpose | Gate Behavior |
|-----------|---------|---------------|
| **standard** | Balanced process quality | Hard gates block, soft gates warn |
| **rapid** | Fast iteration, lower overhead | Many gates bypass, focus on critical validations |
| **compliance** | High assurance, full documentation | Stricter thresholds, more hard gates |

Example archetype configuration:
```json
"workflow_archetypes": {
  "standard": "soft",      // Warn but don't block
  "rapid": "bypass",       // Skip validation entirely  
  "compliance": "hard"     // Block workflow if validation fails
}
```

## Quality Scoring

Gates contribute to overall workflow quality scores used for project reporting and archetype transitions.

```json
"quality_score_weight": 0.08  // This skill contributes 8% to total quality
```

**Weight guidelines**:
- Core methodology skills (requirements, domain modeling): 0.08-0.12
- Documentation/reporting skills: 0.04-0.06 
- Optional enhancement skills: 0.02-0.05
- Critical validation skills (compliance, testing): 0.10-0.15

Total weights should sum to approximately 1.0 across all skills.

## Authoring Best Practices

### 1. Start with Critical Validations
Focus on checks that catch the most common quality issues:
- Key artifact existence
- Basic content structure
- Required metadata presence

### 2. Use Graduated Severity
- **Hard checks**: Prerequisites for next workflow steps  
- **Soft checks**: Quality improvements and best practices
- **Bypass where appropriate**: Not every skill needs hard gates

### 3. Provide Actionable Remediation
Every failed check should offer specific guidance:
```json
"remediation": "Run domain-extractconcepts to identify business entities before proceeding"
```

### 4. Test with Real Projects
Validate gates with actual project artifacts to ensure:
- Patterns match realistic content
- File paths reflect actual usage
- Remediation guidance is effective

### 5. Version and Evolve
Use semantic versioning to track gate evolution:
- PATCH (0.0.X): Bug fixes, typo corrections
- MINOR (0.X.0): New optional checks, refined patterns  
- MAJOR (X.0.0): Breaking changes to check structure

## Examples by Skill Category

### Requirements & Analysis Skills
Focus on content structure, traceability, and completeness.

```json
{
  "checks": [
    {
      "id": "requirements_documented", 
      "type": "artifact_existence",
      "severity": "hard",
      "artifacts": ["artifacts/Requirements/requirements.md"]
    },
    {
      "id": "traceability_present",
      "type": "content_pattern", 
      "severity": "soft",
      "file": "artifacts/Requirements/requirements.md",
      "must_contain_pattern": "REQ-\\d{3}",
      "min_matches": 5
    }
  ]
}
```

### Domain Modeling Skills
Validate entity extraction, relationships, and alignment.

```json
{
  "checks": [
    {
      "id": "entities_extracted",
      "type": "json_schema",
      "severity": "hard", 
      "file": "artifacts/Domain/entities.json",
      "schema": {
        "type": "object", 
        "required": ["entities"],
        "properties": {
          "entities": {"type": "array", "minItems": 3}
        }
      }
    }
  ]
}
```

### Planning & Management Skills
Check scheduling, task derivation, and tracking completeness.

```json
{
  "checks": [
    {
      "id": "tasks_derived",
      "type": "artifact_existence", 
      "severity": "soft",
      "artifacts": ["artifacts/Planning/task-list.md"]
    },
    {
      "id": "effort_estimates",
      "type": "content_pattern",
      "severity": "soft",
      "file": "artifacts/Planning/task-list.md",
      "must_contain": ["Effort:", "Dependencies:"]
    }
  ]
}
```

## Integration with Orchestrator

The `edps-workflow-orchestrator` automatically discovers and evaluates gates:

1. **Discovery**: Reads `gate.json` from skill directory
2. **Evaluation**: Runs all checks when skill completion is requested  
3. **Decision**: Based on archetype and severity, allows/blocks workflow progression
4. **Feedback**: Provides detailed remediation guidance for failed checks

## Testing Gates

Use the orchestrator's gate evaluation function to test your gates:

```bash
# Test a gate configuration  
> orchestrate test-gate requirements-ingest

✅ Gate evaluation: PASSED
   • requirements_exist: ✅ Found artifacts/Requirements/requirements.md
   • content_structure: ⚠️ Missing REQ-IDs (soft failure)
   • quality_threshold: ✅ 85% meets standard archetype minimum

Quality Score: 0.08/0.08 (100% weight contribution)
```

## Migration and Updates

When updating existing gates:

1. **Test with existing projects** to avoid breaking working workflows
2. **Use semantic versioning** to track compatibility  
3. **Provide migration notes** for breaking changes
4. **Update integration tests** to cover new validations

---

This guide provides the foundation for creating effective skill completion gates that enhance EDPS workflow quality while supporting different project archetypes and organizational needs.