# FAQ and Troubleshooting

**Project**: 03-Building-Skills-Iteration-2  
**Version**: 1.0  
**Created**: March 15, 2026

---

## Frequently Asked Questions

### Concepts

---

**Q: What is a "boundary" in EDPS?**

A boundary is a named group of participants in a collaboration diagram that together fulfill a shared responsibility. A boundary has exactly one external interface: one `<<Actor>>` participant may send messages into it. Internally, participants collaborate freely. In Mermaid, a boundary is represented using the `box ... end` block.

---

**Q: When should I create a new hierarchy level?**

Create a Level N+1 diagram when:
- A `<<System>>` (`control`) participant in the current diagram contains logic complex enough to warrant its own collaboration story
- A team member asks "what happens inside `<X>`?"
- The number of interactions at the current level would increase significantly if you flattened the internals  

As a guideline: when internal detail would push a diagram past ~8 meaningful message exchanges, it is worth decomposing.

---

**Q: How deep should the hierarchy go?**

There is no hard limit. In practice, 2–3 levels covers most systems. Stop decomposing when:
- The sub-process has 2–3 participants with straightforward interactions
- The logic is implementation-detail rather than process-level design
- The team already understands the internals without a diagram

---

**Q: Can a `<<UI>>` participant be decomposed?**

No. `<<UI>>` (boundary type) participants are thin interface layers. They do not contain complex business logic and are not decomposed in EDPS. If a "UI" participant turns out to host significant logic, reclassify it as `<<System>>`.

---

**Q: Can I have two `<<UI>>` (`boundary` type) participants in the same box?**

Yes, but only one of them should receive the external actor's first message (enforced by VR-2). Additional `boundary`-type participants can exist inside a box as secondary mediators, but they should receive messages only from internal participants, not directly from an external actor.

---

**Q: What if an entity needs to send a message first (e.g., a scheduled job)?**

Scheduled triggers are not entities. Model them as a separate `<<System>>` component (e.g., a Scheduler or Poller) that wraps the timer logic and relays it forward. The triggered entity remains passive.

---

**Q: Can a `<<System>>` participant appear at Level 0 without a box?**

Yes. At Level 0, top-level system boundaries appear as plain `control`-type participants (no `box` syntax). Level 0 establishes the high-level external contracts before any internal decomposition is shown.

---

**Q: What is the difference between `<<System>>` and `<<UI>>`?**

| | `<<System>>` | `<<UI>>` |
|---|---|---|
| Mermaid type | `control` | `boundary` |
| Decomposable | Yes | No |
| First recipient in box | Never | Always |
| Role | Business logic | Interface/mediation |

Use `<<UI>>` when the participant's sole job is to receive requests from outside and translate them for internal consumption. Use `<<System>>` when the participant processes, orchestrates, or transforms.

---

### Mermaid Syntax

---

**Q: My diagram is not rendering — what should I check first?**

1. Confirm the opening line is `sequenceDiagram` (no trailing space or typo)
2. Every `box` must have a matching `end`
3. Participant IDs must not contain spaces — use `CamelCase` or underscores
4. The `@{ ... }` annotation must use double quotes, not single quotes
5. Check for unclosed strings in message labels

---

**Q: The participant stereotype annotation `@{ "type": "actor" }` breaks rendering. What is wrong?**

Ensure you are using Mermaid v10.6+. Earlier versions do not support participant type annotations. Update your Mermaid library or preview extension.

Verify the syntax matches exactly:
```
participant User@{ "type": "actor" } as Display Name
```
Note: there is a space before `as`. No comma between the annotation and `as`.

---

**Q: My `box` block content is not grouping visually. Why?**

- Ensure participants declared inside the `box ... end` block are not also declared outside it
- Each participant can appear in only one `box` or outside all boxes
- Do not mix declaration styles (some with `as` aliases, some without) inside the same box

---

**Q: Can I use `box` in other Mermaid diagram types (flowchart, class, etc.)?**

No. The `box` syntax is specific to Mermaid `sequenceDiagram`. For other diagram types, use subgraphs (flowchart) or namespaces (class diagrams) as appropriate.

---

**Q: How do I add color to a box?**

The Mermaid `box` syntax accepts an optional color parameter:
```
box blue My System Name
    participant ...
end
```
Supported values: any CSS color name or hex code (e.g., `#eef`, `lightblue`, `rgb(200,220,255)`).

---

### Validation Rules

---

**Q: VR-2 fails even though my `<<UI>>` participant is the first one declared inside the box. Why?**

VR-2 checks message order, not declaration order. The validator scans the sequence of messages and checks that the first message from an external actor that lands inside a box targets a `boundary`-type participant. If you declare `<<UI>>` first but then write a message to `<<System>>` before any message to `<<UI>>`, VR-2 will fail.

---

**Q: I have two actors sending to the same boundary. Does that break VR-1?**

Yes. VR-1 limits each boundary to exactly one external actor interface. If two actors both send directly into the box, you need to restructure. Options:
- Add a `<<UI>>` aggregator at Level 0 that accepts both actors and forwards to one boundary
- Split into two separate boundaries (one per actor)

---

**Q: VR-4 says no actor inside a box, but I need to model a "system-to-system" interaction where system B is external. How?**

If system B is external to the current boundary, it should be modeled as a `control`-type participant outside the box (at the current level), not as an `actor`. Reserve `actor` type for human end-users or truly external third-party systems that you do not control.

---

### Hierarchy & Folder Structure

---

**Q: What naming convention should I use for sub-folders?**

Format: `{nn}-{BoundaryName}` where:
- `nn` is a two-digit zero-padded sequence number (01, 02, 03…)
- `BoundaryName` is the boundary label with spaces replaced by hyphens and special characters removed

Examples: `01-QueryEngine`, `02-EventBus`, `03-DecisionEngine`

---

**Q: Does every `control` participant need a sub-folder?**

No. Create a sub-folder only when you intend to produce a Level N+1 collaboration diagram for that participant. Leave the folder out until you need it — the hierarchy grows on demand.

---

**Q: How do I cross-reference a child diagram from its parent?**

In the parent `collaboration.md`, add a note or comment below the relevant participant:

```markdown
<!-- OrderService is decomposed in: ./01-OrderService/collaboration.md -->
```

In the child `main.md`, link back:
```markdown
**Parent Level**: [E-Commerce Platform](../../collaboration.md)
```

---

## Error Reference

| Error Code / Message | Cause | Resolution |
|---|---|---|
| VR-1: Multiple actor interfaces | More than one actor sends into a box | Restructure to one entry point or split boxes |
| VR-2: Wrong first recipient | Actor's first in-box message targets non-boundary | Move or create a `boundary`-type participant as the first recipient |
| VR-3: Non-control decomposed | A sub-folder exists for a `boundary` or `entity` participant | Remove the sub-folder or reclassify the participant as `control` |
| VR-4: Actor inside box | An `actor`-type participant is declared in a `box` block | Move actor outside the box |
| Mermaid parse error: `box` | Missing `end` keyword or malformed participant annotation | Add `end` after last participant, fix annotation quotes |
| Mermaid: participant not found | Message uses an ID not declared in any `participant` line | Add a `participant` declaration for that ID |

---

## See Also

- [User Guide](user-guide.md) — Modeling methodology overview
- [Participant Type Reference](participant-type-reference.md) — Stereotype quick reference
- [Migration Guide](migration-guide.md) — Upgrade from Project 1
- [Quick-Start Tutorial](quick-start-tutorial.md) — 30-minute onboarding
