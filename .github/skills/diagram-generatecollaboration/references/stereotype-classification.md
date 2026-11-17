# Participant Stereotype Classification

Every participant in a hierarchical collaboration diagram must be classified into exactly one of four stereotypes. Classification drives annotation generation, decomposition eligibility, and message routing validation.

### Stereotype Definitions

| Stereotype | Comment value | Role | Decomposable? |
|-----------|---------------------|------|---------------|
| Actor | `actor` | External entity that initiates interactions | No |
| Boundary | `boundary` | Interface mediator between actors and internal components | No |
| Control | `control` | Business logic / orchestration component | **Yes** |
| Entity | `entity` | Data store or passive resource | No |

### Automatic Type Inference Rules

When a participant does not have an explicit stereotype, the skill infers its type using the following ordered heuristic rules:

1. **Actor inference** — A participant is classified as `actor` when:
   - It appears **outside all `box` boundaries**
   - It only **initiates** interactions (sends first messages) and never receives unsolicited internal messages
   - Its name matches common actor patterns: *User*, *Customer*, *Client*, *Admin*, *External*, *Partner*
   - It has a `<<Actor>>` stereotype tag in domain concepts

2. **Boundary inference** — A participant is classified as `boundary` when:
   - It is the **first participant inside a `box`** to receive a message from an external actor
   - Its name matches interface patterns: *UI*, *API*, *Gateway*, *Portal*, *Interface*, *Handler*, *Endpoint*, *Facade*
   - It primarily **mediates** between external actors and internal components
   - It has a `<<UI>>` stereotype tag in domain concepts

3. **Entity inference** — A participant is classified as `entity` when:
   - It primarily **receives** data operation messages (CRUD: store, retrieve, query, update, delete)
   - Its name matches data patterns: *DB*, *Database*, *Repository*, *Store*, *Cache*, *Registry*, *Storage*, *Table*, *Queue*
   - It **does not initiate** complex orchestration sequences
   - It has a `<<Entity>>` stereotype tag in domain concepts

4. **Control inference (default)** — A participant is classified as `control` when:
   - It does **not** match actor, boundary, or entity patterns
   - It performs **business logic**, orchestration, or coordination
   - Its name matches service patterns: *Service*, *Manager*, *Processor*, *Engine*, *Handler*, *Coordinator*, *Orchestrator*, *Validator*
   - It has a `<<System>>` stereotype tag in domain concepts
   - **Fallback**: any participant that cannot be classified by the above rules defaults to `control`

### Manual Type Override

Explicit type specification always takes precedence over inference. Types can be set via:

**Input JSON:**
```json
{
  "participants": [
    { "name": "OrderService", "stereotype": "control" },
    { "name": "AuditLog", "stereotype": "entity" },
    { "name": "AdminPortal", "stereotype": "boundary" }
  ]
}
```

**Inline annotation (already in diagram):**
```
%% Stereotypes: OrderService=control
participant OrderService as "Order Service"
```

When a manual override conflicts with inferred type, the override wins and a note is added to the diagram metadata:
```json
{
  "type_overrides": [
    { "participant": "AuditLog", "inferred": "control", "override": "entity", "reason": "manual" }
  ]
}
```

### Mermaid Annotation Generation

After classification, every participant definition in the Mermaid output must use the standard `participant [Alias] as "[Label]"` syntax, with stereotypes tracked in a `%% Stereotypes:` comment:

```
sequenceDiagram
    %% Stereotypes: Customer=actor | API=boundary, OrderSvc=control, OrderDB=entity
    participant Customer as "Customer"
    
    box "Order Processing"
        participant API as "Order API"
        participant OrderSvc as "Order Service"
        participant OrderDB as "Order Database"
    end
    
    Customer->>API: Place Order
    API->>OrderSvc: Process Order
    OrderSvc->>OrderDB: Store Order
```

**Generation rules:**
- Use `participant [Alias] as "[Label]"` for every participant
- Include a `%% Stereotypes:` comment listing all participants with their types
- Format: `Alias=type` pairs, separated by commas within a box and `|` between boxes
- Actors are declared **before** any `box` block
- Boundary participants are declared **first** inside their `box` block
- **NEVER** use `@{ "type": "...", "label": "..." }` syntax — it is not supported by most Mermaid renderers (GitHub, Mermaid Live, VS Code preview)
- Always quote box labels: `box "Name"` not `box Name`

### Decomposition Rule Enforcement

Before generating a decomposition (sub-process diagram) for any participant, the skill **must** validate decomposition eligibility:

#### Rule 1: Control-Only Decomposition
- **Only** participants with `"type": "control"` may be decomposed into sub-process diagrams
- Attempting to decompose an `actor`, `boundary`, or `entity` participant **must** produce a validation error

**Validation output on violation:**
```json
{
  "validation_errors": [
    {
      "rule": "control-only-decomposition",
      "participant": "CustomerDB",
      "type": "entity",
      "message": "Cannot decompose participant 'CustomerDB' (type: entity). Only control-type participants can be decomposed into sub-processes.",
      "suggestion": "If this participant requires internal detail, consider reclassifying it as 'control' or modeling its internals as a separate entity-focused diagram."
    }
  ]
}
```

#### Rule 2: Boundary-First Reception
- Within any `box` boundary, the **first message from an external actor** must be received by a `boundary`-type participant
- If no boundary-type participant exists in a box, a validation warning is generated
- If an actor sends a message directly to a `control` or `entity` participant inside a box, a validation error is generated

**Valid pattern:**
```
Customer (actor) ->> API (boundary) ->> Service (control) ->> DB (entity)
```

**Invalid pattern (produces error):**
```
Customer (actor) ->> Service (control)   ❌ skips boundary
```

**Validation output on violation:**
```json
{
  "validation_errors": [
    {
      "rule": "boundary-first-reception",
      "boundary": "Order Processing",
      "actor": "Customer",
      "received_by": "OrderService",
      "received_by_type": "control",
      "message": "Actor 'Customer' sends directly to 'OrderService' (type: control) inside boundary 'Order Processing'. Messages from actors must be received by a boundary-type participant first.",
      "suggestion": "Add or designate a boundary-type participant (e.g., API Gateway) as the entry point for this boundary."
    }
  ]
}
```

#### Rule 3: Actor Externality
- `actor`-type participants must **never** appear inside a `box` boundary
- Actors must be declared at the top level, before any `box` block

#### Rule 4: Entity Stability
- `entity`-type participants **should not** be decomposed
- Entities represent stable data/resource concerns; if internal detail is needed, model it as a separate entity-relationship diagram rather than a process decomposition

### Type Consistency Across Hierarchy Levels

When a participant is decomposed from Level N to Level N+1:
- The **parent participant** at Level N retains its original type annotation
- The **decomposed diagram** at Level N+1 introduces new participants with their own type classifications
- The **entry point** in the Level N+1 diagram should be a `boundary`-type participant matching the parent's external interface
- Type classifications must be **consistent** — a participant classified as `control` at Level N cannot appear as `entity` at Level N+1

### Participant Type Summary

After classification, the skill generates a type summary in the diagram metadata:

```json
{
  "participant_type_summary": {
    "total_participants": 8,
    "by_type": {
      "actor": { "count": 2, "participants": ["Customer", "Admin"] },
      "boundary": { "count": 2, "participants": ["WebUI", "AdminPortal"] },
      "control": { "count": 3, "participants": ["OrderService", "PaymentService", "NotificationService"] },
      "entity": { "count": 1, "participants": ["OrderDB"] }
    },
    "decomposable": ["OrderService", "PaymentService", "NotificationService"],
    "type_overrides": [],
    "inference_confidence": {
      "high": ["Customer", "WebUI", "OrderDB"],
      "medium": ["OrderService", "PaymentService"],
      "low": ["NotificationService"]
    }
  }
}
```

### Classification Input Parameters

```json
{
  "stereotype_classification": true,
  "auto_inference": true,
  "manual_overrides": [
    { "participant": "AuditLog", "type": "entity" }
  ],
  "enforce_decomposition_rules": true,
  "enforce_boundary_first_reception": true,
  "generate_type_summary": true
}
```
