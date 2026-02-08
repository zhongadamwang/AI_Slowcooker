# Requirements Ingest - Output Structure & Guidelines

## Folder Structure

```
outputs/
├── projects/                           # Project-based organization
│   ├── {project_id}/                   # Individual project folder
│   │   ├── requirements.json           # 🎯 Main output for downstream skills
│   │   ├── processing_log.json         # Processing metadata & audit trail
│   │   ├── glossary.json              # Extracted domain terms
│   │   ├── source_files/              # Source file references & copies
│   │   │   ├── file_mapping.json      # Source file tracking
│   │   │   └── originals/             # Optional: source file copies
│   │   └── versions/                  # Version history (optional)
│   │       ├── v1_2026-02-08_14-30.json
│   │       └── v2_2026-02-08_15-45.json
│   └── another_project_id/
├── templates/                         # Standard templates
│   ├── requirements_schema.json      # JSON schema validation
│   └── processing_template.json      # Processing log template
└── README.md                         # Output folder documentation
```

## File Specifications

### 1. `requirements.json` - Primary Output
**Purpose**: Main file for downstream skill consumption
**Schema**: Standard requirements format
```json
{
  "project_id": "PROJECT-001",
  "generated_at": "2026-02-08T14:30:00Z",
  "version": "1.0",
  "total_requirements": 25,
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
  "glossary_suspects": ["authentication", "API", "system"],
  "processing_summary": {
    "files_processed": 3,
    "requirements_extracted": 25,
    "avg_confidence": 0.87,
    "processing_time_seconds": 2.5
  }
}
```

### 2. `processing_log.json` - Audit Trail
**Purpose**: Processing metadata, errors, and audit information
```json
{
  "project_id": "PROJECT-001",
  "processing_session": {
    "timestamp": "2026-02-08T14:30:00Z",
    "version": "1.0",
    "tool_version": "requirements-ingest-v2.1",
    "user": "adam.wang",
    "method": "copilot" // or "traditional_script"
  },
  "input_files": [
    {
      "file_path": "spec.pdf",
      "file_size": 1024000,
      "file_hash": "sha256:abc123...",
      "processed_successfully": true,
      "requirements_extracted": 12
    }
  ],
  "processing_stats": {
    "total_files": 3,
    "successful_files": 3,
    "failed_files": 0,
    "total_requirements": 25,
    "avg_confidence": 0.87,
    "processing_time_seconds": 2.5
  },
  "errors": [],
  "warnings": [
    "Low confidence requirement R-015 (0.45)"
  ]
}
```

### 3. `glossary.json` - Domain Terms
**Purpose**: Extracted glossary for domain modeling
```json
{
  "project_id": "PROJECT-001",
  "extracted_terms": [
    {
      "term": "authentication",
      "frequency": 8,
      "contexts": ["user authentication", "API authentication"],
      "confidence": 0.92
    }
  ],
  "suggested_definitions": [
    {
      "term": "OAuth2",
      "suggested_definition": "Industry standard authorization protocol",
      "sources": ["R-001", "R-007"]
    }
  ]
}
```

## File Naming Conventions

### Project IDs
- **Format**: `PROJ-YYYYMMDD-NNN` or custom identifiers
- **Examples**: `PROJ-20260208-001`, `ECOM-PHASE1`, `USER-AUTH-REQ`

### Versioning
- **Format**: `v{major}_{YYYY-MM-DD}_{HH-mm}`
- **Examples**: `v1_2026-02-08_14-30.json`

### File Names
- **Requirements**: `requirements.json` (fixed name for downstream tools)
- **Logs**: `processing_log.json`
- **Glossary**: `glossary.json`
- **Versions**: `v{version}_{timestamp}.json`

## Downstream Integration Guidelines

### For Skills Consuming Output
1. **Standard Path**: `outputs/projects/{project_id}/requirements.json`
2. **Validation**: Use JSON schema in `templates/requirements_schema.json`
3. **Error Handling**: Check `processing_log.json` for warnings/errors
4. **Glossary Access**: `glossary.json` for domain terms

### File Access Patterns
```python
# Standard downstream access pattern
def load_requirements(project_id: str):
    base_path = f"outputs/projects/{project_id}"
    
    # Primary requirements
    requirements_file = f"{base_path}/requirements.json"
    
    # Optional: Check processing status
    log_file = f"{base_path}/processing_log.json"
    
    # Optional: Access glossary
    glossary_file = f"{base_path}/glossary.json"
    
    return load_json(requirements_file)
```

## Directory Management

### Auto-Creation
- Create `outputs/projects/{project_id}/` if not exists
- Create subdirectories as needed
- Handle permissions appropriately

### Backup Strategy
- Previous versions moved to `versions/` folder
- Keep last 5 versions by default
- Option to disable versioning for space

### Cleanup Policy
- Archive projects older than 90 days (configurable)
- Compress archived projects
- Clean empty directories

## Configuration Options

### Output Location
- **Default**: `./outputs/` (relative to execution directory)
- **Environment Variable**: `REQUIREMENTS_OUTPUT_DIR`
- **Config File**: `config.json` in skill directory

### Processing Options
- **Versioning**: enabled/disabled
- **Source File Copying**: enabled/disabled
- **Compression**: enabled for archives
- **Validation**: JSON schema validation on/off