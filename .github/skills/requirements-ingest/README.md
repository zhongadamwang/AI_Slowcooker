# Requirements Ingest Skill

A comprehensive skill for normalizing requirements from multiple file formats into structured, atomic chunks with classification and traceability. **Now featuring AI-powered processing for superior accuracy.**

## Quick Start

1. **GitHub Copilot Integration (Recommended - No API Keys!):**
   ```
   @workspace Use requirements-ingest skill to process this document:
   [PASTE REQUIREMENTS HERE]
   
   Project ID: MY-PROJECT
   Return structured JSON with atomic requirements and classifications.
   ```

3. **Traditional Script (Batch Processing):**
   ```python
   from src.requirements_ingest import RequirementsIngestor
   
   ingestor = RequirementsIngestor()
   result = ingestor.process_files(["specs.pdf"], "MY-PROJECT")
   ```

## Features

### 🤖 GitHub Copilot Integration (New!)
- **No API Keys Required**: Uses Copilot's built-in AI capabilities
- **Context Aware**: Understands your workspace and project context
- **Interactive Processing**: Refine results through conversation
- **Integrated Workflow**: Works seamlessly within VS Code
- **Cost Effective**: No additional API costs beyond Copilot subscription

### 📝 Traditional Script Processing  
- **Multi-format Support**: PDF, DOCX, Markdown, Email, Plain Text
- **Atomic Chunking**: Breaks requirements into verifiable units (<200 tokens)
- **Rule-based Classification**: Tags as functional/nonfunctional/constraint/assumption/out-of-scope
- **Traceability**: Preserves source file and location references
- **Batch Processing**: High-volume processing for consistent formats

## Output Format

```json
{
  "project_id": "string",
  "requirements": [
    {
      "id": "R-001",
      "source_file": "requirements.pdf",
      "location_hint": "page 3, para 2", 
      "text": "System shall authenticate users within 2 seconds",
      "tags": ["functional", "nonfunctional"],
      "confidence": 0.95
    }
  ],
  "glossary_suspects": ["authentication", "API", "system"]
}
```

## File Structure

```
requirements-ingest/
├── SKILL.md                    # Skill definition with Copilot integration guide
├── LICENSE                     # MIT license
├── README.md                   # This file
├── requirements.txt            # Python dependencies (minimal)
├── setup.py                    # Setup script
├── src/
│   └── requirements_ingest.py  # Traditional script for batch processing
├── examples/
│   └── copilot_integration.md  # Copilot usage examples (primary method)
├── test_data/                  # Sample requirement documents
└── test_skill.py               # Comprehensive test suite
```

## Dependencies

### For GitHub Copilot Integration (Primary)
- **No dependencies required!** Works with your existing Copilot subscription

### For Traditional Script Processing  
- `pdfplumber` - PDF text extraction
- `python-docx` - DOCX processing  
- `PyPDF2` - Alternative PDF parser

Install with: `pip install -r requirements.txt`

## Testing

### Comprehensive Testing  
```bash
# Full test suite with Copilot guidance and traditional script validation
python test_skill.py
```

### Test with Sample Data
```bash
# Traditional processing with provided samples
python src/requirements_ingest.py SAMPLE-001 test_data/*.md test_data/*.txt

# Copilot integration (paste content into Copilot Chat)
# See examples/copilot_integration.md for detailed examples
```

### Manual Testing
```python
# Test traditional approach
from src.requirements_ingest import RequirementsIngestor
ingestor = RequirementsIngestor() 
result = ingestor.process_files(["your_file.pdf"], "TEST-001")

# Test Copilot approach
# Use Copilot Chat: "@workspace Use requirements-ingest skill to process this document:"
```

## Classification Rules

- **Functional**: System behavior, user actions, features
- **Nonfunctional**: Performance, security, usability
- **Constraint**: Budget, technology limits, regulations
- **Assumption**: Dependencies, prerequisites, environment
- **Out-of-scope**: Explicitly excluded items

## Quality Assurance

- Chunks are atomic (one requirement each)
- Maximum 200 tokens per chunk
- Location hints specify source context
- Confidence scores indicate text clarity
- Glossary terms appear 2+ times in text

## License

MIT License - see [LICENSE](LICENSE) file for details.