# Domain Alignment — Output Format

The complete templates for this skill's JSON and Markdown outputs. Values shown are illustrative.

### JSON Structure (`domain-alignment.json`)
```json
{
  "project_id": "string",
  "alignment_metadata": {
    "generated_at": "ISO8601",
    "source_concepts_file": "domain-concepts.json",
    "reference_models": ["orgModel/01-skill-dev/domain-model.md"],
    "reference_vocabularies": ["orgModel/01-skill-dev/vocabulary.md"],
    "total_alignments": "number",
    "conflict_count": "number",
    "alignment_confidence": "0.0-1.0"
  },
  "entity_alignments": [
    {
      "extracted_entity": {
        "id": "ENT-001",
        "name": "User",
        "attributes": ["user_id", "email", "role"],
        "operations": ["authenticate", "updateProfile"],
        "source": "domain-concepts.json"
      },
      "alignment_result": {
        "type": "direct_match|partial_match|new_entity|conflict",
        "target_entity": {
          "name": "Team Member",
          "source": "orgModel/01-skill-dev/domain-model.md",
          "section": "Actors.Primary Actors"
        },
        "confidence": "0.0-1.0",
        "mapping_rationale": "Both represent individuals using system functionality",
        "recommended_action": "map_to_existing|rename_extracted|create_new|resolve_conflict",
        "notes": "Consider if User is more specific than Team Member"
      }
    }
  ],
  "terminology_alignments": [
    {
      "extracted_term": {
        "term": "Authentication",
        "definition": "Process of verifying user identity",
        "source": "domain-concepts.json"
      },
      "alignment_result": {
        "type": "vocabulary_match|vocabulary_conflict|new_term|synonym_detected",
        "target_term": {
          "term": "Skills Assessment",
          "definition": "Systematic evaluation of current skill levels",
          "source": "orgModel/01-skill-dev/vocabulary.md"
        },
        "confidence": "0.0-1.0",
        "relationship": "unrelated|synonym|broader|narrower|similar",
        "recommended_action": "adopt_standard|define_new|clarify_distinction",
        "notes": "No direct relationship - different domains"
      }
    }
  ],
  "relationship_alignments": [
    {
      "extracted_relationship": {
        "id": "REL-001",
        "source_entity": "User",
        "target_entity": "Role",
        "type": "association"
      },
      "alignment_result": {
        "alignment_pattern": "existing_pattern|new_pattern",
        "similar_relationships": [
          {
            "source": "Team Member",
            "target": "Skill Profile",
            "type": "has",
            "model": "orgModel/01-skill-dev/domain-model.md"
          }
        ],
        "recommended_action": "use_existing_pattern|define_new_pattern",
        "notes": "Similar ownership pattern exists in organizational model"
      }
    }
  ],
  "conflicts_detected": [
    {
      "conflict_id": "CONF-001",
      "type": "naming_conflict|definition_conflict|structure_conflict",
      "description": "Term 'User' conflicts with established 'Team Member' terminology",
      "affected_items": ["ENT-001", "termUser"],
      "severity": "high|medium|low",
      "resolution_options": [
        {
          "option": "rename_extracted",
          "description": "Rename 'User' to 'Team Member' in extracted concepts",
          "impact": "Updates project terminology to match organizational standard"
        },
        {
          "option": "create_distinction",
          "description": "Define 'User' as a specialization of 'Team Member'",
          "impact": "Extends organizational model with new concept"
        }
      ]
    }
  ],
  "operation_alignments": [
    {
      "extracted_operation": {
        "entity": "User",
        "operation": "authenticate",
        "parameters": ["username", "password"],
        "return_type": "boolean",
        "source": "domain-concepts.json"
      },
      "alignment_result": {
        "type": "method_match|method_conflict|new_method",
        "target_operation": {
          "entity": "Team Member",
          "operation": "validateCredentials", 
          "parameters": ["credentials"],
          "source": "orgModel/01-skill-dev/domain-model.md"
        },
        "confidence": "0.0-1.0",
        "similarity": "identical|similar|different",
        "recommended_action": "use_existing|rename_operation|define_new",
        "notes": "Similar functionality, consider parameter alignment"
      }
    }
  ],
  "recommendations": [
    {
      "id": "REC-001",
      "type": "standardization|extension|clarification",
      "priority": "high|medium|low",
      "description": "Adopt organizational 'Team Member' terminology instead of 'User'",
      "impact": "Improves consistency across projects",
      "implementation": "Update domain-concepts.json and project documentation"
    }
  ]
}
```

### Markdown Structure (`domain-alignment.md`)
```markdown
# Domain Alignment Report

**Project**: [project_id]  
**Generated**: [timestamp]  
**Source Concepts**: domain-concepts.json ([count] entities, [count] concepts)  
**Reference Models**: [list of organizational models]  
**Alignment Confidence**: [score]/1.0

## Executive Summary

**Total Alignments**: [count]  
**Direct Matches**: [count] | **Partial Matches**: [count] | **New Entities**: [count]  
**Conflicts Detected**: [count] | **Recommendations**: [count]

## Entity Alignments

### ✅ Direct Matches
Extracted entities that directly align with existing organizational entities.

#### User → Team Member *(ENT-001)*
**Confidence**: 0.95  
**Source Model**: orgModel/01-skill-dev/domain-model.md  
**Rationale**: Both represent individuals using system functionality  
**Action**: ✅ Map to existing organizational entity

### ⚠️ Partial Matches  
Extracted entities with similar but not identical organizational counterparts.

#### ProjectOwner → Team Lead *(ENT-002)*
**Confidence**: 0.75  
**Source Model**: orgModel/01-skill-dev/domain-model.md  
**Differences**: ProjectOwner broader scope, Team Lead specific to team management  
**Action**: 🔄 Consider creating specialization relationship

### 🆕 New Entities
Extracted entities with no organizational counterparts - potential model extensions.

#### SkillFramework *(ENT-003)*
**Domain Area**: Learning Management  
**Rationale**: Project-specific concept not in organizational model  
**Action**: ➕ Propose addition to organizational model

## Operation Alignments

### ✅ Method Matches
Extracted operations that align with existing organizational entity methods.

#### User.authenticate() → Team Member.validateCredentials() *(OP-001)*
**Confidence**: 0.85  
**Source Entity**: Team Member (orgModel/01-skill-dev/domain-model.md)  
**Parameter Mapping**: [username, password] → [credentials]  
**Action**: ✅ Align with organizational operation pattern

### 🆕 New Operations
Extracted operations with no organizational counterparts.

#### User.updateProfile() *(OP-002)*
**Entity**: User  
**Parameters**: [profile_data]  
**Return Type**: void  
**Action**: 🆕 Propose as new capability

## Terminology Alignments

### ✅ Vocabulary Matches
| Extracted Term | Organization Term | Confidence | Action |
|----------------|-------------------|------------|---------|
| Assessment | Skills Assessment | 0.90 | Adopt standard term |

### ⚠️ Conflicting Definitions
| Term | Extracted Definition | Org Definition | Resolution |
|------|---------------------|----------------|------------|
| Validation | Process verification | Skill demonstration requirement | Clarify context distinction |

### 🆕 New Terminology
Terms not in organizational vocabulary that could be valuable additions.

## Relationship Patterns

### Existing Patterns Applied
- **Ownership Pattern**: User ↔ Role similar to Team Member ↔ Skill Profile
- **Validation Pattern**: Assessment validates Skills (organizational model)

### New Patterns Identified
- **Framework Hierarchy**: SkillFramework contains multiple Skills
- **Progress Tracking**: Assessment tracks learning progression

## Conflicts & Resolutions

### 🔴 High Priority Conflicts

#### CONF-001: Naming Conflict - User vs Team Member
**Issue**: Project uses "User" while organization uses "Team Member"  
**Impact**: Terminology inconsistency across projects  
**Resolution Options**:
1. ✅ **Recommended**: Rename to "Team Member" for consistency
2. Define "User" as specialization of "Team Member"

### 🟡 Medium Priority Issues

#### CONF-002: Definition Scope - Assessment scope differences
**Issue**: Project Assessment broader than organizational Skills Assessment  
**Impact**: Potential confusion in assessment processes  
**Resolution**: Define Assessment as supertype of Skills Assessment

## Recommendations

### 🎯 High Priority Actions

1. **Standardize Entity Names** (Impact: High)
   - Rename "User" → "Team Member"
   - Update all references and relationships

2. **Adopt Organizational Vocabulary** (Impact: Medium)
   - Use "Skills Assessment" instead of generic "Assessment"
   - Maintain traceability in concept definitions

### 🔄 Domain Model Evolution

1. **Proposed Extensions**
   - Add "SkillFramework" entity to organizational model
   - Define relationship patterns for framework hierarchies

2. **Vocabulary Additions**
   - Add project-specific terms to organizational vocabulary
   - Document context-specific usage patterns

---
**Traceability**: Aligned concepts from domain-concepts.json against [org models]  
**Next Steps**: Review recommendations with domain stakeholders  
**Generated**: [timestamp]
```
