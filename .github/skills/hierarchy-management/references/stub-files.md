# Stub File Specification

When `hierarchy-management` creates a new sub-process folder, it writes **stub files only** — minimal-content placeholders that are syntactically valid Markdown and Mermaid but contain no generated process knowledge. Stub files pass `hierarchy-validation` rule HN-2 (Required Files Present) immediately after creation.

Full content generation is exclusively the responsibility of `documentation-automation`. Once `documentation-automation` has run, it replaces these stubs with content-complete documents.

**Machine-detectable stub marker**: Every stub file contains the exact substring `[TO BE GENERATED - invoke documentation-automation]`. The Content Guard in `documentation-automation` uses this substring to distinguish stubs from generated files.

### `main.md` Stub

```markdown
# [ParticipantName] Boundary

**Level**: [N+1]  
**Parent Process**: [[ParentProcessName]](../main.md)  
**Status**: Draft

## System Boundary

- **Boundary ID**: `BND-[NN]-[ParticipantName]`
- **Boundary Type**: `unknown` — **[ACTION REQUIRED]** confirm whether this boundary is `software` or `non-software`, then replace this line. See the [cross-model alignment contract](../model-validatealignment/references/cross-model-alignment-contract.md) Section 2.1.
- **Hierarchy Path**: `[relative path from orgModel process root]`
- **Parent Boundary ID**: `[parent's Boundary ID, or "none" at hierarchy root]`
- **Corresponds To Participant**: `[ParticipantName]` (control-type, decomposed per HV-1 in parent's collaboration.md)

## Navigation

**Breadcrumb**: [TO BE GENERATED - invoke documentation-automation]

**Parent Process**: [[ParentProcessName]](../main.md)

**Sub-Processes**: [TO BE GENERATED - invoke documentation-automation]

## Overview

[TO BE GENERATED - invoke documentation-automation]

## Collaboration Diagram

See [collaboration.md](collaboration.md)

## Process Flow

See [process.md](process.md)

## Domain Model

See [domain-model.md](domain-model.md)

## Sub-Processes

[TO BE GENERATED - invoke documentation-automation]
```

### `process.md` Stub

```markdown
<!-- Identifier: P-[NN] -->

# [ParticipantName] Boundary — Process Flow

**Hierarchy Level**: [N+1]

[TO BE GENERATED - invoke documentation-automation]
```

### `collaboration.md` Stub

```markdown
# [ParticipantName] Boundary — Level [N+1]

**Parent Process**: [[ParentProcessName]](../collaboration.md)  
**Hierarchy Level**: [N+1]  
**Decomposed From**: `[ParticipantName]` ([parent folder name])  
**Diagram Status**: [TO BE GENERATED - invoke documentation-automation]

```mermaid
sequenceDiagram
    %% TO BE GENERATED — invoke documentation-automation to populate this diagram
```

**Source Requirements**: [TBD]
```

### `domain-model.md` Stub

```markdown
<!-- Identifier: D-[NN] -->

# [ParticipantName] Boundary — Domain Model

**Hierarchy Level**: [N+1]  
**Diagram Status**: [TO BE GENERATED - invoke documentation-automation]

```mermaid
classDiagram
    %% TO BE GENERATED — invoke documentation-automation to populate this diagram
```
```
