# Box Syntax Generation

This section defines how the skill generates Mermaid `box ... end` syntax blocks for boundary grouping in hierarchical sequence diagrams. All rules in this section apply whenever `hierarchical_decomposition: true` or explicit boundaries are configured.

### Core Box Syntax Template

Every boundary is rendered as a `box` block. External actors are declared **before** all box blocks; participants inside a boundary appear inside the corresponding `box ... end` block:

```
sequenceDiagram

    %% Stereotypes: [ActorName]=actor | [BoundaryParticipant]=boundary, [ControlParticipant1]=control, [ControlParticipant2]=control, [EntityParticipant1]=entity

    %% External participants (actors) — outside all boundaries
    participant [ActorName] as "[Human-readable Actor Label]"

    %% Boundary: [BoundaryName]
    box "[BoundaryName]"
        participant [BoundaryParticipant] as "[Label]"
        participant [ControlParticipant1] as "[Label]"
        participant [ControlParticipant2] as "[Label]"
        participant [EntityParticipant1] as "[Label]"
    end

    %% Interactions
    [ActorName]->>[BoundaryParticipant]: [Action]
    ...
```

**Generation rules:**
- All `actor`-type participants are emitted **before** any `box` block
- Each boundary produces exactly one `box "[BoundaryName]" ... end` block — always quote the label
- Box blocks are separated by a blank line plus a `%% Boundary:` comment for readability
- **MANDATORY**: Include a `%% Stereotypes:` comment listing every participant's type
- **MANDATORY**: Use `participant [Alias] as "[Label]"` syntax — NEVER use `@{ ... }` JSON metadata
- **MANDATORY**: Participants inside each `box` must follow strict ordering: `boundary` first, then `control`, then `entity` (see Participant Ordering Within a Box)
- **MANDATORY**: Box blocks are ordered by first interaction received from the actor — boundaries that receive the actor's first message come first
- Mermaid does not support nested `box` blocks; decomposition to sub-boundaries is expressed through separate diagrams linked by decomposition references

### Participant Ordering Within a Box

Participants inside each `box` block must follow a strict ordering to satisfy EDPS boundary rules and produce readable diagrams:

| Order | Stereotype | Rationale |
|-------|-----------|-----------|
| 1st | `boundary` | First recipient of actor messages; entry point to boundary |
| 2nd–Nth | `control` | Business logic components; eligible for further decomposition |
| Last | `entity` | Data / resource stores; passive, no first-message routing needed |

**Example of correct ordering:**
```
box "Payment Service Boundary"
    participant Gateway as "Payment Gateway"
    participant Processor as "Transaction Processor"
    participant Validator as "Payment Validator"
    participant Ledger as "Transaction Ledger"
end
```

If a boundary contains **no** `boundary`-type participant, emit a validation warning and list all `control` participants first, followed by `entity` participants.

### Multi-Boundary Generation

Multiple non-overlapping boundaries are supported in a single sequence diagram. Each gets its own `box` block, declared in order of first interaction:

```
sequenceDiagram

    %% Stereotypes: Customer=actor | Web=boundary, Order=control, Inventory=control, CustomerDB=entity | PayAPI=boundary, TxProcessor=control, Ledger=entity | FulfillAPI=boundary, Warehouse=control, Shipment=entity
    participant Customer as "Customer"

    %% Boundary: E-commerce Platform
    box "E-commerce Platform Boundary"
        participant Web as "Web Frontend"
        participant Order as "Order Service"
        participant Inventory as "Inventory Service"
        participant CustomerDB as "Customer Database"
    end

    %% Boundary: Payment System
    box "Payment System Boundary"
        participant PayAPI as "Payment API"
        participant TxProcessor as "Transaction Processor"
        participant Ledger as "Transaction Ledger"
    end

    %% Boundary: Fulfillment Center
    box "Fulfillment Center Boundary"
        participant FulfillAPI as "Fulfillment API"
        participant Warehouse as "Warehouse Manager"
        participant Shipment as "Shipment Record"
    end

    Customer->>Web: Place Order
    Web->>Order: Create Order
    Order->>PayAPI: Process Payment
    Order->>FulfillAPI: Schedule Delivery
```

**Multi-boundary constraints:**
- Participants cannot belong to more than one boundary block
- Boundaries must be non-overlapping; if a conflict is detected during generation, report a validation error
- Recommended maximum of **5 boundaries** per diagram for readability; beyond 5, consider splitting into multiple diagrams
- Order of `box` blocks follows the sequence of first message receipt by each boundary

### Boundary Naming Conventions

Boundary names are derived automatically from context using the following priority order:

| Priority | Source | Example Output |
|----------|--------|----------------|
| 1 | Manual `name` in input configuration | `"Payment Gateway"` → `Payment Gateway` |
| 2 | Domain concept name + `" Boundary"` suffix | concept `OrderManagement` → `Order Management Boundary` |
| 3 | Dominant participant name + type suffix | primary control `CreditChecker` → `Credit Check Service Boundary` |
| 4 | Functional role inference from participant names | names contain `inventory`, `stock` → `Inventory Management Boundary` |
| 5 | Generic fallback with ordinal | `System Boundary 1`, `System Boundary 2` |

**Naming formatting rules:**
- Use Title Case for all boundary names
- Append `" Boundary"` suffix to system/component names; omit suffix for naturally scoped phrases that are already descriptive (e.g., `E-commerce Platform`)
- Avoid acronyms unless they are widely understood in the project domain
- Maximum name length: 50 characters; truncate with `...` if exceeded

### Boundary Color and Styling

Boundaries support optional color customization. Colors are applied via Mermaid's `box` color parameter:

```
box rgb(235, 245, 255) "E-commerce Platform Boundary"
    participant Web as "Web Frontend"
    ...
end
```

**Default color palette (applied round-robin when `auto_color: true`):**

| Boundary Index | Color | RGB Value | Semantic Meaning |
|---------------|-------|-----------|-----------------|
| 1st boundary | Light blue | `rgb(235, 245, 255)` | Primary system |
| 2nd boundary | Light green | `rgb(235, 255, 240)` | Secondary system |
| 3rd boundary | Light amber | `rgb(255, 250, 235)` | Supporting system |
| 4th boundary | Light lavender | `rgb(245, 235, 255)` | Integration layer |
| 5th+ boundary | Light grey | `rgb(245, 245, 245)` | Additional systems |

**Styling configuration:**
```json
{
  "boundary_styling": {
    "auto_color": true,
    "manual_colors": {
      "Payment System Boundary": "rgb(255, 243, 224)",
      "Security Boundary": "rgb(255, 235, 235)"
    }
  }
}
```

When `auto_color: false` (default) and no `manual_colors` are provided, the `box` keyword is used without a color parameter.

### Boundary Summary Comments

When `generate_boundary_comments: true` is set (recommended), the skill inserts structured comments into the Mermaid output to improve readability and navigation:

```
sequenceDiagram
    %% ─────────────────────────────────────────────────────
    %% BOUNDARY SUMMARY
    %% ─────────────────────────────────────────────────────    
    %% [B-1] E-commerce Platform Boundary
    %%         Participants: Web Frontend (boundary), Order Service (control),
    %%                       Inventory Service (control), Customer Database (entity)
    %%         Decomposable: Order Service, Inventory Service
    %%         External actor: Customer
    %%
    %% [B-2] Payment System Boundary
    %%         Participants: Payment API (boundary), Transaction Processor (control),
    %%                       Transaction Ledger (entity)
    %%         Decomposable: Transaction Processor
    %%         External actor: none (called from E-commerce Platform)
    %% ─────────────────────────────────────────────────────

    participant Customer as "Customer"

    %% [B-1] E-commerce Platform Boundary
    box "E-commerce Platform Boundary"
        ...
    end

    %% [B-2] Payment System Boundary
    box "Payment System Boundary"
        ...
    end
```

### Edge Case Handling

| Edge Case | Detection | Handling |
|-----------|-----------|----------|
| **Single participant boundary** | Only one participant inside a `box` block | Emit a warning in metadata; still generate the box; suggest merging with a related boundary |
| **External participants between boxes** | Participants not assigned to any boundary | Declare outside all `box` blocks; include in `external_participants` metadata list |
| **No `boundary`-type participant in box** | Box contains only `control`/`entity` participants | Emit validation warning; list controls first, entities last; add `%% WARNING: No boundary-type entry point` comment inside the box |
| **Empty boundary** | Boundary configured with zero participants | Skip generation; emit error `empty-boundary-skipped` in metadata |
| **Duplicate participant across boundaries** | Same participant ID appears in two boxes | Emit validation error `duplicate-participant`; use first boundary assignment; suggest renaming |
| **More than 5 boundaries** | `boundary_count > 5` | Emit readability warning; continue generation; recommend splitting into multiple diagrams |

### Box Syntax Configuration Parameters

```json
{
  "box_syntax": {
    "enabled": true,
    "participant_ordering": "boundary-control-entity",
    "generate_boundary_comments": true,
    "boundary_naming": {
      "strategy": "domain-concept-first",
      "suffix": "Boundary",
      "title_case": true
    },
    "boundary_styling": {
      "auto_color": false,
      "manual_colors": {}
    },
    "validation": {
      "enforce_participant_ordering": true,
      "warn_single_participant_boundary": true,
      "error_on_empty_boundary": true,
      "warn_no_boundary_type_entry_point": true,
      "error_on_duplicate_participant": true,
      "warn_exceeds_boundary_count": 5
    }
  }
}
```

### Box Syntax Metadata Output

After box syntax generation the skill emits a `box_syntax_metadata` block in `collaboration-diagrams.json`:

```json
{
  "box_syntax_metadata": {
    "total_boundaries": 3,
    "boundaries": [
      {
        "id": "B-1",
        "name": "E-commerce Platform Boundary",
        "color": null,
        "participants": {
          "boundary": ["Web"],
          "control": ["Order", "Inventory"],
          "entity": ["CustomerDB"]
        },
        "decomposable_participants": ["Order", "Inventory"],
        "external_actors": ["Customer"],
        "warnings": []
      },
      {
        "id": "B-2",
        "name": "Payment System Boundary",
        "color": null,
        "participants": {
          "boundary": ["PayAPI"],
          "control": ["TxProcessor"],
          "entity": ["Ledger"]
        },
        "decomposable_participants": ["TxProcessor"],
        "external_actors": [],
        "warnings": []
      }
    ],
    "external_participants": [],
    "validation_errors": [],
    "validation_warnings": []
  }
}
```
