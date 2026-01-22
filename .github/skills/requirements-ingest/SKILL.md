---
name: requirements-ingest
description: Normalize requirements from any format into consistent, chunked representation with traceability and classification.
license: MIT
---

# Requirements Ingest

Transforms requirements documents (PDF/DOCX/Markdown/Email) into structured, atomic chunks with classification and traceability.

## Core Function

**Input**: Raw files + project_id
**Output**: JSON with chunked requirements, each tagged and traceable to source

## Usage

**GitHub Copilot Integration (Recommended):**
```markdown
Use this skill directly in Copilot by providing requirements documents.
Copilot will automatically extract and classify requirements using its built-in AI.

Example prompt:
"Use requirements-ingest skill to process this requirements document and return structured JSON with atomic requirements, classifications, and traceability."
```

**Traditional Script Approach:**
```python
from requirements_ingest import RequirementsIngestor
ingestor = RequirementsIngestor()
result = ingestor.process_files(files=["requirements.pdf"], project_id="PRJ-001")
```

## Output Schema

ALWAYS return exactly this JSON structure:

```json
{
  "project_id": "string",
  "requirements": [
    {
      "id": "R-001",
      "source_file": "requirements.pdf",
      "location_hint": "page 3, para 2",
      "text": "The system shall authenticate users within 2 seconds",
      "tags": ["functional", "performance"],
      "confidence": 0.95
    }
  ],
  "glossary_suspects": ["authentication", "API", "dashboard"]
}
```

## GitHub Copilot Integration

### Direct Usage in Copilot Chat
Simply paste your requirements document and ask:

```
@workspace Use the requirements-ingest skill to process this document:

[PASTE YOUR REQUIREMENTS DOCUMENT HERE]

Project ID: MY-PROJECT-001

Extract atomic requirements with:
- Unique IDs (R-XXX format)  
- Source traceability
- Classification tags
- Confidence scores
- Glossary terms

Return structured JSON following the schema.
```

### Copilot Prompt Template
```
Analyze requirements document using requirements-ingest methodology:

1. EXTRACT: Break into atomic requirements (max 200 tokens each)
2. CLASSIFY: Tag as functional|nonfunctional|constraint|assumption|out-of-scope  
3. TRACE: Preserve source location (section, page, paragraph)
4. SCORE: Confidence 0.0-1.0 based on clarity
5. GLOSSARY: Identify domain terms (2+ occurrences)

Output exact JSON schema with project_id, requirements array, glossary_suspects.
```

**Advantages of Copilot Integration:**
- ✅ **No API Keys Required**: Uses Copilot's built-in AI capabilities
- ✅ **Context Aware**: Understands your workspace and project context  
- ✅ **Interactive**: Can ask follow-up questions and refine results
- ✅ **Integrated Workflow**: Works seamlessly with your development process

## AI Classification Prompt

```
Classify each requirement using these tags:

- **functional**: What the system does (features, user actions, behaviors)
- **nonfunctional**: How well it does it (performance, security, usability)
- **constraint**: External limitations (budget, technology, regulations)
- **assumption**: Dependencies and prerequisites
- **out-of-scope**: Explicitly excluded items

Multiple tags allowed. Explain reasoning for complex cases.
```

## Processing Rules

1. **Chunk Size**: Max 200 tokens per requirement  
2. **Atomic**: One verifiable requirement per chunk
3. **Traceability**: Preserve source file + location hint
4. **Confidence**: 0.0-1.0 based on clarity and context