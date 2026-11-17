# Process Level Tracking and Scale Management

Analyse a collaboration diagram at any hierarchy level to calculate complexity metrics, issue warnings, and identify decomposition candidates. This section is invoked automatically after every decomposition and can also be triggered explicitly by the user.

### Default Thresholds

| Setting | Default | Description |
|---------|---------|-------------|
| `level_0_max_interactions` | 7 | Maximum interactions before Level 0 diagram is flagged |
| `level_n_max_interactions` | 12 | Maximum interactions before Level N (N ≥ 1) diagram is flagged |
| `decomposition_candidate_min_interactions` | 5 | Minimum interactions for a control-type participant to be listed as a candidate |
| Advisory trigger | 80 % of max | Interaction count ≥ 80 % of threshold triggers an advisory warning |

Thresholds can be overridden per hierarchy by setting `complexity_thresholds` in `hierarchy-metadata.json` (see [references/hierarchy-metadata-schema.md](references/hierarchy-metadata-schema.md)).

### Complexity Metrics Calculation

For a given `collaboration.md`, count:

1. **`interaction_count`** — total number of message arrows (`->>`, `-->>`, `-x`, `-->`, `=>>`, ...) in the Mermaid `sequenceDiagram` block. Each arrow counts as one interaction regardless of direction.
2. **`participant_count`** — number of `participant` declarations in the Mermaid `sequenceDiagram` block.
3. **`nesting_depth`** — number of nested `box … end` blocks at the deepest level (a `box` inside a `box` = depth 2).

### Warning Levels

| Level | Condition | Severity |
|-------|-----------|----------|
| `none` | interaction_count ≤ threshold | No action needed |
| `advisory` | interaction_count ≥ ⌊threshold × 0.8⌋ but ≤ threshold | Consider decomposing soon |
| `critical` | interaction_count > threshold | Decomposition recommended |

**Warning message format:**

```
⚠ [ADVISORY|CRITICAL] Scale warning — [process-folder]/collaboration.md (Level [N])
  Interaction count: [actual] / [threshold] (threshold: [level_0|level_n]_max_interactions = [value])
  Action: [Consider|Recommend] decomposing one or more control-type participants.
```

**Examples:**

```
⚠ ADVISORY  Scale warning — 01-EcommercePlatformBoundary/collaboration.md (Level 0)
  Interaction count: 6 / 7 (threshold: level_0_max_interactions = 7)
  Action: Consider decomposing one or more control-type participants.

⚠ CRITICAL  Scale warning — 01-EcommercePlatformBoundary/01-OrderManagementBoundary/collaboration.md (Level 1)
  Interaction count: 14 / 12 (threshold: level_n_max_interactions = 12)
  Action: Recommend decomposing one or more control-type participants.
```

### Decomposition Candidate Identification

After calculating `interaction_count` per participant:

1. For each control-type participant in the diagram, count the number of message arrows **involving** that participant (as sender or receiver).
2. If a participant's involvement count ≥ `decomposition_candidate_min_interactions`, add it to `decomposition_candidates`.
3. Sort candidates by involvement count descending.

**Candidate report format:**

```
🔍 Decomposition Candidates — [process-folder]/collaboration.md (Level [N])
  [ParticipantName]  ([involvement_count] interactions, type: control)  ← highest priority
  [ParticipantName2] ([involvement_count2] interactions, type: control)
```

If no candidates are found:

```
✓ No decomposition candidates identified at this level.
```

### Scale Management Analysis Workflow

When invoked (automatically post-decomposition or on user request):

1. **Read** `collaboration.md` for the target level.
2. **Count** `interaction_count`, `participant_count`, and `nesting_depth`.
3. **Determine warning level** using thresholds from `hierarchy-metadata.json` (or defaults if absent).
4. **Identify decomposition candidates** among control-type participants.
5. **Update** the node's `complexity_metrics` object in `hierarchy-metadata.json`.
6. **Recompute** `hierarchy_statistics.scale_management` aggregates:
   - `critical_warnings` — list of node ids with `complexity_warning = "critical"`
   - `advisory_warnings` — list of node ids with `complexity_warning = "advisory"`
   - `decomposition_candidates` — union of all candidate lists across all nodes
   - `total_interactions_by_level` — sum of `interaction_count` per level
7. **Report** warnings and candidates to the user.

### Hierarchy Depth and Breadth Tracking

In addition to per-node metrics, maintain these hierarchy-wide statistics in `hierarchy_statistics`:

| Field | Description |
|-------|-------------|
| `max_depth` | Deepest level index (0-based) |
| `breadth_at_deepest_level` | Number of nodes at the deepest level |
| `boundary_count` | Total number of boundary-type nodes across all levels |
| `nodes_by_level` | Map of level index → node count |

When the user requests a depth/breadth summary, output:

```
📊 Hierarchy Scale Summary — [root process name]
  Total Levels:       [max_depth + 1]
  Total Processes:    [total_nodes]
  Leaf Processes:     [leaf_count]
  Boundary Nodes:     [boundary_count]
  Decomposed Nodes:   [decomposed_count]
  Available to Decompose: [available_count]
  Breadth at Deepest Level: [breadth_at_deepest_level]

  Scale Warnings:
    Critical: [critical_warnings count] ([list of node ids])
    Advisory: [advisory_warnings count] ([list of node ids])

  Decomposition Candidates (across all levels):
    [list of candidate node ids with involvement counts]
```

### Configuring Thresholds

To override the default thresholds for a hierarchy, add or update `complexity_thresholds` in `hierarchy-metadata.json`:

```json
"complexity_thresholds": {
  "level_0_max_interactions": 10,
  "level_n_max_interactions": 15,
  "decomposition_candidate_min_interactions": 4
}
```

After saving, re-run scale management analysis on all levels to recalculate warnings with the new thresholds.

---

## Hierarchy Statistics

When the user asks for statistics, compute from `hierarchy-metadata.json` and report:

| Metric | Value |
|--------|-------|
| Max Depth | Deepest level in the tree |
| Total Nodes | All process nodes (all levels) |
| Leaf Nodes | Nodes with no children |
| Decomposed Nodes | Nodes with `status: "decomposed"` |
| Available to Decompose | Nodes with `status: "available"` and `type: "control"` |
| Breadth at Deepest Level | Count of nodes at max depth |
