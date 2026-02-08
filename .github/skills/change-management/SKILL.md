---
name: change-management
description: Identify, document, and track changes to requirements, processes, and specifications with automated referencing and impact analysis. Converts AI conversation text into structured change documents following established change tracking workflows.
license: MIT
---

# Change Management

Transforms AI conversation text and requirement discussions into structured change documents with automatic classification, impact analysis, and reference updates.

## Core Function

**Input**: Conversation text + project context + change scope  
**Output**: Structured change document + affected file list + reference updates

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing conversation text that contains requirement changes.
Copilot will automatically identify changes, classify them, and generate proper documentation.

Example prompt:
"Use change-management skill to analyze this conversation for requirement changes and create proper change documentation with impact analysis and reference updates."
```

**Traditional Script Approach:**
```python
from change_management import ChangeProcessor
processor = ChangeProcessor()
result = processor.process_conversation(text=conversation_text, project_id="PRJ-001")
```

## Output Schema

ALWAYS return exactly this JSON structure:

```json
{
  "project_id": "string",
  "changes_identified": [
    {
      "change_id": "PROC-CHG-001", 
      "change_type": "REQ-CHG|REQ-ADD|REQ-REM|SCOPE-CHG|PROC-CHG",
      "title": "Brief description for filename",
      "summary": "One-line change summary",
      "priority": "Low|Medium|High|Critical",
      "status": "Proposed",
      "rationale": "Why this change is needed",
      "current_state": "Description of current requirement/process",
      "proposed_state": "Description after change",
      "impact_analysis": {
        "affected_documents": [
          {
            "file_path": "relative/path/to/file.md",
            "impact_description": "How this file is affected",
            "update_required": true
          }
        ],
        "affected_tasks": [
          {
            "task_id": "T2",
            "impact_description": "How this task is affected"
          }
        ],
        "risk_level": "Low|Medium|High",
        "estimated_effort": "X hours/days"
      }
    }
  ],
  "reference_updates": [
    {
      "file_path": "relative/path/to/file.md",
      "section": "Related Changes",
      "new_reference": "- [PROC-CHG-001](../artifacts/Changes/2026-02-08-PROC-CHG-001-title.md) - Description"
    }
  ],
  "next_actions": [
    "Action item 1",
    "Action item 2"
  ]
}
```

## GitHub Copilot Integration

### Direct Usage in Copilot Chat
Paste your conversation or discussion text and ask:

```
@workspace Use the change-management skill to process this conversation:

[PASTE CONVERSATION TEXT HERE]

Project ID: AI-SLOWCOOKER-001
Context: Building Skills project

Identify requirement changes and:
- Classify change types (REQ-CHG, PROC-CHG, etc.)
- Generate impact analysis
- Create proper change documentation
- Identify files needing reference updates
- Suggest next actions

Return structured JSON following the schema.
```

### Copilot Prompt Template
```
Analyze conversation using change-management methodology:

1. IDENTIFY: Scan for explicit/implicit requirement changes
2. CLASSIFY: Categorize as REQ-CHG|REQ-ADD|REQ-REM|SCOPE-CHG|PROC-CHG
3. ANALYZE: Assess impact on documents, tasks, orgModel files
4. DOCUMENT: Generate structured change document content
5. REFERENCE: Identify files needing reference updates

Output exact JSON schema with changes_identified, reference_updates, next_actions.
```

## Classification Rules

### Change Types
- **REQ-CHG**: Modifications to existing requirements
- **REQ-ADD**: New requirements added to project scope
- **REQ-REM**: Requirements removed or marked obsolete  
- **SCOPE-CHG**: Project scope adjustments (budget, timeline, deliverables)
- **PROC-CHG**: Development process or workflow modifications

### Priority Assessment
- **Critical**: Blocks progress, affects core functionality
- **High**: Significant impact on project deliverables
- **Medium**: Moderate impact, can be scheduled normally
- **Low**: Minor impact, can be deferred

### Risk Levels
- **Low**: Minimal impact, easy implementation
- **Medium**: Some complexity, moderate impact
- **High**: Significant impact, complex implementation

## Processing Rules

1. **Change Detection**: Identify explicit statements ("we need to change") and implicit changes ("actually, it should...")
2. **Context Awareness**: Consider project phase, existing constraints, stakeholder roles
3. **Impact Analysis**: Evaluate effects on requirements, tasks, process models, timeline
4. **Traceability**: Maintain links between changes and affected components
5. **File Naming**: Generate proper filename using format `YYYY-MM-DD-{TYPE}-{ID}-{title}.md`

## Reference Path Patterns

- **From Tasks to Changes**: `../artifacts/Changes/`
- **From OrgModel to Changes**: `../../projects/{project-name}/artifacts/Changes/`
- **From Project Root to Changes**: `artifacts/Changes/`

## Quality Checks

1. **Change ID Uniqueness**: Ensure sequential IDs don't conflict
2. **Impact Completeness**: Verify all affected files identified
3. **Reference Accuracy**: Check path correctness for different file locations
4. **Documentation Standards**: Follow established template structure
5. **Status Consistency**: Align status with approval workflow

## Integration Points

- **Requirements Ingest**: Changes may trigger re-ingestion of modified requirements
- **Task Planning**: New changes may spawn additional tasks or modify existing ones
- **Status Reporting**: Changes feed into project status and progress tracking
- **Document Management**: Changes integrate with overall project documentation structure

## AI Conversation Patterns

### Detection Signals
- "We need to change..." / "Actually, we should..."
- "I think the requirement should be..." / "Let me clarify..."
- "Instead of X, we need Y..." / "This doesn't work because..."
- "Add to the scope..." / "Remove from the scope..."
- "The process should..." / "Our workflow needs..."

### Context Clues
- Reference to existing requirement documents
- Discussion of implementation challenges
- Stakeholder feedback incorporation  
- Technical constraint discoveries
- Business priority adjustments

## File Generation

The skill generates change documents following this template structure:

```markdown
# Change Title

**Change ID**: {TYPE}-{###}  
**Date Created**: {YYYY-MM-DD}  
**Status**: Proposed  
**Priority**: {Level}  
**Requested By**: [Extracted from context]

## Summary
{One-line description}

## Change Details
{Detailed description extracted from conversation}

### Current State
{Current situation description}

### Proposed State  
{Desired future state}

### Rationale
{Why change is needed}

## Impact Analysis
{Generated impact assessment}

## Implementation Plan
{Suggested implementation steps}

## Acceptance Criteria
{Generated success criteria}
```