# Test Execution Checklist

**Purpose**: Step-by-step checklist for executing AI Agent Skills validation tests  
**Created**: 2026-02-17  
**Usage**: Follow this checklist to systematically validate skills using test samples

## Pre-Test Setup ✅

- [ ] VS Code is open with AI_Slowcooker workspace loaded
- [ ] GitHub Copilot extension is active and authenticated
- [ ] Skills are available in `.github/skills/` directory
- [ ] Test samples are accessible in `artifacts/Sample Data/`
- [ ] Copilot can access workspace files (test with `@workspace`)

## Basic Skill Validation Tests

### Requirements Ingestion Skill Testing

- [ ] **Test Simple Sample**
  ```
  @workspace Use the requirements-ingest skill to process /artifacts/Sample Data/simple-todo-app.md
  ```
  - [ ] Verify requirements are extracted and structured
  - [ ] Check that traceability links are created
  - [ ] Confirm no parsing errors or missing content

- [ ] **Test Complex Sample**  
  ```
  @workspace Use the requirements-ingest skill to process /artifacts/Sample Data/banking-transactions.md
  ```
  - [ ] Verify technical specifications are properly parsed
  - [ ] Check that requirements are categorized correctly
  - [ ] Confirm complex formatting is preserved

- [ ] **Test Mixed Format**
  ```
  @workspace Use the requirements-ingest skill to process /artifacts/Sample Data/ecommerce-marketplace.md
  ```
  - [ ] Verify mixed content (narrative + user stories + technical specs) is handled
  - [ ] Check that different sections are properly identified
  - [ ] Confirm no content is lost in processing

### Domain Concepts Extraction Testing

- [ ] **Healthcare Domain Test**
  ```
  @workspace Apply the domain-extractconcepts skill to the healthcare EMR requirements from /artifacts/Sample Data/healthcare-emr.md
  ```
  - [ ] Verify healthcare entities identified: Patient, Provider, EMR, Medical Record, Insurance
  - [ ] Check regulatory concepts: HIPAA compliance, data sovereignty
  - [ ] Confirm relationships are mapped: Patient-Provider, Appointment-Patient

- [ ] **E-commerce Domain Test**
  ```
  @workspace Apply the domain-extractconcepts skill to /artifacts/Sample Data/ecommerce-marketplace.md
  ```
  - [ ] Verify complex relationships: Manufacturer-Reseller-Customer hierarchy
  - [ ] Check business entities: Product Catalog, Pricing, Commission, Inventory
  - [ ] Confirm integration concepts: EDI, ERP, API endpoints

- [ ] **Simple Domain Test**
  ```
  @workspace Apply the domain-extractconcepts skill to /artifacts/Sample Data/simple-todo-app.md
  ```
  - [ ] Verify basic entities: Task, User, Todo List
  - [ ] Check simple relationships: User owns Todo List, List contains Tasks
  - [ ] Confirm proportionate analysis depth

### Goals Extraction Testing

- [ ] **Clear Goals Test**
  ```
  @workspace Apply the goals-extract skill to analyze business goals in /artifacts/Sample Data/healthcare-emr.md
  ```
  - [ ] Verify primary goal identified: Modernize patient management system
  - [ ] Check success criteria: 30% doc time reduction, 99.5% availability, 15% satisfaction improvement
  - [ ] Confirm constraints: $2.8M budget, 18-month timeline, US data sovereignty

- [ ] **Complex Goals Test**
  ```
  @workspace Apply the goals-extract skill to /artifacts/Sample Data/ecommerce-marketplace.md
  ```
  - [ ] Verify multiple stakeholder goals identified
  - [ ] Check business metrics: $50M GMV, 85% retention, <2 week onboarding
  - [ ] Confirm technical goals: 99.9% uptime, <200ms search response

### W5H Analysis Testing

- [ ] **Comprehensive Analysis Test**
  ```
  @workspace Perform W5H analysis on /artifacts/Sample Data/banking-transactions.md
  ```
  - [ ] Verify Who: Stakeholders and user roles identified
  - [ ] Check What: System capabilities and features covered
  - [ ] Confirm When: Timeline and implementation phases
  - [ ] Verify Where: Deployment and infrastructure context
  - [ ] Check Why: Business drivers and rationale
  - [ ] Confirm How: Technical approach and methodologies

## Advanced Testing

### Error Handling and Edge Cases

- [ ] **Conflict Detection Test**
  ```
  @workspace Analyze /artifacts/Sample Data/conflicting-requirements.md for requirement conflicts
  ```
  - [ ] Verify conflicts are identified and categorized
  - [ ] Check stakeholder mapping for conflict ownership
  - [ ] Confirm resolution guidance is provided

- [ ] **Gap Analysis Test**
  ```
  @workspace Analyze /artifacts/Sample Data/incomplete-requirements.md and identify missing information
  ```
  - [ ] Verify gap identification across all information categories
  - [ ] Check assumption surfacing and documentation
  - [ ] Confirm question generation for information gathering

### End-to-End Workflow Testing

- [ ] **Complete Skills Chain Test**
  ```
  @workspace Execute the complete analysis workflow on /artifacts/Sample Data/healthcare-emr.md:
  1. Requirements ingestion
  2. Domain concept extraction
  3. Goals analysis  
  4. W5H framework analysis
  5. Change management setup
  
  Maintain traceability between all outputs.
  ```
  - [ ] Verify all skills execute successfully
  - [ ] Check data flows correctly between skills
  - [ ] Confirm traceability is maintained
  - [ ] Verify output consistency and quality

### Performance and Quality Validation

- [ ] **Performance Measurement**
  ```
  @workspace Time the execution of each skill on the banking-transactions.md sample and report processing times
  ```
  - [ ] Record processing times for each skill
  - [ ] Verify times are within acceptable bounds
  - [ ] Check memory usage during processing

- [ ] **Quality Assessment**
  ```
  @workspace Evaluate the quality and accuracy of domain analysis on healthcare-emr.md against the expected outcomes documented in the file
  ```
  - [ ] Compare actual vs expected outcomes
  - [ ] Calculate accuracy percentages
  - [ ] Document any deviations or issues

## Test Results Documentation

### Individual Test Results
- [ ] Create test execution log with timestamps
- [ ] Record all skill outputs for comparison
- [ ] Document any errors or unexpected behaviors
- [ ] Note performance measurements

### Summary Report Generation
- [ ] **Generate Test Summary**
  ```
  @workspace Create a comprehensive test validation summary including:
  - Skills tested and samples used
  - Accuracy rates and quality metrics
  - Performance measurements
  - Issues identified and recommendations
  ```
  - [ ] Review summary for completeness
  - [ ] Identify patterns in results
  - [ ] Note areas for improvement

## Post-Test Actions

- [ ] **Archive Test Results**: Save all outputs with timestamps for regression comparison
- [ ] **Update Baselines**: Record performance and quality metrics as new baselines
- [ ] **Document Issues**: Log any bugs or unexpected behaviors for skill improvement
- [ ] **Schedule Regression**: Plan next test execution after skill modifications

## Continuous Testing Setup

- [ ] **Establish Regular Testing**: Schedule weekly skill validation runs
- [ ] **Monitor Performance**: Track skill performance trends over time
- [ ] **Update Test Samples**: Add new samples as use cases evolve
- [ ] **Automate Testing**: Integrate testing into skill development workflow

---

**Execution Notes**:
- Execute tests in sequence to build confidence from simple to complex
- Document all issues for pattern analysis
- Compare results against expected outcomes in each sample
- Focus on end-to-end workflow integrity, not just individual skill performance

**Next Steps After Testing**:
1. Address any identified skill issues or gaps
2. Optimize performance based on measurement results  
3. Expand test coverage with additional samples
4. Implement automated regression testing