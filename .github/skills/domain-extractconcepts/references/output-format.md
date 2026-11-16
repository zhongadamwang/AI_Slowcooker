# Domain Concepts — Output Format

The complete templates for this skill's JSON and Markdown outputs. Values shown are illustrative.

### JSON Structure (`domain-concepts.json`)
```json
{
  "project_id": "string",
  "extraction_metadata": {
    "generated_at": "ISO8601",
    "source_files": ["requirements.json", "goals.json"],
    "total_concepts": "number",
    "total_entities": "number",
    "confidence_score": "0.0-1.0"
  },
  "domain_entities": [
    {
      "id": "ENT-001",
      "name": "User",
      "description": "System user who interacts with the application",
      "attributes": [
        {
          "name": "user_id",
          "type": "identifier",
          "description": "Unique user identifier",
          "visibility": "public"
        },
        {
          "name": "role",
          "type": "enumeration",
          "description": "User access level",
          "values": ["admin", "user", "guest"],
          "visibility": "public"
        }
      ],
      "operations": [
        {
          "name": "authenticate",
          "description": "Verify user credentials",
          "parameters": ["username", "password"],
          "return_type": "boolean",
          "visibility": "public"
        },
        {
          "name": "updateProfile",
          "description": "Modify user profile data",
          "parameters": ["profile_data"],
          "return_type": "void",
          "visibility": "public"
        }
      ],
      "domain_area": "Authentication",
      "source_refs": ["R-001:section1", "R-003:section2"],
      "confidence": "0.0-1.0"
    }
  ],
  "business_concepts": [
    {
      "id": "CON-001",
      "name": "Authentication",
      "definition": "Process of verifying user identity",
      "synonyms": ["login", "sign-in", "verification"],
      "domain_area": "Security",
      "source_refs": ["R-001:section1"],
      "confidence": "0.0-1.0"
    }
  ],
  "terminology": [
    {
      "term": "API",
      "definition": "Application Programming Interface",
      "context": "Interface for system interactions",
      "domain_area": "Technical",
      "source_refs": ["R-005:section3"]
    }
  ],
  "relationships": [
    {
      "id": "REL-001",
      "type": "association",
      "source_entity": "User",
      "target_entity": "Role",
      "description": "User has assigned role",
      "cardinality": "many-to-one",
      "source_refs": ["R-002:section1"]
    }
  ],
  "domain_areas": [
    {
      "name": "Authentication",
      "description": "User identity verification and access control",
      "entities": ["User", "Role", "Session"],
      "concepts": ["Authentication", "Authorization"],
      "key_processes": ["Login", "Logout", "Password Reset"]
    }
  ]
}
```

### Markdown Structure (`domain-concepts.md`)
```markdown
# Domain Concepts Analysis

**Project**: [project_id]  
**Generated**: [timestamp]  
**Source**: requirements.json, goals.json  
**Total Entities**: [count] | **Total Concepts**: [count]

## Domain Areas

### Authentication & Security
**Key Entities**: User, Role, Session  
**Core Concepts**: Authentication, Authorization, Access Control  
**Primary Processes**: Login, Logout, Password Reset

### [Additional Domain Areas...]

## Entities

### User *(ENT-001)*
**Domain Area**: Authentication  
**Description**: System user who interacts with the application

**Attributes**:
- `user_id` (identifier): Unique user identifier [public]
- `role` (enumeration): User access level [admin, user, guest] [public]
- `email` (string): User contact information [public]

**Operations**:
- `authenticate(username, password)` → boolean: Verify user credentials [public]
- `updateProfile(profile_data)` → void: Modify user profile data [public]
- `validateSession()` → boolean: Check session validity [private]

**Source References**: [R-001:section1], [R-003:section2]

### [Additional Entities...]

## Business Concepts

### Authentication *(CON-001)*
**Domain Area**: Security  
**Definition**: Process of verifying user identity  
**Synonyms**: login, sign-in, verification  
**Source References**: [R-001:section1]

### [Additional Concepts...]

## Terminology Glossary

| Term | Definition | Domain Area | Context |
|------|------------|-------------|---------|
| API | Application Programming Interface | Technical | Interface for system interactions |
| OAuth | Open Authorization standard | Security | Third-party authentication protocol |

## Entity Relationships

### User ↔ Role *(REL-001)*
**Type**: Association (many-to-one)  
**Description**: User has assigned role  
**Source**: [R-002:section1]

### [Additional Relationships...]

---
**Traceability**: Extracted from requirements [R-001, R-002, R-003...]  
**Confidence Score**: 0.85/1.0  
**Generated**: [timestamp]
```
