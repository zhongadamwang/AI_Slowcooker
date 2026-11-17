# Collaboration Diagrams — Output Format

The complete templates for `collaboration-diagrams.md` and `collaboration-diagrams.json`. Values shown are illustrative.

### Markdown Structure (`collaboration-diagrams.md`)
```markdown
# Collaboration Diagrams

**Project**: [project_id]  
**Generated**: [timestamp]  
**Source**: domain-concepts.json, requirements.json

## Domain Class Model

### Entity Relationship Overview *(Diagram D-001)*
**Source Requirements**: [R-001], [R-003]  
**Domain Source**: orgModel/01-skill-dev/domain-model.md

```mermaid
classDiagram
    class User:::core {
        +user_id: String
        +name: String
        +email: String
        +role: UserRole
        +authenticate()
        +updateProfile()
    }
    
    class UserRole:::core {
        +role_id: String
        +name: String
        +permissions: String[]
        +grantAccess()
    }
    
    class Session:::entity {
        +session_id: String
        +start_time: DateTime
        +expiry_time: DateTime
        +is_active: Boolean
        +extend()
        +terminate()
    }
    
    User "1" --> "1" UserRole : has
    User "1" *-- "*" Session : creates
    
    %% Styling Definitions
    classDef core fill:#e1f5fe
    classDef entity fill:#f3e5f5
    classDef enum fill:#fff3e0
    classDef ai fill:#e8f5e8
```

## User-System Interactions

### Authentication Flow *(Diagram D-002)*
**Source Requirements**: [R-001], [R-003]  
**Entities Involved**: User, AuthenticationService, Database

```mermaid
sequenceDiagram
    participant U as User
    participant AS as AuthenticationService  
    participant DB as Database
    
    U->>AS: Login request (username, password)
    AS->>DB: Validate credentials
    DB-->>AS: User record
    AS->>AS: Generate JWT token
    AS-->>U: Authentication response (token)
    
    Note over AS: Token valid for 24 hours
    Note over U,DB: Secure HTTPS communication
```


### [Additional User-System Diagrams...]

## System-System Interactions

### API Integration Flow *(Diagram D-002)*
**Source Requirements**: [R-005], [R-007]  
**Entities Involved**: APIGateway, ExternalService, Cache

```mermaid
sequenceDiagram
    participant AG as API Gateway
    participant ES as External Service
    participant C as Cache
    
    AG->>C: Check cache for data
    alt Cache Hit
        C-->>AG: Return cached data
    else Cache Miss
        AG->>ES: Request external data
        ES-->>AG: Return fresh data
        AG->>C: Store in cache (TTL: 5min)
    end
    AG-->>Client: Return data response
```

### [Additional System-System Diagrams...]

## Hierarchical Collaboration Diagrams

### System Boundary View *(Diagram D-005)*
**Source Requirements**: [R-010]
**Decomposition**: `01-ECommerce-Platform/collaboration.md`

```mermaid
sequenceDiagram
    %% Stereotypes: User=actor | ECommerce=control | Payment=control | Shipping=control
    participant User as "User"
    
    box "E-commerce Platform"
        participant ECommerce as "E-commerce Platform"
    end
    
    box "Payment System"
        participant Payment as "Payment System"
    end
    
    box "Shipping System"
        participant Shipping as "Shipping System"
    end
    
    User->>ECommerce: Place Order
    ECommerce->>Payment: Process Payment
    ECommerce->>Shipping: Schedule Delivery
```

## Process Workflows

### [Business Process Diagrams...]
```

### JSON Structure (`collaboration-diagrams.json`)
```json
{
  "project_id": "string",
  "generation_metadata": {
    "generated_at": "ISO8601",
    "source_files": ["domain-concepts.json", "requirements.json"],
    "total_diagrams": "number",
    "diagram_types": ["class", "sequence", "flowchart", "stateDiagram"]
  },
  "diagrams": [
    {
      "id": "D-001",
      "title": "Entity Relationship Overview", 
      "type": "class",
      "category": "domain-model",
      "description": "Core domain entities and their relationships",
      "entities": ["User", "UserRole", "Session"],
      "source_requirements": ["R-001", "R-003"],
      "mermaid_code": "classDiagram...",
      "complexity": "medium",
      "maintenance_priority": "high"
    },
    {
      "id": "D-002",
      "title": "Authentication Flow", 
      "type": "sequence",
      "category": "user-system",
      "description": "User authentication and JWT token generation",
      "entities": ["User", "AuthenticationService", "Database"],
      "source_requirements": ["R-001", "R-003"],
      "mermaid_code": "sequenceDiagram...",
      "complexity": "medium",
      "maintenance_priority": "high"
    }
  ]
}
```
