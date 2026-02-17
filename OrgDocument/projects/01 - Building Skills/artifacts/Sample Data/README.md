# Test Suite Requirements Samples

This directory contains diverse requirement samples designed to validate the AI Agent Skills system. Each sample targets specific skill validation scenarios and complexity levels.

## Sample Categories

### Domain Diversity
- **Healthcare**: Medical records management system
- **E-commerce**: Online marketplace platform
- **Education**: Learning management system
- **Financial**: Banking transaction system
- **Manufacturing**: Supply chain tracking system

### Complexity Levels
- **Simple**: Basic CRUD operations, single stakeholder
- **Medium**: Multiple stakeholders, moderate business logic
- **Complex**: Enterprise-scale, multiple integrations, regulatory compliance

### Format Variations
- **Narrative**: Prose-style requirements
- **Structured**: Bullet points and numbered lists
- **User Stories**: Agile-style user story format
- **Technical Specs**: API and system specifications
- **Mixed**: Combination of multiple formats

### Validation Targets
Each sample is designed to test specific skills:
- Requirements ingestion and parsing
- Domain concept extraction and alignment
- Goals and success criteria identification
- W5H analysis framework
- Change management traceability
- Scope minimization capabilities

## Usage Instructions

### Quick Start
1. **Follow the step-by-step checklist**: See [test-execution-checklist.md](test-execution-checklist.md) for guided testing
2. **Start with simple samples**: Begin with `simple-todo-app.md` to validate basic skill functionality
3. **Progress to complex samples**: Move to `healthcare-emr.md` and `banking-transactions.md` for comprehensive testing
4. **Use Copilot commands**: Execute tests via `@workspace` commands in VS Code

### Execution Methods
- **Manual Testing**: Use individual Copilot commands for each skill/sample combination
- **Workflow Testing**: Execute complete skill chains for end-to-end validation  
- **Batch Testing**: Follow systematic testing procedures in the validation framework

### Getting Started
```
@workspace Use the requirements-ingest skill to process /artifacts/Sample Data/simple-todo-app.md
```

1. Use samples individually to test specific skill components
2. Run complete test suite to validate end-to-end workflow
3. Compare skill outputs against expected results documented in each sample
4. Use edge cases to test error handling and boundary conditions

## Test Execution Files

- **[test-execution-checklist.md](test-execution-checklist.md)** - Step-by-step testing guide with checkboxes
- **[test-validation-framework.md](test-validation-framework.md)** - Complete testing procedures and automation guidelines

## Sample Inventory

| Sample | Domain | Complexity | Format | Validation Target |
|--------|--------|------------|--------|------------------|
| healthcare-emr | Healthcare | Medium | Narrative | Domain extraction, regulatory compliance |
| ecommerce-marketplace | E-commerce | Complex | Mixed | Multi-stakeholder analysis, scope minimization |
| education-lms | Education | Simple | User Stories | Goals extraction, W5H analysis |
| banking-transactions | Financial | Complex | Technical Specs | Change management, integration analysis |
| manufacturing-supply | Manufacturing | Medium | Structured | Process analysis, dependency mapping |
| simple-todo-app | Generic | Simple | Narrative | Basic skill validation |
| conflicting-requirements | Generic | Medium | Mixed | Error handling, conflict resolution |
| incomplete-requirements | Generic | Simple | Narrative | Gap analysis, assumption identification |
| regulatory-compliance | Healthcare | Complex | Technical Specs | Compliance mapping, risk analysis |
| legacy-modernization | Generic | Complex | Mixed | Migration analysis, integration planning |

## Test Execution Files

| File | Purpose | Usage |
|------|---------|-------|
| test-execution-checklist.md | Step-by-step testing guide | Follow checkboxes for systematic validation |
| test-validation-framework.md | Complete testing framework | Reference for automation and procedures |
| README.md | Test suite overview | Getting started and sample inventory |

## Expected Outcomes

Each sample includes documentation of expected skill outputs to enable automated validation testing.