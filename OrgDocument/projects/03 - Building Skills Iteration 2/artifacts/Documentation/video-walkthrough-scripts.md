# Video Walkthrough Scripts and Storyboards

**Project**: 03-Building-Skills-Iteration-2  
**Version**: 1.0  
**Created**: March 15, 2026  
**Purpose**: Production-ready scripts and visual storyboards for recorded tutorial videos

---

## Overview

Three video walkthroughs are planned. Each is designed to be self-contained and suitable for async viewing (e.g., recorded Loom, Confluence video, or YouTube).

| Video | Title | Audience | Target Duration |
|---|---|---|---|
| V1 | Introduction to Boundaries and Stereotypes | New team members | 8 minutes |
| V2 | Building Your First Hierarchical Diagram | Engineers | 12 minutes |
| V3 | Migrating a Project 1 Diagram | Existing users | 10 minutes |

---

## Video 1 — Introduction to Boundaries and Stereotypes

**Title**: "EDPS Hierarchical Modeling: Boundaries and Stereotypes Explained"  
**Duration**: ~8 minutes  
**Format**: Slides with voiceover; no live coding

---

### Scene 1 — Introduction (0:00–0:45)

**Slide**: Title card — "EDPS Hierarchical Process Modeling"

**Script**:
> "Welcome. In this video, we'll cover the core concepts behind hierarchical process modeling in EDPS: what boundaries are, why we use participant stereotypes, and the four validation rules that keep diagrams consistent. This is the foundation for everything else in the framework."

---

### Scene 2 — Problem with Flat Diagrams (0:45–1:45)

**Slide**: Side-by-side comparison — a cluttered flat diagram (Project 1) vs. a clean Level 1 box diagram (Project 3)

**Script**:
> "Traditional collaboration diagrams show all participants at once. This works fine for small systems but quickly becomes unreadable when a system grows. Imagine trying to understand an e-commerce platform with 15 services all shown on one diagram. You can't tell who does what at a glance."
>
> "Hierarchical modeling solves this by organizing participants into levels. Each level shows only what's relevant at that scope. Internal complexity is hidden until you need it."

---

### Scene 3 — What Is a Boundary? (1:45–3:00)

**Slide**: Boundary diagram with one actor outside and three internal participants inside a `box`

**Script**:
> "A boundary is a named group of participants that together fulfill a shared responsibility. Think of it like a department in a company: external stakeholders interact with the department through one point of contact, and internal staff collaborate inside without being visible to the outside."
>
> "In EDPS, a boundary has exactly one external actor interface — one entry point. Inside the boundary, participants collaborate freely. This encapsulation is what allows each level to stay focused."

---

### Scene 4 — The Four Stereotypes (3:00–5:30)

**Slide**: Table of four stereotypes with icons and descriptions (flip through each)

**Script**:
> "Every participant in a boundary diagram carries a stereotype that tells us its role. There are four:"
>
> "First: Actor. An actor is an external entity — a user, a client application, a partner system. Actors always appear outside all boundary boxes. They initiate interactions but are never decomposed."
>
> "Second: UI, or boundary type. The UI is the door into a boundary. When an actor sends a message into a boundary, the first participant to receive it must be a UI type. Think of it as the customer service desk — it translates external requests into internal vocabulary."
>
> "Third: System, or control type. A System participant contains business logic and can be decomposed into a sub-boundary. If you want to drill deeper, only System participants qualify."
>
> "Fourth: Entity. An Entity is a data store or resource. Databases, caches, configuration registries. They receive read and write requests but do not initiate interactions and are not decomposed."

---

### Scene 5 — The Four Validation Rules (5:30–7:15)

**Slide**: Four rules listed, each with a ✓ and ✗ example

**Script**:
> "To keep diagrams consistent and enforce the boundary contract, four validation rules are applied automatically:"
>
> "VR-1: Only one actor may interact with a boundary. More than one external actor entering the same box breaks the single-interface rule."
>
> "VR-2: The first message from an actor into a boundary must target a UI-type participant. You cannot skip the UI and go directly to a System."
>
> "VR-3: Only System participants may be decomposed into child boundaries. Trying to decompose an Entity or UI participant violates this rule."
>
> "VR-4: Actor types may not appear inside a box. Actors are always external."

---

### Scene 6 — Summary (7:15–8:00)

**Slide**: Summary card

**Script**:
> "To recap: a boundary encapsulates related participants with a single external interface. Each participant has a stereotype — Actor, UI, System, or Entity — that governs its behavior. And four validation rules ensure diagrams remain well-formed across all hierarchy levels."
>
> "In the next video, we'll build a complete two-level hierarchical diagram from scratch. See you there."

---

## Video 2 — Building Your First Hierarchical Diagram

**Title**: "Build a Hierarchical Collaboration Diagram Step by Step"  
**Duration**: ~12 minutes  
**Format**: Screen recording with voiceover; VS Code with Mermaid preview

---

### Scene 1 — Setup (0:00–0:30)

**Screen**: VS Code open with an empty `collaboration.md`

**Script**:
> "In this video, we'll build a two-level hierarchical diagram for an e-commerce 'Place Order' workflow. Open a new file and call it collaboration.md."

---

### Scene 2 — Level 0 Diagram (0:30–3:30)

**Screen**: Typing the Level 0 sequenceDiagram; Mermaid preview updating live

**Script**:
> "We start at Level 0 — the external view. We have three participants: Customer, E-Commerce Platform, and Payment Provider."
>
> "Add the sequenceDiagram header, then declare each participant with its stereotype. Customer is an actor — type 'actor'. E-Commerce Platform and Payment Provider are systems — type 'control'. At Level 0, we don't use the box syntax yet."
>
> [types code live, preview updates]
>
> "Now add the messages. Customer browses, places an order, E-Commerce forwards the payment request to Payment Provider. Preview looks good. Save this as the Level 0 diagram."

---

### Scene 3 — Create Sub-Folder (3:30–4:30)

**Screen**: VS Code explorer panel; creating folder `01-ECommercePlatform/`

**Script**:
> "Now we'll decompose the E-Commerce Platform. Create a sub-folder called 01-ECommercePlatform. The prefix '01' is the sequence number — we use two digits so folders sort correctly."
>
> "Inside the folder, create a new collaboration.md. This will be our Level 1 diagram."

---

### Scene 4 — Level 1 Diagram (4:30–8:30)

**Screen**: Typing the Level 1 diagram with box syntax; preview updates

**Script**:
> "For Level 1, we're inside the E-Commerce Platform. Ask: what components collaborate here?"
>
> "We have: Web Interface (UI type — the entry point), Order Service (control — has business logic), Inventory Service (control — checks stock), and Customer Database (entity — data store)."
>
> "Start with the sequenceDiagram header. Declare the external actor Customer outside the box. Then write the box block: 'box E-Commerce Platform', declare all four internal participants, close with 'end'."
>
> [types code live]
>
> "Now write the messages: Customer to Web Interface first — VR-2 requires the boundary type to receive the first external message. Watch the preview: the box renders with the label, participants are grouped inside."
>
> "Add the internal message chain: WebUI to OrderService, OrderService to InventoryService, Inventory to CustomerDB, return path back to the customer."

---

### Scene 5 — Validate (8:30–10:00)

**Screen**: Running validation check (mental walkthrough or diagram-skill invocation)

**Script**:
> "Before we call this done, check the four rules. VR-1: one actor, Customer, outside the box — check. VR-2: Customer's first message goes to WebUI, which is boundary type — check. VR-3: OrderService and InventoryService are control type, the only candidates for decomposition — check. VR-4: no actor inside the box — check. All four pass."

---

### Scene 6 — Folder Review and main.md (10:00–11:30)

**Screen**: Explorer showing folder tree; typing main.md

**Script**:
> "Here's our folder structure: the parent folder has collaboration.md for the Level 0 diagram, and the child folder has collaboration.md for Level 1."
>
> "Create a main.md in the child folder to describe the boundary's purpose and link back to the parent. This cross-reference is important for navigation as hierarchies grow."

---

### Scene 7 — Summary (11:30–12:00)

**Slide**: Summary card

**Script**:
> "You've built a two-level hierarchical diagram. Level 0 shows the external system view; Level 1 zooms into one boundary. Each level follows the same rules while keeping detail appropriate to its scope."
>
> "In Video 3, we'll take an existing flat Project 1 diagram and migrate it to this style."

---

## Video 3 — Migrating a Project 1 Diagram

**Title**: "Upgrade a Flat Diagram to Hierarchical EDPS Style"  
**Duration**: ~10 minutes  
**Format**: Screen recording with voiceover; before/after comparison

---

### Scene 1 — The Flat Diagram (0:00–1:30)

**Screen**: Project 1-style flat diagram open in preview

**Script**:
> "Here's a typical Project 1 collaboration diagram: all participants listed at the top, messages running left and right with no grouping. It works, but as soon as we add a few more participants it becomes hard to understand system boundaries."
>
> "We're going to upgrade this to a hierarchical boundary-based diagram — step by step, without losing any of the original information."

---

### Scene 2 — Classify Each Participant (1:30–3:30)

**Screen**: Annotation pass over the diagram — highlighting each participant and naming its stereotype

**Script**:
> "First step: classify every participant. For each one, ask: Is it external? Is it an interface? Does it contain business logic? Is it a data store?"
>
> [walks through each participant in the example, naming the stereotype]
>
> "External users become actors. API layers and web interfaces become UI (boundary type). Services and processors become systems (control type). Databases and caches become entities."

---

### Scene 3 — Add Type Annotations (3:30–5:00)

**Screen**: Adding `@{ "type": "..." }` syntax to each participant; preview updates

**Script**:
> "Now add the stereotype annotations. This is non-breaking — the diagram renders identically, just with richer metadata."
>
> [adds annotations one by one]
>
> "Notice the preview updates with the richer participant shapes as the Mermaid renderer picks up the type hints."

---

### Scene 4 — Add Box Groupings (5:00–7:30)

**Screen**: Wrapping participants in box blocks

**Script**:
> "Now group participants into boundary boxes. Identify which participants collaborate on the same responsibility and wrap them in a box."
>
> [adds box blocks]
>
> "Make sure the actor is outside the box and the first message from the actor lands on the UI-type participant. Run through VR-1 through VR-4 quickly."

---

### Scene 5 — Create Sub-Folders for Decomposable Participants (7:30–9:00)

**Screen**: Creating child folders for each control-type participant

**Script**:
> "Now identify control-type participants worth decomposing. For each one, create a numbered sub-folder and a Level N+1 collaboration.md. You don't have to fill them all in today — create the folder as a placeholder to signal intent."

---

### Scene 6 — Summary (9:00–10:00)

**Slide**: Before/after side-by-side

**Script**:
> "Compare before and after. The messages are identical — no information was lost. But now we understand exactly which participants belong to which boundary, who the external interface is, and which components could be decomposed for future detail."
>
> "That's the migration process. Start with classification, add annotations, add boxes, create child folders. Each step is reversible and non-breaking."

---

## Production Notes

### Recording Setup
- Resolution: 1920×1080 minimum  
- Terminal/editor font size: 16pt or larger for code legibility  
- Mermaid preview pane visible alongside code editor at all times  
- Use a quiet background with no notification sounds

### Slide Template
- Background: white  
- Accent color: `#0078d4` (VS Code blue)  
- Font: Segoe UI or system sans-serif  
- Diagrams: embed Mermaid renders as PNG, not live renders

### Captions
All videos should include auto-generated captions reviewed for accuracy. Technical terms (Mermaid, EDPS, VR-1, stereotype) should be manually corrected in caption files.
