# Document Tree Building Guidelines

This workspace organizes documents using a hierarchical folder structure to describe an organization's business requirements and analysis/design document for application development. Follow these guidelines to maintain consistency and clarity:

## 1. File Structure

```
root/
├── LICENSE                     # MIT license
├── README.md                   # This file
├── projects/                   # Root folder for projects
│   ├── 01 - project               # Folder for project 1
│   │   ├── requirements/       # Folder for project 1 requirements files
│   │   └── artifacts/          # Folder for the artifacts generated during the analysis. There can be sub-folders folders (e.g., `Analysis`, `Requirement`, `Sample Data`, `UI Mockup`) are for storing supporting materials and references.
│   └── projects.md             # Projects Id and name mapping
├── orgModel/                   # Folder for modeling documents
│   ├── 01 - process/              # Sub Process folder for "process 1"
│   │   ├── main.md             # Main documentation of each sub-folder or process. It should provide an overview of the folder's purpose and link to related documents or subfolders.
│   │   ├── process.md          # Mermaid Activity Diagram, should describe step-by-step procedures, workflows, or business logic.
│   │   ├── collaboration.md    # Mermaid sequence diagram to describe the collaborations among the indentified entities. It drives the next level process breakdowns.
│   │   ├── domain-model.md     # Contains identified actors, systems, entities in the scope of current level process, and also their relationships
│   │   ├── vocabulary.md       # vocabulary mapping for canonical names and its variants identified during the analysis
│   │   └── test-cases/         # Test cases generated to verify the process implmenentation
│   ├── main.md                 # 
│   ├── process.md              # 
│   ├── collaboration.md        # 
│   ├── domain-model.md         # 
│   ├── vocabulary.md           # 
│   └── test-cases/             # 
└── examples/                   #
    └── usage_examples.md       # Examples and use cases
```

## 2. Naming Conventions
- Use clear, descriptive folder and file names. Prefix folders with numbers to indicate sequence/order.
- Avoid spaces in file names; use spaces in folder names only for clarity.
- For versioned documents, append version info (e.g., `Job Design Tool - Basic Parts R2.pptx`).

## 3. Adding New Content
- Create a new numbered folder for each new process phase or activity.
- Add `main.md`, `process.md`, and `collaboration.md` as needed.
- Store supporting documents in appropriate artifact subfolders.

## 4. General Tips
- Keep documentation up to date and well-linked.
- Use Markdown for all documentation files for easy readability and version control.
- Store all process-related files within their respective folders for easy navigation.

## 5. organization Document Identifier Numbering
- Purpose: Standardize the `Identifier` comment at the top of each Markdown file so it encodes document type and hierarchical location consistently.
- Format: `<Type>-NN[-NN[-NN[...]]]` where each `NN` is a two‑digit decimal segment taken from the folder prefixes in the document's path.
- Type Prefix:
  - `I`: Main document (`main.md`)
  - `P`: Process document (`process.md`)
  - `C`: Collaboration document (`collaboration.md`)
  - `D`: Domain model (`domain-model.md`)
  - `V`: Vocabulary (`vocabulary.md`)
- Segment Source: Use the numeric prefixes from ancestor folders, in order from root to leaf. Always use decimal with leading zeros (e.g., `01`, `02`, `10`), never hexadecimal (avoid `0a`).

### Examples
- OrgModel folder:
  - File: [orgModel/04 - Cementing Service Request/main.md](orgModel/04%20-%20Cementing%20Service%20Request/main.md)
  - Identifier: `I-04`
- Second level activity:
  - File: [orgModel/04 - Cementing Service Request/09 - Prepare Material/main.md](orgModel/04%20-%20Cementing%20Service%20Request/09%20-%20Prepare%20Material/main.md)
  - Identifier: `I-04-09`
- Third level activity:
  - File: [orgModel/04 - Cementing Service Request/09 - Prepare Material/05 - Blend Approval Process/main.md](orgModel/04%20-%20Cementing%20Service%20Request/09%20-%20Prepare%20Material/05%20-%20Blend%20Approval%20Process/main.md)
  - Identifier: `I-04-09-05`
- Deep leaf process:
  - File: [orgModel/04 - Cementing Service Request/09 - Prepare Material/05 - Blend Approval Process/11 - Document Update/process.md](orgModel/04%20-%20Cementing%20Service%20Request/09%20-%20Prepare%20Material/05%20-%20Blend%20Approval%20Process/11%20-%20Document%20Update/process.md)
  - Identifier: `P-04-09-05-11`

### Special Cases
- Root overview files (no numbered folder):
  - [orgModel/main.md](Documents/main.md) → `I`
  - [orgModel/process.md](Documents/process.md) → `P`
  - [orgModel/collaboration.md](Documents/collaboration.md) → `C`
  - [orgModel/domain-model.md](Documents/domain-model.md) → `D`
  - [orgModel/vocabulary.md](Documents/vocabulary.md) → `V`
- Multiple leaf documents in the same folder: If a folder contains more than one `main.md`-like document that must be distinguished, append a final two‑digit sequence: `I-XX-YY-01`, `I-XX-YY-02`, etc. Prefer a single `main.md` per folder when possible.

### Consistency Rules
- Always derive identifier segments directly from folder number prefixes.
- Use hyphens between type and segments, and between segments.
- Keep segments decimal with leading zeros; do not mix formats (`10` not `0a`).
- Update any legacy identifiers to match these rules when editing affected files.