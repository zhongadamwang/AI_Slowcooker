# Document Tree Building Guidelines

This workspace organizes documents using a hierarchical folder structure to describe an organization's business requirements and analysis/design document for application development. Follow these guidelines to maintain consistency and clarity:

## 1. File Structure

```
orgDocument/
├── LICENSE                     # MIT license
├── instructions.md                   # This file
├── projects/                   # Root folder for projects
│   ├── NN - [project name]               # Folder for project NN
│   │   ├── requirements/       # Folder for project NN requirements files
│   │   ├── artifacts/          # Folder for the artifacts generated during the analysis. There can be sub-folders folders (e.g., `Analysis`, `Requirement`, `Sample Data`, `UI Mockup`) are for storing supporting materials and references.
│   │   └── tasks/             # Individual task files in GitHub issue format for team collaboration
│   └── projects.md             # Projects Id and name mapping
├── orgModel/                   # Folder for modeling documents
│   ├── NN - Process Name/           # Sub Process folder for sub-process "NN - Process Name" definined in collaboration.md of root orgModel folder
│   │   ├── main.md             # Main documentation of each sub-folder or process. It should provide an overview of the folder's purpose and link to related documents or subfolders.
│   │   ├── process.md          # Mermaid Activity Diagram, should describe step-by-step procedures, workflows, or business logic.
│   │   ├── collaboration.md    # Mermaid sequence diagram to describe the collaborations among the indentified entities. It drives the next level process breakdowns.
│   │   ├── domain-model.md     # Contains identified actors, systems, entities in the scope of current level process, and also their relationships
during the analysis
│   │   ├── test-case-list.md   # Lists test cases for the current process level, with metadata for each test case (master list with ID, Title, Type, Priority, Status)
│   │   ├── NN - Sub-Process Name/   # Sub-process folder for "NN - Sub-Process Name" defined in collaboration.md of parent folder
│   │   └── test-cases/         # Test cases generated to verify the process implmenentation
│   │       └── tc-[identifier]-[3-digit-sequence].md  # Individual test case files
│   ├── main.md                 # Root level main documentation
│   ├── process.md              # root level Mermaid Activity Diagram
│   ├── collaboration.md        # root level Mermaid sequence diagram
│   ├── domain-model.md         # root level domain model
│   ├── vocabulary.md           # root level vocabulary mapping canonical names and their variants identified during the analysis
│   ├── test-case-list.md       # root level test case list
│   └── test-cases/             # root level test cases folder
└── examples/                   #
    └── usage_examples.md       # Examples and use cases
```
### Summary of Key Files and Folders
- `projects/`: Root folder for all projects. Each project has its own numbered folder containing requirements and artifacts.
- `projects.md`: Lists project identifiers and names, mapping them to their respective folders.
- `artifacts/`: Contains supporting materials and references generated during analysis, organized into subfolders as needed (e.g., Analysis, Requirements, Sample Data, UI Mockups). These subfolders help keep related documents together for easy access. The naming of these subfolders should reflect their content clearly. There is no strict requirement to number these artifact subfolders and filenames.
- `tasks/`: Contains individual task files formatted as GitHub issues to enable seamless integration with GitHub's issue tracking system. Task files follow T##-task-name.md naming convention and include clear acceptance criteria, dependencies, and effort estimates.
- `orgModel/`: It is the root folder that contains modeling documents for processes, including main documentation, process diagrams, collaboration diagrams, domain models, and vocabulary mappings.
- `main.md`: Provides an overview of the folder's purpose and links to related documents or subfolders.
- `process.md`: Contains Mermaid Activity Diagrams describing workflows or business logic.  
- `collaboration.md`: Contains Mermaid sequence diagrams illustrating collaborations among identified entities.
- `domain-model.md`: Lists identified actors, systems, entities, and their relationships within the scope of the current process.
- `vocabulary.md`: Maps canonical names and their variants identified during analysis.  
- `test-case-list.md`: Lists test cases for the current process level, with metadata for each test case (master list with ID, Title, Type, Priority, Status). Located at process folder level alongside main.md.
- `test-cases/`: Contains test cases generated to verify current process implementation. Includes individual test case files named `tc-[identifier]-[3-digit-sequence].md`.
- `<number> - <name>/`: Numbered folders for processes or sub-processes, indicating sequence/order. This structure can be nested to represent hierarchical process breakdowns. Each sub-process folder follows the same structure as its parent. The sub-process folder is dervied from the `collaboration.md` of its parent process.

## 2. Naming Conventions
- Use clear, descriptive folder and file names. Prefix folders with numbers to indicate sequence/order.
- Avoid spaces in file names; use spaces in folder names only for clarity.
- Use lowercase letters and hyphens for file names (e.g., `main.md`, `process.md`).

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
  - `T`: Test cases list document (`test-case-list.md`)
  - `PRJ`: Project documents (projects folder)
  - `ART`: Artifact documents (within projects/artifacts subfolders)
  - `TASK`: Individual task files (within projects/tasks subfolders, uses T##-task-name.md format)
- Segment Source: Use the numeric prefixes from ancestor folders, in order from root to leaf. Always use decimal with leading zeros (e.g., `01`, `02`, `10`), never hexadecimal (avoid `0a`).

### Projects Integration Rules
- Project identifiers follow format: `PRJ-NN` where NN matches the project folder number
- Artifact files use: `ART-NN-[subfolder-type]` (e.g., `ART-01-Analysis`, `ART-01-Requirements`)
- Task files use: `T##-task-name.md` format aligned with project plan task numbering
- Project documents link to orgModel processes using cross-references
- projects.md format: `PRJ-NN, Project Description, Folder Path, Related OrgModel Process`



### Examples
- Projects folder:
  - File: [projects/01 - project/requirements/requirement1.pdf](projects/01%20-%20project/requirements/requirement1.pdf)
  - Identifier: `<Type>-NN`
- projects.md file:
  - File: [projects/projects.md](projects/projects.md)
  - Identifier: `project list`
  - format: Project Identfier, Project Description, Project folder path mapping (e.g., 'PRJ-01, Cementing Service Request, projects/01 - Cementing Service Request')
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
- Test cases list:
  - File: [orgModel/04 - Cementing Service Request/09 - Prepare Material/test-case-list.md](orgModel/04%20-%20Cementing%20Service%20Request/09%20-%20Prepare%20Material/test-case-list.md)
  - Identifier: `T-04-09`
- Individual test case:
  - File: [orgModel/04 - Cementing Service Request/09 - Prepare Material/test-cases/tc-04-09-001.md](orgModel/04%20-%20Cementing%20Service%20Request/09%20-%20Prepare%20Material/test-cases/tc-04-09-001.md)
  - Identifier: `tc-04-09-001`
- Project task files:
  - File: [projects/01 - Building Skills/tasks/T1-skill-framework-setup.md](projects/01%20-%20Building%20Skills/tasks/T1-skill-framework-setup.md)
  - Format: T##-task-name.md (aligned with project plan task numbering)

### Special Cases
- Root overview files (no numbered folder):
  - [orgModel/main.md](orgModel/main.md) → `I`
  - [orgModel/process.md](orgModel/process.md) → `P`
  - [orgModel/collaboration.md](orgModel/collaboration.md) → `C`
  - [orgModel/domain-model.md](orgModel/domain-model.md) → `D`
  - [orgModel/vocabulary.md](orgModel/vocabulary.md) → `V`
  - [orgModel/test-case-list.md](orgModel/test-case-list.md) → `T`
- Multiple leaf documents in the same folder: If a folder contains more than one `main.md`-like document that must be distinguished, append a final two‑digit sequence: `I-XX-YY-01`, `I-XX-YY-02`, etc. Prefer a single `main.md` per folder when possible.

### Test Cases Organization
- Each process folder contains both `test-case-list.md` (at process level) and a `test-cases/` subfolder.
- `test-case-list.md`: Master list at process folder level containing test case metadata (ID, Title, Type, Priority, Status). Identifier derived from parent process by replacing type prefix with 'T' (e.g., if process main.md has `I-04-09`, test-case-list.md has `T-04-09`).
- Individual test case files: Located in `test-cases/` subfolder, named `tc-[identifier]-[3-digit-sequence].md` (e.g., `tc-04-09-001.md`, `tc-04-09-002.md`).
- **Workflow**: 
  1. Create entry in `test-case-list.md` with unique identifier
  2. Create corresponding file in `test-cases/` subfolder
  3. Link from master list to individual test case file
- Test cases inherit the hierarchical numbering from their containing process folder.

### Consistency Rules
- Always derive identifier segments directly from folder number prefixes.
- Use hyphens between type and segments, and between segments.
- Keep segments decimal with leading zeros; do not mix formats (`10` not `0a`).
- Update any legacy identifiers to match these rules when editing affected files.

### Validation Checklist
- **Before creating new documents**:
  - [ ] Folder numbering follows sequential order
  - [ ] Identifier matches folder hierarchy exactly
  - [ ] test-case-list.md exists before creating individual test cases
  - [ ] Cross-references use relative paths
- **After document creation**:
  - [ ] Document identifier matches file location
  - [ ] All links resolve correctly
  - [ ] File follows naming conventions
  - [ ] Document appears in relevant master lists
- **Common Issues**:
  - Missing leading zeros in identifiers
  - Inconsistent test case file locations
  - Broken links after folder restructuring
  - Missing entries in projects.md or test-case-list.md

### Validation Checklist
- **Before creating new documents**:
  - [ ] Folder numbering follows sequential order
  - [ ] Identifier matches folder hierarchy exactly
  - [ ] test-case-list.md exists before creating individual test cases
  - [ ] Cross-references use relative paths
- **After document creation**:
  - [ ] Document identifier matches file location
  - [ ] All links resolve correctly
  - [ ] File follows naming conventions
  - [ ] Document appears in relevant master lists
- **Common Issues**:
  - Missing leading zeros in identifiers
  - Inconsistent test case file locations
  - Broken links after folder restructuring
  - Missing entries in projects.md or test-case-list.md

### Version Control Guidelines
- **Commit Message Format**: `[Type] Brief description of changes`
  - Types: `[DOC]` documentation, `[PROC]` process changes, `[TEST]` test cases, `[REF]` refactoring
  - Example: `[DOC] Add test case tc-04-09-001 for material preparation`
- **Branch Strategy**: 
  - `main`: Stable documentation
  - `feature/process-name`: New process development
  - `update/identifier`: Updates to existing documents
- **File Types Coverage**:
  - `.md` files: Use identifier system as specified
  - `.pdf`, `.docx`, `.pptx`: Use descriptive names with process context (e.g., `requirements-04-09.pdf`)
  - Images: Use format `img-[process-id]-[sequence].png` (e.g., `img-04-09-001.png`)
  - All files should include process context in naming for traceability

### Cross-Referencing
- When referencing other documents, use relative paths to maintain link integrity.
- **Same folder**: `[See Process Document](process.md)`
- **Parent folder**: `[See Parent Main](../main.md)`
- **Sibling process**: `[See Other Process](../05%20-%20Other%20Process/main.md)`
- **Test cases**: `[See Test Cases](test-cases/tc-04-09-001.md)`
- **Project artifacts**: `[See Requirements](../../projects/01%20-%20Project/artifacts/Requirements/req-001.md)`
- **Cross-level**: `[See Root Process](../../process.md)`
- Ensure that all links are updated if files are moved or renamed.
- Use encoded spaces (%20) in URLs for folders with spaces.
- Maintain a link validation checklist when restructuring folders.