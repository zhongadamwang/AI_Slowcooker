# Boundary Validation

This section defines the complete set of boundary validation rules, the two execution modes (strict vs advisory), and the machine-readable validation report format emitted by the skill. Boundary validation runs as a **pre-render check** after participant classification and box syntax generation, and before final Mermaid output is written.

### Overview

All hierarchical collaboration diagrams produced by this skill are validated against four EDPS boundary rules. Each rule can independently raise an **error** (hard violation) or a **warning** (advisory issue) depending on the active mode.

| Rule ID | Rule Name | Default Severity |
|---------|-----------|-----------------|
| VR-1 | Single External Interface | Error |
| VR-2 | Boundary-First Reception | Error |
| VR-3 | Control-Only Decomposition | Error |
| VR-4 | Cohesive Responsibility | Warning |

---

### Rule VR-1: Single External Interface

**Requirement**: Each boundary must have exactly one external actor sending messages directly into it. Multiple external actors communicating directly with internal boundary participants violates EDPS encapsulation principles.

**Valid:**
```
Customer (actor) ->> API (boundary) [inside Order Boundary]
```

**Invalid:**
```
Customer (actor)  ->> API     [inside Order Boundary]  ✅
Admin (actor)     ->> Service [inside Order Boundary]  ❌  second actor enters boundary directly
```

**Detection logic:**
- Collect all message senders that are `actor`-type and outside the boundary
- If `count(distinct external actors sending into boundary) > 1` → violation

**Validation output on violation:**
```json
{
  "rule": "VR-1",
  "rule_name": "single-external-interface",
  "severity": "error",
  "boundary": "Order Processing Boundary",
  "actors_found": ["Customer", "Admin"],
  "message": "Boundary 'Order Processing Boundary' is accessed by 2 external actors (Customer, Admin). Only one external actor may interact directly with a boundary.",
  "suggestion": "Split into two separate boundaries — one per external actor — or introduce a shared entry-point gateway that aggregates actor messages before forwarding into a single boundary."
}
```

---

### Rule VR-2: Boundary-First Reception

**Requirement**: Within any `box` boundary, the first message sent from an external actor must be received by a `boundary`-type participant. Actors must not bypass the boundary-type entry point and send directly to `control` or `entity` participants.

**Valid:**
```
Customer (actor) ->> Gateway (boundary) ->> OrderService (control)
```

**Invalid:**
```
Customer (actor) ->> OrderService (control)   ❌  skips boundary-type entry point
```

**Detection logic:**
- For each boundary, identify the first inbound message from an external actor
- Check the receiver's type; if it is not `boundary` → violation

**Validation output on violation:**
```json
{
  "rule": "VR-2",
  "rule_name": "boundary-first-reception",
  "severity": "error",
  "boundary": "Order Processing Boundary",
  "actor": "Customer",
  "received_by": "OrderService",
  "received_by_type": "control",
  "message": "Actor 'Customer' sends directly to 'OrderService' (type: control) inside boundary 'Order Processing Boundary'. The first recipient inside a boundary must be a boundary-type participant.",
  "suggestion": "Add or designate a boundary-type participant (e.g., 'Order API' or 'Order Portal') as the single entry point. Route the actor message through that participant first."
}
```

---

### Rule VR-3: Control-Only Decomposition

**Requirement**: Only participants with `type: control` may be decomposed into sub-process diagrams. Attempting to decompose an `actor`, `boundary`, or `entity` participant is a structural violation.

**Valid:**
```
decompose: OrderService (control)  ✅
```

**Invalid:**
```
decompose: OrderDB (entity)        ❌
decompose: API (boundary)          ❌
decompose: Customer (actor)        ❌
```

**Detection logic:**
- For each participant listed in `decomposable` or referenced as a sub-diagram root
- If participant type ≠ `control` → violation

**Validation output on violation:**
```json
{
  "rule": "VR-3",
  "rule_name": "control-only-decomposition",
  "severity": "error",
  "participant": "OrderDB",
  "participant_type": "entity",
  "message": "Cannot decompose participant 'OrderDB' (type: entity). Only control-type participants are eligible for sub-process decomposition.",
  "suggestion": "If this participant requires internal detail, reclassify it as 'control', or model its internal structure as a separate entity-relationship class diagram rather than a process decomposition."
}
```

---

### Rule VR-4: Cohesive Responsibility

**Requirement**: All participants grouped inside a `box` boundary should share related functionality or capability. Mixing unrelated concerns (e.g., database queries, email sending, and user authentication) inside a single boundary is a cohesion violation.

**Detection logic (heuristic):**
- Extract domain area tags or functional keywords from each participant's label and domain-concept entry
- Compute pairwise similarity across participants in the boundary
- If `min_cohesion_score < 0.3` (configurable) → warning
- Cohesion check is advisory by default; it does not block diagram generation

**Validation output on violation:**
```json
{
  "rule": "VR-4",
  "rule_name": "cohesive-responsibility",
  "severity": "warning",
  "boundary": "Mixed Services Boundary",
  "participants": ["QueryEngine", "EmailSender", "AuthHandler"],
  "cohesion_score": 0.18,
  "message": "Boundary 'Mixed Services Boundary' contains participants with unrelated functional concerns (query, email, authentication). Low cohesion score: 0.18.",
  "suggestion": "Refactor into separate boundaries — e.g., 'Data Access Boundary' (QueryEngine), 'Notification Boundary' (EmailSender), 'Security Boundary' (AuthHandler) — to enforce single-responsibility encapsulation."
}
```

---

### Validation Modes

The boundary validation pipeline supports two modes controlling how violations affect diagram generation:

#### Strict Mode (`validation_mode: "strict"`)
- **Errors** (VR-1, VR-2, VR-3 violations) **block** diagram generation
- The skill returns a validation report and does **not** produce Mermaid output
- Displays a clear error message identifying which rule was violated and where
- **Warnings** (VR-4 violations) are included in the report but do not block output
- Use this mode in automated pipelines or CI/CD environments where diagram correctness is mandatory

#### Advisory Mode (`validation_mode: "advisory"`)  *(default)*
- All violations (errors and warnings) are **reported** but do **not** block diagram generation
- Mermaid output is generated; validation findings are embedded as structured comments inside the output and in the JSON report
- Violation comments are injected inline in the Mermaid source at the point of violation:
  ```
  %% [VR-2 ERROR] Actor 'Customer' bypasses boundary-type entry point → OrderService (control)
  Customer->>OrderService: Place Order
  ```
- Use this mode during iterative modeling sessions where diagrams may be intentionally incomplete

**Mode configuration:**
```json
{
  "boundary_validation": {
    "validation_mode": "advisory",
    "rules": {
      "VR-1": { "enabled": true, "severity": "error" },
      "VR-2": { "enabled": true, "severity": "error" },
      "VR-3": { "enabled": true, "severity": "error" },
      "VR-4": { "enabled": true, "severity": "warning", "cohesion_threshold": 0.3 }
    }
  }
}
```

---

### Validation Report Format

After validation the skill emits a `boundary_validation_report` block in `collaboration-diagrams.json` and a matching markdown summary in `collaboration-diagrams.md`.

#### Machine-Readable JSON Report

```json
{
  "boundary_validation_report": {
    "validation_mode": "advisory",
    "validated_at": "2026-03-14T10:00:00Z",
    "overall_status": "PASS_WITH_WARNINGS",
    "summary": {
      "total_boundaries_checked": 3,
      "passed": 2,
      "failed": 0,
      "warnings": 1,
      "errors": 0
    },
    "rule_results": [
      {
        "rule": "VR-1",
        "rule_name": "single-external-interface",
        "status": "PASS",
        "boundaries_checked": 3,
        "violations": []
      },
      {
        "rule": "VR-2",
        "rule_name": "boundary-first-reception",
        "status": "PASS",
        "boundaries_checked": 3,
        "violations": []
      },
      {
        "rule": "VR-3",
        "rule_name": "control-only-decomposition",
        "status": "PASS",
        "participants_checked": 7,
        "violations": []
      },
      {
        "rule": "VR-4",
        "rule_name": "cohesive-responsibility",
        "status": "WARNING",
        "boundaries_checked": 3,
        "violations": [
          {
            "severity": "warning",
            "boundary": "Mixed Services Boundary",
            "participants": ["QueryEngine", "EmailSender", "AuthHandler"],
            "cohesion_score": 0.18,
            "message": "Boundary 'Mixed Services Boundary' contains participants with unrelated functional concerns.",
            "suggestion": "Refactor into separate boundaries by functional domain."
          }
        ]
      }
    ],
    "blocking_errors": [],
    "diagram_generation_blocked": false
  }
}
```

**`overall_status` values:**

| Status | Meaning |
|--------|---------|
| `PASS` | All rules passed with no violations |
| `PASS_WITH_WARNINGS` | No errors; one or more warnings |
| `FAIL` | One or more error-level violations (only in strict mode blocks generation) |
| `BLOCKED` | Diagram generation blocked due to errors in strict mode |

#### Markdown Validation Summary

The skill embeds a formatted validation summary section in `collaboration-diagrams.md` directly above the first diagram:

```markdown
## Boundary Validation Summary

**Validated**: 2026-03-14T10:00:00Z  
**Mode**: Advisory  
**Overall Status**: ⚠️ PASS WITH WARNINGS

| Rule | Name | Status | Details |
|------|------|--------|---------|
| VR-1 | Single External Interface | ✅ PASS | 3 boundaries checked |
| VR-2 | Boundary-First Reception | ✅ PASS | 3 boundaries checked |
| VR-3 | Control-Only Decomposition | ✅ PASS | 7 participants checked |
| VR-4 | Cohesive Responsibility | ⚠️ WARNING | 1 boundary has low cohesion |

### Warnings

**[VR-4] Cohesive Responsibility — Mixed Services Boundary**  
Participants with unrelated concerns: QueryEngine, EmailSender, AuthHandler (cohesion score: 0.18)  
*Suggestion*: Refactor into separate boundaries by functional domain.
```

---

### Validation Configuration Parameters

```json
{
  "boundary_validation": {
    "enabled": true,
    "validation_mode": "advisory",
    "inject_inline_comments": true,
    "generate_markdown_summary": true,
    "rules": {
      "VR-1": {
        "enabled": true,
        "severity": "error",
        "description": "Each boundary must have exactly one external actor interface"
      },
      "VR-2": {
        "enabled": true,
        "severity": "error",
        "description": "Boundary-type participant must be first recipient of actor messages"
      },
      "VR-3": {
        "enabled": true,
        "severity": "error",
        "description": "Only control-type participants may be decomposed"
      },
      "VR-4": {
        "enabled": true,
        "severity": "warning",
        "cohesion_threshold": 0.3,
        "description": "All boundary participants should share related functional concerns"
      }
    }
  }
}
```

---

### Validation Pipeline Integration

Boundary validation is integrated into the diagram generation pipeline at the **pre-render** stage:

```
1. Input Analysis              ← load domain-concepts.json + requirements.json
2. Participant Classification  ← stereotype inference + manual overrides
3. Box Syntax Generation       ← generate box blocks with participant ordering
4. ► Boundary Validation ◄     ← run VR-1 through VR-4 against generated structure
     ├── strict mode  → block generation on errors; return validation report only
     └── advisory mode → annotate output with violations; continue generation
5. Mermaid Output Generation   ← render final diagram with optional violation comments
6. Validation Report Emit      ← write boundary_validation_report to JSON + markdown
```
