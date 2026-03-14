# Hierarchy Metadata Schema

## Table of Contents
1. [Schema Overview](#schema-overview)
2. [Top-Level Fields](#top-level-fields)
3. [Node Object](#node-object)
4. [Hierarchy Statistics](#hierarchy-statistics)
5. [Example Document](#example-document)
6. [Update Rules](#update-rules)

---

## Schema Overview

`hierarchy-metadata.json` tracks the full process decomposition tree rooted at a given process folder. One file lives at the root level; sub-folders may have their own scoped copies.

---

## Top-Level Fields

```json
{
  "schema_version": "1.0",
  "root_process": {
    "id": "string — unique process identifier (slug, e.g. 'customer-order-journey')",
    "name": "string — human-readable process name",
    "folder": "string — relative path to root folder",
    "level": 0
  },
  "generated_at": "ISO8601 timestamp",
  "last_updated": "ISO8601 timestamp",
  "nodes": { },
  "hierarchy_statistics": { }
}
```

---

## Node Object

Each key in `nodes` is the participant's identifier (PascalCase slug). Each value:

```json
{
  "id": "string — PascalCase slug, e.g. 'OrderService'",
  "label": "string — human-readable display name, e.g. 'Order Management Service'",
  "type": "actor | boundary | control | entity",
  "level": "number — 0-based depth in hierarchy",
  "status": "available | decomposed | leaf",
  "folder": "string — relative path to this node's folder (null for non-decomposed nodes)",
  "parent_id": "string | null — id of parent node (null for root)",
  "children": ["array of child node ids"],
  "source_diagram": "string — relative path to the collaboration.md where this participant is defined",
  "decomposition_link": "string | null — relative path to child collaboration.md (set when status=decomposed)"
}
```

**Status values:**
- `available` — control-type, not yet decomposed; eligible for decomposition
- `decomposed` — decomposed into a child sub-process
- `leaf` — non-control type (actor, boundary, entity) or a control that will not be further decomposed

---

## Hierarchy Statistics

```json
{
  "hierarchy_statistics": {
    "total_nodes": "number",
    "max_depth": "number — deepest level index",
    "leaf_count": "number — nodes with no children",
    "decomposed_count": "number — nodes with status='decomposed'",
    "available_count": "number — control nodes with status='available'",
    "nodes_by_level": {
      "0": "number",
      "1": "number",
      "2": "number"
    },
    "breadth_at_deepest_level": "number"
  }
}
```

---

## Example Document

```json
{
  "schema_version": "1.0",
  "root_process": {
    "id": "customer-order-journey",
    "name": "Customer Order Journey",
    "folder": "01-CustomerOrderJourney",
    "level": 0
  },
  "generated_at": "2026-03-14T10:00:00Z",
  "last_updated": "2026-03-14T12:30:00Z",
  "nodes": {
    "Customer": {
      "id": "Customer",
      "label": "Customer",
      "type": "actor",
      "level": 0,
      "status": "leaf",
      "folder": null,
      "parent_id": null,
      "children": [],
      "source_diagram": "collaboration.md",
      "decomposition_link": null
    },
    "ECommercePlatform": {
      "id": "ECommercePlatform",
      "label": "E-commerce Platform",
      "type": "control",
      "level": 0,
      "status": "decomposed",
      "folder": "01-EcommercePlatformBoundary",
      "parent_id": null,
      "children": ["WebFrontend", "CartService", "OrderService", "InventoryService"],
      "source_diagram": "collaboration.md",
      "decomposition_link": "01-EcommercePlatformBoundary/collaboration.md"
    },
    "WebFrontend": {
      "id": "WebFrontend",
      "label": "Web Frontend",
      "type": "boundary",
      "level": 1,
      "status": "leaf",
      "folder": null,
      "parent_id": "ECommercePlatform",
      "children": [],
      "source_diagram": "01-EcommercePlatformBoundary/collaboration.md",
      "decomposition_link": null
    },
    "OrderService": {
      "id": "OrderService",
      "label": "Order Management Service",
      "type": "control",
      "level": 1,
      "status": "decomposed",
      "folder": "01-EcommercePlatformBoundary/01-OrderManagementBoundary",
      "parent_id": "ECommercePlatform",
      "children": ["OrderAPI", "OrderValidator", "OrderEngine", "OrderRepository"],
      "source_diagram": "01-EcommercePlatformBoundary/collaboration.md",
      "decomposition_link": "01-EcommercePlatformBoundary/01-OrderManagementBoundary/collaboration.md"
    },
    "CartService": {
      "id": "CartService",
      "label": "Shopping Cart Service",
      "type": "control",
      "level": 1,
      "status": "available",
      "folder": null,
      "parent_id": "ECommercePlatform",
      "children": [],
      "source_diagram": "01-EcommercePlatformBoundary/collaboration.md",
      "decomposition_link": null
    },
    "OrderAPI": {
      "id": "OrderAPI",
      "label": "Order API",
      "type": "boundary",
      "level": 2,
      "status": "leaf",
      "folder": null,
      "parent_id": "OrderService",
      "children": [],
      "source_diagram": "01-EcommercePlatformBoundary/01-OrderManagementBoundary/collaboration.md",
      "decomposition_link": null
    },
    "OrderEngine": {
      "id": "OrderEngine",
      "label": "Order Processing Engine",
      "type": "control",
      "level": 2,
      "status": "available",
      "folder": null,
      "parent_id": "OrderService",
      "children": [],
      "source_diagram": "01-EcommercePlatformBoundary/01-OrderManagementBoundary/collaboration.md",
      "decomposition_link": null
    }
  },
  "hierarchy_statistics": {
    "total_nodes": 7,
    "max_depth": 2,
    "leaf_count": 4,
    "decomposed_count": 2,
    "available_count": 2,
    "nodes_by_level": {
      "0": 2,
      "1": 4,
      "2": 4
    },
    "breadth_at_deepest_level": 4
  }
}
```

---

## Update Rules

When a decomposition is performed, update `hierarchy-metadata.json` as follows:

1. **Parent node**: set `status` → `"decomposed"`, set `folder`, set `decomposition_link`, append child IDs to `children`
2. **New child nodes**: add one node entry per participant in the new sub-process diagram (using stereotype classification to assign `type`)
3. **Statistics**: recompute all `hierarchy_statistics` fields from the updated `nodes` map
4. **`last_updated`**: set to current ISO8601 timestamp

When a rollback is performed:
1. Remove all child node entries that were added by the decomposition
2. Reset parent node: `status` → `"available"`, `folder` → `null`, `decomposition_link` → `null`, `children` → `[]`
3. Recompute `hierarchy_statistics`
4. Update `last_updated`
